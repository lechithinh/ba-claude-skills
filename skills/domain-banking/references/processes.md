# Core retail banking processes

## Capability map (use for functional decomposition)
1. **Customer Management** — onboarding/eKYC, KYC update, customer profile, segmentation, consent
2. **Account Management** — open/close account, account status, statements, dormant handling, nice/vanity account numbers
3. **Payments & Transfers** — internal, interbank instant (24/7), interbank normal, scheduled/recurring, bill payment, QR payment, beneficiary management
4. **Cards** — issuance, activation, PIN, lock/unlock, limits, transactions, statements (credit), disputes
5. **Lending** — application, appraisal, approval, disbursement, repayment, restructuring, collection
6. **Deposits** — open term deposit, rollover, early withdrawal, interest calculation
7. **Service & Disputes** — tra soát/complaints, SLA tracking, refunds
8. **Security & Access** — login, device binding, authentication methods, limits, fraud monitoring
9. **Back office** — posting, reconciliation, EOD, GL, reporting
10. **Compliance** — AML screening & monitoring, regulatory reporting, audit trail

---

## 1. Digital onboarding (eKYC)
1. Capture ID document (chip-based citizen ID, NFC read where supported) → OCR
2. Liveness check + face match (selfie vs ID photo / chip data)
3. Verify identity data against national data sources where required
4. Collect additional info (occupation, address, purpose), consent & T&C
5. AML / sanctions screening
6. Create CIF + payment account, set initial limits
7. Register digital banking credentials, bind device, set up authentication method

**BA watch-outs:** existing customer (duplicate CIF), failed liveness retry limits, manual review queue, limits for eKYC-opened accounts may differ from in-branch, minors/foreigners excluded, ID expiry, data retention for images.

## 2. Fund transfer (internal & interbank)
1. Select source account → enter beneficiary (account/card/QR) → **name inquiry**
2. Enter amount, content (remark) → validate balance, limits, account status
3. Calculate fee → show confirmation
4. **Authenticate** (OTP / Smart OTP / biometric depending on amount & risk)
5. Debit source (or hold) → send to switch (internal posting / NAPAS / CITAD)
6. Receive response: **success / failed / timeout (pending)**
7. Notify customer (push/SMS), update history
8. **Reconciliation** resolves pending: confirm success or reverse/refund

**BA watch-outs:** timeout handling is where most production incidents live; duplicate submission; beneficiary account closed; holiday/cut-off for non-instant routes; transfer content character limits & no Vietnamese diacritics on some routes; scheduled transfer failing on execution date.

## 3. Card lifecycle
Apply → approve (credit) → issue (physical/virtual) → deliver → activate & set PIN → use (authorize → settle) → statement (credit) → repayment → renew/replace → close.
**BA watch-outs:** temporary lock vs permanent block (lost/stolen), online/overseas usage toggles, limit changes, card replacement keeps or changes PAN, dispute window.

## 4. Lending (Loan origination → servicing)
Application → document collection → CIC inquiry & scoring → appraisal → approval (by authority level) → contract & collateral → disbursement → repayment schedule → collection (DPD buckets) → settlement/early repayment → closure.
**BA watch-outs:** approval matrix by amount/product, early repayment fee, partial disbursement, rate reset (floating), restructuring, insurance bundling, consent for CIC inquiry.

## 5. Term deposit
Open (online/branch) → interest rate by tenor/amount/channel → maturity → rollover (principal only / principal + interest) or payout → early withdrawal (penalty rate) → pledge as collateral.

## 6. Dispute / Investigation (Tra soát)
Customer raises request → classify (wrong beneficiary, debited not credited, card dispute, fraud) → assign → investigate with counterpart bank/switch → result → refund/reversal or rejection → notify → close within SLA.

## 7. End-of-Day (EOD)
Stop/queue certain transactions → interest accrual → fees → standing orders → batch postings → reports → open new business date. **Ask:** which channels stay available during EOD?
