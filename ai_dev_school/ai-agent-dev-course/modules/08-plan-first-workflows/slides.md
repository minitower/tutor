---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 8
## Plan-First Workflows
### Case study focus: Ephemeral plans + approval gates

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->
## Agenda

- Where plan-first fits in the methodology map
- Plan mode & approval gates
- A worked plan, end to end
- ADRs as agent input
- Plan-first vs. DDD
- Lab: a plan-gated refactor
- Deliverable & wrap-up

---

<!-- Slide 3 -->
## Learning objectives

- Separate **planning** from **execution** so scope is agreed *before* code changes
- Recognize when risk lives in the **approach**, not the **requirements**
- Use an approval gate as a real checkpoint — not a rubber stamp
- Know when plan-first is overkill

---

<!-- Slide 4 -->
## Quick recap: Module 6 sets up the contrast

| | DDD (Module 6) | Plan-first (this module) |
|---|---|---|
| Artifact | Spec | Plan |
| Lifespan | Durable | Ephemeral |
| Authored by | Human (up front) | Agent (per task) |
| Answers | *What* should this do? | *How* will we get there? |

Same discipline — agree before code — different object of agreement.

---

<!-- Slide 5 -->
## What is a "plan-first" workflow?

1. Agent proposes an explicit plan: files, changes, sequence, rationale
2. Human (or reviewer agent) approves, amends, or rejects
3. Execution starts **only** after approval

No tests, no diff yet — this gate happens *before* any code exists.

---

<!-- Slide 6 -->
## Plan mode / approval gates — the mechanic

- Split the agentic loop into a **propose** turn and an **act** turn
- Claude Code's plan mode: read-only exploration, produces a plan, no edits until you approve
- An approval gate is a checkpoint where a human (or reviewer agent) must explicitly say "go"
- Silence ≠ approval — an unread plan is not a reviewed plan

---

<!-- Slide 7 -->
## Anatomy of a good plan

- **Files it intends to touch, and why** for each one
- **Sequencing** — what depends on what
- **Explicit call-outs** of open questions or risky spots
- **Non-goals** — what it will deliberately *not* touch

A plan missing any of these is a plan you haven't finished reviewing.

---

<!-- Slide 8 -->
## Worked example — the task

> Extract the `formatCurrency` logic, currently duplicated in three
> modules (`invoice.ts`, `checkout.ts`, `reports.ts`), into a shared
> `lib/format.ts`.

Unconstrained risk: agent could touch call sites inconsistently, rename
the export, or quietly change rounding behavior along the way.

---

<!-- Slide 9 -->
## Worked example — the agent's plan

```
1. Create lib/format.ts, move formatCurrency() there unchanged
   (byte-for-byte — no behavior change in this step)
2. Update invoice.ts to import from lib/format.ts, remove local copy
3. Update checkout.ts — same as above
4. Update reports.ts — same as above
   NOTE: reports.ts's copy rounds to 0 decimals for summary rows;
   confirm before removing whether that's a bug or intentional
5. Will NOT touch billing/invoice-legacy.ts (deprecated, separate ticket)
```

---

<!-- Slide 10 -->
## Approval gate in action

**Reviewer comment:** "Point 4 — don't guess. Check with the reports
owner about the 0-decimal rounding before merging behavior."

**Agent amends the plan:** step 4 now proposes preserving the 0-decimal
rounding as a documented parameter, not silently unifying it.

**Re-approved → execution begins.**

---

<!-- Slide 11 -->
## What the approval gate is actually for

- Catching scope creep **before** it's code
- Catching duplicated/conflicting logic getting silently merged
- Confirming risky files are touched only when truly necessary
- **Not** a substitute for reviewing the diff afterward

---

<!-- Slide 12 -->
## Common plan failure modes

- **Too vague:** "update the relevant files" — not a plan, a promise
- **Silent scope creep:** a plan that omits a file it will actually touch
- **Rubber-stamp approval:** clicking "approve" without reading step 4
- **Undocumented drift:** execution departs from the plan and nobody notes why

---

<!-- Slide 13 -->
## ADRs — Architecture Decision Records

A durable doc capturing **one decision**, its context, the alternatives
considered, and the consequences.

```
Title: ADR-0007 — Centralize currency formatting in lib/format.ts
Status: Accepted
Context: 3 divergent copies of formatCurrency, one with a silent
         rounding difference discovered during Module 8's refactor
Decision: One canonical implementation; callers pass a `precision`
          param instead of hand-rolling rounding
Consequences: Reports' 0-decimal behavior is now explicit, not implicit
```

---

<!-- Slide 14 -->
## ADRs as agent input

- Plans are thrown away after the task — without a durable record, the
  **next** plan re-litigates the same tradeoff
- Point the agent at `docs/adr/` (referenced from `CLAUDE.md` / `AGENTS.md`)
  *before* it plans
- Result: ADR-0007 above means a future refactor's plan starts from
  "use lib/format.ts," not from re-discovering the rounding bug

---

<!-- Slide 15 -->
## Plan vs. ADR — ephemeral vs. durable

| | Plan | ADR |
|---|---|---|
| Scope | One task | One decision |
| Lifespan | Thrown away after merge | Kept, referenced later |
| Answers | Files + sequence for *this* change | *Why* this approach, generally |

Analogy: a plan is one flight's flight plan; an ADR is the airline's route policy.

---

<!-- Slide 16 -->
## Plan-first vs. DDD, side by side

| | DDD (spec) | Plan-first |
|---|---|---|
| Durable? | Yes | No (ephemeral) |
| Authored by | Human, up front | Agent, proposes; human approves |
| Reduces risk in | *What* to build | *How* to build it safely |

Both require agreement before code — they differ in **what** is being agreed to.

---

<!-- Slide 17 -->
## When plan-first beats DDD

- Requirements are **clear** — the *approach* is what's risky
- Multi-file refactors, migrations, cross-cutting renames
- What needs review is the plan, not a requirements doc
- (Contrast Module 6: there, the *requirements* were the risky part)

---

<!-- Slide 18 -->
## When plan-first is overkill

- Small, reversible, single-file changes
- Writing and reviewing a plan costs more than doing the thing and
  checking the diff
- Rule of thumb: if you can't name two *plausibly different* approaches,
  skip the plan step

---

<!-- Slide 19 -->
## Lab: a plan-gated multi-file refactor

Pick a real multi-file refactor in your sample repo:
- Extract a shared module, **or**
- Rename a widely-used interface

Require an explicit plan — files + why — before any edit happens.

---

<!-- Slide 20 -->
## Lab steps

1. Describe the refactor; ask for a **plan only**, no edits
2. Review the plan against the anatomy checklist (Slide 7)
3. Amend / request changes; re-approve
4. Let the agent execute
5. Review the diff; note any plan/execution divergence

---

<!-- Slide 21 -->
## Deliverable

- The **approved plan** (including any amendments)
- The **resulting diff**
- A written note on **any divergence** between plan and execution — and why

---

<!-- Slide 22 -->
## Recap & next module

- Plan-first separates *agreeing on approach* from *writing code*
- Approval gates only work if someone actually reads the plan
- ADRs make agent decisions durable across tasks — plans don't have to
- Next: **Module 9 — TDD with Agents** — tests as the spec
