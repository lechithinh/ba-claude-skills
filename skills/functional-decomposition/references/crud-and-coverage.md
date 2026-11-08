# CRUD và kiểm tra độ phủ

## Ý tưởng
Với mỗi **đối tượng nghiệp vụ** (đơn, thẻ, lịch hẹn…), hỏi: ai tạo, ai xem, ai sửa, ai hủy hoặc lưu trữ? Ô nào trống là một chức năng có thể đang bị bỏ sót. Đây là cách rẻ nhất để tìm thiếu sót, và là phần `fd_lint.py` kiểm tự động (mã D1–D6).

## Cách khai báo trong spec
```json
"objects": [{"id": "appt", "name": "Lịch hẹn"}],
... {"id": "1.2.1", "name": "Hủy lịch hẹn online", "ops": {"appt": "D"}}
```
`ops` là chữ cái `C`, `R`, `U`, `D` (gộp được: `"CU"`). `D` gồm hủy, lưu trữ, vô hiệu hóa và xóa.

## Ma trận mẫu
| Đối tượng | Create | Read | Update | Delete / Hủy |
|---|---|---|---|---|
| Lịch hẹn | 1.1.2, 1.1.3 | 1.3.1, 1.3.2 | 1.3.3 | 1.2.1, 1.2.2 |
| Hồ sơ bệnh nhân | 5.1.1 | 5.1.3 | 5.1.2 | — (miễn) |

## Khi ô trống là hợp lệ
Không phải ô trống nào cũng là lỗi. Ghi rõ lý do thay vì lờ đi:
| Tình huống | Cách khai báo |
|---|---|
| Dữ liệu do hệ thống khác sở hữu, hệ thống này chỉ đọc | `"source": "external"` (bỏ qua D1, D3, D4) |
| Bản ghi bất biến (nhật ký, lịch sử thông báo) | `"immutable": true` |
| Cố ý không xóa (giao dịch tài chính, hồ sơ phải lưu) | `"no_delete": true` + `note` giải thích |
| Cảnh báo khác muốn bỏ qua có lý do | `"waive": {"D6:3.2.3": "lý do"}` |

Mọi miễn trừ hiện trong báo cáo ở mức **MIỄN**, không biến mất.

## Ngoài CRUD: vòng đời và chuyển trạng thái
Đối tượng có trạng thái (đơn: chờ thanh toán → đã xác nhận → đang giao…) cần thêm chức năng **chuyển trạng thái**: duyệt, từ chối, khóa, mở khóa, hoàn tiền, đóng. Chúng thường nằm dưới `U` nhưng nên có tên riêng. Hãy vẽ sơ đồ trạng thái (`ba-diagrams`) và kiểm: mỗi mũi tên chuyển trạng thái có một chức năng làm việc đó không?

## Ba loại ma trận khác từ cùng spec
| Ma trận | Hỏi | Dùng để |
|---|---|---|
| **Yêu cầu → chức năng** | Yêu cầu nào chưa có chức năng? | Phát hiện bỏ sót (lint C2) |
| **Chức năng → yêu cầu** | Chức năng nào chưa có nguồn? | Phát hiện mạ vàng, bịa chức năng (lint C3) |
| **Actor × Module** | Ai dùng phần nào? | Điểm xuất phát cho ma trận vai trò – quyền |

`spec_to_table.py` và trang explorer đều sinh sẵn cả bốn ma trận.

## Độ phủ ≠ chất lượng
Đủ CRUD chỉ chứng tỏ không thiếu *loại* chức năng, không chứng tỏ từng chức năng được mô tả đúng. Phần "đúng" thuộc về acceptance criteria (`user-story-writer`) và người nghiệp vụ xác nhận.
