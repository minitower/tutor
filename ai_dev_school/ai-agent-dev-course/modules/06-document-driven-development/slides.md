---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 6
## Document-Driven Development (DDD)

**Case study focus:** Spec docs as the source of truth

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->

## Agenda

- Why ambiguity is the #1 tax on agent work
- Anatomy of a spec an agent can actually execute against
- The loop: spec → plan → implementation → spec-update
- Repo-level agent docs vs. feature specs
- Common pitfalls (and how to avoid them)
- Lab: write a real spec, hand it to an agent, close the gaps

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

- Use a written spec as the **contract** an agent implements against
- Tell the difference between a spec that's too vague and one that's
  over-specified
- Run the full DDD loop, including the step teams usually skip
- Keep a spec a **living artifact**, not a one-time handoff
- Recognize when DDD is *not* the right tool for the job

---

<!-- Slide 4 -->

## The problem DDD solves

The single biggest source of wasted agent turns: **ambiguity**.

- Agent guesses at intent → builds the wrong thing
- You spend more time correcting than you'd have spent writing the
  intent down once
- The conversation where you "explained it" leaves no durable trace

DDD front-loads that cost into a **document** instead of a
**conversation** — and you keep the document.

---

<!-- Slide 5 -->

## What is Document-Driven Development?

> A written spec is the **primary interface** between human and agent
> for a piece of work.

The agent:
1. Reads the spec
2. Plans against it
3. Implements against it
4. Helps **update it** when reality diverges from the plan

The last part is the part teams skip. It's also the part that makes
this "document-driven" rather than "wrote a doc once."

---

<!-- Slide 6 -->

## Anatomy of a spec — overview

1. **Goal** — one paragraph, plain language
2. **Non-goals** — explicitly out of scope
3. **Interfaces / contracts** — what the agent must not invent
4. **Edge cases** — the ones you already know about
5. **Acceptance criteria** — testable, ideally literal commands/tests
6. **Open questions** — left for the agent to propose an answer to

Worked example on the next slides: *CSV export for a reports dashboard.*

---

<!-- Slide 7 -->

## Goal + Non-goals

```markdown
## Goal
Let a user export the currently filtered report rows to a CSV file,
matching the date range they've already selected on the dashboard.

## Non-goals
- No new file formats (CSV only, not XLSX/PDF)
- No server-side scheduled/emailed exports — synchronous,
  on-click download only
```

Non-goals are what save you from silent scope creep — they're as load
-bearing as the goal itself.

---

<!-- Slide 8 -->

## Interfaces / contracts

```markdown
## Interface
- A button labeled "Export CSV" next to the existing date-range picker
- Clicking it downloads a file named `report_<start>_<end>.csv`
- Columns match the currently visible table columns, in the same order
```

If it matters and you don't write it down, the agent invents it — and
its invention becomes the de facto contract the next reader has to
reverse-engineer.

---

<!-- Slide 9 -->

## Edge cases

```markdown
## Edge cases
- No rows in the selected range → header-only CSV, not an error
- Date range spans a DST transition → use UTC dates in filename and
  date columns, to avoid off-by-one-day bugs
- User has an active column filter (not just date range) → export
  respects it too, not just the date range
```

You already know these. Writing them down doesn't cost time — *not*
writing them down just moves the cost from "spec" to "debugging."

---

<!-- Slide 10 -->

## Acceptance criteria + Open questions

```markdown
## Acceptance criteria
- Exporting a known 3-row range produces exactly those 3 rows + header
- Exporting an empty range produces a header-only CSV, not a 500
- Filename matches `report_<start>_<end>.csv` using UTC dates

## Open questions
- Should the export button be disabled (vs. hidden) when there's no
  data? Leaving this to the agent to propose in the plan step.
```

Open questions marked explicitly keep the spec from becoming a
straitjacket — they invite a proposal instead of demanding a guess.

---

<!-- Slide 11 -->

## The loop

```
write spec
   → agent proposes a plan against it
   → human approves/edits plan
   → agent implements
   → verify against acceptance criteria
   → update spec to match what was actually built
     (or fix the build to match spec)
```

Four of these steps are easy. Teams skip the last one.

---

<!-- Slide 12 -->

## Why the last step is the whole point

