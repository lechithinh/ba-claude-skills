---
title: "E-commerce Business Rule Patterns: Vouchers, Inventory, Orders, Refunds"
description: "Business-rule patterns for pricing, promotion stacking, inventory reservation, split orders, shipping, refunds, returns and marketplaces."
lang: en
---

{% raw %}
All values are **business decisions** — confirm them; keep them configurable.

## 1. Pricing


- Price precedence: flash sale price > promotion price > sale price > list price (confirm actual order).
- Price displayed in cart is **not locked** until order placement.
- Rounding (VND, no decimals); price includes VAT?

## 2. Promotions & vouchers


- Types: % off, fixed amount off, free shipping, buy X get Y, bundle price, gift with purchase.
- Conditions: min order value, eligible categories/SKUs/sellers, customer segment, first order, payment method, channel (app only).
- Caps: max discount per order, total budget, usage per customer, total usage.
- **Stacking matrix** (define explicitly!): platform voucher + seller voucher + shipping voucher + product promotion — which combine?
- Order of application: product discounts → order discounts → shipping discounts (typical).
- Allocation of order-level discount to line items (needed for partial returns & invoicing).
- Voucher restoration when order cancelled/returned: restore or not? Before/after expiry?

## 3. Inventory


- ATS = on hand − reserved − safety stock.
- Reservation timing: at add-to-cart (rare), at order placement (common), at payment success.
- Reservation expiry for unpaid orders: [N minutes].
- Flash sale: dedicated stock allocation; purchase limit per customer.
- Multi-warehouse allocation rule: nearest, cheapest, single-shipment preferred.
- Oversell policy: block, allow backorder, or cancel & compensate.

## 4. Orders


- Split rules: by seller, by warehouse, by shipping type (bulky/standard), by pre-order item.
- Cancellation: customer can cancel until status [Processing]; after that request approval.
- Modification after placement (address, items) — usually not allowed or only before processing.
- Auto-cancel unpaid orders after [N minutes]; auto-complete delivered orders after [N days].

## 5. Shipping


- Fee by weight (actual vs volumetric), zone, carrier, speed; free shipping thresholds.
- Delivery attempts: [N] before RTS.
- COD limits: max COD order value; COD disabled for some customers (high refusal history).

## 6. Payment & refunds


- Refund to original payment method by default; COD → bank transfer / wallet / store credit.
- Refund timing per method (card refunds can take days); partial refunds per line item.
- Shipping fee refundable? Depends on return reason (seller fault vs change of mind).

## 7. Returns


- Return window: [N days] from delivery; category exclusions (underwear, perishables, digital goods).
- Required evidence (photos/unboxing video) for damage claims.
- Who pays return shipping by reason.
- Inspection outcome: full refund, partial refund, rejected (return to customer).

## 8. Marketplace


- Commission by category; payment fee; service fees; penalties.
- Settlement hold period after delivery/complete; reserve for returns.
- Seller SLA: confirm within [N hours], ship within [N days]; late → auto-cancel + penalty.
- Product listing rules: prohibited/restricted categories, mandatory attributes, brand authorization.

## 9. Loyalty


- Points earn rate, exclusions (shipping, vouchers), points expiry, points reversal on return.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-ecommerce/SKILL.md).
