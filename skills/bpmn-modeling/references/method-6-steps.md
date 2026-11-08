# Phương pháp 6 bước dựng sơ đồ BPMN

Dựng sơ đồ theo lớp: mỗi bước thêm một loại ký hiệu và trả lời một câu hỏi. Không nhảy cóc - vẽ ngoại lệ trước khi có happy path là nguồn gốc của phần lớn sơ đồ rối.

Mỗi bước, ghi lại quyết định theo mẫu **Làm gì → Vì sao dùng → Vì sao không dùng cách khác**. Phần "vì sao không" giúp người đọc tin sơ đồ và giúp người review phát hiện chỗ chọn sai ký hiệu.

---

## Bước 1 · Xác định phạm vi
**Câu hỏi:** điều gì kích hoạt quy trình, khi nào coi là xong, những gì *không* vẽ?

| Làm gì | Đầu ra |
|---|---|
| Ghi trigger, kết quả mong đợi (cả kết quả thất bại), phần ngoài phạm vi | Process Scope Statement 2–3 dòng; start event và các end event đặt tên theo trạng thái |

- **Vì sao dùng** start event trống: khi người dùng tự khởi phát, không có tin nhắn/mốc giờ nào kích hoạt. Dùng *message start* khi quy trình bắt đầu bằng một yêu cầu từ bên khác; *timer start* khi chạy theo lịch.
- **Vì sao không** vẽ luôn các quy trình kề bên (vd soát vé tại rạp sau khi mua vé online): khác trigger, khác người làm, khác thời điểm → tách sơ đồ riêng.
- **Vì sao không** đặt tên "Bắt đầu / Kết thúc": không cho người đọc biết gì.

## Bước 2 · Xác định actor & swimlane
**Câu hỏi:** ai/hệ thống nào có hành động trong quy trình, ai thuộc tổ chức khác?

| Làm gì | Đầu ra |
|---|---|
| Liệt kê mọi bên có *hành động*; phân loại cùng tổ chức hay độc lập | 1 pool cho bên sở hữu quy trình, lane cho từng vai trò/hệ thống bên trong; pool thu gọn cho bên ngoài |

- **Vì sao dùng** lane cho người/bộ phận/hệ thống cùng tổ chức: họ chung một luồng điều khiển.
- **Vì sao dùng** pool thu gọn cho bên ngoài (cổng thanh toán, đối tác): ta không thấy và không điều khiển các bước bên trong họ, chỉ gửi/nhận tin nhắn.
- **Vì sao không** chia lane theo màn hình hay module ("Màn chọn ghế"): lane trả lời *ai làm*, không phải *ở đâu*.
- Chi tiết khi phân vân: `pool-vs-lane.md`.

## Bước 3 · Vẽ happy path
**Câu hỏi:** khi mọi thứ suôn sẻ, từng bên làm gì, theo thứ tự nào? **Chưa** rẽ nhánh.

| Làm gì | Đầu ra |
|---|---|
| Vẽ trái → phải; mỗi task nằm trong lane của bên thực sự làm; tên Động từ + Danh từ | Chuỗi task + sequence flow + message flow tới pool ngoài |

- **Vì sao dùng** đúng loại task: user task (người thao tác trên phần mềm), service task (hệ thống tự làm), send/receive task (trao đổi với bên ngoài, đi kèm message flow). Xem `symbol-decisions.md`.
- **Vì sao không** gộp "Thanh toán" thành một task khi có bên ngoài xử lý: sẽ che mất khoảng *chờ kết quả* - chỗ hay phát sinh lỗi nhất.
- **Vì sao không** vẽ ngoại lệ lúc này: mất mạch chính, khó review.

## Bước 4 · Thêm gateway
**Câu hỏi:** ở đâu có "nếu… thì…", việc nào độc lập có thể chạy song song?

| Làm gì | Đầu ra |
|---|---|
| Tìm các câu điều kiện trong lời kể; tìm việc không phụ thuộc nhau | Gateway đặt tên là câu hỏi, mỗi nhánh có nhãn; cặp tách/gộp cùng loại |

- **Vì sao dùng** XOR khi các kết quả loại trừ nhau (thành công / thất bại). Dùng XOR gộp khi nhánh quay lại luồng chính.
- **Vì sao dùng** AND khi các việc luôn cùng xảy ra và độc lập (gửi vé + cộng điểm). AND gộp chờ đủ mọi nhánh.
- **Vì sao không** dùng OR cho kết quả loại trừ nhau.
- **Vì sao không** đặt gateway ngay sau một bước không tạo ra dữ kiện: gateway không tự kiểm tra, cần task lấy dữ kiện trước.
- **Vì sao không** nối tiếp hai việc độc lập: tạo phụ thuộc giả, lỗi ở việc phụ chặn việc chính.

## Bước 5 · Thêm ngoại lệ & sự kiện
**Câu hỏi:** với mỗi bước phải *chờ*, nếu chờ quá lâu, bị lỗi, hoặc người dùng bỏ dở thì sao?

| Làm gì | Đầu ra |
|---|---|
| Duyệt từng task có chờ đợi (người, hệ thống ngoài, thanh toán) | Boundary event (timer/message/error) + luồng ngoại lệ, gộp các lý do huỷ về cùng kết cục; annotation cho quy tắc nghiệp vụ |

- **Vì sao dùng** timer boundary **viền liền** (ngắt) khi hết giờ thì dừng việc đang làm (hết thời gian giữ chỗ).
- **Vì sao dùng** timer boundary **viền đứt** (không ngắt) khi chỉ cần nhắc/leo thang mà việc chính vẫn chạy.
- **Vì sao không** dùng gateway "Quá 10 phút?": gateway chỉ đọc dữ liệu tại một thời điểm, không biết chờ.
- **Vì sao không** dùng error event cho hết giờ: hết giờ là tình huống nghiệp vụ bình thường, không phải lỗi.

## Bước 6 · Review bằng token
**Câu hỏi:** mọi kịch bản thật có tới được một end event không?

| Làm gì | Đầu ra |
|---|---|
| Viết 4–6 kịch bản (thành công, mỗi ngoại lệ chính, mỗi bên ngoài im lặng); chạy token; soát checklist | Bảng kịch bản → kết cục; danh sách lỗ hổng; đề xuất sửa (TO-BE) |

- Dùng `scripts/simulate_tokens.py` và `scripts/build_token_page.py`. Phương pháp: `token-review.md`.
- Kịch bản không tới end event = lỗ hổng. Cách sửa phổ biến: thêm boundary timer + bước đối soát/hoàn tác (xem `examples/cinema-ticketing`).

---

## Ghi quyết định
Báo cáo cuối luôn có bảng:

| Bước | Ký hiệu đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|---|
| 2 | Cổng thanh toán = pool thu gọn | Tổ chức khác, chỉ trao đổi tin nhắn | Lane ngụ ý ta điều khiển các bước của họ |
