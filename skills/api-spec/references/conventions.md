# Quy ước API (khởi điểm cho bản nháp)

Chỉ là đề xuất mặc định; đội kỹ thuật có thể đã có chuẩn riêng, hãy ưu tiên chuẩn của họ.

## Đặt tên
| Thành phần | Quy ước | Ví dụ |
|---|---|---|
| Tài nguyên | Danh từ số nhiều, chữ thường, gạch ngang | `/appointments`, `/doctors/{doctorId}/slots` |
| Hành động không phải CRUD | `POST` lên tài nguyên + động từ con | `POST /appointments/{id}/cancel` |
| Trường JSON | `camelCase` | `appointmentId`, `startTime` |
| Enum | Chữ hoa, gạch dưới | `CONFIRMED`, `NO_SHOW` |
| Mã lỗi nghiệp vụ | Chữ hoa, gạch dưới, ngắn gọn | `SLOT_TAKEN` |

## Method
| Method | Dùng | Idempotent |
|---|---|:-:|
| GET | Đọc | ✓ |
| POST | Tạo, hoặc hành động | ✗ (dùng `Idempotency-Key` khi quan trọng) |
| PUT | Thay toàn bộ | ✓ |
| PATCH | Sửa một phần | thường ✗ |
| DELETE | Xóa / hủy | ✓ |

## Mã HTTP
| Mã | Khi nào |
|---|---|
| 200 / 201 / 202 / 204 | Thành công / đã tạo / đã nhận, xử lý sau / thành công không nội dung |
| 400 | Request sai cấu trúc hoặc thiếu trường |
| 401 / 403 | Chưa xác thực / không có quyền |
| 404 | Không tìm thấy |
| 409 | Xung đột trạng thái (khung giờ đã có người đặt, trùng) |
| 422 | Dữ liệu hợp lệ về cấu trúc nhưng vi phạm quy tắc nghiệp vụ |
| 429 | Vượt giới hạn tốc độ |
| 5xx | Lỗi máy chủ / đối tác |

## Cấu trúc lỗi chung
```json
{ "code": "SLOT_TAKEN", "message": "Khung giờ này vừa có người đặt.", "details": [{"field": "slotId", "issue": "unavailable"}], "traceId": "..." }
```
`code` cho máy, `message` cho người; không đưa stack trace hay chi tiết nội bộ.

## Quy ước dữ liệu
| Dữ liệu | Quy ước |
|---|---|
| Tiền | Số nguyên theo đơn vị nhỏ nhất kèm `currency` (VND: `amount: 150000`), hoặc chuỗi thập phân; **một kiểu duy nhất** toàn API |
| Ngày giờ | ISO 8601 có múi giờ: `2026-11-20T08:30:00+07:00` |
| ID | Chuỗi, không đoán được; không lộ số thứ tự nội bộ |
| Phân trang | `page`, `pageSize` (hoặc con trỏ `cursor`), trả `total`/`nextCursor` |
| Lọc / sắp xếp | `?status=CONFIRMED&sort=-startTime` |
| Trường nhạy cảm | Che khi trả về (`0912****78`); ghi chú trong schema |

## Idempotency và bất đồng bộ
- `POST` tạo đơn/thanh toán nhận header `Idempotency-Key`; cùng khóa + cùng nội dung trả lại **cùng kết quả**, không tạo trùng.
- Việc kéo dài: trả `202` + tài nguyên trạng thái `PENDING`; client hỏi lại hoặc nhận **webhook** (nêu rõ cách xác thực và retry của webhook).

## Phiên bản
Đặt phiên bản trong đường dẫn (`/v1`) hoặc header; thay đổi phá vỡ ra phiên bản mới; ghi chính sách ngừng hỗ trợ.
