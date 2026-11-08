# Phản biện yêu cầu / Requirement Challenge

## Vì sao cần
Phần lớn lỗi nghiêm trọng không nằm ở "happy path" mà ở thứ **không ai hỏi**: hai người cùng đặt hàng cuối, cổng thanh toán trả lời muộn, voucher hết hạn ngay lúc bấm. Một BA giỏi là người hỏi những câu đó *trước khi* dev viết code.

## Tư duy
1. **Mỗi bước hỏi "nếu nó thất bại thì sao?"** và **"nếu nó xảy ra hai lần thì sao?"**
2. **Hỏi về thời gian**: cái gì chờ, chờ bao lâu, hết hạn khi nào.
3. **Hỏi về người khác**: ai khác cùng chạm vào dữ liệu này lúc này?
4. **Hỏi về bên ngoài**: đối tác lỗi, chậm, trả trùng.
5. **Chọn lọc**: danh sách dài 80 mục sẽ không ai đọc. 10 mục đúng chỗ thì có.

## Cách đưa đi họp
Mỗi tình huống đổi thành **câu hỏi có hai lựa chọn** cho người quyết: "Khi voucher hết lượt giữa chừng: (a) báo lỗi và giữ giỏ hàng, (b) tự bỏ voucher và hỏi lại?" Stakeholder trả lời dễ hơn câu hỏi mở.

## Lỗi hay gặp
- Liệt kê rất nhiều, không xếp ưu tiên.
- Bàn chuyện kỹ thuật bên trong mà BA không nhìn thấy.
- Tự quyết hành vi thay stakeholder.
- Quên hỏi *ai bị ảnh hưởng nếu sai* (khách, CSKH, kế toán).

## Thực hành
Lấy một user story sắp vào sprint, hỏi Claude: *"Tìm edge case cho story này, 10 mục quan trọng nhất."* Mang các câu hỏi vào buổi refinement.
