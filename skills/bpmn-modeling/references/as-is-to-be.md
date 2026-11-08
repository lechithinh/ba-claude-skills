# AS-IS → TO-BE

Lỗi phổ biến nhất: vẽ TO-BE ngay khi chưa hiểu AS-IS.

## AS-IS (hiện trạng)
- **Mục đích**: ghi ĐÚNG những gì đang chạy hôm nay, kể cả bước thừa, thao tác thủ công, vòng lặp vô lý - khác với quy trình "trong sách vở".
- **Thu thập**: job shadowing, phỏng vấn, walk-through từng bước; không chỉ dựa vào tài liệu quy trình.
- **Lưu ý**: ghi 100% quan sát, kể cả bước "vá lỗi" tạm thời (vd gọi điện xác nhận thủ công vì hệ thống hay lỗi). Đừng vội sửa/bỏ.
- **Đầu ra**: AS-IS BPMN + danh sách **Pain Points** cụ thể có số liệu ("bước 4 mất TB 2 ngày vì chờ email phê duyệt").

Nếu người dùng chỉ đưa mô tả (không quan sát): đánh dấu AS-IS là **bản dựng từ mô tả, chưa kiểm chứng** và liệt kê câu hỏi cần xác nhận.

## TO-BE (đề xuất)
- **Mục đích**: giải quyết trực tiếp các pain point của AS-IS, không "vẽ cho đẹp".
- **Căn cứ**: Gap Analysis (AS-IS so với mục tiêu), benchmark, đối chiếu mục tiêu kinh doanh.
- **Nguyên tắc**: chỉ giữ bước tạo giá trị; loại bước dư thừa; đề xuất tự động hoá ở chỗ thủ công tốn nhất; giữ nguyên bước bắt buộc về pháp lý.
- **Đầu ra**: TO-BE BPMN + **Gap Analysis Report**: khác AS-IS ở đâu, mỗi thay đổi giải quyết pain point nào, vì sao an toàn khi bỏ bước.

## Tìm pain point bằng token
Ngoài phỏng vấn, chạy token qua AS-IS với kịch bản "bên ngoài im lặng", "người dùng bỏ dở", "lặp lại nhiều lần" (`token-review.md`). Kịch bản kẹt là pain point có bằng chứng; ghi vào Gap Analysis cùng đề xuất sửa. Ví dụ: `examples/cinema-ticketing/review.md` (AS-IS kẹt khi cổng thanh toán không trả kết quả → TO-BE thêm timer + đối soát).

## Prompt đề xuất TO-BE
"Đây là sơ đồ AS-IS. Hãy đề xuất TO-BE với ràng buộc: giữ nguyên bước thẩm định thủ công cho khoản trên 100 triệu, không được bỏ bước tra cứu CIC vì lý do pháp lý. Với mỗi thay đổi, nêu rõ bước nào bị loại bỏ và vì sao an toàn khi loại bỏ."

## Mẫu Gap Analysis
| # | Bước AS-IS | Pain point | Thay đổi ở TO-BE | Lý do an toàn / ràng buộc | Chỉ số kỳ vọng |
|---|---|---|---|---|---|
| 1 | Nhập liệu thủ công | Sai sót, 2 giờ/hồ sơ | Lấy dữ liệu từ eKYC | Giữ lưu vết nguồn | Giảm lỗi nhập 90% |

Ví dụ: duyệt vay tiêu dùng 3–5 ngày, 2 lần đến chi nhánh, bỏ dở 41% → dưới 5 phút cho khoản nhỏ, 0 lần đến chi nhánh, mục tiêu bỏ dở dưới 15%.
