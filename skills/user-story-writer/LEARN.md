# Learn: User Stories & Acceptance Criteria

## The format
> **As a** <role> **I want** <goal> **so that** <value>

The "so that" is the most skipped and most important part — it tells the team *why*, which enables better solutions.

## INVEST
| Letter | Meaning | Quick test |
|---|---|---|
| I | Independent | Can it be delivered without another story in the same sprint? |
| N | Negotiable | Is the "how" still open for discussion? |
| V | Valuable | Would a user or the business notice it? |
| E | Estimable | Can the team size it? |
| S | Small | Fits in a sprint (ideally a few days)? |
| T | Testable | Are there clear acceptance criteria? |

## Gherkin acceptance criteria
```gherkin
Scenario: <short name>
  Given <context / precondition>
  When <action>
  Then <observable outcome>
```
Why Gherkin? It is readable by business people **and** can be automated by QA (Cucumber, SpecFlow, Behave).

## Splitting patterns
Workflow steps · Business rule variations · Happy / unhappy path · CRUD operations · Data variations · Platforms/interfaces · Defer performance.

## Lỗi thường gặp của BA mới
- Viết role chung chung là "user".
- Viết story như task kỹ thuật: "Tạo bảng database bookings".
- Chỉ có happy path, thiếu kịch bản lỗi.
- AC mô tả giao diện quá chi tiết làm mất tính "Negotiable".

## Practice
Take one feature from your functional decomposition and ask Claude: *"Viết user story kèm Gherkin AC cho chức năng 1.1."* Then try splitting the largest story with two different patterns.
