# Khung prompt và vòng Prompt → Lint → Sửa

## Khung 5 phần
1. **Bối cảnh và mô hình**: hệ thống gì, cho ai, kênh nào (*"App đặt lịch cho phòng khám, bệnh nhân dùng app, lễ tân dùng web"*).
2. **Phạm vi**: trong/ngoài (*"chưa làm thanh toán đặt cọc"*).
3. **Nguồn**: dán biên bản, đoạn BRD, danh sách yêu cầu có ID; nhắc thay dữ liệu thật bằng dữ liệu giả.
4. **Ràng buộc**: số module mong muốn, độ sâu, domain pack dùng, ngôn ngữ.
5. **Đầu ra**: spec + bảng + Mermaid; có cần CSV/explorer không.

### Ví dụ
> Phân rã chức năng cho app đặt lịch phòng khám (bệnh nhân dùng app, lễ tân dùng web). Ngoài phạm vi: thanh toán đặt cọc, hồ sơ bệnh án. Yêu cầu: FR-01…FR-08 dưới đây [dán]. Độ sâu 3 cấp, dùng ID cho truy vết. Cho tôi spec JSON, bảng phân cấp, sơ đồ Mermaid và kết quả lint.

## Vòng 3 bước
1. **Prompt** – sinh bản đầu.
2. **Lint và soát** – chạy `fd_lint.py`, ghi danh sách lỗi cụ thể (không phải cảm giác "chưa ổn").
3. **Refine** – sửa theo danh sách, chạy lại tới 0 lỗi.

## Câu sửa cho lỗi hay gặp
| Hiện tượng | Câu sửa |
|---|---|
| Tên lá là "Quản lý X" | "Mọi chức năng đặt tên Động từ + Danh từ; tách 'Quản lý X' thành từng thao tác." |
| Hai module chồng lấn | "Gộp 'A' và 'B' hoặc nêu ranh giới rõ ràng; không để hai tên gần giống ở hai nhánh." |
| Thiếu xuyên suốt | "Thêm đăng nhập/phân quyền, thông báo, nhật ký thao tác, báo cáo, cấu hình, hoặc nêu lý do chưa cần." |
| Chức năng không rõ nguồn | "Mọi chức năng phải có yêu cầu nguồn; chức năng suy ra thì ghi 'derived' kèm lý do." |
| Cây sâu 5 cấp | "Dừng ở cấp 3; chi tiết hơn để vào user story." |
| Bịa chi tiết nghiệp vụ | "Không bịa; giá trị chưa biết ghi [xác nhận] và liệt kê câu hỏi mở." |

## Mẫu prompt cho từng chế độ
| Chế độ | Prompt mẫu |
|---|---|
| A. Phân rã | "Phân rã chức năng cho … Ngoài phạm vi: … Nguồn: [dán]. Xuất spec và bảng." |
| B. Soát | "Soát danh sách chức năng này [dán]: tìm lỗi cấu trúc, thiếu sót, và 5 câu hỏi cho stakeholder." |
| C. Dựng ngược | "Đây là menu và danh sách API của hệ thống cũ [dán]. Dựng danh mục chức năng và chỉ ra chức năng nghi đã chết." |
| D. Giải thích | "Phân rã chức năng khác sơ đồ quy trình thế nào? Nên dừng ở cấp nào?" |
| Đối chiếu yêu cầu | "Đối chiếu danh sách yêu cầu này với cây chức năng: yêu cầu nào chưa được phủ, chức năng nào chưa có nguồn?" |
| Thay đổi phạm vi | "Thêm yêu cầu mới [dán]; chức năng nào bị ảnh hưởng, cần thêm gì?" |
