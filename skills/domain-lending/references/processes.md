# Core consumer lending processes

## Capability map (use for functional decomposition)
1. **Customer and application**: eKYC, application form, documents, consent, partner/channel intake
2. **Credit assessment and decision**: bureau inquiry, scoring, income verification, rules, auto-decision, manual review, approval authority
3. **Offer and contract**: pricing, offer, e-contract, e-signature, disclosure
4. **Disbursement**: account validation, payout, fees, insurance bundling
5. **Servicing and repayment**: schedule, auto-debit, payment allocation, statements, partial and early repayment
6. **Collections**: reminders, DPD buckets, contact strategy, promise to pay, field/third-party, legal
7. **Restructuring and settlement**: extension, holiday, rescheduling, settlement offers
8. **Closure and write-off**: payoff, release of collateral, write-off
9. **Risk and reporting**: classification, provisioning, portfolio reports, regulatory reports
10. **Fraud and compliance**: identity fraud, application fraud, AML, audit
11. **Partner management** (if BNPL/installment): merchants, funding, settlement

## Origination -> disbursement (typical)
Application -> eKYC and consent -> bureau inquiry -> scoring and rules -> **auto-approve / reject / manual review** -> offer -> e-contract signing -> disbursement -> schedule created -> first installment reminder.
Watch-outs: customer drops out between steps (resume), income mismatch, offer expiry, multiple applications, re-application after rejection, contract signed but disbursement failed.

## Repayment (typical)
Schedule -> reminder before due date -> auto-debit or customer payment -> **allocation** (penalty, interest, principal in the agreed order) -> update balance and DPD -> receipt. Missed payment -> DPD starts -> reminders -> collections.

## Early / partial repayment
Customer asks for payoff amount (valid until a date) -> pays -> recalculate interest to the payment date, apply fee if any -> close or recompute remaining schedule (shorter term or lower installment).

## Collections by bucket (illustrative)
| DPD | Typical action |
|---|---|
| 1-10 | Soft reminders (SMS, push, call) |
| 11-30 | Calls, promise-to-pay, late fee/penalty |
| 31-90 | Escalation, collection team, restructuring offers |
| 90+ | Third-party/field/legal, provisioning, write-off review |
Buckets, actions and contact limits are policy and regulation driven: confirm.
