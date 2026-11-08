#!/usr/bin/env python3
"""Kiểm tra bảng quyết định: liệt kê mọi tổ hợp điều kiện, tìm tổ hợp THIẾU rule, rule MÂU THUẪN,
rule CHỒNG LẤN (thừa), rút gọn bằng "-" (không quan tâm) và sinh test case.

    python3 dt_check.py spec.json                 # báo cáo kiểm tra (thoát mã 1 nếu có LỖI)
    python3 dt_check.py spec.json --table         # bảng đầy đủ mọi tổ hợp (để rà soát với stakeholder)
    python3 dt_check.py spec.json --simplify      # bảng rút gọn (gộp tổ hợp có cùng kết quả)
    python3 dt_check.py spec.json --tests         # test case: mỗi tổ hợp một dòng

Spec JSON:
{
  "name": "Hủy đơn hàng",
  "conditions": [{"id": "C1", "name": "Trạng thái đơn", "values": ["Chờ thanh toán", "Đã xác nhận"]}],
  "actions":    [{"id": "A1", "name": "Hủy ngay"}],
  "rules": [{"id": "R1", "when": {"C1": "Chờ thanh toán"}, "then": ["A1"], "source": "BR-01"}]
}
`when` bỏ qua điều kiện nào = điều kiện đó không quan tâm (mọi giá trị). `then` rỗng = không làm gì (hợp lệ).
Giá trị trong `values` phải loại trừ nhau và đủ bao phủ (chia khoảng số: "≤ 2 giờ", "> 2 giờ").
"""
import itertools
import json
import sys

LIMIT = 5000


def load(path):
    try:
        s = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Không đọc được spec: {e}")
    for k in ("conditions", "actions", "rules"):
        if not isinstance(s.get(k), list):
            sys.exit(f"Spec thiếu '{k}'")
    if not s["conditions"]:
        sys.exit("Spec cần ít nhất 1 điều kiện (conditions)")
    return s


def check(s):
    errs, warns = [], []
    conds = s["conditions"]
    cid = [c["id"] for c in conds]
    vals = {c["id"]: c["values"] for c in conds}
    acts = {a["id"]: a["name"] for a in s["actions"]}
    for c in conds:
        if len(c["values"]) < 2:
            warns.append(("C", c["id"], "Điều kiện chỉ có 1 giá trị: không phân biệt được gì"))
        if len(set(c["values"])) != len(c["values"]):
            errs.append(("C", c["id"], "Giá trị bị trùng nhau trong cùng điều kiện"))
    total = 1
    for c in conds:
        total *= max(1, len(c["values"]))
    if total > LIMIT:
        sys.exit(f"{total} tổ hợp (> {LIMIT}): tách thành nhiều bảng nhỏ hoặc gộp bớt giá trị.")
    seen = set()
    for r in s["rules"]:
        if r["id"] in seen:
            errs.append(("R", r["id"], "ID rule trùng"))
        seen.add(r["id"])
        for k, v in (r.get("when") or {}).items():
            if k not in vals:
                errs.append(("R", r["id"], f"Điều kiện '{k}' không tồn tại"))
            elif v not in vals[k] and v != "-":
                errs.append(("R", r["id"], f"Giá trị '{v}' không thuộc {k} {vals[k]}"))
        for a in r.get("then") or []:
            if a not in acts:
                errs.append(("R", r["id"], f"Hành động '{a}' không tồn tại"))
    combos = list(itertools.product(*[vals[c] for c in cid]))
    cov = {}
    used = {r["id"]: 0 for r in s["rules"]}
    for combo in combos:
        m = dict(zip(cid, combo))
        hit = [r for r in s["rules"] if all(v == "-" or m.get(k) == v for k, v in (r.get("when") or {}).items())]
        cov[combo] = hit
        for r in hit:
            used[r["id"]] += 1
    for combo, hit in cov.items():
        desc = ", ".join(f"{c['name']}={v}" for c, v in zip(conds, combo))
        if not hit:
            warns.append(("THIẾU", desc, "Chưa có rule nào cho tổ hợp này"))
        elif len(hit) > 1:
            outs = {tuple(sorted(r.get("then") or [])) for r in hit}
            ids = ", ".join(r["id"] for r in hit)
            if len(outs) > 1:
                errs.append(("MÂU THUẪN", desc, f"{ids} cùng áp dụng nhưng cho kết quả khác nhau"))
            else:
                warns.append(("CHỒNG LẤN", desc, f"{ids} cùng áp dụng, kết quả giống nhau (rule thừa hoặc chưa tách rõ)"))
    for rid, n in used.items():
        if n == 0 and not any(e[1] == rid for e in errs):
            warns.append(("R", rid, "Rule không áp dụng cho tổ hợp nào"))
    return errs, warns, combos, cov, conds, acts


