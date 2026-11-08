# Phần mềm bán hàng quán cà phê

**Trong phạm vi:** Gọi món và thu tiền tại quầy; Pha chế; Thực đơn và giá; Chốt ca và báo cáo ngày
**Ngoài phạm vi:** Giao hàng; Kho nguyên liệu; Tích điểm khách hàng
**Actor:** Thu ngân, Pha chế, Quản lý quán, Hệ thống

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Ghi chú |
|---|---|---|---|---|---|
| 1 | **Gọi món và tạo đơn** | Module |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Tạo đơn tại quầy | Feature |  |  |  |
| 1.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chọn món vào đơn | Function | Thu ngân | M |  |
| 1.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ghi chú tuỳ chọn cho món | Function | Thu ngân | S |  |
| 1.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Áp dụng giảm giá cho đơn | Function | Thu ngân, Quản lý quán | C | Giảm trên ngưỡng cần quản lý xác nhận |
| 1.2 | &nbsp;&nbsp;&nbsp;Sửa và hủy đơn | Feature |  |  |  |
| 1.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sửa món trong đơn chưa thanh toán | Function | Thu ngân | M |  |
| 1.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy đơn | Function | Thu ngân, Quản lý quán | M | Hủy đơn đã thanh toán cần quản lý |
| 1.3 | &nbsp;&nbsp;&nbsp;Xem đơn | Feature |  |  |  |
| 1.3.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem hàng chờ pha chế | Function | Pha chế | M |  |
| 1.3.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tra cứu đơn theo mã | Function | Thu ngân, Quản lý quán | S |  |
| 2 | **Pha chế** | Module |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Nhận đơn vào hàng chờ | Function | Pha chế | M |  |
| 2.2 | &nbsp;&nbsp;&nbsp;Đánh dấu đơn đã xong | Function | Pha chế | M |  |
| 2.3 | &nbsp;&nbsp;&nbsp;Gọi khách nhận món | Function | Thu ngân | S |  |
| 3 | **Thanh toán** | Module |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Thu tiền mặt | Function | Thu ngân | M |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Thu tiền qua mã QR | Function | Thu ngân | S |  |
| 3.3 | &nbsp;&nbsp;&nbsp;In hoá đơn | Function | Thu ngân | M |  |
| 3.4 | &nbsp;&nbsp;&nbsp;Hoàn tiền đơn đã hủy | Function | Quản lý quán | S |  |
| 4 | **Thực đơn và giá** | Module |  |  |  |
| 4.1 | &nbsp;&nbsp;&nbsp;Thêm món mới | Function | Quản lý quán | M |  |
| 4.2 | &nbsp;&nbsp;&nbsp;Sửa giá món | Function | Quản lý quán | M |  |
| 4.3 | &nbsp;&nbsp;&nbsp;Ngừng bán món | Function | Quản lý quán | S | Lưu trữ, không xoá để giữ lịch sử đơn |
| 5 | **Chốt ca và báo cáo** | Module |  |  |  |
| 5.1 | &nbsp;&nbsp;&nbsp;Chốt ca | Function | Thu ngân | M |  |
| 5.2 | &nbsp;&nbsp;&nbsp;Đối chiếu tiền cuối ca | Function | Thu ngân, Quản lý quán | M |  |
| 5.3 | &nbsp;&nbsp;&nbsp;Xem doanh thu theo ngày | Function | Quản lý quán | S |  |
| 6 | **Hệ thống** | Module |  |  |  |
| 6.1 | &nbsp;&nbsp;&nbsp;Đăng nhập theo vai trò | Function | Thu ngân, Pha chế, Quản lý quán | M |  |
| 6.2 | &nbsp;&nbsp;&nbsp;Ghi nhật ký thao tác nhạy cảm | Function | Hệ thống | S |  |
| 6.3 | &nbsp;&nbsp;&nbsp;Khai báo thông số quán | Function | Quản lý quán | C | Giờ mở cửa, thuế, mẫu hoá đơn |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Đơn gọi món | 1.1.1 | 1.3.1, 1.3.2 | 1.1.2, 1.1.3, 1.2.1, 2.1, 2.2 | 1.2.2 |
| Món trong thực đơn | 4.1 | 1.1.1 | 4.2 | 4.3 |
| Giao dịch thanh toán | 3.1, 3.2 | 3.3 | 3.4 | — (miễn: Giao dịch tài chính không xóa; sai sót xử lý bằng hoàn tiền) |

## 4. Actor × Module (số chức năng)

| Actor | 1. Gọi món và tạo đơn | 2. Pha chế | 3. Thanh toán | 4. Thực đơn và giá | 5. Chốt ca và báo cáo | 6. Hệ thống |
|---|---|---|---|---|---|---|
| Thu ngân | 6 | 1 | 3 |  | 2 | 1 |
| Pha chế | 1 | 2 |  |  |  | 1 |
| Quản lý quán | 3 |  | 1 | 3 | 2 | 2 |
| Hệ thống |  |  |  |  |  | 1 |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **6** · Tính năng: **3** · Chức năng (lá): **23** · Độ sâu: **3** cấp
- Ưu tiên: C: 2, M: 13, S: 8
