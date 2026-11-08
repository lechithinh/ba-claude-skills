# Chế độ Soát danh sách chức năng có sẵn

Soát dễ hơn dựng mới và rủi ro bịa thấp, vì AI chỉ nhận xét trên nội dung được đưa. **Không phân rã lại từ đầu** trừ khi được yêu cầu.

## Nhận đầu vào
| Người dùng đưa | Cách xử lý |
|---|---|
| Danh sách có ID hoặc thụt lề (văn bản, Excel dán) | `scripts/outline_to_spec.py` dựng spec khung, rồi `fd_lint.py` |
| Spec JSON | Chạy thẳng `fd_lint.py` |
| Sơ đồ Mermaid hoặc ảnh cây | Tự dựng lại danh sách (ghi rõ chỗ không đọc được), rồi như trên |
| Tài liệu mô tả bằng lời | Rút danh sách chức năng, hỏi lại nếu mơ hồ |

Spec khung chưa có `objects` và `requirements`. Hỏi người dùng đối tượng chính và danh sách yêu cầu (nếu có), bổ sung rồi lint lại để có CRUD và truy vết.

## Ba việc
1. **LỖI CẤU TRÚC** – chạy lint; dẫn mã (A1…F1) và vị trí. Soát tay các lỗi nhóm G (`mistakes-catalog.md`): module theo màn hình, trộn luồng với cây, phân rã theo giải pháp, bịa chức năng.
2. **THIẾU SÓT** – đối chiếu CRUD, xuyên suốt, domain pack (nếu có), kịch bản ngoại lệ (hủy, hết hạn, timeout, đối soát); với mỗi chức năng chính hỏi "khi X thất bại thì ai làm gì?".
3. **CÂU HỎI CHO STAKEHOLDER** – 5 câu làm rõ điểm còn mơ hồ, ghi ai nên trả lời.

## Mẫu trả lời
```
1. LỖI CẤU TRÚC
   - [LỖI/CẢNH BÁO] [mã] vị trí - mô tả - cách sửa
2. THIẾU SÓT
   - chức năng/nhóm còn thiếu - vì sao cần - đề xuất ID và tên
3. CÂU HỎI CHO STAKEHOLDER
   - câu hỏi (ai nên trả lời)
4. TÓM TẮT: x lỗi, y cảnh báo, độ phủ yêu cầu a/b, CRUD còn thiếu c ô
```

## Mức nghiêm trọng
- **Chặn** (lint báo LỖI): ID sai, tên "Quản lý X" ở lá, yêu cầu chưa phủ, đối tượng không có chức năng Tạo, actor chưa khai báo.
- **Nên sửa**: tên lá là danh từ, gộp hai hành vi, thiếu nhóm xuyên suốt, độ sâu lệch.
- **Gợi ý**: đổi thứ tự module, gộp tính năng chỉ có một con, thêm ưu tiên.

## Nguyên tắc nhận xét
- Dẫn đúng nguyên văn tên bị gắn cờ; không diễn giải lại.
- Cảnh báo lint là **gợi ý có kiểm chứng bằng người**: B1, B3, B4, B5 dùng heuristic, có thể báo oan. Nói rõ và để người dùng quyết.
- Nếu cây đã tốt, nói thẳng và chỉ liệt kê vài điểm chỉnh nhỏ; đừng bắt lỗi cho có.
- Dùng `waive` với lý do thay vì xóa cảnh báo.

## Dịch cho stakeholder
Tóm tắt cây trong 8 câu tiếng Việt đơn giản: hệ thống gồm những phần lớn nào, ai dùng phần nào, phần nào chưa làm, điều gì còn cần quyết. Không dùng mã lỗi hay thuật ngữ kỹ thuật.
