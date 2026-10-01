---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 7
## Deterministic Design Systems for AI-Generated UI

**Case study: Tokens + design docs for reproducible UI**

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->

## Agenda

1. Why this module exists
2. The core problem: drift from vague adjectives
3. Design tokens — values, not prose, and how they wire into a project
4. Design system doc — patterns and rationale
5. Repo-level enforcement rule
6. Packaging design work as a Skill — and how to write your own
7. Closing the loop with visual review, including agent-driven testing
8. Lab: Sessions A / B / C
9. Deliverable & discussion

---

<!-- Slide 3 -->

## Why this module exists

- An agent session has **no memory** of why it picked a given blue, spacing scale, or font last time
- If "the design" only lives in a chat conversation, every new session re-derives it from adjectives
- Same problem as Module 6 (DDD), applied to visuals:
  determinism comes from moving decisions into **files**, not from a prompting trick

---

<!-- Slide 4 -->

## Learning objectives

- Externalize design decisions into artifacts an agent reads **before** generating any UI
- Understand why **concrete values** (hex codes, spacing scale, type stack) buy determinism
- Close the loop with **visual verification**, not just a text-only diff

---

<!-- Slide 5 -->

## The core problem: "modern and clean"

- "Modern," "clean," "professional" — all underspecified
- Session A picks `#4f46e5`; Session B, with the same prompt, picks `#4338ca`
- Both are "modern indigo." Neither is wrong. They just don't **match**
- Vague adjectives aren't a communication failure you can prompt-engineer away —
  they're a category of instruction that has no single fixed answer

---

<!-- Slide 6 -->

## Key concept 1: Design tokens — values, not prose

A real `tokens.css` / `tokens.json` that the **code actually imports** —
not documentation *about* the palette.

```css
:root {
  --color-bg: #0b0d10;
  --color-accent: #6ee7ff;
  --font-heading: "Inter", system-ui, sans-serif;
  --space-unit: 8px;
  --radius-base: 6px;
}
```

---

<!-- Slide 7 -->

## Tokens: what makes this different from a style guide PDF

- Every value is machine-consumable and code references it: `color: var(--color-accent)`
- No interpretation step between "the design" and the rendered pixel
- A spacing *scale* (`--space-unit: 8px`, then `2x`, `3x`, `4x`...) beats ad hoc `margin: 14px`
- One file = one source of truth, not "the palette from three weeks ago"

---

<!-- Slide 8 -->

## Why tokens structurally prevent drift

- To introduce a new color, the agent must **edit `tokens.css`**
- That edit shows up in the diff — a human (or a review agent) can catch it
- Compare: a color baked directly into a component's inline style — invisible until you're staring at two screenshots side by side
- Determinism here isn't about a smarter model — it's about **removing the decision from the conversation entirely**

---

<!-- Slide 9 -->

## How a token actually lands in a project

- Adding a new token is one line in `tokens.css`: `--color-accent-2: #22c55e;`
- HTML/CSS pick it up immediately via `var(--color-accent-2)` — no separate build step
- An agent hooks in the same way a person does: the `CLAUDE.md` rule says to read `design/tokens.css` before any styling work

```
design/
  tokens.css   # source of truth — imported by index.html
  system.md    # patterns and rationale (Key concept 2)
```

---

<!-- Slide 10 -->

## Key concept 2: Design system doc — patterns and rationale

A short doc — **one page, not a brand book**:

- Layout grid & breakpoints
- Component states: hover / active / disabled / error
- Tone / voice
- 1–2 reference sites ("look like this, not like that")

Tokens say *what*. This doc says *why* and *how they combine*.

---

<!-- Slide 11 -->

## What belongs in the doc (and what doesn't)

**In:**
- "Cards use `--radius-base`, 1px border in `--color-border`, shadow only on hover"
- "Primary actions are always `--color-accent`; never more than one per screen"

**Out:**
- A restatement of the tokens file (redundant, goes stale)
- Full brand mythology, logo-usage rules, marketing copy guidelines

---

<!-- Slide 12 -->

## Key concept 3: A repo-level rule that forces the check

Neither artifact helps if the agent doesn't know to look for it.
This is an **explicit instruction**, not an assumption.

```md
## Design
Before any UI/styling work, read design/tokens.css and
design/system.md. Do not introduce new colors, fonts, or
spacing values outside the tokens file — extend the tokens
file instead and use the new token.
```

Lives in `CLAUDE.md` / `AGENTS.md` — read at the start of every session.

---

<!-- Slide 13 -->

## Why you need all three, not just one

| Artifact alone | Failure mode |
|---|---|
| Tokens, no rule | Agent never opens the file; invents new hex codes anyway |
| Doc, no tokens | "Use a calm blue" is still an adjective in disguise |
| Rule, no artifacts | Agent dutifully looks — and finds nothing to enforce |

The rule is the **hook**; tokens + doc are what it hooks *into*.

---

