# Danh mục 12 nhóm tình huống biên

Dùng như bảng kiểm: với mỗi nhóm, hỏi câu gợi ý, chỉ giữ cái áp dụng được.

| # | Nhóm | Câu hỏi gợi ý |
|---|---|---|
| 1 | **Dữ liệu** | Trống, chỉ khoảng trắng, quá dài, ký tự đặc biệt, trùng lặp, giá trị biên (min, max, ±1)? |
| 2 | **Thời gian** | Hết hạn đúng lúc đang thao tác? Múi giờ, cuối tháng/năm, ngày lễ, ngày giờ hệ thống lệch? Chờ quá lâu thì sao? |
| 3 | **Đồng thời** | Bấm đúp? Hai người cùng sửa/đặt một thứ (hàng cuối, khung giờ cuối)? Hai tab? Thao tác trong lúc job đêm chạy? |
| 4 | **Quyền hạn** | Người không có quyền vào tận đường dẫn? Quyền bị thu hồi giữa chừng? Làm hộ người khác? |
| 5 | **Trạng thái** | Thao tác ở trạng thái không cho phép? Thao tác lặp lại? Đối tượng đã bị xóa/khóa/hủy giữa chừng? Quay lại bước trước? |
| 6 | **Hệ thống ngoài** | Timeout? Trả lỗi? Trả thành công nhưng ta không nhận được? Trả trùng? Trả chậm sau khi ta đã hủy? Bảo trì? |
| 7 | **Số lượng** | 0, 1, nhiều, vượt giới hạn? Danh sách rất dài? Hàng loạt cùng lúc (khuyến mãi, 11.11)? |
| 8 | **Tiền tệ và số** | Làm tròn, phần lẻ, số âm, chia đều không hết, nhiều tiền tệ, thứ tự áp giảm giá? |
| 9 | **Tiếng Việt và ký tự** | Dấu tổ hợp/dựng sẵn, tìm kiếm không dấu, tên dài, emoji, ký tự điều khiển, khoảng trắng đặc biệt? |
| 10 | **Kênh và thiết bị** | Web vs app vs hotline cùng thao tác? Phiên bản app cũ? Mạng yếu, mất mạng giữa chừng? Bấm Back? |
| 11 | **Vận hành và dữ liệu cũ** | Dữ liệu tạo trước khi có tính năng này? Di chuyển dữ liệu? Rollback? Cấu hình đổi lúc đang chạy? Hỗ trợ khách xử lý thủ công thế nào? |
| 12 | **Lạm dụng và bảo mật** | Thử liên tục (brute force, dò mã)? Một người nhiều tài khoản? Lộ dữ liệu của người khác qua ID? Gian lận có tổ chức? |

## Cách chọn cái đáng giữ
- **Tác động cao + khả năng cao**: luôn giữ (thường nhóm 3, 6, 8).
- **Tác động cao + hiếm**: giữ nếu dính tiền, dữ liệu cá nhân hoặc pháp lý.
- **Tác động thấp + hiếm**: bỏ.
- Trùng nguyên nhân gốc: gộp thành một mục.

## Phân loại kết quả
| Loại | Nghĩa | Việc kế tiếp |
|---|---|---|
| **Yêu cầu** | Cần quyết định nghiệp vụ mới | Câu hỏi cho stakeholder, thêm vào BRD/story |
| **NFR** | Hiệu năng, bảo mật, độ tin cậy | Thêm yêu cầu phi chức năng |
| **Test** | Hành vi đã rõ, chỉ cần kiểm thử | Thêm AC/test case |
