---
name: functional-decomposition
description: Phân rã chức năng (Functional Decomposition) - biến mô tả, biên bản họp, BRD hoặc hệ thống có sẵn thành cây hệ thống → module → tính năng → chức năng với ID ổn định, actor, ưu tiên, truy vết yêu cầu; kiểm tra MECE, ma trận CRUD, chức năng xuyên suốt; xuất bảng Markdown, Mermaid, SVG, CSV/Jira và trang HTML khám phá; có lint tự động, chế độ soát danh sách có sẵn, dựng ngược từ hệ thống cũ, tích hợp domain pack ngân hàng/TMĐT. Dùng khi cần phân rã chức năng, liệt kê module/tính năng, function breakdown, scope breakdown, soát danh sách chức năng, đối chiếu yêu cầu với chức năng. Trigger - "phân rã chức năng", "sơ đồ phân rã", "liệt kê chức năng hệ thống", "functional decomposition", "feature breakdown", "module list", "WBS chức năng".
---

# Phân rã chức năng (Functional Decomposition)

Biến mô tả hệ thống thành một **cây chức năng** đủ nhỏ để ước lượng, viết user story và kiểm thử; mỗi nút có ID ổn định, actor, nguồn yêu cầu, và được kiểm chứng bằng lint (MECE, CRUD, xuyên suốt, truy vết). AI chỉ **phác thảo bản nháp**; việc xác nhận nghiệp vụ thuộc về người vận hành và stakeholder.

## Chọn chế độ

| Người dùng muốn | Chế độ | Đọc |
|---|---|---|
| Phân rã hệ thống mới từ ý tưởng, biên bản, BRD, danh sách yêu cầu | **A. Phân rã** | 6 bước dưới + `references/method-6-steps.md` |
| Kiểm tra danh sách chức năng/cây có sẵn (dán văn bản, Excel, Mermaid, spec) | **B. Soát** | `references/review-mode.md`, `mistakes-catalog.md` |
| Có hệ thống đang chạy, cần danh mục chức năng (di chuyển, thay thế, tài liệu hóa) | **C. Dựng ngược** | `references/decomposing-existing-system.md` |
| Hỏi khi nào dùng, dừng ở cấp nào, khác BPMN/WBS/story map thế nào | **D. Giải thích** | `levels-and-depth.md`, `decomposition-vs-others.md`, `naming-guide.md` |

Đối chiếu yêu cầu ↔ chức năng và phân tích tác động khi yêu cầu đổi đều dùng chung spec (`references/traceability.md`).

## Chế độ A: Phân rã (6 bước)

1. **Phạm vi và biên** - mục tiêu 1–2 dòng, `scope.in` / `scope.out`, giả định.
2. **Actor và đối tượng nghiệp vụ** - ai dùng; hệ thống lưu giữ "danh từ" nào cần theo dõi vòng đời (đối tượng nào do hệ thống khác sở hữu thì `source: external`).
3. **Cấp 1: năng lực** - 4–9 module theo năng lực nghiệp vụ, không theo màn hình hay phòng ban; có domain pack thì lấy capability map làm khung.
4. **Cấp 2–3: tính năng → chức năng** - lá là hành động nguyên tử, tên *Động từ + Danh từ*, gắn actor và ưu tiên; qua "hàm test nguyên tử" (`levels-and-depth.md`).
5. **Kiểm MECE, CRUD, xuyên suốt** - mọi đối tượng đủ Tạo/Xem/Sửa/Hủy (hoặc miễn trừ có lý do); có xác thực, thông báo, nhật ký, báo cáo, cấu hình (hoặc miễn trừ).
6. **Truy vết và lint** - gắn `reqs` (chức năng suy ra thì `derived`), chạy `fd_lint.py` tới 0 lỗi, giải thích các cảnh báo còn lại.

Ở mỗi bước, ghi quyết định theo mẫu **Làm gì → Vì sao làm vậy → Vì sao không làm cách khác**.

