# Soát bản nháp phòng khám: từ lỗi tới bản đã sửa

Chế độ **B. Soát**. Đầu vào: một danh sách chức năng do đồng nghiệp viết (`spec-asis.json`, hiển thị dạng cây ở `hierarchy-asis.md` và `explorer-asis.html`). Không phân rã lại từ đầu; chỉ nhận xét và chỉ ra cách sửa.

## Cách dựng đầu vào
Nếu đồng nghiệp gửi danh sách dạng văn bản, dùng:
```bash
python3 scripts/outline_to_spec.py outline.txt spec.json --name "Đặt lịch khám phòng khám"
```
rồi bổ sung `objects`, `requirements`.

## 1. LỖI CẤU TRÚC — kết quả `fd_lint.py spec-asis.json`
```
Spec: Đặt lịch khám phòng khám — BẢN NHÁP CÓ LỖI (AS-IS để soát) — 3 module · 8 chức năng · sâu 4 cấp
LỖI       [A1] 4.1.1    ID có 3 đoạn nhưng nằm ở cấp 2
LỖI       [A1] 4.1.1    ID không khớp cha 3
LỖI       [B2] 1.1      "Quản lý lịch hẹn" dùng động từ chung chung - liệt kê từng thao tác cụ thể (tạo/xem/sửa/hủy…)
LỖI       [C2] FR-08    Yêu cầu chưa được chức năng nào phủ
CẢNH BÁO  [A2] 2        "Thông báo" chỉ có 1 con - thường là thừa một cấp
CẢNH BÁO  [A2] 2.1      "Nhắc lịch" chỉ có 1 con - thường là thừa một cấp
CẢNH BÁO  [A2] 3.3      "Hệ thống" chỉ có 1 con - thường là thừa một cấp
CẢNH BÁO  [A2] 3.3.1    "Cấu hình" chỉ có 1 con - thường là thừa một cấp
CẢNH BÁO  [A4] 3        Các nhánh con của "Lịch bác sĩ" sâu không đều (lệch 2 cấp)
CẢNH BÁO  [B1] 1.3      "Màn hình lịch trong ngày của lễ tân" có vẻ không bắt đầu bằng động từ (cần Động từ + Danh từ)
CẢNH BÁO  [B4] 2.1.1    "Gửi và nhắc lịch qua SMS" có vẻ gồm nhiều hành vi (sau và/hoặc là một động từ) - cân nhắc tách
CẢNH BÁO  [B5] 1.3      "Màn hình lịch trong ngày của lễ tân" nhắc tới màn hình/giao diện - chức năng mô tả việc làm, không mô tả chỗ làm
CẢNH BÁO  [C1] 1.3      "Màn hình lịch trong ngày của lễ tân" chưa có actor
CẢNH BÁO  [D2] timeoff  "Lịch nghỉ bác sĩ" chưa có chức năng Xem/Tìm
CẢNH BÁO  [D3] timeoff  "Lịch nghỉ bác sĩ" chưa có chức năng Sửa (nếu bất biến, đánh dấu "immutable": true)
CẢNH BÁO  [D4] slot     "Khung giờ" chưa có chức năng Hủy/Lưu trữ/Xóa (nếu cố ý không xóa, đánh dấu "no_delete": true)
CẢNH BÁO  [D4] timeoff  "Lịch nghỉ bác sĩ" chưa có chức năng Hủy/Lưu trữ/Xóa (nếu cố ý không xóa, đánh dấu "no_delete": true)
CẢNH BÁO  [D6] 1.1      "Quản lý lịch hẹn" làm đủ C-R-U-D trên một đối tượng - đây là 'Quản lý X' gộp, nên tách
CẢNH BÁO  [E1] audit    Chưa thấy nhóm chức năng xuyên suốt: Nhật ký thao tác (audit) (thêm hoặc miễn trừ kèm lý do)
CẢNH BÁO  [E1] auth     Chưa thấy nhóm chức năng xuyên suốt: Xác thực & phân quyền (thêm hoặc miễn trừ kèm lý do)
Kết quả: 4 lỗi, 16 cảnh báo, 0 miễn trừ
```

