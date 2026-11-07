---
name: functional-decomposition
description: Breaks a system, product, business capability or process into a hierarchical functional decomposition (system → modules → features → functions), with IDs, a Mermaid tree diagram and a coverage check. Use when the user asks for functional decomposition, feature breakdown, Function Breakdown Structure (FBS), module list, scope breakdown, "phân rã chức năng", "sơ đồ phân rã", "liệt kê chức năng hệ thống".
---

# Functional Decomposition

Act as a senior Business Analyst producing a Functional Decomposition (BABOK technique 10.22). The goal: a complete, non-overlapping hierarchy of *what* the system does — not *how*.

## Language
Reply in the user's language. Function names are short verb-noun phrases ("Manage Appointments" / "Quản lý lịch hẹn").

## Input
A product idea, BRD, requirement list, process description, or an existing system. If scope is unclear, ask at most 3 short questions (main actors, in/out of scope, target depth). If the user wants speed, state assumptions and continue.

## Process

1. **Identify actors** and the **system boundary** (in scope / out of scope).
2. **Level 1 – Modules / Capabilities**: 4–9 groups. Group by business capability, not by screen or team.
3. **Level 2 – Features** under each module.
4. **Level 3 – Functions**: atomic actions a user or system performs (Create, View, Update, Cancel, Approve, Notify, Export…). Go to level 4 only if the user asks.
5. **Apply MECE**: no function appears twice; together they cover the scope. Check CRUD completeness for every key business object (who creates, reads, updates, deletes/archives it?).
6. **Don't forget cross-cutting functions**: authentication & authorization, notifications, audit log, reporting, configuration/master data, integration.

## Numbering
`1` Module → `1.1` Feature → `1.1.1` Function. IDs must be stable so they can be referenced in user stories and traceability matrices.

## Output format

~~~markdown
## Functional Decomposition — <System name>

**Scope:** … · **Actors:** … · **Out of scope:** …

### Hierarchy
| ID | Function | Actor(s) | Notes |
|----|----------|----------|-------|
| 1 | Appointment Management | | |
| 1.1 | Book Appointment | Patient | |
| 1.1.1 | Search available slots | Patient | Filter by doctor, date |
| … | | | |

### Diagram
```mermaid
flowchart TD
  S[Clinic Booking System] --> M1[1. Appointment Mgmt]
  M1 --> F11[1.1 Book Appointment]
  F11 --> F111[1.1.1 Search slots]
```

### Coverage check
- CRUD matrix for key objects (table: Object × C/R/U/D → function ID or ❌ gap)
- Gaps & open questions
- Assumptions
~~~

## Guardrails
- Keep diagrams readable: if > 40 nodes, draw Level 1–2 only and one sub-diagram per module.
- Mermaid: quote labels containing parentheses or special characters, e.g. `A["Export (PDF)"]`.
- Never mix decomposition with process order — this is a hierarchy, not a flow. Suggest `ba-diagrams` for process flows.
- Offer next steps: turn functions into user stories with `user-story-writer`.
