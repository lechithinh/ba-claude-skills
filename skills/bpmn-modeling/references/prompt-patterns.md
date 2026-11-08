# Khung prompt và vòng làm việc với AI

## Khung 5 phần
1. **Bối cảnh** – công ty/sản phẩm, hệ thống tích hợp, ràng buộc pháp lý.
2. **Phạm vi** – từ sự kiện nào đến sự kiện nào; ngoài phạm vi là gì.
3. **Lane (đúng thứ tự)** – ai/hệ thống nào.
4. **Ngoại lệ bắt buộc** – từ chối, timeout, huỷ giữa chừng…
5. **Đầu ra** – định dạng + "chỉ trả về khối mã" + "liệt kê các giả định đã đặt".

## Yếu vs tốt
- Yếu: "Vẽ sơ đồ BPMN cho quy trình mở tài khoản ngân hàng." → một lane, chỉ happy path, không nhắc eKYC/Core, trả về đoạn văn.
- Tốt (mẫu):
```
Bối cảnh: ngân hàng số - app mobile, tích hợp Core Banking + eKYC Provider bên thứ 3, tuân thủ quy định NHNN.
Phạm vi: từ lúc khách bấm "Mở tài khoản" đến khi tài khoản kích hoạt hoặc hồ sơ bị từ chối. Ngoài phạm vi: đăng nhập, nạp tiền, phát hành thẻ.
Lane (đúng thứ tự): Khách hàng / App ngân hàng / eKYC Provider / Thẩm định.
Ngoại lệ bắt buộc: eKYC không khớp → thẩm định thủ công; eKYC timeout 30s → thử lại tối đa 3 lần; khách bỏ dở → lưu nháp 7 ngày.
Đầu ra: Mermaid flowchart TD, subgraph cho từng lane, chỉ trả về khối mã. Sau đó liệt kê các giả định bạn đã tự đặt.
```

## Vòng Prompt → Review → Refine
1. **Mô tả bằng lời** (10–15 phút, đáng đầu tư nhất): nếu không kể được bằng câu thường thì AI cũng không vẽ được.
2. **Sinh bản nháp** (Mermaid vòng đầu, 2–3 phút).
3. **Soát bằng checklist 8 điểm** → ghi *danh sách lỗi cụ thể*, không phải cảm giác "chưa ổn".
4. **Prompt sửa có chỉ định**: "Giữ nguyên toàn bộ sơ đồ, chỉ sửa 3 điểm sau: (1)… (2)… (3)…". Không nói "giữ nguyên" thì AI vẽ lại từ đầu và làm hỏng chỗ đúng.
5. **Xác nhận với người thật** làm quy trình: "Có bước nào ở đây anh/chị không bao giờ làm không?", "Khi nào quy trình này không chạy như vậy?".

## Prompt hữu ích
- Bảng cấu trúc: "Liệt kê dưới dạng bảng (Lane | Activity/Event | Loại: Start/Task/Gateway/End | Điều kiện nhánh nếu có)".
- Xuất XML: "Trả BPMN 2.0 XML kèm phần BPMNDiagram có toạ độ, nếu không shape sẽ chồng nhau."
- Giải thích cho stakeholder: "Diễn giải sơ đồ này thành 8 câu tiếng Việt đơn giản."
