#!/usr/bin/env python3
"""Vẽ sơ đồ BPMN thành SVG (xem ngay trên trình duyệt, chèn vào tài liệu/slide)
từ cùng file spec JSON của spec_to_bpmn.py. Toạ độ giống hệt file .bpmn.

    python3 spec_to_svg.py spec.json out.svg

Màu và font lấy từ assets/svg-theme.css (được nhúng vào SVG); sửa file đó để đổi theme.
"""
import json
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec_to_bpmn import BOUNDARY, EVENTS, GATES, TASKS, geometry  # noqa: E402

THEME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "svg-theme.css")


def wrap(text, width_chars):
    words, lines, cur = (text or "").split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def tspans(cx, cy, lines, cls, lh=15):
    y0 = cy - (len(lines) - 1) * lh / 2 + 4
    return "".join(f'<text x="{cx:.1f}" y="{y0 + i * lh:.1f}" text-anchor="middle" class="{cls}">{escape(l)}</text>'
                   for i, l in enumerate(lines))


# ---------------- icons ----------------
def envelope(cx, cy, s=1.0, filled=False):
    w, h = 16 * s, 11 * s
    x, y = cx - w / 2, cy - h / 2
    fill = 'class="ink"' if filled else 'fill="var(--bp-paper)" stroke="var(--bp-ink)" stroke-width="1.4"'
    line = "var(--bp-paper)" if filled else "var(--bp-ink)"
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {fill}/>'
            f'<polyline points="{x:.1f},{y:.1f} {cx:.1f},{cy + 1:.1f} {x + w:.1f},{y:.1f}" fill="none" stroke="{line}" stroke-width="1.4"/>')


def clock(cx, cy, r):
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" class="shape thin"/>'
    import math
    for i in range(12):
        a = math.radians(i * 30)
        out += (f'<line x1="{cx + math.cos(a) * r * .72:.1f}" y1="{cy + math.sin(a) * r * .72:.1f}" '
                f'x2="{cx + math.cos(a) * r * .92:.1f}" y2="{cy + math.sin(a) * r * .92:.1f}" stroke="var(--bp-ink)" stroke-width="1"/>')
    return out + f'<polyline points="{cx},{cy - r * .6:.1f} {cx},{cy} {cx + r * .45:.1f},{cy + r * .15:.1f}" class="line"/>'


def bolt(cx, cy, filled=False):
    pts = f"{cx - 6},{cy + 6} {cx - 2},{cy - 5} {cx + 2},{cy + 1} {cx + 6},{cy - 7} {cx + 2},{cy + 5} {cx - 2},{cy - 1}"
    style = 'class="ink"' if filled else 'fill="none" stroke="var(--bp-ink)" stroke-width="1.4"'
    return f'<polygon points="{pts}" {style}/>'


def user_icon(x, y):
    return (f'<circle cx="{x + 12}" cy="{y + 10}" r="4" class="shape thin"/>'
            f'<path d="M{x + 4},{y + 23} C{x + 4},{y + 16} {x + 8},{y + 14.5} {x + 12},{y + 14.5} '
            f'C{x + 16},{y + 14.5} {x + 20},{y + 16} {x + 20},{y + 23} Z" class="shape thin"/>')


def gear_icon(x, y):
    import math
    out = ""
    for cx, cy in ((x + 11, y + 11), (x + 17, y + 17)):
        for i in range(8):
            a = math.radians(i * 45)
            out += (f'<line x1="{cx + math.cos(a) * 4:.1f}" y1="{cy + math.sin(a) * 4:.1f}" '
                    f'x2="{cx + math.cos(a) * 7:.1f}" y2="{cy + math.sin(a) * 7:.1f}" stroke="var(--bp-ink)" stroke-width="2"/>')
        out += f'<circle cx="{cx}" cy="{cy}" r="4.5" class="shape thin"/><circle cx="{cx}" cy="{cy}" r="1.8" class="ink"/>'
    return out


