---
title: "Banking BA Checklist: Questions to Ask Stakeholders (Câu hỏi BA ngân hàng)"
description: "The questions a senior banking BA always asks for transactions, onboarding, cards, lending and non-functional requirements."
lang: en
---

{% raw %}
Use this when eliciting, linting requirements or writing acceptance criteria. Pick the sections relevant to the feature.

## Any financial transaction
- [ ] Which accounts/products are eligible as source? Which statuses block it?
- [ ] Limits: per transaction, per day, per channel, per segment? Minimum amount? Who configures them?
- [ ] Authentication: which method at which amount? Step-up rules for new device/new beneficiary?
- [ ] Fee: how calculated, who pays, shown before confirm? VAT?
- [ ] Cut-off and holidays: what happens after cut-off?
- [ ] **Timeout**: what does the customer see? How is pending resolved? Reconciliation SLA?
- [ ] Duplicate prevention (double tap, retry, network resend)?
- [ ] Reversal / refund: automatic or manual? Notification?
- [ ] Notifications: channel (push/SMS/email), content, masking?
- [ ] Transaction history: what fields, how long searchable, downloadable statement?
- [ ] AML / fraud screening: which rules, what happens when flagged?
- [ ] Audit log fields?
- [ ] Accounting: which GL entries? (confirm with Finance/Operations)

## Onboarding / eKYC
- [ ] Eligible customers (age, nationality, ID type)?
- [ ] Liveness/face match retry limits; manual review flow and SLA?
- [ ] Existing customer detection (same ID → existing CIF)?
- [ ] Limits for eKYC accounts vs in-branch verified accounts?
- [ ] Consent texts and data retention for images?
- [ ] Where does onboarding resume if the app is closed mid-way?

## Cards
- [ ] Virtual vs physical; delivery; activation channel?
- [ ] Lock (temporary) vs block (permanent); who can unlock?
- [ ] Online/overseas/contactless toggles default ON or OFF?
- [ ] Dispute window and required evidence?

## Lending
- [ ] Products, tenors, rate type (fixed/floating), reset rules?
- [ ] Required documents per customer type?
- [ ] Approval authority matrix?
- [ ] CIC consent & inquiry timing?
- [ ] Disbursement method; partial disbursement?
- [ ] Early repayment fee; grace period; overdue penalty?

## Non-functional (banking-specific)
- [ ] Availability target & maintenance windows; behaviour during EOD?
- [ ] Peak load (salary day, Tết, month-end)?
- [ ] Session timeout, device binding, rooted/jailbroken device policy?
- [ ] Data residency & personal data protection requirements?
- [ ] Data retention period for transactions & logs?
- [ ] Regulatory reports affected?

## Stakeholders to involve (often forgotten)
Product · Operations/back office · Compliance & AML · Risk · Finance/Accounting · IT Security · Customer service/Call center · Legal · Core banking team · Card center.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-banking/SKILL.md).
