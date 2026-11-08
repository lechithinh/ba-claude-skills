#!/usr/bin/env python3
"""Generate the animated BPMN token demo for the README (pure CSS SVG, no JavaScript) and, optionally,
an interactive page. GitHub shows the SVG through an <img> tag. The token path comes from the real
simulation in skills/bpmn-modeling/scripts/simulate_tokens.py, not from a hand-drawn animation.

    python3 scripts/make_token_demo.py spec.json out.svg --scenarios A,E --badge "AS-IS" --bad
    python3 scripts/make_token_demo.py spec.json out.html --page          # interactive page, all scenarios

    --scenarios  scenarios played one after another in a single loop (default: all)
    --badge      label at the top left, for example "AS-IS" or "TO-BE"
    --bad        red badge (default green)
    --speed      coordinate units per ms (default 0.75)
    --lang       en (default) or vi: language of captions and labels (en rewrites the Vietnamese
                 captions of steps_for from the simulation events; node names come from the spec)
"""
import html
import os
import re
import sys
import textwrap
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "skills", "bpmn-modeling", "scripts")
sys.path.insert(0, SKILL)
import json  # noqa: E402

from build_token_page import PAGE, PLAYER, steps_for  # noqa: E402
from simulate_tokens import Model, auto_scenarios, simulate  # noqa: E402
from spec_to_bpmn import TASKS, geometry  # noqa: E402
from spec_to_svg import render  # noqa: E402

HEADER, FOOTER = 66, 92
GREEN, PINK, YELLOW, RED, INK = "#1F8A4C", "#E8508F", "#F2C94C", "#C81E3A", "#1B1B1F"
COLORS = {"green": GREEN, "yellow": YELLOW, "pink": PINK, "red": RED}
MIN_CAP, HOLD, GAP = 1250, 1800, 350


class Track:
    """An animated object: a list of (t, state) points that becomes @keyframes."""

    def __init__(self, kind, x, y, color=GREEN):
        self.kind, self.pts, self.last = kind, [], None
        self.set(0, x=x, y=y, op=0, color=color)

    def set(self, t, jump=True, **kw):
        s = dict(self.last or {})
        s.update(kw)
        if self.last is not None and jump:
            self.pts.append((max(t - 1, self.pts[-1][0]), dict(self.last)))
        self.pts.append((max(t, self.pts[-1][0] + 0.5 if self.pts else 0), s))
        self.last = s


def clean(text):
    text = html.unescape(re.sub(r"</?b>", "", text))
    return re.sub(r"\s+", " ", text).strip()


STR = {
    "en": {"scenario": "Scenario", "stuck": "STUCK", "title": "Token run on a BPMN diagram",
           "hint": "Pick a scenario to watch the token run. The dot is a <b>token</b>; the yellow envelope is a "
                   "<b>message</b> between pools; the pink pulsing border marks the task being worked on.",
           "pick": "Pick a scenario above.", "cols": ("Scenario", "Outcome", "Problem"), "none": "None"},
    "vi": {"scenario": "Kịch bản", "stuck": "KẸT", "title": "Token chạy trên sơ đồ BPMN"},
}
KIND_EN = {"task": "Task", "user_task": "User task", "manual_task": "Manual task", "service_task": "Service task",
           "send_task": "Send task", "receive_task": "Receive task", "script_task": "Script task",
           "business_rule_task": "Business rule task", "subprocess": "Sub-process", "call_activity": "Call activity",
           "timer": "Timer event", "message_catch": "Message catch event", "message_throw": "Message throw event"}


VI_CHARS = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)


def strip_vi_comments(text):
    """Remove CSS/JS comments written in Vietnamese by the skill, so an English demo has no Vietnamese in its source."""
    text = re.sub(r"/\*.*?\*/", lambda m: "" if VI_CHARS.search(m.group(0)) else m.group(0), text, flags=re.S)
    return re.sub(r"[ \t]//[^\n]*", lambda m: "" if VI_CHARS.search(m.group(0)) else m.group(0), text)


def q(text):
    """Highlighted, escaped name for captions: <b>“name”</b>."""
    return f"<b>“{html.escape(text)}”</b>"


