---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 2
## Prompting & Task Specification
### Precision in, precision out

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->
## Agenda

- The gap: what you meant vs. what you typed
- Context vs. instructions
- Acceptance criteria
- Constraints
- Anti-patterns
- Worked example: vague → constrained → fully specified
- Lab + deliverable

---

<!-- Slide 3 -->
## Objectives

- Write task descriptions that reduce the agent's need to guess
- Recognize the gap between "what I meant" and "what I typed" —
  and close it **before** the agent starts, not after

---

<!-- Slide 4 -->
## Why this comes right after Module 1

- Module 1: the agent loop — plan → act with tools → observe → repeat
- The loop is only as good as what kicks it off
- A bad prompt doesn't make the agent stop and ask (usually) —
  it makes the agent **guess, confidently, and proceed**
- Today: controlling the input side of the loop

---

<!-- Slide 5 -->
## The core problem

> "What I meant" vs. "what I typed"

- The agent doesn't share your mental model, your team's conventions,
  or your unstated assumptions
- It fills every gap you leave with the most *plausible* guess —
  not necessarily *your* guess
- **Precision in, precision out.** Ambiguity in, expensive rework out.

---

<!-- Slide 6 -->
## Context vs. instructions

- **Context** — what the agent needs to *know*
  (facts, conventions, existing patterns, non-negotiables)
- **Instructions** — what you need it to *do*
  (the actual task, stated once, unambiguously)
- Conflating them buries the ask in trivia, or gives instructions
  with no grounding to check them against

---

<!-- Slide 7 -->
## Context vs. instructions — before / after

**Before (mixed):**
> "Our API uses Express and Postgres, and we use cursor-based
> pagination elsewhere in the codebase, can you add pagination to
> the users list endpoint, also make it fast"

**After (separated):**
```
Context: Express + Postgres. Existing endpoints use cursor-based
pagination (see src/routes/orders.js for the pattern).

Task: Add cursor-based pagination to GET /api/users, following
the same pattern as orders.js.
```

---

<!-- Slide 8 -->
## Acceptance criteria

- A task without a testable definition of "done" is a task the
  agent will finish **incorrectly, with full confidence**
- The agent *will* stop somewhere — the only question is whether
  it stops where you needed it to
- "Testable" = something you (or a test suite) can check, pass/fail

---

<!-- Slide 9 -->
## Acceptance criteria — before / after

**Before:**
> "Add pagination to the products endpoint so it's not too slow"

**After:**
```
Acceptance criteria:
- GET /api/products accepts `limit` (default 20, max 100) and
  `cursor` (opaque string from a prior response)
- Response includes `next_cursor` (string, or null on the last page)
- limit > 100 → 400 with an error body
- No query params → first page, same item shape as today
```

---

<!-- Slide 10 -->
## Constraints matter as much as goals

- Goals say *where to go*. Constraints say *what not to break*
  on the way there.
- No constraints stated = the agent is free to satisfy the goal
  in the cheapest way it can find — including ways you didn't want
- "Don't touch the public API," "keep it in one file,"
  "no new dependencies" — say the boundary, not just the destination

---

<!-- Slide 11 -->
## Constraints — before / after

**Before:**
> "Refactor the auth module to be cleaner"

**After:**
```
Refactor auth/session.js for readability.
Constraints:
- Do not change exported function signatures in auth/index.js
  (three other services import them)
- No new dependencies
- Keep the diff under ~150 lines
- All existing tests must pass unmodified
```

---

<!-- Slide 12 -->
## Anti-pattern #1 — the vague ask

> "Make this better."
> "Clean up the error handling."
> "Optimize this."

- "Better" has no shared definition between you and the agent
- The agent will pick *a* definition and commit to it fully

---

<!-- Slide 13 -->
## Anti-pattern #2 — missing "done"

> "Add rate limiting to the API."

- Which endpoints? Per-user or per-IP? What limit?
  What happens when it's exceeded — 429? Retry-After header?
- Every unanswered question becomes an agent decision you didn't make

---

<!-- Slide 14 -->
## Anti-pattern #3 — burying the requirement

> "We've had this pagination discussion before, the old approach
> used offsets, our DB team doesn't love that, there was a ticket
> about it last quarter... anyway, this needs to ship before the
> 3pm demo so **please only touch the frontend, not the API.**"

- The one hard constraint is the last clause of the last sentence
- Lead with constraints and acceptance criteria — don't bury them

---

<!-- Slide 15 -->
## Anatomy of a well-specified task

1. **Context** — facts and patterns the agent needs
2. **Task** — one unambiguous sentence: what to build
3. **Constraints** — what must not change or break
4. **Acceptance criteria** — testable definition of "done"
5. **Edge cases** — what happens at the boundaries

Not every task needs all five in full — but skipping one is a choice,
not an accident.

---

<!-- Slide 16 -->
## Worked example: three passes, one feature

**Feature:** add pagination to `GET /api/products`

- V1 — Vague
- V2 — Constrained
- V3 — Fully specified

Same feature, same starting repo, clean session each time.
Watch what changes in the output as precision goes up.

---

<!-- Slide 17 -->
## V1 — Vague

```
Add pagination to the products list endpoint.
```

**Typical agent behavior:** picks *a* pagination style (often
offset/limit, since it's the most common pattern in training data)
with an unbounded or arbitrarily-chosen limit, and no guarantee it
matches conventions already used elsewhere in your codebase.

---

<!-- Slide 18 -->
## V2 — Constrained

```
Add pagination to GET /api/products.
- limit: default 20, max 100
- cursor: opaque, from response's next_cursor
- response adds next_cursor (string | null)
```

**Typical agent behavior:** gets the shape right — but edge cases
like an invalid or expired cursor, or a request past the last page,
are still up to its judgment. Might 500. Might silently return empty.

---

<!-- Slide 19 -->
## V3 — Fully specified

```
...(V2, plus:)
Edge cases:
- invalid cursor format → 400
- cursor past last page → empty items, next_cursor: null
- no params → first page, existing response shape preserved
Acceptance: existing integration tests for GET /api/products
must still pass unmodified.
```

**Typical agent behavior:** handles the edge cases — because they
were named. Precision bought correctness exactly where you spent it.

---

<!-- Slide 20 -->
## Lab

- Pick one small feature (your own, or the pagination example)
- Write three versions of the request: vague → constrained →
  fully specified
- Run each from a **clean agent session** (no shared history)
- Diff the three resulting outputs

---

<!-- Slide 21 -->
## Deliverable

- The 3 prompts
- The 3 resulting diffs
- A short comparison:
  - What did extra precision buy you?
  - Where did it stop mattering?

---

<!-- Slide 22 -->
## Recap & next module

- Precision in, precision out — the agent fills every gap you leave
- Context vs. instructions, acceptance criteria, constraints:
  three habits, one goal — less guessing, less rework
- **Next — Module 3: Document-Driven Development.**
  Turning today's prompt discipline into a durable spec doc the
  whole team (and the agent) can keep working against.
