# Đặt lịch khám phòng khám — BẢN NHÁP CÓ LỖI (AS-IS để soát)

**Trong phạm vi:** Đặt và hủy lịch khám; Nhắc lịch; Lịch làm việc bác sĩ; Báo cáo no-show
**Ngoài phạm vi:** Thanh toán đặt cọc (chờ Q1); Zalo (phase 2); Hồ sơ bệnh án
**Actor:** Bệnh nhân, Lễ tân, Bác sĩ, Quản lý phòng khám, Hệ thống

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Yêu cầu | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | **Quản lý lịch hẹn** | Module |  |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Quản lý lịch hẹn | Function | Bệnh nhân |  | FR-01, FR-03 |  |
| 1.2 | &nbsp;&nbsp;&nbsp;Đặt lịch | Function | Bệnh nhân, Lễ tân |  | FR-01, FR-04 |  |
| 1.3 | &nbsp;&nbsp;&nbsp;Màn hình lịch trong ngày của lễ tân | Function |  |  | FR-05 |  |
| 2 | **Thông báo** | Module |  |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Nhắc lịch | Feature |  |  |  |  |
| 2.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Gửi và nhắc lịch qua SMS | Function | Hệ thống |  | FR-02 |  |
| 3 | **Lịch bác sĩ** | Module |  |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Khóa lịch nghỉ phép | Function | Bác sĩ |  | FR-06 |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Đặt lịch hẹn | Function | Bệnh nhân |  | FR-01 |  |
| 3.3 | &nbsp;&nbsp;&nbsp;Hệ thống | Feature |  |  |  |  |
| 3.3.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cấu hình | Feature |  |  |  |  |
| 3.3.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khai báo giờ làm việc | Function | Quản lý phòng khám |  |  |  |
| 4.1.1 | &nbsp;&nbsp;&nbsp;Báo cáo no-show | Function | Quản lý phòng khám |  | FR-07 |  |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Lịch hẹn | 1.1, 1.2, 3.2 | 1.1, 1.3 | 1.1 | 1.1 |
| Khung giờ | 3.3.1.1 | 1.2 | 3.1 | ❌ |
| Lịch nghỉ bác sĩ | 3.1 | ❌ | ❌ | ❌ |

## 3. Truy vết yêu cầu → chức năng

| Yêu cầu | Nội dung | Chức năng phủ |
|---|---|---|
| FR-01 | Bệnh nhân tự đặt lịch online, chọn bác sĩ và khung giờ | 1.1, 1.2, 3.2 |
| FR-02 | Hệ thống nhắc lịch trước 1 ngày | 2.1.1 |
| FR-03 | Bệnh nhân hủy lịch online (trước giờ hẹn ít nhất 2 giờ) | 1.1 |
| FR-04 | Lễ tân đặt lịch hộ bệnh nhân | 1.2 |
| FR-05 | Lễ tân xem lịch trong ngày theo từng bác sĩ | 1.3 |
| FR-06 | Bác sĩ tự khóa lịch khi nghỉ phép | 3.1 |
| FR-07 | Báo cáo tỷ lệ no-show theo bác sĩ hàng tháng | 4.1.1 |
| FR-08 | Ngăn hai lịch hẹn trên cùng một khung giờ | ❌ chưa phủ |

## 4. Actor × Module (số chức năng)

| Actor | 1. Quản lý lịch hẹn | 2. Thông báo | 3. Lịch bác sĩ |
|---|---|---|---|
| Bệnh nhân | 2 |  | 1 |
| Lễ tân | 1 |  |  |
| Bác sĩ |  |  | 1 |
| Quản lý phòng khám |  |  | 2 |
| Hệ thống |  | 1 |  |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **3** · Tính năng: **3** · Chức năng (lá): **8** · Độ sâu: **4** cấp
- Ưu tiên: -: 8
