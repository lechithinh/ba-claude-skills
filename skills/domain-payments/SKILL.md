---
name: domain-payments
description: Payments and e-wallet domain knowledge for Business Analysts - glossary, core processes (merchant onboarding, wallet and KYC levels, top-up, withdrawal, P2P, online/QR payment, refund and chargeback, settlement, reconciliation), business rules (wallet limits by KYC level, authorize/capture, callback as source of truth, idempotency, three-way reconciliation, fees), data model with status sets, integrations (banks, NAPAS/QR, card schemes, PSP, KYC, AML), regulatory touchpoints and a BA question checklist. Use together with any BA task whenever the context is e-wallet, payment gateway, payment service provider, QR payment, top-up, withdrawal, merchant acquiring, settlement or reconciliation - or the user mentions "ví điện tử", "cổng thanh toán", "thanh toán QR", "nạp tiền", "rút tiền", "đối soát", "chargeback", "merchant", "PSP", "trung gian thanh toán".
---

# Domain Pack: Payments & E-wallet / Thanh toán và ví điện tử

This skill adds **domain knowledge** on top of the BA method skills (`meeting-to-requirements`, `requirements-linter`, `functional-decomposition`, `user-story-writer`, `decision-table`, `edge-case-finder`, `api-spec`, `screen-spec`, `bpmn-modeling`, `ba-diagrams`). It makes their output *payments-correct*. For bank-owned products (accounts, transfers, cards) also load `domain-banking`.

## How to use the references
| Task | Read |
|---|---|
| Terminology | `references/glossary.md` |
| Decompose functions, draw processes | `references/processes.md` |
| Requirements, stories, AC, decision tables | `references/business-rules.md` + `references/checklist.md` |
| ERD, API payloads, status sets | `references/data-model.md` |
| Context/sequence diagrams, integration specs | `references/integrations.md` |
| Compliance, security | `references/regulations.md` |
| Goals, reports | `references/kpis.md` |

## How to apply domain knowledge
1. **Identify the role first**: wallet issuer, payment gateway/PSP, acquirer, merchant, or a bank channel. It changes almost every rule.
2. **Add the scenarios a payments BA never forgets**: **callback lost or late**, timeout then pending, duplicate request, partial refund, refund after settlement, chargeback window, reconciliation mismatch, wallet limit by KYC level, negative balance prevention, concurrent debits.
3. **Money first, UI second**: define ledger movements and statuses before screens.
4. **Ask, don't invent**: limits, fees, settlement cycles and windows are business or partner decisions -> `[value - confirm]`.
5. **Flag regulatory touchpoints** (licensing, identification level, AML, data protection, card data) and add *"verify the current regulation with Compliance/Legal"*.

## Guardrails
- Generic typical practice with a Vietnam focus; each provider differs. Present as typical, not as the client's truth.
- `references/regulations.md` has a "last reviewed" date and lists **topics to ask about**, not legal conclusions.
- Never include real card numbers, wallet IDs, or customer data; use masked values.