def hand_icon(x, y):
    return (f'<path d="M{x + 4},{y + 12} h9 l-3,-4 q1,-2 3,-1 l6,5 h5 q2,1.5 0,3 h-5 m0,0 h4 q2,1.5 0,3 h-4 '
            f'm0,0 h3 q2,1.5 0,3 h-12 q-4,0 -4,-4 z" class="shape thin"/>')


def table_icon(x, y):
    return (f'<rect x="{x + 4}" y="{y + 5}" width="18" height="13" class="shape thin"/>'
            f'<rect x="{x + 4}" y="{y + 5}" width="18" height="4" class="ink"/>'
            f'<line x1="{x + 4}" y1="{y + 13.5}" x2="{x + 22}" y2="{y + 13.5}" stroke="var(--bp-ink)"/>'
            f'<line x1="{x + 10}" y1="{y + 9}" x2="{x + 10}" y2="{y + 18}" stroke="var(--bp-ink)"/>')


def script_icon(x, y):
    return (f'<path d="M{x + 7},{y + 4} h12 q-4,4 -1,8 q3,4 -1,8 h-12 q4,-4 1,-8 q-3,-4 1,-8 z" class="shape thin"/>'
            f'<line x1="{x + 8}" y1="{y + 9}" x2="{x + 15}" y2="{y + 9}" stroke="var(--bp-ink)"/>'
            f'<line x1="{x + 9}" y1="{y + 14}" x2="{x + 16}" y2="{y + 14}" stroke="var(--bp-ink)"/>')


TASK_ICON = {"user_task": user_icon, "service_task": gear_icon, "manual_task": hand_icon,
             "business_rule_task": table_icon, "script_task": script_icon,
             "send_task": lambda x, y: envelope(x + 13, y + 11, 1.0, True),
             "receive_task": lambda x, y: envelope(x + 13, y + 11, 1.0, False)}


def draw_task(n, x, y, w, h):
    t = n["type"]
    thick = ' style="stroke-width:5"' if t == "call_activity" else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="shape"{thick}/>'
    if t in TASK_ICON:
        out += TASK_ICON[t](x, y)
    if t in ("subprocess", "call_activity"):
        bx, by = x + w / 2 - 7, y + h - 17
        out += (f'<rect x="{bx}" y="{by}" width="14" height="14" class="shape thin"/>'
                f'<line x1="{bx + 3}" y1="{by + 7}" x2="{bx + 11}" y2="{by + 7}" stroke="var(--bp-ink)" stroke-width="1.5"/>'
                f'<line x1="{bx + 7}" y1="{by + 3}" x2="{bx + 7}" y2="{by + 11}" stroke="var(--bp-ink)" stroke-width="1.5"/>')
    shift = 4 if t in TASK_ICON else 0
    lines = wrap(n.get("name", ""), 13)[:4]
    return out + tspans(x + w / 2 + shift, y + h / 2 + (4 if t in TASK_ICON else 0), lines, "t-node")