def english_says(spec, M, res):
    """One English caption per event that steps_for turns into a 'say' step, in the same order."""
    msgs = {m["id"]: m for m in spec.get("messages", [])}
    out = []
    for e in res["events"]:
        t = e["t"]
        if t == "start":
            out.append(f"Token appears at start event {q(M.name(e['node']))}.")
        elif t == "work":
            n = M.nodes[e["node"]]
            if n["type"] in TASKS:
                out.append(f"{KIND_EN.get(n['type'], 'Task')} {q(M.name(e['node']))}.")
            elif not n["type"].startswith("end"):
                out.append(f"{KIND_EN.get(n['type'], 'Event')} {q(M.name(e['node']))}.")
        elif t in ("msg_out", "msg_in"):
            m = msgs[e["msg"]]
            name = m.get("name") or m["id"]
            if t == "msg_out":
                out.append(f"Send message {q(name)} to {html.escape(M.name(m['to']))}.")
            else:
                out.append(f"Receive message {q(name)} from {html.escape(M.name(m['from']))}.")
        elif t == "choice":
            out.append(f"Gateway {q(M.name(e['node']))}: takes branch {q(e['label'])}.")
        elif t == "split":
            out.append(f"{'OR' if e.get('or') else 'AND'} split: one token becomes {len(e['toks'])}, branches run in parallel.")
        elif t == "join_wait":
            out.append(f"Token waits at the joining gateway {q(M.name(e['node']))}.")
        elif t == "join":
            out.append("All branches arrived: the joining gateway releases a single token.")
        elif t == "boundary":
            if e["interrupting"]:
                out.append(f"Boundary {q(M.name(e['node']))} fires (solid border, interrupting): "
                           "the task is cancelled and the token follows the exception path.")
            else:
                out.append(f"Boundary {q(M.name(e['node']))} fires (dashed border, non-interrupting): "
                           "the task keeps running and a second token starts.")
        elif t == "end":
            out.append(f"Ends at end event {q(M.name(e['node']))}.")
        elif t == "stuck":
            msg = re.findall(r"“([^”]+)”", e.get("reason", ""))
            why = f"waiting for message {q(msg[0])} that never arrives" if msg else html.escape(e.get("reason", ""))
            out.append(f"Token is <b>stuck</b> at {q(M.name(e['node']))}: {why}. This is the gap to fix.")
    return out


def localize(steps, spec, M, res):
    """Replace the Vietnamese captions of steps_for with English ones built from the simulation events."""
    texts = english_says(spec, M, res)
    says = [s for s in steps if s["t"] == "say"]
    if len(says) != len(texts):
        sys.exit(f"Internal mismatch: {len(says)} captions vs {len(texts)} events. A step type is not covered by english_says().")
    for st, tx in zip(says, texts):
        st["text"] = tx
    return steps


def build(spec, ids, badge, bad, speed, lang="en"):
    G = geometry(spec)
    allsc = {s["id"]: s for s in spec.get("scenarios", [])}
    ids = ids or list(allsc)
    tracks, rings, busys, caps, heads, marks = [], [], [], [], [], []
    t = 0.0
    for si, sid in enumerate(ids):
        sc = allsc[sid]
        res = simulate(Model(spec), sc)
        steps = steps_for(spec, Model(spec), G, res)
        if lang == "en":
            steps = localize(steps, spec, Model(spec), res)
        scen_start, cur, toks = t, None, {}

        def close_caption(upto):
            nonlocal t, cur
            if cur:
                t = max(t, cur["start"] + MIN_CAP, upto)
                cur["end"] = t
                caps.append(cur)
                cur = None

        for i, st in enumerate(steps):
            k = st["t"]
            if k == "say":
                close_caption(t)
                stuck_next = any(s["t"] == "stuck" for s in steps[i + 1:i + 3])
                cur = {"start": t, "text": clean(st["text"]), "bad": stuck_next}
            elif k == "spawn":
                key = (si, st["tok"])
                tr = Track("tok", st["at"][0], st["at"][1], COLORS.get(st.get("color", "green"), GREEN))
                tr.set(t, op=1)
                tracks.append(tr)
                toks[key] = tr
            elif k == "move":
                tr = toks[(si, st["tok"])]
                pts = st["pts"]
                for a, b in zip(pts, pts[1:]):
                    d = max(abs(b[0] - a[0]) + abs(b[1] - a[1]), 1) / speed
                    t += d
                    tr.set(t, jump=False, x=b[0], y=b[1])
            elif k == "msg":
                tr = Track("msg", st["pts"][0][0], st["pts"][0][1], YELLOW)
                tr.set(t, op=1)
                for a, b in zip(st["pts"], st["pts"][1:]):
                    t += max(abs(b[0] - a[0]) + abs(b[1] - a[1]), 1) / (speed * 0.8)
                    tr.set(t, jump=False, x=b[0], y=b[1])
                tr.set(t + 250, op=0)
                tracks.append(tr)
            elif k == "busy":
                ms = min(st.get("ms", 800), 450)
                busys.append((t, t + ms, st["box"]))
                t += ms
            elif k == "ring":
                rings.append((t, st["at"], COLORS.get(st.get("color", "green"), GREEN)))
            elif k == "wait":
                t += st["ms"] * 0.5
            elif k in ("fade", "kill"):
                tr = toks.get((si, st["tok"]))
                if tr:
                    if k == "kill":
                        tr.set(t, color=PINK)
                        t += 250
                    tr.set(t + 400, jump=False, op=0)
            elif k == "stuck":
                tr = toks[(si, st["tok"])]
                tr.set(t, color=RED)
                x, y = st["at"]
                marks.append((t, x, y))
                for j in range(4):
                    rings.append((t + j * 800, st["at"], RED))
                t += 4 * 800
        close_caption(t)
        for tr in toks.values():
            if tr.last.get("op"):
                tr.set(t + 300, jump=False, op=0)
        t += 300
        heads.append((scen_start, t, f"{STR[lang]['scenario']} {sid} · {sc.get('name', '')}", bool(res["stuck"])))
        t += GAP
    t += HOLD - GAP
    return tracks, rings, busys, caps, heads, marks, t


