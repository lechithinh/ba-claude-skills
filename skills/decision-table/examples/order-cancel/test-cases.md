| # | Trạng thái đơn | Hình thức thanh toán | Người hủy | Kết quả mong đợi |
|---|---|---|---|---|
| TC01 | Chờ thanh toán | Trả trước | Khách | Hủy đơn và giải phóng tồn kho |
| TC02 | Chờ thanh toán | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho |
| TC03 | Chờ thanh toán | COD | Khách | Tổ hợp không hợp lệ, hệ thống không cho xảy ra |
| TC04 | Chờ thanh toán | COD | Người bán | Tổ hợp không hợp lệ, hệ thống không cho xảy ra |
| TC05 | Đã xác nhận | Trả trước | Khách | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc |
| TC06 | Đã xác nhận | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc |
| TC07 | Đã xác nhận | COD | Khách | Hủy đơn và giải phóng tồn kho |
| TC08 | Đã xác nhận | COD | Người bán | Hủy đơn và giải phóng tồn kho |
| TC09 | Đang xử lý | Trả trước | Khách | Gửi yêu cầu hủy chờ người bán duyệt |
| TC10 | Đang xử lý | Trả trước | Người bán | Hủy đơn và giải phóng tồn kho, Hoàn tiền về phương thức gốc |
| TC11 | Đang xử lý | COD | Khách | Gửi yêu cầu hủy chờ người bán duyệt |
| TC12 | Đang xử lý | COD | Người bán | Hủy đơn và giải phóng tồn kho |
| TC13 | Đang giao | Trả trước | Khách | Từ chối hủy, hướng dẫn quy trình trả hàng |
| TC14 | Đang giao | Trả trước | Người bán | Từ chối hủy, hướng dẫn quy trình trả hàng |
| TC15 | Đang giao | COD | Khách | Từ chối hủy, hướng dẫn quy trình trả hàng |
| TC16 | Đang giao | COD | Người bán | Từ chối hủy, hướng dẫn quy trình trả hàng |
