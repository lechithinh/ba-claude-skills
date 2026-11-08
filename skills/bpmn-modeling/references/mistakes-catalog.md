# Danh mục lỗi sai thường gặp

Mỗi lỗi: **Sai** (dấu hiệu nhận ra) → **Vì sao sai** → **Sửa**. Cột *Lint* cho biết `scripts/bpmn_lint.py` có tự bắt được không (✓ = có, ~ = cảnh báo gần đúng, – = cần người soát).

## A. Lỗi chung
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| A1 | Sequence flow nối giữa hai pool | Ngụ ý hai tổ chức chung một luồng điều khiển | Dùng message flow (nét đứt, tròn rỗng đầu, tam giác rỗng cuối) | ✓ (XML) |
| A2 | Tách AND nhưng gộp bằng XOR (hoặc không gộp) | XOR không chờ đủ nhánh: bước sau chạy nhiều lần | Tách AND thì gộp AND | ✓ |
| A3 | Gateway không có câu hỏi, nhánh không nhãn | Người đọc không biết khi nào đi nhánh nào | Đặt tên gateway là câu hỏi; nhãn loại trừ nhau trên từng nhánh | ✓ |
| A4 | Nhánh cụt, thiếu end event | Không rõ quy trình kết thúc hay còn chờ | Mỗi nhánh về một end event, đặt tên theo kết quả | ✓ |
| A5 | Message flow giữa hai lane cùng pool | Cùng tổ chức, cùng luồng điều khiển, không "gửi tin nhắn" cho nhau | Dùng sequence flow | ✓ |
| A6 | Tên task mơ hồ ("Hoá đơn", "Xử lý", "Bước 3") | Mỗi người hiểu một kiểu | Động từ + Danh từ: "Xuất hoá đơn" | ~ |

## B. Dùng sai event
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| B1 | Luồng đi vào start event | Start là điểm khởi đầu; vẽ ở giữa làm token "sinh ra" lần nữa | Mốc giữa process dùng intermediate event hoặc nối thẳng task → task | ✓ |
| B2 | Luồng đi ra từ end event | Bước sau end không bao giờ chạy | Đưa bước đó lên trước end event | ✓ |
| B3 | Timer ở end event ("Hết 10 phút") | Timer chỉ có dạng bắt | Timer boundary trên task đang chờ → bước xử lý → end | ✓ |
| B4 | Nhận message bằng start event trống | Người đọc không biết quy trình chờ ai | Dùng message start event | ✓ (cảnh báo) |
| B5 | Timer trung gian nối tiếp thay cho timer boundary | Nghĩa thành "làm xong rồi chờ thêm X", không phải "quá X thì huỷ" | Giới hạn thời gian của task → gắn timer lên viền task | – |
| B6 | Sau event-based gateway là task thường | Cổng chờ sự kiện; mỗi nhánh phải bắt đầu bằng thứ "chờ" được | Chỉ dùng event bắt hoặc receive task sau cổng | ✓ |

## C. Nối sai event, task và đường nối
| # | Sai | Vì sao sai | Sửa | Lint |
|---|---|---|---|---|
| C1 | Sequence flow đi vào boundary event | Boundary chỉ "nghe" sự kiện khi task chạy, không phải một bước | Luồng chính vào task; boundary chỉ có luồng ra | ✓ |
| C2 | Boundary event không có luồng ra | Khi kích hoạt, token không có đường đi | Nối tới bước xử lý ngoại lệ hoặc end event | ✓ |
| C3 | Association (nét chấm) nối hai task | Token không đi theo association: task sau không bao giờ chạy | Thứ tự luôn dùng sequence flow | – |
| C4 | Data object nằm giữa luồng, nối bằng sequence flow | Dữ liệu không "chạy" | Nối task → task; data object treo bên cạnh bằng data association | – |
| C5 | Hai luồng ra khỏi task, không có gateway | Nghĩa là mọi nhánh cùng chạy, dù có nhãn "Còn / Hết" | Thêm XOR gateway ngay sau task | ~ |
| C6 | Message flow nối vào data store | Message flow là tin nhắn giữa hai bên; phải có task/event "nhận" | Nối tới receive task; task ghi vào data store bằng data association | – |

## D. Lỗi nghiệp vụ (cú pháp đúng nhưng sai thực tế)
| # | Sai | Vì sao sai | Sửa |
|---|---|---|---|
| D1 | Task nằm sai lane (khách "gọi API") | Sai người chịu trách nhiệm | Đặt task vào lane của bên thực sự làm |
| D2 | Không xử lý bên ngoài im lặng (không phản hồi) | Token kẹt mãi ở receive task - người dùng mất tiền/mất thời gian | Timer boundary + bước đối soát/hoàn tác (`token-review.md`) |
| D3 | Gateway không có task lấy dữ kiện trước | Gateway không tự kiểm tra | Thêm task kiểm tra trước gateway |
| D4 | Bịa bước "nghe hợp lý" (thêm cấp phê duyệt) | Sơ đồ không phản ánh thực tế | Đưa vào danh sách giả định để người vận hành xác nhận |

Khi soát sơ đồ, dẫn mã lỗi (vd "B5", "C1") để người dùng tra lại phần giải thích.