def kf(name, T, points, fmt):
    body = "".join(f"{round(100 * min(p, T) / T, 3)}%{{{fmt(s)}}}" for p, s in points)
    return f"@keyframes {name}{{{body}}}"


def make(spec, ids, badge, bad, speed, lang="en"):
    svg = render(spec)
    m = re.match(r'<svg ([^>]*?)viewBox="(-?\d+) (-?\d+) (\d+) (\d+)"([^>]*)>', svg)
    pre, vx, vy, vw, vh, post = m.group(1), *map(int, m.groups()[1:5]), m.group(6)
    inner = svg[m.end():].rsplit("</svg>", 1)[0]
    tracks, rings, busys, caps, heads, marks, T = build(spec, ids, badge, bad, speed, lang)
    T = max(T, 1000) + 500
    css, nodes, n = [], [], 0

    def anim(name):
        return f'style="animation:{name} {T / 1000:.2f}s linear infinite"'

    # tokens and messages
    for tr in tracks:
        n += 1
        nm = f"k{n}"
        pts = tr.pts + [(T, {**tr.last, "op": 0})]
        css.append(kf(nm, T, pts, lambda s: f"transform:translate({s['x']:.1f}px,{s['y']:.1f}px);opacity:{s['op']};fill:{s['color']}"))
        if tr.kind == "tok":
            nodes.append(f'<circle class="tok" r="11" {anim(nm)}/>')
        else:
            nodes.append(f'<rect class="env" x="-11" y="-7" width="22" height="14" rx="2" {anim(nm)}/>')
    # rings
    for t0, (x, y), col in rings:
        n += 1
        nm = f"k{n}"
        pts = [(0, (0, .6)), (max(t0 - 1, 0), (0, .6)), (t0, (1, .6)), (t0 + 900, (0, 2.3)), (T, (0, 2.3))]
        css.append(kf(nm, T, pts, lambda s: f"opacity:{s[0]};transform:scale({s[1]})"))
        nodes.append(f'<circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="24" stroke="{col}" {anim(nm)}/>')
    # task being worked on
    for t0, t1, (x, y, w, h) in busys:
        n += 1
        nm = f"k{n}"
        pts = [(0, .0), (max(t0 - 1, 0), 0), (t0, .35), ((t0 + t1) / 2, .95), (t1, .35), (t1 + 1, 0), (T, 0)]
        css.append(kf(nm, T, pts, lambda s: f"opacity:{s}"))
        nodes.append(f'<rect class="busy" x="{x - 3:.1f}" y="{y - 3:.1f}" width="{w + 6:.1f}" height="{h + 6:.1f}" rx="10" {anim(nm)}/>')
    # STUCK badge
    for t0, x, y in marks:
        n += 1
        nm = f"k{n}"
        pts = [(0, 0), (max(t0 - 1, 0), 0), (t0, 1), (T - 600, 1), (T - 300, 0), (T, 0)]
        css.append(kf(nm, T, pts, lambda s: f"opacity:{s}"))
        nodes.append(f'<g {anim(nm)}><rect x="{x - 40:.1f}" y="{y - 84:.1f}" width="80" height="30" rx="15" fill="{RED}"/>'
                     f'<text class="stuck" x="{x:.1f}" y="{y - 63:.1f}" text-anchor="middle">{STR[lang]["stuck"]}</text></g>')
    # header (scenario name) and footer (caption)
    fy = vy + vh
    for t0, t1, label, stuck in heads:
        n += 1
        nm = f"k{n}"
        pts = [(0, 0), (max(t0 - 1, 0), 0), (t0, 1), (t1, 1), (t1 + 1, 0), (T, 0)]
        css.append(kf(nm, T, pts, lambda s: f"opacity:{s}"))
        nodes.append(f'<text class="head{" bad" if stuck else ""}" x="{vx + 150}" y="{vy - HEADER + 41}" {anim(nm)}>{escape(label)}</text>')
    for c in caps:
        n += 1
        nm = f"k{n}"
        pts = [(0, 0), (max(c["start"] - 1, 0), 0), (c["start"], 1), (c["end"] - 1, 1), (c["end"], 0), (T, 0)]
        css.append(kf(nm, T, pts, lambda s: f"opacity:{s}"))
        lines = textwrap.wrap(clean(c["text"]), 118)[:2] or [""]
        tsp = "".join(f'<tspan x="{vx + 24}" dy="{0 if i == 0 else 26}">{escape(l)}</tspan>' for i, l in enumerate(lines))
        y0 = fy + (40 if len(lines) == 2 else 52)
        nodes.append(f'<text class="cap{" bad" if c["bad"] else ""}" x="{vx + 24}" y="{y0}" {anim(nm)}>{tsp}</text>')

    # static frame: header and footer
    chip = RED if bad else GREEN
    frame = (
        f'<rect x="{vx}" y="{vy - HEADER}" width="{vw}" height="{HEADER}" fill="{INK}"/>'
        f'<rect x="{vx + 20}" y="{vy - HEADER + 16}" width="112" height="34" rx="17" fill="{chip}"/>'
        f'<text class="chip" x="{vx + 76}" y="{vy - HEADER + 39}" text-anchor="middle">{escape(badge)}</text>'
        f'<circle cx="{vx + vw - 250}" cy="{vy - HEADER + 33}" r="9" fill="{GREEN}" stroke="#fff" stroke-width="2"/>'
        f'<text class="legend" x="{vx + vw - 233}" y="{vy - HEADER + 38}">token</text>'
        f'<rect x="{vx + vw - 168}" y="{vy - HEADER + 26}" width="20" height="13" rx="2" fill="{YELLOW}" stroke="#fff" stroke-width="1.5"/>'
        f'<text class="legend" x="{vx + vw - 142}" y="{vy - HEADER + 38}">message</text>'
        f'<rect x="{vx}" y="{fy}" width="{vw}" height="{FOOTER}" fill="{INK}"/>'
    )
    style = (
        ".bpmn-svg .tok{stroke:#fff;stroke-width:3;filter:drop-shadow(0 2px 2px rgba(0,0,0,.35));opacity:0}"
        ".bpmn-svg .env{stroke:#1B1B1F;stroke-width:1.6;opacity:0}"
        ".bpmn-svg .ring{fill:none;stroke-width:5;opacity:0;transform-box:fill-box;transform-origin:center}"
        f".bpmn-svg .busy{{fill:none;stroke:{PINK};stroke-width:5;opacity:0}}"
        ".bpmn-svg .stuck{font:800 17px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#fff}"
        ".bpmn-svg .chip{font:800 16px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#fff;letter-spacing:.5px}"
        ".bpmn-svg .legend{font:600 14px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#d9d9e0}"
        ".bpmn-svg .head{font:700 21px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#fff;opacity:0}"
        f".bpmn-svg .head.bad{{fill:#FFB4C0}}"
        ".bpmn-svg .cap{font:500 19px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#fff;opacity:0}"
        ".bpmn-svg .cap.bad{fill:#FFB4C0;font-weight:700}"
        "@media (prefers-reduced-motion:reduce){.bpmn-svg .tok,.bpmn-svg .env,.bpmn-svg .ring,.bpmn-svg .busy,.bpmn-svg .head,.bpmn-svg .cap{animation:none!important}}"
    )
    title = f"{STR[lang]['title']}: {spec.get('name', '')} ({badge})"
    head = (f'<svg {pre}viewBox="{vx} {vy - HEADER} {vw} {vh + HEADER + FOOTER}"{post}>'
            .replace('aria-label="', 'aria-label="' + escape(title) + " - ", 1))
    out = (head + inner + frame + f"<style>{style}{''.join(css)}</style>"
           f'<g class="demo">{"".join(nodes)}</g></svg>')
    return strip_vi_comments(out) if lang == "en" else out


