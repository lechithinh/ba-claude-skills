---
name: edge-case-finder
description: Đóng vai "luật sư phản biện" cho yêu cầu, user story hay luồng nghiệp vụ - quét theo 12 nhóm tình huống biên (dữ liệu, thời gian, đồng thời, quyền hạn, trạng thái, hệ thống ngoài, số lượng, tiền tệ, tiếng Việt/ký tự, kênh/thiết bị, vận hành/dữ liệu cũ, lạm dụng/bảo mật) và trả về danh sách NGẮN, xếp ưu tiên, mỗi mục có hậu quả nếu bỏ sót, đề xuất hành vi hoặc câu hỏi cho stakeholder, kèm AC Gherkin cho các mục quan trọng nhất. Dùng khi người dùng muốn tìm lỗ hổng trong yêu cầu trước khi dev bắt đầu, review story, "nếu… thì sao", chuẩn bị UAT. Trigger - "edge case", "trường hợp biên", "nếu… thì sao", "tìm lỗ hổng yêu cầu", "phản biện yêu cầu", "ngoại lệ", "negative test", "kịch bản lỗi".
---

# Edge Case Finder (phản biện yêu cầu)

Đọc một yêu cầu, story hoặc luồng và tìm những tình huống **có thể xảy ra thật** mà yêu cầu chưa trả lời. Mục tiêu không phải liệt kê 80 trường hợp chung chung mà là **10–15 điều đáng hỏi nhất cho đúng tính năng này**, xếp theo mức nguy hại.

## Quy trình

1. **Hiểu hành vi chính**: ai làm gì, dữ liệu vào/ra, trạng thái trước/sau, hệ thống ngoài nào tham gia. Nếu thiếu, hỏi tối đa 3 câu hoặc ghi giả định.
2. **Quét 12 nhóm** trong `references/edge-case-catalog.md`; với mỗi nhóm chỉ giữ tình huống *áp dụng được* cho tính năng này.
3. **Đánh giá** mỗi tình huống: **Tác động** (mất tiền/dữ liệu/uy tín > khó chịu nhỏ) × **Khả năng xảy ra** (hằng ngày > hiếm). Giữ top 10–15.
4. **Với mỗi tình huống ghi**: bối cảnh cụ thể → hậu quả nếu bỏ sót → **đề xuất hành vi hoặc câu hỏi** → loại (lỗ hổng yêu cầu / NFR / chỉ cần test).
5. **Gom câu hỏi theo stakeholder** (ai quyết) để BA mang đi họp.
6. **Viết AC Gherkin** cho 3–5 tình huống đầu bảng.

## Đầu ra

```markdown
## Edge cases: <tên tính năng>
**Yêu cầu gốc (trích):** "…"   **Giả định:** …

### Danh sách ưu tiên
| # | Nhóm | Tình huống | Hậu quả nếu bỏ sót | Mức | Đề xuất / câu hỏi | Loại |
|---|---|---|---|---|---|---|
| 1 | Đồng thời | Hai tab cùng áp một voucher còn 1 lượt | Dùng vượt lượt, mất tiền | Cao | Trừ lượt nguyên tử khi tạo đơn; báo lỗi rõ cho tab sau | Yêu cầu |

### Câu hỏi theo stakeholder
**Marketing:** …  **Vận hành:** …  **Tech lead:** …

### AC Gherkin cho các mục đầu bảng
```gherkin
Scenario: Hai người cùng dùng lượt voucher cuối
  Given voucher "SALE10" còn 1 lượt
  When hai khách đặt đơn dùng "SALE10" cùng lúc
  Then chỉ một đơn được giảm giá
  And đơn còn lại nhận thông báo "Voucher đã hết lượt"
```

### Đã quét nhưng không áp dụng
(liệt kê ngắn các nhóm bị loại để người đọc biết đã cân nhắc)
```

## Quy tắc
- **Ngắn mà sắc**: tối đa 15 mục; không lặp lại cùng một lỗi ở nhiều nhóm; không liệt kê thứ hiển nhiên ("mất điện").
- **Gắn với văn bản**: trích câu yêu cầu liên quan; không bàn tới thứ yêu cầu không đụng tới.
- **Đưa ra câu hỏi, không tự quyết nghiệp vụ**: hành vi đề xuất ghi là *đề xuất*; giá trị cụ thể (thời hạn, hạn mức) ghi `[xác nhận]`.
- Phân loại rõ để người dùng biết cái nào là *thay đổi yêu cầu*, cái nào là *NFR* (hiệu năng, bảo mật), cái nào chỉ là *test*.
- Có domain pack thì đọc `checklist.md` và `business-rules.md` của pack (`domain-banking`, `domain-ecommerce`, `domain-payments`, `domain-lending`, `domain-logistics`) để nhặt các tình huống đặc thù ngành, đánh dấu `[domain]`.
- Không phỏng đoán lỗi kỹ thuật bên trong code mà bạn chưa thấy; chỉ nói về hành vi quan sát được từ phía nghiệp vụ.

## Chuỗi skill
`user-story-writer` / `screen-spec` / `api-spec` → **`edge-case-finder`** → cập nhật AC; rule nhiều tổ hợp → `decision-table`; kiểm tra chất lượng câu chữ → `requirements-linter`.

## Tham chiếu
| File | Nội dung |
|---|---|
| `references/edge-case-catalog.md` | 12 nhóm tình huống, mỗi nhóm kèm câu hỏi gợi ý |
| `LEARN.md` | Tư duy phản biện yêu cầu, cách chọn cái đáng hỏi |
| `examples/voucher-checkout.md` | Ví dụ đầy đủ: áp voucher khi thanh toán |
