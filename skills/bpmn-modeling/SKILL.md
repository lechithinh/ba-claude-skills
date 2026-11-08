---
name: bpmn-modeling
description: Mô hình hoá quy trình nghiệp vụ bằng BPMN 2.0 - từ mô tả bằng lời tới sơ đồ Mermaid, file .bpmn (BPMN 2.0 XML có toạ độ, mở được trong bpmn.io, draw.io, Camunda Modeler), SVG và trang HTML chạy token theo từng kịch bản; kèm giải thích vì sao chọn từng ký hiệu, kiểm tra lỗi và review bằng token để tìm lỗ hổng. Dùng khi người dùng muốn vẽ/soát/cải tiến quy trình với pool, lane, event, task, gateway, ngoại lệ, AS-IS và TO-BE, hỏi nên dùng ký hiệu BPMN nào, hoặc muốn mô phỏng các kịch bản của quy trình. Trigger - "BPMN", "vẽ quy trình", "swimlane", "process flow", "AS-IS TO-BE", "sơ đồ quy trình nghiệp vụ", "gateway", "business process model", "soát sơ đồ BPMN", "chạy token", "kịch bản quy trình".
---

# BPMN Modeling

Biến mô tả quy trình thành sơ đồ BPMN 2.0 đúng chuẩn OMG, có lý do cho từng lựa chọn ký hiệu và được kiểm chứng bằng token. AI chỉ **phác thảo bản nháp**; việc xác nhận nghiệp vụ thuộc về người vận hành quy trình.

## Chọn chế độ

| Người dùng muốn | Chế độ | Đọc |
|---|---|---|
| Vẽ quy trình mới từ mô tả | **A. Vẽ** | 6 bước dưới + `references/method-6-steps.md` |
| Cải tiến quy trình hiện có | **B. AS-IS → TO-BE** | `references/as-is-to-be.md`, `token-review.md` |
| Kiểm tra sơ đồ có sẵn (Mermaid/XML/mô tả/ảnh) | **C. Soát** | `references/review-mode.md`, `mistakes-catalog.md` |
| Hỏi nên dùng ký hiệu nào, ký hiệu nghĩa là gì | **D. Giải thích** | `symbol-decisions.md`, `notation-core.md`, `pool-vs-lane.md` |

Mặc định dùng ký hiệu trong `notation-core.md`. Chỉ dùng `notation-advanced.md` (signal, escalation, compensation, complex gateway, sub-process…) khi người dùng hỏi tới hoặc quy trình thật sự cần, và giải thích thêm một câu khi dùng.

## Chế độ A – Vẽ (6 bước)

1. **Phạm vi** – trigger, kết quả mong đợi (cả kết quả thất bại), phần ngoài phạm vi. Viết Process Scope Statement 2–3 dòng.
2. **Actor & swimlane** – một tổ chức = một pool; vai trò/hệ thống cùng tổ chức = lane; bên ngoài = pool thu gọn nối bằng message flow (`pool-vs-lane.md`).
3. **Happy path** – trái → phải, chưa rẽ nhánh; task *Động từ + Danh từ*, đúng lane, đúng loại (`symbol-decisions.md`).
4. **Gateway** – điều kiện → XOR (câu hỏi + nhãn nhánh); việc độc lập → AND tách/gộp; luôn có task lấy dữ kiện trước gateway.
5. **Ngoại lệ & sự kiện** – mỗi bước phải *chờ*: chờ quá lâu, lỗi, người dùng bỏ dở thì sao → boundary event + luồng ngoại lệ; gộp các lý do huỷ về một kết cục.
6. **Review bằng token** – viết 4–6 kịch bản (thành công, từng ngoại lệ, từng bên ngoài im lặng), chạy `simulate_tokens.py`, soát checklist 8 điểm (`modeling-rules.md`). Kịch bản kẹt = lỗ hổng → đề xuất sửa.

Ở mỗi bước, ghi quyết định theo mẫu **Làm gì → Vì sao dùng → Vì sao không dùng cách khác**.

### Thiếu thông tin thì hỏi gì
Chỉ hỏi khi mô tả chưa nêu (tối đa 4 câu, một lượt): (1) bắt đầu/kết thúc ở đâu, (2) ai/hệ thống nào tham gia, bên nào thuộc tổ chức khác, (3) ngoại lệ nào có thật (từ chối, hết giờ, huỷ, không phản hồi), (4) có hệ thống bên thứ ba nào. Không đủ thì vẽ theo **giả định ghi rõ**, đừng bịa bước.

## Đầu ra

Viết **một spec JSON** (định dạng: `references/output-formats.md`, mẫu: `examples/*/spec.json`), rồi sinh mọi định dạng từ đó:

```bash
python3 scripts/spec_to_mermaid.py  spec.json diagram.mmd     # vòng nháp, dán mermaid.live / Notion / GitHub
python3 scripts/spec_to_bpmn.py     spec.json diagram.bpmn    # BPMN 2.0 XML có toạ độ
python3 scripts/bpmn_lint.py        diagram.bpmn              # phải 0 lỗi trước khi giao
python3 scripts/spec_to_svg.py      spec.json diagram.svg     # hình đẹp để chèn tài liệu
python3 scripts/simulate_tokens.py  spec.json                 # kịch bản → kết cục, token kẹt ở đâu
python3 scripts/build_token_page.py spec.json tokens.html     # trang HTML: chọn kịch bản, xem token chạy
```

