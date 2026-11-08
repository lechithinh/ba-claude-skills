# Consumer lending business-rule patterns

All values are configurable - confirm with product, risk and Compliance.

1. **Eligibility**: age, residency, income minimum, employment status, existing exposure, blacklist; reasons returned to the customer must be compliant.
2. **Decisioning**: policy rules first (hard knock-outs), then score cut-offs (approve / review / reject), then approval authority by amount and risk. Model this as a **decision table**.
3. **Interest method**: state clearly **flat vs reducing balance**; always compute and display the **effective annual rate** for comparison. Rounding rule (VND has no decimals) and day-count convention.
4. **Schedule**: equal installments (annuity) vs equal principal; first due date rule; **due date on a non-business day** moves to next/previous business day [confirm]; last installment absorbs rounding.
5. **Repayment allocation order**: typically fees and penalty, then interest, then principal [confirm order]; define for partial payments and overpayments.
6. **Late payment**: penalty interest base and rate, grace days, cap, fee per reminder [confirm legality]; DPD counting starts after due date.
7. **Auto-debit**: retry schedule, partial debit allowed or not, source account validation, mandate expiry.
8. **Early repayment**: payoff quote with validity date; fee by period; recalculation method; minimum amount.
9. **Partial prepayment**: reduce term or reduce installment, customer chooses [confirm].
10. **Restructuring**: eligibility, max number, effect on DPD/classification and credit reporting.
11. **Disbursement**: only after signed contract and passed checks; verify beneficiary name; fee deduction timing; idempotent payout; failed payout handling.
12. **Cancellation / cooling-off**: window, refund of fees [confirm applicability].
13. **Debt classification and provisioning**: groups driven by DPD and other criteria; changes trigger reports.
14. **Authority and audit**: maker-checker for manual changes, overrides, waivers; full audit trail.
15. **Data and consent**: consent to bureau inquiry and data sharing recorded with time and version of text.
