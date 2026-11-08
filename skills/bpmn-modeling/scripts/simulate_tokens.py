#!/usr/bin/env python3
"""Chạy token qua sơ đồ (spec JSON) theo từng kịch bản để review quy trình:
kịch bản nào tới End nào, token kẹt ở đâu, nhánh nào chưa kịch bản nào đi qua.

    python3 simulate_tokens.py spec.json            # dùng "scenarios" trong spec, thiếu thì tự sinh
    python3 simulate_tokens.py spec.json --auto     # luôn tự sinh kịch bản phủ mọi nhánh/ngoại lệ
    python3 simulate_tokens.py spec.json --json trace.json   # ghi vết chi tiết (dùng cho build_token_page.py)

Kịch bản trong spec:
  "scenarios": [
    {"id": "A", "name": "Mua thành công", "choices": {"g1": "Có", "g2": "Có"}, "expect": "e1"},
    {"id": "B", "name": "Ghế bị giữ", "choices": {"g1": ["Không", "Có"]}},   # list = lần qua thứ 1, 2, ...
    {"id": "D", "name": "Quá 10 phút", "fire": ["b1"]},                     # boundary event kích hoạt
    {"id": "E", "name": "Không có kết quả", "silent": ["m2"]}                # message không bao giờ tới
  ]
choices: tên nhánh (nhãn flow) hoặc id node đích. Không chỉ định thì đi default flow, không có default thì nhánh đầu.
Gateway OR: list = các nhánh cùng được chọn trong một lần qua.
Thoát mã 1 nếu có kịch bản bị kẹt hoặc không tới End mong đợi.
"""
import json
import sys
from collections import defaultdict, deque

BOUNDARY_T = {"boundary_timer", "boundary_message", "boundary_error"}
GATES = {"xor", "and", "or", "event_based"}
MAX_VISITS = 25

KIND = {"user_task": "user task", "manual_task": "manual task", "service_task": "service task",
        "send_task": "send task", "receive_task": "receive task", "script_task": "script task",
        "business_rule_task": "business rule task", "subprocess": "sub-process",
        "call_activity": "call activity", "task": "task", "timer": "timer event",
        "message_catch": "message event (bắt)", "message_throw": "message event (ném)"}


class Model:
    def __init__(self, spec):
        self.spec = spec
        self.nodes = {n["id"]: n for n in spec["nodes"]}
        self.pools = {p["id"]: p for p in spec.get("pools", [])}
        self.out, self.inn = defaultdict(list), defaultdict(list)
        for i, f in enumerate(spec["flows"]):
            f.setdefault("id", f"Flow_{i + 1}")
            self.out[f["from"]].append(f)
            self.inn[f["to"]].append(f)
        self.bound = defaultdict(list)
        for n in spec["nodes"]:
            if n["type"] in BOUNDARY_T:
                self.bound[n["attached_to"]].append(n)
        self.msg_in, self.msg_out = defaultdict(list), defaultdict(list)
        for i, m in enumerate(spec.get("messages", [])):
            m.setdefault("id", f"m{i + 1}")
            if m["to"] in self.nodes:
                self.msg_in[m["to"]].append(m)
            if m["from"] in self.nodes:
                self.msg_out[m["from"]].append(m)

    def name(self, k):
        if k in self.nodes:
            return self.nodes[k].get("name") or k
        return self.pools.get(k, {}).get("name", k)