- **Vòng nháp:** Mermaid + bảng tóm tắt để người dùng soát nội dung nhanh.
- **Vòng cuối** (khi đã chốt nội dung, hoặc người dùng cần file): `.bpmn` + lint + SVG; thêm trang token khi cần trình bày/review.
- Spec hỗ trợ một pool nhiều lane cho process chính, pool ngoài thu gọn (`pools`) và message flow (`messages`). Bố cục tự động là bản nháp: đường nối có thể chồng nhau; nhắc người dùng kéo chỉnh trong bpmn.io (nội dung và logic không đổi).
- Màu SVG/HTML chỉnh trong `assets/svg-theme.css`.

## Báo cáo kèm theo (luôn có)

Theo mẫu `assets/report-template.md`:
- **Phạm vi** (2–3 dòng).
- **Bảng tóm tắt**: Lane | Activity/Event | Loại | Điều kiện nhánh.
- **Bảng quyết định ký hiệu**: những lựa chọn không hiển nhiên, mỗi dòng có "vì sao dùng / vì sao không".
- **Kịch bản token**: kịch bản → kết cục, kịch bản kẹt (nếu có) và đề xuất sửa.
- **Kết quả lint**: số lỗi/cảnh báo, đã sửa gì.
- **Danh sách giả định**: mỗi bước không có trong mô tả gốc, để người dùng gạch bỏ.
- **3–5 câu hỏi cho người vận hành** (`review-mode.md`).

## Quy tắc chất lượng
- Start/end rõ ràng; mỗi kết cục một end event đặt tên theo trạng thái ("Đã giao món").
- Gateway là câu hỏi, có task lấy dữ kiện trước; mọi nhánh ra khỏi XOR/OR có nhãn; tách loại nào gộp loại đó.
- Task đúng lane của bên thực sự làm (khách không "gọi API").
- Sequence flow chỉ trong một pool; giữa các pool dùng message flow; mọi trao đổi với bên ngoài đi qua send/receive task.
- Mọi bước phải chờ đều đã có câu trả lời cho "chờ quá lâu thì sao?" - nếu không, kịch bản "bên ngoài im lặng" sẽ kẹt.
- Không bịa bước "nghe hợp lý" khi mô tả không nêu - đưa vào giả định.
- **Dữ liệu nhạy cảm**: nếu người dùng dán dữ liệu thật (tên, số tài khoản), nhắc thay bằng dữ liệu giả.
- Dùng tên chung cho ví dụ ("cổng thanh toán", "ứng dụng gọi xe"), không gắn thương hiệu thật nếu người dùng không yêu cầu.

## Tham chiếu
| File | Nội dung |
|---|---|
| `references/method-6-steps.md` | 6 bước dựng sơ đồ, mỗi bước: câu hỏi, đầu ra, vì sao dùng / vì sao không |
| `references/notation-core.md` | Ký hiệu cốt lõi, mỗi ký hiệu có "Dùng khi" |
| `references/notation-advanced.md` | Signal, escalation, compensation, link, complex gateway, marker, sub-process… |
| `references/symbol-decisions.md` | Tình huống → ký hiệu đúng → vì sao không dùng ký hiệu khác |
| `references/pool-vs-lane.md` | Quy tắc pool/lane và các trường hợp hay phân vân |
| `references/mistakes-catalog.md` | 22 lỗi sai (A1–D4): sai / vì sao / sửa, lint có bắt được không |
| `references/token-review.md` | Luật đi của token, viết kịch bản, từ lỗ hổng tới TO-BE |
| `references/modeling-rules.md` | Quy tắc nền, lỗi AI hay mắc, checklist 8 điểm, rủi ro khi dùng AI |
| `references/output-formats.md` | Spec JSON (pools, messages, scenarios), Mermaid, XML, SVG, trang token |
| `references/prompt-patterns.md` | Khung prompt 5 phần, vòng Prompt → Review → Refine |
| `references/as-is-to-be.md` | Thu thập AS-IS, pain point, TO-BE, Gap Analysis |
| `references/review-mode.md` | Soát sơ đồ có sẵn, mức nghiêm trọng, câu hỏi stakeholder |
| `references/tools.md` | bpmn.io, draw.io, Camunda Modeler… |
| `examples/cinema-ticketing/` | Ví dụ đầy đủ: 6 bước (`walkthrough.md`), AS-IS có lỗ hổng, review, TO-BE |
| `examples/ride-hailing/` | Collaboration 3 pool, event-based gateway, vòng lặp thử lại |
| `examples/food-delivery/` | AND tách/gộp, error boundary, timer không ngắt |
| `examples/counter-order/` | Ví dụ tối giản cho người mới |
| `examples/ekyc/` | Mở tài khoản ngân hàng số, thẩm định thủ công |
| `evals/` | Đề bài kiểm tra chất lượng skill và tiêu chí đạt |
