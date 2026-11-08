# Sàn thương mại điện tử: từ giỏ hàng đến đổi trả

**Trong phạm vi:** Giỏ hàng và checkout; Voucher; Thanh toán; Đơn hàng nhiều người bán; Giao vận và COD; Đổi trả và hoàn tiền
**Ngoài phạm vi:** Danh mục sản phẩm; Đánh giá; Quảng cáo; Đối soát chi trả người bán (làm ở phase 2)
**Actor:** Người mua, Người bán, Marketing, Kế toán, CSKH, Hệ thống

**Giả định:**
- Mô hình sàn nhiều người bán, có COD
- Capability map lấy từ domain-ecommerce; giá trị cụ thể (thời hạn đổi trả, ma trận voucher) cần xác nhận

## 1. Bảng phân cấp

| ID | Chức năng | Loại | Actor | Ưu tiên | Ghi chú |
|---|---|---|---|---|---|
| 1 | **Giỏ hàng và checkout** | Module |  |  |  |
| 1.1 | &nbsp;&nbsp;&nbsp;Giỏ hàng | Feature |  |  |  |
| 1.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Thêm sản phẩm vào giỏ | Function | Người mua | M |  |
| 1.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cập nhật số lượng trong giỏ | Function | Người mua | M |  |
| 1.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xóa sản phẩm khỏi giỏ | Function | Người mua | M |  |
| 1.1.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem giỏ hàng | Function | Người mua | M |  |
| 1.2 | &nbsp;&nbsp;&nbsp;Đặt hàng | Feature |  |  |  |
| 1.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chọn địa chỉ giao hàng | Function | Người mua | M |  |
| 1.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tính phí vận chuyển theo địa chỉ và trọng lượng | Function | Hệ thống | M |  |
| 1.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kiểm tra lại tồn kho, giá, voucher khi đặt hàng | Function | Hệ thống | M | [domain] Giá/tồn kho có thể đổi giữa giỏ và đặt hàng |
| 1.2.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo đơn hàng | Function | Người mua | M |  |
| 2 | **Khuyến mãi và voucher** | Module |  |  |  |
| 2.1 | &nbsp;&nbsp;&nbsp;Chương trình voucher | Feature |  |  |  |
| 2.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo chương trình voucher | Function | Marketing | M |  |
| 2.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cấu hình điều kiện và ma trận cộng dồn | Function | Marketing | M | [domain] Voucher sàn + shop + vận chuyển cộng dồn thế nào |
| 2.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dừng chương trình voucher | Function | Marketing | S |  |
| 2.1.4 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem hiệu quả chương trình voucher | Function | Marketing | C |  |
| 2.2 | &nbsp;&nbsp;&nbsp;Áp dụng voucher | Feature |  |  |  |
| 2.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Áp dụng voucher vào đơn | Function | Người mua | M |  |
| 2.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Phân bổ giảm giá về từng sản phẩm | Function | Hệ thống | M | [domain] Cần cho hoàn tiền một phần |
| 2.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hoàn lại voucher khi hủy đơn | Function | Hệ thống | S | Có hoàn hay không: chờ quyết định [xác nhận] |
| 3 | **Thanh toán** | Module |  |  |  |
| 3.1 | &nbsp;&nbsp;&nbsp;Tạo yêu cầu thanh toán | Function | Hệ thống | M |  |
| 3.2 | &nbsp;&nbsp;&nbsp;Nhận kết quả thanh toán từ cổng | Function | Hệ thống | M | [domain] Callback là nguồn sự thật; xử lý callback mất |
| 3.3 | &nbsp;&nbsp;&nbsp;Hủy đơn hết hạn thanh toán | Function | Hệ thống | M | [domain] Giải phóng tồn kho |
| 3.4 | &nbsp;&nbsp;&nbsp;Đối soát thanh toán với cổng | Function | Kế toán | M |  |
| 4 | **Quản lý đơn hàng** | Module |  |  |  |
| 4.1 | &nbsp;&nbsp;&nbsp;Đơn của người mua | Feature |  |  |  |
| 4.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem đơn hàng của tôi | Function | Người mua | M |  |
| 4.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy đơn khi chưa xử lý | Function | Người mua | M |  |
| 4.2 | &nbsp;&nbsp;&nbsp;Đơn của người bán | Feature |  |  |  |
| 4.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xác nhận đơn | Function | Người bán | M |  |
| 4.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tách đơn theo người bán | Function | Hệ thống | M | [domain] Đơn cha và đơn con mỗi seller |
| 4.2.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cập nhật trạng thái đơn theo vận đơn | Function | Hệ thống | M |  |
| 5 | **Giao vận và COD** | Module |  |  |  |
| 5.1 | &nbsp;&nbsp;&nbsp;Tạo vận đơn với hãng vận chuyển | Function | Người bán | M |  |
| 5.2 | &nbsp;&nbsp;&nbsp;Nhận trạng thái giao hàng từ hãng | Function | Hệ thống | M |  |
| 5.3 | &nbsp;&nbsp;&nbsp;Theo dõi vận đơn | Function | Người mua | S |  |
| 5.4 | &nbsp;&nbsp;&nbsp;Hoàn hàng về người bán sau giao thất bại | Function | Hệ thống | M |  |
| 5.5 | &nbsp;&nbsp;&nbsp;Đối soát tiền COD với hãng vận chuyển | Function | Kế toán | M |  |
| 6 | **Đổi trả và hoàn tiền** | Module |  |  |  |
| 6.1 | &nbsp;&nbsp;&nbsp;Yêu cầu trả hàng | Feature |  |  |  |
| 6.1.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tạo yêu cầu trả hàng | Function | Người mua | M |  |
| 6.1.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem trạng thái yêu cầu trả hàng | Function | Người mua, Người bán | M |  |
| 6.1.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hủy yêu cầu trả hàng | Function | Người mua | C |  |
| 6.2 | &nbsp;&nbsp;&nbsp;Xử lý trả hàng | Feature |  |  |  |
| 6.2.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Duyệt yêu cầu trả hàng | Function | Người bán, CSKH | M |  |
| 6.2.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kiểm hàng trả về | Function | Người bán | M |  |
| 6.3 | &nbsp;&nbsp;&nbsp;Hoàn tiền | Feature |  |  |  |
| 6.3.1 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tính số tiền hoàn theo phân bổ voucher | Function | Hệ thống | M |  |
| 6.3.2 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hoàn tiền về phương thức thanh toán gốc | Function | Hệ thống | M |  |
| 6.3.3 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xem trạng thái hoàn tiền | Function | Người mua, Kế toán | M |  |
| 7 | **Xuyên suốt và quản trị** | Module |  |  |  |
| 7.1 | &nbsp;&nbsp;&nbsp;Đăng nhập theo vai trò | Function | Người mua, Người bán, Marketing, Kế toán, CSKH | M |  |
| 7.2 | &nbsp;&nbsp;&nbsp;Gửi thông báo trạng thái đơn | Function | Hệ thống | M |  |
| 7.3 | &nbsp;&nbsp;&nbsp;Ghi nhật ký thao tác nhạy cảm | Function | Hệ thống | M |  |
| 7.4 | &nbsp;&nbsp;&nbsp;Xem báo cáo đơn hủy và đơn trả | Function | Kế toán, Marketing | S |  |
| 7.5 | &nbsp;&nbsp;&nbsp;Cấu hình thời hạn đổi trả và chính sách | Function | Marketing | S |  |
| 7.6 | &nbsp;&nbsp;&nbsp;Điều chỉnh hóa đơn điện tử khi hoàn tiền | Function | Kế toán | S | [domain] Hóa đơn đã xuất thì xử lý điều chỉnh |

