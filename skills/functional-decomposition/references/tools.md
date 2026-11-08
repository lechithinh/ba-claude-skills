# Công cụ đi kèm

| Công cụ | Dùng để | Cách đưa dữ liệu vào |
|---|---|---|
| **Excel / Google Sheets** | Bảng phân cấp, lọc, tính toán, chia sẻ | Mở `tree.csv` (UTF-8). Có sẵn cột ID, Parent ID, Cấp, Actor, Ưu tiên, Yêu cầu |
| **Jira** | Đưa chức năng thành Epic/Story | `tree-jira.csv`; trong màn hình import CSV, map `Issue Id`, `Parent`, `Issue Type`, `Summary`. Kiểm tra phiên bản và quyền của Jira bạn đang dùng |
| **Confluence / Notion / GitHub** | Tài liệu sống | Dán bảng Markdown; Mermaid dùng macro/khối code (tuỳ nền tảng) |
| **mermaid.live** | Xem và xuất PNG/SVG sơ đồ Mermaid | Dán nội dung `.mmd` |
| **draw.io / diagrams.net** | Sơ đồ vẽ tay, trình bày | Chèn Mermaid hoặc nhập SVG |
| **Miro, XMind** (mind map) | Workshop phân rã cùng stakeholder trước khi chuẩn hóa | Dán outline văn bản; sau workshop dùng `outline_to_spec.py` để đưa lại vào spec |

Gợi ý quy trình: **workshop trên bảng trắng/mind map → outline → `outline_to_spec.py` → bổ sung đối tượng, yêu cầu → lint → đầu ra → CSV vào công cụ quản lý.**

Tên công cụ trên thuộc chủ sở hữu tương ứng và chỉ được nhắc để nêu khả năng tương thích; skill không kèm mã của họ. Giao diện công cụ thay đổi theo thời gian: kiểm tra lại khi dùng.
