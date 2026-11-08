# Decision Table / Bảng quyết định

## Là gì
Một bảng liệt kê **mọi tổ hợp điều kiện** và hành động tương ứng. Khác danh sách rule dạng văn xuôi, bảng buộc bạn nhìn thấy tổ hợp *chưa ai nghĩ tới*. Đây là kỹ thuật phân tích rule nghiệp vụ trong BABOK (Decision Modelling).

## Vì sao BA nên dùng
Văn xuôi: *"Khách hủy được nếu đơn chưa giao, trừ đơn COD đã xác nhận…"*. Người đọc nào cũng tin là đủ. Bảng cho thấy 16 tổ hợp và 3 ô trống.

## Cách chia điều kiện
| Loại | Cách chia | Ví dụ |
|---|---|---|
| Có/Không | 2 giá trị | Đã thanh toán? |
| Danh sách | Mỗi mục một giá trị | Trạng thái đơn: Chờ thanh toán, Đã xác nhận… |
| **Số/thời gian** | **Chia khoảng, nêu rõ biên** | "≤ 2 giờ" / "> 2 giờ" |
| Điều kiện phụ thuộc nhau | Gộp hoặc dùng rule "không hợp lệ" | Chờ thanh toán + COD không tồn tại |

## Ba loại phát hiện
- **Thiếu:** tổ hợp chưa có rule. *Hỏi*, đừng tự điền.
- **Mâu thuẫn:** hai rule cùng áp dụng, kết quả khác. Hầu như luôn do một rule viết quá rộng.
- **Chồng lấn:** hai rule cùng kết quả. Vô hại về hành vi nhưng là dấu hiệu rule chưa rõ.

## Lỗi hay gặp
- Điều kiện không loại trừ nhau ("VIP" và "Khách mới" có thể cùng đúng).
- Ngưỡng thiếu biên (≥ hay >?).
- Quá nhiều điều kiện trong một bảng (6 điều kiện × 4 giá trị = 4096 tổ hợp). Tách bảng.
- Quên tổ hợp **bất khả thi**: nên ghi tường minh và yêu cầu hệ thống chặn.

## Thực hành
Lấy một đoạn rule bạn đang viết trong BRD, hỏi Claude: *"Dựng bảng quyết định cho rule này và kiểm tra tổ hợp thiếu."* Xem bao nhiêu ô trống.
