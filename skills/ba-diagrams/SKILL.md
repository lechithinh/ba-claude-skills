---
name: ba-diagrams
description: Creates Business Analysis diagrams as Mermaid code — process flows (BPMN-style swimlanes), use case diagrams, sequence diagrams, ERDs, state diagrams, context diagrams and data flow — and picks the right diagram for the question being asked. Use when the user asks to draw, model, visualize or diagram a business process, As-Is/To-Be flow, use case, system interaction, data model or status lifecycle, or says "vẽ sơ đồ", "vẽ quy trình", "vẽ use case", "vẽ ERD", "sơ đồ trạng thái".
---

# BA Diagrams

Act as a senior Business Analyst who chooses the **right** model for the audience, then draws it as valid Mermaid code that renders on GitHub, Notion, Confluence (Mermaid plugin), GitLab and mermaid.live.

## Language
Labels in the user's language. Keep node IDs ASCII (`A1`, `checkSlot`) and put Vietnamese text inside quoted labels: `A1["Kiểm tra lịch trống"]`.

## Step 1 — Choose the diagram

| The question is… | Use | Mermaid type |
|---|---|---|
| Who does what, in which order, across roles? | Swimlane process flow (BPMN-style) | `flowchart LR` + `subgraph` per lane |
| What can each actor do with the system? | Use case diagram | `flowchart LR` with actor nodes and a system boundary `subgraph` |
| How do systems/components talk over time? | Sequence diagram | `sequenceDiagram` |
| What data do we store and how is it related? | ERD | `erDiagram` |
| What statuses does an object go through? | State diagram | `stateDiagram-v2` |
| What is inside vs outside the system? | Context diagram | `flowchart` with the system in the center |
| What does the scope hierarchy look like? | Use the `functional-decomposition` skill | — |

If the user's request is ambiguous, pick the best fit, say why in one line, and offer the alternative.

## Step 2 — Model rules
- **Process flows**: one start, explicit end(s); decisions are diamonds `{"Còn chỗ?"}` with labelled exits (`-->|Yes|`); one lane per role; activities are verb-noun.
- **As-Is vs To-Be**: draw both when asked to improve a process, and list the changes (removed steps, automated steps, pain points fixed).
- **Use case**: actors outside the boundary; use cases as rounded nodes `UC1(["Đặt lịch"])`; show `<<include>>`/`<<extend>>` as labelled dotted edges `-.->|include|`.
- **Sequence**: name participants by role/system; show the error path with `alt`/`else`.
- **ERD**: entities singular, PK/FK marked, cardinality explicit (`||--o{`).
- **State**: every state reachable; terminal states go to `[*]`; transitions labelled with the triggering event.

## Step 3 — Output

1. One-line purpose of the diagram and audience.
2. The Mermaid code block.
3. A short **legend / notes**: assumptions, open questions, things deliberately left out.
4. Offer the next useful diagram (e.g. after a process flow → the state diagram of the main object).

## Mermaid safety checklist (avoid render errors)
- Quote any label containing `( ) [ ] { } : ; , " / #` or non-ASCII → `A["Huỷ lịch (trước 2h)"]`.
- Do not use `end` as a node ID (reserved); use `endNode`.
- No HTML except `<br/>` for line breaks.
- Keep ≤ 30 nodes per diagram; split large processes into sub-processes.
- `erDiagram` attribute types must be a single word (`string`, `int`, `datetime`).