def simulate(model, sc):
    M = model
    ev = []                       # vết sự kiện
    q = deque()                   # (tid, node)
    visits = defaultdict(int)
    fired_used = set()
    and_wait = defaultdict(list)
    or_wait = defaultdict(list)
    alive = set()
    ends, stuck, notes = [], [], []
    tid_seq = [0]
    fire = set(sc.get("fire", []))
    silent = set(sc.get("silent", []))
    choices = sc.get("choices", {})

    def new_tid():
        tid_seq[0] += 1
        alive.add(tid_seq[0])
        return tid_seq[0]

    def kill(tid):
        alive.discard(tid)

    def go(tid, f):
        ev.append({"t": "move", "tok": tid, "flow": f["id"], "from": f["from"], "to": f["to"]})
        q.append((tid, f["to"]))

    def pick(node, outs):
        want = choices.get(node)
        n = M.nodes[node]
        if isinstance(want, list) and n["type"] != "or":
            idx = visits[node] - 1
            want = want[idx] if idx < len(want) else None
        def match(w):
            w = str(w).strip().lower()
            return [f for f in outs if (f.get("name") or "").strip().lower() == w or f["to"].lower() == w]
        if n["type"] == "or" and isinstance(want, list):
            got = [f for w in want for f in match(w)]
            if got:
                return got
        elif want is not None:
            got = match(want)
            if got:
                return got[:1]
            notes.append(f"“{M.name(node)}”: không có nhánh “{want}”, dùng nhánh mặc định")
        d = [f for f in outs if f.get("default")]
        if want is None and not d and len(outs) > 1:
            notes.append(f"“{M.name(node)}”: chưa chọn nhánh, đi nhánh đầu “{outs[0].get('name') or M.name(outs[0]['to'])}”")
        return d[:1] or outs[:1]

    starts = [n["id"] for n in M.spec["nodes"] if n["type"].startswith("start")]
    start = sc.get("start") or (starts[0] if starts else None)
    if not start:
        return {"events": ev, "ends": ends, "stuck": [{"node": None, "reason": "không có start event"}], "notes": notes}
    t0 = new_tid()
    ev.append({"t": "start", "tok": t0, "node": start})
    q.append((t0, start))
    first = True

    def step(tid, node):
        n = M.nodes[node]
        t = n["type"]
        visits[node] += 1
        if visits[node] > MAX_VISITS:
            stuck.append({"tok": tid, "node": node, "reason": f"vòng lặp quá {MAX_VISITS} lần (kiểm tra choices)"})
            ev.append({"t": "stuck", "tok": tid, "node": node, "reason": "vòng lặp không thoát"})
            kill(tid)
            return
        if t not in GATES and not t.startswith("start"):
            ev.append({"t": "work", "tok": tid, "node": node})
        elif t.startswith("start") and visits[node] > 1 or (t.startswith("start") and M.inn[node]):
            ev.append({"t": "pass", "tok": tid, "node": node})   # start nằm giữa luồng (lỗi B1) vẫn ghi nhận đã đi qua
        # boundary events gắn trên activity này
        interrupting = None
        for b in M.bound.get(node, []):
            if b["id"] in fire and b["id"] not in fired_used:
                fired_used.add(b["id"])
                if b.get("interrupting", True) is False:
                    nt = new_tid()
                    ev.append({"t": "boundary", "node": b["id"], "interrupting": False, "tok": tid, "new": nt})
                    if not M.out[b["id"]]:
                        stuck.append({"tok": nt, "node": b["id"], "reason": "boundary kích hoạt nhưng không có luồng ra"})
                        ev.append({"t": "stuck", "tok": nt, "node": b["id"], "reason": "boundary không có luồng ra"})
                        kill(nt)
                    for f in M.out[b["id"]]:
                        go(nt, f)
                elif interrupting is None:
                    interrupting = b
        if interrupting is not None:
            nt = new_tid()
            ev.append({"t": "boundary", "node": interrupting["id"], "interrupting": True, "tok": tid, "new": nt})
            kill(tid)
            if not M.out[interrupting["id"]]:
                stuck.append({"tok": nt, "node": interrupting["id"], "reason": "boundary kích hoạt nhưng không có luồng ra"})
                ev.append({"t": "stuck", "tok": nt, "node": interrupting["id"], "reason": "boundary không có luồng ra"})
                kill(nt)
            for f in M.out[interrupting["id"]]:
                go(nt, f)
            return
        # message phải tới mới chạy tiếp
        for m in M.msg_in.get(node, []):
            if m["id"] in silent or node in silent:
                stuck.append({"tok": tid, "node": node, "reason": f"chờ message “{m.get('name') or m['id']}” không bao giờ tới"})
                ev.append({"t": "stuck", "tok": tid, "node": node, "reason": f"chờ message “{m.get('name') or m['id']}”"})
                kill(tid)
                return
            ev.append({"t": "msg_in", "msg": m["id"], "tok": tid, "node": node})
        for m in M.msg_out.get(node, []):
            ev.append({"t": "msg_out", "msg": m["id"], "tok": tid, "node": node})
        if t.startswith("end"):
            ends.append(node)
            ev.append({"t": "end", "tok": tid, "node": node, "terminate": t == "end_terminate"})
            kill(tid)
            if t == "end_terminate":
                for other in list(alive):
                    ev.append({"t": "kill", "tok": other})
                    kill(other)
                q.clear()
            return
        outs = M.out[node]
        ins = M.inn[node]
        if t == "and" and len(ins) > 1:
            and_wait[node].append(tid)
            if len(and_wait[node]) < len(ins):
                ev.append({"t": "join_wait", "tok": tid, "node": node,
                           "have": len(and_wait[node]), "need": len(ins)})
                return
            merged = and_wait.pop(node)
            for x in merged:
                kill(x)
            tid = new_tid()
            ev.append({"t": "join", "node": node, "toks": merged, "new": tid})
        if t == "or" and len(ins) > 1:
            or_wait[node].append(tid)
            ev.append({"t": "join_wait", "tok": tid, "node": node, "have": len(or_wait[node]), "need": None})
            return
        if not outs:
            stuck.append({"tok": tid, "node": node, "reason": "nhánh cụt: không có luồng ra và không phải end event"})
            ev.append({"t": "stuck", "tok": tid, "node": node, "reason": "nhánh cụt"})
            kill(tid)
            return
        if len(outs) == 1:
            if t in GATES:
                ev.append({"t": "pass", "tok": tid, "node": node})
            go(tid, outs[0])
            return
        if t == "and":
            kill(tid)
            kids = [new_tid() for _ in outs]
            ev.append({"t": "split", "node": node, "tok": tid, "toks": kids})
            for k, f in zip(kids, outs):
                go(k, f)
            return
        if t in GATES:
            chosen = pick(node, outs)
            if t == "or" and len(chosen) > 1:
                kill(tid)
                kids = [new_tid() for _ in chosen]
                ev.append({"t": "split", "node": node, "tok": tid, "toks": kids, "or": True})
                for k, f in zip(kids, chosen):
                    go(k, f)
                return
            ev.append({"t": "choice", "node": node, "flow": chosen[0]["id"],
                       "label": chosen[0].get("name") or M.name(chosen[0]["to"])})
            go(tid, chosen[0])
            return
        # activity có nhiều luồng ra không qua gateway = chạy song song tất cả
        notes.append(f"“{M.name(node)}” có {len(outs)} luồng ra không qua gateway: mọi nhánh cùng chạy")
        kill(tid)
        kids = [new_tid() for _ in outs]
        ev.append({"t": "split", "node": node, "tok": tid, "toks": kids, "implicit": True})
        for k, f in zip(kids, outs):
            go(k, f)

    while True:
        while q:
            tid, node = q.popleft()
            if tid in alive:
                step(tid, node)
        # OR gộp: nhả khi không còn token nào khác đang chạy (mọi nhánh được kích hoạt đã tới)
        released = False
        for node, toks in list(or_wait.items()):
            if toks and not [x for x in alive if x not in toks]:
                for x in toks:
                    kill(x)
                nt = new_tid()
                ev.append({"t": "join", "node": node, "toks": toks, "new": nt})
                del or_wait[node]
                if M.out[node]:
                    go(nt, M.out[node][0])
                released = True
        if not released:
            break
    for node, toks in and_wait.items():
        for x in toks:
            stuck.append({"tok": x, "node": node, "reason": f"AND gộp chờ {len(M.inn[node])} nhánh nhưng chỉ {len(toks)} nhánh tới"})
            ev.append({"t": "stuck", "tok": x, "node": node, "reason": "AND gộp thiếu nhánh"})
    return {"events": ev, "ends": ends, "stuck": stuck, "notes": notes}


