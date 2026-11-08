# Mẫu báo cáo kèm sơ đồ BPMN

Dùng cho mọi lần giao sơ đồ (chế độ Vẽ và AS-IS → TO-BE). Bỏ mục không áp dụng, đừng để trống.

---

## 1. Phạm vi
- **Trigger:** …
- **Kết thúc khi:** … (thành công) / … (thất bại, huỷ)
- **Ngoài phạm vi:** …

## 2. Tóm tắt sơ đồ
| Lane / Pool | Activity / Event | Loại | Điều kiện nhánh |
|---|---|---|---|
| Khách hàng | Chọn ghế | User task | |
| Hệ thống | Ghế còn trống? | XOR gateway | Có → Chọn combo; Không → Chọn lại ghế |

## 3. Quyết định ký hiệu
Chỉ ghi những lựa chọn không hiển nhiên.

| Phần tử | Đã chọn | Vì sao dùng | Vì sao không dùng |
|---|---|---|---|
| Cổng thanh toán | Pool thu gọn | Tổ chức khác, chỉ trao đổi tin nhắn | Lane: ngụ ý ta điều khiển các bước của họ |
| Hết 10 phút giữ ghế | Timer boundary viền liền | Hết giờ thì dừng việc thanh toán | Gateway "Quá 10 phút?": gateway không biết chờ |

## 4. Kịch bản token
| # | Kịch bản | Kết cục | Vấn đề |
|---|---|---|---|
| A | Thành công | Khách đã có vé | Không |
| E | Bên ngoài không phản hồi | — | **Kẹt** ở "Nhận kết quả thanh toán" |

**Lỗ hổng & đề xuất:** …

## 5. Kiểm tra
- Lint: X lỗi, Y cảnh báo (đã sửa: …)
- Checklist 8 điểm: …/8

## 6. Giả định
- [ ] … (bước không có trong mô tả gốc - gạch bỏ nếu sai)

## 7. Câu hỏi cho người vận hành
1. Có bước nào ở đây anh/chị không bao giờ làm?
2. Khi nào quy trình không chạy như vậy?
3. Nếu <bên ngoài> không trả lời thì hôm nay đang xử lý thế nào?
