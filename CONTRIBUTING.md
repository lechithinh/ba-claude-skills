# Contributing / Đóng góp

Thanks for helping Business Analysts work better with AI! 🙌 Contributions in English or Vietnamese are both welcome.

## Ways to contribute
- **Request a skill** → open an issue with the *Skill request* template.
- **Improve a skill** → better rules, edge cases, examples, Vietnamese wording.
- **Add an example** → a real-world (anonymized!) input + output under `examples/`.
- **Add a new skill** → follow the steps below.

## Adding a new skill
1. Pick an item from [ROADMAP.md](ROADMAP.md) or propose one in an issue first.
2. Copy the template:
   ```bash
   mkdir skills/<skill-name>
   cp templates/SKILL_TEMPLATE.md skills/<skill-name>/SKILL.md
   ```
3. Fill in:
   - `name`: kebab-case, same as the folder name.
   - `description`: **what it does + when to use it**, including trigger phrases in English *and* Vietnamese. This is what Claude reads to decide whether to load the skill.
4. Add `LEARN.md` explaining the BA technique (BABOK reference, common mistakes, a practice exercise).
5. Test it: run the skill on at least **2 different inputs** in Claude Code or Claude.ai and paste one result in your PR.
6. Update the skill tables in `README.md`, `README.vi.md` and `ROADMAP.md`.

## Adding or improving a domain pack ⭐
Domain knowledge from practitioners is the most valuable contribution.
1. Open an issue "Domain: <name>" to claim it and avoid duplicate work.
2. Copy the template: `cp -r templates/DOMAIN_TEMPLATE skills/domain-<name>` and use `skills/domain-banking` as the reference example.
3. Fill all 8 reference files. Prioritize **`checklist.md`** (questions a senior BA always asks) and **`business-rules.md`** (patterns, with values as `[confirm]`).
4. `regulations.md` must have a **Last reviewed** date, cite each document, and never present a regulation as legal advice.
5. Write generic industry practice — **no confidential employer/client information**.
6. Add a before/after showcase in `examples/domain-showcase/`.

**Domain maintainers** review PRs for their pack and are credited in the pack's `SKILL.md` and in the README.

## Quality bar for skills
- ✅ Has a clear **process** (numbered steps) and an **output format**.
- ✅ Never invents business facts — uses `[value — confirm]` placeholders.
- ✅ Mermaid output follows the safety checklist in `skills/ba-diagrams/SKILL.md`.
- ✅ Works in both English and Vietnamese.
- ✅ Keeps `SKILL.md` focused (ideally < 200 lines); put long references in extra files inside the skill folder.
- ❌ No confidential client data in examples.

## Website (GitHub Pages)
The site at https://lechithinh.github.io/ba-claude-skills/ is built from `docs/`. Learn pages, domain reference pages and examples are **generated** — after editing a `LEARN.md`, a domain reference or an example, run:
```bash
python3 scripts/build_docs.py
```
and commit the changes in `docs/`. When adding a new skill or domain, add its SEO title and description in `scripts/build_docs.py`.

## Pull requests
- One skill or one topic per PR.
- Describe what you changed and show a before/after if you improved an existing skill.
