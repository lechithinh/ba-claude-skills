# Tiêu chí đạt

Mỗi đề đạt khi thoả **tất cả** mục "Bắt buộc". Mục "Nên có" dùng để so sánh chất lượng giữa các phiên bản skill.

## Áp dụng cho mọi đề phân rã (E1, E3, E4, E9)
**Bắt buộc**
- Có **spec JSON** và ít nhất bảng phân cấp hoặc Mermaid; chạy `fd_lint.py` **0 lỗi**.
- Báo cáo có đủ: phạm vi và giả định, bảng tóm tắt, bảng quyết định cấu trúc (vì sao làm / vì sao không), CRUD và truy vết, kết quả lint, danh sách giả định, câu hỏi cho stakeholder.
- Module theo **năng lực** (không theo màn hình hay phòng ban); 4–9 module.
- Mọi lá bắt đầu bằng **động từ cụ thể**, không "Quản lý X"; ID đúng dạng `1 / 1.1 / 1.1.1`.
- Có đủ nhóm xuyên suốt (xác thực/phân quyền, thông báo, nhật ký, báo cáo, cấu hình) **hoặc** miễn trừ kèm lý do.
- Không bịa giá trị nghiệp vụ; giá trị chưa biết ghi `[xác nhận]`.

**Nên có**
- Ma trận CRUD cho đối tượng chính, có chỉ ra thiếu sót hoặc miễn trừ hợp lệ.
- Gợi ý bước tiếp theo (`user-story-writer`, `bpmn-modeling`).

## E1
- Nêu giả định rõ vì chưa có domain pack: duyệt một cấp, nhiều loại nghỉ, chính sách phép cần xác nhận với HR.
- Có các chức năng dễ bỏ sót: **ủy quyền duyệt**, **nhắc/chuyển cấp khi quá hạn duyệt**, **xin hủy đơn đã duyệt**, **chuyển phép tồn sang năm sau**, **đồng bộ cây tổ chức**.
- Không tự thêm tính năng ngoài phạm vi (tính lương, chấm công chi tiết) mà không ghi rõ.

## E2
- Hỏi tối đa 4 câu trong một lượt (lĩnh vực/mô hình bán hàng, ngoài phạm vi, có tài liệu yêu cầu không, mức chi tiết) **hoặc** làm với danh sách giả định rõ. Không dựng cây to đùng chung chung như một sản phẩm hoàn chỉnh.

## E3
- Nạp `domain-banking`; lấy khung từ capability map, **cắt đúng phạm vi** (không kéo cả cho vay, mở tài khoản vào).
- Có chức năng **suy ra từ domain** gắn `derived: true` + `[domain]`: tra cứu tên người thụ hưởng, kiểm tra hạn mức, **xác thực theo ngưỡng**, **xử lý timeout/pending và đối soát**, chống gửi trùng, tính phí, nhật ký/AML.
- Không khẳng định hạn mức hay ngưỡng cụ thể là sự thật; ghi `[xác nhận]`, nhắc kiểm tra quy định hiện hành.

## E4
- Nạp `domain-ecommerce`; hỏi hoặc nêu giả định mô hình sàn nhiều người bán.
- Có: **kiểm lại tồn kho/giá/voucher khi đặt hàng**, **xử lý callback thanh toán mất**, **hết hạn thanh toán → giải phóng tồn kho**, **tách đơn theo người bán**, **đối soát COD**, **phân bổ voucher để hoàn tiền một phần**, **hoàn tiền về phương thức gốc**, điều chỉnh hóa đơn điện tử.
- Cây Mermaid ≤ 40 node hoặc tách theo module.

## E5
Phải chỉ ra (dẫn mã trong `mistakes-catalog.md`):
- **B2**: "Quản lý đơn hàng" ở lá; **G1/B5**: "Màn hình đơn hàng" là module theo màn hình.
- **B1**: "Khách hàng" là danh từ; **B4**: "Thêm và sửa khách hàng" gộp hai hành vi.
- **B3 (lỗi)**: hai "Thanh toán online" trùng tên ngay trong cùng nhóm (3.1, 3.2).
- **A2**: module 2 chỉ có một con.
- **D**: thiếu Xem/Hủy cho khách hàng; thiếu Tạo/Hủy rõ ràng cho đơn hàng.
- **E1**: thiếu xác thực, nhật ký, báo cáo, cấu hình.
Không phân rã lại toàn bộ trừ khi được yêu cầu; có 5 câu hỏi cho stakeholder.

## E6
- Liệt kê R4 và R6 là **chưa phủ** (C2) và hai chức năng chưa có nguồn (C3); đề xuất thêm chức năng cho R4, R6 hoặc ghi rõ yêu cầu bị loại.
- Không tự gán yêu cầu cho chức năng mồ côi để "cho khớp"; hỏi nguồn.

## E7
- Dựng module theo năng lực, **không chép cấu trúc menu**; nói rõ điều đó.
- Đánh dấu "Công cụ X" là *nghi đã chết*, hỏi vận hành xác nhận; "Gộp mã", "Chạy job đêm" là chức năng thật cần mô tả mục đích.
- Ghi các suy luận là **giả định**; có danh sách câu hỏi cho đội vận hành.

## E8
- Phân biệt: cây = *cái gì* (cấu trúc), BPMN = *theo thứ tự nào* (luồng); không trộn.
- Hàm test chức năng nguyên tử (5 câu) và quy tắc dừng ở cấp 3; "Quản lý X" chưa phải chức năng.
- Gợi ý chuỗi dùng cùng `user-story-writer`, `bpmn-modeling`.

## E9
- Giữ **xung đột** của stakeholder trong câu hỏi mở, không tự giải quyết.
- Chức năng có `reqs` trỏ về yêu cầu trích từ biên bản; chức năng thêm từ chuyên môn gắn `derived`.
- Không lặp lại dữ liệu cá nhân trong biên bản.

## E10
- Truy từ yêu cầu → chức năng bị ảnh hưởng (1.2.x hủy, 1.3.x xem…); đề xuất thêm chức năng "Đổi lịch hẹn" với ID kế tiếp, **không đánh lại số** các ID cũ.
- Nêu hệ quả: đối tượng, quy tắc khung giờ, thông báo, báo cáo no-show; hỏi lại điểm chưa rõ (đổi lịch tính vào hạn hủy 2 giờ không?).
