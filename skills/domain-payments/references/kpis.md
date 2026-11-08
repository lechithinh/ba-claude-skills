# Payments KPIs

| KPI | Meaning | Requirement implications |
|---|---|---|
| TPV (total payment volume) | Value of successful payments | Define: gross or net of refunds? |
| Take rate | Revenue / TPV | Fee model and reporting |
| Success rate by method | Successful / attempted | Error-code tracking, method ranking |
| Pending rate and time-to-resolve | Share of payments stuck pending | Query/callback/reconciliation design |
| Cash-in / cash-out success rate | By source and bank | Per-bank monitoring |
| Reconciliation break rate and aging | Unmatched items and how old | Break workflow, tooling, SLA |
| Refund rate | Refunds / payments | Reason codes, abuse detection |
| Chargeback ratio | Chargebacks / card payments | Evidence collection, merchant risk |
| Settlement time | Capture to merchant payout | Cycle and cut-off design |
| Fraud loss rate | Fraud loss / TPV | Rule design and review queues |
| Active wallets / transacting users | MAU | Engagement features |
| Time to first transaction | After onboarding | Onboarding funnel |
