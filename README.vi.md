<div align="center">

# 🧩 BA Claude Skills

**Từ biên bản họp đến yêu cầu, user story và sơ đồ — bộ skill Claude dành cho Business Analyst.**

Theo chuẩn BABOK · Tiếng Việt & English · Dùng được trên Claude Code, Claude.ai và các AI agent khác

[![GitHub stars](https://img.shields.io/github/stars/lechithinh/ba-claude-skills?style=social)](https://github.com/lechithinh/ba-claude-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-5-blue)](#-danh-sách-skill)

[English](README.md) · **Tiếng Việt**

</div>

---

## Vì sao có repo này?

Prompt chung chung cho ra kết quả BA chung chung: yêu cầu mơ hồ, user story chỉ có happy path, sơ đồ Mermaid lỗi không hiển thị. Các skill trong repo này đóng gói **cách một BA nhiều kinh nghiệm thực sự làm việc** — checklist, cấu trúc, câu hỏi cần đặt ra — để Claude tạo ra tài liệu đủ chất lượng đưa cho stakeholder.

| Prompt thông thường | Với BA Claude Skills |
|---|---|
| "Hệ thống phải nhanh và dễ dùng." ✅ nhìn có vẻ ổn | ❌ Bị đánh dấu: *mơ hồ (nhanh, dễ dùng), không kiểm thử được, gộp 2 yêu cầu* → viết lại thành 2 NFR đo được + câu hỏi cho stakeholder |
| Một danh sách tính năng | **Sơ đồ phân rã chức năng** đánh số, kèm bảng CRUD phát hiện chức năng bị thiếu |
| User story chỉ có happy path | Story đạt **INVEST**, acceptance criteria dạng **Gherkin**, có kịch bản lỗi và truy vết business rule |

## 🧰 Danh sách skill

| Skill | Chức năng | Thử nói |
|---|---|---|
| [**meeting-to-requirements**](skills/meeting-to-requirements/SKILL.md) | Biên bản họp → mục tiêu, FR, NFR, business rule, câu hỏi mở, action item — mỗi mục có trích dẫn nguồn | *"Trích xuất yêu cầu từ biên bản họp này"* |
| [**requirements-linter**](skills/requirements-linter/SKILL.md) ⭐ | Chấm điểm từng yêu cầu, phát hiện từ mơ hồ / không kiểm thử được / yêu cầu gộp, đề xuất viết lại | *"Kiểm tra chất lượng các yêu cầu này"* |
| [**functional-decomposition**](skills/functional-decomposition/SKILL.md) | Hệ thống → module → tính năng → chức năng, sơ đồ cây Mermaid, kiểm tra CRUD | *"Phân rã chức năng app đặt lịch khám"* |
| [**user-story-writer**](skills/user-story-writer/SKILL.md) | User story chuẩn INVEST + AC Gherkin, tách story, xuất CSV cho Jira | *"Viết user story cho chức năng 1.1"* |
| [**ba-diagrams**](skills/ba-diagrams/SKILL.md) | Chọn đúng loại sơ đồ và vẽ bằng Mermaid: quy trình swimlane, use case, sequence, ERD, state, context | *"Vẽ quy trình đặt lịch To-Be dạng swimlane"* |

Mỗi skill đi kèm file **`LEARN.md`** giải thích kỹ thuật BA phía sau (tham chiếu BABOK, lỗi thường gặp, bài tập thực hành).

## 🔗 Ví dụ xuyên suốt

Xem case study đầy đủ tại [`examples/clinic-booking`](examples/clinic-booking/README.md) — từ biên bản họp tiếng Việt đến yêu cầu, báo cáo chất lượng, phân rã chức năng, user story và sơ đồ.

## 🚀 Cài đặt

### Claude Code (khuyến nghị)
```bash
/plugin marketplace add lechithinh/ba-claude-skills
/plugin install ba-claude-skills@ba-claude-skills
```
Sau đó chỉ cần mô tả công việc — Claude tự động dùng skill phù hợp.

### Cài thủ công
```bash
git clone https://github.com/lechithinh/ba-claude-skills.git
cp -r ba-claude-skills/skills/* ~/.claude/skills/
```

### Claude.ai
1. Tải file zip của skill trong mục [Releases](https://github.com/lechithinh/ba-claude-skills/releases) (hoặc tự nén một thư mục trong `skills/`).
2. Vào **Settings → Capabilities → Skills** trên Claude.ai và upload file zip.

### AI agent khác (Cursor, Codex, Gemini CLI…)
Mỗi `SKILL.md` là Markdown thuần. Trỏ agent tới [`AGENTS.md`](AGENTS.md) hoặc dán nội dung skill vào rules của dự án.

## 🗺️ Lộ trình

Sắp xếp theo knowledge area của BABOK — xem [ROADMAP.md](ROADMAP.md). Sắp có: stakeholder map, phân tích quy trình As-Is/To-Be, gap analysis, checklist NFR, ma trận truy vết, sinh test case UAT, viết BRD/SRS.

👉 Muốn có skill mới? [Gửi đề xuất](https://github.com/lechithinh/ba-claude-skills/issues/new?template=skill_request.md).

## 🤝 Đóng góp

Chào đón BA, PO, QA cùng đóng góp! Đọc [CONTRIBUTING.md](CONTRIBUTING.md) và bắt đầu từ [`templates/SKILL_TEMPLATE.md`](templates/SKILL_TEMPLATE.md).

## 👤 Tác giả

**[Lê Chí Thịnh](https://github.com/lechithinh)** — Business Analyst chia sẻ quy trình làm BA cùng AI.

Nếu repo giúp bạn tiết kiệm thời gian, hãy ⭐ **star** để nhiều BA khác tìm thấy.

## Giấy phép

[MIT](LICENSE)