def draw_event(n, x, y, w, h, interrupting=True):
    t = n["type"]
    cx, cy, r = x + w / 2, y + h / 2, w / 2
    defn = EVENTS[t][1] if t in EVENTS else BOUNDARY.get(t)
    if t.startswith("end"):
        out = f'<circle cx="{cx}" cy="{cy}" r="{r}" class="shape end"/>'
    elif t.startswith("start"):
        out = f'<circle cx="{cx}" cy="{cy}" r="{r}" class="shape"/>'
    else:  # intermediate / boundary: viền đôi
        dash = " dashed" if not interrupting else ""
        out = (f'<circle cx="{cx}" cy="{cy}" r="{r}" class="shape thin{dash}"/>'
               f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" class="shape thin{dash}" style="fill:none"/>')
    throwing = t.startswith("end") or t == "message_throw"
    if defn == "message":
        out += envelope(cx, cy, 0.95, throwing)
    elif defn == "timer":
        out += clock(cx, cy, r - 7)
    elif defn == "error":
        out += bolt(cx, cy, throwing)
    elif defn == "terminate":
        out += f'<circle cx="{cx}" cy="{cy}" r="{r - 8}" class="ink"/>'
    return out


def draw_gateway(n, x, y, w, h):
    cx, cy, s = x + w / 2, y + h / 2, w / 2
    out = f'<polygon points="{cx},{cy - s} {cx + s},{cy} {cx},{cy + s} {cx - s},{cy}" class="shape"/>'
    t, k = n["type"], s / 2.8
    if t == "xor":
        out += (f'<line x1="{cx - k}" y1="{cy - k}" x2="{cx + k}" y2="{cy + k}" stroke="var(--bp-ink)" stroke-width="4"/>'
                f'<line x1="{cx + k}" y1="{cy - k}" x2="{cx - k}" y2="{cy + k}" stroke="var(--bp-ink)" stroke-width="4"/>')
    elif t == "and":
        k = s / 2.2
        out += (f'<line x1="{cx}" y1="{cy - k}" x2="{cx}" y2="{cy + k}" stroke="var(--bp-ink)" stroke-width="4"/>'
                f'<line x1="{cx - k}" y1="{cy}" x2="{cx + k}" y2="{cy}" stroke="var(--bp-ink)" stroke-width="4"/>')
    elif t == "or":
        out += f'<circle cx="{cx}" cy="{cy}" r="{s / 2.3}" fill="none" stroke="var(--bp-ink)" stroke-width="3.5"/>'
    elif t == "event_based":
        out += (f'<circle cx="{cx}" cy="{cy}" r="{s / 1.9}" fill="none" stroke="var(--bp-ink)" stroke-width="1.3"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{s / 2.4}" fill="none" stroke="var(--bp-ink)" stroke-width="1.3"/>'
                f'<polygon points="{cx},{cy - 6} {cx + 6},{cy - 2} {cx + 4},{cy + 5} {cx - 4},{cy + 5} {cx - 6},{cy - 2}" class="line"/>')
    return out


def pts_attr(pts):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)


def label_pos(pts):
    """Vị trí nhãn: giữa đoạn dài nhất."""
    best, bi = -1, 0
    for i in range(len(pts) - 1):
        d = abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1])
        if d > best:
            best, bi = d, i
    (x1, y1), (x2, y2) = pts[bi], pts[bi + 1]
    return (x1 + x2) / 2, (y1 + y2) / 2, abs(y2 - y1) > abs(x2 - x1)


