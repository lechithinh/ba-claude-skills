---
title: "Banking Business Rule Patterns: Limits, Cut-off, Authentication, Reconciliation"
description: "Reusable banking business-rule patterns for requirements: limits, threshold-based authentication, cut-off, timeout and pending status, maker-checker, fees, interest."
lang: en
---

{% raw %}
Treat every value below as a **configurable parameter** — confirm actual values with the bank's product & compliance teams.

## 1. Limits (Hạn mức)


- Dimensions: per transaction · per day · per month · per channel (app/web/branch) · per transaction type · per customer segment · per authentication method.
- Minimum amount per transaction.
- Customer-defined limits must be ≤ bank-defined limits.
- Rule: *"If amount > per-transaction limit OR daily used + amount > daily limit → reject with specific message."*
- Edge: limits reset time (00:00? business date?), reversed transactions — do they restore the used limit?

## 2. Threshold-based authentication


- Authentication strength increases with amount/risk: e.g. OTP below a threshold, biometric above a threshold or above a daily cumulative total.
- New device / first transaction to a new beneficiary may require stronger authentication.
- Rule pattern: *"If single amount > [X] OR daily cumulative > [Y] → require biometric authentication."* (Vietnam has regulatory thresholds — see `regulations.md`.)

## 3. Cut-off time & business calendar


- Non-instant routes have cut-off; after cut-off → next business day.
- Holidays/weekends calendar is maintained in the system.
- Value date rules for scheduled transfers falling on holidays (move forward/backward?).

## 4. Transaction status & timeout


- Standard statuses: `Initiated → Pending → Success | Failed | Reversed`.
- Timeout from switch → **Pending**, never shown as failed immediately. Customer sees "processing".
- Reconciliation job resolves pending within [X] hours/days; if failed → automatic refund + notification.
- Idempotency: same request ID must not debit twice.

## 5. Account status rules


- Statuses: Active, Inactive/Dormant, Blocked (debit/credit/both), Closed.
- Debit block (e.g. legal hold): incoming allowed, outgoing denied.
- Dormant account: after [N] months no customer-initiated activity; reactivation requires [branch / eKYC].

## 6. Maker–checker (four-eyes)


- Required for: corporate payments, back-office parameter changes, manual adjustments, limit overrides.
- Maker ≠ checker. Approval may be multi-level by amount.
- Rejected items return to maker with reason; pending items expire after [N] hours.

## 7. Fees


- Fee by route (internal/interbank), channel, amount band, customer segment, package.
- Fee charged from source account or added on top? Fee waiver campaigns. VAT on fees.
- If balance covers amount but not fee → reject or deduct?

## 8. Interest


- Day-count convention (e.g. Actual/365), accrual daily, capitalization frequency.
- Rate by tenor/amount/channel; rate locked at opening.
- Early withdrawal → demand-deposit rate on the withdrawn amount (typical).
- Rounding rules (VND has no decimals).

## 9. Beneficiary & transfer content


- Name inquiry before confirm; mismatch warnings.
- Saved beneficiaries; first transfer to new beneficiary may be limited.
- Transfer remark: max length, allowed characters, default content.

## 10. Fraud & risk


- Velocity rules (many transactions in short time), unusual amount, new device + high amount, transfers to known fraud accounts.
- Actions: warn, step-up authentication, hold for review, block.
- Cooling-off period after device change or password reset.

## 11. Lending


- Approval authority matrix by amount and product.
- Debt-to-income (DTI), loan-to-value (LTV) thresholds.
- DPD buckets → collection actions & classification.
- Early repayment fee schedule; grace period.

## 12. Audit & data


- Every financial and configuration action logs who/when/what/before/after/channel/IP/device.
- Card numbers & account numbers masked in UI, logs, notifications.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-banking/SKILL.md).
