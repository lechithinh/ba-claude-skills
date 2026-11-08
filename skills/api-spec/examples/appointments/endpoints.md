# Đầu ra: bảng endpoint và lỗi nghiệp vụ (đặt lịch khám)

> Prompt: *"Viết API spec cho các yêu cầu FR-01 (đặt lịch), FR-03 (hủy lịch), FR-08 (không trùng khung giờ)."* File OpenAPI đầy đủ: [openapi.yaml](openapi.yaml).

**Đối tượng gọi:** app của bệnh nhân. **Xác thực:** Bearer JWT. **Phiên bản:** `/v1`.

## Bảng endpoint
| Method | Đường dẫn | Mục đích | Idempotent | Thành công |
|---|---|---|:-:|---|
| GET | `/doctors/{doctorId}/slots?date=` | Xem khung giờ trống theo ngày | ✓ | 200 |
| POST | `/appointments` | Đặt lịch (header `Idempotency-Key`) | ✓ nhờ khóa | 201 |
| GET | `/appointments` | Xem lịch hẹn của tôi, lọc `status`, phân trang | ✓ | 200 |
| POST | `/appointments/{appointmentId}/cancel` | Hủy lịch hẹn | ✓ (hủy lại vẫn 200) | 200 |

## Lỗi nghiệp vụ
| Mã lỗi | HTTP | Khi nào | Thông điệp |
|---|---|---|---|
| `SLOT_TAKEN` | 409 | Khung giờ vừa có người đặt (FR-08) | "Khung giờ này vừa có người đặt." |
| `LIMIT_REACHED` | 422 | Đã giữ tối đa [2: xác nhận] lịch hẹn sắp tới | "Bạn chỉ được giữ tối đa 2 lịch hẹn sắp tới." |
| `CANCEL_WINDOW_PASSED` | 422 | Hủy sau mốc [2 giờ: xác nhận] trước giờ hẹn (FR-03) | "Chỉ hủy được trước giờ hẹn ít nhất 2 giờ…" |
| `VALIDATION_ERROR` | 400 | Thiếu/sai định dạng trường | "Dữ liệu không hợp lệ." |

## Giả định và câu hỏi mở
1. Tên trường và cấu trúc là **đề xuất**; đội kỹ thuật có thể đã có chuẩn đặt tên.
2. Checkbox đồng ý SMS (`smsReminderConsent`) có bắt buộc `true` không? (Pháp chế)
3. Hủy sau mốc 2 giờ: chặn như hiện tại, hay cho hủy nhưng tính no-show? (Quản lý phòng khám)
4. Có cần webhook báo cho hệ thống phòng khám khi lịch thay đổi không? (Tech lead)
5. Giới hạn tốc độ cụ thể (429) là bao nhiêu? (Tech lead)
