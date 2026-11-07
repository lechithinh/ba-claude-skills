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
| Draw process, use case, sequence, ERD, state or context diagrams | `skills/ba-diagrams/SKILL.md` |

## Domain packs
If the context is a business domain below, ALSO read the domain `SKILL.md` and the reference files it points to (only the ones needed for the task).

| Context | Read |
|---|---|
| Bank, digital/mobile banking, transfers, cards, loans, deposits, eKYC | `skills/domain-banking/SKILL.md` |
| Online store, marketplace, checkout, orders, vouchers, shipping, COD, returns | `skills/domain-ecommerce/SKILL.md` |

## Conventions
- Reply in the user's language (Vietnamese or English).
- Never invent business facts — use `[value — confirm]` placeholders.
- Diagrams are Mermaid code blocks.
