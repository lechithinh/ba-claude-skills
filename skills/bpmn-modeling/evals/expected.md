# Tiêu chí đạt

Mỗi đề đạt khi thoả **tất cả** mục "Bắt buộc". Mục "Nên có" dùng để so sánh chất lượng giữa các phiên bản skill.

## Áp dụng cho mọi đề vẽ (E1, E3, E5)
**Bắt buộc**
- Có spec JSON và ít nhất: Mermaid hoặc `.bpmn`; nếu có `.bpmn` thì `bpmn_lint.py` 0 lỗi.
- Báo cáo có đủ: phạm vi, bảng tóm tắt, bảng quyết định ký hiệu (vì sao dùng / vì sao không), kịch bản token, giả định, câu hỏi cho người vận hành.
- Bên ngoài (cổng thanh toán, đơn vị vận chuyển) là pool riêng, nối bằng message flow.
- Mọi end event đặt tên theo trạng thái; mọi XOR có câu hỏi và nhãn nhánh.

**Nên có**
- Có kịch bản "bên ngoài không phản hồi" và xử lý nó (timer + đối soát), hoặc chỉ ra là lỗ hổng.
- Trang `tokens.html` khi người dùng cần trình bày.

## E1
- Timer boundary **viền liền** 15 phút trên bước đặt cọc (không dùng gateway "Quá 15 phút?").
- Message boundary hoặc nhánh xử lý "bác sĩ huỷ lịch" quay lại bước chọn giờ qua XOR gộp.

## E2
- Hỏi tối đa 4 câu trong một lượt (ai duyệt, có nhiều cấp không, hết hạn duyệt thì sao, có hệ thống HR không) **hoặc** vẽ với danh sách giả định rõ ràng. Không bịa thêm cấp phê duyệt mà không ghi là giả định.

## E3
- Ít nhất 3 bên: sàn, người bán, đơn vị vận chuyển; người mua là pool thu gọn hoặc được giải thích theo `pool-vs-lane.md`.
- Vòng giao lại có giới hạn ("Đã giao thất bại 3 lần?") và nhánh hoàn hàng.

## E4
Phải chỉ ra (dẫn mã lỗi trong `mistakes-catalog.md`):
- A6: task "Đơn hàng" là danh từ.
- A3: gateway không tên, nhánh không nhãn.
- A4: nhánh "Huỷ đơn" không về end event.
- B2: luồng đi ra từ end event "Kết thúc".
- End event tên "Kết thúc" không theo trạng thái.
Không vẽ lại toàn bộ trừ khi được yêu cầu.

## E5
- AS-IS ghi đúng các bước thủ công (tải hồ sơ, email trưởng phòng).
- Chỉ ra pain point "chờ trưởng phòng không giới hạn" (bằng token: kịch bản trưởng phòng im lặng bị kẹt).
- TO-BE có timer/nhắc việc hoặc leo thang + Gap Analysis; giữ bước bắt buộc về pháp lý nếu có.

## E6
- Trả lời: **timer boundary viền liền** trên task chờ thanh toán. Giải thích vì sao không dùng gateway (không biết chờ) và vì sao không viền đứt (việc thanh toán vẫn chạy trên đơn đã huỷ).

## E7
- Hệ thống điều phối: lane (hoặc pool chính). Tài xế, ví điện tử: pool riêng. Khách hàng: pool riêng hoặc lane, có lý do, và nói rõ hệ quả (message flow vs sequence flow).

## E8
- Viết `scenarios` (choices / fire / silent) và chạy `simulate_tokens.py`.
- Báo đúng kịch bản kẹt (nếu E1 chưa xử lý cổng thanh toán im lặng) và đề xuất sửa.
