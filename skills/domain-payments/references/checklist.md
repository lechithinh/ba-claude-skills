# Payments BA checklist / Câu hỏi BA phải hỏi

## Any payment flow
- [ ] Our role (issuer, gateway/PSP, merchant, channel)? Which partners per method?
- [ ] Statuses and transitions; **what happens on timeout**; who resolves pending and how fast?
- [ ] **Callback**: how authenticated, retried, ordered, deduplicated? What if it never arrives or arrives after expiry?
- [ ] Idempotency: key scope, how long kept, behaviour on conflicting payload?
- [ ] Amount rules: min/max, currency, fee shown before confirm, who pays the fee?
- [ ] Authentication step and thresholds (OTP, biometric, 3DS)?
- [ ] Duplicate payment of the same order; two customers paying one QR; payment after cancel?
- [ ] Refund/void: full or partial, window, source of funds, effect on settlement, customer message?
- [ ] Notifications: channels, content, masking, retries?

## Wallet
- [ ] KYC levels, limits per level, upgrade flow, behaviour at the limit?
- [ ] Balance rules (no negative, holds, expiry)? Dormant wallets? Closing a wallet with balance?
- [ ] Top-up and withdrawal: sources, fees, cut-offs, failure and reversal?

## Merchant and settlement
- [ ] Onboarding documents (KYB), risk tier, contract fee plan, API credentials lifecycle?
- [ ] Settlement cycle, cut-off, holidays, reserves, minimum payout, statement format?
- [ ] Sub-merchants and split payments?

## Reconciliation and operations
- [ ] Which three sources are matched, by what keys, how often? Tolerances?
- [ ] Break types (missing, amount mismatch, duplicate, status mismatch), owner, SLA, adjustment process (maker-checker)?
- [ ] Support tools for pending and failed payments?

## Risk, compliance, non-functional
- [ ] Fraud rules and actions; AML screening and reporting; blacklists?
- [ ] Audit trail fields; data retention; card data scope (avoid storing PAN; tokenize)?
- [ ] Peak load (campaign days, salary day), availability target, maintenance windows, partner downtime handling?

## Stakeholders often forgotten
Finance/Accounting (ledger, invoicing) · Compliance and Risk · Partner/Bank relations · Operations (reconciliation) · Customer support · Security · Merchant support.