def outcome(hit, acts):
    if not hit:
        return None
    return tuple(sorted(hit[0].get("then") or []))


def label(o, acts):
    if o is None:
        return "❌ THIẾU"
    return ", ".join(acts[a] for a in o) or "(không làm gì)"


def full_table(conds, cov, acts):
    head = [c["name"] for c in conds] + ["Kết quả", "Rule"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for combo, hit in cov.items():
        conflict = len({tuple(sorted(r.get("then") or [])) for r in hit}) > 1
        res = "⚠️ MÂU THUẪN" if conflict else label(outcome(hit, acts), acts)
        L.append("| " + " | ".join(combo) + f" | {res} | {', '.join(r['id'] for r in hit) or '-'} |")
    return "\n".join(L)


def simplify(conds, cov, acts):
    """Gộp các tổ hợp có cùng kết quả: nếu một điều kiện nhận đủ mọi giá trị thì thay bằng '-'."""
    cid = [c["id"] for c in conds]
    vals = {c["id"]: c["values"] for c in conds}
    groups = {}
    for combo, hit in cov.items():
        o = outcome(hit, acts)
        if len(hit) > 1 and len({tuple(sorted(r.get("then") or [])) for r in hit}) > 1:
            o = ("!conflict",)
        groups.setdefault(o, []).append(combo)
    rows = []
    for o, items in groups.items():
        cur = {tuple(i) for i in items}
        changed = True
        while changed:
            changed = False
            for pos, c in enumerate(cid):
                buckets = {}
                for row in cur:
                    key = row[:pos] + row[pos + 1:]
                    buckets.setdefault(key, set()).add(row[pos])
                for key, vs in buckets.items():
                    if "-" not in vs and set(vs) >= set(vals[c]):
                        for v in list(vs):
                            cur.discard(key[:pos] + (v,) + key[pos:])
                        cur.add(key[:pos] + ("-",) + key[pos:])
                        changed = True
                        break
                if changed:
                    break
        for row in cur:
            rows.append((row, o))
    rows.sort(key=lambda x: [vals[c].index(v) if v != "-" else -1 for c, v in zip(cid, x[0])])
    head = [c["name"] for c in conds] + ["Kết quả"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for row, o in rows:
        res = "⚠️ MÂU THUẪN" if o == ("!conflict",) else label(o, acts)
        L.append("| " + " | ".join(row) + f" | {res} |")
    return "\n".join(L), len(rows)


def main():
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(pos) != 1:
        sys.exit(__doc__)
    s = load(pos[0])
    errs, warns, combos, cov, conds, acts = check(s)
    if "--table" in sys.argv:
        print(full_table(conds, cov, acts))
        return
    if "--simplify" in sys.argv:
        t, n = simplify(conds, cov, acts)
        print(t)
        print(f"\n{len(combos)} tổ hợp → {n} dòng sau khi rút gọn.")
        return
    if "--tests" in sys.argv:
        head = ["#"] + [c["name"] for c in conds] + ["Kết quả mong đợi"]
        print("| " + " | ".join(head) + " |\n|" + "---|" * len(head))
        for i, (combo, hit) in enumerate(cov.items(), 1):
            print(f"| TC{i:02d} | " + " | ".join(combo) + f" | {label(outcome(hit, acts), acts)} |")
        return
    print(f"Bảng quyết định: {s.get('name', '')} — {len(conds)} điều kiện · {len(combos)} tổ hợp · {len(s['rules'])} rule")
    for kind, where, msg in errs:
        print(f"LỖI       [{kind}] {where}: {msg}")
    for kind, where, msg in warns:
        print(f"CẢNH BÁO  [{kind}] {where}: {msg}")
    covered = sum(1 for h in cov.values() if h)
    print(f"Kết quả: {len(errs)} lỗi, {len(warns)} cảnh báo · phủ {covered}/{len(combos)} tổ hợp")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
