# Review bằng token

**Token** là "đồng xu" đặt ở start event rồi đẩy theo mũi tên - process engine chạy quy trình đúng như vậy. Review bằng token biến câu hỏi "sơ đồ đã đúng chưa?" thành câu hỏi cụ thể: *với kịch bản này, token có tới được end event không, và tới end nào?*

## Luật đi của token
| Gặp | Token làm gì |
|---|---|
| Start event | Xuất hiện |
| Task | Dừng lại trong lúc task chạy; boundary event có thể kích hoạt lúc này |
| XOR / event-based | Đi **đúng một** nhánh |
| AND tách | Một token thành nhiều, mỗi nhánh một token |
| AND gộp | Chờ **đủ** token từ mọi nhánh rồi đi tiếp một token |
| OR tách / gộp | Đi các nhánh có điều kiện đúng; gộp chờ đủ các nhánh đã được kích hoạt |
| Boundary viền liền (ngắt) | Token trong task bị huỷ; token mới đi luồng ngoại lệ |
| Boundary viền đứt (không ngắt) | Thêm một token đi luồng ngoại lệ; token trong task vẫn ở lại |
| Receive task / message event bắt | Chờ message; message không tới thì token **kẹt** |
| End event | Token kết thúc |

Message (tin nhắn giữa các pool) **không phải** token: nó kích hoạt hoặc đánh thức token ở bên nhận.

## Viết kịch bản
Tối thiểu cho mỗi sơ đồ:
1. **Thành công** - đi hết luồng chính.
2. **Mỗi nhánh "Không" của gateway quan trọng** - ghế hết, thanh toán thất bại, hồ sơ bị từ chối.
3. **Mỗi boundary event** - hết giờ, lỗi, người dùng huỷ.
4. **Mỗi bên ngoài im lặng** - message trả lời không bao giờ tới. Đây là kịch bản hay lộ lỗ hổng nhất.
5. **Vòng lặp** - nhánh quay lại chạy 2 lần rồi thoát.

Trong spec (`output-formats.md`):
```json
"scenarios": [
  {"id": "A", "name": "Mua thành công", "choices": {"g1": "Có", "g2": "Có"}, "expect": "e1"},
  {"id": "B", "name": "Ghế bị giữ", "choices": {"g1": ["Không", "Có"]}, "expect": "e1"},
  {"id": "D", "name": "Quá 10 phút", "fire": ["b1"], "expect": "e2"},
  {"id": "E", "name": "Không có kết quả", "silent": ["mres"]}
]
```
Không có `scenarios`, script tự sinh: nhánh mặc định, từng nhánh của mỗi gateway, từng boundary, từng message không tới.

## Chạy
```bash
python3 scripts/simulate_tokens.py spec.json             # bảng kịch bản → kết cục, kẹt ở đâu
python3 scripts/build_token_page.py spec.json tokens.html # trang HTML có animation để trình bày
```
Đọc kết quả:
- **KẸT** - token không tới được end: lỗ hổng cần sửa.
- **SAI KỲ VỌNG** - tới end khác với `expect`.
- **Node/luồng chưa kịch bản nào đi qua** - thiếu kịch bản, hoặc phần sơ đồ thừa.

## Từ lỗ hổng tới TO-BE
| Lỗ hổng điển hình | Đề xuất |
|---|---|
| Receive task chờ mãi | Timer boundary (ngắt) → bước hỏi lại trạng thái/đối soát → XOR theo kết quả → hoàn tác (hoàn tiền) hoặc đi tiếp |
| AND gộp chờ nhánh không bao giờ tới | Nhánh đó có XOR rẽ ra ngoài → gộp lại trước AND, hoặc đổi sang OR |
| Vòng lặp không thoát | Thêm bộ đếm/giới hạn và nhánh thoát ("Đã thử 3 lần?") |
| Ngoại lệ dẫn tới end chung "Kết thúc" | Tách end theo kết cục để báo cáo được tỉ lệ từng kết cục |

Ví dụ đầy đủ AS-IS → kịch bản kẹt → TO-BE: `examples/cinema-ticketing/review.md`.

## Trình bày với stakeholder
Đi từng kịch bản cùng người vận hành, hỏi ở mỗi gateway: "Thực tế có trường hợp nào khác không?", ở mỗi task chờ: "Nếu bên kia không trả lời thì hôm nay đang làm gì?". Câu trả lời thường là bước thủ công chưa được vẽ.
