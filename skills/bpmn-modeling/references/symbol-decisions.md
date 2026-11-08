# Chọn ký hiệu: tình huống → ký hiệu đúng → vì sao không dùng cách khác

Dùng bảng này khi quyết định ký hiệu và khi giải thích quyết định trong báo cáo. Mỗi dòng có phần "vì sao không" vì đó là chỗ người mới hay chọn sai.

## Activity
| Tình huống | Dùng | Vì sao không dùng… |
|---|---|---|
| Người dùng bấm chọn trên app | **User task** | *Manual task*: người dùng đang thao tác trên phần mềm, không phải làm tay ngoài hệ thống |
| Hệ thống tự kiểm tra/ghi dữ liệu | **Service task** | *User task*: không có người tham gia. *Script task*: chỉ khi engine chạy script do người mô hình viết |
| Nhân viên làm việc tay (kiểm hàng, soát vé) | **Manual task** | *User task*: không có phần mềm hỗ trợ |
| Gửi yêu cầu sang tổ chức khác | **Send task + message flow** | *Sequence flow*: tổ chức khác không chung luồng điều khiển. *Message event ném*: send task dễ đọc hơn |
| Chờ kết quả từ tổ chức khác | **Receive task + message flow** | *Gộp vào task gửi*: che mất khoảng chờ, chỗ hay có lỗi nhất |
| Tính giá theo bảng quy tắc | **Business rule task** | *Gateway nhiều nhánh*: bảng quy tắc gọn hơn, sửa quy tắc không phải vẽ lại |

## Rẽ nhánh
| Tình huống | Dùng | Vì sao không dùng… |
|---|---|---|
| Thành công / thất bại | **XOR** | *OR*: hai kết quả loại trừ nhau, không bao giờ cùng đúng |
| Hai việc độc lập luôn cùng xảy ra | **AND tách + AND gộp** | *Nối tiếp*: tạo phụ thuộc giả. *XOR*: chỉ chạy được một việc |
| Khách có thể chọn thêm A và/hoặc B | **OR tách + OR gộp** | *AND*: không phải lúc nào cũng có cả hai. *XOR*: chọn được nhiều |
| Chờ phản hồi hay hết giờ, cái nào đến trước | **Event-based gateway** | *XOR*: XOR đọc dữ liệu đang có, không biết chờ sự kiện |
| Quyết định dựa trên kết quả kiểm tra | **Task lấy dữ kiện → XOR** | *XOR ngay sau bước không tạo dữ kiện*: gateway không tự kiểm tra |
| Nhánh "Không" quay lại bước trước | **XOR gộp trước bước đó** | *Nối thẳng vào task*: vẫn hợp lệ nhưng khó đọc; gộp rõ ràng hơn |

## Thời gian & ngoại lệ
| Tình huống | Dùng | Vì sao không dùng… |
|---|---|---|
| Hết thời hạn thì huỷ việc đang làm | **Timer boundary viền liền (ngắt)** | *Gateway "Quá X phút?"*: gateway không biết chờ. *Viền đứt*: việc cũ vẫn chạy, có thể xử lý trên dữ liệu đã huỷ |
| Quá hạn thì nhắc, việc vẫn tiếp tục | **Timer boundary viền đứt (không ngắt)** | *Viền liền*: sẽ huỷ luôn việc chính |
| Chờ một khoảng cố định rồi mới làm tiếp | **Intermediate timer (nối tiếp)** | *Boundary*: boundary là giới hạn thời gian của task, không phải thời gian chờ |
| Hệ thống ngoài báo lỗi trong lúc xử lý | **Error boundary** | *Error event ở giữa luồng*: error chỉ ném ở end event |
| Người dùng huỷ giữa chừng | **Message boundary viền liền** hoặc event sub-process | *Gateway*: gateway không nhận được sự kiện xảy ra trong lúc task đang chạy |
| Không nhận được phản hồi từ bên ngoài | **Timer boundary trên receive task + bước đối soát** | *Để trống*: token kẹt mãi (lỗ hổng phổ biến nhất) |

## Bắt đầu & kết thúc
| Tình huống | Dùng | Vì sao không dùng… |
|---|---|---|
| Người dùng tự khởi phát | **Start event None** | *Message start*: không có tin nhắn nào kích hoạt |
| Bắt đầu khi nhận yêu cầu từ bên khác | **Message start event** | *Start None*: người đọc không biết quy trình chờ ai |
| Chạy theo lịch | **Timer start event** | *Start None + ghi chú*: mất thông tin kích hoạt |
| Mỗi kết cục khác nhau | **End event riêng, tên theo trạng thái** | *Một end chung "Kết thúc"*: không biết quy trình kết thúc ra sao |

## Đường nối & dữ liệu
| Tình huống | Dùng | Vì sao không dùng… |
|---|---|---|
| Thứ tự trong cùng tổ chức (kể cả khác lane) | **Sequence flow** | *Message flow*: hai lane cùng pool không "gửi tin nhắn" cho nhau |
| Trao đổi giữa hai tổ chức | **Message flow** | *Sequence flow*: ngụ ý hai bên chung một luồng điều khiển |
| Task đọc/ghi dữ liệu | **Data association** | *Sequence flow qua data object*: dữ liệu không "chạy", không đứng trong luồng |
| Ghi chú quy tắc | **Text annotation + association** | *Task "Ghi chú…"*: annotation không phải bước công việc |
