# Đặt lịch khám phòng khám — phân rã qua 6 bước

**Đầu vào (rút gọn từ biên bản họp 15/10):** "Bệnh nhân gọi điện đặt lịch, giờ cao điểm lễ tân không nghe kịp, no-show khoảng 30%, Excel hay trùng lịch. Muốn bệnh nhân tự đặt lịch online, chọn bác sĩ và giờ; nhắc lịch trước một ngày; hủy online trước 2 giờ; lễ tân đặt hộ người già và xem lịch từng bác sĩ trong ngày; bác sĩ tự khóa lịch khi nghỉ phép; cuối tháng cần báo cáo no-show theo bác sĩ."

Yêu cầu đã chốt `FR-01…FR-08` (xem `spec.json`). Kết quả cuối: `spec.json` → `hierarchy.md`, `diagram.mmd`, `diagram.svg`, `tree.csv`, `explorer.html`. Bản nháp có lỗi và cách soát: `spec-asis.json`, `review.md`.

---

## Bước 1 · Phạm vi và biên
- **Mục tiêu:** giảm no-show và giảm tải điện thoại cho lễ tân bằng đặt lịch tự phục vụ.
- **Trong phạm vi:** đặt và hủy lịch, nhắc lịch, lịch làm việc bác sĩ, báo cáo no-show.
- **Ngoài phạm vi:** thanh toán đặt cọc (ban giám đốc chưa quyết), Zalo (phase 2), hồ sơ bệnh án.

| Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|
| Ghi `scope.out` ngay từ đầu | Đặt cọc và Zalo được nhắc trong buổi họp nhưng chưa được hứa | Để lửng: về sau ai cũng nghĩ là có |
| Ghi giả định "một cơ sở, khung giờ cố định theo ca" | Ảnh hưởng thiết kế khung giờ | Bỏ qua: ước lượng sai |

## Bước 2 · Actor và đối tượng nghiệp vụ
- **Actor:** Bệnh nhân, Lễ tân, Bác sĩ, Quản lý phòng khám, Hệ thống.
- **Đối tượng:** Lịch hẹn, Khung giờ, Lịch nghỉ bác sĩ, Hồ sơ bệnh nhân, Bác sĩ.

| Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|
| "Khung giờ" là đối tượng riêng | Nó bị đọc, tạo, đóng khi bác sĩ nghỉ; có vòng đời riêng với lịch hẹn | Gộp vào Lịch hẹn: mất chỗ biểu diễn "khung giờ trống" và FR-08 (trùng giờ) |
| "Lịch nghỉ" `immutable` | Quy trình là hủy khai báo rồi tạo lại | Cho sửa: thêm quy tắc xung đột với lịch hẹn đã có mà chưa ai yêu cầu |
| "Hồ sơ bệnh nhân" `no_delete` | Hồ sơ phải lưu theo quy định quản lý | Cho xóa: rủi ro mất dữ liệu y tế |

## Bước 3 · Cấp 1: năng lực
Năm module: **1 Đặt và quản lý lịch hẹn · 2 Lịch làm việc bác sĩ · 3 Thông báo · 4 Báo cáo · 5 Truy cập và quản trị**.

| Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|
| Module theo năng lực | Còn đúng khi đổi giao diện hay đổi team | Theo màn hình ("Màn bệnh nhân", "Màn lễ tân"): cùng một chức năng xuất hiện hai nơi |
| "Thông báo" là module riêng | Dùng chung cho xác nhận, nhắc, hủy; sau này thêm kênh Zalo | Nằm trong từng module: lặp ba lần, đổi kênh phải sửa ba chỗ |

## Bước 4 · Cấp 2–3
Ví dụ module 1 → tính năng **1.1 Đặt lịch khám** → chức năng *1.1.1 Tìm khung giờ trống theo bác sĩ và ngày*, *1.1.2 Tạo lịch hẹn tự phục vụ*, *1.1.3 Tạo lịch hẹn hộ bệnh nhân*, *1.1.4 Chặn đặt trùng khung giờ*.

| Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|
| Tách "tự phục vụ" và "đặt hộ" (1.1.2, 1.1.3) | Actor, kênh và quy tắc khác nhau (người già gọi điện) | Một chức năng "Đặt lịch": không biết ai làm, không viết AC riêng |
| 1.1.4 "Chặn đặt trùng" là chức năng riêng | FR-08 là yêu cầu riêng, có kịch bản kiểm thử riêng (hai người cùng chọn một giờ) | Chôn trong 1.1.2: dễ quên khi lễ tân cũng đặt (1.1.3) |
| Dừng ở cấp 3 | Mỗi lá viết được một user story | Xuống cấp 4 ("Kiểm tra giờ", "Lưu lịch"): đã là thiết kế |

## Bước 5 · Kiểm MECE, CRUD, xuyên suốt
Ma trận CRUD cho **Lịch hẹn**: Tạo 1.1.2, 1.1.3 · Xem 1.3.1, 1.3.2 · Sửa 1.3.3 (ghi nhận đến/vắng) · Hủy 1.2.1, 1.2.2.

Kiểm tìm ra thiếu sót mà biên bản không nhắc:
- **1.3.3 Ghi nhận bệnh nhân đến hoặc vắng:** bắt buộc để tính no-show (FR-07), chưa ai nói tới.
- **2.2.4 Cảnh báo lịch hẹn trùng thời gian nghỉ:** nếu bác sĩ khóa lịch mà đã có lịch hẹn thì sao? Đưa vào câu hỏi mở.
- **Xuyên suốt:** thêm đăng nhập (5.1.1, 5.2.1), nhật ký (5.3), cấu hình (5.4); thông báo (module 3) và báo cáo (module 4) đã có.

| Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|
| "Hồ sơ bệnh nhân" miễn D bằng `no_delete` | Có lý do rõ | Thêm "Xóa hồ sơ": trái quy định lưu trữ |
| Các chức năng suy ra gắn `derived: true` | Tách rõ "stakeholder nói" với "BA đề xuất" | Gắn đại yêu cầu gần nghĩa: truy vết giả |

## Bước 6 · Truy vết và lint
- 8 yêu cầu `FR-01…FR-08`: **đủ 8/8** có chức năng phủ.
- Chức năng không có yêu cầu: tất cả đã `derived` (thông lệ và domain), liệt kê trong báo cáo để xác nhận.
- Lint: **0 lỗi, 0 cảnh báo** (`python3 scripts/fd_lint.py examples/clinic-booking/spec.json`).

## Danh sách giả định
- [ ] Một cơ sở, khung giờ cố định theo ca.
- [ ] Nhắc lịch qua SMS ở phase 1.
- [ ] Hủy trước giờ hẹn 2 giờ là cố định (có thể cần cấu hình: Q).

## Câu hỏi cho phòng khám
1. Bác sĩ khóa lịch khi đã có lịch hẹn: ai liên hệ bệnh nhân? (Quản lý)
2. Hủy sau mốc 2 giờ: chặn hay cho hủy nhưng tính no-show? (Quản lý)
3. Có cho đổi lịch, hay chỉ hủy rồi đặt lại? (Quản lý)
4. Đặt cọc online có thu không, thu từ khi nào? (Ban giám đốc)
