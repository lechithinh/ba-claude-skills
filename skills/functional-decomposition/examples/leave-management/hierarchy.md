# Hệ thống quản lý nghỉ phép nhân viên

**Trong phạm vi:** Đăng ký nghỉ; Duyệt; Số dư phép và chính sách; Lịch nghỉ nhóm; Báo cáo
**Ngoài phạm vi:** Tính lương; Chấm công chi tiết
**Actor:** Nhân viên, Quản lý trực tiếp, HR, Hệ thống

**Giả định:**
- Công ty 300 người, duyệt một cấp bởi quản lý trực tiếp
- Có nhiều loại nghỉ: phép năm, ốm, không lương, khác [xác nhận với HR]
- Số ngày phép theo chính sách công ty và quy định hiện hành [xác nhận với HR/Pháp chế]
- Chưa có domain pack cho nhân sự: danh mục chức năng dựa trên thông lệ chung

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Ghi chú |
|---|---|---|---|---|---|
| 1 | **Đăng ký nghỉ** | Module |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Tạo và gửi đơn | Feature |  |  |  |
| 1.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo đơn nghỉ | Function | Nhân viên | M |  |
| 1.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kiểm tra số dư phép khi gửi đơn | Function | Hệ thống | M |  |
| 1.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo đơn nghỉ hộ nhân viên | Function | HR, Quản lý trực tiếp | C |  |
| 1.2 | &nbsp;&nbsp;&nbsp;Sửa và hủy đơn | Feature |  |  |  |
| 1.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sửa đơn chưa duyệt | Function | Nhân viên | S |  |
| 1.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy đơn chưa duyệt | Function | Nhân viên | M |  |
| 1.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xin hủy đơn đã duyệt | Function | Nhân viên | S | Cần quản lý duyệt lại |
| 1.3 | &nbsp;&nbsp;&nbsp;Xem lịch sử đơn của tôi | Function | Nhân viên | M |  |
| 2 | **Duyệt đơn** | Module |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Xử lý đơn chờ duyệt | Feature |  |  |  |
| 2.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem danh sách đơn chờ duyệt | Function | Quản lý trực tiếp | M |  |
| 2.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Duyệt đơn nghỉ | Function | Quản lý trực tiếp | M |  |
| 2.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Từ chối đơn nghỉ kèm lý do | Function | Quản lý trực tiếp | M |  |
| 2.2 | &nbsp;&nbsp;&nbsp;Duyệt khi vắng mặt | Feature |  |  |  |
| 2.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ủy quyền duyệt đơn | Function | Quản lý trực tiếp | S | Hay bị bỏ sót |
| 2.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nhắc người duyệt khi đơn quá hạn | Function | Hệ thống | S |  |
| 2.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chuyển cấp duyệt khi quá hạn kéo dài | Function | Hệ thống | C |  |
| 3 | **Số dư phép và chính sách** | Module |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Cấp phép | Feature |  |  |  |
| 3.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cấp phép năm theo thâm niên | Function | Hệ thống, HR | M |  |
| 3.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chuyển phép tồn sang năm sau | Function | Hệ thống | S |  |
| 3.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Điều chỉnh số dư thủ công kèm lý do | Function | HR | S |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Chính sách | Feature |  |  |  |
| 3.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khai báo loại nghỉ và quy tắc | Function | HR | M |  |
| 3.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ngừng sử dụng loại nghỉ | Function | HR | C |  |
| 3.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khai báo ngày lễ | Function | HR | M |  |
| 4 | **Lịch và khả năng bao phủ** | Module |  |  |  |
| 4.1 | &nbsp;&nbsp;&nbsp;Xem lịch nghỉ nhóm | Function | Quản lý trực tiếp, Nhân viên | S |  |
| 4.2 | &nbsp;&nbsp;&nbsp;Cảnh báo trùng lịch nghỉ hay thiếu người | Function | Hệ thống | C |  |
| 5 | **Báo cáo** | Module |  |  |  |
| 5.1 | &nbsp;&nbsp;&nbsp;Xem báo cáo số dư theo phòng ban | Function | HR | M |  |
| 5.2 | &nbsp;&nbsp;&nbsp;Xuất dữ liệu nghỉ cho bảng lương | Function | HR | S |  |
| 6 | **Truy cập và quản trị** | Module |  |  |  |
| 6.1 | &nbsp;&nbsp;&nbsp;Đăng nhập bằng tài khoản công ty (SSO) | Function | Nhân viên, Quản lý trực tiếp, HR | M |  |
| 6.2 | &nbsp;&nbsp;&nbsp;Đồng bộ cây tổ chức và người duyệt | Function | Hệ thống | M | Nghỉ việc/chuyển phòng giữa kỳ: xử lý đơn đang chờ? [xác nhận] |
| 6.3 | &nbsp;&nbsp;&nbsp;Ghi nhật ký thay đổi dữ liệu nghỉ phép | Function | Hệ thống | M |  |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Đơn nghỉ | 1.1.1, 1.1.3 | 1.3, 2.1.1, 4.1, 5.2 | 1.2.1, 1.2.3, 2.1.2, 2.1.3 | 1.2.2 |
| Số dư phép | 3.1.1 | 1.1.2, 5.1 | 2.1.2, 3.1.2, 3.1.3 | — (miễn: Số dư theo năm, không xoá; điều chỉnh bằng bút toán) |
| Loại nghỉ | 3.2.1 | 1.1.1 | 3.2.1 | 3.2.2 |
| Ngày lễ | 3.2.3 | 3.2.3 | 3.2.3 | 3.2.3 |
| Cây tổ chức và người duyệt | — (miễn: dữ liệu do hệ thống khác sở hữu) | 6.2 | — (miễn: dữ liệu do hệ thống khác sở hữu) | — (miễn: dữ liệu do hệ thống khác sở hữu) |

## 4. Actor × Module (số chức năng)

| Actor | 1. Đăng ký nghỉ | 2. Duyệt đơn | 3. Số dư phép và chính sách | 4. Lịch và khả năng bao phủ | 5. Báo cáo | 6. Truy cập và quản trị |
|---|---|---|---|---|---|---|
| Nhân viên | 5 |  |  | 1 |  | 1 |
| Quản lý trực tiếp | 1 | 4 |  | 1 |  | 1 |
| HR | 1 |  | 5 |  | 2 | 1 |
| Hệ thống | 1 | 2 | 2 | 1 |  | 2 |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **6** · Tính năng: **6** · Chức năng (lá): **26** · Độ sâu: **3** cấp
- Ưu tiên: C: 4, M: 14, S: 8
