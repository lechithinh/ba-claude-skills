#!/usr/bin/env python3
"""Xuất một trang HTML độc lập: sơ đồ BPMN + nút chọn kịch bản + animation token chạy
theo từng kịch bản (kèm câu thuyết minh từng bước). Mở bằng trình duyệt, không cần mạng.

    python3 build_token_page.py spec.json out.html          # kịch bản trong spec, thiếu thì tự sinh
    python3 build_token_page.py spec.json out.html --auto   # luôn tự sinh kịch bản

Kịch bản viết trong spec như mô tả ở simulate_tokens.py.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from simulate_tokens import KIND, Model, auto_scenarios, simulate  # noqa: E402
from spec_to_bpmn import BOUNDARY, TASKS, geometry  # noqa: E402
from spec_to_svg import render  # noqa: E402

PLAYER = os.path.join(HERE, "..", "assets", "token-player.js")


def steps_for(spec, M, G, result):
    geo = G["geo"]
    flows = {f["id"]: f for f in spec["flows"]}
    msgs = {m["id"]: m for m in spec.get("messages", [])}
    c = lambda k: [geo[k][0] + geo[k][2] / 2, geo[k][1] + geo[k][3] / 2]
    nm = lambda k: html.escape(M.name(k))
    S = []
    say = lambda t: S.append({"t": "say", "text": t})
    for e in result["events"]:
        t = e["t"]
        if t == "start":
            S.append({"t": "spawn", "tok": e["tok"], "at": c(e["node"])})
            S.append({"t": "ring", "at": c(e["node"])})
            say(f"Token xuất hiện ở start event <b>“{nm(e['node'])}”</b>.")
            S.append({"t": "wait", "ms": 600})
        elif t == "move":
            f = flows[e["flow"]]
            pts = [c(f["from"])] + [list(p) for p in G["seq"][e["flow"]]] + [c(f["to"])]
            S.append({"t": "move", "tok": e["tok"], "pts": pts})
        elif t == "work":
            n = M.nodes[e["node"]]
            if n["type"] in TASKS:
                say(f"{KIND.get(n['type'], 'Task').capitalize()} <b>“{nm(e['node'])}”</b>.")
                x, y, w, h = geo[e["node"]]
                S.append({"t": "busy", "box": [x, y, w, h], "ms": 800})
            elif not n["type"].startswith("end"):
                say(f"{KIND.get(n['type'], 'Event').capitalize()} <b>“{nm(e['node'])}”</b>.")
                S.append({"t": "ring", "at": c(e["node"])})
                S.append({"t": "wait", "ms": 500})
        elif t in ("msg_out", "msg_in"):
            m = msgs[e["msg"]]
            other = m["to"] if t == "msg_out" else m["from"]
            verb = "Gửi" if t == "msg_out" else "Nhận"
            say(f"{verb} message <b>“{html.escape(m.get('name') or m['id'])}”</b> "
                f"{'sang' if t == 'msg_out' else 'từ'} {nm(other)}.")
            S.append({"t": "msg", "pts": [list(p) for p in G["msg"][m["id"]]]})
        elif t == "choice":
            say(f"Gateway <b>“{nm(e['node'])}”</b>: đi nhánh <b>“{html.escape(e['label'])}”</b>.")
            S.append({"t": "ring", "at": c(e["node"])})
            S.append({"t": "wait", "ms": 600})
        elif t == "split":
            S.append({"t": "fade", "tok": e["tok"]})
            S.append({"t": "ring", "at": c(e["node"])})
            for k in e["toks"]:
                S.append({"t": "spawn", "tok": k, "at": c(e["node"])})
            if e.get("implicit"):
                say(f"<b>“{nm(e['node'])}”</b> có nhiều luồng ra không qua gateway: <b>mọi nhánh cùng chạy</b>.")
            else:
                say(f"<b>{'OR' if e.get('or') else 'AND'} tách</b>: một token thành {len(e['toks'])}, các nhánh chạy song song.")
            S.append({"t": "wait", "ms": 600})
        elif t == "join_wait":
            need = f" ({e['have']}/{e['need']} nhánh)" if e.get("need") else ""
            say(f"Token chờ ở gateway gộp <b>“{nm(e['node'])}”</b>{need}.")
            S.append({"t": "wait", "ms": 500})
        elif t == "join":
            for k in e["toks"]:
                S.append({"t": "fade", "tok": k})
            S.append({"t": "spawn", "tok": e["new"], "at": c(e["node"])})
            S.append({"t": "ring", "at": c(e["node"])})
            say("Đủ các nhánh: gateway gộp cho đi tiếp <b>một</b> token.")
            S.append({"t": "wait", "ms": 600})
        elif t == "boundary":
            b = M.nodes[e["node"]]
            S.append({"t": "ring", "at": c(e["node"]), "color": "pink" if e["interrupting"] else "yellow"})
            if e["interrupting"]:
                say(f"Boundary <b>“{nm(e['node'])}”</b> kích hoạt (viền liền, <b>ngắt</b>): task bị huỷ, token đi luồng ngoại lệ.")
                S.append({"t": "kill", "tok": e["tok"]})
                S.append({"t": "spawn", "tok": e["new"], "at": c(e["node"])})
            else:
                say(f"Boundary <b>“{nm(e['node'])}”</b> kích hoạt (viền đứt, <b>không ngắt</b>): task vẫn chạy, thêm một token vàng.")
                S.append({"t": "spawn", "tok": e["new"], "at": c(e["node"]), "color": "yellow"})
            S.append({"t": "wait", "ms": 700})
        elif t == "end":
            S.append({"t": "ring", "at": c(e["node"])})
            say(f"Kết thúc ở end event <b>“{nm(e['node'])}”</b>.")
            S.append({"t": "wait", "ms": 700})
            S.append({"t": "fade", "tok": e["tok"]})
        elif t == "kill":
            S.append({"t": "kill", "tok": e["tok"]})
        elif t == "stuck":
            say(f"Token <b>kẹt</b> ở <b>“{nm(e['node'])}”</b>: {html.escape(e['reason'])}. Đây là lỗ hổng cần xử lý.")
            S.append({"t": "stuck", "tok": e["tok"], "at": c(e["node"])})
    return S


PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{ --ink:#1B1B1F; --bg:#F7F5EF; --green:#1F8A4C; --pink:#E8508F; }}
*{{ box-sizing:border-box; }}
body{{ margin:0; background:var(--bg); color:var(--ink); font-family:"Be Vietnam Pro","Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
main{{ max-width:1500px; margin:0 auto; padding:24px 16px 40px; }}
h1{{ font-size:26px; margin:0 0 6px; }}
.hint{{ margin:0 0 14px; color:#55555f; }}
.bar{{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px; }}
.bar button{{ font:inherit; font-weight:700; border:2px solid var(--ink); background:#fff; padding:8px 14px; cursor:pointer; border-radius:6px; }}
.bar button.on{{ background:var(--green); color:#fff; }}
.cap{{ min-height:28px; font-size:18px; margin:4px 0 12px; }}
.cap b{{ color:var(--green); }}
.fig{{ border:2px solid var(--ink); background:#fff; padding:8px; border-radius:8px; overflow:auto; }}
.fig svg{{ width:100%; height:auto; display:block; min-width:900px; }}
table{{ border-collapse:collapse; margin-top:18px; width:100%; font-size:14px; }}
th,td{{ border:1px solid #c9c4b6; padding:6px 10px; text-align:left; vertical-align:top; }}
th{{ background:#ece7da; }}
.bad{{ color:#b0174f; font-weight:700; }}
</style></head><body><main>
<h1>{title}</h1>
<p class="hint">Chọn một kịch bản để xem token chạy. Chấm tròn là <b>token</b>; phong bì vàng là <b>message</b> giữa các pool; viền hồng nhấp nháy là task đang làm.</p>
<div class="bar">{buttons}</div>
<p class="cap" id="cap">Chọn một kịch bản ở trên.</p>
<div class="fig">{svg}</div>
<table><thead><tr><th>Kịch bản</th><th>Kết cục</th><th>Vấn đề</th></tr></thead><tbody>{rows}</tbody></table>
</main>
<script>{player}</script>
<script>
tokenPlayer({{ svg: document.querySelector('.fig svg'), caption: document.getElementById('cap'),
  buttons: document.querySelectorAll('.bar [data-sc]'), scenarios: {data} }});
</script></body></html>
"""


