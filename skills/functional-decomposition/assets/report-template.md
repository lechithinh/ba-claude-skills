# Mẫu báo cáo kèm cây phân rã chức năng

Dùng cho mọi lần giao cây (chế độ Phân rã, Soát, Dựng ngược). Bỏ mục không áp dụng, đừng để trống.

---

## 1. Phạm vi và giả định
- **Mục tiêu:** …
- **Trong phạm vi:** … · **Ngoài phạm vi:** …
- **Actor:** …
- **Giả định:** … (gạch bỏ nếu sai)

## 2. Tóm tắt cây
| ID | Chức năng | Actor | Ưu tiên | Yêu cầu |
|---|---|---|---|---|
| **1** | **Đặt và quản lý lịch hẹn** | | | |
| 1.1.2 | Tạo lịch hẹn tự phục vụ | Bệnh nhân | M | FR-01 |

Thống kê: … module · … tính năng · … chức năng · sâu … cấp. Sơ đồ: `diagram.mmd` / `diagram.svg`.

## 3. Quyết định cấu trúc
Chỉ ghi những lựa chọn không hiển nhiên.

| Phần tử | Đã chọn | Vì sao làm | Vì sao không làm cách khác |
|---|---|---|---|
| Module "Thông báo" tách riêng | Cấp 1 | Dùng chung cho đặt, hủy, nhắc lịch | Đặt trong từng module: lặp 3 lần, khó đổi kênh |
| "Quản lý lịch hẹn" | Tách thành Tạo / Xem / Hủy | Mỗi thao tác có quy tắc và actor riêng | Giữ một dòng: không ước lượng, không viết AC được |

## 4. CRUD và truy vết
| Đối tượng | Create | Read | Update | Delete | Ghi chú |
|---|---|---|---|---|---|
| Lịch hẹn | 1.1.2 | 1.3.1 | 1.3.3 | 1.2.1 | |

- **Yêu cầu chưa phủ:** …
- **Chức năng `derived` cần xác nhận:** … (nguồn: domain pack / thông lệ)

## 5. Kiểm tra
- Lint: X lỗi, Y cảnh báo, Z miễn trừ (đã sửa: …; miễn trừ: … vì …)
- Checklist 8 điểm: …/8

## 6. Giả định
- [ ] … (chức năng/giá trị không có trong nguồn - gạch bỏ nếu sai)

## 7. Câu hỏi cho stakeholder
1. … (ai nên trả lời)
2. …
3. …

## 8. Bước tiếp theo
- Viết user story + AC cho chức năng ưu tiên `M` (`user-story-writer`)
- Vẽ quy trình chi tiết cho chức năng chính (`bpmn-modeling`)
- Kiểm tra chất lượng yêu cầu (`requirements-linter`)
