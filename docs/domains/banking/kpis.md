---
title: "Banking KPIs Every Business Analyst Should Know"
description: "CASA, NIM, NPL, onboarding conversion, transaction success rate, STP rate and more, with requirement implications."
lang: en
---

{% raw %}
| KPI | Meaning | Typical use in requirements |
|---|---|---|
| CASA ratio | Share of non-term deposits in total deposits | Business goal for digital account campaigns |
| NIM (Net Interest Margin) | Interest income − interest expense, over earning assets | Strategy context for pricing features |
| NPL ratio | Non-performing loans / total loans | Lending & collection features |
| Onboarding conversion | % of users who start eKYC and get an active account | Funnel analytics events per step |
| eKYC auto-approval rate | % passing without manual review | Thresholds, vendor evaluation |
| Transaction success rate | Success / total initiated (by route, error code) | Monitoring dashboards, alerting NFRs |
| Pending/timeout rate | % transactions ending pending | Reconciliation design |
| STP rate | % processed without manual touch | Back-office automation goals |
| Time-to-yes / time-to-cash | Application → approval / → disbursement | Lending journey goals |
| Digital active users (MAU) | Monthly active digital banking users | Engagement features |
| Fraud loss rate | Fraud losses / transaction volume | Fraud rule requirements |
| Dispute resolution SLA | % disputes closed within SLA | Case management requirements |
| Cost-to-income ratio | Operating costs / income | Business case for automation |
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-banking/SKILL.md).
