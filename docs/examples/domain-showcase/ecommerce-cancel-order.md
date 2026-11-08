---
title: "Showcase · E-commerce — \"Lint this requirement: order cancellation\""
description: "Domain showcase: same prompt with and without a domain pack"
lang: en
---

{% raw %}
**Prompt:** *"Kiểm tra yêu cầu này: Khách hàng có thể hủy đơn hàng và được hoàn tiền."*

> Illustrative, lightly edited outputs.

---

## ❌ Without a domain pack (typical generic output)

- "có thể" is slightly vague → specify conditions.
- Compound requirement (cancel + refund) → split.

**Rewrite:** *"The customer shall be able to cancel an order. The system shall refund the customer after cancellation."*

Correct grammar — but every hard business question is still open.

---

## ✅ With `requirements-linter` + `domain-ecommerce`

**Score: 1/10** · Issues: CMP, TST, **DOM ×3 (capped at −4)**

| Rule | Finding |
|---|---|
| CMP | Cancellation and refund are two behaviours |
| TST | No condition on *when* cancellation is allowed; "hoàn tiền" has no destination, amount or timing a tester can verify |
| DOM | Missing: cancellation rules **per order status** (Pending payment / Confirmed / Processing / Shipping) |
| DOM | Missing: **voucher, loyalty points and stock** handling on cancellation |
| DOM | Missing: **COD vs prepaid** refund routing; split/marketplace orders (cancel one seller's sub-order?) |

**Rewrite (split):**
> **FR-CAN-01:** The customer shall be able to cancel an order while its status is `Pending payment` or `Confirmed`. For status `Processing`, the customer may submit a cancellation request that the [seller/ops — confirm] approves or rejects within [N hours — confirm]. Orders in `Shipping` or later cannot be cancelled; the customer is directed to the return process.
>
> **FR-CAN-02:** When a prepaid order is cancelled, the system shall refund the paid amount to the **original payment method** within [N business days per method — confirm]. COD orders that were not paid require no refund.
>
> **FR-CAN-03:** On cancellation the system shall release reserved stock immediately, reverse loyalty points earned, and [restore / not restore — confirm] the voucher if it is still within its validity period.
>
> **FR-CAN-04:** The customer shall select a cancellation reason from a configurable list (needed for cancellation-rate analytics).

**Clarifying questions**

- *Merchandising/Marketing:* voucher restoration policy? Flash-sale items cancellable?
- *Finance:* refund timing per payment method; e-invoice already issued → adjustment process?
- *Operations:* cutoff between "Confirmed" and "Processing" — what event triggers it?
- *Marketplace (if multi-seller):* can the customer cancel one seller's part of a split order?

**What the domain pack added:** status-based cancellation · refund routing (original method vs COD) · stock release · voucher & loyalty reversal · split orders · e-invoice impact · cancellation reasons for KPIs.
{% endraw %}
