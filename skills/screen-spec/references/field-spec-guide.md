# Danh mục validation và thông báo lỗi thường dùng

Mọi con số là **ví dụ khởi điểm**, luôn ghi `[xác nhận]` với stakeholder.

## Quy tắc theo kiểu dữ liệu
| Kiểu | Validation hay dùng | Ví dụ thông báo lỗi |
|---|---|---|
| Bắt buộc | Không rỗng sau khi cắt khoảng trắng đầu/cuối | "Vui lòng nhập {tên trường}" |
| Văn bản ngắn | Độ dài tối thiểu/tối đa; ký tự cho phép | "{Tên trường} tối đa {N} ký tự" |
| Họ tên | Không chỉ toàn số/ký tự đặc biệt; cho phép dấu tiếng Việt | "Họ và tên không hợp lệ" |
| Số điện thoại VN | 10 chữ số bắt đầu bằng 0 [xác nhận]; cho phép dán có khoảng trắng, +84 | "Số điện thoại không hợp lệ" |
| Email | Có @ và tên miền hợp lệ | "Email không hợp lệ" |
| Ngày | Định dạng dd/mm/yyyy; ngày có thật; giới hạn quá khứ/tương lai | "Ngày không hợp lệ" · "Không thể chọn ngày trong quá khứ" |
| Tiền VND | Số nguyên ≥ 0; phân cách hàng nghìn; min/max | "Số tiền tối thiểu {X}đ" |
| Số CCCD | 12 chữ số [xác nhận có chấp nhận CMND 9 số cũ không] | "Số giấy tờ không hợp lệ" |
| Mật khẩu | Độ dài, ký tự bắt buộc, không trùng mật khẩu cũ | Nêu **cụ thể** quy tắc nào chưa đạt |
| Tệp tải lên | Định dạng, kích thước tối đa, số lượng | "Chỉ nhận {định dạng}, tối đa {N}MB" |
| Checkbox đồng ý | Bắt buộc/tùy chọn; ai chịu trách nhiệm nội dung | "Vui lòng đồng ý điều khoản để tiếp tục" |

## Thời điểm validate
- **Khi rời trường** cho lỗi định dạng; **khi gửi** cho lỗi chéo trường và lỗi từ máy chủ.
- Máy chủ **luôn** validate lại, kể cả khi giao diện đã chặn.

## Trạng thái cần mô tả
| Trạng thái | Câu hỏi |
|---|---|
| Đang tải | Hiện gì? Có chặn thao tác không? |
| Rỗng | Hiện gì, có nút hướng dẫn không? |
| Lỗi tải | Thử lại thế nào? Giữ dữ liệu đã nhập? |
| Lỗi khi gửi | Mất mạng, máy chủ 5xx, dữ liệu xung đột (đã có người đặt) |
| Hết phiên | Quay về đăng nhập, giữ lại dữ liệu? |
| Chỉ-đọc / ẩn theo quyền | Vai trò nào thấy trường nào? |
| Nút gửi | Bật khi nào? Chống bấm đúp ra sao? |

## Thông báo
Nêu **vấn đề + cách sửa** ("Số điện thoại cần 10 chữ số"), không đổ lỗi ("Bạn nhập sai"), không dùng mã lỗi kỹ thuật cho người dùng cuối.
