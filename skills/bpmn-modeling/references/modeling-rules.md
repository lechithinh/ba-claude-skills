# Quy tắc vẽ BPMN, lỗi AI hay mắc, checklist nghiệm thu

## Quy tắc nền
1. Mỗi process có start và end rõ ràng; end đặt tên theo trạng thái: "Đã giao món".
2. Task *Động từ + Danh từ*: "Tính giá cước", "Gửi biên lai".
3. Gateway là câu hỏi, có task lấy dữ kiện trước; các nhánh là câu trả lời loại trừ nhau.
4. Tách loại nào gộp loại đó (AND–AND, OR–OR).
5. Trao đổi giữa hai pool dùng send/receive task kèm message flow.
6. Sơ đồ dài: gom bằng sub-process/call activity; link event khi đường nối quá xa.
7. Mọi bước phải *chờ* (người, hệ thống ngoài) đều đã trả lời "chờ quá lâu thì sao?".

Lỗi cụ thể kèm cách sửa: `mistakes-catalog.md`. Cách chọn ký hiệu: `symbol-decisions.md`.

## 6 lỗi AI mắc đi mắc lại và câu sửa
| # | Lỗi | Câu sửa trong prompt |
|---|---|---|
| 1 | Thiếu End Event cho nhánh phụ | "Mỗi nhánh phải có End Event riêng, đặt tên theo kết quả." |
| 2 | Gateway không nhãn điều kiện | "Mọi luồng ra khỏi Exclusive Gateway phải có nhãn điều kiện." |
| 3 | Task sai lane (vd khách "gọi eKYC") | Nêu rõ ai sở hữu từng nhóm hành động. |
| 4 | Task đặt tên bằng danh từ | "Mọi Activity đặt tên Động từ + Tân ngữ." |
| 5 | Rẽ nhánh song song không gộp | "Mỗi Parallel Gateway mở phải có gateway gộp tương ứng." |
| 6 | Bịa bước không tồn tại | Yêu cầu liệt kê giả định; gạch bỏ bước sai. |

Lint `bpmn_lint.py` bắt được #1, #2, #4 (gần đúng), #5; #3 và #6 cần người xác nhận.

## Checklist 8 điểm trước khi đưa vào tài liệu
1. **Cú pháp** – start/end đúng chỗ; mọi nhánh kết thúc bằng End; lint 0 lỗi.
2. **Gateway** – mọi luồng ra có nhãn; gateway mở có gateway gộp.
3. **Lane** – task nằm đúng lane của bên thực hiện.
4. **Đặt tên** – task động từ + tân ngữ; event là danh từ/trạng thái.
5. **Ngoại lệ** – đủ timeout, từ chối, huỷ giữa chừng mà nghiệp vụ có thật; chạy token (`token-review.md`) không còn kịch bản kẹt.
6. **Hệ thống** – bước gọi bên thứ ba khớp danh sách tích hợp đã chốt.
7. **Giả định** – đã đọc hết giả định của AI, loại cái không đúng.
8. **Xác nhận** – ít nhất 1 người thật làm quy trình đã xem lại.

Chưa đủ 8/8 thì sơ đồ chưa được rời khỏi máy BA.

## Rủi ro khi dùng AI
- **Rò rỉ dữ liệu**: thay dữ liệu thật bằng dữ liệu giả trước khi dán; dùng bản doanh nghiệp.
- **Sai quy định pháp lý**: AI không biết thông tư mới nhất; bước tuân thủ do người có thẩm quyền xác nhận.
- **Ảo giác quy trình**: bước nghe hợp lý nhưng không có trong tổ chức; luôn liệt kê giả định.
- **Teo kỹ năng**: vẽ tay đủ nhiều sơ đồ trước khi dựa vào AI.
