#!/usr/bin/env python3
"""Chuyển một outline văn bản (danh sách phân cấp có sẵn) thành spec JSON "khung" để chạy lint.
Dùng cho chế độ Soát: người dùng dán danh sách chức năng, script dựng spec, lint chỉ ra lỗi.

    python3 outline_to_spec.py outline.txt spec.json --name "Tên hệ thống"

Hai kiểu outline (không trộn):
  1) Có ID:        1 Đặt lịch / 1.1 Tìm khung giờ trống [bệnh nhân, lễ tân] / 1.2 ...
  2) Thụt lề:      dòng con thụt vào so với dòng cha (2 hoặc 4 dấu cách, hoặc tab; có thể có "-", "*")
Phần [a, b] cuối dòng là actor (tuỳ chọn). ID được tự đánh khi outline không có ID.
Khung này chưa có 'objects' và 'requirements' - bổ sung tay để lint kiểm CRUD và truy vết.
"""
import json
import re
import sys

import fdlib as F

LINE_ID = re.compile(r"^\s*[-*•]?\s*(\d+(?:\.\d+)*)[.)]?\s+(.*\S)\s*$")


def slug(s):
    return re.sub(r"\s+", "_", F.norm(s)) or "actor"


def parse_tail(text, actors):
    m = re.search(r"\[([^\]]+)\]\s*$", text)
    acts = []
    if m:
        for a in m.group(1).split(","):
            a = a.strip()
            if a:
                actors.setdefault(slug(a), a)
                acts.append(slug(a))
        text = text[: m.start()].strip()
    return text, acts


def main():
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    name = "Hệ thống"
    if "--name" in sys.argv:
        name = sys.argv[sys.argv.index("--name") + 1]
        pos = [p for p in pos if p != name]
    if len(pos) != 2:
        sys.exit(__doc__)
    lines = [l.rstrip("\n") for l in open(pos[0], encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")]
    actors, flat = {}, []
    with_id = all(LINE_ID.match(l) for l in lines)
    if with_id:
        for l in lines:
            i, t = LINE_ID.match(l).groups()
            t, acts = parse_tail(t, actors)
            flat.append({"id": i, "name": t, "actors": acts})
    else:
        stack, counters = [], {}
        for l in lines:
            expanded = l.replace("\t", "    ")
            ind = len(expanded) - len(expanded.lstrip(" "))
            text = re.sub(r"^[-*•]\s*", "", expanded.strip())
            text, acts = parse_tail(text, actors)
            while stack and stack[-1][0] >= ind:
                stack.pop()
            parent = stack[-1][1] if stack else ""
            counters[parent] = counters.get(parent, 0) + 1
            i = f"{parent}.{counters[parent]}" if parent else str(counters[parent])
            stack.append((ind, i))
            flat.append({"id": i, "name": text, "actors": acts})
    nodes = {}
    roots = []
    for f in flat:
        node = {"id": f["id"], "name": f["name"]}
        if f["actors"]:
            node["actors"] = f["actors"]
        nodes[f["id"]] = node
        parent = f["id"].rsplit(".", 1)[0] if "." in f["id"] else None
        if parent and parent in nodes:
            nodes[parent].setdefault("children", []).append(node)
        else:
            roots.append(node)
    spec = {"name": name, "scope": {"in": [], "out": []},
            "actors": [{"id": k, "name": v} for k, v in actors.items()],
            "objects": [], "requirements": [], "modules": roots}
    json.dump(spec, open(pos[1], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Đã dựng {len(flat)} dòng → {pos[1]} ({len(roots)} module). Bổ sung objects/requirements rồi chạy fd_lint.py.")


if __name__ == "__main__":
    main()