def build(spec, use_auto=False):
    M = Model(spec)
    G = geometry(spec)
    scenarios = auto_scenarios(M) if (use_auto or not spec.get("scenarios")) else spec["scenarios"]
    data, buttons, rows = {}, [], []
    for sc in scenarios:
        r = simulate(Model(spec), sc)
        data[sc["id"]] = steps_for(spec, M, G, r)
        label = html.escape(f"{sc['id']} · {sc.get('name', '')}")
        buttons.append(f'<button type="button" data-sc="{html.escape(sc["id"])}">{label}</button>')
        ends = ", ".join(f"“{html.escape(M.name(e))}”" for e in r["ends"]) or "–"
        probs = "; ".join(f"kẹt ở “{html.escape(M.name(s['node']))}”: {html.escape(s['reason'])}" for s in r["stuck"])
        if sc.get("expect") and sc["expect"] not in r["ends"]:
            probs = (probs + "; " if probs else "") + f"không tới “{html.escape(M.name(sc['expect']))}” như mong đợi"
        rows.append(f"<tr><td>{label}</td><td>{ends}</td><td class=\"{'bad' if probs else ''}\">{probs or 'Không'}</td></tr>")
    return PAGE.format(title=html.escape(spec.get("name", "Quy trình BPMN")), buttons="".join(buttons),
                       svg=render(spec), rows="".join(rows), player=open(PLAYER, encoding="utf-8").read(),
                       data=json.dumps(data, ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    spec = json.load(open(args[0], encoding="utf-8"))
    open(args[1], "w", encoding="utf-8").write(build(spec, "--auto" in args))
    print(f"Đã ghi {args[1]}")


if __name__ == "__main__":
    main()
