#!/usr/bin/env python3
"""Thư viện dùng chung cho các script phân rã chức năng: đọc spec JSON, duyệt cây, hằng số.
Chỉ dùng thư viện chuẩn của Python 3."""
import json
import re
import sys
import unicodedata

PRIORITIES = {"M": "Must", "S": "Should", "C": "Could", "W": "Won't (lần này)"}
CROSS_TAGS = {
    "auth": "Xác thực & phân quyền",
    "notify": "Thông báo",
    "audit": "Nhật ký thao tác (audit)",
    "report": "Báo cáo",
    "config": "Cấu hình & danh mục",
}
ID_RE = re.compile(r"^\d+(\.\d+)*$")


class SpecError(Exception):
    pass


def norm(s):
    """Chữ thường, bỏ dấu tiếng Việt, bỏ ký tự thừa - để so sánh tên."""
    s = (s or "").lower().replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def load(path):
    try:
        spec = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SpecError(f"Không đọc được spec: {e}")
    if not isinstance(spec, dict) or not spec.get("name"):
        raise SpecError("Spec cần có trường 'name'")
    if not spec.get("modules"):
        raise SpecError("Spec cần có 'modules' (ít nhất một module)")
    spec.setdefault("actors", [])
    spec.setdefault("objects", [])
    spec.setdefault("requirements", [])
    spec.setdefault("waive", {})
    spec.setdefault("scope", {"in": [], "out": []})
    return spec


def walk(spec):
    """Trả về danh sách phẳng theo thứ tự cây. Mỗi phần tử:
    {n: node, id, depth, parent_id, top_id, is_leaf, kind, path}"""
    out = []

    def rec(node, depth, parent, top, path):
        children = node.get("children") or []
        item = {
            "n": node, "id": str(node.get("id", "")), "depth": depth,
            "parent_id": parent, "top_id": top or str(node.get("id", "")),
            "is_leaf": not children, "path": path + [node.get("name", "")],
        }
        item["kind"] = "Module" if depth == 1 else ("Function" if item["is_leaf"] else "Feature")
        out.append(item)
        for c in children:
            rec(c, depth + 1, item["id"], item["top_id"], item["path"])

    for m in spec["modules"]:
        rec(m, 1, None, None, [])
    return out


def functions(items):
    return [i for i in items if i["is_leaf"]]


def ops_of(node):
    """Trả về {object_id: 'CRU'} đã chuẩn hoá."""
    res = {}
    for k, v in (node.get("ops") or {}).items():
        res[k] = "".join(ch for ch in "CRUD" if ch in str(v).upper())
    return res


def actor_name(spec, aid):
    for a in spec["actors"]:
        if a.get("id") == aid:
            return a.get("name", aid)
    return aid


def object_name(spec, oid):
    for o in spec["objects"]:
        if o.get("id") == oid:
            return o.get("name", oid)
    return oid


def fail(msg, code=2):
    sys.stderr.write(msg + "\n")
    sys.exit(code)


CRUD_CODE = {"C": "D1", "R": "D2", "U": "D3", "D": "D4"}


def crud_waiver(spec, obj, ch):
    """Trả về lý do miễn trừ cho ô (đối tượng, C/R/U/D) hoặc None. Gộp cờ trên đối tượng và spec['waive']."""
    if obj.get("source") == "external" and ch in "CUD":
        return "dữ liệu do hệ thống khác sở hữu"
    if ch == "U" and obj.get("immutable"):
        return "bất biến"
    if ch == "D" and obj.get("no_delete"):
        return obj.get("note") or "không xóa"
    return (spec.get("waive") or {}).get(f"{CRUD_CODE[ch]}:{obj.get('id')}")
