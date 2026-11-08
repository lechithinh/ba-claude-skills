# Đặt vé xem phim online – dựng sơ đồ qua 6 bước

**Mô tả đầu vào (ví dụ):** "Khách mở app, chọn phim, suất chiếu, chọn ghế. Hệ thống giữ ghế 10 phút. Khách chọn combo bắp nước rồi thanh toán qua cổng thanh toán. Thanh toán xong thì gửi vé QR qua email và cộng điểm thành viên. Người dùng hay phàn nàn: ghế bị người khác lấy mất, và bị trừ tiền nhưng không thấy vé."

Kết quả cuối: `spec.json` → `diagram.bpmn`, `diagram.svg`, `diagram.mmd`, `tokens.html`. Review và TO-BE: `review.md`.

---

## Bước 1 · Phạm vi
- **Trigger:** khách muốn mua vé trên app. **Kết thúc:** "Khách đã có vé" hoặc "Đơn bị huỷ".
- **Ngoài phạm vi:** xem trailer, nhận khuyến mãi, soát vé tại rạp, đổi/hoàn vé.

| Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|
| Start event None "Khách muốn mua vé" | Khách tự khởi phát, không có tin nhắn/lịch kích hoạt | Message start: không có bên nào gửi yêu cầu |
| Hai end event theo trạng thái | Báo cáo được tỉ lệ từng kết cục | Một end "Kết thúc": không biết quy trình kết thúc ra sao |
| Không vẽ soát vé tại rạp | Khác trigger, người làm, thời điểm | Gộp vào: sơ đồ quá dài, khó review |

## Bước 2 · Actor & swimlane
| Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|
| Pool "Đặt vé xem phim online" với lane **Khách hàng**, **Hệ thống đặt vé** | Khách thao tác trên giao diện do rạp thiết kế; rạp quyết định thứ tự bước | Lane theo màn hình ("Màn chọn ghế"): lane là *ai làm* |
| **Cổng thanh toán** = pool thu gọn ở trên | Tổ chức khác; rạp chỉ gửi yêu cầu, nhận kết quả | Lane: ngụ ý rạp điều khiển các bước của cổng thanh toán |

## Bước 3 · Happy path
Chọn phim và suất chiếu → Chọn ghế → Kiểm tra và giữ ghế → Chọn combo và thanh toán → Gửi yêu cầu thanh toán → Nhận kết quả thanh toán → Gửi vé QR qua email → Khách đã có vé.

| Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|
| User task cho bước khách làm | Người thao tác trên phần mềm | Manual task: không phải việc làm tay ngoài hệ thống |
| Service task "Kiểm tra và giữ ghế" | Hệ thống tự làm | User task: không có người tham gia |
| Send task + receive task + 2 message flow | Thấy rõ khoảng **chờ** kết quả từ bên ngoài | Một task "Thanh toán": che mất chỗ hay lỗi nhất |

## Bước 4 · Gateway
| Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|
| XOR "Ghế còn trống?" sau task kiểm tra | Hai kết quả loại trừ nhau; có dữ kiện trước | Gateway ngay sau "Chọn ghế": gateway không tự kiểm tra |
| XOR gộp trước "Chọn ghế" cho nhánh "Không" | Vòng chọn lại ghế rõ ràng | Nối thẳng vào task: hợp lệ nhưng khó đọc |
| XOR "Thanh toán thành công?" | Thành công / thất bại loại trừ nhau | OR: không thể cùng đúng |
| AND tách + gộp: gửi vé, cộng điểm | Hai việc độc lập, luôn cùng xảy ra | Nối tiếp: lỗi cộng điểm sẽ chặn khách nhận vé |

## Bước 5 · Ngoại lệ & sự kiện
| Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|
| Timer boundary **viền liền** "Hết 10 phút" trên "Chọn combo và thanh toán" | Hết giờ giữ ghế thì dừng việc thanh toán | Gateway "Quá 10 phút?": gateway không biết chờ. Viền đứt: khách vẫn trả tiền cho ghế đã nhả |
| XOR gộp trước "Nhả ghế đang giữ" | Hết giờ và thanh toán lỗi dùng chung một bước | Hai task "Nhả ghế" trùng nhau |

## Bước 6 · Review bằng token
Chạy `python3 scripts/simulate_tokens.py examples/cinema-ticketing/spec.json`: 5 kịch bản, kịch bản **E (cổng thanh toán không trả kết quả)** kẹt ở "Nhận kết quả thanh toán". Đây đúng là lời phàn nàn "bị trừ tiền nhưng không thấy vé". Phân tích và TO-BE: `review.md`.
