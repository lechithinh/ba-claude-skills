# Ví dụ

Mỗi thư mục có `spec.json` (nguồn) và các file sinh ra từ nó: `diagram.bpmn`, `diagram.mmd`, `diagram.svg`, `tokens.html`. Mở `tokens.html` bằng trình duyệt để chọn kịch bản và xem token chạy.

| Ví dụ | Minh hoạ | Kịch bản token |
|---|---|---|
| `counter-order/` | Ví dụ tối giản: start, task, XOR, end, 2 lane | Còn món / hết món |
| `cinema-ticketing/` | **Ví dụ đầy đủ**: pool ngoài + message flow, user/service/send/receive task, XOR gộp vòng lặp, AND, timer boundary ngắt; có `walkthrough.md` (6 bước) và `review.md` (lỗ hổng → TO-BE, `spec-to-be.json`) | A–E (E kẹt ở AS-IS), A–F ở TO-BE |
| `ride-hailing/` | Collaboration 3 pool, message start event, event-based gateway, vòng thử lại tối đa 3 lần | Tài xế nhận ngay / thử lại / không có xe |
| `food-delivery/` | AND tách và gộp, error boundary (ngắt), timer boundary không ngắt | Thành công / quán nấu quá 15 phút / thanh toán lỗi |
| `ekyc/` | Mở tài khoản ngân hàng số, 4 lane, thẩm định thủ công khi không khớp | Tự sinh (`--auto`) |

Sinh lại toàn bộ (chạy ở thư mục gốc của skill):
```bash
for d in examples/*/; do
  python3 scripts/spec_to_bpmn.py     $d/spec.json $d/diagram.bpmn
  python3 scripts/bpmn_lint.py        $d/diagram.bpmn
  python3 scripts/spec_to_mermaid.py  $d/spec.json $d/diagram.mmd
  python3 scripts/spec_to_svg.py      $d/spec.json $d/diagram.svg
  python3 scripts/build_token_page.py $d/spec.json $d/tokens.html
done
```
