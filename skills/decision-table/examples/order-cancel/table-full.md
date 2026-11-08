| Trạng thái đơn | Hình thức thanh toán | Người hủy | Kết quả | Rule |
|---|---|---|---|---|
| Chờ thanh toán | Trả trước | Khách | Hủy đơn và giải phóng tồn kho | R1 |
| Chờ thanh toán | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho | R1 |
| Chờ thanh toán | COD | Khách | Tổ hợp không hợp lệ, hệ thống không cho xảy ra | R0 |
| Chờ thanh toán | COD | Người bán | Tổ hợp không hợp lệ, hệ thống không cho xảy ra | R0 |
| Đã xác nhận | Trả trước | Khách | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc | R2 |
| Đã xác nhận | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc | R2 |
| Đã xác nhận | COD | Khách | Hủy đơn và giải phóng tồn kho | R3 |
| Đã xác nhận | COD | Người bán | Hủy đơn và giải phóng tồn kho | R3 |
| Đang xử lý | Trả trước | Khách | Gửi yêu cầu hủy chờ người bán duyệt | R4 |
| Đang xử lý | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc | R5 |
| Đang xử lý | COD | Khách | Gửi yêu cầu hủy chờ người bán duyệt | R4 |
| Đang xử lý | COD | Người bán | Hủy đơn và giải phóng tồn kho | R6 |
| Đang giao | Trả trước | Khách | Từ chối hủy, hướng dẫn quy trình trả hàng | R7 |
| Đang giao | Trả trước | Người bán | Từ chối hủy, hướng dẫn quy trình trả hàng | R7 |
| Đang giao | COD | Khách | Từ chối hủy, hướng dẫn quy trình trả hàng | R7 |
| Đang giao | COD | Người bán | Từ chối hủy, hướng dẫn quy trình trả hàng | R7 |
