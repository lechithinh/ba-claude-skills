---
name: screen-spec
description: Từ ảnh mockup/wireframe/screenshot (hoặc mô tả bằng lời) viết đặc tả màn hình cho dev và tester - mục đích, actor, điều hướng, bảng trường (loại control, kiểu dữ liệu, bắt buộc, độ dài, định dạng, mặc định, nguồn dữ liệu, validation, thông báo lỗi), hành vi nút, các trạng thái màn hình (loading, rỗng, lỗi, phân quyền), quy tắc tương tác giữa các trường; tách rõ điều nhìn thấy trong ảnh với điều suy ra và câu hỏi còn mở. Dùng khi người dùng đưa ảnh thiết kế UI và cần viết đặc tả màn hình, field spec, screen description cho SRS/BRD. Trigger - "đặc tả màn hình", "screen spec", "mô tả màn hình", "field spec", "bảng trường", "validation", "từ mockup viết spec", "đặc tả UI".
---

# Đặc tả màn hình (Screen Spec)

Đọc một ảnh thiết kế rồi viết đặc tả mà dev code được và tester kiểm thử được, **không bịa** những gì ảnh không cho thấy. Phần đặc tả màn hình thường ngốn nhiều giờ nhất trong SRS; skill này làm bản nháp đầy đủ để BA chỉ còn việc xác nhận.

## Quy trình

1. **Nhận diện màn hình** - tên, mục đích, actor, tiền điều kiện, đi vào từ đâu / đi ra đâu.
2. **Kiểm kê thành phần theo vùng** (thanh tiêu đề, form, danh sách/bảng, nút, thông báo). Đánh số để tham chiếu.
3. **Bảng trường** - mỗi trường nhập/hiển thị một dòng (khuôn bên dưới). Dùng `references/field-spec-guide.md` để chọn kiểu validation và thông báo lỗi phổ biến.
4. **Nút và hành động** - điều kiện bật/tắt, việc xảy ra khi bấm, kết quả thành công và thất bại.
5. **Trạng thái màn hình** - đang tải, rỗng, lỗi tải, lỗi mạng khi gửi, hết phiên, chỉ-đọc theo quyền, trạng thái từng control (mặc định, chọn, vô hiệu, lỗi).
6. **Quy tắc tương tác** - trường phụ thuộc nhau (chọn A thì B tải lại), tự tính, tự điền, thứ tự validate (khi rời trường hay khi gửi).
7. **Thông báo và văn bản** - nội dung lỗi/thành công/xác nhận, đúng giọng điệu sản phẩm.
8. **Tách bạch nguồn thông tin** - đánh dấu mỗi chi tiết là **[ảnh]** (nhìn thấy), **[suy ra]** (hợp lý nhưng ảnh không nêu) hoặc **[xác nhận]** (giá trị cần stakeholder quyết). Cuối cùng liệt kê câu hỏi mở.

## Khuôn bảng trường

| # | Nhãn | Control | Kiểu dữ liệu | Bắt buộc | Độ dài/định dạng | Mặc định | Nguồn dữ liệu | Validation | Thông báo lỗi | Nguồn tt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Chuyên khoa | Dropdown | Mã danh mục | Có [ảnh: dấu *] | - | Trống, placeholder "Chọn chuyên khoa" | Danh mục chuyên khoa | Phải chọn | "Vui lòng chọn chuyên khoa" | [ảnh] |

## Đầu ra

```markdown
## Đặc tả màn hình: <tên>
**Mục đích · Actor · Tiền điều kiện · Điều hướng (vào/ra)**
### 1. Thành phần màn hình     (đánh số, theo vùng)
### 2. Bảng trường             (khuôn trên)
### 3. Nút và hành động
### 4. Trạng thái màn hình
### 5. Quy tắc tương tác
### 6. Thông báo và văn bản
### 7. Giả định và điều không thấy trong ảnh
### 8. Câu hỏi mở (ai nên trả lời)
```

## Quy tắc
- **Không bịa giá trị**: độ dài tối đa, định dạng, hạn mức, thời hạn không thể hiện trong ảnh thì ghi `[xác nhận]` kèm đề xuất thông lệ, không khẳng định.
- **Chỉ mô tả điều nhìn thấy hoặc suy ra có lý do.** Nếu ảnh mờ, bị cắt, hay không có trạng thái lỗi, nói rõ "không thấy trong ảnh".
- Mô tả **hành vi**, không mô tả màu sắc, phông chữ, vị trí pixel (đó là việc của thiết kế).
- Mỗi trường bắt buộc/tùy chọn phải bám theo ký hiệu trong ảnh (dấu `*`), nếu mâu thuẫn với logic nghiệp vụ thì nêu thành câu hỏi.
- Dữ liệu cá nhân và nhạy cảm (số điện thoại, số tài khoản, CCCD): ghi rõ che/mask thế nào khi hiển thị; nhắc thay dữ liệu thật trong ảnh bằng dữ liệu giả.
- Phần đồng ý/consent (SMS, marketing, điều khoản): ghi rõ **bắt buộc hay tùy chọn** và hỏi bộ phận pháp lý nếu là điều kiện để dùng dịch vụ.
- Với domain có pack (`domain-banking`: số tài khoản, OTP, hạn mức; `domain-ecommerce`: giá, tồn kho, voucher; `domain-payments`, `domain-lending`, `domain-logistics`), dùng `checklist.md` để bổ sung trạng thái và thông báo hay bị quên, đánh dấu `[domain]`.
- Ảnh nhiều màn hình: mỗi màn hình một đặc tả; mô tả luồng giữa các màn bằng `bpmn-modeling` hoặc `ba-diagrams`.

## Chuỗi skill
`functional-decomposition` (chức năng) → **`screen-spec`** (đặc tả màn) → `user-story-writer` (story + AC) → `edge-case-finder` (phản biện). Ma trận lỗi validation nhiều tổ hợp: `decision-table`.

## Tham chiếu
| File | Nội dung |
|---|---|
| `references/field-spec-guide.md` | Danh mục validation, định dạng và mẫu thông báo lỗi thường dùng |
| `LEARN.md` | Đặc tả màn hình tốt gồm những gì, lỗi thường gặp |
| `examples/booking-form/` | Ảnh `mockup.png` + đặc tả sinh ra từ ảnh đó |
