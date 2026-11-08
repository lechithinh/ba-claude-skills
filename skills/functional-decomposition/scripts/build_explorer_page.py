#!/usr/bin/env python3
"""Dựng một trang HTML (một file, không cần mạng) để khám phá phân rã chức năng:
cây có lọc theo actor/ưu tiên/từ khoá, ma trận CRUD, truy vết yêu cầu, actor × module, kết quả lint.

    python3 build_explorer_page.py spec.json explorer.html
"""
import json
import os
import sys
from collections import defaultdict

import fdlib as F
from fd_lint import lint

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Phân rã chức năng</title>
<style>
__CSS__
body { margin: 0; background: var(--fd-bg); color: var(--fd-ink); font: 15px/1.55 var(--fd-font); }
.wrap { max-width: 1100px; margin: 0 auto; padding: 16px; }
h1 { font-size: 1.4rem; margin: 0 0 2px; } .muted { color: var(--fd-muted); }
.tabs { display: flex; gap: 4px; flex-wrap: wrap; border-bottom: 1px solid var(--fd-border); margin: 14px 0; }
.tabs button { background: none; border: 0; padding: 9px 12px; color: var(--fd-muted); font: inherit; cursor: pointer; border-bottom: 2px solid transparent; }
.tabs button[aria-selected=true] { color: var(--fd-accent); border-color: var(--fd-accent); font-weight: 600; }
.filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.filters input { min-width: 240px; flex: 1; }
.filters input, .filters select, .filters button { padding: 7px 9px; border: 1px solid var(--fd-border); border-radius: 7px; background: var(--fd-surface); color: var(--fd-ink); font: inherit; }
ul.tree, ul.tree ul { list-style: none; padding-left: 18px; margin: 2px 0; border-left: 1px dashed var(--fd-border); } ul.tree { padding-left: 0; border: 0; }
summary { cursor: pointer; padding: 3px 0; } li.leaf { padding: 3px 0 3px 4px; }
.nid { font-weight: 700; color: var(--fd-muted); font-variant-numeric: tabular-nums; } li.depth1 > details > summary .nname { font-weight: 700; font-size: 1.05em; }
.chip { display: inline-block; font-size: 11.5px; padding: 0 7px; border-radius: 10px; background: var(--fd-surface); border: 1px solid var(--fd-border); }
.chip.ops { color: var(--fd-accent); } .chip.req { color: var(--fd-muted); }
.chip.p-M { background: #fee2e2; color: #991b1b; border-color: #fca5a5; } .chip.p-S { background: #fef3c7; color: #92400e; border-color: #fcd34d; }
.chip.p-C { background: #dcfce7; color: #166534; border-color: #86efac; } .chip.p-W { background: #f1f5f9; color: #475569; border-color: #cbd5e1; }
.note { color: var(--fd-muted); font-size: 13px; }
table { border-collapse: collapse; width: 100%; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--fd-border); padding: 6px 9px; text-align: left; vertical-align: top; } th { background: var(--fd-surface); }
td.bad, p.bad { color: var(--fd-bad); font-weight: 600; } td.warn, p.warn { color: var(--fd-warn); } td.muted { color: var(--fd-muted); } p.ok { color: var(--fd-ok); font-weight: 600; }
</style></head>
<body class="fd-page"><div class="wrap">
<h1 id="title"></h1><div class="muted" id="stats"></div>
<div class="tabs" role="tablist">
 <button role="tab" aria-selected="true" data-panel="p-tree">Cây chức năng</button>
 <button role="tab" aria-selected="false" data-panel="p-crud">Ma trận CRUD</button>
 <button role="tab" aria-selected="false" data-panel="p-reqs">Truy vết yêu cầu</button>
 <button role="tab" aria-selected="false" data-panel="p-matrix">Actor × Module</button>
 <button role="tab" aria-selected="false" data-panel="p-lint" id="tab-lint">Kiểm tra</button>
</div>
<section class="panel" id="p-tree"><div class="filters">
 <input id="f-q" type="search" placeholder="Tìm theo tên, ID, yêu cầu…" aria-label="Tìm">
 <select id="f-actor" aria-label="Lọc theo actor"></select>
 <select id="f-prio" aria-label="Lọc theo ưu tiên"><option value="">Mọi ưu tiên</option><option value="M">Must</option><option value="S">Should</option><option value="C">Could</option><option value="W">Won't</option></select>
 <button id="expand">Mở hết</button><button id="collapse">Thu gọn</button></div><div id="tree"></div></section>
<section class="panel" id="p-crud" hidden><div id="crud"></div></section>
<section class="panel" id="p-reqs" hidden><div id="reqs"></div></section>
<section class="panel" id="p-matrix" hidden><div id="matrix"></div></section>
<section class="panel" id="p-lint" hidden><div id="lint"></div></section>
</div>
<script>window.FD_DATA = __DATA__;</script>
<script>
__JS__
</script></body></html>"""


def node_json(it_node, depth):
    kids = it_node.get("children") or []
    d = {"id": str(it_node["id"]), "name": it_node.get("name", ""), "depth": depth, "leaf": not kids}
    for k in ("actors", "priority", "reqs", "note", "derived", "tags"):
        if it_node.get(k):
            d[k] = it_node[k]
    ops = F.ops_of(it_node)
    if ops:
        d["ops"] = ops
    d["children"] = [node_json(c, depth + 1) for c in kids]
    return d


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    try:
        spec = F.load(sys.argv[1])
    except F.SpecError as e:
        F.fail(str(e))
    items = F.walk(spec)
    funcs = F.functions(items)
    crud = defaultdict(lambda: defaultdict(list))
    cover = defaultdict(list)
    matrix = defaultdict(lambda: defaultdict(int))
    for it in funcs:
        for o, letters in F.ops_of(it["n"]).items():
            for ch in letters:
                crud[o][ch].append(it["id"])
        for r in it["n"].get("reqs") or []:
            cover[r].append(it["id"])
        for a in it["n"].get("actors") or []:
            matrix[a][it["top_id"]] += 1
    waived_cells = {o["id"]: {ch: F.crud_waiver(spec, o, ch) for ch in "CRUD"} for o in spec["objects"] if "id" in o}
    res, _, _ = lint(spec)
    data = {
        "name": spec["name"], "depth": max(i["depth"] for i in items),
        "actors": spec["actors"], "objects": spec["objects"], "requirements": spec["requirements"],
        "modules": [node_json(m, 1) for m in spec["modules"]],
        "functions": [{"id": f["id"], "reqs": f["n"].get("reqs"), "derived": f["n"].get("derived")} for f in funcs],
        "crud": crud, "waived": waived_cells, "cover": cover, "matrix": matrix,
        "lint": [{"level": l, "code": c, "where": w, "message": m} for l, c, w, m in res],
    }
    css = open(os.path.join(ASSETS, "svg-theme.css"), encoding="utf-8").read()
    js = open(os.path.join(ASSETS, "explorer.js"), encoding="utf-8").read()
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.replace("__TITLE__", spec["name"].replace("<", "&lt;")).replace("__CSS__", css) \
        .replace("__DATA__", blob).replace("__JS__", js.replace("</", "<\\/"))
    open(sys.argv[2], "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    main()
