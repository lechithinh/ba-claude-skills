#!/usr/bin/env python3
"""Sinh sơ đồ cây Mermaid (flowchart LR) từ spec phân rã chức năng.

    python3 spec_to_mermaid.py spec.json out.mmd                # mặc định: sâu nhất mà vẫn ≤ 40 node
    python3 spec_to_mermaid.py spec.json out.mmd --depth 2      # chỉ định số cấp
    python3 spec_to_mermaid.py spec.json out.mmd --module 2     # chỉ module 2, đủ độ sâu
    python3 spec_to_mermaid.py spec.json out.mmd --split        # thêm một file cho từng module

Khi cây quá lớn, sơ đồ chính chỉ vẽ tới cấp vừa 40 node; dùng --split để có thêm một sơ đồ chi tiết cho
từng module (out-m1.mmd, out-m2.mmd…).
"""
import re
import sys

import fdlib as F

LIMIT = 40


def nid(i):
    return "n_" + re.sub(r"\W", "_", i)


def label(n):
    return (n["id"] + " " + n["name"]).replace('"', "'")


def render(spec, depth, module=None):
    items = [i for i in F.walk(spec) if i["depth"] <= depth and (module is None or i["top_id"] == module)]
    L = ["flowchart LR"]
    root = nid("root")
    title = spec["name"].replace('"', "'")
    if module is None:
        L.append(f'    {root}(["{title}"])')
    for it in items:
        n = it["n"]
        if it["depth"] == 1:
            cls = "mod"
        elif it["is_leaf"]:
            cls = "fn"
        else:
            cls = "feat"
        L.append(f'    {nid(it["id"])}["{label(n)}"]:::{cls}')
    for it in items:
        if it["parent_id"]:
            L.append(f'    {nid(it["parent_id"])} --> {nid(it["id"])}')
        elif module is None:
            L.append(f"    {root} --> {nid(it['id'])}")
    L += ["    classDef mod fill:#1e3a8a,color:#fff,stroke:#1e3a8a",
          "    classDef feat fill:#dbeafe,stroke:#60a5fa,color:#0f172a",
          "    classDef fn fill:#fff,stroke:#94a3b8,color:#0f172a"]
    return "\n".join(L) + "\n", len(items)


def main():
    argv = sys.argv[1:]
    pos = [a for a in argv if not a.startswith("--")]
    opts = {}
    for k in ("--depth", "--module"):
        if k in argv:
            opts[k] = argv[argv.index(k) + 1]
            if opts[k] in pos:
                pos.remove(opts[k])
    if len(pos) != 2:
        sys.exit(__doc__)
    try:
        spec = F.load(pos[0])
    except F.SpecError as e:
        F.fail(str(e))
    module = opts.get("--module")
    explicit = "--depth" in opts
    depth = int(opts.get("--depth", 9))
    text, count = render(spec, depth, module)
    while count > LIMIT and depth > 1 and not explicit:
        depth -= 1
        text, count = render(spec, depth, module)
    if not explicit and depth < max(i["depth"] for i in F.walk(spec)):
        sys.stderr.write(f"Ghi chú: cây lớn hơn {LIMIT} node, sơ đồ chính vẽ tới cấp {depth}. Dùng --split hoặc --module để xem chi tiết.\n")
    elif count > LIMIT:
        sys.stderr.write(f"Cảnh báo: {count} node (> {LIMIT}) - khó đọc, cân nhắc giảm --depth hoặc dùng --split.\n")
    open(pos[1], "w", encoding="utf-8").write(text)
    reduced = depth < max(i["depth"] for i in F.walk(spec))
    if "--split" in argv and module is None and reduced:
        stem = pos[1].rsplit(".", 1)[0]
        for m in spec["modules"]:
            t, c = render(spec, 9, str(m["id"]))
            if c > LIMIT:
                sys.stderr.write(f"Cảnh báo: module {m['id']} có {c} node (> {LIMIT}) - cân nhắc tách module.\n")
            open(f"{stem}-m{m['id']}.mmd", "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    main()
