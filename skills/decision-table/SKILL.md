---
name: decision-table
description: Biến các quy tắc nghiệp vụ rời rạc thành bảng quyết định (decision table) và kiểm tra bằng script - liệt kê mọi tổ hợp điều kiện, chỉ ra tổ hợp THIẾU rule, rule MÂU THUẪN, rule CHỒNG LẤN, rút gọn bảng và sinh test case. Dùng khi người dùng có nhiều điều kiện chồng nhau (trạng thái × loại khách × hình thức thanh toán…), cần chốt business rule, kiểm tra rule có đủ và nhất quán không, hoặc sinh test từ rule. Trigger - "bảng quyết định", "decision table", "business rule", "tổ hợp điều kiện", "rule có đủ chưa", "rule mâu thuẫn", "if-else nhiều nhánh", "sinh test từ rule".
---

# Bảng quyết định (Decision Table)

Biến một đoạn mô tả rule kiểu "nếu A thì… trừ khi B thì…" thành bảng điều kiện × hành động, rồi **kiểm tra bằng máy**: mọi tổ hợp đã có rule chưa, hai rule có mâu thuẫn không. AI chỉ phác thảo; kết quả mỗi tổ hợp thiếu phải do **người chủ nghiệp vụ quyết định**.

## Khi nào dùng
- Rule có **từ 2 điều kiện trở lên** tác động chéo nhau (trạng thái đơn × hình thức thanh toán × người hủy).
- Mô tả rule hiện có nhiều "trừ khi", "ngoại trừ", "nếu không thì".
- Cần **test case** bám sát rule, hoặc cần chứng minh rule đã đủ trước khi dev bắt đầu.
- *Không* dùng cho thứ tự các bước (dùng `bpmn-modeling`) hoặc vòng đời một đối tượng (dùng sơ đồ trạng thái ở `ba-diagrams`).

## Quy trình

1. **Gom rule và nguồn.** Rút từ mô tả/BRD: danh sách *điều kiện* và *hành động*, mỗi rule gắn nguồn (BR-xx, người nói). Không có nguồn thì ghi `[xác nhận]`.
2. **Chuẩn hoá điều kiện** - mỗi điều kiện là một tập giá trị **loại trừ nhau và phủ hết**: có/không, danh sách trạng thái, hoặc *chia khoảng* cho số ("≤ 2 giờ", "> 2 giờ"; "< 10 triệu", "10 triệu trở lên"). Ngưỡng thiếu biên (≥ hay >?) là câu hỏi đầu tiên cho stakeholder.
3. **Viết spec JSON** (khuôn trong `scripts/dt_check.py`, mẫu `examples/order-cancel/spec.json`): `conditions`, `actions`, `rules`. Điều kiện nào rule không nhắc thì bỏ trống = "không quan tâm".
4. **Chạy kiểm tra:**
   ```bash
   python3 scripts/dt_check.py spec.json               # THIẾU / MÂU THUẪN / CHỒNG LẤN, thoát 1 nếu có LỖI
   python3 scripts/dt_check.py spec.json --table       # mọi tổ hợp, để rà soát với stakeholder
   python3 scripts/dt_check.py spec.json --simplify    # bảng rút gọn bằng "-" (không quan tâm)
   python3 scripts/dt_check.py spec.json --tests       # test case, mỗi tổ hợp một dòng
   ```
5. **Xử lý từng phát hiện** (bảng dưới), sửa spec, chạy lại tới 0 lỗi.
6. **Báo cáo** theo mẫu bên dưới, kèm câu hỏi cho stakeholder.

| Phát hiện | Nghĩa | Hành động |
|---|---|---|
| **THIẾU** | Tổ hợp chưa có rule | Hỏi stakeholder; **không tự điền**. Nếu tổ hợp *không thể xảy ra*, thêm rule "không hợp lệ" và yêu cầu hệ thống chặn nó |
| **MÂU THUẪN** (lỗi) | Hai rule cùng áp dụng nhưng cho kết quả khác | Hỏi rule nào đúng; thường do một rule viết quá rộng |
| **CHỒNG LẤN** | Hai rule cùng áp dụng, cùng kết quả | Gộp hoặc thu hẹp điều kiện cho rõ |
| Rule không áp dụng cho tổ hợp nào | Rule thừa hoặc sai giá trị | Xoá hoặc sửa |

## Đầu ra

```markdown
## Bảng quyết định - <tên>
**Phạm vi:** …  · **Điều kiện:** C1 …, C2 … · **Số tổ hợp:** 16 → 8 dòng sau rút gọn

### Bảng (đã rút gọn)
| Trạng thái đơn | Hình thức thanh toán | Người hủy | Hành động |
|---|---|---|---|
| Chờ thanh toán | Trả trước | - | Hủy đơn, giải phóng tồn kho |

### Kết quả kiểm tra
0 lỗi, 0 cảnh báo · phủ 16/16 tổ hợp (bản nháp: 2 mâu thuẫn, 3 thiếu, 2 chồng lấn)

### Câu hỏi cho stakeholder
1. Đơn đang xử lý, khách hủy, trả trước: hủy ngay hay chờ người bán duyệt? (Vận hành)

### Test case (từ --tests, thêm test biên cho ngưỡng số)
```

## Quy tắc
- **Không bịa giá trị**: ngưỡng, thời hạn, số tiền chưa có thì `[xác nhận]`, không tự chọn.
- Tối đa **5–6 điều kiện** mỗi bảng; nhiều hơn thì tách theo nhóm điều kiện (script từ chối khi vượt 5000 tổ hợp).
- Điều kiện số phải có **test biên**: giá trị ngay dưới, bằng và ngay trên ngưỡng.
- Mỗi rule có ID và nguồn để truy vết (`functional-decomposition`, `user-story-writer` dùng lại ID này).
- Nếu có domain pack (`domain-banking`, `domain-ecommerce`, `domain-payments`, `domain-lending`, `domain-logistics`), dùng `business-rules.md` của pack để gợi ý điều kiện hay bị bỏ sót (kênh, hạng khách, phương thức thanh toán…), và ghi rõ chúng là gợi ý cần xác nhận.
- Bảng và script chỉ chứng minh **đủ và nhất quán**, không chứng minh rule **đúng nghiệp vụ**.

## Tham chiếu
| File | Nội dung |
|---|---|
| `LEARN.md` | Kỹ thuật decision table: khi nào dùng, cách chia khoảng, lỗi thường gặp |
| `scripts/dt_check.py` | Kiểm tra, rút gọn, sinh test (chỉ cần Python 3) |
| `examples/order-cancel/` | Hủy đơn hàng: bản nháp có lỗi → bản đã sửa, bảng đầy đủ/rút gọn, test case |
