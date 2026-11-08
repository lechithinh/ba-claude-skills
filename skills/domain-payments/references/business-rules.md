# Payments business-rule patterns

All values are configurable parameters - confirm with product, partner contracts and Compliance.

1. **Wallet limits by KYC level**: balance cap, per transaction, per day, per month; stricter for lower levels; limits for top-up, transfer and withdrawal can differ.
2. **Ledger integrity**: balance changes only through ledger entries (double entry); no negative balance; every movement has a reference and reason.
3. **Status model**: `Initiated -> Pending -> Success | Failed | Expired`; refunds and chargebacks have their own statuses. **Timeout = Pending.**
4. **Callback is the source of truth**: the redirect is a hint. Also query status if no callback arrives. Verify callback authenticity (signature) and amount.
5. **Idempotency**: same idempotency key + same payload returns the same result; same order reference cannot be paid twice.
6. **Expiry**: unpaid payments expire after [N minutes]; a late success after expiry needs a defined path (credit anyway, or refund).
7. **Authorize and capture** (cards): hold expires after [N days]; capture <= authorized amount; void before settlement.
8. **Refund rules**: window [N days]; total refunds <= captured amount; partial refunds allowed or not; refund goes to the **original source** by default; refund fee kept or returned?
9. **Chargeback**: response deadline from the scheme; funds debited from merchant on loss; reserve may apply.
10. **Settlement**: cycle [T+n], cut-off times, holidays; net = gross - fee - refunds - chargebacks - reserve; minimum payout threshold.
11. **Fees**: percentage + fixed; by method, channel, merchant plan; rounding rule (VND has no decimals); who bears the fee.
12. **Reconciliation**: three-way match (internal ledger, partner report, bank statement) by reference id and amount; tolerance, break classification, aging, owner and SLA.
13. **Risk**: velocity rules, amount thresholds, new-device rules, blacklists; actions: allow, step-up, hold, block.
14. **Reversal and adjustment**: manual adjustments need maker-checker, reason, audit trail.
15. **Notifications**: customer and merchant notified of success/failure/refund; mask account and card data.
