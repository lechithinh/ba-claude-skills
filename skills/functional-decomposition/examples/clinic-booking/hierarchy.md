# Hệ thống đặt lịch khám phòng khám

**Trong phạm vi:** Đặt và hủy lịch khám; Nhắc lịch; Lịch làm việc bác sĩ; Báo cáo no-show
**Ngoài phạm vi:** Thanh toán đặt cọc (chờ Q1); Zalo (phase 2); Hồ sơ bệnh án
**Actor:** Bệnh nhân, Lễ tân, Bác sĩ, Quản lý phòng khám, Hệ thống

**Giả định:**
- Một cơ sở, mỗi bác sĩ có khung giờ cố định theo ca
- Nhắc lịch qua SMS ở phase 1; Zalo phase 2
- Đặt cọc online chờ quyết định ban giám đốc (Q1), chưa vào phạm vi

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Yêu cầu | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | **Đặt và quản lý lịch hẹn** | Module |  |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Đặt lịch khám | Feature |  |  |  |  |
| 1.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tìm khung giờ trống theo bác sĩ và ngày | Function | Bệnh nhân, Lễ tân | M | FR-01, FR-04 |  |
| 1.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo lịch hẹn tự phục vụ | Function | Bệnh nhân | M | FR-01 |  |
| 1.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo lịch hẹn hộ bệnh nhân | Function | Lễ tân | M | FR-04 |  |
| 1.1.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chặn đặt trùng khung giờ | Function | Hệ thống | M | FR-08 |  |
| 1.2 | &nbsp;&nbsp;&nbsp;Hủy lịch hẹn | Feature |  |  |  |  |
| 1.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy lịch hẹn online trước giờ hẹn 2 giờ | Function | Bệnh nhân | M | FR-03 |  |
| 1.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy lịch hẹn hộ bệnh nhân | Function | Lễ tân | S |  |  |
| 1.3 | &nbsp;&nbsp;&nbsp;Theo dõi lịch hẹn | Feature |  |  |  |  |
| 1.3.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem lịch hẹn sắp tới của tôi | Function | Bệnh nhân | S |  |  |
| 1.3.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem lịch trong ngày theo bác sĩ | Function | Lễ tân | M | FR-05 |  |
| 1.3.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ghi nhận bệnh nhân đến hoặc vắng mặt | Function | Lễ tân | M | FR-07 |  |
| 2 | **Lịch làm việc bác sĩ** | Module |  |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Khung giờ khám | Feature |  |  |  |  |
| 2.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo khung giờ theo ca làm việc | Function | Quản lý phòng khám | M |  |  |
| 2.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Điều chỉnh khung giờ | Function | Quản lý phòng khám | S |  |  |
| 2.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đóng khung giờ không nhận lịch | Function | Quản lý phòng khám, Bác sĩ | M | FR-06 |  |
| 2.2 | &nbsp;&nbsp;&nbsp;Nghỉ phép của bác sĩ | Feature |  |  |  |  |
| 2.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khai báo thời gian nghỉ | Function | Bác sĩ | M | FR-06 |  |
| 2.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem lịch nghỉ | Function | Bác sĩ, Lễ tân | S | FR-06 |  |
| 2.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy khai báo nghỉ | Function | Bác sĩ | S | FR-06 |  |
| 2.2.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cảnh báo lịch hẹn trùng thời gian nghỉ | Function | Hệ thống | M |  | Câu hỏi mở: ai liên hệ bệnh nhân [Q] |
| 3 | **Thông báo** | Module |  |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Gửi xác nhận đặt lịch | Function | Hệ thống | M |  |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Gửi SMS nhắc lịch trước một ngày | Function | Hệ thống | M | FR-02 |  |
| 3.3 | &nbsp;&nbsp;&nbsp;Gửi thông báo hủy lịch | Function | Hệ thống | S |  |  |
| 4 | **Báo cáo** | Module |  |  |  |  |
| 4.1 | &nbsp;&nbsp;&nbsp;Xem tỷ lệ no-show theo bác sĩ theo tháng | Function | Quản lý phòng khám | M | FR-07 |  |
| 4.2 | &nbsp;&nbsp;&nbsp;Xuất báo cáo no-show ra Excel | Function | Quản lý phòng khám | C |  |  |
| 5 | **Truy cập và quản trị** | Module |  |  |  |  |
| 5.1 | &nbsp;&nbsp;&nbsp;Hồ sơ bệnh nhân | Feature |  |  |  |  |
| 5.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đăng ký tài khoản bệnh nhân bằng OTP | Function | Bệnh nhân | M |  |  |
| 5.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cập nhật hồ sơ của tôi | Function | Bệnh nhân | S |  |  |
| 5.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem hồ sơ của tôi | Function | Bệnh nhân | S |  |  |
| 5.2 | &nbsp;&nbsp;&nbsp;Nhân viên và bác sĩ | Feature |  |  |  |  |
| 5.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đăng nhập nhân viên theo vai trò | Function | Lễ tân, Bác sĩ, Quản lý phòng khám | M |  |  |
| 5.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Thêm bác sĩ | Function | Quản lý phòng khám | M |  |  |
| 5.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cập nhật thông tin bác sĩ | Function | Quản lý phòng khám | S |  |  |
| 5.2.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem danh sách bác sĩ | Function | Bệnh nhân, Lễ tân, Quản lý phòng khám | M |  |  |
| 5.2.5 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ngừng hoạt động bác sĩ | Function | Quản lý phòng khám | C |  |  |
| 5.3 | &nbsp;&nbsp;&nbsp;Ghi nhật ký thao tác trên lịch hẹn | Function | Hệ thống | S |  |  |
| 5.4 | &nbsp;&nbsp;&nbsp;Khai báo danh mục chuyên khoa và tham số hệ thống | Function | Quản lý phòng khám | C |  |  |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Lịch hẹn | 1.1.2, 1.1.3 | 1.3.1, 1.3.2 | 1.3.3 | 1.2.1, 1.2.2 |
| Khung giờ | 2.1.1 | 1.1.1 | 2.1.2 | 2.1.3 |
| Lịch nghỉ bác sĩ | 2.2.1 | 2.2.2 | — (miễn: bất biến) | 2.2.3 |
| Hồ sơ bệnh nhân | 5.1.1 | 5.1.3 | 5.1.2 | — (miễn: Lưu theo yêu cầu quản lý hồ sơ) |
| Bác sĩ | 5.2.2 | 5.2.4 | 5.2.3 | 5.2.5 |

