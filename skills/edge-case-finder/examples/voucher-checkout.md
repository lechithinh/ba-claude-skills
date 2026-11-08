# Ví dụ: áp voucher khi thanh toán (sàn TMĐT)

> Prompt: *"Tìm edge case cho yêu cầu này."* + dán yêu cầu. Chú thích `[domain]`: lấy từ `domain-ecommerce`.

**Yêu cầu gốc (trích):** *"Khách hàng nhập mã voucher ở bước thanh toán. Nếu hợp lệ, hệ thống trừ số tiền giảm vào tổng đơn hàng."*
**Giả định:** sàn nhiều người bán; voucher có hạn dùng và giới hạn lượt; thanh toán trả trước và COD.

## Danh sách ưu tiên
| # | Nhóm | Tình huống | Hậu quả nếu bỏ sót | Mức | Đề xuất / câu hỏi | Loại |
|---|---|---|---|---|---|---|
| 1 | Đồng thời | Hai khách cùng dùng lượt voucher cuối | Dùng vượt lượt, mất tiền khuyến mãi | Cao | Trừ lượt nguyên tử khi tạo đơn; khách sau nhận thông báo rõ | Yêu cầu |
| 2 | Thời gian | Voucher hết hạn **giữa lúc** khách đang ở trang thanh toán | Khách thấy giá giảm rồi bị tính giá đầy đủ, khiếu nại | Cao | Kiểm tra lại voucher khi bấm "Đặt hàng" [domain]; nếu hết hạn, hiện giá mới và hỏi xác nhận | Yêu cầu |
| 3 | Số/tiền | Tổng đơn thấp hơn mức giảm (voucher 50.000đ, đơn 30.000đ) | Tổng âm hoặc trả tiền ngược cho khách | Cao | Giảm tối đa bằng giá trị đơn, hay yêu cầu đơn tối thiểu? | Yêu cầu |
| 4 | Số/tiền | Đơn nhiều người bán, voucher của sàn: giảm chia cho từng đơn con thế nào | Hoàn tiền một phần sai khi trả hàng | Cao | Quy tắc phân bổ giảm giá về từng sản phẩm [domain] | Yêu cầu |
| 5 | Trạng thái | Đơn bị hủy sau khi dùng voucher | Voucher mất oan hoặc dùng lại được vô hạn | Cao | Hoàn voucher khi hủy không? Còn hạn mới hoàn? | Yêu cầu |
| 6 | Hệ thống ngoài | Cổng thanh toán timeout sau khi đã trừ lượt voucher | Khách mất voucher, đơn không tạo | Trung | Giải phóng lượt khi thanh toán không thành công/hết hạn | Yêu cầu |
| 7 | Lạm dụng | Một người nhiều tài khoản để lấy voucher "khách mới" | Chi phí khuyến mãi vô ích | Trung | Giới hạn theo thiết bị/SĐT/địa chỉ? | Yêu cầu + NFR |
| 8 | Lạm dụng | Dò mã voucher bằng cách thử liên tục | Lộ mã, mất tiền | Trung | Giới hạn số lần nhập sai trong thời gian | NFR |
| 9 | Dữ liệu | Mã nhập chữ hoa/thường, khoảng trắng, dấu | Khách nhập đúng mà báo sai | Trung | Chuẩn hóa mã trước khi so khớp | Test |
| 10 | Kênh | Voucher "chỉ dùng trên app" nhưng khách đặt trên web | Thông báo khó hiểu | Thấp | Thông báo nêu rõ lý do và cách dùng | Test |
| 11 | Quyền hạn | Mã dành riêng cho khách này bị người khác dùng | Dùng sai đối tượng | Trung | Kiểm tra voucher gắn tài khoản | Test |
| 12 | Vận hành | Đơn đặt trước khi đổi cấu hình voucher | Đơn cũ bị tính lại hay giữ nguyên? | Thấp | Giữ nguyên điều kiện tại thời điểm đặt | Yêu cầu |

## Câu hỏi theo stakeholder
**Marketing:** voucher có đơn tối thiểu/giảm tối đa không? Hoàn voucher khi hủy đơn? Cộng dồn nhiều voucher thế nào?
**Vận hành/CSKH:** khi voucher hết hạn giữa chừng, khách thấy gì? CSKH xử lý khiếu nại bằng cách nào?
**Tech lead:** trừ lượt voucher ở bước nào (khi áp dụng hay khi tạo đơn)? Cơ chế chống dùng trùng?

## AC Gherkin cho các mục đầu bảng
```gherkin
Scenario: Hai khách cùng dùng lượt voucher cuối
  Given voucher "SALE10" còn 1 lượt
  When hai khách đặt đơn dùng "SALE10" cùng lúc
  Then chỉ một đơn được giảm giá
  And đơn còn lại nhận thông báo "Voucher đã hết lượt"

Scenario: Voucher hết hạn khi khách đang ở bước thanh toán
  Given khách đã áp voucher "SALE10" hợp lệ lúc 23:59:30
  And voucher hết hạn lúc 00:00:00
  When khách bấm "Đặt hàng" lúc 00:00:10
  Then hệ thống không tạo đơn
  And hiển thị giá mới không có giảm giá để khách xác nhận lại

Scenario: Mức giảm lớn hơn tổng đơn
  Given voucher giảm 50.000đ và đơn hàng 30.000đ
  When khách áp voucher
  Then tổng thanh toán không âm
  And áp dụng quy tắc [giảm tối đa bằng giá trị đơn / yêu cầu đơn tối thiểu: xác nhận]
```

## Đã quét nhưng không áp dụng
Tiếng Việt/ký tự đặc biệt (mã voucher chỉ gồm chữ và số); dữ liệu cũ (tính năng mới ra mắt).
