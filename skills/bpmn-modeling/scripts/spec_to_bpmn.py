#!/usr/bin/env python3
"""Sinh file BPMN 2.0 XML (có BPMNDiagram, mở được trong bpmn.io / Camunda Modeler)
từ một mô tả JSON ngắn gọn.

    python3 spec_to_bpmn.py spec.json out.bpmn

Spec:
{
  "name": "Đăng ký & eKYC",
  "lanes": [{"id": "kh", "name": "Khách hàng"}, {"id": "app", "name": "App"}],
  "nodes": [
    {"id": "s", "type": "start", "lane": "kh", "name": "Cần mở tài khoản"},
    {"id": "t1", "type": "user_task", "lane": "kh", "name": "Nhập thông tin"},
    {"id": "g1", "type": "xor", "lane": "app", "name": "Dữ liệu hợp lệ?"},
    {"id": "e", "type": "end", "lane": "app", "name": "Tài khoản đã kích hoạt"}
  ],
  "flows": [
    {"from": "s", "to": "t1"},
    {"from": "g1", "to": "e", "name": "Hợp lệ"},
    {"from": "g1", "to": "t1", "name": "Không hợp lệ", "default": true}
  ]
}
Loại node: start, start_message, start_timer, end, end_error, end_terminate,
end_message, timer, message_catch, message_throw, task, user_task, manual_task,
service_task, send_task, receive_task, script_task, business_rule_task,
subprocess, call_activity, xor, and, or, event_based.
Gắn boundary event: {"id":"b1","type":"boundary_timer","attached_to":"t1","interrupting":false,
"name":"Sau 2 phút"}; loại boundary_timer | boundary_message | boundary_error.
Pool bên ngoài (hộp đen) và message flow (tuỳ chọn):
  "pools": [{"id": "pay", "name": "Cổng thanh toán", "position": "top"}],   # top | bottom
  "messages": [{"id": "m1", "from": "t3", "to": "pay", "name": "Yêu cầu thanh toán"},
               {"id": "m2", "from": "pay", "to": "t4", "name": "Kết quả giao dịch"}]
Process chính là một pool nhiều lane; các pool khác vẽ thu gọn và chỉ nối bằng message flow.
"""
import json
import sys
from collections import defaultdict, deque
from xml.sax.saxutils import escape, quoteattr

TASKS = {"task": "task", "user_task": "userTask", "manual_task": "manualTask",
         "service_task": "serviceTask", "send_task": "sendTask", "receive_task": "receiveTask",
         "script_task": "scriptTask", "business_rule_task": "businessRuleTask",
         "subprocess": "subProcess", "call_activity": "callActivity"}
GATES = {"xor": "exclusiveGateway", "and": "parallelGateway",
         "or": "inclusiveGateway", "event_based": "eventBasedGateway"}
# type -> (tag, eventDefinition)
EVENTS = {"start": ("startEvent", None), "start_message": ("startEvent", "message"),
          "start_timer": ("startEvent", "timer"), "end": ("endEvent", None),
          "end_error": ("endEvent", "error"), "end_terminate": ("endEvent", "terminate"),
          "end_message": ("endEvent", "message"), "timer": ("intermediateCatchEvent", "timer"),
          "message_catch": ("intermediateCatchEvent", "message"),
          "message_throw": ("intermediateThrowEvent", "message")}
BOUNDARY = {"boundary_timer": "timer", "boundary_message": "message", "boundary_error": "error"}

W_TASK, H_TASK = 110, 70
D_EVENT, D_GATE = 36, 50
COL, PAD_X, ROW, LANE_PAD = 170, 60, 100, 30
LABEL_W = 30  # dải tên lane


def size(t):
    if t in TASKS:
        return W_TASK, H_TASK
    if t in GATES:
        return D_GATE, D_GATE
    return D_EVENT, D_EVENT


def tag_of(t):
    if t in TASKS:
        return TASKS[t]
    if t in GATES:
        return GATES[t]
    if t in EVENTS:
        return EVENTS[t][0]
    if t in BOUNDARY:
        return "boundaryEvent"
    raise SystemExit(f"Loại node không hỗ trợ: {t}")


