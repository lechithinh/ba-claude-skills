---
title: "Bộ Skill Claude cho Business Analyst: Phân tích yêu cầu, User Story, Sơ đồ & Nghiệp vụ"
description: "Bộ skill Claude miễn phí, mã nguồn mở cho BA: phân tích và kiểm tra chất lượng yêu cầu, viết user story kèm acceptance criteria Gherkin, phân rã chức năng, vẽ sơ đồ BPMN/UML bằng Mermaid, kèm kiến thức nghiệp vụ Ngân hàng và Thương mại điện tử."
lang: vi
alt_lang: en
alt_url: /
hide_title: true
---

<div class="hero">
  <img src="{{ '/assets/banner.png' | relative_url }}" alt="Bộ skill Claude cho Business Analyst — phân tích yêu cầu, user story, sơ đồ, nghiệp vụ ngân hàng và thương mại điện tử">
  <h1>Bộ Skill Claude cho Business Analyst</h1>
  <p class="lead">Skill Claude mã nguồn mở làm việc như một BA lâu năm: phân tích yêu cầu, viết user story kèm acceptance criteria, phân rã chức năng, vẽ sơ đồ BPMN/UML, <b>cùng kiến thức nghiệp vụ Ngân hàng và Thương mại điện tử</b>.</p>
  <a class="btn primary" href="https://github.com/lechithinh/ba-claude-skills">★ Xem trên GitHub</a>
  <a class="btn" href="#bat-dau-nhanh">Bắt đầu nhanh</a>
  <a class="btn" href="{{ '/' | relative_url }}">English</a>
</div>

## Bắt đầu nhanh {#bat-dau-nhanh}

Trong Claude Code:

```bash
/plugin marketplace add lechithinh/ba-claude-skills
/plugin install ba-claude-skills@ba-claude-skills
```

Sau đó mô tả công việc kèm bối cảnh nghiệp vụ, ví dụ: *"Viết user story kèm acceptance criteria cho chức năng chuyển tiền liên ngân hàng trên mobile banking."* Nếu dùng Claude.ai, hãy tải file zip ở [Releases](https://github.com/lechithinh/ba-claude-skills/releases) rồi upload tại **Settings → Capabilities → Skills**.

## Vì sao kiến thức nghiệp vụ quan trọng

AI đã biết *cách viết* yêu cầu. BA lâu năm biết **cần hỏi gì** trong từng ngành. Với cùng prompt *"user story chuyển tiền liên ngân hàng"*, AI không có bối cảnh chỉ ra 2 kịch bản: thành công và không đủ số dư. Có domain pack ngân hàng, bạn nhận 7 kịch bản: truy vấn tên người thụ hưởng, hạn mức, xác thực sinh trắc học khi vượt ngưỡng, **timeout → đang xử lý → đối soát**, chống trùng giao dịch, phí, kèm câu hỏi mở cho Compliance.

[Xem ví dụ so sánh đầy đủ →]({{ '/examples/domain-showcase/' | relative_url }})

## Skill phương pháp {#skill}

<div class="cards">
  <div class="card"><h3><a href="{{ '/learn/meeting-to-requirements' | relative_url }}">Trích xuất yêu cầu từ biên bản họp</a></h3><p>Biên bản thành mục tiêu, yêu cầu chức năng và phi chức năng, business rule, câu hỏi mở, có trích dẫn nguồn.</p></div>
  <div class="card"><h3><a href="{{ '/learn/requirements-linter' | relative_url }}">Kiểm tra chất lượng yêu cầu</a></h3><p>Chấm điểm 0–10, phát hiện yêu cầu mơ hồ, không kiểm thử được, gộp nhiều ý, thiếu kịch bản nghiệp vụ, rồi đề xuất viết lại.</p></div>
  <div class="card"><h3><a href="{{ '/learn/functional-decomposition' | relative_url }}">Phân rã chức năng</a></h3><p>Hệ thống → module → tính năng → chức năng, kèm sơ đồ cây và kiểm tra CRUD.</p></div>
  <div class="card"><h3><a href="{{ '/learn/user-story-writer' | relative_url }}">Viết user story</a></h3><p>User story chuẩn INVEST, acceptance criteria Gherkin có kịch bản lỗi, xuất CSV cho Jira.</p></div>
  <div class="card"><h3><a href="{{ '/learn/ba-diagrams' | relative_url }}">Vẽ sơ đồ cho BA</a></h3><p>Sơ đồ quy trình swimlane, use case, sequence, ERD, trạng thái, context bằng Mermaid.</p></div>
</div>

## Domain pack {#domain}

<div class="cards">
  <div class="card"><h3><a href="{{ '/domains/banking/' | relative_url }}">🏦 Ngân hàng</a></h3><p>eKYC, tài khoản, chuyển tiền (NAPAS, CITAD), thẻ, cho vay, tiền gửi, tra soát: rule, checklist, data model, tích hợp, pháp lý, KPI.</p></div>
  <div class="card"><h3><a href="{{ '/domains/ecommerce/' | relative_url }}">🛒 Thương mại điện tử</a></h3><p>Danh mục, voucher, checkout, thanh toán, đơn hàng, vận chuyển và COD, đổi trả, đối soát seller: rule, checklist, data model, tích hợp, pháp lý, KPI.</p></div>
</div>

## Học kỹ thuật BA {#hoc}

- [Thuật ngữ ngân hàng Anh–Việt cho BA]({{ '/domains/banking/glossary' | relative_url }})
- [Câu hỏi BA ngân hàng phải hỏi stakeholder]({{ '/domains/banking/checklist' | relative_url }})
- [Thuật ngữ thương mại điện tử Anh–Việt]({{ '/domains/ecommerce/glossary' | relative_url }})
- [Câu hỏi BA thương mại điện tử phải hỏi]({{ '/domains/ecommerce/checklist' | relative_url }})
- [Phân rã chức năng là gì, khi nào dùng]({{ '/learn/functional-decomposition' | relative_url }})
- [Cách viết user story và acceptance criteria Gherkin]({{ '/learn/user-story-writer' | relative_url }})
- [Checklist chất lượng yêu cầu]({{ '/learn/requirements-linter' | relative_url }})
- [Chọn đúng loại sơ đồ cho BA]({{ '/learn/ba-diagrams' | relative_url }})
- [Case study: app đặt lịch phòng khám, từ biên bản họp đến user story]({{ '/examples/clinic-booking/' | relative_url }})

## Câu hỏi thường gặp

**Có miễn phí không?** Có. Repo mã nguồn mở, giấy phép MIT.

**Skill có tự bịa business rule không?** Không. Giá trị chưa biết được để dạng `[giá trị — xác nhận]`, kèm danh sách câu hỏi mở.

**Dùng tiếng Việt được không?** Được. Skill trả lời theo ngôn ngữ bạn dùng.

**Tôi đóng góp domain mới được không?** Được. Xem [hướng dẫn đóng góp](https://github.com/lechithinh/ba-claude-skills/blob/main/CONTRIBUTING.md).