<!-- Slide 14 -->

## Key concept 4: Package repeated design work as a Skill

- If pages/components get built often, "build a page following our design system" becomes a repeatable request
- Wrap it as a **Skill** (`SKILL.md`) that *always* loads the tokens + system doc first, before writing any markup
- Moves enforcement from "the agent remembered the `CLAUDE.md` rule" to **"the workflow can't run without it"**

---

<!-- Slide 15 -->

## Skill vs. rule: enforcement by construction

- A repo rule depends on the agent choosing to follow it that session
- A Skill's steps are baked into *how the task gets done at all*
- Same relationship as Module 6's spec → plan → implementation loop, applied to a narrower, repeatable job
- Good candidate once you've built the same *kind* of page 2–3 times by hand

---

<!-- Slide 16 -->

## What a Skill is made of: SKILL.md and a folder

- A Skill is a folder, not a single file: `SKILL.md` plus, when needed, `references/*.md` for detail that doesn't need to load into context every time
- `SKILL.md` opens with frontmatter — `name`, `description` — the agent decides whether to load the Skill at all based on that description
- The body is plain markdown: which files to read first, steps, example components

```
.claude/skills/
  write-slides-html/
    SKILL.md
    references/
      components.md
      icons.md
```

---

<!-- Slide 17 -->

## Claude can write a Skill for you

- A Skill is just another file in the repo — which means you can ask an agent to write one instead of authoring it by hand
- A ready-made meta-skill, `skill-creator`, walks through the structure, the `description` wording, and checking it actually triggers
- Same logic as Key concept 4, applied to the act of writing Skills itself: give a procedure instead of explaining it once in chat

*The `write-slides-html` Skill Claude just used to edit this very slide was itself written through that procedure.*

---

<!-- Slide 18 -->

## Key concept 5: Verify visually, not just by reading the diff

- A clean-looking code diff can still **render wrong**: a token used in the wrong context, a state that was never styled
- Text-only review misses this category of bug entirely
- Render the page — dev server + browser preview, or a screenshot — every session
- Compare against the design doc's reference sites and component states

---

<!-- Slide 19 -->

## An agent can visually test too

- Key concept 5 said "render and compare" — an agent can do that itself, not just a person
- The agent spins up a dev server, opens the page in a browser, takes a screenshot, and reads the DOM programmatically
- Checks don't have to be "by eye": `element.scrollHeight <= element.clientHeight` catches overflow automatically, no human deciding "looks fine"

*This course uses that exact verification loop on its own slides — a working example of agent-driven visual testing.*

---

<!-- Slide 20 -->

## Closing the loop

```
tokens.css + system.md  →  repo rule (CLAUDE.md/AGENTS.md)
        │                          │
        └────────► agent generates UI ◄────────┘
                         │
                    render / screenshot
                         │
              compare against design doc
                         │
              gap found? → fix the doc, not just the page
```

---

<!-- Slide 21 -->

## Lab: three sessions, one UI

1. Write a tokens file + one-page design doc for a small multi-page UI (3–4 screens/components)
2. Add the `CLAUDE.md`/`AGENTS.md` rule pointing at both
3. **Session A** — fresh session, build using *only* tokens + doc + rule
4. **Session B** — fresh session, no memory of A, build a *different* page, same constraints
5. **Session C (control)** — fresh session, same ask, *no* tokens/doc — just "make it look modern and consistent"

---

<!-- Slide 22 -->

## Lab: what to actually compare

- Screenshot A, B, and C side by side
- Where do A and B **match** — same accent color, same spacing rhythm, same corner radius?
- Where does C **drift** — different blue, different button shape, inconsistent spacing?
- If A and B *also* disagree somewhere: that's not the lab failing —
  it's a **gap in the tokens/doc** you need to close

---

<!-- Slide 23 -->

## Deliverable

- The tokens file and design system doc
- The `CLAUDE.md`/`AGENTS.md` snippet
- Screenshots from Sessions A, B, and C
- A short writeup: where A/B matched, where C drifted, and whether any A/B mismatch traces back to an underspecified doc

---

<!-- Slide 24 -->

## Discussion questions

- When does a design doc get so detailed it costs more to maintain than the drift it prevents?
- Should tokens live with functional specs, or stay separate with their own update cadence?
- How does this change for designs meant to *vary* — generative or artistic pages?

---

<!-- Slide 25 -->

## Recap

- Vague adjectives are where session-to-session drift comes from — not a prompting problem, a **specification** problem
- Tokens (values) + design doc (rationale) + repo rule (enforcement) + Skill (construction) + visual review (verification) — five layers, each closing a different gap
- Same discipline as Module 6's DDD, aimed at pixels instead of behavior

---

<!-- Slide 26 -->

## Next module

**Module 8 — Plan-First Workflows**

Separating *planning* from *execution*: approval gates, ADRs, and why an
ephemeral plan solves a different problem than a durable spec or a
tokens file.