### Diễn giải các lỗi chính
| Mã | Vị trí | Vấn đề | Cách sửa (đã làm trong `spec.json`) |
|---|---|---|---|
| A1 | 4.1.1 | Mã đánh `4.1.1` nhưng nằm dưới module 3: ID không khớp cha | Tạo module 4 "Báo cáo" riêng, ID `4.1` |
| B2, D6 | 1.1 | "Quản lý lịch hẹn" làm đủ C-R-U-D: một dòng giấu ít nhất 5 chức năng | Tách thành Tạo tự phục vụ (1.1.2), Tạo hộ (1.1.3), Hủy (1.2.1), Xem (1.3.1)… |
| C2 | FR-08 | Không chức năng nào phủ "ngăn trùng khung giờ" | Thêm 1.1.4 "Chặn đặt trùng khung giờ" |
| B4 | 2.1.1 | "Gửi và nhắc lịch" gộp hai thời điểm | Tách 3.1 xác nhận và 3.2 nhắc lịch trước một ngày |
| B5, B1, C1 | 1.3 | "Màn hình lịch trong ngày của lễ tân" tả màn hình, không có actor | "Xem lịch trong ngày theo bác sĩ" (1.3.2), actor: lễ tân |
| A2, A4 | 2, 2.1, 3.3 | Cấp thừa (một con), nhánh 3.3.1.1 sâu lệch 2 cấp | Làm phẳng; đưa "Khai báo giờ làm việc" thành 2.1.1 |
| D2–D4 | Lịch nghỉ, Khung giờ | Thiếu Xem/Sửa/Hủy | Thêm 2.2.2, 2.2.3, 2.1.2, 2.1.3 |
| E1 | auth, audit | Thiếu đăng nhập và nhật ký | Thêm 5.1.1, 5.2.1, 5.3 |

## 2. THIẾU SÓT (lint không bắt được, người soát nhận ra)
- **Chồng lấn "Đặt lịch" (1.2) và "Đặt lịch hẹn" (3.2):** hai chức năng cùng việc nằm ở hai module. Lint B3 *không* báo vì tên ngắn (dưới 3 tiếng) - hạ ngưỡng thì báo oan quá nhiều, nên đây là việc của người soát. → giữ 1.1.2, bỏ bản ở module Lịch bác sĩ (không thuộc năng lực đó).
- **Ghi nhận bệnh nhân đến hoặc vắng** (chưa ai nhắc): cần để tính no-show của FR-07. → đã thêm 1.3.3.
- **Hồ sơ bệnh nhân** hoàn toàn vắng mặt dù bệnh nhân phải đăng ký tài khoản để đặt lịch. → đã thêm 5.1 (đăng ký, xem, cập nhật), đánh dấu `no_delete`.
- **Bác sĩ nghỉ khi đã có lịch hẹn:** chưa có chức năng cảnh báo. → thêm 2.2.4 và đưa vào câu hỏi mở.
- **Hủy hộ:** lễ tân đặt hộ nhưng không hủy hộ được. → thêm 1.2.2.

## 3. CÂU HỎI CHO STAKEHOLDER
1. Bác sĩ khóa lịch khi đã có lịch hẹn: ai liên hệ bệnh nhân và bằng cách nào? (Quản lý phòng khám)
2. Hủy sau mốc 2 giờ: chặn hay cho hủy nhưng tính vào no-show? (Quản lý phòng khám)
3. Có cho đổi lịch, hay chỉ hủy rồi đặt lại? (Quản lý phòng khám)
4. Đăng ký tài khoản bệnh nhân bằng gì: số điện thoại + OTP, hay cần thêm giấy tờ? (Lễ tân)
5. No-show tính từ lúc nào: quá giờ hẹn bao lâu không đến? (Quản lý phòng khám)

## 4. TÓM TẮT
| | Bản nháp | Bản đã sửa (`spec.json`) |
|---|---|---|
| Lỗi chặn | 4 | **0** |
| Cảnh báo | 16 | **0** |
| Yêu cầu được phủ | 7/8 | **8/8** |
| Chức năng (lá) | 8 | 31 |

## Cách chạy lại
```bash
python3 scripts/fd_lint.py examples/clinic-booking/spec-asis.json    # 4 lỗi, 16 cảnh báo
python3 scripts/fd_lint.py examples/clinic-booking/spec.json         # 0 lỗi, 0 cảnh báo
```

> Lưu ý: B1, B3, B4, B5 là heuristic: có thể **báo oan** (nên để người dùng quyết, dùng `waive` kèm lý do) và có thể **bỏ sót** (như trường hợp "Đặt lịch" ở trên). Lint là lưới lọc đầu tiên, không thay được người soát.