### Thiếu thông tin thì hỏi gì
Chỉ hỏi khi mô tả chưa nêu (tối đa 4 câu, một lượt): (1) hệ thống thuộc lĩnh vực/mô hình nào và dành cho ai, (2) đâu là ngoài phạm vi, (3) có danh sách yêu cầu hoặc tài liệu nguồn không, (4) mức chi tiết mong muốn (thống nhất phạm vi, ước lượng, hay backlog). Không đủ thì làm theo **giả định ghi rõ** và đừng bịa chức năng.

## Domain knowledge
Nếu hệ thống thuộc lĩnh vực có domain pack - `domain-banking`, `domain-ecommerce` (xem thêm `skills/domain-*`) - nạp pack đó: lấy capability map làm khung cấp 1, đối chiếu `checklist.md` và `business-rules.md` để tìm chức năng bắt buộc mà stakeholder không nhắc, thêm chúng với `derived: true` và `note` bắt đầu bằng `[domain]`, rồi hỏi stakeholder xác nhận. Chưa có pack: hỏi một câu về lĩnh vực hoặc nêu giả định. Chi tiết: `references/domain-integration.md`.

## Đầu ra

Viết **một spec JSON** (định dạng: `references/output-formats.md`, mẫu: `examples/*/spec.json`), rồi sinh mọi định dạng từ đó:

```bash
python3 scripts/fd_lint.py             spec.json                # phải 0 lỗi trước khi giao
python3 scripts/spec_to_table.py       spec.json hierarchy.md   # bảng phân cấp, CRUD, truy vết, Actor × Module
python3 scripts/spec_to_mermaid.py     spec.json diagram.mmd    # vòng nháp; tự giữ ≤ 40 node, --split theo module
python3 scripts/spec_to_svg.py         spec.json diagram.svg    # hình đẹp để chèn tài liệu
python3 scripts/spec_to_csv.py         spec.json tree.csv       # Excel/Sheets; thêm --jira cho Jira
python3 scripts/build_explorer_page.py spec.json explorer.html  # trang lọc theo actor/ưu tiên, xem CRUD, truy vết, lint
python3 scripts/outline_to_spec.py     outline.txt spec.json    # chế độ Soát: dựng spec khung từ danh sách có sẵn
sh scripts/build_all.sh spec.json thu-muc-dau-ra                # chạy tất cả
```

- **Vòng nháp:** bảng + Mermaid để người dùng soát nội dung nhanh.
- **Vòng cuối** (khi đã chốt nội dung): lint 0 lỗi + SVG + explorer; CSV khi cần đưa vào công cụ quản lý.
- Mermaid chỉ vẽ tới độ sâu vừa 40 node; cây lớn dùng `--module` hoặc `--split`.
- Màu SVG/HTML chỉnh trong `assets/svg-theme.css`.

## Báo cáo kèm theo (luôn có)

Theo mẫu `assets/report-template.md`:
- **Phạm vi và giả định.**
- **Bảng tóm tắt**: module → tính năng → chức năng, actor, ưu tiên.
- **Bảng quyết định cấu trúc**: lựa chọn không hiển nhiên, mỗi dòng có "vì sao làm / vì sao không".
- **CRUD và truy vết**: ô thiếu, yêu cầu chưa phủ, chức năng `derived` cần xác nhận.
- **Kết quả lint**: số lỗi/cảnh báo/miễn trừ, đã sửa gì.
- **Danh sách giả định** và **3–5 câu hỏi cho stakeholder**.