def render(spec, embed_css=True):
    G = geometry(spec)
    geo, W, H = G["geo"], G["width"], G["height"]
    nodes = {n["id"]: n for n in spec["nodes"]}
    css = open(THEME, encoding="utf-8").read() if embed_css else ""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" class="bpmn-svg" viewBox="-10 -10 {W + 20} {H + 10}" '
         f'role="img" aria-label="{escape(spec.get("name", "BPMN"))}">',
         f"<style>{css}</style>" if css else "",
         '<defs>'
         '<marker id="bp-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="11" markerHeight="11" '
         'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L10,5 L0,9 z" class="ink"/></marker>'
         '<marker id="bp-msg-end" viewBox="0 0 12 12" refX="11.5" refY="6" markerWidth="13" markerHeight="13" '
         'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L11,6 L1,11 z" fill="var(--bp-paper)" stroke="var(--bp-ink)" stroke-width="1.3"/></marker>'
         '<marker id="bp-msg-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="10" markerHeight="10" '
         'markerUnits="userSpaceOnUse" orient="auto"><circle cx="5" cy="5" r="3.8" fill="var(--bp-paper)" stroke="var(--bp-ink)" stroke-width="1.3"/></marker>'
         '</defs>',
         f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 10}" class="bg"/>']
    # pools
    px, py, pw, ph = G["main"]
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" class="pool"/>')
    o.append(f'<rect x="{px}" y="{py}" width="30" height="{ph}" class="pool-head"/>')
    o.append(f'<text x="{px + 15}" y="{py + ph / 2}" text-anchor="middle" dominant-baseline="middle" class="t-pool" '
             f'transform="rotate(-90 {px + 15} {py + ph / 2})">{escape(spec.get("name", ""))[:60]}</text>')
    for i, l in enumerate(spec["lanes"]):
        lx, ly, lw, lh = G["lanes"][l["id"]]
        o.append(f'<rect x="{lx}" y="{ly}" width="30" height="{lh}" class="lane-head"/>')
        o.append(f'<text x="{lx + 15}" y="{ly + lh / 2}" text-anchor="middle" dominant-baseline="middle" class="t-lane" '
                 f'transform="rotate(-90 {lx + 15} {ly + lh / 2})">{escape(l["name"])}</text>')
        if i:
            o.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + lw}" y2="{ly}" class="lane-line"/>')
    for p in spec.get("pools", []):
        x, y, w, h = G["pools"][p["id"]]
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="ext-pool"/>')
        o.append(f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" class="t-pool">{escape(p["name"])}</text>')
    # sequence flows
    default_ids = set()
    for i, f in enumerate(spec["flows"]):
        fid = f.get("id", f"Flow_{i + 1}")
        pts = G["seq"][fid]
        o.append(f'<polyline points="{pts_attr(pts)}" class="flow" marker-end="url(#bp-arrow)"/>')
        if f.get("default"):
            default_ids.add(fid)
            (x1, y1), (x2, y2) = pts[0], pts[1]
            d = max(1, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5)
            mx, my = x1 + (x2 - x1) / d * 10, y1 + (y2 - y1) / d * 10
            o.append(f'<line x1="{mx - 5}" y1="{my + 6}" x2="{mx + 5}" y2="{my - 6}" stroke="var(--bp-ink)" stroke-width="2"/>')
        if f.get("name"):
            x, y, vertical = label_pos(pts)
            if vertical:
                o.append(f'<text x="{x + 6}" y="{y}" class="t-flow">{escape(f["name"])}</text>')
            else:
                o.append(f'<text x="{x}" y="{y - 6}" text-anchor="middle" class="t-flow">{escape(f["name"])}</text>')
    # message flows
    for m in spec.get("messages", []):
        pts = G["msg"][m["id"]]
        o.append(f'<polyline points="{pts_attr(pts)}" class="msg" marker-start="url(#bp-msg-start)" marker-end="url(#bp-msg-end)"/>')
        if m.get("name"):
            x, y = pts[0][0], (pts[0][1] + pts[-1][1]) / 2
            o.append(f'<text x="{x + 6}" y="{y}" class="t-msg">{escape(m["name"])}</text>')
    # nodes (boundary last so they sit on top of tasks)
    for n in sorted(spec["nodes"], key=lambda n: n["type"] in BOUNDARY):
        x, y, w, h = geo[n["id"]]
        t = n["type"]
        if t in TASKS:
            o.append(draw_task(n, x, y, w, h))
        elif t in GATES:
            o.append(draw_gateway(n, x, y, w, h))
            if n.get("name"):
                o.append(tspans(x + w / 2, y - 18, wrap(n["name"], 18)[:2], "t-label", 13))
        else:
            o.append(draw_event(n, x, y, w, h, n.get("interrupting", True) is not False))
            if n.get("name") and t in BOUNDARY:   # nhãn boundary đặt bên phải để không đè luồng ngoại lệ
                for i, line in enumerate(wrap(n["name"], 16)[:2]):
                    o.append(f'<text x="{x + w + 4}" y="{y + h + 4 + i * 13}" class="t-label">{escape(line)}</text>')
            elif n.get("name"):
                lines = wrap(n["name"], 16)[:2]
                o.append(tspans(x + w / 2, y + h + 12 + (len(lines) - 1) * 7, lines, "t-label", 13))
    o.append("</svg>")
    return "".join(o)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[2], "w", encoding="utf-8").write(render(spec))
    print(f"Đã ghi {sys.argv[2]}")


if __name__ == "__main__":
    main()
