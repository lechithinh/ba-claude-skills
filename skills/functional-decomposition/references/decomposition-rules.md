# Quy tắc phân rã, checklist nghiệm thu, rủi ro khi dùng AI

## Quy tắc nền
1. **MECE**: các nhánh con không chồng lấn và cộng lại đủ nghĩa của nhánh cha.
2. **Phân rã theo năng lực**, không theo màn hình, phòng ban hay bảng dữ liệu.
3. **Lá = chức năng nguyên tử**: một actor chính, một mục tiêu, một kết quả quan sát được (`levels-and-depth.md`).
4. **Tên chức năng là Động từ + Danh từ**; không dùng "Quản lý", "Xử lý" làm tên lá (`naming-guide.md`).
5. **Cây là cấu trúc, không phải thứ tự.** Trình tự các bước thuộc về sơ đồ quy trình (`decomposition-vs-others.md`).
6. **Mỗi nút 2–9 con.** Một con duy nhất nghĩa là thừa một cấp; hơn chín nghĩa là chưa gom nhóm.
7. **ID ổn định**: `1`, `1.1`, `1.1.1`; không đánh lại số khi sửa cây (`traceability.md`).
8. **Mọi chức năng có nguồn**: yêu cầu, hoặc đánh dấu `derived` kèm lý do.

Lỗi cụ thể kèm cách sửa: `mistakes-catalog.md`.

## Checklist 8 điểm trước khi đưa vào tài liệu
1. **Phạm vi** – có `scope.in/out`, giả định, danh sách actor.
2. **MECE** – không chồng lấn (kể cả hai tên gần giống ở hai nhánh), không bỏ trống.
3. **Mức chi tiết** – mọi lá qua "hàm test nguyên tử"; độ sâu giữa các nhánh không lệch nhiều.
4. **Đặt tên** – mọi lá bắt đầu bằng động từ cụ thể.
5. **CRUD và vòng đời** – mọi đối tượng có đủ Tạo, Xem, Sửa, Hủy/Lưu trữ, hoặc có miễn trừ ghi lý do.
6. **Xuyên suốt** – xác thực/phân quyền, thông báo, nhật ký, báo cáo, cấu hình đã có hoặc đã miễn trừ.
7. **Truy vết** – mọi yêu cầu có chức năng phủ; chức năng không có yêu cầu thì `derived` có lý do; lint 0 lỗi.
8. **Xác nhận** – ít nhất một người nghiệp vụ và một người kỹ thuật đã đọc.

Chưa đủ 8/8 thì cây chưa được rời khỏi máy BA.

## Rủi ro khi dùng AI
| Rủi ro | Biểu hiện | Cách chặn |
|---|---|---|
| **Bịa chức năng** | Thêm "tích điểm", "chatbot"… không ai yêu cầu | Mọi chức năng phải có `reqs` hoặc `derived` kèm lý do; lint C3 |
| **Tràn phạm vi** | Cây đầy đủ như sản phẩm hoàn chỉnh | Viết `scope.out` trước; hỏi lại khi chức năng nằm ngoài |
| **Kiến thức chung chung** | Cây giống hệt mọi hệ thống cùng loại, thiếu đặc thù | Dùng domain pack; hỏi mô hình kinh doanh |
| **Sai quy định** | Khẳng định thủ tục pháp lý | Ghi `[xác nhận]`; chức năng tuân thủ do người có thẩm quyền duyệt |
| **Rò rỉ dữ liệu** | Dán tài liệu nội bộ nhạy cảm | Thay tên khách hàng, số tài khoản bằng dữ liệu giả trước khi dán |
| **Teo kỹ năng** | BA chỉ chỉnh bản AI | Tự phân rã tay vài hệ thống nhỏ trước khi dựa vào AI |
