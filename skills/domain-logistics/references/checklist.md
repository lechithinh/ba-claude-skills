# Logistics BA checklist / Câu hỏi BA phải hỏi

## Role and scope
- [ ] Are we the shipper, carrier, 3PL or marketplace? Own fleet or partner couriers? Parcels, pallets, both?
- [ ] Stages in scope: first mile, hubs, last mile, returns, warehouse?

## Shipments and pricing
- [ ] Required data per shipment (address parts, weight, dimensions, declared value, COD)?
- [ ] Volumetric divisor, rounding, zone map, surcharges, quote vs final charge, weight disputes?
- [ ] Address validation and normalisation; what if the address cannot be resolved?

## Delivery and exceptions
- [ ] Status list and which scan or action sets each; who may override?
- [ ] **Failed delivery reasons, number of attempts, gap between attempts, notification, return trigger?**
- [ ] Reschedule, change address, change COD amount: allowed until which status?
- [ ] Partial delivery, split shipment, refused parcel, delivery to neighbour/locker?
- [ ] Proof of delivery requirements?

## COD
- [ ] Limits, partial collection, who handles shortages, remittance cycle and format, reconciliation keys, tolerance, fees?
- [ ] COD for parcels returned after collection?

## Warehouse
- [ ] Inbound check (ASN vs actual), QC, putaway rules, lot/serial/expiry, FIFO/FEFO?
- [ ] Reservation timing, safety stock, oversell protection, multi-warehouse allocation?
- [ ] Picking strategy, short pick, packing and label rules, handover scan?
- [ ] Cycle count frequency, variance thresholds, adjustment approval?

## Claims, SLA, non-functional
- [ ] Lost/damaged claim flow, windows, compensation, evidence?
- [ ] SLA measures and penalties; scan latency tolerance; offline mode for couriers?
- [ ] Peak load (sale days), integration downtime handling, data retention for tracking events?

## Stakeholders often forgotten
Operations and hub managers · Couriers and customer support · Finance (COD, carrier billing) · Carrier partners · Sellers/shippers · Legal (restricted goods) · IT (scanners, apps, integrations).
