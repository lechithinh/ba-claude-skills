#!/usr/bin/env python3
"""Sinh bảng Markdown từ spec phân rã chức năng: bảng phân cấp, ma trận CRUD,
ma trận truy vết yêu cầu, ma trận actor × module, thống kê.

    python3 spec_to_table.py spec.json out.md
    python3 spec_to_table.py spec.json -            # in ra màn hình
"""
import sys
from collections import defaultdict

import fdlib as F


def cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ")


def build(spec):
    items = F.walk(spec)
    funcs = F.functions(items)
    L = [f"# {spec['name']}", ""]
    sc = spec.get("scope", {})
    if sc.get("in"):
        L.append("**Trong phạm vi:** " + "; ".join(sc["in"]))
    if sc.get("out"):
        L.append("**Ngoài phạm vi:** " + "; ".join(sc["out"]))
    if spec["actors"]:
        L.append("**Actor:** " + ", ".join(f"{a.get('name', a['id'])}" for a in spec["actors"]))
    if spec.get("assumptions"):
        L += ["", "**Giả định:**"] + [f"- {a}" for a in spec["assumptions"]]
    L.append("")

    # 1. Phân cấp
    has_req = bool(spec["requirements"])
    L += ["## 1. Bảng phân cấp", ""]
    head = "| ID | Chức năng | Loại | Actor | Ưu tiên |" + (" Yêu cầu |" if has_req else "") + " Ghi chú |"
    L += [head, "|" + "---|" * (head.count("|") - 1)]
    for it in items:
        n = it["n"]
        indent = "&nbsp;&nbsp;&nbsp;" * (it["depth"] - 1)
        name = f"**{n['name']}**" if it["depth"] == 1 else n["name"]
        acts = ", ".join(F.actor_name(spec, a) for a in (n.get("actors") or []))
        pr = n.get("priority", "")
        row = f"| {it['id']} | {indent}{cell(name)} | {it['kind']} | {cell(acts)} | {pr} |"
        if has_req:
            row += f" {', '.join(n.get('reqs') or [])} |"
        row += f" {cell(n.get('note', ''))} |"
        L.append(row)
    L.append("")

    # 2. CRUD
    if spec["objects"]:
        per = defaultdict(lambda: defaultdict(list))
        for it in funcs:
            for o, letters in F.ops_of(it["n"]).items():
                for ch in letters:
                    per[o][ch].append(it["id"])
        L += ["## 2. Ma trận CRUD theo đối tượng nghiệp vụ", "",
              "| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |", "|---|---|---|---|---|"]
        for o in spec["objects"]:
            row = [o.get("name", o["id"])]
            for ch in "CRUD":
                ids = per[o["id"]].get(ch)
                waived = F.crud_waiver(spec, o, ch)
                row.append(", ".join(ids) if ids else (f"— (miễn: {waived})" if waived else "❌"))
            L.append("| " + " | ".join(cell(x) for x in row) + " |")
        L.append("")

    # 3. Truy vết yêu cầu
    if has_req:
        cov = defaultdict(list)
        for it in funcs:
            for r in it["n"].get("reqs") or []:
                cov[r].append(it["id"])
        L += ["## 3. Truy vết yêu cầu → chức năng", "", "| Yêu cầu | Nội dung | Chức năng phủ |", "|---|---|---|"]
        for r in spec["requirements"]:
            ids = cov.get(r["id"])
            L.append(f"| {r['id']} | {cell(r.get('text', ''))} | {', '.join(ids) if ids else '❌ chưa phủ'} |")
        orphan = [it["id"] for it in funcs if not (it["n"].get("reqs") or it["n"].get("derived"))]
        if orphan:
            L += ["", "Chức năng chưa truy về yêu cầu: " + ", ".join(orphan)]
        L.append("")

    # 4. Actor x Module
    if spec["actors"]:
        mods = spec["modules"]
        cnt = defaultdict(lambda: defaultdict(int))
        for it in funcs:
            for a in it["n"].get("actors") or []:
                cnt[a][it["top_id"]] += 1
        L += ["## 4. Actor × Module (số chức năng)", "",
              "| Actor | " + " | ".join(f"{m['id']}. {cell(m['name'])}" for m in mods) + " |",
              "|---|" + "---|" * len(mods)]
        for a in spec["actors"]:
            L.append(f"| {a.get('name', a['id'])} | " + " | ".join(str(cnt[a['id']].get(m['id'], '') or '') for m in mods) + " |")
        L += ["", "_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._", ""]

    # 5. Thống kê
    pr = defaultdict(int)
    for it in funcs:
        pr[it["n"].get("priority") or "-"] += 1
    L += ["## 5. Thống kê", "",
          f"- Module: **{len(spec['modules'])}** · Tính năng: **{len([i for i in items if i['kind']=='Feature'])}** · Chức năng (lá): **{len(funcs)}** · Độ sâu: **{max(i['depth'] for i in items)}** cấp",
          "- Ưu tiên: " + ", ".join(f"{k}: {v}" for k, v in sorted(pr.items())), ""]
    return "\n".join(L)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    try:
        spec = F.load(sys.argv[1])
    except F.SpecError as e:
        F.fail(str(e))
    out = build(spec)
    if sys.argv[2] == "-":
        print(out)
    else:
        open(sys.argv[2], "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    main()
