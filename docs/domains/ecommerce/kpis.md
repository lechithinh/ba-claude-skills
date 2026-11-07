---
title: "E-commerce KPIs Every Business Analyst Should Know"
description: "GMV, conversion, AOV, cart abandonment, payment success, cancellation, COD refusal, return rate and more, with requirement implications."
lang: en
---

{% raw %}
| KPI | Formula / meaning | Requirement implications |
|---|---|---|
| GMV | Total value of orders placed | Define: before/after cancellations? incl. shipping? |
| Net revenue | GMV − cancellations − returns − discounts (by definition) | Finance alignment on definitions |
| Conversion rate (CR) | Orders / sessions | Funnel tracking events per step |
| AOV | Revenue / orders | Bundles, free-shipping thresholds |
| Cart abandonment rate | Carts without order / carts created | Abandoned-cart reminders, checkout UX |
| Checkout drop-off by step | % leaving at each checkout step | Analytics events on each step |
| Payment success rate | Successful / attempted payments by method | Payment method ranking, retries |
| Cancellation rate | Cancelled / placed (by reason, actor) | Mandatory cancel reasons |
| COD refusal rate | Refused COD / COD shipped | COD eligibility rules |
| On-time delivery rate | Delivered within promise / delivered | Delivery estimate logic |
| Return rate | Returned items / sold items (by category/reason) | Mandatory return reasons, photo evidence |
| Seller SLA compliance | Orders confirmed/shipped on time | Seller penalties, dashboards |
| Customer lifetime value (CLV) / Repeat rate | Value over lifetime / % returning buyers | Loyalty features, CRM |
| Promotion ROI | Incremental revenue / promotion cost | Voucher tracking per order line |
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-ecommerce/SKILL.md).
