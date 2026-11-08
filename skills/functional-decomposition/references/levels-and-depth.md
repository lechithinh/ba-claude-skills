# Cấp độ và độ sâu: dừng ở đâu là đủ

## Các cấp
| Cấp | Tên | Trả lời | ID | Số lượng thường gặp |
|---|---|---|---|---|
| 1 | **Module** (năng lực) | Hệ thống làm được *việc lớn* nào? | `1` | 4–9 |
| 2 | **Tính năng** | Người dùng muốn đạt *mục tiêu* nào trong năng lực đó? | `1.1` | 2–9 mỗi module |
| 3 | **Chức năng** (lá) | *Hành động nguyên tử* nào hiện thực mục tiêu đó? | `1.1.1` | 2–9 mỗi tính năng |
| 4 | Chức năng con | Chỉ khi hệ thống kỹ thuật, một chức năng còn quá lớn | `1.1.1.1` | hiếm |

Mặc định **dừng ở cấp 3**. Cấp 4 xuất hiện khi chức năng vẫn quá lớn để ước lượng; nếu phải xuống cấp 5 thì thường đang vẽ thiết kế, không còn là phân rã chức năng (lint A5 cảnh báo khi sâu hơn 4).

### Bỏ cấp 2 khi module nhỏ
Module chỉ có 3–6 chức năng không cần cấp tính năng; để lá nằm thẳng dưới module (ID `2.1`, `2.2`…). Ví dụ `examples/cafe-pos`. Đừng tạo tính năng chỉ có một con (lint A2). Hậu quả: các nhánh trong cây có thể sâu khác nhau, nhưng **anh em cùng cha không nên lệch từ 2 cấp** trở lên (lint A4).

## Hàm test "chức năng nguyên tử"
Một nút là lá đúng khi trả lời **có** cho phần lớn câu sau:
1. Có **một actor chính** thực hiện không?
2. Có **một mục tiêu / một kết quả quan sát được** không? (tester nhìn vào biết pass hay fail)
3. Đặt được tên bằng **một động từ cụ thể** không?
4. Viết được **một user story** với khoảng 3–7 tiêu chí chấp nhận không?
5. Developer ước lượng được trong **khoảng một sprint** hoặc ngắn hơn không?

| Kết quả | Hành động |
|---|---|
| Hai câu trở lên trả lời "không" | **Tách** thêm |
| Các mảnh sau khi tách không có tiêu chí chấp nhận riêng | **Gộp lại**, đã nhỏ quá |
| Chức năng chỉ khác nhau ở một tham số (loại thẻ, loại nghỉ) | Giữ một chức năng, ghi biến thể vào `note` hoặc business rule |

## Khi nào dừng
- **Dừng** khi lá qua hàm test, và đội có thể ước lượng và kiểm thử.
- **Đừng dừng** ở "Quản lý X", "Báo cáo", "Tích hợp": đó là nhóm, chưa phải chức năng.
- **Đừng đi quá** khi bắt đầu mô tả cách làm (bảng, API, thuật toán): đó là thiết kế.

## Độ sâu theo mục đích
| Mục đích | Độ sâu hợp lý |
|---|---|
| Thống nhất phạm vi với lãnh đạo | Cấp 1–2 |
| Ước lượng sơ bộ, lập kế hoạch release | Cấp 2–3 |
| Viết backlog, truy vết yêu cầu, test | Cấp 3 (lá) |
| Tài liệu hệ thống kế thừa | Theo mức cần hiểu; ưu tiên module quan trọng |

Cùng một spec có thể xuất sơ đồ ở nhiều độ sâu (`spec_to_mermaid.py --depth`, `spec_to_svg.py --depth`).