def make_page(spec, lang="en"):
    """Interactive page: scenario buttons, token player and an outcome table. English captions."""
    M, G = Model(spec), geometry(spec)
    scenarios = spec.get("scenarios") or auto_scenarios(M)
    data, buttons, rows = {}, [], []
    for sc in scenarios:
        res = simulate(Model(spec), sc)
        steps = steps_for(spec, M, G, res)
        data[sc["id"]] = localize(steps, spec, Model(spec), res) if lang == "en" else steps
        label = html.escape(f"{sc['id']} · {sc.get('name', '')}")
        buttons.append(f'<button type="button" data-sc="{html.escape(sc["id"])}">{label}</button>')
        ends = ", ".join(f"“{html.escape(M.name(e))}”" for e in res["ends"]) or "-"
        probs = []
        for st in res["stuck"]:
            msg = re.findall(r"“([^”]+)”", st.get("reason", ""))
            why = f"waiting for message “{html.escape(msg[0])}” that never arrives" if msg else html.escape(st.get("reason", ""))
            probs.append(f"stuck at “{html.escape(M.name(st['node']))}”: {why}")
        if sc.get("expect") and sc["expect"] not in res["ends"]:
            probs.append(f"did not reach “{html.escape(M.name(sc['expect']))}” as expected")
        text = "; ".join(probs)
        rows.append(f"<tr><td>{label}</td><td>{ends}</td><td class=\"{'bad' if text else ''}\">{text or STR['en']['none']}</td></tr>")
    page = PAGE
    c = STR["en"]["cols"]
    page = page.replace('<html lang="vi">', '<html lang="en">')
    page = re.sub(r'<p class="hint">.*?</p>', '<p class="hint">' + STR["en"]["hint"].replace("{", "{{").replace("}", "}}") + "</p>", page, flags=re.S)
    page = page.replace("Chọn một kịch bản ở trên.", STR["en"]["pick"])
    page = page.replace("<th>Kịch bản</th><th>Kết cục</th><th>Vấn đề</th>", f"<th>{c[0]}</th><th>{c[1]}</th><th>{c[2]}</th>")
    out = page.format(title=html.escape(spec.get("name", "BPMN process")), buttons="".join(buttons), svg=render(spec),
                      rows="".join(rows), player=open(PLAYER, encoding="utf-8").read(),
                      data=json.dumps(data, ensure_ascii=False))
    return strip_vi_comments(out) if lang == "en" else out


def main():
    args = sys.argv[1:]
    pos = [a for a in args if not a.startswith("--")]
    opt = {}
    for key in ("--scenarios", "--badge", "--speed", "--lang"):
        if key in args:
            opt[key] = args[args.index(key) + 1]
            pos = [p for p in pos if p != opt[key]]
    if len(pos) != 2:
        sys.exit(__doc__)
    spec = json.load(open(pos[0], encoding="utf-8"))
    ids = opt["--scenarios"].split(",") if "--scenarios" in opt else None
    lang = opt.get("--lang", "en")
    if lang not in STR:
        sys.exit("--lang must be en or vi")
    if "--page" in args:
        out = make_page(spec, lang)
    else:
        out = make(spec, ids, opt.get("--badge", "DEMO"), "--bad" in args, float(opt.get("--speed", 0.75)), lang)
    open(pos[1], "w", encoding="utf-8").write(out)
    print(f"Wrote {pos[1]} ({len(out) // 1024} KB)")


if __name__ == "__main__":
    main()
