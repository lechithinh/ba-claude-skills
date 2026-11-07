---
title: "Banking Regulatory Touchpoints in Vietnam for BAs"
description: "Regulatory topics a banking BA must raise with Compliance: online banking security, biometric authentication, eKYC, cards, AML, personal data."
lang: en
---

{% raw %}
> **Last reviewed:** 2026-11 · **Status:** community draft — needs review by a banking compliance expert.
> ⚠️ Regulations are amended frequently. Use this list to **know what to ask Compliance**, not as legal advice. Always verify the current version, effective date and the bank's internal policy.

## Vietnam (State Bank of Vietnam — NHNN and others)
| Topic | Reference (verify current version) | What a BA should check |
|---|---|---|
| Online banking safety & security | Thông tư 50/2024/TT-NHNN on safety and security for online banking services | Authentication methods by transaction type/amount, device binding, security measures for apps |
| Biometric authentication for transfers | Quyết định 2345/QĐ-NHNN (applied from 07/2024): biometric authentication for online transfers above a per-transaction threshold or a daily cumulative threshold (commonly cited: > 10 million VND/transaction or > 20 million VND/day) | Thresholds, first-time device login, how biometric data is matched against chip-ID data |
| Payment accounts & eKYC | Thông tư 17/2024/TT-NHNN on opening and using payment accounts | eKYC steps, identity verification, limits & conditions for remotely-opened accounts |
| Bank cards | Thông tư 18/2024/TT-NHNN on bank card operations | Card issuance (incl. eKYC), card types, limits |
| Anti-money laundering | Luật Phòng, chống rửa tiền 2022 and guiding documents | CDD/EDD, reporting thresholds, suspicious transaction reports, record retention |
| Personal data protection | Nghị định 13/2023/NĐ-CP; Luật Bảo vệ dữ liệu cá nhân (2025, effective 2026) | Consent, purpose limitation, sensitive data (biometrics, financial), data subject rights, breach notification |
| Loan classification & provisioning | Current NHNN circular on debt classification and risk provisioning | Debt groups 1–5, DPD thresholds, CIC reporting |
| Electronic transactions | Luật Giao dịch điện tử 2023 | Validity of e-contracts, e-signatures, records |

## International standards
| Standard | When it matters |
|---|---|
| PCI DSS | Anything that stores/processes/transmits card numbers |
| ISO 20022 | Payment messaging formats (increasingly used by payment systems) |
| EMV / 3-D Secure | Card-present chip transactions / online card authentication |
| Basel (capital & liquidity) | Risk & finance reporting projects |
| IFRS 9 | Expected credit loss / provisioning projects |
| OWASP MASVS | Mobile banking app security requirements |

## How to turn this into requirements
- Create explicit **compliance requirements** (e.g. *"The system shall require biometric authentication when [threshold rule] — ref: [regulation], verified by Compliance on [date]"*).
- Keep thresholds **configurable** so a regulatory change is a parameter change, not a release.
- Add Compliance as an approver in the requirements sign-off.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-banking/SKILL.md).
