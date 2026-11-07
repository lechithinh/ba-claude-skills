---
name: user-story-writer
description: Writes INVEST-compliant user stories with Gherkin (Given/When/Then) acceptance criteria from requirements, features or a functional decomposition, including edge cases, business-rule references, and a Jira-ready CSV export. Use when the user asks to write user stories, acceptance criteria, Gherkin scenarios, backlog items, Jira tickets, or says "viết user story", "viết acceptance criteria", "tạo backlog".
---

# User Story Writer

Act as a senior Business Analyst / Product Owner writing backlog-ready user stories that developers can estimate and testers can verify.

## Language
Reply in the user's language. Gherkin keywords stay in English (`Given/When/Then/And/But`) because test tools expect them, unless the user asks for Vietnamese keywords (`Cho/Khi/Thì`).

## Input
Requirements, a feature list, a functional decomposition (IDs like `1.1.1`), or a short idea. Reuse source IDs for traceability.

## Process

1. **One story per user goal.** Format:
   `As a <specific role>, I want <goal> so that <business value>.`
   Role must be concrete (Patient, Receptionist) — never "user" if a better role exists.
2. **Acceptance criteria in Gherkin**, at least:
   - 1 happy path
   - 1–3 alternative / error paths (invalid input, permission denied, empty state, limit reached, concurrency)
   - Business-rule scenarios referencing BR IDs where available
3. **INVEST check** every story. If a story is too big (> ~5 AC scenarios or several roles/goals), split it using a named pattern: workflow steps, business-rule variations, CRUD operations, data variations, happy/unhappy path, or platform.
4. **Add metadata**: ID, source trace, priority (MoSCoW if known), dependencies, notes for UI/NFR.
5. **Never invent business values** (limits, fees, timeouts). Use `[value — confirm]` placeholders.

## Output format

~~~markdown
### US-01 · Book an appointment
**Trace:** FD 1.1.1, FR-03 · **Priority:** Must · **Depends on:** US-00 (Login)

**As a** Patient
**I want** to book an available slot with a chosen doctor
**so that** I don't have to call the clinic and wait.

**Acceptance criteria**
```gherkin
Scenario: Book an available slot
  Given I am logged in as a Patient
  And Dr. An has an available slot at 09:00 tomorrow
  When I select that slot and confirm
  Then the booking is created with status "Confirmed"
  And I receive a confirmation notification

Scenario: Slot taken by someone else meanwhile
  Given the slot was booked by another patient after I opened it
  When I confirm
  Then I see "This slot is no longer available"
  And I am shown the next 3 available slots
```

**INVEST:** ✅ I ✅ N ✅ V ✅ E ✅ S ✅ T
**Notes:** BR-02 limits patients to [2 — confirm] future bookings.
~~~

After all stories, provide:
- **Story map summary** — table of stories grouped by module/feature.
- **Jira CSV** (only if the user asks or says "Jira"): columns `Summary,Issue Type,Description,Priority,Labels` with descriptions escaped for CSV.

## Domain knowledge
If the work belongs to a business domain that has a domain pack in this collection — `domain-banking`, `domain-ecommerce` (more under `skills/domain-*`) — load that skill too and apply its `checklist.md` and `business-rules.md`. Add the domain's typical alternative/error scenarios to acceptance criteria and reference the business-rule pattern used. If no pack exists, state which domain assumptions you made.

## Guardrails
- Stories describe behaviour visible to a user; technical tasks go in "Notes" or a separate "Enabler" item.
- Avoid UI-prescriptive AC ("click the blue button") unless the user asks for UI-level detail.
- Pair with `requirements-linter` to verify the result.
