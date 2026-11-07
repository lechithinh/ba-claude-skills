# Learn: Choosing the Right BA Diagram

A diagram is an answer to a question. Pick the question first, then the notation.

| Stakeholder question | Diagram | BABOK technique |
|---|---|---|
| "Ai làm gì, theo thứ tự nào?" | Process model (BPMN / swimlane) | 10.35 Process Modelling |
| "Người dùng làm được gì với hệ thống?" | Use case diagram | 10.47 Use Cases & Scenarios |
| "Các hệ thống gọi nhau thế nào?" | Sequence diagram | 10.42 Sequence Diagrams |
| "Lưu những dữ liệu gì?" | ERD | 10.15 Data Modelling |
| "Đơn hàng có những trạng thái nào?" | State diagram | 10.44 State Modelling |
| "Phạm vi hệ thống đến đâu?" | Context diagram | 10.41 Scope Modelling |

## Why Mermaid?
- Text-based → versioned in Git, diffable, reviewable in pull requests.
- Renders natively on GitHub, GitLab, Notion, Obsidian and many wikis.
- AI can generate and edit it reliably.

For formal BPMN 2.0 with pools, message flows and events, export to a dedicated tool (Camunda Modeler, draw.io, Visual Paradigm) — Mermaid gives a fast, readable approximation.

## Mẹo
- Vẽ **As-Is** trước, hỏi stakeholder "đau ở đâu?", rồi mới vẽ **To-Be**.
- Mỗi sơ đồ chỉ trả lời **một** câu hỏi. Sơ đồ ôm đồm sẽ không ai đọc.
- Paste code vào https://mermaid.live để xem và xuất PNG/SVG.
