---
name: api-spec
description: Từ yêu cầu, user story hoặc luồng nghiệp vụ viết bản nháp API contract - danh sách endpoint (method, đường dẫn, mục đích, xác thực, idempotent), schema request/response kèm ví dụ, mã lỗi HTTP và mã lỗi nghiệp vụ, phân trang/lọc/sắp xếp, idempotency key, webhook nếu có - và xuất file OpenAPI 3.0 YAML import được vào Postman, Swagger/Redoc. Dùng khi BA cần đặc tả API cho dev/đối tác, hoặc tài liệu tích hợp. Trigger - "API spec", "đặc tả API", "OpenAPI", "Swagger", "endpoint", "REST API", "request response", "mã lỗi API", "tài liệu tích hợp", "Postman collection".
---

# API Spec (bản nháp OpenAPI từ yêu cầu)

Biến yêu cầu nghiệp vụ thành **hợp đồng API** rõ ràng để dev hai phía và tester cùng đọc. BA làm bản nháp đủ chi tiết về *hành vi và dữ liệu nghiệp vụ*; kiến trúc sư/dev tinh chỉnh phần kỹ thuật.

## Quy trình

1. **Xác định tài nguyên và hành động**: danh từ nghiệp vụ (lịch hẹn, đơn hàng, thanh toán) → tài nguyên; thao tác (đặt, hủy, hoàn) → method hoặc "hành động con" (`POST /appointments/{id}/cancel`). Lấy từ cây chức năng (`functional-decomposition`) và story (`user-story-writer`) nếu có.
2. **Ai gọi, xác thực thế nào**: người dùng cuối, hệ thống nội bộ, đối tác; token, API key; phạm vi quyền.
3. **Bảng endpoint**: method, đường dẫn, mục đích, xác thực, **idempotent hay không**, mã thành công.
4. **Schema và ví dụ**: trường, kiểu, bắt buộc, ràng buộc (độ dài, enum, định dạng), nullable; mỗi request/response có ví dụ thật. Tiền, ngày, trạng thái theo quy ước trong `references/conventions.md`.
5. **Lỗi**: mỗi endpoint liệt kê mã HTTP và **mã lỗi nghiệp vụ** (ví dụ `SLOT_TAKEN`) kèm thông điệp; một cấu trúc lỗi chung.
6. **Hành vi đặc biệt**: phân trang, lọc, sắp xếp, idempotency-key, giới hạn tốc độ, bất đồng bộ/webhook, phiên bản.
7. **Xuất OpenAPI 3.0 YAML**, tự soát theo checklist bên dưới.
8. **Câu hỏi mở** cho dev/đối tác.

## Đầu ra

```markdown
## API: <tên>
**Phạm vi · Đối tượng gọi · Xác thực · Base URL / phiên bản**
### Bảng endpoint
| Method | Đường dẫn | Mục đích | Auth | Idempotent | Thành công |
### Lỗi nghiệp vụ
| Mã lỗi | HTTP | Khi nào | Thông điệp |
### OpenAPI (YAML)      (một khối ```yaml)
### Giả định và câu hỏi mở
```

## Checklist soát trước khi giao
- [ ] Mọi endpoint có `operationId` duy nhất, `summary`, `tags`.
- [ ] Có response thành công **và** các lỗi 400/401/403/404, cùng 409/422 cho lỗi nghiệp vụ; 429, 5xx ở mức chung.
- [ ] Mọi `$ref` trỏ tới schema có thật; mọi tham số đường dẫn được khai báo.
- [ ] Mọi request/response có `example`.
- [ ] POST gây thay đổi quan trọng (tiền, đơn hàng) có **Idempotency-Key**.
- [ ] Trường tiền dùng kiểu đã thống nhất; ngày giờ ISO 8601; trạng thái là `enum`.
- [ ] Trường nhạy cảm (SĐT, số tài khoản, CCCD) được ghi chú và che khi trả về.
- [ ] Không nhúng khóa bí mật, token thật, dữ liệu cá nhân thật trong ví dụ.

## Quy tắc
- **Không bịa quy tắc nghiệp vụ**: giới hạn, thời hạn, mã lỗi chưa có trong yêu cầu thì ghi `[xác nhận]` hoặc đưa vào câu hỏi mở.
- Ghi rõ **giả định** về tên trường và cấu trúc; đó là đề xuất để dev phản hồi, không phải hợp đồng cuối cùng.
- Tên trường và đường dẫn nhất quán một kiểu (`camelCase` trường, danh từ số nhiều cho tài nguyên) theo `references/conventions.md`.
- Lỗi trả về **mã máy đọc được + thông điệp người đọc được**; không lộ chi tiết nội bộ.
- Có domain pack: dùng `data-model.md` để lấy bộ trạng thái (`status` enum), `integrations.md` để thấy callback/timeout cần xử lý (`domain-payments`, `domain-banking`, `domain-ecommerce`, `domain-lending`, `domain-logistics`).
- Skill chỉ viết hợp đồng; việc kiểm thử API và mock server không thuộc phạm vi (xuất YAML rồi dùng công cụ như Postman).

## Chuỗi skill
`functional-decomposition` → `user-story-writer` → **`api-spec`** → `edge-case-finder` (timeout, trùng, đồng thời) → `decision-table` (rule nghiệp vụ trong API).

## Tham chiếu
| File | Nội dung |
|---|---|
| `references/conventions.md` | Quy ước đặt tên, mã HTTP, cấu trúc lỗi, phân trang, idempotency, tiền và ngày |
| `LEARN.md` | API contract là gì, vì sao BA nên viết bản nháp |
| `examples/appointments/` | `openapi.yaml` + bảng endpoint cho đặt lịch khám |
