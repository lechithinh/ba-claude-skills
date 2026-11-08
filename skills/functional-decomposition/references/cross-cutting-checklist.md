# Chức năng xuyên suốt

Đây là nhóm chức năng gần như hệ thống nào cũng cần nhưng stakeholder hiếm khi nhắc, vì "hiển nhiên". Chúng chiếm một phần đáng kể công sức và là nơi thiếu sót gây đau nhất về sau. `fd_lint.py` kiểm 5 nhóm đầu (mã E1), nhận biết bằng `tags` hoặc từ khóa trong tên.

| Tag | Nhóm | Hỏi | Ví dụ chức năng |
|---|---|---|---|
| `auth` | Xác thực & phân quyền | Ai đăng nhập bằng cách nào? Vai trò nào thấy gì? | Đăng nhập theo vai trò; Phân quyền nhân viên |
| `notify` | Thông báo | Sự kiện nào cần báo ai, bằng kênh nào? Mất thông báo thì sao? | Gửi xác nhận; Nhắc người duyệt quá hạn |
| `audit` | Nhật ký thao tác | Thao tác nhạy cảm nào phải truy vết ai, khi nào, giá trị trước-sau? | Ghi nhật ký thay đổi số dư |
| `report` | Báo cáo | Ai cần số liệu nào, theo chu kỳ nào, xuất ra đâu? | Xem doanh thu theo ngày; Xuất Excel |
| `config` | Cấu hình & danh mục | Giá trị nào *không nên* hard-code (hạn mức, thời hạn, danh mục)? | Khai báo thông số; Khai báo ngày lễ |

## Các nhóm khác nên cân nhắc (lint chưa kiểm)
| Nhóm | Hỏi |
|---|---|
| Tích hợp | Hệ thống nào gửi/nhận dữ liệu? Khi đối tác lỗi, retry và đối soát thế nào? |
| Dữ liệu | Nhập/xuất hàng loạt, di chuyển dữ liệu cũ, lưu trữ và xóa theo thời hạn? |
| Hỗ trợ vận hành | Công cụ cho CSKH tra cứu và xử lý ngoại lệ? Truy cập khẩn cấp? |
| Tuân thủ | Chức năng nào do quy định bắt buộc (lưu hồ sơ, báo cáo cơ quan quản lý)? |
| Đa ngôn ngữ, đa tiền tệ, đa múi giờ | Có thật sự cần? |

## Nếu không cần: miễn trừ có lý do
```json
"waive": {"E1:notify": "Bản đầu không gửi thông báo; khách nghe gọi số tại quầy"}
```
Lý do tốt trả lời được "vì sao *chưa* cần", không chỉ "không cần". Khi phạm vi đổi, đọc lại các miễn trừ.

## Domain pack bổ sung gì
Pack ngân hàng nhắc xác thực theo ngưỡng, đối soát, nhật ký truy vết; pack thương mại điện tử nhắc đối soát thanh toán, hóa đơn điện tử, hoàn voucher. Xem `domain-integration.md`.
