# Đặc tả màn hình / Screen Specification

## Vì sao tốn công mà vẫn quan trọng
Dev nhìn ảnh Figma thấy *giao diện*, không thấy *quy tắc*: trường nào bắt buộc, nhập sai thì báo gì, nút nào bật khi nào, danh sách rỗng thì hiện gì. Những thứ đó nằm trong đặc tả màn hình. Thiếu nó, dev tự đoán, tester tự đoán, rồi UAT mới lộ ra.

## Một đặc tả tốt gồm
1. **Bối cảnh**: màn hình phục vụ ai, đi vào từ đâu.
2. **Bảng trường** đầy đủ (loại, bắt buộc, định dạng, mặc định, nguồn, validation, thông báo lỗi).
3. **Hành vi nút**, gồm cả đường thất bại.
4. **Mọi trạng thái**, không chỉ trạng thái đẹp: tải, rỗng, lỗi, chỉ-đọc.
5. **Quy tắc tương tác** giữa các trường.
6. **Phân biệt** điều đã chốt với điều còn là giả định.

## Lỗi thường gặp của BA
- Chỉ mô tả trạng thái "có dữ liệu", quên trạng thái rỗng và lỗi.
- Viết "hiển thị thông báo lỗi" mà không nói nội dung.
- Trộn **giao diện** (màu, vị trí) với **hành vi** (validation). Giao diện thuộc về thiết kế.
- Bịa độ dài, định dạng vì ảnh không ghi.
- Quên checkbox đồng ý/điều khoản: bắt buộc hay không?

## Mẹo
- Đọc từ trên xuống dưới như người dùng, mỗi control tự hỏi: *bỏ trống thì sao? nhập sai thì sao? mất mạng thì sao?*
- Đưa đặc tả cho tester xem **trước** khi dev bắt đầu: câu hỏi của họ là danh sách thiếu sót miễn phí.

## Thực hành
Chụp một màn hình ứng dụng bạn thường dùng, đưa cho Claude: *"Viết đặc tả màn hình cho ảnh này."* So sánh những gì nó đánh dấu `[xác nhận]` với những điều bạn cũng chưa chắc.
