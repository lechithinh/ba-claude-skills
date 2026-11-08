---
name: domain-lending
description: Consumer lending domain knowledge for Business Analysts - glossary, core processes (origination, eKYC, credit assessment and decisioning, offer and e-contract, disbursement, repayment schedule, collections by days-past-due, early repayment, restructuring, closure), business rules (eligibility, interest and repayment calculation methods, repayment allocation order, schedule recalculation, DPD buckets, approval authority), data model with status sets, integrations (credit bureau CIC, eKYC, core/ledger, auto-debit, e-sign, scoring), regulatory touchpoints and a BA question checklist. Use together with any BA task whenever the context is consumer loans, personal loans, buy-now-pay-later, installment, finance company, loan origination system (LOS), loan management system (LMS) or collections - or the user mentions "cho vay", "khoản vay", "vay tiêu dùng", "trả góp", "BNPL", "thẩm định", "giải ngân", "nợ quá hạn", "thu hồi nợ", "lãi suất", "CIC".
---

# Domain Pack: Consumer Lending / Cho vay tiêu dùng

This skill adds **domain knowledge** on top of the BA method skills (`meeting-to-requirements`, `requirements-linter`, `functional-decomposition`, `user-story-writer`, `decision-table`, `edge-case-finder`, `api-spec`, `screen-spec`, `bpmn-modeling`, `ba-diagrams`). It makes their output *lending-correct*. It focuses on **retail/consumer loans** (personal loan, BNPL, installment); corporate lending is out of scope. For the bank around the loan (accounts, transfers) also load `domain-banking`.

## How to use the references
| Task | Read |
|---|---|
| Terminology | `references/glossary.md` |
| Decompose functions, draw processes | `references/processes.md` |
| Requirements, stories, AC, **decision tables** (approval, allocation) | `references/business-rules.md` + `references/checklist.md` |
| ERD, API payloads, status sets | `references/data-model.md` |
| Context/sequence diagrams, integration specs | `references/integrations.md` |
| Compliance | `references/regulations.md` |
| Goals, reports | `references/kpis.md` |

## How to apply domain knowledge
1. **Identify the product**: cash loan, installment at point of sale, BNPL, credit line; secured or unsecured; own funds or partner funded. It changes the process and the rules.
2. **Add the scenarios a lending BA never forgets**: **interest method** (flat vs reducing balance) and how it is disclosed, repayment allocation order, due date on a holiday, partial and early repayment recalculation, failed auto-debit retries, DPD buckets and collection actions, restructuring, loan after eKYC mismatch or fraud, cooling-off or cancellation, manual review fallback.
3. **Separate decision logic from workflow**: eligibility, approval authority and allocation are rules (use `decision-table`), not flow.
4. **Ask, don't invent**: rates, fees, limits and cut-offs are product and risk decisions -> `[value - confirm]`.
5. **Flag regulatory touchpoints** (rate and fee disclosure, consumer protection, credit reporting, provisioning, data protection) with *"verify the current regulation with Compliance/Legal"*.

## Guardrails
- Generic typical practice (Vietnam focus); each lender differs. Never state an interest cap or legal threshold as fact.
- `references/regulations.md` has a "last reviewed" date and lists topics to ask about, not legal conclusions.
- Use masked values for ID numbers, phone numbers and incomes in examples.
