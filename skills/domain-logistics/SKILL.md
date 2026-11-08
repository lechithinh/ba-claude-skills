---
name: domain-logistics
description: Logistics and fulfillment domain knowledge for Business Analysts - glossary, core processes (order intake, first-mile pickup, hub sorting, last-mile delivery, failed delivery and return-to-sender, COD collection and remittance, returns, warehouse inbound/putaway/pick/pack/outbound, inventory control, carrier management and rate cards, tracking, claims), business rules (volumetric and chargeable weight, zone pricing, delivery attempts, COD limits, status model, inventory reservation, SLA), data model with status sets, integrations (OMS/e-commerce, carriers, maps/geocoding, scanners, payment/bank for COD), regulatory touchpoints and a BA question checklist. Use together with any BA task whenever the context is parcel delivery, courier, 3PL, warehouse (WMS), transportation (TMS), last mile, COD or fulfillment - or the user mentions "vận chuyển", "giao hàng", "kho", "WMS", "TMS", "vận đơn", "COD", "đối soát COD", "giao thất bại", "hoàn hàng", "chặng cuối", "đơn vị vận chuyển".
---

# Domain Pack: Logistics & Fulfillment / Vận chuyển và kho vận

This skill adds **domain knowledge** on top of the BA method skills (`meeting-to-requirements`, `requirements-linter`, `functional-decomposition`, `user-story-writer`, `decision-table`, `edge-case-finder`, `api-spec`, `screen-spec`, `bpmn-modeling`, `ba-diagrams`). It makes their output *logistics-correct*. For the selling side (checkout, orders, returns policy) also load `domain-ecommerce`; for cash collected on delivery and settlement also see `domain-payments`.

## How to use the references
| Task | Read |
|---|---|
| Terminology | `references/glossary.md` |
| Decompose functions, draw processes | `references/processes.md` |
| Requirements, stories, AC, **decision tables** (pricing, routing) | `references/business-rules.md` + `references/checklist.md` |
| ERD, API payloads, status sets | `references/data-model.md` |
| Context/sequence diagrams, integration specs | `references/integrations.md` |
| Compliance | `references/regulations.md` |
| Goals, reports | `references/kpis.md` |

## How to apply domain knowledge
1. **Identify the role and scope**: shipper/seller, carrier (courier), 3PL warehouse, marketplace logistics, or in-house fleet; parcels or pallets; first/middle/last mile; warehouse only. It changes almost every rule.
2. **Add the scenarios a logistics BA never forgets**: **failed delivery and retry limits**, return-to-sender, **COD collected but not remitted**, wrong or unnormalised address, parcel lost/damaged claim, weight disputes (actual vs volumetric), partial delivery, split shipment, reroute, scan gaps, inventory mismatch after counting.
3. **Think in event streams**: tracking events and handover scans are the facts; statuses are derived.
4. **Ask, don't invent**: rate cards, divisors, retry counts, COD limits and claim windows are commercial decisions -> `[value - confirm]`.
5. **Flag regulatory touchpoints** (restricted/dangerous goods, personal data of recipients, COD handling, vehicle and driver rules) with *"verify the current regulation with Legal/Compliance"*.

## Guardrails
- Generic typical practice (Vietnam focus); each carrier or warehouse differs. Do not name a carrier as required unless the user did.
- `references/regulations.md` has a "last reviewed" date and lists topics to ask about, not legal conclusions.
- Mask recipient names, phone numbers and addresses in examples.
