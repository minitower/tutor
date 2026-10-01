# Module 7 — Deterministic Design Systems for AI-Generated UI

## Why this module exists

An agent session has no memory of *why* it picked a given blue, spacing
scale, or font last time. If "the design" only exists as a chat
conversation, every new session re-derives it from vague adjectives
("modern," "clean") and produces a visibly different result. This is the
same problem Module 6 (DDD) solves for feature behavior, applied to
visuals: determinism comes from moving decisions out of the conversation
and into files the agent reads fresh every session, not from a prompting
trick.

## Learning objectives
- Externalize design decisions into artifacts an agent reads before
  generating any UI, instead of re-deriving them from adjectives each
  session
- Understand why concrete values (hex codes, a spacing scale, a type
  stack) are what buys determinism — descriptive language is exactly
  where session-to-session drift creeps in
- Close the loop with visual verification instead of trusting a text-only
  diff to catch design drift

## Key concepts

**1. Design tokens file — values, not prose.**
A real `tokens.css`/`tokens.json` (or equivalent) that the actual code
imports, not just documentation about the palette:
```css
:root {
  --color-bg: #0b0d10;
  --color-accent: #6ee7ff;
  --font-heading: "Inter", system-ui, sans-serif;
  --space-unit: 8px;
  --radius-base: 6px;
}
```
Because the tokens are consumed by the code, drift is structurally
harder — the agent has to touch the tokens file to introduce a new color,
which is a visible, reviewable change instead of a silent one.

**2. Design system doc — patterns and rationale.**
A short doc (one page, not a brand book): layout grid, breakpoints,
component states (hover/active/disabled), tone/voice, 1–2 reference
sites. This is the "why" that a tokens file alone can't carry.

**3. A repo-level rule that forces the check.**
Neither artifact helps if the agent doesn't know to look for it. This
belongs in `CLAUDE.md`/`AGENTS.md` as an explicit instruction, not an
assumption:
```md
## Design
Before any UI/styling work, read design/tokens.css and design/system.md.
Do not introduce new colors, fonts, or spacing values outside the tokens
file — extend the tokens file instead and use the new token.
```

**4. Package repeated design work as a Skill.**
If pages/components get built often, wrap "build a page following our
design system" as a Skill (Module 6.5 / [practice-tasks.md](../practice-tasks.md))
that always loads the tokens + system doc first. This makes the check
happen by construction instead of depending on memory.

**5. Verify visually, not just by reading the diff.**
Text-only review misses design drift. Render the page (dev server +
browser preview, or a screenshot) and compare against the design doc
every session — catch regressions immediately instead of after they
accumulate across weeks of sessions.

## Lab

1. Write a tokens file and a one-page design system doc for a small
   multi-page/multi-component UI (3–4 screens or components is enough).
2. Add the `CLAUDE.md`/`AGENTS.md` rule pointing at both.
3. **Session A:** in a fresh session, build the UI using only the tokens
   file, design doc, and repo rule — no additional verbal design
   guidance beyond the feature itself.
4. **Session B:** fresh session again (no memory of Session A), build a
   *different* page/component from the same UI using the same
   constraints. Screenshot both and compare visual consistency.
5. **Session C (control):** fresh session, same feature ask, but *without*
   pointing it at the tokens file or doc — just "make it look modern and
   consistent with the rest of the site." Screenshot and compare against
   A/B to see the drift directly.

## Deliverable
- The tokens file and design system doc
- The `CLAUDE.md`/`AGENTS.md` snippet
- Screenshots from Sessions A, B, and C
- A short writeup: where A and B matched, where C drifted, and whether
  any drift in A/B traces back to something the tokens/doc left
  underspecified (if so, that's a doc gap to close, same discipline as
  Module 6's spec-correction step)

## Discussion questions
- At what point does a design system doc become so detailed it's more
  expensive to maintain than the drift it prevents?
- Should design tokens live in the same spec as functional requirements,
  or stay a separate document with its own update cadence?
- How does this change for a design that's deliberately meant to vary
  (e.g. generative/artistic pages) rather than stay consistent?