def auto_scenarios(model):
    M = model
    sc = [{"id": "S0", "name": "Luồng mặc định (mọi gateway đi default flow hoặc nhánh đầu)"}]
    k = 1
    for n in M.spec["nodes"]:
        outs = M.out[n["id"]]
        if n["type"] in ("xor", "event_based", "or") and len(outs) > 1:
            base = [f for f in outs if f.get("default")] or outs[:1]
            for f in outs:
                if f in base:
                    continue
                lab = f.get("name") or f["to"]
                sc.append({"id": f"S{k}", "name": f"“{n.get('name') or n['id']}” → {lab}", "choices": {n["id"]: [lab]}})
                k += 1
    for n in M.spec["nodes"]:
        if n["type"] in BOUNDARY_T:
            kind = "không ngắt" if n.get("interrupting") is False else "ngắt"
            sc.append({"id": f"S{k}", "name": f"Boundary “{n.get('name') or n['id']}” kích hoạt ({kind})", "fire": [n["id"]]})
            k += 1
    for m in M.spec.get("messages", []):
        tgt = M.nodes.get(m["to"])
        if tgt and tgt["type"] in ("receive_task", "message_catch", "event_based") or (tgt and not tgt["type"].startswith("start") and m["from"] in M.pools):
            sc.append({"id": f"S{k}", "name": f"Message “{m.get('name') or m['id']}” không bao giờ tới", "silent": [m["id"]]})
            k += 1
    return sc