## 3. Truy vết yêu cầu → chức năng

| Yêu cầu | Nội dung | Chức năng phủ |
|---|---|---|
| FR-01 | Bệnh nhân tự đặt lịch online, chọn bác sĩ và khung giờ | 1.1.1, 1.1.2 |
| FR-02 | Hệ thống nhắc lịch trước 1 ngày | 3.2 |
| FR-03 | Bệnh nhân hủy lịch online (trước giờ hẹn ít nhất 2 giờ) | 1.2.1 |
| FR-04 | Lễ tân đặt lịch hộ bệnh nhân | 1.1.1, 1.1.3 |
| FR-05 | Lễ tân xem lịch trong ngày theo từng bác sĩ | 1.3.2 |
| FR-06 | Bác sĩ tự khóa lịch khi nghỉ phép | 2.1.3, 2.2.1, 2.2.2, 2.2.3 |
| FR-07 | Báo cáo tỷ lệ no-show theo bác sĩ hàng tháng | 1.3.3, 4.1 |
| FR-08 | Ngăn hai lịch hẹn trên cùng một khung giờ | 1.1.4 |

## 4. Actor × Module (số chức năng)

| Actor | 1. Đặt và quản lý lịch hẹn | 2. Lịch làm việc bác sĩ | 3. Thông báo | 4. Báo cáo | 5. Truy cập và quản trị |
|---|---|---|---|---|---|
| Bệnh nhân | 4 |  |  |  | 4 |
| Lễ tân | 5 | 1 |  |  | 2 |
| Bác sĩ |  | 4 |  |  | 1 |
| Quản lý phòng khám |  | 3 |  | 2 | 6 |
| Hệ thống | 1 | 1 | 3 |  | 1 |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **5** · Tính năng: **7** · Chức năng (lá): **31** · Độ sâu: **3** cấp
- Ưu tiên: C: 3, M: 18, S: 10
