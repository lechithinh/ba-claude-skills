---
name: domain-banking
description: Retail banking domain knowledge for Business Analysts — glossary, core processes (eKYC onboarding, accounts, fund transfers, cards, lending, deposits, disputes), common business rules (limits, cut-off, threshold-based authentication, maker-checker, reconciliation), data model, integrations (core banking, NAPAS, CITAD, AML, CIC), Vietnamese regulations and a BA question checklist. Use together with any BA task (requirements, user stories, linting, decomposition, diagrams, API/test design) whenever the context is a bank, digital banking, mobile banking, internet banking, core banking, payments inside a bank, cards or loans — or the user mentions "ngân hàng", "chuyển tiền", "mở tài khoản", "eKYC", "thẻ tín dụng", "khoản vay", "tiền gửi", "tra soát", "NAPAS", "CIF".
---

# Domain Pack: Retail Banking / Ngân hàng bán lẻ

This skill adds **domain knowledge** on top of the BA method skills (`meeting-to-requirements`, `requirements-linter`, `functional-decomposition`, `user-story-writer`, `ba-diagrams`). It does not replace them — it makes their output *banking-correct*.

## How to use the references
Read only the file(s) you need for the current task:

| Task | Read |
|---|---|
| Understand or explain terms; write in proper bank terminology | `references/glossary.md` |
| Decompose functions, draw processes, find missing steps | `references/processes.md` |
| Write/lint requirements, user stories, acceptance criteria | `references/business-rules.md` + `references/checklist.md` |
| ERD, data dictionary, API payloads | `references/data-model.md` |
| Context diagrams, sequence diagrams, integration/API specs | `references/integrations.md` |
| Compliance, NFRs, security, audit | `references/regulations.md` |
| Business goals, reports, success metrics | `references/kpis.md` |

## How to apply domain knowledge
1. **Add the scenarios a banking BA would never forget**: limits, threshold-based authentication, cut-off/holidays, timeout & pending status, reversal, reconciliation, duplicate prevention, maker-checker, audit trail, AML screening.
2. **Ask domain questions, don't invent answers.** Every bank configures limits, fees and products differently. Put unknown values as `[value — confirm with bank policy]` and add the question to the open-questions list.
3. **Use the bank's vocabulary**: CIF, CASA, value date, cut-off, beneficiary, maker/checker, posting, reversal, reconciliation. Provide Vietnamese equivalents when replying in Vietnamese.
4. **Flag regulatory touchpoints** (identity verification, biometric authentication thresholds, data protection, AML) but **never state a regulation as final** — always add: *"verify against the current version of the regulation and the bank's compliance team"*.
5. **Separate business rules from requirements**: limits, fees, cut-off times and thresholds are *configurable parameters*, not hard-coded requirements. Recommend a parameter/config requirement.

## Guardrails
- Knowledge here is generic to retail banking (with a Vietnam focus). Individual banks differ — present it as *typical practice*, not the bank's truth.
- Regulations change. `references/regulations.md` has a "last reviewed" date; mention it when citing.
- Never include real customer data, account numbers or card numbers in examples; use masked values (`9704 **** **** 1234`).
