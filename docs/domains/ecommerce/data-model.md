---
title: "E-commerce Data Model & Order Status Sets for Business Analysts"
description: "Reference ERD for products, SKUs, inventory, orders, payments, shipments and refunds, plus order, payment, shipment and return status sets."
lang: en
---

{% raw %}
```mermaid
erDiagram
  CUSTOMER ||--o{ ADDRESS : has
  CUSTOMER ||--o{ CART : owns
  CUSTOMER ||--o{ ORDER : places
  PRODUCT ||--|{ SKU : "has variants"
  SELLER ||--o{ PRODUCT : lists
  SKU ||--o{ INVENTORY : "stocked in"
  WAREHOUSE ||--o{ INVENTORY : holds
  CART ||--o{ CART_ITEM : contains
  ORDER ||--|{ ORDER_ITEM : contains
  ORDER ||--o{ PAYMENT : "paid by"
  ORDER ||--o{ SHIPMENT : "fulfilled by"
  ORDER ||--o{ ORDER_DISCOUNT : applies
  VOUCHER ||--o{ ORDER_DISCOUNT : "used in"
  ORDER_ITEM ||--o{ RETURN_ITEM : "may be returned"
  RETURN_REQUEST ||--|{ RETURN_ITEM : includes
  RETURN_REQUEST ||--o{ REFUND : triggers

  SKU {
    string sku_id PK
    string product_id FK
    string attributes
    decimal list_price
    decimal sale_price
    decimal weight_kg
  }
  INVENTORY {
    string sku_id FK
    string warehouse_id FK
    int on_hand
    int reserved
    int safety_stock
  }
  ORDER {
    string order_id PK
    string parent_order_id
    string customer_id FK
    string seller_id
    string status
    string payment_method
    decimal subtotal
    decimal discount_total
    decimal shipping_fee
    decimal grand_total
    datetime placed_at
  }
  ORDER_ITEM {
    string order_item_id PK
    string order_id FK
    string sku_id FK
    int quantity
    decimal unit_price
    decimal allocated_discount
  }
  PAYMENT {
    string payment_id PK
    string order_id FK
    string provider
    string provider_txn_id
    decimal amount
    string status
  }
  SHIPMENT {
    string shipment_id PK
    string order_id FK
    string carrier
    string tracking_no
    decimal cod_amount
    string status
  }
  REFUND {
    string refund_id PK
    string return_id FK
    decimal amount
    string method
    string status
  }
```

## Status sets to agree early


- **Order:** PENDING_PAYMENT · CONFIRMED · PROCESSING · READY_TO_SHIP · SHIPPING · DELIVERED · COMPLETED · CANCELLED · RETURNING · RETURNED
- **Payment:** PENDING · AUTHORIZED · PAID · FAILED · EXPIRED · PARTIALLY_REFUNDED · REFUNDED
- **Shipment:** CREATED · PICKED_UP · IN_TRANSIT · OUT_FOR_DELIVERY · DELIVERED · FAILED_ATTEMPT · RETURNING_TO_SENDER · RETURNED
- **Return:** REQUESTED · APPROVED · REJECTED · PICKED_UP · INSPECTING · REFUNDED · CLOSED

> Tip: draw a state diagram per object (`ba-diagrams`) and a mapping table showing how a shipment/payment event moves the order status.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-ecommerce/SKILL.md).
