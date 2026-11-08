# Đầu ra: đặc tả màn hình từ `mockup.png`

> Prompt: *"Viết đặc tả màn hình cho ảnh này (app đặt lịch phòng khám, bệnh nhân dùng)."*
> Chú thích nguồn: **[ảnh]** thấy trong ảnh · **[suy ra]** hợp lý nhưng ảnh không nêu · **[xác nhận]** cần stakeholder quyết.

## Đặc tả màn hình: Đặt lịch khám
**Mục đích:** bệnh nhân chọn chuyên khoa, bác sĩ, ngày, giờ và gửi yêu cầu đặt lịch. **Actor:** Bệnh nhân (đã đăng nhập) [suy ra]. **Tiền điều kiện:** có kết nối mạng. **Điều hướng:** vào từ [màn hình chủ / danh sách bác sĩ: xác nhận]; thoát bằng nút ← [ảnh] hoặc sau khi đặt thành công → [màn hình xác nhận: xác nhận].

### 1. Thành phần
| # | Vùng | Thành phần |
|---|---|---|
| 1 | Thanh tiêu đề | Nút quay lại ←, tiêu đề "Đặt lịch khám" [ảnh] |
| 2 | Form | 8 trường (mục 2) [ảnh] |
| 3 | Chân form | Nút "Xác nhận đặt lịch" [ảnh] |

### 2. Bảng trường
| # | Nhãn | Control | Kiểu dữ liệu | Bắt buộc | Độ dài/định dạng | Mặc định | Nguồn | Validation | Thông báo lỗi |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Chuyên khoa | Dropdown | Mã danh mục | Có [ảnh: *] | - | Trống, "Chọn chuyên khoa" [ảnh] | Danh mục chuyên khoa [suy ra] | Phải chọn | "Vui lòng chọn chuyên khoa" |
| 2 | Bác sĩ | Dropdown | Mã bác sĩ | Có [ảnh] | - | Trống, "Chọn bác sĩ" [ảnh] | Bác sĩ thuộc chuyên khoa đã chọn [suy ra] | Phải chọn; vô hiệu cho tới khi chọn chuyên khoa [suy ra] | "Vui lòng chọn bác sĩ" |
| 3 | Ngày khám | Chọn ngày | Ngày | Có [ảnh] | dd/mm/yyyy [ảnh] | Trống | - | Không chọn ngày quá khứ [suy ra]; giới hạn đặt trước tối đa [N ngày: xác nhận] | "Vui lòng chọn ngày khám" |
| 4 | Khung giờ | Nhóm nút chọn một | Giờ | Có [ảnh] | HH:mm | Không chọn trước [ảnh: 08:30 chỉ là ví dụ trạng thái chọn] | Khung giờ trống của bác sĩ theo ngày [suy ra] | Chọn đúng một khung còn trống | "Vui lòng chọn khung giờ" |
| 5 | Họ và tên | Ô văn bản | Chuỗi | Có [ảnh] | Tối đa [N: xác nhận] | Trống, gợi ý "Nguyễn Văn A" [ảnh] | Có thể điền sẵn từ hồ sơ [xác nhận] | Không chỉ toàn số/ký tự đặc biệt | "Họ và tên không hợp lệ" |
| 6 | Số điện thoại | Ô văn bản (bàn phím số) [suy ra] | Chuỗi số | Có [ảnh] | 10 chữ số bắt đầu bằng 0 [xác nhận] | Trống, gợi ý "09xx xxx xxx" [ảnh] | Có thể điền sẵn từ hồ sơ [xác nhận] | Đúng định dạng | "Số điện thoại không hợp lệ" |
| 7 | Triệu chứng / ghi chú | Ô văn bản nhiều dòng | Chuỗi | Không [ảnh: không có *] | Tối đa **300 ký tự** [ảnh: bộ đếm 0/300] | Trống, gợi ý "Mô tả ngắn…" [ảnh] | - | Cắt/chặn khi quá 300 | "Tối đa 300 ký tự" |
| 8 | Đồng ý nhận SMS nhắc lịch | Checkbox | Boolean | **Có** [ảnh: *] | - | **Chưa chọn** [ảnh] | - | Phải chọn mới gửi được | "Vui lòng đồng ý để tiếp tục" |

### 3. Nút và hành động
| Nút | Điều kiện | Khi bấm | Thất bại |
|---|---|---|---|
| ← | Luôn bật [suy ra] | Quay lại; nếu đã nhập dữ liệu thì hỏi xác nhận bỏ [xác nhận] | - |
| Khung giờ | Còn trống | Chọn khung giờ đó, bỏ chọn khung trước | - |
| Khung giờ xám (09:00) | **Không bấm được** [ảnh: chú thích "đã có người đặt"] | Không phản hồi | - |
| Xác nhận đặt lịch | [Luôn bật, validate khi bấm / chỉ bật khi hợp lệ: xác nhận] | Kiểm tra toàn bộ trường → gửi yêu cầu → chuyển màn hình xác nhận | Khung giờ vừa bị người khác đặt → hiện thông báo và tải lại khung giờ, **giữ nguyên** dữ liệu đã nhập; lỗi mạng/máy chủ → thông báo thử lại, không mất dữ liệu; chống bấm đúp |

### 4. Trạng thái màn hình
| Trạng thái | Hành vi |
|---|---|
| Đang tải danh mục/khung giờ | Hiện chỉ báo tải tại vùng đó [suy ra] |
| Bác sĩ chưa có khung giờ trống ngày đã chọn | Thay nhóm khung giờ bằng thông báo "Bác sĩ chưa có lịch trống ngày này, vui lòng chọn ngày khác" [xác nhận nội dung] |
| Lỗi tải | Thông báo + nút thử lại *(ảnh không có)* |
| Hết phiên đăng nhập | *(ảnh không có)* [xác nhận] |

### 5. Quy tắc tương tác
1. Đổi **Chuyên khoa** → xóa lựa chọn **Bác sĩ** và **Khung giờ**, tải lại danh sách bác sĩ. [suy ra]
2. Đổi **Bác sĩ** hoặc **Ngày** → xóa lựa chọn **Khung giờ**, tải lại khung giờ trống. [suy ra]
3. Giới hạn mỗi bệnh nhân giữ tối đa [2: xác nhận] lịch hẹn sắp tới: kiểm tra khi gửi, báo lỗi nếu vượt. [domain/nghiệp vụ, xác nhận]

### 6. Giả định và điều không thấy trong ảnh
- Không thấy: trạng thái lỗi từng trường, trạng thái tải, màn hình xác nhận sau khi đặt, chọn **cơ sở** nếu có nhiều chi nhánh.
- Không thấy nút/điều hướng **hủy lịch**; việc hủy nằm ở màn khác. [suy ra]

### 7. Câu hỏi mở
1. Checkbox đồng ý nhận SMS là **điều kiện bắt buộc** để đặt lịch: đây là thông báo dịch vụ hay có yếu tố tiếp thị? Cần Pháp chế xác nhận. (Pháp chế)
2. Nút "Xác nhận đặt lịch" luôn bật hay chỉ bật khi đủ hợp lệ? (UX + BA)
3. Họ tên và số điện thoại có điền sẵn từ hồ sơ bệnh nhân không? (Sản phẩm)
4. Giới hạn đặt trước tối đa bao nhiêu ngày? Tối đa bao nhiêu lịch hẹn sắp tới mỗi bệnh nhân? (Quản lý phòng khám)
