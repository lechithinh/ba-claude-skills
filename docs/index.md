---
title: "Business Analyst Skills for Claude: Requirements, User Stories, Diagrams & Domain Knowledge"
description: "Free, open-source Claude skills for Business Analysts: requirements analysis and quality linting, user stories with Gherkin acceptance criteria, functional decomposition, BPMN/UML diagrams in Mermaid, plus Banking and E-commerce domain knowledge. BABOK-aligned, English & Vietnamese."
lang: en
alt_lang: vi
alt_url: /vi/
hide_title: true
---

<div class="hero">
  <img src="{{ '/assets/banner.png' | relative_url }}" alt="Business Analyst Skills for Claude — requirements, user stories, diagrams, banking and e-commerce domain knowledge">
  <h1>Business Analyst Skills for Claude</h1>
  <p class="lead">Open-source Claude skills that work like a senior Business Analyst: requirements analysis, user stories with Gherkin acceptance criteria, functional decomposition and BPMN/UML diagrams, <b>plus domain knowledge for Banking and E-commerce</b>.</p>
  <a class="btn primary" href="https://github.com/lechithinh/ba-claude-skills">★ Get it on GitHub</a>
  <a class="btn" href="#quick-start">Quick start</a>
  <a class="btn" href="{{ '/vi/' | relative_url }}">Tiếng Việt</a>
</div>

## Quick start

In Claude Code:

```bash
/plugin marketplace add lechithinh/ba-claude-skills
/plugin install ba-claude-skills@ba-claude-skills
```

Then describe your task and business context, for example: *"Write user stories with acceptance criteria for interbank transfer in our mobile banking app."* For Claude.ai, download the skill zips from [Releases](https://github.com/lechithinh/ba-claude-skills/releases) and upload them in **Settings → Capabilities → Skills**.

## Why domain knowledge matters

AI already knows *how to write* a requirement. A senior BA knows **what to ask** in a specific domain. For the same prompt, *"user story for interbank transfer"*, AI without context returns 2 scenarios: success and insufficient balance. With the banking domain pack you get 7, including beneficiary name inquiry, limits, biometric authentication above a threshold, **timeout → pending → reconciliation**, duplicate-submission protection and fees, plus open questions for Compliance.

[See the full before/after examples →](examples/domain-showcase/)

## Method skills {#skills}

<div class="cards">
  <div class="card"><h3><a href="{{ '/learn/meeting-to-requirements' | relative_url }}">Meeting → Requirements</a></h3><p>Transcripts become goals, functional and non-functional requirements, business rules and open questions, each traced to a quote.</p></div>
  <div class="card"><h3><a href="{{ '/learn/requirements-linter' | relative_url }}">Requirements Linter</a></h3><p>Scores each requirement 0–10 and flags vague, untestable and compound statements and missing domain scenarios, then rewrites them.</p></div>
  <div class="card"><h3><a href="{{ '/learn/functional-decomposition' | relative_url }}">Functional Decomposition</a></h3><p>System → modules → features → functions, with a Mermaid tree and a CRUD gap check.</p></div>
  <div class="card"><h3><a href="{{ '/learn/user-story-writer' | relative_url }}">User Story Writer</a></h3><p>INVEST user stories with Gherkin acceptance criteria, error paths and Jira CSV export.</p></div>
  <div class="card"><h3><a href="{{ '/learn/ba-diagrams' | relative_url }}">BA Diagrams</a></h3><p>Swimlane process, use case, sequence, ERD, state and context diagrams in valid Mermaid.</p></div>
</div>

## Domain packs {#domains}

<div class="cards">
  <div class="card"><h3><a href="{{ '/domains/banking/' | relative_url }}">🏦 Banking</a></h3><p>eKYC, accounts, transfers (NAPAS, CITAD), cards, lending, deposits, disputes: rules, checklist, data model, integrations, regulations, KPIs.</p></div>
  <div class="card"><h3><a href="{{ '/domains/ecommerce/' | relative_url }}">🛒 E-commerce</a></h3><p>Catalog, vouchers, checkout, payment, orders, shipping and COD, returns, marketplace settlement: rules, checklist, data model, integrations, regulations, KPIs.</p></div>
</div>

## Learn the BA techniques {#learn}

Each skill comes with a short guide to the technique behind it, with BABOK references, common mistakes and practice exercises:

- [Requirements quality checklist](learn/requirements-linter.md)
- [Functional decomposition](learn/functional-decomposition.md)
- [From meeting notes to requirements](learn/meeting-to-requirements.md)
- [User stories & Gherkin acceptance criteria](learn/user-story-writer.md)
- [Choosing the right BA diagram](learn/ba-diagrams.md)
- [Banking BA checklist](domains/banking/checklist.md) · [E-commerce BA checklist](domains/ecommerce/checklist.md)

## Examples

- [BPMN token simulation, AS-IS: the process that gets stuck (interactive)](demo/bpmn-token-as-is.html)
- [BPMN token simulation, TO-BE: the fix with a timer (interactive)](demo/bpmn-token-to-be.html)
- [Domain showcase: with vs without a domain pack](examples/domain-showcase/)
- [Clinic booking case study: from meeting transcript to user stories and diagrams](examples/clinic-booking/)

## FAQ

**Is it free?** Yes, MIT-licensed and open source.

**Does it invent business rules?** No. Unknown values are left as `[value — confirm]`, together with a list of open questions.

**Does it work in Vietnamese?** Yes. Skills reply in your language, and the domain packs include English–Vietnamese glossaries.

**Can I add my domain?** Yes. See the [contributing guide](https://github.com/lechithinh/ba-claude-skills/blob/main/CONTRIBUTING.md).
