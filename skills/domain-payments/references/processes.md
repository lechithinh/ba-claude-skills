# Core payments processes

## Capability map (use for functional decomposition)
1. **Merchant management**: onboarding/KYB, contract, fee plan, API keys, sub-merchants
2. **Wallet and identity**: wallet account, KYC levels, limits, device binding
3. **Cash-in**: bank link, card, QR, bank transfer; **Cash-out**: to bank
4. **Transfers**: wallet to wallet, to bank, scheduled
5. **Merchant payments**: online redirect/in-app, QR (static/dynamic), POS
6. **Refund, void, chargeback and disputes**
7. **Settlement**: batches, cycles, merchant payouts, reserves
8. **Reconciliation**: internal ledger vs partner reports vs bank statements
9. **Fees and revenue**: fee calculation, invoicing, tax
10. **Risk and compliance**: fraud rules, AML screening, limits, case management
11. **Reporting and operations**: dashboards, manual adjustments, support tools

## Online payment (typical)
1. Merchant creates a payment (amount, order reference, return URL, idempotency key).
2. Customer is redirected / opens the app, authenticates (OTP, biometric, 3DS), pays.
3. Provider sends **callback** (IPN) and redirects the customer back.
4. Merchant system **confirms using the callback or a status query**, not the redirect.
5. If no callback: query status at intervals; expire the payment after [N minutes - confirm].
6. Daily reconciliation resolves mismatches.

## Wallet top-up
Choose source -> amount -> fee preview -> authenticate -> debit source -> **credit wallet only after confirmed success** -> notify. Timeout means **pending**, resolved by query/reconciliation; never double-credit.

## Refund
Request (full or partial, reason) -> validate (window, remaining refundable amount, balance of merchant) -> call provider -> status pending -> success/failed -> notify -> adjust merchant statement and settlement.

## Settlement and reconciliation
Close batch at cut-off -> compute net (gross - fees - refunds - chargebacks - reserve) -> pay out [T+n - confirm] -> reconcile with bank statement -> investigate breaks.

## Chargeback
Dispute notice -> deadline to respond -> collect evidence -> accept or contest -> outcome -> debit merchant (possibly with fee).
