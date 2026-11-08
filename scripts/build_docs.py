#!/usr/bin/env python3
"""Generate GitHub Pages content in docs/ from the skills and examples in this repo.

Run from the repo root after editing any LEARN.md, domain reference or example:
    python3 scripts/build_docs.py

Hand-written pages (docs/index.md, docs/vi/index.md, docs/domains/*/index.md,
docs/_layouts, docs/_config.yml) are not touched.
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "https://github.com/lechithinh/ba-claude-skills"

LEARN = {
    "requirements-linter": (
        "Requirements Quality Checklist for Business Analysts (Chất lượng yêu cầu)",
        "How to write unambiguous, testable requirements: the most common defects, BABOK Verify Requirements, examples in English and Vietnamese, plus an AI requirements linter for Claude.",
    ),
    "functional-decomposition": (
        "Functional Decomposition for Business Analysts (Phân rã chức năng)",
        "What functional decomposition is, when to use it, MECE and CRUD rules of thumb, common mistakes, and a Claude skill that builds the decomposition and diagram for you.",
    ),
    "meeting-to-requirements": (
        "From Meeting Notes to Requirements: Elicitation Guide (Trích xuất yêu cầu từ biên bản họp)",
        "Turn stakeholder interviews and meeting transcripts into goals, functional and non-functional requirements, business rules and open questions, traced to quotes.",
    ),
    "user-story-writer": (
        "User Stories & Gherkin Acceptance Criteria: INVEST Guide (Cách viết user story)",
        "How to write INVEST user stories with Given/When/Then acceptance criteria, splitting patterns and common mistakes, with a Claude skill that writes them.",
    ),
    "ba-diagrams": (
        "Choosing the Right BA Diagram: BPMN, Use Case, Sequence, ERD, State (Sơ đồ cho BA)",
        "Which diagram answers which stakeholder question, BABOK references, and how to draw BA diagrams in Mermaid with Claude.",
    ),
}

DOMAIN_REFS = {
    "banking": {
        "glossary": ("Banking Glossary for Business Analysts (Thuật ngữ ngân hàng Anh–Việt)", "40+ banking terms every BA needs, in English and Vietnamese: CIF, CASA, cut-off, name inquiry, reconciliation, maker-checker, DPD, CIC and more."),
        "processes": ("Core Retail Banking Processes for BAs (Quy trình nghiệp vụ ngân hàng)", "Capability map and key processes: eKYC onboarding, fund transfers, cards, lending, term deposits, disputes and end-of-day, with BA watch-outs."),
        "business-rules": ("Banking Business Rule Patterns: Limits, Cut-off, Authentication, Reconciliation", "Reusable banking business-rule patterns for requirements: limits, threshold-based authentication, cut-off, timeout and pending status, maker-checker, fees, interest."),
        "checklist": ("Banking BA Checklist: Questions to Ask Stakeholders (Câu hỏi BA ngân hàng)", "The questions a senior banking BA always asks for transactions, onboarding, cards, lending and non-functional requirements."),
        "data-model": ("Banking Data Model & Status Sets for Business Analysts", "Reference ERD for customers, accounts, transactions, cards and loans, plus status code sets and data sensitivity."),
        "integrations": ("Banking Integration Landscape: Core Banking, NAPAS, CITAD, CIC", "Typical banking integrations and the questions a BA should ask about timeouts, idempotency, error mapping and reconciliation."),
        "regulations": ("Banking Regulatory Touchpoints in Vietnam for BAs", "Regulatory topics a banking BA must raise with Compliance: online banking security, biometric authentication, eKYC, cards, AML, personal data."),
        "kpis": ("Banking KPIs Every Business Analyst Should Know", "CASA, NIM, NPL, onboarding conversion, transaction success rate, STP rate and more, with requirement implications."),
    },
    "ecommerce": {
        "glossary": ("E-commerce Glossary for Business Analysts (Thuật ngữ TMĐT Anh–Việt)", "E-commerce and marketplace terms for BAs in English and Vietnamese: SKU, OMS, WMS, ATS, COD, RTS, settlement, GMV, AOV and more."),
        "processes": ("Core E-commerce Processes for BAs (Quy trình nghiệp vụ TMĐT)", "Capability map and key processes: checkout, payment, order lifecycle, fulfillment, shipping, returns and marketplace seller flow."),
        "business-rules": ("E-commerce Business Rule Patterns: Vouchers, Inventory, Orders, Refunds", "Business-rule patterns for pricing, promotion stacking, inventory reservation, split orders, shipping, refunds, returns and marketplaces."),
        "checklist": ("E-commerce BA Checklist: Questions to Ask Stakeholders (Câu hỏi BA TMĐT)", "The questions a senior e-commerce BA always asks about checkout, promotions, payment, orders, returns, marketplaces and peak events."),
        "data-model": ("E-commerce Data Model & Order Status Sets for Business Analysts", "Reference ERD for products, SKUs, inventory, orders, payments, shipments and refunds, plus order, payment, shipment and return status sets."),
        "integrations": ("E-commerce Integration Landscape: Payments, Carriers, E-invoice, Marketplaces", "Typical e-commerce integrations in Vietnam and the questions a BA should ask about source of truth, sync and reconciliation."),
        "regulations": ("E-commerce Regulatory Touchpoints in Vietnam for BAs", "Regulatory topics an e-commerce BA must raise with Legal: e-commerce operations, consumer protection, e-invoices, seller tax, personal data, promotions."),
        "kpis": ("E-commerce KPIs Every Business Analyst Should Know", "GMV, conversion, AOV, cart abandonment, payment success, cancellation, COD refusal, return rate and more, with requirement implications."),
    },
}

EXAMPLES = {
    "domain-showcase": "Domain showcase: same prompt with and without a domain pack",
    "clinic-booking": "Case study: clinic booking app from meeting transcript to user stories",
}


def esc(s: str) -> str:
    return s.replace('"', '\\"')


# Tags that really are HTML; anything else written like <role> in the source is a text placeholder.
KNOWN_TAGS = {"a", "abbr", "b", "br", "code", "details", "div", "em", "figure", "figcaption", "h1", "h2", "h3", "h4",
              "h5", "h6", "hr", "i", "img", "kbd", "li", "mark", "ol", "p", "pre", "s", "small", "span", "strong",
              "sub", "summary", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul", "svg", "path"}
TAG = re.compile(r"<(/?)([A-Za-z][\w:-]*)((?:\s[^<>]*)?)>")


def escape_placeholders(line: str) -> str:
    """Turn <role>, <short name>, <value> into literal text; keep real HTML tags and anything inside `code`."""
    parts = re.split(r"(`+[^`]*`+)", line)
    for i in range(0, len(parts), 2):          # even indexes are outside code spans
        parts[i] = TAG.sub(lambda m: m.group(0) if m.group(2).lower() in KNOWN_TAGS
                           else "&lt;" + m.group(0)[1:-1] + "&gt;", parts[i])
    return "".join(parts)


def normalize_markdown(body: str) -> str:
    """Make GitHub-flavoured Markdown safe for kramdown (GitHub Pages).

    GitHub accepts a table or list written directly under a heading or paragraph; kramdown does not and prints the
    raw pipes. So: a blank line before every table, list and fenced block that follows text, a blank line after every
    heading, and angle-bracket placeholders escaped. Fenced code blocks are left untouched."""
    out, fence = [], None
    lines = body.split("\n")
    is_table = lambda s: s.lstrip().startswith("|")
    is_list = lambda s: bool(re.match(r"\s*([-*+]|\d+[.)])\s+\S", s))
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if fence:
            out.append(line)
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(line)
            fence = stripped[:3]
            continue
        prev = out[-1] if out else ""
        starts_block = (is_table(line) and not is_table(prev)) or (is_list(line) and not is_list(prev)
                                                                    and not prev.startswith(" ") and not is_table(prev))
        if prev.strip() != "" and starts_block:
            out.append("")                      # blank line before a table / list that follows text
        if prev.lstrip().startswith("#") and line.strip() != "":
            out.append("")                      # blank line after a heading
        if is_table(prev) and line.strip() != "" and not is_table(line):
            out.append("")                      # blank line after a table
        out.append(escape_placeholders(line))
    return "\n".join(out)


def page(path: pathlib.Path, title: str, description: str, body: str, lang: str = "en", footer: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = f'---\ntitle: "{esc(title)}"\ndescription: "{esc(description)}"\nlang: {lang}\n---\n\n'
    # Drop the source H1 (the layout renders the title) and protect content from Liquid.
    body = re.sub(r"\A\s*# .*\n", "", body, count=1)
    body = normalize_markdown(body)
    path.write_text(front + "{% raw %}\n" + body.strip() + "\n{% endraw %}\n" + footer)


def cta(skill_path: str) -> str:
    return (
        "\n---\n\n"
        f"**Use this with Claude:** install the plugin with `/plugin marketplace add lechithinh/ba-claude-skills`, "
        f"or read the skill source on [GitHub]({REPO}/blob/main/{skill_path}).\n"
    )


def main() -> None:
    # Learn pages
    learn_dir = DOCS / "learn"
    shutil.rmtree(learn_dir, ignore_errors=True)
    for skill, (title, desc) in LEARN.items():
        src = (ROOT / "skills" / skill / "LEARN.md").read_text()
        page(learn_dir / f"{skill}.md", title, desc, src, footer=cta(f"skills/{skill}/SKILL.md"))

    # Domain reference pages
    for domain, refs in DOMAIN_REFS.items():
        for ref, (title, desc) in refs.items():
            src = (ROOT / "skills" / f"domain-{domain}" / "references" / f"{ref}.md").read_text()
            page(DOCS / "domains" / domain / f"{ref}.md", title, desc, src,
                 footer=cta(f"skills/domain-{domain}/SKILL.md"))

    # Examples (README.md -> index.md, sibling links rewritten)
    ex_dir = DOCS / "examples"
    shutil.rmtree(ex_dir, ignore_errors=True)
    for ex, ex_title in EXAMPLES.items():
        for src_file in sorted((ROOT / "examples" / ex).glob("*.md")):
            text = src_file.read_text().replace("(README.md)", "(index.md)")
            m = re.search(r"^# (.+)$", text, re.M)
            title = ex_title if src_file.name == "README.md" else (m.group(1) if m else src_file.stem)
            name = "index.md" if src_file.name == "README.md" else src_file.name
            page(ex_dir / ex / name, title, ex_title, text)

    print("docs generated")


if __name__ == "__main__":
    main()