## 2. Ma trận CRUD theo đối tượng nghiệp vụ

| Đối tượng | Create | Read | Update | Delete / Hủy / Lưu trữ |
|---|---|---|---|---|
| Giỏ hàng | 1.1.1 | 1.1.4 | 1.1.1, 1.1.2 | 1.1.3 |
| Đơn hàng | 1.2.4, 4.2.2 | 4.1.1 | 4.2.1, 4.2.3 | 4.1.2 |
| Voucher | 2.1.1 | 2.1.4 | 2.1.2 | 2.1.3 |
| Thanh toán | 3.1 | 3.4 | 3.2 | — (miễn: Giao dịch tài chính không xóa) |
| Vận đơn | 5.1 | 5.3 | 5.2 | — (miễn: Giữ lịch sử giao hàng) |
| Yêu cầu trả hàng | 6.1.1 | 6.1.2 | 6.2.1, 6.2.2 | 6.1.3 |
| Hoàn tiền | 6.3.1 | 6.3.3 | 6.3.2 | — (miễn: Giao dịch tài chính không xóa) |

## 4. Actor × Module (số chức năng)

| Actor | 1. Giỏ hàng và checkout | 2. Khuyến mãi và voucher | 3. Thanh toán | 4. Quản lý đơn hàng | 5. Giao vận và COD | 6. Đổi trả và hoàn tiền | 7. Xuyên suốt và quản trị |
|---|---|---|---|---|---|---|---|
| Người mua | 6 | 1 |  | 2 | 1 | 4 | 1 |
| Người bán |  |  |  | 1 | 1 | 3 | 1 |
| Marketing |  | 4 |  |  |  |  | 3 |
| Kế toán |  |  | 1 |  | 1 | 1 | 3 |
| CSKH |  |  |  |  |  | 1 | 1 |
| Hệ thống | 2 | 2 | 3 | 2 | 2 | 2 | 2 |

_Dùng làm điểm xuất phát cho ma trận vai trò – quyền._

## 5. Thống kê

- Module: **7** · Tính năng: **9** · Chức năng (lá): **43** · Độ sâu: **3** cấp
- Ưu tiên: C: 2, M: 35, S: 6