def layout(spec):
    nodes = {n["id"]: n for n in spec["nodes"]}
    main = [n for n in spec["nodes"] if n["type"] not in BOUNDARY]
    out, inn = defaultdict(list), defaultdict(list)
    for f in spec["flows"]:
        for k in (f["from"], f["to"]):
            if k not in nodes:
                raise SystemExit(f"Flow tham chiếu node không tồn tại: {k}")
        src = nodes[f["from"]].get("attached_to") if nodes[f["from"]]["type"] in BOUNDARY else f["from"]
        out[src].append(f["to"])
        inn[f["to"]].append(src)
    # boundary event: coi như một nhánh ra từ activity chủ
    for n in spec["nodes"]:
        if n["type"] in BOUNDARY:
            if n.get("attached_to") not in nodes:
                raise SystemExit(f"Boundary {n['id']} thiếu attached_to hợp lệ")
    # loại cạnh quay lui bằng DFS
    starts = [n["id"] for n in main if n["type"].startswith("start")] or [main[0]["id"]]
    state, back = {}, set()

    def dfs(u):
        state[u] = 1
        for v in out[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2
    sys.setrecursionlimit(10000)
    for s in starts:
        if s not in state:
            dfs(s)
    for n in main:
        if n["id"] not in state:
            dfs(n["id"])
    rank = {}
    indeg = defaultdict(int)
    for u in out:
        for v in out[u]:
            if (u, v) not in back:
                indeg[v] += 1
    q = deque(n["id"] for n in main if indeg[n["id"]] == 0)
    for k in q:
        rank[k] = 0
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in out[u]:
            if (u, v) in back:
                continue
            rank[v] = max(rank.get(v, 0), rank[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for n in main:
        rank.setdefault(n["id"], 0)
    # xếp hàng trong lane
    lane_ids = [l["id"] for l in spec["lanes"]]
    slot = {}
    used = defaultdict(set)
    for nid in sorted(rank, key=lambda k: (rank[k], [m["id"] for m in main].index(k))):
        key = (nodes[nid]["lane"], rank[nid])
        i = 0
        while i in used[key]:
            i += 1
        used[key].add(i)
        slot[nid] = i
    lane_rows = {l: max([i for (ln, _), s in used.items() if ln == l for i in s] + [0]) + 1 for l in lane_ids}
    lane_h = {l: lane_rows[l] * ROW + 2 * LANE_PAD - 30 + 30 for l in lane_ids}
    lane_y, y = {}, 0
    for l in lane_ids:
        lane_y[l] = y
        y += lane_h[l]
    max_rank = max(rank.values())
    pool_w = LABEL_W + PAD_X * 2 + (max_rank + 1) * COL
    geo = {}
    for n in main:
        w, h = size(n["type"])
        cx = LABEL_W + PAD_X + rank[n["id"]] * COL + COL // 2 - 20
        cy = lane_y[n["lane"]] + LANE_PAD + slot[n["id"]] * ROW + (ROW - 30) // 2
        geo[n["id"]] = (cx - w // 2 + 20, cy - h // 2 + 15, w, h)
    for n in spec["nodes"]:
        if n["type"] in BOUNDARY:
            x, y0, w, h = geo[n["attached_to"]]
            same = [m for m in spec["nodes"] if m["type"] in BOUNDARY and m["attached_to"] == n["attached_to"]]
            i = same.index(n)
            geo[n["id"]] = (x + 20 + i * 45, y0 + h - 18, D_EVENT, D_EVENT)
    return geo, lane_y, lane_h, pool_w, back, rank


def route(src, dst, back, geo, bottom, boundary=False):
    sx, sy, sw, sh = geo[src]
    tx, ty, tw, th = geo[dst]
    if boundary:  # luồng ngoại lệ: đi xuống dưới activity rồi sang target
        bx, by = sx + sw // 2, sy + sh
        tyc = ty + th // 2
        if tyc > by + 10:
            return [(bx, by), (bx, tyc), (tx, tyc)]
        low = by + 28
        return [(bx, by), (bx, low), (tx - 20, low), (tx - 20, tyc), (tx, tyc)]
    if (src, dst) in back:
        b = bottom + 12
        return [(sx + sw // 2, sy + sh), (sx + sw // 2, b), (tx + tw // 2, b), (tx + tw // 2, ty + th)]
    p1 = (sx + sw, sy + sh // 2)
    p2 = (tx, ty + th // 2)
    gate_src = (sw, sh) == (D_GATE, D_GATE)
    if gate_src and abs(p1[1] - p2[1]) >= 2 and p2[0] > p1[0]:
        cx = sx + sw // 2  # gateway rẽ nhánh: đi ra đỉnh/đáy rồi sang ngang
        return [(cx, sy + sh if ty > sy else sy), (cx, p2[1]), p2]
    if abs(p1[1] - p2[1]) < 2:
        return [p1, p2]
    mx = (p1[0] + p2[0]) // 2
    if p2[0] <= p1[0] + 10:  # cùng cột: đi từ trên/dưới
        if ty > sy:
            return [(sx + sw // 2, sy + sh), (sx + sw // 2, ty + th // 2), (tx, ty + th // 2)] \
                if tx > sx + sw // 2 else [(sx + sw // 2, sy + sh), (tx + tw // 2, ty)]
        return [(sx + sw // 2, sy), (tx + tw // 2, ty + th)]
    return [p1, (mx, p1[1]), (mx, p2[1]), p2]


POOL_H, POOL_GAP = 60, 70


def geometry(spec):
    """Toạ độ dùng chung cho XML (BPMNDiagram) và SVG: node, lane, pool, đường nối."""
    geo, lane_y, lane_h, pool_w, back, rank = layout(spec)
    nodes = {n["id"]: n for n in spec["nodes"]}
    pools = spec.get("pools", [])
    top = [p for p in pools if p.get("position", "top") != "bottom"]
    bot = [p for p in pools if p.get("position", "top") == "bottom"]
    dy = len(top) * (POOL_H + POOL_GAP)
    geo = {k: (x, y + dy, w, h) for k, (x, y, w, h) in geo.items()}
    total_h = sum(lane_h.values())
    lanes = {}
    for l in spec["lanes"]:
        lanes[l["id"]] = (LABEL_W, lane_y[l["id"]] + dy, pool_w - LABEL_W, lane_h[l["id"]])
    prect = {}
    for i, p in enumerate(top):
        prect[p["id"]] = (0, i * (POOL_H + POOL_GAP), pool_w, POOL_H)
    for j, p in enumerate(bot):
        prect[p["id"]] = (0, dy + total_h + POOL_GAP + j * (POOL_H + POOL_GAP), pool_w, POOL_H)
    seq = {}
    for i, f in enumerate(spec["flows"]):
        fid = f.get("id", f"Flow_{i+1}")
        seq[fid] = route(f["from"], f["to"], back, geo, dy + total_h, nodes[f["from"]]["type"] in BOUNDARY)
    # message flow: đi thẳng đứng giữa node và pool thu gọn
    msgs = spec.get("messages", [])
    per_node = defaultdict(list)
    for m in msgs:
        for end in (m["from"], m["to"]):
            if end in geo:
                per_node[end].append(m["id"])
    mpts = {}
    for m in msgs:
        a, b = m["from"], m["to"]
        if a in geo and b in prect:
            node, pool, outward = a, b, True
        elif b in geo and a in prect:
            node, pool, outward = b, a, False
        else:
            raise SystemExit(f"Message {m['id']}: một đầu phải là node, đầu kia là pool trong 'pools'")
        x, y, w, h = geo[node]
        k = per_node[node].index(m["id"]) - (len(per_node[node]) - 1) / 2
        mx = x + w / 2 + k * 18
        px, py, pw, ph = prect[pool]
        if py < y:      # pool ở trên
            near, far = (mx, y), (mx, py + ph)
        else:           # pool ở dưới
            near, far = (mx, y + h), (mx, py)
        mpts[m["id"]] = [near, far] if outward else [far, near]
    height = (prect and max(r[1] + r[3] for r in prect.values())) or 0
    return {"geo": geo, "lanes": lanes, "main": (0, dy, pool_w, total_h), "pools": prect,
            "seq": seq, "msg": mpts, "back": back, "width": pool_w,
            "height": max(height, dy + total_h) + 40}


def build(spec):
    G = geometry(spec)
    geo, pool_w, back = G["geo"], G["width"], G["back"]
    nodes = {n["id"]: n for n in spec["nodes"]}
    total_h = G["main"][3]
    dy = G["main"][1]
    lane_y = {k: v[1] for k, v in G["lanes"].items()}
    lane_h = {k: v[3] for k, v in G["lanes"].items()}
    pid, proc = "Process_1", "Participant_1"
    A = quoteattr
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
         'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
         'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
         'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_1" '
         'targetNamespace="http://bpmn.io/schema/bpmn">',
         '  <bpmn:collaboration id="Collaboration_1">',
         f'    <bpmn:participant id="{proc}" name={A(spec.get("name", "Quy trình"))} processRef="{pid}" />']
    for p in spec.get("pools", []):
        L.append(f'    <bpmn:participant id={A("Pool_" + p["id"])} name={A(p["name"])} />')
    ref = lambda k: "Pool_" + k if k in G["pools"] else k
    for m in spec.get("messages", []):
        nm = f' name={A(m["name"])}' if m.get("name") else ""
        L.append(f'    <bpmn:messageFlow id={A("Msg_" + m["id"])}{nm} sourceRef={A(ref(m["from"]))} targetRef={A(ref(m["to"]))} />')
    L += ['  </bpmn:collaboration>',
          f'  <bpmn:process id="{pid}" isExecutable="false">',
          '    <bpmn:laneSet id="LaneSet_1">']
    for l in spec["lanes"]:
        L.append(f'      <bpmn:lane id="Lane_{l["id"]}" name={A(l["name"])}>')
        for n in spec["nodes"]:
            if n["type"] not in BOUNDARY and n["lane"] == l["id"]:
                L.append(f'        <bpmn:flowNodeRef>{escape(n["id"])}</bpmn:flowNodeRef>')
        for n in spec["nodes"]:
            if n["type"] in BOUNDARY and nodes[n["attached_to"]]["lane"] == l["id"]:
                L.append(f'        <bpmn:flowNodeRef>{escape(n["id"])}</bpmn:flowNodeRef>')
        L.append('      </bpmn:lane>')
    L.append('    </bpmn:laneSet>')
    outs, ins = defaultdict(list), defaultdict(list)
    for i, f in enumerate(spec["flows"]):
        f["_id"] = f.get("id", f"Flow_{i+1}")
        outs[f["from"]].append(f["_id"])
        ins[f["to"]].append(f["_id"])
    default_of = {}
    for f in spec["flows"]:
        if f.get("default"):
            default_of[f["from"]] = f["_id"]
    for n in spec["nodes"]:
        t, nid = n["type"], n["id"]
        tag = tag_of(t)
        attrs = f'id={A(nid)} name={A(n.get("name", ""))}'
        if nid in default_of:
            attrs += f' default={A(default_of[nid])}'
        if t in BOUNDARY:
            attrs += f' attachedToRef={A(n["attached_to"])} cancelActivity="{"false" if n.get("interrupting") is False else "true"}"'
        body = []
        for x in ins[nid]:
            body.append(f'      <bpmn:incoming>{x}</bpmn:incoming>')
        for x in outs[nid]:
            body.append(f'      <bpmn:outgoing>{x}</bpmn:outgoing>')
        ed = EVENTS[t][1] if t in EVENTS else BOUNDARY.get(t)
        if ed:
            body.append(f'      <bpmn:{ed}EventDefinition id="{nid}_def" />')
        L.append(f'    <bpmn:{tag} {attrs}>' if body else f'    <bpmn:{tag} {attrs} />')
        if body:
            L += body
            L.append(f'    </bpmn:{tag}>')
    for f in spec["flows"]:
        nm = f' name={A(f["name"])}' if f.get("name") else ""
        L.append(f'    <bpmn:sequenceFlow id="{f["_id"]}"{nm} sourceRef={A(f["from"])} targetRef={A(f["to"])} />')
    L.append('  </bpmn:process>')
    L += ['  <bpmndi:BPMNDiagram id="Diagram_1">',
          '    <bpmndi:BPMNPlane id="Plane_1" bpmnElement="Collaboration_1">',
          f'      <bpmndi:BPMNShape id="{proc}_di" bpmnElement="{proc}" isHorizontal="true">',
          f'        <dc:Bounds x="0" y="{dy}" width="{pool_w}" height="{total_h}" />',
          '      </bpmndi:BPMNShape>']
    for p in spec.get("pools", []):
        x, y, w, h = G["pools"][p["id"]]
        L += [f'      <bpmndi:BPMNShape id="Pool_{p["id"]}_di" bpmnElement="Pool_{p["id"]}" isHorizontal="true">',
              f'        <dc:Bounds x="{x}" y="{y}" width="{w}" height="{h}" />',
              '      </bpmndi:BPMNShape>']
    for l in spec["lanes"]:
        L += [f'      <bpmndi:BPMNShape id="Lane_{l["id"]}_di" bpmnElement="Lane_{l["id"]}" isHorizontal="true">',
              f'        <dc:Bounds x="{LABEL_W}" y="{lane_y[l["id"]]}" width="{pool_w - LABEL_W}" height="{lane_h[l["id"]]}" />',
              '      </bpmndi:BPMNShape>']
    for n in spec["nodes"]:
        x, y, w, h = geo[n["id"]]
        mark = ' isMarkerVisible="true"' if n["type"] == "xor" else ""
        L += [f'      <bpmndi:BPMNShape id="{n["id"]}_di" bpmnElement="{n["id"]}"{mark}>',
              f'        <dc:Bounds x="{x}" y="{y}" width="{w}" height="{h}" />']
        if n["type"] in EVENTS or n["type"] in BOUNDARY or n["type"] in GATES:
            L += ['        <bpmndi:BPMNLabel>',
                  f'          <dc:Bounds x="{x - 25}" y="{y + h + 4}" width="{w + 50}" height="27" />',
                  '        </bpmndi:BPMNLabel>']
        L.append('      </bpmndi:BPMNShape>')
    for f in spec["flows"]:
        pts = [(int(a), int(b)) for a, b in G["seq"][f["_id"]]]
        L.append(f'      <bpmndi:BPMNEdge id="{f["_id"]}_di" bpmnElement="{f["_id"]}">')
        for px, py in pts:
            L.append(f'        <di:waypoint x="{px}" y="{py}" />')
        if f.get("name"):
            mx = (pts[0][0] + pts[-1][0]) // 2 if len(pts) == 2 else pts[1][0]
            my = pts[0][1] if len(pts) == 2 else (pts[1][1] + pts[2][1]) // 2 if len(pts) > 2 else pts[0][1]
            L += ['        <bpmndi:BPMNLabel>',
                  f'          <dc:Bounds x="{min(mx, pts[-1][0]) + 4}" y="{my - 20}" width="80" height="14" />',
                  '        </bpmndi:BPMNLabel>']
        L.append('      </bpmndi:BPMNEdge>')
    for m in spec.get("messages", []):
        L.append(f'      <bpmndi:BPMNEdge id="Msg_{m["id"]}_di" bpmnElement="Msg_{m["id"]}">')
        for px, py in G["msg"][m["id"]]:
            L.append(f'        <di:waypoint x="{int(px)}" y="{int(py)}" />')
        L.append('      </bpmndi:BPMNEdge>')
    L += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>']
    return "\n".join(L) + "\n"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    lane_ids = {l["id"] for l in spec["lanes"]}
    for n in spec["nodes"]:
        if n["type"] not in BOUNDARY and n.get("lane") not in lane_ids:
            sys.exit(f"Node {n['id']}: lane '{n.get('lane')}' không có trong lanes")
        tag_of(n["type"])
    ids = {n["id"] for n in spec["nodes"]} | {p["id"] for p in spec.get("pools", [])}
    for m in spec.get("messages", []):
        for k in (m.get("from"), m.get("to")):
            if k not in ids:
                sys.exit(f"Message {m.get('id')}: '{k}' không phải node hay pool")
    open(sys.argv[2], "w", encoding="utf-8").write(build(spec))
    print(f"Đã ghi {sys.argv[2]}: {len(spec['nodes'])} node, {len(spec['flows'])} flow, {len(spec['lanes'])} lane")


if __name__ == "__main__":
    main()
