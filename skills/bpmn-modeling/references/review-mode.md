# Chế độ Soát sơ đồ có sẵn

Soát dễ hơn sáng tạo, rủi ro ảo giác thấp vì AI chỉ nhận xét trên nội dung được đưa. **Không vẽ lại** trừ khi được yêu cầu.

## Ba việc
1. **LỖI CÚ PHÁP** – vi phạm quy tắc BPMN 2.0. Với file `.bpmn`, chạy `scripts/bpmn_lint.py`; với Mermaid/mô tả, soát tay theo `mistakes-catalog.md` và dẫn mã lỗi (A1…D4).
2. **NGOẠI LỆ THIẾU** – chạy token qua các kịch bản (`token-review.md`; nếu dựng lại được spec thì dùng `scripts/simulate_tokens.py`). Tình huống chưa xử lý (mất mạng giữa chừng, đối tác timeout, số dư đổi giữa lúc quét mã, huỷ giữa chừng, trùng yêu cầu, người duyệt vắng).
3. **CÂU HỎI CHO STAKEHOLDER** – 5 câu làm rõ điểm còn mơ hồ.

## Mẫu trả lời
```
1. LỖI CÚ PHÁP
   - [mức LỖI/CẢNH BÁO] [mã lỗi] vị trí - mô tả - cách sửa
2. NGOẠI LỆ THIẾU
   - tình huống - ảnh hưởng - đề xuất nhánh xử lý
3. CÂU HỎI CHO STAKEHOLDER
   - câu hỏi (ai nên trả lời)
4. DIỄN GIẢI (nếu được yêu cầu): 8 câu tiếng Việt đơn giản
```

## Mức nghiêm trọng
- **Chặn**: nhánh không End, gateway không nhãn, task sai lane, thiếu gộp AND.
- **Nên sửa**: tên task là danh từ, thiếu default flow, thiếu ngoại lệ chính.
- **Gợi ý**: bố cục, tách sub-process, đổi message event thành Send/Receive Task.

## Dịch cho stakeholder
8 câu tiếng Việt đơn giản: ai làm gì, rẽ nhánh khi nào, kết thúc ra sao; không dùng thuật ngữ BPMN.