- A spec that silently drifts from the code is **worse than no spec** —
  it actively misleads the next reader
- "Update the spec" belongs in your definition of done, same as tests
- The value of DDD comes from the plan being checked against the spec
  *before* implementation — not from the doc existing in the repo

DDD ≠ "I wrote a doc once." DDD = the doc stays true.

---

<!-- Slide 13 -->

## Repo-level agent docs vs. feature specs

Two different documents — don't confuse them:

| | Repo-level docs (`CLAUDE.md`, `AGENTS.md`) | Feature spec |
|---|---|---|
| Scope | Whole repo, standing context | One piece of work |
| Contents | Conventions, test commands, architecture constraints | Goal, non-goals, interfaces, edge cases, acceptance criteria |
| Lifecycle | Read every session, rarely changes | Written for this task, archived/deleted after ship |

DDD in this course = the second kind.

---

<!-- Slide 14 -->

## Good repo docs make specs shorter

Example `CLAUDE.md` rule (from the course's worked example):

```markdown
Before any UI/styling work, read `design/tokens.css` and
`design/system.md`. Do not introduce new colors, fonts, or spacing
values outside the tokens file.
```

Because this rule already exists at the repo level, the CSV-export
spec never has to mention design tokens at all — one less thing to
write, one less thing that can go stale inside the feature spec.

---

<!-- Slide 15 -->

## Common pitfalls (1 of 2)

**Stale docs**
Spec says one thing, code does another, nobody notices until it causes
a bug.
→ Mitigation: "update the spec" is part of done.

**Over-specifying**
Dictating implementation details that don't matter — expensive to
write, expensive to keep in sync.
→ Mitigation: specify contracts and behavior, not internals, unless
the internals *are* the point.

---

<!-- Slide 16 -->

## Common pitfalls (2 of 2)

**Under-specifying known edge cases**
If you know about them and don't write them down, you haven't saved
time — you've moved the cost to debugging.

**Treating the spec as a one-way handoff**
The value of DDD comes from the agent's plan being checked against the
spec *before* implementation starts — not from filing the spec and
walking away.

---

<!-- Slide 17 -->

## When DDD is the wrong tool

| Methodology | Best for | Weak for | Artifact left behind |
|---|---|---|---|
| **DDD (spec-first)** | Features with real ambiguity, multi-person context | Tiny fixes (overhead) | Durable spec doc |
| Plan-first | Refactors, risky multi-file changes | Fast exploration | Ephemeral plan/ADR |
| TDD-with-agent | Bug fixes, well-defined logic | Vague/exploratory UI | Test suite |
| Conversational | Prototypes, one-offs | Anything needing a paper trail | None |

A five-line bug fix does not need a spec. A feature with real
ambiguity does.

---

<!-- Slide 18 -->

## Lab: write a spec, hand it to an agent

1. Pick a real, small-to-medium feature (sample repo or your own)
2. Write a **one-page spec** using the anatomy above — time yourself
3. Give the agent **only the spec** as the task — no verbal context
4. Have the agent **propose a plan first**; review it against the spec
   before allowing implementation
5. After implementation, check behavior against acceptance criteria
6. Update the spec to close every gap you find

---

<!-- Slide 19 -->

## Lab: what to watch for

- Every place the agent had to **guess** → the spec was silent
- Every place the plan **surprised you** → catch it before code exists,
  that's the whole point of step 4
- Every acceptance criterion that **fails on first try** → is it the
  code that's wrong, or was the criterion itself unclear?
- Be honest about time spent — this is how you'll later judge whether
  DDD paid for itself on this task size

---

<!-- Slide 20 -->

## Deliverable

- The spec document
- The agent's plan (if plan mode was used)
- The resulting diff
- A short list: **"places the spec was wrong or incomplete, and what I
  changed"**

That last list is the artifact that matters most — it's the direct
evidence of what a spec is worth on real work.

---

<!-- Slide 21 -->

## Recap + next up

Today:
- A spec is a **contract**, not a wish list
- The loop only counts as DDD if the **spec gets updated**
- Repo-level docs and feature specs are different tools, used together

**Next — Module 7: Deterministic Design Systems.** Same idea of
"write it down so the agent doesn't guess," applied to visual
consistency: tokens and design docs instead of vague adjectives.
