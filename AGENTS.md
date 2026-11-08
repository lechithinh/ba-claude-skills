# AGENTS.md

This repository contains Business Analysis skills written as Markdown instructions. Any AI coding agent (Claude Code, Cursor, Codex, Gemini CLI, etc.) can use them.

## How to use the skills
When the user asks for one of the tasks below, read the matching `SKILL.md` and follow its process and output format exactly.

| User intent | Read |
|---|---|
| Extract requirements from meeting notes / transcript | `skills/meeting-to-requirements/SKILL.md` |
| Review, lint, score or validate requirements / user stories | `skills/requirements-linter/SKILL.md` |
| Functional decomposition, feature breakdown, module list | `skills/functional-decomposition/SKILL.md` |
| Write user stories, acceptance criteria, Gherkin, Jira backlog | `skills/user-story-writer/SKILL.md` |
| Model a business process in BPMN 2.0 (pools, lanes, gateways, events), run token scenarios, AS-IS / TO-BE | `skills/bpmn-modeling/SKILL.md` |
| Draw use case, sequence, ERD, state or context diagrams (or a quick process draft) | `skills/ba-diagrams/SKILL.md` |
| Write a screen/UI specification from a mockup image or description | `skills/screen-spec/SKILL.md` |
| Turn business rules into a decision table; find missing or conflicting rule combinations | `skills/decision-table/SKILL.md` |
| Find edge cases, challenge a requirement or story ("what if…") | `skills/edge-case-finder/SKILL.md` |
| Draft an API contract / OpenAPI spec from requirements | `skills/api-spec/SKILL.md` |

## Domain packs
If the context is a business domain below, ALSO read the domain `SKILL.md` and the reference files it points to (only the ones needed for the task).

| Context | Read |
|---|---|
| Bank, digital/mobile banking, transfers, cards, loans, deposits, eKYC | `skills/domain-banking/SKILL.md` |
| Online store, marketplace, checkout, orders, vouchers, shipping, COD, returns | `skills/domain-ecommerce/SKILL.md` |
| E-wallet, payment gateway/PSP, QR payment, top-up, withdrawal, settlement, reconciliation | `skills/domain-payments/SKILL.md` |
| Consumer loans, BNPL, installment, origination, repayment, collections, credit bureau | `skills/domain-lending/SKILL.md` |
| Parcel delivery, courier, last mile, COD remittance, warehouse (WMS), fulfillment | `skills/domain-logistics/SKILL.md` |

## Conventions
- Reply in the user's language (Vietnamese or English).
- Never invent business facts — use `[value — confirm]` placeholders.
- Diagrams are Mermaid code blocks.
