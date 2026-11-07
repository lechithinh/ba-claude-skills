---
title: "Banking Domain Knowledge for Business Analysts (Kiến thức nghiệp vụ ngân hàng cho BA)"
description: "Banking domain pack for BAs and Claude: glossary, retail banking processes, business-rule patterns, stakeholder question checklist, data model, integrations (core banking, NAPAS, CITAD, CIC), Vietnam regulations and KPIs."
lang: en
---

A practical reference for Business Analysts working on retail and digital banking: mobile and internet banking, eKYC onboarding, fund transfers, cards, lending, deposits and disputes. It is also a **Claude skill**: install the plugin and Claude applies this knowledge automatically when your request is about banking.

*Tài liệu tham khảo cho BA ngân hàng bán lẻ và ngân hàng số. Đây cũng là một skill Claude: khi bạn nhắc tới bối cảnh ngân hàng, Claude tự áp dụng kiến thức này.*

| Topic | What you get |
|---|---|
| [Glossary (EN–VI)](glossary.md) | 40+ terms: CIF, CASA, cut-off, name inquiry, reconciliation, maker-checker, DPD, CIC… |
| [Processes](processes.md) | Capability map, eKYC, transfers, cards, lending, deposits, disputes, end-of-day |
| [Business-rule patterns](business-rules.md) | Limits, threshold-based authentication, cut-off, timeout and pending, fees, interest, fraud |
| [**BA checklist**](checklist.md) | The questions a senior banking BA always asks stakeholders |
| [Data model](data-model.md) | Reference ERD, status sets, data sensitivity |
| [Integrations](integrations.md) | Core banking, middleware, NAPAS, CITAD, CMS, LOS, CIC, eKYC, AML |
| [Regulations](regulations.md) | Vietnam and international touchpoints to raise with Compliance (community draft) |
| [KPIs](kpis.md) | CASA, NIM, NPL, onboarding conversion, STP rate and more |

**See it in action:** [interbank transfer user story with vs without this pack](../../examples/domain-showcase/banking-interbank-transfer.md)

**Use with Claude:** `/plugin marketplace add lechithinh/ba-claude-skills` · [Skill source on GitHub](https://github.com/lechithinh/ba-claude-skills/tree/main/skills/domain-banking)
