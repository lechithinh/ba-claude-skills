# Hướng dẫn đặt tên

## Công thức
| Cấp | Dạng tên | Ví dụ |
|---|---|---|
| Module (cấp 1) | Danh từ chỉ năng lực | "Đặt và quản lý lịch hẹn", "Thông báo" |
| Tính năng (cấp 2) | Danh từ hoặc cụm động từ | "Hủy lịch hẹn", "Khung giờ khám" |
| **Chức năng (lá)** | **Động từ cụ thể + Danh từ** | "Hủy lịch hẹn online trước giờ hẹn 2 giờ" |

Lá là thứ duy nhất bị lint kiểm tên (mã B1–B6).

## Động từ nên dùng và nên tránh
| Nên dùng (cụ thể) | Tránh làm tên lá (mơ hồ) |
|---|---|
| Tạo, Xem, Tìm, Sửa, Hủy, Duyệt, Từ chối, Gửi, Nhận, Tính, Kiểm tra, Xuất, Nhập, Khóa, Mở khóa, Đối soát, Cấu hình | Quản lý, Xử lý, Hỗ trợ, Thực hiện, Thao tác (lint B2: **lỗi**) |

"Quản lý X" gom 4–6 chức năng. Thấy tên này ở lá thì tách ra từng thao tác; còn ở module hoặc tính năng thì chấp nhận được miễn là con của nó đã liệt kê cụ thể.

## Một chức năng, một hành vi
| Chưa tốt | Tốt hơn | Vì sao |
|---|---|---|
| Gửi và nhắc lịch | Gửi xác nhận đặt lịch / Gửi SMS nhắc lịch | Hai thời điểm, hai kích hoạt, hai kiểm thử |
| Chốt ca và đối chiếu tiền | Chốt ca / Đối chiếu tiền cuối ca | Hai kết quả khác nhau, có thể do hai người làm |
| Quản lý lịch hẹn | Tạo / Xem / Hủy lịch hẹn | Mỗi thao tác có quy tắc riêng |

Dấu hiệu gộp: "và/hoặc" nối **hai động từ** (lint B4). "và" nối hai danh từ ("Đồng bộ cây tổ chức và người duyệt") thường vẫn là một hành vi.

## Mô tả việc làm, không mô tả chỗ làm
| Chưa tốt | Tốt hơn |
|---|---|
| Màn hình lịch trong ngày của lễ tân | Xem lịch trong ngày theo bác sĩ |
| Popup xác nhận hủy | Xác nhận hủy lịch hẹn |

Màn hình là cách trình bày, có thể đổi; chức năng là thứ doanh nghiệp cần (lint B5).

## Mức chi tiết trong tên
- Đủ để phân biệt với chức năng kề bên, không kể quy tắc: "Hủy lịch hẹn online trước giờ hẹn 2 giờ" tạm chấp nhận; con số **2 giờ** nên nằm ở `note` hoặc business rule vì có thể đổi.
- Quá 12 tiếng: rút gọn, đưa chi tiết vào `note` (lint B6).
- Không đưa tên công nghệ vào chức năng ("Gọi API X"): hãy nói "Gửi yêu cầu thanh toán".

## Ngôn ngữ
Tên theo ngôn ngữ của stakeholder. Thuật ngữ chuẩn ngành giữ nguyên (CIF, COD, SKU) nếu đội đang dùng. Một hệ thống chỉ dùng **một** ngôn ngữ cho tên chức năng để lọc và tìm kiếm không bị rối.
