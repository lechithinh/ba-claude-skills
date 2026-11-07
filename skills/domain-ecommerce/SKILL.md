---
name: domain-ecommerce
description: E-commerce and marketplace domain knowledge for Business Analysts — glossary, core processes (catalog, pricing & promotions, cart & checkout, payment, order management, fulfillment, shipping, returns & refunds, marketplace sellers & settlement), business rules (voucher stacking, inventory reservation, split orders, COD, refund routing), data model, integrations (payment gateways, e-wallets, shipping carriers, e-invoice, marketplaces), Vietnamese regulations and a BA question checklist. Use together with any BA task (requirements, user stories, linting, decomposition, diagrams, API/test design) whenever the context is online retail, an online store, marketplace, omnichannel retail, D2C, social commerce — or the user mentions "thương mại điện tử", "TMĐT", "sàn", "đơn hàng", "giỏ hàng", "voucher", "khuyến mãi", "flash sale", "COD", "vận chuyển", "đổi trả", "hoàn tiền", "seller", "tồn kho".
---

# Domain Pack: E-commerce & Marketplace / Thương mại điện tử

This skill adds **domain knowledge** on top of the BA method skills (`meeting-to-requirements`, `requirements-linter`, `functional-decomposition`, `user-story-writer`, `ba-diagrams`). It makes their output *e-commerce-correct*.

## How to use the references
Read only the file(s) you need for the current task:

| Task | Read |
|---|---|
| Terminology | `references/glossary.md` |
| Decompose functions, draw processes, find missing steps | `references/processes.md` |
| Write/lint requirements, user stories, acceptance criteria | `references/business-rules.md` + `references/checklist.md` |
| ERD, data dictionary, API payloads, order/payment statuses | `references/data-model.md` |
| Context diagrams, sequence diagrams, integration/API specs | `references/integrations.md` |
| Compliance, consumer protection, tax & invoice | `references/regulations.md` |
| Business goals, analytics events, success metrics | `references/kpis.md` |

## How to apply domain knowledge
1. **First identify the business model** — it changes almost every rule:
   - *Single-brand online store (B2C / D2C)* · *Marketplace (multi-seller)* · *Omnichannel retailer (online + stores)* · *B2B ordering*.
   If unknown, ask; otherwise state the assumption.
2. **Add the scenarios an e-commerce BA would never forget**: out-of-stock during checkout, price/promotion changed in cart, voucher stacking, partial payment failure, split orders & partial shipment, COD refusal, failed delivery, return window, refund to original payment method, oversell in flash sale.
3. **Think in state machines**: order, payment, shipment and return each have their own status — and they must stay consistent.
4. **Ask, don't invent**: return windows, voucher rules, shipping fees and commissions are business decisions → `[value — confirm]`.
5. **Flag regulatory touchpoints** (consumer protection, e-invoice, platform obligations, personal data) and add *"verify current regulation with Legal"*.

## Guardrails
- Knowledge is generic (Vietnam focus). Present as *typical practice*, not as the client's policy.
- `references/regulations.md` has a "last reviewed" date; mention it when citing.
- Don't name a specific carrier/payment provider as required unless the user did — list them as common options.
