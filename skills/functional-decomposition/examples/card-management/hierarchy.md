# Tự phục vụ khóa/mở khóa thẻ và hạn mức online (mobile banking)

**Trong phạm vi:** Khóa tạm, báo mất, mở khóa thẻ trên app; Hạn mức chi tiêu online; Thông báo cho chủ thẻ; Đối soát trạng thái với CMS
**Ngoài phạm vi:** Phát hành và kích hoạt thẻ; Khiếu nại giao dịch (tra soát); Thẻ phụ (chờ xác nhận)
**Actor:** Chủ thẻ, Nhân viên hotline, Chuyên viên Fraud, Vận hành thẻ, Hệ thống

**Giả định:**
- Chức năng sinh từ biên bản họp 2026-11-05 và capability 'Cards' của domain-banking
- Khóa/mở khóa thực hiện qua Card Management System (CMS), CMS đôi lúc phản hồi chậm
- Hạn mức mặc định 20 triệu/ngày chưa chốt [xác nhận]
- Các chức năng đánh dấu 'derived' do domain pack gợi ý, không có trong biên bản; cần stakeholder xác nhận

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Yêu cầu | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | **Khóa và mở khóa thẻ** | Module |  |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Khóa thẻ | Feature |  |  |  |  |
| 1.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khóa tạm thẻ trên app | Function | Chủ thẻ | M | FR-01, FR-02, FR-07 |  |
| 1.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Báo mất thẻ | Function | Chủ thẻ | M | FR-02 | Đóng thẻ vĩnh viễn, phải phát hành thẻ mới |
| 1.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Khóa thẻ qua hotline | Function | Nhân viên hotline | S | FR-01 | Đồng bộ trạng thái với app |
| 1.2 | &nbsp;&nbsp;&nbsp;Mở khóa thẻ | Feature |  |  |  |  |
| 1.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mở khóa thẻ khóa tạm bằng xác thực | Function | Chủ thẻ | M | FR-03, FR-07 | Xung đột chờ quyết định: mở ngay hay chờ 24h [xác nhận Q1] |
| 1.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chặn mở khóa thẻ bị gắn cờ gian lận | Function | Hệ thống | M | FR-04 |  |
| 1.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mở khóa thẻ bị gắn cờ sau khi xác minh | Function | Chuyên viên Fraud | S | FR-04 |  |
| 1.3 | &nbsp;&nbsp;&nbsp;Đồng bộ với CMS | Feature |  |  |  |  |
| 1.3.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Gọi CMS đổi trạng thái thẻ | Function | Hệ thống | M | FR-07 |  |
| 1.3.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Thử lại khi CMS phản hồi chậm | Function | Hệ thống | M |  | [domain] Tránh khách tưởng đã khóa nhưng thẻ vẫn quẹt được |
| 1.3.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đối soát trạng thái thẻ giữa app và CMS | Function | Vận hành thẻ | M |  | [domain] Giải quyết giao dịch pending/timeout |
| 2 | **Hạn mức chi tiêu online** | Module |  |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Hạn mức của chủ thẻ | Feature |  |  |  |  |
| 2.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đặt hạn mức online theo ngày | Function | Chủ thẻ | M | FR-05 |  |
| 2.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem hạn mức hiện tại | Function | Chủ thẻ | M | FR-05 |  |
| 2.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Đặt lại hạn mức về mặc định | Function | Chủ thẻ | C | FR-05 |  |
| 2.2 | &nbsp;&nbsp;&nbsp;Kiểm soát rủi ro khi đổi hạn mức | Feature |  |  |  |  |
| 2.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yêu cầu xác thực mạnh khi tăng hạn mức | Function | Hệ thống | S |  | [domain] Chống kẻ gian nâng hạn mức sau khi chiếm app |
| 2.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Áp dụng hạn mức tối đa của ngân hàng | Function | Hệ thống | M |  |  |
| 3 | **Thông báo cho chủ thẻ** | Module |  |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Gửi thông báo khi trạng thái khóa thẻ đổi | Function | Hệ thống | M | FR-06 |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Gửi lại thông báo khi chưa nhận được | Function | Hệ thống | S |  | Khiếu nại 'không thấy thông báo' từ biên bản |
| 3.3 | &nbsp;&nbsp;&nbsp;Xem lịch sử thông báo về thẻ | Function | Chủ thẻ | C |  |  |
| 4 | **Fraud và vận hành** | Module |  |  |  |  |
| 4.1 | &nbsp;&nbsp;&nbsp;Xem danh sách thẻ bị gắn cờ | Function | Chuyên viên Fraud | S |  |  |
| 4.2 | &nbsp;&nbsp;&nbsp;Gắn cờ gian lận cho thẻ | Function | Chuyên viên Fraud | M |  |  |
| 4.3 | &nbsp;&nbsp;&nbsp;Gỡ cờ gian lận cho thẻ | Function | Chuyên viên Fraud | S |  |  |
| 5 | **Truy cập và kiểm soát** | Module |  |  |  |  |
| 5.1 | &nbsp;&nbsp;&nbsp;Xác thực chủ thẻ theo mức rủi ro | Function | Chủ thẻ | M |  | OTP/sinh trắc theo ngưỡng; chờ Compliance [xác nhận Q7] |
| 5.2 | &nbsp;&nbsp;&nbsp;Phân quyền nhân viên theo vai trò | Function | Vận hành thẻ | M |  |  |
| 5.3 | &nbsp;&nbsp;&nbsp;Ghi nhật ký thay đổi thẻ và hạn mức | Function | Hệ thống | M |  |  |
| 5.4 | &nbsp;&nbsp;&nbsp;Xem báo cáo thẻ bị khóa theo ngày | Function | Vận hành thẻ | C |  |  |
| 5.5 | &nbsp;&nbsp;&nbsp;Cấu hình hạn mức mặc định và thời gian chờ CMS | Function | Vận hành thẻ | M |  |  |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Thẻ | — (miễn: dữ liệu do hệ thống khác sở hữu) | 1.1.1, 1.3.3, 4.1 | — (miễn: dữ liệu do hệ thống khác sở hữu) | — (miễn: dữ liệu do hệ thống khác sở hữu) |
| Hạn mức online | 2.1.1 | 2.1.2, 2.2.2 | 2.1.1, 2.1.3, 5.5 | — (miễn: Hạn mức không xóa; 'đặt lại mặc định' (2.1.3) thay cho xóa) |
| Thông báo | 3.1, 3.2 | 3.3 | — (miễn: bất biến) | — (miễn: Bản ghi gửi thông báo không sửa/xóa, phục vụ tra cứu) |

