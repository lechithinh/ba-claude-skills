#!/usr/bin/env python3
"""Kiểm tra spec phân rã chức năng theo quy tắc trong references/decomposition-rules.md
và danh mục lỗi references/mistakes-catalog.md.

    python3 fd_lint.py spec.json            # in kết quả, thoát mã 1 nếu có LỖI
    python3 fd_lint.py spec.json --json     # kết quả dạng JSON
    python3 fd_lint.py spec.json --strict   # coi CẢNH BÁO như LỖI

Mức: LỖI (vi phạm quy tắc, phải sửa) · CẢNH BÁO (nên xem lại) · MIỄN (đã miễn trừ
kèm lý do trong spec["waive"]). Script chỉ kiểm tra cấu trúc và thói quen đặt tên;
việc đúng nghiệp vụ vẫn cần người làm nghiệp vụ xác nhận.
"""
import json
import re
import sys
from collections import defaultdict

import fdlib as F

VERBS_VI = """tao them sua xoa huy xem tim tra gui nhan duyet tu phe xuat nhap in tai dang xac kiem tinh cap
chon dat giu doi thanh hoan khoa mo gan phan dong nhac lap theo ghi luu chuyen giai hach tong kich vo ngung
tam bat tat khai cau ap huong thu chia xep dieu gop tach ra phat nop tich dung loc sap nang ha ky chot ban
mua bo can xin cho lay dua hien chay quet thong dinh tiep sao khoi ung import export goi uy danh bao dem canh chan go yeu tang giam soat so ngoai""".split()
VERBS_EN = """create add edit update delete cancel view search find send receive approve reject export import
print download upload login logout register verify validate calculate select place hold change pay refund
lock unlock assign sync notify remind generate track record save transfer disburse reconcile configure
define set apply submit review assess check confirm activate deactivate archive restore merge split
schedule book reserve capture issue renew close open list filter sort enable disable""".split()
VAGUE = {"quan ly", "xu ly", "ho tro", "thuc hien", "thao tac", "manage", "handle", "process",
         "support", "do"}
UI_RE = re.compile(r"\b(màn hình|trang|popup|nút|tab|screen|page|button|dialog)\b", re.I)  # so trên chữ gốc: "trạng thái" không bị tính là "trang"
CROSS_KEYWORDS = {
    "auth": ["dang nhap", "xac thuc", "phan quyen", "vai tro", "login", "authenticat", "otp"],
    "notify": ["thong bao", "nhac ", "gui email", "gui sms", "notif"],
    "audit": ["nhat ky", "audit", "lich su thao tac", "log thao tac"],
    "report": ["bao cao", "thong ke", "dashboard", "report"],
    "config": ["cau hinh", "danh muc", "khai bao", "tham so", "config", "master data"],
}


def first_word(name):
    n = F.norm(name)
    return n.split(" ")[0] if n else ""


def is_verb_first(name, extra):
    w = first_word(name)
    return w in VERBS_VI or w in VERBS_EN or w in extra


def compound_verbs(name, extra):
    """True nếu sau 'và / hoặc / / / &' là một động từ - dấu hiệu gộp hai hành vi."""
    parts = re.split(r"\s+(?:và|hoặc|va|hoac|and|or)\s+|\s*[/&]\s*", name.strip(), flags=re.I)
    return any(is_verb_first(p, extra) for p in parts[1:] if p.strip())


