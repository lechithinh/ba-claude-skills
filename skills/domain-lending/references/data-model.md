# Lending reference data model (simplified)

```mermaid
erDiagram
  CUSTOMER ||--o{ APPLICATION : submits
  APPLICATION ||--o| DECISION : "gets"
  APPLICATION ||--o| LOAN : "becomes"
  LOAN ||--|{ INSTALLMENT : "has schedule"
  LOAN ||--o{ PAYMENT : receives
  PAYMENT }o--o{ INSTALLMENT : "allocated to"
  LOAN ||--o{ COLLECTION_CASE : "may open"
  LOAN }o--o{ COLLATERAL : "secured by"
  LOAN ||--o{ RESTRUCTURE : "may have"

  APPLICATION {
    string application_id PK
    string customer_id FK
    decimal amount
    int term_months
    string product_code
    string status
    datetime created_at
  }
  DECISION {
    string decision_id PK
    string application_id FK
    string outcome
    int score
    string reason_codes
    string decided_by
  }
  LOAN {
    string loan_id PK
    string application_id FK
    decimal principal
    decimal rate
    string rate_method
    int term_months
    date disbursed_on
    int dpd
    string status
  }
  INSTALLMENT {
    string installment_id PK
    string loan_id FK
    int seq
    date due_date
    decimal principal_due
    decimal interest_due
    decimal paid
    string status
  }
  PAYMENT {
    string payment_id PK
    string loan_id FK
    decimal amount
    string channel
    datetime paid_at
  }
  COLLECTION_CASE {
    string case_id PK
    string loan_id FK
    string bucket
    string status
  }
```

## Status sets to agree early
- **Application:** DRAFT · SUBMITTED · IN_REVIEW · APPROVED · REJECTED · OFFERED · SIGNED · EXPIRED · CANCELLED
- **Loan:** PENDING_DISBURSEMENT · ACTIVE · OVERDUE · RESTRUCTURED · PAID_OFF · WRITTEN_OFF · CANCELLED
- **Installment:** SCHEDULED · DUE · PARTIALLY_PAID · PAID · OVERDUE
- **Disbursement:** INITIATED · PENDING · SUCCESS · FAILED

## Data sensitivity
ID numbers, income, bureau data, contact details: personal data; mask in logs and documents; restrict access and keep audit trail.