## 3. Truy vết yêu cầu → chức năng

| Yêu cầu | Nội dung | Chức năng phủ |
|---|---|---|
| FR-01 | Khách khóa được thẻ ngay trên app | 1.1.1, 1.1.3 |
| FR-02 | Hai loại: Khóa tạm (mở lại được) và Báo mất (đóng vĩnh viễn) | 1.1.1, 1.1.2 |
| FR-03 | Khách mở khóa được thẻ ở trạng thái khóa tạm | 1.2.1 |
| FR-04 | Thẻ bị flag gian lận thì khách không tự mở khóa được | 1.2.2, 1.2.3 |
| FR-05 | Khách tự đặt hạn mức chi tiêu online theo ngày | 2.1.1, 2.1.2, 2.1.3 |
| FR-06 | Khách nhận thông báo khi khóa xong | 3.1 |
| FR-07 | Hệ thống gọi CMS để khóa/mở khóa | 1.1.1, 1.2.1, 1.3.1 |

## 4. Actor × Module (số chức năng)

| Actor | 1. Khóa và mở khóa thẻ | 2. Hạn mức chi tiêu online | 3. Thông báo cho chủ thẻ | 4. Fraud và vận hành | 5. Truy cập và kiểm soát |
|---|---|---|---|---|---|
| Chủ thẻ | 3 | 3 | 1 |  | 1 |
| Nhân viên hotline | 1 |  |  |  |  |
| Chuyên viên Fraud | 1 |  |  | 3 |  |
| Vận hành thẻ | 1 |  |  |  | 3 |
| Hệ thống | 3 | 2 | 2 |  | 1 |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **5** · Tính năng: **5** · Chức năng (lá): **25** · Độ sâu: **3** cấp
- Ưu tiên: C: 3, M: 16, S: 6
