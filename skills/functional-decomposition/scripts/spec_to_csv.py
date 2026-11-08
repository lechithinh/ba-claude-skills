#!/usr/bin/env python3
"""Xuất spec phân rã chức năng ra CSV (UTF-8 có BOM, mở thẳng bằng Excel / Google Sheets).

    python3 spec_to_csv.py spec.json out.csv           # bảng đầy đủ
    python3 spec_to_csv.py spec.json out.csv --jira    # cột cho import Jira (kiểm tra lại mapping khi import)
"""
import csv
import sys

import fdlib as F

JIRA_PRIO = {"M": "High", "S": "Medium", "C": "Low", "W": "Lowest"}


def main():
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(pos) != 2:
        sys.exit(__doc__)
    try:
        spec = F.load(pos[0])
    except F.SpecError as e:
        F.fail(str(e))
    items = F.walk(spec)
    jira = "--jira" in sys.argv
    with open(pos[1], "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if jira:
            w.writerow(["Issue Id", "Issue Type", "Summary", "Parent", "Description", "Priority", "Labels"])
            for it in items:
                n = it["n"]
                typ = "Epic" if it["depth"] == 1 else "Story"
                desc = n.get("note", "")
                if n.get("reqs"):
                    desc = (desc + "\nYêu cầu: " + ", ".join(n["reqs"])).strip()
                labels = " ".join(["FD"] + (n.get("tags") or []))
                w.writerow([it["id"], typ, n["name"], it["parent_id"] or "", desc,
                            JIRA_PRIO.get(n.get("priority"), ""), labels])
        else:
            w.writerow(["ID", "Parent ID", "Cấp", "Loại", "Chức năng", "Actor", "Đối tượng (ops)",
                        "Ưu tiên", "Phase", "Yêu cầu", "Tag", "Ghi chú"])
            for it in items:
                n = it["n"]
                ops = "; ".join(f"{F.object_name(spec, o)}:{l}" for o, l in F.ops_of(n).items())
                w.writerow([it["id"], it["parent_id"] or "", it["depth"], it["kind"], n["name"],
                            ", ".join(F.actor_name(spec, a) for a in (n.get("actors") or [])), ops,
                            n.get("priority", ""), n.get("phase", ""), ", ".join(n.get("reqs") or []),
                            ", ".join(n.get("tags") or []), n.get("note", "")])


if __name__ == "__main__":
    main()
