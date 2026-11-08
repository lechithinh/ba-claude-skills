# Logistics reference data model (simplified)

```mermaid
erDiagram
  SHIPPER ||--o{ SHIPMENT : creates
  SHIPMENT ||--|{ PARCEL : contains
  PARCEL ||--o{ TRACKING_EVENT : "has events"
  SHIPMENT }o--|| RATE_CARD : "priced by"
  SHIPMENT ||--o| COD_COLLECTION : "may have"
  COD_COLLECTION }o--|| COD_REMITTANCE : "paid in"
  SHIPMENT }o--o| ROUTE : "delivered on"
  COURIER ||--o{ ROUTE : drives
  HUB ||--o{ TRACKING_EVENT : scans
  WAREHOUSE ||--o{ STOCK_LEVEL : holds
  SKU ||--o{ STOCK_LEVEL : "stocked as"
  SHIPMENT ||--o{ CLAIM : "may have"

  SHIPMENT {
    string shipment_id PK
    string waybill_no
    string shipper_id FK
    string service_level
    string from_address
    string to_address
    decimal chargeable_weight
    decimal declared_value
    decimal cod_amount
    string status
  }
  PARCEL {
    string parcel_id PK
    string shipment_id FK
    decimal actual_weight
    decimal volumetric_weight
  }
  TRACKING_EVENT {
    string event_id PK
    string parcel_id FK
    string event_type
    string location
    string reason_code
    datetime occurred_at
  }
  COD_REMITTANCE {
    string remittance_id PK
    date cycle_date
    decimal amount
    string status
  }
  STOCK_LEVEL {
    string sku_id FK
    string warehouse_id FK
    string bin
    int on_hand
    int reserved
  }
```

## Status sets to agree early
- **Shipment:** CREATED · PICKUP_SCHEDULED · PICKED_UP · IN_TRANSIT · OUT_FOR_DELIVERY · DELIVERED · FAILED_ATTEMPT · RETURNING · RETURNED · LOST · CANCELLED
- **COD:** PENDING_COLLECTION · COLLECTED · HANDED_OVER · REMITTED · DISPUTED
- **Claim:** OPENED · EVIDENCE_REQUESTED · APPROVED · REJECTED · PAID
- **Inbound (warehouse):** EXPECTED · RECEIVING · QC · PUT_AWAY · CLOSED
- **Pick task:** CREATED · ASSIGNED · PICKED · SHORT · PACKED

> Tip: draw the shipment state diagram (`ba-diagrams`) and map each tracking event to the status it produces.

## Data sensitivity
Recipient name, phone and address are personal data: mask in notifications and logs; restrict access; define retention.