## Quy tắc chất lượng
- Phân rã theo **năng lực**, không theo màn hình, phòng ban hay bảng dữ liệu; cây là cấu trúc, không có thứ tự (thứ tự thuộc BPMN).
- Mỗi nút 2–9 con; lá là chức năng nguyên tử, **tên Động từ + Danh từ**, không "Quản lý X".
- ID ổn định `1 / 1.1 / 1.1.1`; không đánh lại số, không tái sử dụng ID đã bỏ.
- Mọi chức năng có nguồn: `reqs`, hoặc `derived: true` kèm lý do. **Không bịa chức năng "nghe hợp lý"**: đưa vào giả định.
- Không bịa giá trị nghiệp vụ (hạn mức, thời hạn): ghi `[xác nhận]`; không khẳng định quy định pháp lý.
- Miễn trừ cảnh báo bằng `waive` kèm lý do; không xóa cảnh báo âm thầm.
- **Dữ liệu nhạy cảm**: nếu người dùng dán dữ liệu thật (tên, số tài khoản), nhắc thay bằng dữ liệu giả.
- Dùng tên chung cho ví dụ; không gắn thương hiệu thật nếu người dùng không yêu cầu.
- Lint chỉ kiểm cấu trúc và thói quen đặt tên (B1, B3, B4, B5 là heuristic, có thể báo oan); việc đúng nghiệp vụ cần người xác nhận.

## Chuỗi skill
Biên bản → yêu cầu (`meeting-to-requirements`) → **phân rã chức năng** → user story + AC (`user-story-writer`) → chất lượng yêu cầu (`requirements-linter`); quy trình chi tiết (`bpmn-modeling`), trạng thái/ERD/context (`ba-diagrams`). Gợi ý bước tiếp theo ở cuối báo cáo.

## Tham chiếu
| File | Nội dung |
|---|---|
| `references/method-6-steps.md` | 6 bước, mỗi bước: câu hỏi, đầu ra, vì sao làm / vì sao không |
| `references/decomposition-rules.md` | Quy tắc nền, checklist 8 điểm, rủi ro khi dùng AI |
| `references/naming-guide.md` | Cách đặt tên: động từ cụ thể, một chức năng một hành vi |
| `references/levels-and-depth.md` | Các cấp, hàm test chức năng nguyên tử, khi nào dừng |
| `references/crud-and-coverage.md` | Ma trận CRUD, miễn trừ hợp lệ, vòng đời, 4 loại ma trận |
| `references/cross-cutting-checklist.md` | Xác thực, thông báo, nhật ký, báo cáo, cấu hình và các nhóm khác |
| `references/decomposition-vs-others.md` | So với BPMN, WBS, capability map, story map, use case |
| `references/mistakes-catalog.md` | Mã lỗi A1–G8: sai / vì sao / sửa, lint có bắt không |
| `references/traceability.md` | Chuỗi yêu cầu → chức năng → story → test, ID ổn định, tác động thay đổi |
| `references/domain-integration.md` | Dùng domain pack ngân hàng/TMĐT; khi chưa có pack |
| `references/decomposing-existing-system.md` | Dựng ngược từ hệ thống đang chạy |
| `references/review-mode.md` | Soát danh sách có sẵn, mức nghiêm trọng, câu hỏi stakeholder |
| `references/output-formats.md` | Spec JSON, outline, các định dạng đầu ra |
| `references/prompt-patterns.md` | Khung prompt 5 phần, vòng Prompt → Lint → Sửa |
| `references/tools.md` | Excel, Jira, Confluence, mermaid.live, Miro… |
| `examples/cafe-pos/` | Tối giản: 6 module, cấp 2 trực tiếp dưới module nhỏ |
| `examples/leave-management/` | Chưa có domain pack: giả định ghi rõ, `waive` có lý do |
| `examples/card-management/` | Domain banking: truy vết yêu cầu, `derived` có nhãn `[domain]` |
| `examples/marketplace-orders/` | Domain e-commerce, 43 chức năng, tách Mermaid theo module |
| `examples/clinic-booking/` | **Đầy đủ**: `walkthrough.md` (6 bước), bản AS-IS có lỗi, `review.md`, bản đã sửa |
| `evals/` | Đề bài kiểm tra chất lượng skill và tiêu chí đạt |
