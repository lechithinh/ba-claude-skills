# Payments reference data model (simplified)

```mermaid
erDiagram
  CUSTOMER ||--o{ WALLET : owns
  WALLET ||--o{ LEDGER_ENTRY : records
  MERCHANT ||--o{ PAYMENT : receives
  CUSTOMER ||--o{ PAYMENT : pays
  PAYMENT ||--o{ REFUND : "may have"
  PAYMENT ||--o| CHARGEBACK : "may have"
  PAYMENT ||--o{ LEDGER_ENTRY : creates
  MERCHANT ||--o{ SETTLEMENT : "paid by"
  SETTLEMENT ||--o{ PAYMENT : includes
  PAYMENT ||--o{ RECON_ITEM : "matched in"

  WALLET {
    string wallet_id PK
    string customer_id FK
    string kyc_level
    decimal balance
    string status
  }
  PAYMENT {
    string payment_id PK
    string idempotency_key
    string merchant_id FK
    string method
    decimal amount
    decimal fee
    string status
    string provider_ref
    datetime created_at
    datetime expires_at
  }
  LEDGER_ENTRY {
    string entry_id PK
    string wallet_id FK
    string payment_id FK
    string direction
    decimal amount
    string reason
  }
  REFUND {
    string refund_id PK
    string payment_id FK
    decimal amount
    string status
  }
  SETTLEMENT {
    string settlement_id PK
    string merchant_id FK
    date cycle_date
    decimal gross
    decimal net
    string status
  }
  RECON_ITEM {
    string item_id PK
    string payment_id FK
    string source
    string match_status
  }
```

## Status sets to agree early
- **Payment:** INITIATED · PENDING · SUCCESS · FAILED · EXPIRED · REFUNDED · PARTIALLY_REFUNDED
- **Refund:** REQUESTED · PENDING · SUCCESS · FAILED
- **Chargeback:** OPENED · EVIDENCE_SUBMITTED · WON · LOST · CLOSED
- **Settlement:** OPEN · CLOSED · PAID · ON_HOLD
- **Wallet:** ACTIVE · LIMITED · LOCKED · CLOSED
- **Reconciliation item:** MATCHED · MISSING_INTERNAL · MISSING_PARTNER · AMOUNT_MISMATCH · STATUS_MISMATCH · RESOLVED

## Data sensitivity
Card PAN: never store raw, tokenize. Wallet/account numbers and phone: mask in logs and notifications. Keys and signatures: secrets, never in documents.
