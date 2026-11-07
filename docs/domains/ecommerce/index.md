---
title: "E-commerce Domain Knowledge for Business Analysts (Kiến thức nghiệp vụ TMĐT cho BA)"
description: "E-commerce and marketplace domain pack for BAs and Claude: glossary, processes, business-rule patterns (vouchers, inventory, orders, refunds), stakeholder question checklist, data model, integrations, Vietnam regulations and KPIs."
lang: en
---

A practical reference for Business Analysts working on online stores, marketplaces and omnichannel retail: catalog, pricing and vouchers, checkout, payment, orders, fulfillment, shipping and COD, returns and seller settlement. It is also a **Claude skill**: install the plugin and Claude applies this knowledge automatically when your request is about e-commerce.

*Tài liệu tham khảo cho BA thương mại điện tử và sàn TMĐT. Đây cũng là một skill Claude: khi bạn nhắc tới bối cảnh TMĐT, Claude tự áp dụng kiến thức này.*

| Topic | What you get |
|---|---|
| [Glossary (EN–VI)](glossary.md) | SKU, OMS, WMS, ATS, COD, RTS, settlement, GMV, AOV… |
| [Processes](processes.md) | Capability map, checkout, payment, order lifecycle, fulfillment, returns, marketplace |
| [Business-rule patterns](business-rules.md) | Pricing precedence, voucher stacking, inventory reservation, split orders, refunds |
| [**BA checklist**](checklist.md) | The questions a senior e-commerce BA always asks stakeholders |
| [Data model](data-model.md) | Reference ERD, order / payment / shipment / return status sets |
| [Integrations](integrations.md) | Payment gateways & e-wallets, carriers, e-invoice, ERP, marketplaces |
| [Regulations](regulations.md) | Vietnam and international touchpoints to raise with Legal (community draft) |
| [KPIs](kpis.md) | GMV, conversion, AOV, cart abandonment, return rate and more |

**See it in action:** [order cancellation requirement with vs without this pack](../../examples/domain-showcase/ecommerce-cancel-order.md)

**Use with Claude:** `/plugin marketplace add lechithinh/ba-claude-skills` · [Skill source on GitHub](https://github.com/lechithinh/ba-claude-skills/tree/main/skills/domain-ecommerce)
