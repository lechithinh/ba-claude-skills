---
title: "Core E-commerce Processes for BAs (Quy trình nghiệp vụ TMĐT)"
description: "Capability map and key processes: checkout, payment, order lifecycle, fulfillment, shipping, returns and marketplace seller flow."
lang: en
---

{% raw %}
## Capability map (use for functional decomposition)


1. **Catalog** — product/SKU, attributes, categories, media, search & filter, product detail page
2. **Pricing & Promotions** — price lists, promotions, vouchers, flash sales, bundles, loyalty points
3. **Customer** — registration/login, profile, addresses, wishlist, consent, loyalty tier
4. **Cart & Checkout** — cart, shipping options & fee, payment method selection, order placement
5. **Payment** — gateway, e-wallet, COD, BNPL, refunds, reconciliation
6. **Order Management** — order lifecycle, split orders, cancellation, modification, customer service tools
7. **Inventory & Fulfillment** — stock sync, reservation, warehouse allocation, pick/pack
8. **Shipping** — carrier integration, label/tracking, failed delivery, RTS
9. **Returns & Refunds** — return request, pickup, inspection, refund/exchange
10. **Marketplace** (if multi-seller) — seller onboarding/KYC, product approval, commission, settlement, seller performance
11. **Engagement** — reviews & ratings, notifications, recommendations, campaigns
12. **Back office** — reporting, e-invoice, accounting export, admin & roles

---

## 1. Browse → Cart → Checkout


1. Search/browse → product page (price, promotion, stock status, delivery estimate)
2. Add to cart (validate stock & purchase limits)
3. Cart: recalculate price & promotions on every view; show changes since added
4. Checkout: select address → calculate shipping options & fees → apply voucher(s) → choose payment method
5. **Re-validate** stock, price, promotion, voucher at "Place order"
6. Create order → reserve inventory → redirect to payment (or confirm for COD)

**BA watch-outs:** guest checkout? price changed between cart and order; voucher no longer valid; address outside delivery zone; max quantity per customer in flash sale; minimum order value; mixed cart from multiple sellers/warehouses.

## 2. Payment


1. Create payment request with order reference & amount
2. Customer pays at gateway/e-wallet/QR
3. Receive callback (IPN) **and** redirect — treat callback as source of truth
4. Update payment status → confirm order or release reservation on failure/expiry
5. Daily reconciliation with gateway reports

**BA watch-outs:** payment success but callback lost; customer pays twice; payment expiry window; partial refunds; payment fees; COD has no upfront payment → higher cancellation/refusal risk.

## 3. Order lifecycle (typical)

`Pending payment → Confirmed → Processing (pick/pack) → Ready to ship → Shipping → Delivered → Completed`
Branches: `Cancelled` (by customer/seller/system), `Delivery failed → Returning → Returned`, `Return requested → Refunded`.

**BA watch-outs:** which statuses allow customer cancellation; who can cancel at each stage; auto-complete after N days delivered (affects return window & seller payout); status sync from carrier webhooks.

## 4. Fulfillment & shipping

Allocate warehouse → pick → pack → create shipment with carrier → print label → handover → tracking updates → delivered / failed → re-delivery attempts → RTS.

## 5. Returns & refunds

Request (reason, photos, within window) → approve/reject (auto or manual) → pickup or drop-off → inspection → refund (to original method / wallet / store credit) or exchange → restock or write-off.

## 6. Marketplace seller flow

Seller registration & verification → shop setup → product listing & approval → order handling with SLA → shipping → settlement after hold period (net of commission, fees, refunds) → performance scoring & penalties.
{% endraw %}

---

**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, or read the skill source on [GitHub](https://github.com/lechithinh/ba-claude-skills/blob/main/skills/domain-ecommerce/SKILL.md).
