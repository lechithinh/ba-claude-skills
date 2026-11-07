---
title: "E-commerce Regulatory Touchpoints in Vietnam for BAs"
description: "Regulatory topics an e-commerce BA must raise with Legal: e-commerce operations, consumer protection, e-invoices, seller tax, personal data, promotions."
lang: en
---

{% raw %}
> **Last reviewed:** 2026-11 · **Status:** community draft — needs review by a legal expert.
> ⚠️ Use this list to **know what to ask Legal/Finance**, not as legal advice. Verify the current version, effective date and any newer law (e-commerce legislation in Vietnam is being updated).

## Vietnam
| Topic | Reference (verify current version) | What a BA should check |
|---|---|---|
| E-commerce operations | Nghị định 52/2013/NĐ-CP, amended by Nghị định 85/2021/NĐ-CP; check whether a newer E-commerce Law/decree applies | Website/app notification or registration with the Ministry of Industry and Trade; information to display (seller, product, price, terms); marketplace obligations |
| Consumer protection | Luật Bảo vệ quyền lợi người tiêu dùng 2023 (effective 07/2024) and guiding decree | Contract terms, return/complaint handling, information disclosure, platform responsibilities |
| E-invoices | Nghị định 123/2020/NĐ-CP and amendments; Thông tư 78/2021/TT-BTC | When invoices are issued, adjustments for returns, buyer data fields |
| Tax on online sellers | Tax administration rules for e-commerce platforms (platforms with payment functions may withhold/declare tax for household sellers — verify current decree) | Marketplace settlement & reporting requirements |
| Personal data protection | Nghị định 13/2023/NĐ-CP; Luật Bảo vệ dữ liệu cá nhân (2025, effective 2026) | Consent for marketing, data sharing with sellers/carriers, data subject rights |
| Advertising & promotions | Luật Quảng cáo; Luật Thương mại and decrees on promotions | Promotion registration/notification, max discount rules, prize promotions |
| Electronic transactions | Luật Giao dịch điện tử 2023 | Validity of online contracts & confirmations |

## International / standards
| Standard | When it matters |
|---|---|
| PCI DSS | If you store/process card data (prefer hosted payment pages/tokenization to reduce scope) |
| GDPR | Serving EU customers |
| WCAG 2.x | Accessibility requirements for storefronts |

## How to turn this into requirements
- Add a **"Legal & compliance"** section in the BRD with each touchpoint, owner and sign-off date.
- Keep legal parameters (return windows, displayed info, consent text) configurable.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-ecommerce/SKILL.md).
