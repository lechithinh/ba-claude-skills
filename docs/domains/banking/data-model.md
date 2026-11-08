---
title: "Banking Data Model & Status Sets for Business Analysts"
description: "Reference ERD for customers, accounts, transactions, cards and loans, plus status code sets and data sensitivity."
lang: en
---

{% raw %}
Use as a starting point for ERDs, data dictionaries and API payloads. Real core banking models are much larger.

```mermaid
erDiagram
  CUSTOMER ||--o{ ACCOUNT : owns
  CUSTOMER ||--o{ CARD : holds
  CUSTOMER ||--o{ LOAN : borrows
  CUSTOMER ||--o{ BENEFICIARY : saves
  CUSTOMER ||--o{ DEVICE : binds
  PRODUCT ||--o{ ACCOUNT : defines
  ACCOUNT ||--o{ TRANSACTION : records
  ACCOUNT ||--o{ HOLD : has
  CARD }o--|| ACCOUNT : "linked to"
  LOAN ||--o{ REPAYMENT_SCHEDULE : has
  LOAN }o--o{ COLLATERAL : "secured by"
  TRANSACTION ||--o| DISPUTE : "may have"

  CUSTOMER {
    string cif PK
    string full_name
    string id_type
    string id_number
    date id_expiry
    string segment
    string kyc_status
    string risk_rating
  }
  ACCOUNT {
    string account_no PK
    string cif FK
    string product_code FK
    string currency
    decimal ledger_balance
    decimal available_balance
    string status
    date opened_date
  }
  TRANSACTION {
    string txn_id PK
    string idempotency_key
    string account_no FK
    string txn_type
    string channel
    decimal amount
    decimal fee
    string beneficiary_account
    string beneficiary_bank
    string remark
    string status
    datetime created_at
    date value_date
  }
  HOLD {
    string hold_id PK
    string account_no FK
    decimal amount
    string reason
    datetime expiry
  }
  CARD {
    string card_id PK
    string masked_pan
    string cif FK
    string card_type
    string status
    date expiry
  }
  LOAN {
    string loan_id PK
    string cif FK
    decimal principal
    decimal rate
    int tenor_months
    int dpd
    string debt_group
    string status
  }
```

## Status code sets to agree early


- **Account:** ACTIVE · DORMANT · DEBIT_BLOCKED · CREDIT_BLOCKED · BLOCKED · CLOSED
- **Transaction:** INITIATED · PENDING · SUCCESS · FAILED · REVERSED
- **Card:** INACTIVE · ACTIVE · LOCKED · BLOCKED · EXPIRED · CLOSED
- **Loan:** APPLIED · APPROVED · REJECTED · DISBURSED · ACTIVE · OVERDUE · SETTLED · WRITTEN_OFF
- **KYC:** PENDING · VERIFIED · MANUAL_REVIEW · REJECTED · EXPIRED

## Data sensitivity


| Data | Treatment |
|---|---|
| ID number, biometric images | Personal data (sensitive) — encryption, access control, retention policy |
| PAN (card number) | Mask everywhere; PCI DSS scope |
| Account number | Mask in notifications/logs where possible |
| Balances, transactions | Confidential; audit access |
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-banking/SKILL.md).
