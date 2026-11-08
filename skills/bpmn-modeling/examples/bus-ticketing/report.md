# Đặt vé xe khách trực tuyến – Báo cáo

## 1. Phạm vi
- **Trigger:** hành khách cần đi xe khách.
- **Kết thúc khi:** Đã có vé (thành công) / Không có chuyến / Đặt vé không thành công (từ chối thanh toán, hết 10 phút, bỏ dở).
- **Ngoài phạm vi:** hoàn vé, đổi vé, check-in, lên xe.

## 2. Tóm tắt sơ đồ
| Lane / Pool | Activity / Event | Loại | Điều kiện nhánh |
|---|---|---|---|
| Hành khách | Cần đi xe khách | Start | |
| Hành khách | Nhập tuyến và ngày đi | User task | |
| Hệ thống đặt vé | Tìm chuyến còn chỗ | Service task | |
| Hệ thống đặt vé | Có chuyến phù hợp? | XOR | Không → Không có chuyến; Có → Chọn chuyến |
| Hành khách | Chọn chuyến và ghế | User task | |
| Hệ thống đặt vé | Giữ ghế 10 phút | Service task | |
| Hệ thống đặt vé | Giữ ghế được? | XOR | Không (ghế đã bán) → Chọn lại; Được → Nhập thông tin |
| Hành khách | Nhập thông tin hành khách | User task + timer boundary ngắt | Hết 10 phút → Nhả ghế |
| Hệ thống đặt vé | Gửi yêu cầu thanh toán | Send task | → pool Cổng thanh toán |
| Hệ thống đặt vé | Nhận kết quả / Hết 10 phút | Event-based gateway | Đến trước thì đi nhánh đó |
| Hệ thống đặt vé | Thanh toán thành công? | XOR | Có → Xuất vé; Không → Nhả ghế |
| Hệ thống đặt vé | Xuất vé điện tử, Gửi vé | Service task, send task | → Đã có vé |
| Hệ thống đặt vé | Nhả ghế đã giữ | Service task | → Đặt vé không thành công |
| Cổng thanh toán | | Pool thu gọn | Message flow |

## 3. Quyết định ký hiệu
| Phần tử | Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|---|
| Cổng thanh toán | Pool thu gọn | Tổ chức khác, chỉ trao đổi tin nhắn | Lane: ngụ ý mình điều khiển bước của họ |
| Chờ kết quả thanh toán | Event-based gateway | Chờ sự kiện đến trước, có đường ra khi cổng im lặng | XOR "Quá 10 phút?": gateway không biết chờ |
| Hết giờ khi nhập thông tin | Timer boundary ngắt | Hết giờ giữ ghế thì dừng việc nhập | Bỏ qua: ghế bị giữ mãi |
| Các lý do thất bại | Gộp qua XOR về một "Nhả ghế" và một end | Cùng một hệ quả | 3 end riêng: trùng kết cục |
| Ghế đã bán | Vòng lặp về "Chọn chuyến và ghế" | Cho chọn ghế khác | Kết thúc luôn: mất khách |

## 4. Kịch bản token
| # | Kịch bản | Kết cục | Vấn đề |
|---|---|---|---|
| A | Đặt vé thành công | Đã có vé | Không |
| B | Không có chuyến phù hợp | Không có chuyến | Không |
| C | Ghế bị mua trước, chọn lại | Đã có vé | Không |
| D | Thanh toán bị từ chối | Đặt vé không thành công | Không |
| E | Cổng thanh toán im lặng | Đặt vé không thành công | Không |
| F | Hành khách bỏ dở | Đặt vé không thành công | Không |

## 5. Kiểm tra
- Lint: 0 lỗi, 0 cảnh báo.
- Token: 6 kịch bản, 0 bị kẹt.

## 6. Giả định (được áp dụng làm cơ sở triển khai)
- [x] Ghế giữ đúng 10 phút, tính từ lúc chọn ghế.
- [x] Chỉ một cổng thanh toán, không có bước chọn phương thức.
- [x] Vé điện tử gửi qua email hoặc SMS.
- [x] Thanh toán lỗi thì không thử lại, phải đặt lại từ đầu.
- [x] Tìm chuyến không cần đăng nhập; một hành khách, một chiều.

## 7. Câu hỏi cần xác nhận với nhà xe
1. Thời gian giữ ghế thực tế, có gia hạn được không?
2. Thanh toán thất bại có cho thử lại với ghế đang giữ không?
3. Cổng đã trừ tiền nhưng kết quả về trễ sau khi hết giờ thì xử lý thế nào?
4. Có cần đăng nhập hoặc xác thực số điện thoại trước khi giữ ghế không?