def lint(spec):
    res = []  # (level, code, where, msg)

    def add(level, code, where, msg, waive_key=None):
        if level != "LỖI" and waive_key and waive_key in spec["waive"]:
            res.append(("MIỄN", code, where, f"{msg}  → miễn: {spec['waive'][waive_key]}"))
        else:
            res.append((level, code, where, msg))

    items = F.walk(spec)
    byid = defaultdict(list)
    for it in items:
        byid[it["id"]].append(it)
    funcs = F.functions(items)
    extra = {F.norm(v) for v in spec.get("extra_verbs", [])}
    actors = {a["id"] for a in spec["actors"] if "id" in a}
    objects = {o["id"]: o for o in spec["objects"] if "id" in o}
    reqs = {r["id"] for r in spec["requirements"] if "id" in r}

    # ---- A. Cấu trúc & ID
    for i, lst in byid.items():
        if len(lst) > 1:
            add("LỖI", "A1", i, f"ID trùng ({len(lst)} lần)")
    for it in items:
        i = it["id"]
        if not F.ID_RE.match(i):
            add("LỖI", "A1", i or "(trống)", "ID phải có dạng 1 / 1.2 / 1.2.3")
            continue
        segs = i.split(".")
        if it["depth"] != len(segs):
            add("LỖI", "A1", i, f"ID có {len(segs)} đoạn nhưng nằm ở cấp {it['depth']}")
        if it["parent_id"] and not (i.startswith(it["parent_id"] + ".") and len(segs) == len(it["parent_id"].split(".")) + 1):
            add("LỖI", "A1", i, f"ID không khớp cha {it['parent_id']}")
        if not (it["n"].get("name") or "").strip():
            add("LỖI", "B6", i, "Thiếu tên")
        if it["depth"] == 1 and it["is_leaf"]:
            add("LỖI", "A6", i, f"Module \"{it['n'].get('name')}\" không có chức năng con")
        kids = it["n"].get("children") or []
        if len(kids) == 1:
            add("CẢNH BÁO", "A2", i, f"\"{it['n'].get('name')}\" chỉ có 1 con - thường là thừa một cấp", f"A2:{i}")
        if len(kids) > 9:
            add("CẢNH BÁO", "A3", i, f"\"{it['n'].get('name')}\" có {len(kids)} con (> 9) - nên gom nhóm", f"A3:{i}")
        if it["depth"] > 4:
            add("CẢNH BÁO", "A5", i, f"Sâu {it['depth']} cấp (> 4) - khó đọc, khó truy vết")
    mods = spec["modules"]
    if len(mods) > 9:
        add("CẢNH BÁO", "A3", "root", f"Có {len(mods)} module cấp 1 (> 9)", "A3:root")
    if len(mods) < 3:
        add("CẢNH BÁO", "A3", "root", f"Chỉ có {len(mods)} module cấp 1 - kiểm tra có bỏ sót năng lực nào", "A3:root")
    for it in items:  # A4: độ sâu lá lệch trong cùng một cha
        kids = it["n"].get("children") or []
        if len(kids) > 1:
            depths = []
            for k in kids:
                sub = [x for x in items if x["id"] == str(k.get("id")) or x["id"].startswith(str(k.get("id")) + ".")]
                lv = [x["depth"] for x in sub if x["is_leaf"]]
                depths.append((max(lv) if lv else it["depth"] + 1) - (it["depth"] + 1))
            if max(depths) - min(depths) >= 2:
                add("CẢNH BÁO", "A4", it["id"], f"Các nhánh con của \"{it['n'].get('name')}\" sâu không đều (lệch {max(depths) - min(depths)} cấp)", f"A4:{it['id']}")

    # ---- B. Đặt tên (B1, B2, B4, B6 chỉ cho chức năng = lá; B5 cho mọi nút)
    for it in items:
        nm = it['n'].get('name', '')
        if UI_RE.search(nm):
            what = 'chức năng' if it['is_leaf'] else 'module/tính năng'
            add('CẢNH BÁO', 'B5', it['id'], f'"{nm}" nhắc tới màn hình/giao diện - {what} mô tả việc làm hoặc năng lực, không mô tả chỗ làm', f"B5:{it['id']}")
    for it in funcs:
        n, i = it["n"].get("name", ""), it["id"]
        nn = F.norm(n)
        if any(nn == v or nn.startswith(v + " ") for v in VAGUE):
            add("LỖI", "B2", i, f"\"{n}\" dùng động từ chung chung - liệt kê từng thao tác cụ thể (tạo/xem/sửa/hủy…)")
        elif not is_verb_first(n, extra):
            add("CẢNH BÁO", "B1", i, f"\"{n}\" có vẻ không bắt đầu bằng động từ (cần Động từ + Danh từ)", f"B1:{i}")
        if compound_verbs(n, extra):
            add("CẢNH BÁO", "B4", i, f"\"{n}\" có vẻ gồm nhiều hành vi (sau và/hoặc là một động từ) - cân nhắc tách", f"B4:{i}")
        if len(n.split()) > 12:
            add("CẢNH BÁO", "B6", i, f"Tên dài {len(n.split())} tiếng - rút gọn, đưa chi tiết vào ghi chú")
    seen = {}
    for it in funcs:
        key = F.norm(it["n"].get("name", ""))
        if key in seen and seen[key]["parent_id"] == it["parent_id"]:
            add("LỖI", "B3", it["id"], f"Trùng tên với {seen[key]['id']} (\"{it['n'].get('name')}\") ngay trong cùng một nhóm")
        elif key in seen:
            add("CẢNH BÁO", "B3", it["id"], f"Trùng tên với {seen[key]['id']} (\"{it['n'].get('name')}\") - có thể chồng lấn", f"B3:{it['id']}")
        else:
            seen.setdefault(key, it)
    ws = [(it, set(F.norm(it["n"].get("name", "")).split())) for it in funcs]
    for a in range(len(ws)):
        for b in range(a + 1, len(ws)):
            (ia, sa), (ib, sb) = ws[a], ws[b]
            if len(sa) >= 3 and len(sb) >= 3 and ia["parent_id"] != ib["parent_id"] \
               and F.norm(ia["n"]["name"]) != F.norm(ib["n"]["name"]):
                j = len(sa & sb) / len(sa | sb)
                if j >= 0.75:
                    add("CẢNH BÁO", "B3", ia["id"], f"Tên gần giống {ib['id']} (\"{ib['n']['name']}\") - kiểm tra chồng lấn (MECE)", f"B3:{ia['id']}")

    # ---- C. Actor, truy vết
    used_actors, covered = set(), defaultdict(list)
    for it in funcs:
        n, i = it["n"], it["id"]
        acts = n.get("actors") or []
        if not acts:
            add("CẢNH BÁO", "C1", i, f"\"{n.get('name')}\" chưa có actor", f"C1:{i}")
        for a in acts:
            used_actors.add(a)
            if a not in actors:
                add("LỖI", "C1", i, f"Actor \"{a}\" chưa khai báo trong 'actors'")
        for r in n.get("reqs") or []:
            if reqs and r not in reqs:
                add("LỖI", "C4", i, f"Tham chiếu yêu cầu \"{r}\" không tồn tại")
            covered[r].append(i)
        if reqs and not (n.get("reqs") or n.get("derived")):
            add("CẢNH BÁO", "C3", i, f"\"{n.get('name')}\" chưa truy về yêu cầu nào (hoặc đánh dấu \"derived\": true nếu là chức năng suy ra)", f"C3:{i}")
    for r in sorted(reqs):
        if r not in covered:
            add("LỖI", "C2", r, "Yêu cầu chưa được chức năng nào phủ")
    for a in sorted(actors - used_actors):
        add("CẢNH BÁO", "C5", a, f"Actor \"{a}\" khai báo nhưng không có chức năng nào", f"C5:{a}")

    # ---- D. CRUD theo đối tượng nghiệp vụ
    per_obj = defaultdict(lambda: defaultdict(list))
    for it in funcs:
        ops = F.ops_of(it["n"])
        for o, letters in ops.items():
            if o not in objects:
                add("LỖI", "D5", it["id"], f"Đối tượng \"{o}\" chưa khai báo trong 'objects'")
            for ch in letters:
                per_obj[o][ch].append(it["id"])
        for o, raw in (it["n"].get("ops") or {}).items():
            if not re.fullmatch(r"[CRUDcrud]+", str(raw)):
                add("LỖI", "D5", it["id"], f"ops \"{raw}\" chứa ký tự ngoài C/R/U/D")
        if sum(1 for letters in ops.values() if len(letters) == 4) >= 1:
            add("CẢNH BÁO", "D6", it["id"], f"\"{it['n'].get('name')}\" làm đủ C-R-U-D trên một đối tượng - đây là 'Quản lý X' gộp, nên tách", f"D6:{it['id']}")
    for oid, o in objects.items():
        has = per_obj.get(oid, {})
        nm = o.get("name", oid)
        if "C" not in has and o.get("source") != "external":
            add("LỖI", "D1", oid, f"\"{nm}\" chưa có chức năng Tạo (hoặc đánh dấu \"source\": \"external\" nếu dữ liệu đến từ hệ thống khác)")
        if "R" not in has:
            add("CẢNH BÁO", "D2", oid, f"\"{nm}\" chưa có chức năng Xem/Tìm", f"D2:{oid}")
        ext = o.get("source") == "external"
        if "U" not in has and not o.get("immutable") and not ext:
            add("CẢNH BÁO", "D3", oid, f"\"{nm}\" chưa có chức năng Sửa (nếu bất biến, đánh dấu \"immutable\": true)", f"D3:{oid}")
        if "D" not in has and not o.get("no_delete") and not ext:
            add("CẢNH BÁO", "D4", oid, f"\"{nm}\" chưa có chức năng Hủy/Lưu trữ/Xóa (nếu cố ý không xóa, đánh dấu \"no_delete\": true)", f"D4:{oid}")

    # ---- E. Chức năng xuyên suốt
    present = set()
    for it in items:
        for t in it["n"].get("tags") or []:
            present.add(t)
        nn = F.norm(it["n"].get("name", "")) + " "
        for t, kws in CROSS_KEYWORDS.items():
            if any(k in nn for k in kws):
                present.add(t)
    for t, label in F.CROSS_TAGS.items():
        if t not in present:
            add("CẢNH BÁO", "E1", t, f"Chưa thấy nhóm chức năng xuyên suốt: {label} (thêm hoặc miễn trừ kèm lý do)", f"E1:{t}")

    # ---- F. Phạm vi & ưu tiên
    withp = [it for it in funcs if it["n"].get("priority")]
    for it in withp:
        if it["n"]["priority"] not in F.PRIORITIES:
            add("LỖI", "F1", it["id"], f"priority \"{it['n']['priority']}\" phải là M/S/C/W")
    if withp and len(withp) != len(funcs):
        add("CẢNH BÁO", "F1", "root", f"Chỉ {len(withp)}/{len(funcs)} chức năng có priority - nên gán đủ hoặc bỏ hết", "F1:root")
    return res, items, funcs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    try:
        spec = F.load(args[0])
    except F.SpecError as e:
        F.fail(str(e))
    res, items, funcs = lint(spec)
    strict = "--strict" in sys.argv
    errs = [r for r in res if r[0] == "LỖI" or (strict and r[0] == "CẢNH BÁO")]
    warns = [r for r in res if r[0] == "CẢNH BÁO"]
    waived = [r for r in res if r[0] == "MIỄN"]
    if "--json" in sys.argv:
        print(json.dumps([{"level": l, "code": c, "where": w, "message": m} for l, c, w, m in res], ensure_ascii=False, indent=2))
    else:
        mods = len(spec["modules"])
        depth = max(i["depth"] for i in items)
        print(f"Spec: {spec['name']} — {mods} module · {len(funcs)} chức năng · sâu {depth} cấp")
        order = {"LỖI": 0, "CẢNH BÁO": 1, "MIỄN": 2}
        for lvl, code, where, msg in sorted(res, key=lambda r: (order[r[0]], r[1], r[2])):
            print(f"{lvl:<9} [{code}] {where:<8} {msg}")
        print(f"Kết quả: {len([r for r in res if r[0]=='LỖI'])} lỗi, {len(warns)} cảnh báo, {len(waived)} miễn trừ")
    sys.exit(1 if [r for r in res if r[0] == "LỖI"] or (strict and warns) else 0)


if __name__ == "__main__":
    main()
