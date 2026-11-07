---
title: "Showcase · Banking — \"User story: interbank transfer\""
description: "Domain showcase: same prompt with and without a domain pack"
lang: en
---

{% raw %}
**Prompt:** *"Viết user story kèm acceptance criteria cho chức năng chuyển tiền liên ngân hàng trên mobile banking."*

> Illustrative, lightly edited outputs. Values in `[… — confirm]` are deliberately left for the bank to decide.

---

## ❌ Without a domain pack (typical generic output)

**As a** customer **I want** to transfer money to another bank **so that** I can pay people.

```gherkin
Scenario: Successful transfer
  Given I am logged in
  When I enter account number, bank, amount and confirm with OTP
  Then the money is transferred
  And I see a success message

Scenario: Insufficient balance
  Given my balance is lower than the amount
  When I confirm
  Then I see "Insufficient balance"
```

2 scenarios. Happy path + one error. Nothing about timeouts, limits, authentication thresholds, fees or reconciliation.

---

## ✅ With `user-story-writer` + `domain-banking`

**US-TRF-01 · Instant interbank transfer (24/7)**
**Trace:** Capability 3. Payments & Transfers · BR patterns: Limits, Threshold-based authentication, Transaction status & timeout, Fees

**As a** retail customer
**I want** to transfer money instantly to an account at another bank
**so that** the beneficiary receives it immediately, any time of day.

```gherkin
Scenario: Successful instant transfer
  Given my payment account is Active with sufficient available balance
  When I enter a beneficiary account at another bank
  Then the system performs a name inquiry and shows the beneficiary name
  When I enter an amount within my limits and confirm
  And I authenticate with the method required for this amount
  Then my account is debited amount + fee
  And the transaction status is "Success"
  And I receive a notification with the masked account number

Scenario: Beneficiary name inquiry fails
  Given the beneficiary account does not exist or is closed
  When the name inquiry is performed
  Then I see "Không tìm thấy tài khoản người thụ hưởng"
  And I cannot continue

Scenario: Amount exceeds per-transaction or daily limit
  Given my daily used amount + this amount > my daily limit [confirm]
  When I confirm
  Then the transfer is rejected with the remaining daily limit shown

Scenario: Stronger authentication above threshold
  Given the amount or my daily cumulative total exceeds the biometric threshold [confirm with Compliance]
  When I confirm
  Then I must complete biometric authentication instead of OTP

Scenario: Switch timeout — transaction pending
  Given the interbank switch does not respond within [N seconds — confirm]
  When the timeout occurs
  Then the transaction status is "Pending" (not "Failed")
  And I see "Giao dịch đang được xử lý, chúng tôi sẽ thông báo kết quả"
  And the transaction is resolved by reconciliation within [SLA — confirm]
  And if it is finally failed, my account is refunded automatically and I am notified

Scenario: Duplicate submission
  Given I tapped "Confirm" twice or the app retried after a network error
  When the second request arrives with the same idempotency key
  Then only one debit is made

Scenario: Fee not covered by balance
  Given my balance covers the amount but not amount + fee
  When I confirm
  Then the transfer is rejected with a message showing the fee
```

**Open questions `[domain]`**
1. Limit values per segment/channel and who can change them?
2. Authentication thresholds — confirmed by Compliance against the current regulation?
3. Fee schedule and waivers?
4. Reconciliation SLA and customer notification for pending transactions?
5. Is AML/fraud screening synchronous (blocks) or asynchronous (alerts)?

**What the domain pack added:** name inquiry · limits · threshold-based authentication · **timeout → pending → reconciliation** · idempotency · fee handling · masking · compliance questions.
{% endraw %}
