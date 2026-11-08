# API Contract cho BA

## Vì sao BA nên viết bản nháp
Dev frontend và backend (hoặc hai công ty đối tác) cần thống nhất **hình dạng dữ liệu** trước khi code. Nếu không, họ thống nhất bằng tin nhắn, rồi lệch nhau lúc tích hợp. BA không cần quyết định kiến trúc; BA đưa vào **ngôn ngữ nghiệp vụ**: trường nào bắt buộc, trạng thái nào có, lỗi nghiệp vụ nào, hành vi khi trùng yêu cầu.

## Những thứ BA thật sự đóng góp
| BA đóng góp | Dev bổ sung |
|---|---|
| Tài nguyên và hành động theo nghiệp vụ | Cấu trúc URL cuối cùng |
| Trường, ràng buộc, enum trạng thái | Kiểu dữ liệu chi tiết, hiệu năng |
| **Mã lỗi nghiệp vụ** và khi nào xảy ra | Mã HTTP chính xác, cơ chế retry |
| Hành vi trùng, hết hạn, hủy | Cách đảm bảo bằng idempotency, khóa |

## Khái niệm cần nắm
- **Idempotency**: gọi cùng yêu cầu hai lần không làm hai lần (quan trọng với thanh toán, tạo đơn).
- **Bất đồng bộ / callback**: kết quả đến sau; cần webhook, trạng thái `pending`.
- **Mã lỗi nghiệp vụ**: tách khỏi mã HTTP để client xử lý (`SLOT_TAKEN` → tải lại khung giờ).
- **Phiên bản**: thay đổi phá vỡ phải ra phiên bản mới.

## Công cụ
Dán YAML vào **Swagger Editor** hoặc import vào **Postman** để xem tài liệu, tạo collection, dựng mock. Kiểm tra phiên bản công cụ hiện hành.

## Thực hành
Lấy một user story ("khách hủy lịch hẹn"), hỏi Claude: *"Viết API spec OpenAPI cho story này."* Xem các mã lỗi nghiệp vụ mà nó đề xuất và đối chiếu với quy tắc thực tế của bạn.
