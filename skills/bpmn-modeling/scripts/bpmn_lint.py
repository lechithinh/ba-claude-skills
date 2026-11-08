#!/usr/bin/env python3
"""Kiểm tra một file BPMN 2.0 XML theo quy tắc BPMN 2.0 và quy ước trong references/modeling-rules.md.

    python3 bpmn_lint.py diagram.bpmn

Mức: LỖI (vi phạm quy tắc BPMN/quy ước mô hình hoá) · CẢNH BÁO (nên xem lại).
Thoát mã 1 nếu có LỖI. Script chỉ kiểm tra cấu trúc; việc đúng nghiệp vụ vẫn cần
người làm quy trình xác nhận.
"""
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = {"b": "http://www.omg.org/spec/BPMN/20100524/MODEL",
      "di": "http://www.omg.org/spec/BPMN/20100524/DI"}
B = "{%s}" % NS["b"]
TASK_TAGS = {"task", "userTask", "manualTask", "serviceTask", "sendTask", "receiveTask",
             "scriptTask", "businessRuleTask", "subProcess", "callActivity", "transaction", "adHocSubProcess"}
GATE_TAGS = {"exclusiveGateway", "parallelGateway", "inclusiveGateway", "eventBasedGateway", "complexGateway"}
EVENT_TAGS = {"startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent", "boundaryEvent"}


def local(t):
    return t.split("}")[-1]


def words(name):
    return len([w for w in re.split(r"\s+", (name or "").strip()) if w])


