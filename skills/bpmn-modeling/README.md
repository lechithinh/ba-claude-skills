# BPMN Modeling Skill

Mô hình hoá quy trình nghiệp vụ bằng BPMN 2.0 (chuẩn OMG): từ mô tả bằng lời → bản nháp Mermaid → file `.bpmn` có toạ độ → SVG → trang HTML chạy token theo kịch bản. Mỗi lựa chọn ký hiệu đi kèm lý do, và sơ đồ được kiểm chứng bằng lint + mô phỏng token trước khi giao.

## Làm được gì
- **Vẽ** quy trình mới theo 6 bước (phạm vi → swimlane → happy path → gateway → ngoại lệ → review bằng token), giải thích "vì sao dùng / vì sao không" cho từng ký hiệu.
- **AS-IS → TO-BE**: tìm pain point bằng token (kịch bản bị kẹt), đề xuất TO-BE và Gap Analysis.
- **Soát** sơ đồ có sẵn theo danh mục 22 lỗi sai, kèm mã lỗi và cách sửa.
- **Giải thích** nên dùng ký hiệu nào cho tình huống nào, pool hay lane.
- Xuất **Mermaid, `.bpmn`** (bpmn.io, draw.io, Camunda Modeler), **SVG** và **trang token HTML** từ cùng một spec JSON.

## Ví dụ câu lệnh
- "Vẽ BPMN luồng đặt đồ ăn online có thanh toán lỗi và nhắc quán sau 15 phút."
- "Đây là quy trình duyệt vay AS-IS, đề xuất TO-BE và Gap Analysis."
- "Soát giúp tôi sơ đồ BPMN này (dán Mermaid/XML)."
- "Khách không thanh toán trong 10 phút thì huỷ: dùng timer hay gateway?"
- "Chạy thử các kịch bản của quy trình này, kịch bản nào bị kẹt?"

## Cấu trúc
```
bpmn-modeling/
├── SKILL.md                    # điều phối: chế độ, 6 bước, đầu ra, báo cáo, quy tắc chất lượng
├── README.md
├── references/
│   ├── method-6-steps.md       # 6 bước + vì sao dùng / vì sao không
│   ├── notation-core.md        # ký hiệu cốt lõi, mỗi ký hiệu có "Dùng khi"
│   ├── notation-advanced.md    # ký hiệu ít gặp
│   ├── symbol-decisions.md     # tình huống → ký hiệu → vì sao không dùng cách khác
│   ├── pool-vs-lane.md
│   ├── mistakes-catalog.md     # 22 lỗi sai A1–D4
│   ├── token-review.md         # review bằng token, từ lỗ hổng tới TO-BE
│   ├── modeling-rules.md       # quy tắc nền, checklist 8 điểm, rủi ro khi dùng AI
│   ├── output-formats.md       # spec JSON, Mermaid, XML, SVG, trang token
│   └── prompt-patterns.md, as-is-to-be.md, review-mode.md, tools.md
├── scripts/                    # chỉ cần Python 3, không cài thêm thư viện
│   ├── spec_to_mermaid.py      # JSON -> Mermaid
│   ├── spec_to_bpmn.py         # JSON -> BPMN 2.0 XML (có BPMNDiagram, pool ngoài, message flow)
│   ├── bpmn_lint.py            # kiểm tra quy tắc trên file .bpmn
│   ├── spec_to_svg.py          # JSON -> SVG
│   ├── simulate_tokens.py      # chạy token theo kịch bản, báo kẹt / nhánh chưa phủ
│   └── build_token_page.py     # JSON -> trang HTML có animation token
├── assets/
│   ├── svg-theme.css           # màu, font cho SVG/HTML (đổi theo thương hiệu)
│   ├── token-player.js         # engine animation token
│   └── report-template.md      # mẫu báo cáo giao kèm sơ đồ
├── examples/                   # cinema-ticketing, ride-hailing, food-delivery, counter-order, ekyc
└── evals/                      # đề bài + tiêu chí đạt để kiểm tra chất lượng skill
```

## Bắt đầu nhanh
```bash
python3 scripts/spec_to_svg.py      examples/cinema-ticketing/spec.json cinema.svg
python3 scripts/simulate_tokens.py  examples/cinema-ticketing/spec.json
python3 scripts/build_token_page.py examples/cinema-ticketing/spec.json cinema.html
```

## Giới hạn
- Bố cục tự động là bản nháp: đường nối có thể chồng nhau khi có boundary event hoặc nhiều nhánh; kéo chỉnh trong bpmn.io là xong (nội dung và logic không đổi).
- Process chính là một pool nhiều lane; các bên khác là pool thu gọn nối bằng message flow. Muốn vẽ chi tiết bên trong nhiều pool, sửa tiếp trong bpmn.io.
- Mô phỏng token kiểm tra cấu trúc luồng (kẹt, nhánh cụt, AND thiếu nhánh), không thay thế việc người vận hành xác nhận nghiệp vụ.
- AI chỉ phác thảo - nghiệp vụ phải được người vận hành quy trình xác nhận.

## Nguồn kiến thức
Đặc tả BPMN 2.0 của OMG (Object Management Group) và các thực hành mô hình hoá quy trình phổ biến cho Business Analyst. Các khuyến nghị riêng của skill (ví dụ ưu tiên send/receive task thay cho message event) được ghi rõ là khuyến nghị, không phải quy tắc bắt buộc của chuẩn.

## Bản quyền & ghi công
- **Tác giả:** Lê Chí Thịnh. Giấy phép **MIT** theo [LICENSE](../../LICENSE) của repo.
- **Nội dung do tác giả viết:** hướng dẫn, danh mục 22 lỗi sai, checklist, ví dụ, script Python, `token-player.js` và `svg-theme.css`. Các khái niệm BPMN được diễn đạt lại bằng lời riêng, không sao chép nguyên văn đặc tả OMG hay sách/tài liệu của bên khác.
- **Nhãn hiệu:** BPMN™ là nhãn hiệu của Object Management Group (OMG). Dự án này độc lập, không liên kết hay được OMG bảo trợ. "BPMN 2.0" chỉ dùng để nêu chuẩn mà file xuất ra hướng tới tuân theo.
- **Công cụ bên thứ ba** (bpmn.io, draw.io, Camunda Modeler, Lucidchart, Miro, Visual Paradigm, SAP Signavio) thuộc chủ sở hữu tương ứng; chỉ được nhắc để người dùng biết khả năng tương thích. Skill không kèm mã nguồn của các công cụ đó.
- **Font:** `svg-theme.css` chỉ *khai báo* Be Vietnam Pro, Inter, JetBrains Mono, không đóng gói file font. Nếu bạn nhúng hoặc phân phối file font, hãy kiểm tra giấy phép của từng font.
- **Ví dụ:** dùng tên chung, không gắn thương hiệu hay dữ liệu của doanh nghiệp thật.
