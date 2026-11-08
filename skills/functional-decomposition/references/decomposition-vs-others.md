# Phân rã chức năng khác gì các kỹ thuật kề bên

| Kỹ thuật | Trả lời | Hình dạng | Dùng khi |
|---|---|---|---|
| **Phân rã chức năng** | Hệ thống *làm được gì*? | Cây (cấu trúc) | Chốt phạm vi, ước lượng, nền cho backlog và truy vết |
| Sơ đồ quy trình (BPMN) | Việc diễn ra *theo thứ tự nào*, ai làm, rẽ nhánh ra sao? | Luồng | Hiểu và cải tiến quy trình; xem skill `bpmn-modeling` |
| Bản đồ năng lực (capability map) | Doanh nghiệp *có khả năng gì* (cấp chiến lược)? | Lưới/cây thô | Hoạch định chiến lược, ưu tiên đầu tư; thường là đầu vào cho cấp 1 |
| WBS (cấu trúc công việc) | *Dự án* cần làm những công việc gì? | Cây công việc | Lập kế hoạch dự án; khác bản chất: là việc *xây*, không phải việc hệ thống *làm* |
| Story map / backlog | Người dùng *đi qua hành trình* nào, giá trị theo lát cắt nào? | Lưới theo hành trình | Lập kế hoạch release theo giá trị; skill `user-story-writer` |
| Danh sách use case | Actor *tương tác* gì với hệ thống? | Danh sách / sơ đồ | Hợp đồng tương tác ở mức actor–hệ thống |
| Sơ đồ kiến trúc | Hệ thống *được xây từ thành phần* nào? | Khối | Thiết kế kỹ thuật; không phải việc của phân rã chức năng |

## Hai lỗi lẫn lộn phổ biến
1. **Trộn cây với luồng.** "Chọn ghế → Thanh toán → Nhận vé" là thứ tự (quy trình), không phải cấu trúc. Trong cây, ba mục đó chỉ là ba chức năng nằm đâu đó dưới các module phù hợp. Thấy mình viết "sau đó", hãy chuyển sang BPMN (lint không bắt được, mã G2).
2. **Nhầm WBS với phân rã chức năng.** "Thiết kế CSDL", "Viết API", "Kiểm thử" là công việc dự án, không phải chức năng của hệ thống.

## Chuỗi dùng cùng nhau
```
Biên bản họp ──► Yêu cầu ──► Phân rã chức năng ──► User story + AC ──► Test case
 (meeting-to-requirements)   (skill này)         (user-story-writer)
                                 │
                                 ├──► Quy trình chi tiết (bpmn-modeling)
                                 └──► Trạng thái, ERD, context (ba-diagrams)
```
Cây là *xương sống*: mỗi chức năng lá thường thành một hoặc vài user story; mỗi quy trình BPMN thường chạm vào nhiều chức năng.