def run(spec, scenarios):
    M = Model(spec)
    results, bad = [], False
    seen_nodes, seen_flows = set(), set()
    for sc in scenarios:
        r = simulate(M, sc)
        r["scenario"] = sc
        for e in r["events"]:
            if e.get("node"):
                seen_nodes.add(e["node"])
            if e["t"] == "move":
                seen_flows.add(e["flow"])
        if r["stuck"] or (sc.get("expect") and sc["expect"] not in r["ends"]):
            bad = True
        results.append(r)
    unvisited = [n for n in spec["nodes"] if n["id"] not in seen_nodes]
    untaken = [f for f in spec["flows"] if f["id"] not in seen_flows]
    return M, results, unvisited, untaken, bad


def report(M, results, unvisited, untaken):
    L = []
    for r in results:
        sc = r["scenario"]
        path = [M.name(e["node"]) for e in r["events"] if e["t"] in ("start", "work", "choice")]
        L.append(f"[{sc['id']}] {sc.get('name', '')}")
        steps = [x for i, x in enumerate(path) if i == 0 or x != path[i - 1]]   # gộp bước trùng liền nhau
        L.append("    Đường đi : " + " → ".join(steps))
        if r["ends"]:
            L.append("    Kết cục  : " + ", ".join(f"“{M.name(e)}”" for e in r["ends"]))
        for s in r["stuck"]:
            L.append(f"    KẸT      : “{M.name(s['node'])}” – {s['reason']}")
        if sc.get("expect") and sc["expect"] not in r["ends"]:
            L.append(f"    SAI KỲ VỌNG: mong đợi tới “{M.name(sc['expect'])}”")
        for n in r["notes"]:
            L.append(f"    Ghi chú  : {n}")
    if unvisited:
        L.append("\nNode chưa kịch bản nào đi qua: " + ", ".join(f"“{n.get('name') or n['id']}”" for n in unvisited))
    if untaken:
        L.append("Luồng chưa kịch bản nào đi qua: " + ", ".join(
            f"{M.name(f['from'])} → {M.name(f['to'])}" + (f" [{f['name']}]" if f.get("name") else "") for f in untaken))
    n_stuck = sum(1 for r in results if r["stuck"])
    L.append(f"\n{len(results)} kịch bản, {n_stuck} kịch bản bị kẹt.")
    return "\n".join(L)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    spec = json.load(open(args[0], encoding="utf-8"))
    M0 = Model(spec)
    scenarios = auto_scenarios(M0) if ("--auto" in args or not spec.get("scenarios")) else spec["scenarios"]
    M, results, unvisited, untaken, bad = run(spec, scenarios)
    print(report(M, results, unvisited, untaken))
    if "--json" in args:
        out = args[args.index("--json") + 1]
        json.dump([{"scenario": r["scenario"], "events": r["events"], "ends": r["ends"], "stuck": r["stuck"]}
                   for r in results], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"Đã ghi vết: {out}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
