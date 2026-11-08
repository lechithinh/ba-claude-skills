#!/usr/bin/env python3
"""Sinh bản nháp Mermaid (flowchart TD, mỗi lane là một subgraph) từ cùng file spec JSON
của spec_to_bpmn.py. Dùng cho vòng lặp nhanh trước khi xuất BPMN XML.
Pool bên ngoài vẽ thành hộp [[ ]], message flow là mũi tên nét đứt -.->.

    python3 spec_to_mermaid.py spec.json out.mmd
"""
import json
import sys


def shape(n):
    t, name = n["type"], n.get("name", "").replace('"', "'")
    if t.startswith("start"):
        return f'{n["id"]}(("{name or "Bắt đầu"}"))'
    if t.startswith("end"):
        return f'{n["id"]}((("{name or "Kết thúc"}")))'
    if t in ("xor", "or", "event_based"):
        return f'{n["id"]}{{"{name}"}}'
    if t == "and":
        return f'{n["id"]}{{"+ {name}"}}'
    if t in ("timer", "message_catch", "message_throw") or t.startswith("boundary"):
        return f'{n["id"]}(["{name}"])'
    return f'{n["id"]}["{name}"]'


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    s = json.load(open(sys.argv[1], encoding="utf-8"))
    L = ["flowchart TD"]
    for lane in s["lanes"]:
        L.append(f'    subgraph {lane["id"]}["{lane["name"]}"]')
        for n in s["nodes"]:
            if n.get("lane") == lane["id"]:
                L.append(f"        {shape(n)}")
        L.append("    end")
    pools = {p["id"] for p in s.get("pools", [])}
    for p in s.get("pools", []):
        L.append(f'    pool_{p["id"]}[["{p["name"]}"]]')
    for n in s["nodes"]:
        if n["type"].startswith("boundary"):
            L.append(f'    {n["attached_to"]} -.- {shape(n)}')
    for f in s["flows"]:
        lab = f'|{f["name"]}|' if f.get("name") else ""
        L.append(f'    {f["from"]} -->{lab} {f["to"]}')
    ref = lambda k: f"pool_{k}" if k in pools else k
    for m in s.get("messages", []):
        lab = f'|{m["name"]}|' if m.get("name") else ""
        L.append(f'    {ref(m["from"])} -.->{lab} {ref(m["to"])}')
    open(sys.argv[2], "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"Đã ghi {sys.argv[2]}")


if __name__ == "__main__":
    main()
