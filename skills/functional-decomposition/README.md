# Functional Decomposition Skill (Phân rã chức năng)

Biến mô tả hệ thống, biên bản họp, BRD hoặc hệ thống có sẵn thành **cây chức năng** (hệ thống → module → tính năng → chức năng) với ID ổn định, actor, ưu tiên và truy vết yêu cầu. Cây được kiểm chứng bằng lint (MECE, CRUD, chức năng xuyên suốt, truy vết) trước khi giao, và xuất ra bảng, Mermaid, SVG, CSV/Jira, trang HTML khám phá. Kết hợp được với domain pack ngân hàng và thương mại điện tử.

## Làm được gì
- **Phân rã** hệ thống mới theo 6 bước (phạm vi → actor và đối tượng → năng lực → chức năng → kiểm MECE/CRUD → truy vết và lint), giải thích "vì sao làm / vì sao không".
- **Soát** danh sách chức năng có sẵn (dán văn bản hoặc Excel): dựng spec khung, chạy lint, chỉ ra lỗi theo mã, thiếu sót và 5 câu hỏi cho stakeholder.
- **Dựng ngược** danh mục chức năng từ hệ thống đang chạy (menu, API, job, bảng dữ liệu), chỉ ra chức năng nghi đã chết hoặc trùng lặp.
- **Đối chiếu** yêu cầu ↔ chức năng: yêu cầu nào chưa được phủ, chức năng nào chưa có nguồn; phân tích tác động khi yêu cầu đổi.
- **Giải thích**: khi nào dùng, dừng ở cấp nào, khác BPMN/WBS/story map thế nào.
- Xuất **bảng Markdown, Mermaid, SVG, CSV (Excel/Jira) và trang explorer** từ cùng một spec JSON.

## Ví dụ câu lệnh
- "Phân rã chức năng cho app đặt lịch phòng khám; ngoài phạm vi: thanh toán đặt cọc."
- "Phân rã tính năng chuyển tiền liên ngân hàng trên mobile banking." (nạp `domain-banking`)
- "Soát giúp mình danh sách chức năng này [dán]; đối tượng chính: khách hàng, đơn hàng."
- "Đây là menu hệ thống kế toán cũ [dán]; dựng danh mục chức năng và chỉ ra chức năng nghi đã chết."
- "Đối chiếu danh sách yêu cầu R1–R8 với cây chức năng: yêu cầu nào chưa được phủ?"
- "Nên dừng phân rã ở cấp nào? Khác sơ đồ quy trình thế nào?"

## Cấu trúc
```
functional-decomposition/
├── SKILL.md                      # điều phối: chế độ, 6 bước, đầu ra, báo cáo, quy tắc chất lượng
├── README.md, LEARN.md
├── references/
│   ├── method-6-steps.md         # 6 bước + vì sao làm / vì sao không
│   ├── decomposition-rules.md    # quy tắc nền, checklist 8 điểm, rủi ro khi dùng AI
│   ├── naming-guide.md, levels-and-depth.md, crud-and-coverage.md
│   ├── cross-cutting-checklist.md, decomposition-vs-others.md
│   ├── mistakes-catalog.md       # mã lỗi A1–G8, lint có bắt không
│   ├── traceability.md, domain-integration.md, decomposing-existing-system.md
│   └── review-mode.md, output-formats.md, prompt-patterns.md, tools.md
├── scripts/                      # chỉ cần Python 3, không cài thêm thư viện
│   ├── fd_lint.py                # kiểm tra spec (mã A1–F1), thoát 1 nếu có LỖI
│   ├── spec_to_table.py          # bảng phân cấp, CRUD, truy vết, Actor × Module
│   ├── spec_to_mermaid.py        # sơ đồ cây, tự giữ ≤ 40 node, --split theo module
│   ├── spec_to_svg.py            # cây SVG, màu theo module, chấm ưu tiên
│   ├── spec_to_csv.py            # CSV cho Excel, hoặc --jira
│   ├── build_explorer_page.py    # trang HTML: lọc, CRUD, truy vết, lint
│   ├── outline_to_spec.py        # outline văn bản → spec khung (chế độ Soát)
│   ├── build_all.sh, fdlib.py
├── assets/
│   ├── svg-theme.css             # màu, font (đổi theo thương hiệu; có chế độ tối)
│   ├── explorer.js               # engine trang explorer
│   └── report-template.md        # mẫu báo cáo giao kèm cây
├── examples/                     # cafe-pos, leave-management, card-management, marketplace-orders, clinic-booking
└── evals/                        # 10 đề bài + tiêu chí đạt
```

## Bắt đầu nhanh
```bash
python3 scripts/fd_lint.py             examples/clinic-booking/spec.json
python3 scripts/spec_to_svg.py         examples/clinic-booking/spec.json clinic.svg
python3 scripts/build_explorer_page.py examples/clinic-booking/spec.json clinic.html
python3 scripts/fd_lint.py             examples/clinic-booking/spec-asis.json   # xem lint bắt lỗi
```
Mở `clinic.html` bằng trình duyệt để lọc cây theo actor, ưu tiên và xem ma trận CRUD.

## Giới hạn
- **Lint chỉ kiểm cấu trúc và thói quen đặt tên.** B1, B3, B4, B5 là heuristic: có thể báo oan, có thể bỏ sót (ví dụ hai tên ngắn trùng việc). Việc đúng nghiệp vụ cần người làm nghiệp vụ xác nhận.
- Danh sách động từ của lint là tiếng Việt và tiếng Anh thông dụng; động từ hiếm có thể bị báo B1. Thêm vào `extra_verbs` trong spec.
- Chức năng `derived` từ domain pack là **gợi ý cần xác nhận**, không phải phạm vi đã chốt.
- SVG tự bố cục: cây rất lớn nên dùng `--depth` hoặc `--module`. CSV Jira chỉ là điểm khởi đầu, kiểm tra mapping khi import.
- AI chỉ phác thảo: cây phải được người nghiệp vụ và người kỹ thuật xác nhận.

## Bản quyền & ghi công
- **Tác giả:** Lê Chí Thịnh. Giấy phép **MIT** theo [LICENSE](../../LICENSE) của repo.
- **Nội dung do tác giả viết:** hướng dẫn, danh mục mã lỗi, checklist, ví dụ, script Python, `explorer.js` và `svg-theme.css`. Khái niệm phân rã chức năng được diễn đạt lại bằng lời riêng, không sao chép nguyên văn sách hay tài liệu của bên khác.
- **Thương hiệu:** BABOK® là nhãn hiệu của IIBA; BPMN™ là nhãn hiệu của OMG. Dự án này độc lập, không liên kết hay được các tổ chức đó bảo trợ. Tên "Functional Decomposition" chỉ dùng để gọi một kỹ thuật phân tích nghiệp vụ phổ biến.
- **Công cụ bên thứ ba** (Excel, Jira, Confluence, Miro, draw.io, mermaid.live…) thuộc chủ sở hữu tương ứng; chỉ được nhắc để nêu khả năng tương thích, không kèm mã của họ. Trang explorer không tải thư viện hay font từ bên ngoài.
- **Font:** `svg-theme.css` chỉ *khai báo* Be Vietnam Pro, Inter; không đóng gói file font.
- **Ví dụ:** dùng tên chung, không gắn thương hiệu hay dữ liệu của doanh nghiệp thật.