def lint(path):
    root = ET.parse(path).getroot()
    errs, warns = [], []
    for proc in root.iter(B + "process"):
        pname = proc.get("name") or proc.get("id")
        nodes = {}
        for el in proc:
            tag = local(el.tag)
            if tag in TASK_TAGS | GATE_TAGS | EVENT_TAGS:
                nodes[el.get("id")] = el
        flows = [e for e in proc if local(e.tag) == "sequenceFlow"]
        out, inn = defaultdict(list), defaultdict(list)
        for f in flows:
            out[f.get("sourceRef")].append(f)
            inn[f.get("targetRef")].append(f)

        def nm(i):
            return f'{local(nodes[i].tag)} "{nodes[i].get("name") or i}"'

        starts = [i for i, e in nodes.items() if local(e.tag) == "startEvent"]
        ends = [i for i, e in nodes.items() if local(e.tag) == "endEvent"]
        if len(starts) == 0:
            errs.append(f"[{pname}] thiếu Start Event")
        if len(starts) > 1:
            warns.append(f"[{pname}] có {len(starts)} Start Event - chỉ nên 1 trừ khi các trigger khác nhau có chủ đích")
        if not ends:
            errs.append(f"[{pname}] thiếu End Event")
        defs = lambda e: {local(c.tag) for c in e if local(c.tag).endswith("EventDefinition")}
        for i, e in nodes.items():
            tag = local(e.tag)
            if tag == "boundaryEvent":
                if inn[i]:
                    errs.append(f"[{pname}] sequence flow đi vào boundary event {nm(i)} - luồng chính phải vào task, boundary chỉ có luồng ra")
                if not out[i]:
                    errs.append(f"[{pname}] boundary event {nm(i)} không có luồng ra - khi kích hoạt token không có đường đi")
                continue
            if tag == "startEvent" and inn[i]:
                errs.append(f"[{pname}] {nm(i)} có luồng đi vào - start event chỉ có luồng ra; mốc giữa process dùng intermediate event")
            if tag == "endEvent" and out[i]:
                errs.append(f"[{pname}] {nm(i)} có luồng đi ra - end event là điểm kết thúc của nhánh")
            if tag in ("endEvent", "intermediateThrowEvent") and "timerEventDefinition" in defs(e):
                errs.append(f"[{pname}] {nm(i)} là timer dạng ném - timer chỉ có dạng bắt (start, intermediate catch, boundary)")
            if tag == "eventBasedGateway":
                for f in out[i]:
                    tgt = nodes.get(f.get("targetRef"))
                    if tgt is not None and local(tgt.tag) not in ("intermediateCatchEvent", "receiveTask"):
                        errs.append(f"[{pname}] sau event-based gateway {nm(i)} là {nm(f.get('targetRef'))} - chỉ được là event bắt hoặc receive task")
            if tag in TASK_TAGS and len(out[i]) > 1 and not any(f.find(B + "conditionExpression") is not None for f in out[i]):
                warns.append(f"[{pname}] {nm(i)} có {len(out[i])} luồng ra không qua gateway - mọi nhánh sẽ cùng chạy; muốn chọn 1 nhánh thì thêm XOR gateway")
            if tag != "startEvent" and not inn[i]:
                errs.append(f"[{pname}] {nm(i)} không có luồng vào")
            if tag != "endEvent" and not out[i]:
                errs.append(f"[{pname}] {nm(i)} không có luồng ra (nhánh phải kết thúc bằng End Event)")
            if tag in TASK_TAGS:
                n = (e.get("name") or "").strip()
                if not n:
                    errs.append(f"[{pname}] {local(e.tag)} {i} chưa đặt tên")
                elif words(n) < 2:
                    warns.append(f'[{pname}] task "{n}" chỉ 1 từ - đặt tên Động từ + Tân ngữ')
            if tag in EVENT_TAGS and tag in ("startEvent", "endEvent") and not (e.get("name") or "").strip():
                warns.append(f"[{pname}] {tag} {i} chưa đặt tên (nên theo trạng thái, vd 'Đã giao món')")
            if tag in GATE_TAGS:
                n = (e.get("name") or "").strip()
                split = len(out[i]) > 1
                if split and tag in ("exclusiveGateway", "inclusiveGateway", "eventBasedGateway"):
                    default = e.get("default")
                    if tag != "eventBasedGateway":
                        if not n:
                            warns.append(f"[{pname}] {nm(i)} rẽ nhánh nhưng chưa đặt tên dạng câu hỏi")
                        elif not n.endswith("?"):
                            warns.append(f'[{pname}] gateway "{n}" nên là câu hỏi (kết thúc bằng ?)')
                        for f in out[i]:
                            if not (f.get("name") or "").strip() and f.get("id") != default:
                                errs.append(f"[{pname}] luồng ra từ {nm(i)} không có nhãn điều kiện")
                        if not default and len(out[i]) > 2:
                            warns.append(f"[{pname}] {nm(i)} có {len(out[i])} nhánh nhưng chưa có default flow - process có thể bị kẹt nếu không điều kiện nào đúng")
                if len(out[i]) == 1 and len(inn[i]) == 1:
                    warns.append(f"[{pname}] {nm(i)} chỉ 1 vào 1 ra - không cần gateway")
        # gateway tách/gộp
        for kind, label in (("parallelGateway", "AND"), ("inclusiveGateway", "OR")):
            splits = [i for i, e in nodes.items() if local(e.tag) == kind and len(out[i]) > 1]
            joins = [i for i, e in nodes.items() if local(e.tag) == kind and len(inn[i]) > 1]
            if len(joins) < len(splits):
                errs.append(f"[{pname}] có {len(splits)} gateway {label} tách nhưng chỉ {len(joins)} gateway {label} gộp - tách {label} thì gộp {label}")
        # error event
        for e in root.iter(B + "intermediateThrowEvent"):
            if e.find(B + "errorEventDefinition") is not None:
                errs.append(f'[{pname}] Error ném ở Intermediate Event "{e.get("name")}" - Error chỉ ném ở End Event')
        # task trong lane đúng: mỗi node phải thuộc 1 lane nếu có laneSet
        ls = proc.find(B + "laneSet")
        if ls is not None:
            ref = {r.text for r in ls.iter(B + "flowNodeRef")}
            for i in nodes:
                if i not in ref:
                    errs.append(f"[{pname}] {nm(i)} không thuộc lane nào")
        # luồng từ activity sang compensation / markers không kiểm tra thêm
    # message flow phải khác pool
    parts = {p.get("id"): p.get("processRef") for p in root.iter(B + "participant")}
    owner = {}
    for pid, ref in parts.items():
        proc = next((p for p in root.iter(B + "process") if p.get("id") == ref), None)
        if proc is not None:
            for el in proc.iter():
                if el.get("id"):
                    owner[el.get("id")] = pid
    by_id = {el.get("id"): el for el in root.iter() if el.get("id")}
    for m in root.iter(B + "messageFlow"):
        tgt = by_id.get(m.get("targetRef"))
        if tgt is not None and local(tgt.tag) == "startEvent" and tgt.find(B + "messageEventDefinition") is None:
            warns.append(f'start event "{tgt.get("name") or tgt.get("id")}" nhận message flow nhưng là start trống - dùng Message start event')
        a, b = owner.get(m.get("sourceRef")), owner.get(m.get("targetRef"))
        if a and b and a == b:
            errs.append(f"messageFlow {m.get('id')} nối trong cùng pool - dùng sequence flow")
    # DI
    shapes = {s.get("bpmnElement") for s in root.iter("{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape")}
    if not shapes:
        warns.append("Không có BPMNDiagram (toạ độ) - import vào bpmn.io/Camunda sẽ không hiện hình")
    else:
        for el in root.iter():
            if local(el.tag) in TASK_TAGS | GATE_TAGS | EVENT_TAGS and el.get("id") not in shapes:
                warns.append(f"{local(el.tag)} {el.get('id')} thiếu BPMNShape")
    return errs, warns


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    errs, warns = lint(sys.argv[1])
    for e in errs:
        print("LỖI     ", e)
    for w in warns:
        print("CẢNH BÁO", w)
    print(f"\n{len(errs)} lỗi, {len(warns)} cảnh báo.")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
