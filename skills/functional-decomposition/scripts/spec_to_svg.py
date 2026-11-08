#!/usr/bin/env python3
"""Vẽ cây phân rã chức năng thành SVG (trái → phải, mỗi module một màu, chấm màu = ưu tiên).
Màu và font chỉnh trong assets/svg-theme.css.

    python3 spec_to_svg.py spec.json out.svg
    python3 spec_to_svg.py spec.json out.svg --depth 2      # chỉ vẽ tới cấp 2
    python3 spec_to_svg.py spec.json out.svg --module 2     # chỉ module 2
"""
import html
import os
import sys
import textwrap

import fdlib as F

BOX_H, GAP_Y, GAP_X, PAD, WRAP = 46, 12, 46, 24, 30


def text_w(s):
    return len(s) * 7.0


def main():
    argv = sys.argv[1:]
    pos = [a for a in argv if not a.startswith("--")]
    opts = {}
    for k in ("--depth", "--module"):
        if k in argv:
            opts[k] = argv[argv.index(k) + 1]
            pos = [p for p in pos if p != opts[k]]
    if len(pos) != 2:
        sys.exit(__doc__)
    try:
        spec = F.load(pos[0])
    except F.SpecError as e:
        F.fail(str(e))
    maxd = int(opts.get("--depth", 99))
    only = opts.get("--module")

    # Dựng cây ảo có gốc
    def build(node, depth):
        kids = [] if depth >= maxd else [build(c, depth + 1) for c in (node.get("children") or [])]
        return {"n": node, "depth": depth, "kids": kids}

    mods = [m for m in spec["modules"] if only is None or str(m["id"]) == only]
    root = {"n": {"id": "", "name": spec["name"]}, "depth": 0, "kids": [build(m, 1) for m in mods]}

    # Độ rộng theo cấp
    widths = {}

    def measure(t):
        nm = t["n"].get("name", "")
        w = min(text_w(nm) + 28, WRAP * 7.0 + 28) if t["depth"] else min(text_w(nm) + 28, 230)
        widths[t["depth"]] = max(widths.get(t["depth"], 120), w, text_w(t["n"].get("id", "")) + 28)
        for k in t["kids"]:
            measure(k)
    measure(root)
    xs, x = {}, PAD
    for d in sorted(widths):
        xs[d] = x
        x += widths[d] + GAP_X

    # Vị trí y
    cursor = [PAD + 34]

    def layout(t):
        if not t["kids"]:
            t["y"] = cursor[0]
            cursor[0] += BOX_H + GAP_Y
        else:
            for k in t["kids"]:
                layout(k)
            t["y"] = (t["kids"][0]["y"] + t["kids"][-1]["y"]) / 2
    layout(root)
    W = x - GAP_X + PAD
    H = cursor[0] + PAD + 18

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" class="fd-svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Sơ đồ phân rã chức năng: {html.escape(spec["name"])}">']
    css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "svg-theme.css")
    if os.path.exists(css):
        out.append("<style>" + open(css, encoding="utf-8").read() + "</style>")
    out.append(f'<rect class="bg" width="{W:.0f}" height="{H:.0f}"/>')
    out.append(f'<text class="title" x="{PAD}" y="{PAD + 6}">{html.escape(spec["name"])}</text>')
    mod_index = {str(m["id"]): i for i, m in enumerate(spec["modules"])}

    def draw(t, cls_idx=None):
        n, d = t["n"], t["depth"]
        bx, bw = xs[d], widths[d]
        by = t["y"]
        if d == 1:
            cls_idx = mod_index.get(str(n["id"]), 0) % 9
        cls = "root" if d == 0 else f"m{cls_idx}"
        out.append(f'<g class="{cls}"><title>{html.escape((n.get("id","") + " " + n.get("name","")).strip())}</title>')
        out.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{BOX_H}" rx="8"/>')
        nm = n.get("name", "")
        lines = textwrap.wrap(nm, WRAP) or [nm]
        if d == 0:
            out.append(f'<text x="{bx + 12:.1f}" y="{by + BOX_H / 2 + 4.5:.1f}">{html.escape(lines[0] + ("…" if len(lines) > 1 else ""))}</text>')
        else:
            out.append(f'<text class="id" x="{bx + 10:.1f}" y="{by + 13:.1f}">{html.escape(str(n.get("id", "")))}</text>')
            base = 30 if len(lines) == 1 else 26
            for li, ln in enumerate(lines[:2]):
                out.append(f'<text class="name" x="{bx + 10:.1f}" y="{by + base + li * 13:.1f}">{html.escape(ln + ("…" if li == 1 and len(lines) > 2 else ""))}</text>')
            if n.get("priority") in F.PRIORITIES:
                out.append(f'<circle class="p-{n["priority"]}" cx="{bx + bw - 10:.1f}" cy="{by + 10:.1f}" r="4"><title>{F.PRIORITIES[n["priority"]]}</title></circle>')
        out.append("</g>")
        for k in t["kids"]:
            x1, y1 = bx + bw, by + BOX_H / 2
            x2, y2 = xs[k["depth"]], k["y"] + BOX_H / 2
            xm = (x1 + x2) / 2
            out.append(f'<path class="link" d="M{x1:.1f} {y1:.1f} H{xm:.1f} V{y2:.1f} H{x2:.1f}"/>')
            draw(k, cls_idx)
    draw(root)
    lx = PAD
    for key, label in (("M", "Must"), ("S", "Should"), ("C", "Could"), ("W", "Won't")):
        out.append(f'<circle class="p-{key}" cx="{lx + 4}" cy="{H - 14:.0f}" r="4"/><text class="legend" x="{lx + 13}" y="{H - 10:.0f}">{label}</text>')
        lx += 70
    out.append("</svg>")
    open(pos[1], "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
