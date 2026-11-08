# Dựng ngược chức năng từ hệ thống có sẵn

Dùng khi người dùng có một hệ thống đang chạy (hoặc kế thừa) và cần danh mục chức năng: để di chuyển, thay thế, ước lượng bảo trì, hay đơn giản là hiểu nó làm gì.

## Nguồn dữ liệu, từ đáng tin nhất
| Nguồn | Cho biết | Cảnh giác |
|---|---|---|
| **Nhật ký sử dụng / số liệu truy cập** | Chức năng nào *thật sự* được dùng | Chức năng dùng hàng năm một lần dễ bị coi nhầm là chết |
| **API, job, batch** | Hành vi hệ thống tự chạy, tích hợp | Có thể chứa chức năng không ai nhớ |
| **Báo cáo** | Câu hỏi nghiệp vụ đang được trả lời | Báo cáo cũ không còn ai xem |
| **Menu và màn hình** | Cách hệ thống *trình bày* chức năng | **Menu ≠ năng lực.** Menu thường theo lịch sử hoặc theo team |
| **Bảng dữ liệu / mô hình dữ liệu** | Đối tượng nghiệp vụ và vòng đời | Tên bảng là kỹ thuật, không phải ngôn ngữ nghiệp vụ |
| **Tài liệu cũ** | Ý định ban đầu | Thường lỗi thời |
| **Người dùng và vận hành** | Cách làm thực tế, đường vòng | Quan trọng nhất; cần phỏng vấn |

## Quy trình
1. **Đối tượng trước**: từ bảng/dữ liệu suy ra đối tượng nghiệp vụ và đặt tên theo ngôn ngữ nghiệp vụ.
2. **Chức năng theo đối tượng**: với mỗi đối tượng, tìm trong menu, API, job: ai tạo, xem, sửa, hủy (CRUD thực tế).
3. **Gom theo năng lực**: tạo module theo việc hệ thống làm, *không* chép cấu trúc menu.
4. **Đối chiếu với số liệu sử dụng**: gắn `note` cho từng chức năng: "dùng thường xuyên / hiếm / không thấy dùng".
5. **Đánh dấu bất thường**: chức năng trùng nhau, chức năng không có tài liệu, chức năng chết, chức năng chỉ một người biết.
6. **Câu hỏi cho đội vận hành**: "Chức năng này còn dùng không? Ai dùng? Nếu bỏ thì ai kêu?"

## Đầu ra
- Spec "as-is" (đánh dấu trong tên hoặc `note`; thêm `"as_is": true` nếu muốn) và đầu ra từ spec.
- Danh sách **chức năng nghi ngờ đã chết**, **trùng lặp**, **thiếu tài liệu**.
- Bảng đối chiếu: chức năng hiện có ↔ chức năng mong muốn (cho dự án thay thế) → Gap Analysis.

## Lưu ý
- Không suy diễn nghiệp vụ từ tên bảng hoặc tên hàm; ghi là **giả định** và nhờ người vận hành xác nhận.
- Hệ thống lớn: làm theo từng module, không cố phân rã toàn bộ một lượt.
- Dữ liệu thật (tên khách, số tài khoản) trong ảnh chụp màn hình: nhắc che trước khi dán.
