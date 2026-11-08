# Logistics business-rule patterns

All values are commercial or operational parameters - confirm with the business and partners.

1. **Chargeable weight**: max(actual weight, volumetric weight); volumetric = (length x width x height) / [divisor - confirm, varies by carrier]; rounding steps (e.g. per 0.5 kg).
2. **Pricing**: rate card by zone (origin-destination), weight band, service level; surcharges (remote area, oversize, fuel, COD fee, insurance); free-shipping thresholds are set by the seller, not the carrier.
3. **Address rules**: required components, normalisation to administrative units, **administrative boundary changes** and old/new names, geocoding confidence, remote-area flag. Confirm how historical addresses are handled.
4. **Service level and SLA**: delivery time promise by zone and service; cut-off times for same-day; holidays.
5. **Status model** is derived from scan events: `Created -> Picked up -> In transit -> Out for delivery -> Delivered | Failed attempt -> (Reattempt | Returning) -> Returned`. Define allowed transitions and which scan creates each status.
6. **Delivery attempts**: max [N] attempts, minimum gap, recipient contact attempts, reschedule limits, then return to sender.
7. **COD**: amount limits, who can change COD amount and until when, collection by courier, partial COD not allowed or allowed, **remittance cycle**, tolerance, fees; COD on returned parcel must be zero.
8. **Proof of delivery**: signature/photo/OTP/geo-stamp requirements by value or service.
9. **Return to sender**: trigger conditions, return shipping charge, who pays, return SLA.
10. **Claims**: lost/damaged definitions, claim window [N days], compensation = declared value or cap [confirm], evidence required, status flow.
11. **Inventory**: reservation at order allocation; available = on hand - reserved - safety stock; FIFO/FEFO rules; lot/serial tracking; cycle count variance thresholds and approval for adjustments.
12. **Picking**: allocation rules (nearest bin, oldest lot), short-pick handling, substitution rules.
13. **Handover control**: parcels leaving the warehouse are scanned against the manifest; discrepancies block departure or raise exception.
14. **Billing**: carrier invoice vs shipment data reconciliation, weight disputes, adjustment windows.
