# Core logistics processes

## Capability map (use for functional decomposition)
1. **Order and shipment intake**: create shipment, bulk upload, API from OMS/marketplace, address capture and validation, pricing quote
2. **Pickup (first mile)**: schedule, assign courier, pickup confirmation, failed pickup
3. **Sorting and transport (middle mile)**: hub scan in/out, sorting rules, linehaul, manifests
4. **Delivery (last mile)**: dispatch, route, delivery attempt, proof of delivery, notification to recipient
5. **Exceptions**: failed delivery, reschedule, address change, return to sender, lost/damaged
6. **COD**: collection, handover, remittance and reconciliation
7. **Returns (reverse logistics)**: return pickup, inspection, restock or dispose
8. **Warehouse**: inbound, putaway, inventory, picking, packing, outbound, cycle count
9. **Carrier and pricing management**: carriers, rate cards, surcharges, service levels, routing rules
10. **Tracking and communication**: events, customer tracking, notifications
11. **Claims and billing**: claims, carrier invoices, shipper billing
12. **Reporting and SLA monitoring**

## Last-mile delivery (typical)
Parcel arrives at delivery hub -> assigned to courier/route -> out for delivery -> attempt -> **delivered (POD)** or **failed (reason)** -> reattempt up to [N] -> return to sender. COD: collect cash, record, hand over, remit later.

## COD remittance
Courier collects -> records per parcel -> hands cash/transfers to hub -> carrier consolidates -> **remits to shipper per cycle [T+n - confirm]** -> shipper reconciles by parcel list. Mismatch types: parcel delivered but cash missing, amount differs, parcel returned but marked collected.

## Warehouse fulfillment
Receive (ASN vs actual) -> QC -> putaway to bin -> stock available -> order allocated -> pick -> pack -> label -> handover to carrier (scan) -> stock deducted. Returns: receive -> inspect -> restock/quarantine/dispose.

## Failed delivery and return
Failed reasons (not home, refused, wrong address, unreachable) -> notify recipient/shipper -> reschedule or change address -> after [N] attempts or deadline -> return to sender -> shipper receives and updates order.
