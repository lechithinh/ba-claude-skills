# Review bằng token: AS-IS → lỗ hổng → TO-BE

## AS-IS (`spec.json`)
Lệnh: `python3 scripts/simulate_tokens.py examples/cinema-ticketing/spec.json`

| # | Kịch bản | Thiết lập trong spec | Kết cục |
|---|---|---|---|
| A | Mua thành công | `g1: Có`, `g2: Có` | Khách đã có vé |
| B | Ghế vừa bị người khác giữ | `g1: [Không, Có]` | Khách đã có vé (đi vòng chọn lại ghế 1 lần) |
| C | Thanh toán thất bại | `g2: Không` | Đơn bị huỷ |
| D | Khách bỏ dở quá 10 phút | `fire: [b1]` | Đơn bị huỷ (timer ngắt task thanh toán) |
| E | Cổng thanh toán không trả kết quả | `silent: [mres]` | **KẸT** ở "Nhận kết quả thanh toán" |

**Lỗ hổng:** receive task "Nhận kết quả thanh toán" không có giới hạn thời gian. Nếu cổng thanh toán đã trừ tiền nhưng kết quả không về (mất kết nối, timeout phía đối tác), token chờ mãi: khách mất tiền, không có vé, ghế vẫn bị giữ. Lỗi khớp với phàn nàn của người dùng; nguyên nhân không nằm ở khách nhập sai thông tin.

## TO-BE (`spec-to-be.json`)
Thêm vào sau "Gửi yêu cầu thanh toán":
- **Timer boundary viền liền "Hết 5 phút"** trên "Nhận kết quả thanh toán".
- **Service task "Hỏi lại trạng thái giao dịch"** (đối soát chủ động với cổng thanh toán).
- **XOR "Đã trừ tiền?"**: Có → gộp vào nhánh thành công (gửi vé + cộng điểm); Không → nhả ghế, huỷ đơn.

| # | Kịch bản | Kết cục |
|---|---|---|
| A–D | như AS-IS | không đổi |
| E | Không có kết quả, đối soát thấy đã trừ tiền | Khách đã có vé |
| F | Không có kết quả, đối soát thấy chưa trừ tiền | Đơn bị huỷ |

Lệnh kiểm tra: `simulate_tokens.py spec-to-be.json` → 6 kịch bản, 0 kẹt; `bpmn_lint.py diagram-to-be.bpmn` → 0 lỗi.

## Gap analysis
| Bước AS-IS | Pain point | Thay đổi TO-BE | Ràng buộc / an toàn | Chỉ số theo dõi |
|---|---|---|---|---|
| Nhận kết quả thanh toán | Không giới hạn thời gian chờ; khách bị trừ tiền không có vé | Timer 5 phút + đối soát + rẽ nhánh theo trạng thái thật | Chỉ huỷ đơn khi xác nhận chưa trừ tiền | Số đơn "đã trừ tiền, chưa có vé" → 0; thời gian xử lý khiếu nại |

## Câu hỏi cho người vận hành
1. Hôm nay khi khách báo "trừ tiền mà không có vé", bộ phận nào xử lý và mất bao lâu?
2. Cổng thanh toán có API tra cứu trạng thái giao dịch không? Giới hạn số lần gọi?
3. 5 phút có phù hợp với thời gian xử lý thật của cổng thanh toán không?
4. Nếu đối soát thấy đã trừ tiền nhưng ghế đã bị nhả, xử lý thế nào (giữ lại ghế, đổi ghế, hoàn tiền)?
