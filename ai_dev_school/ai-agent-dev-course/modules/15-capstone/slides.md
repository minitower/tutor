---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 15
## Capstone
### Case study focus: Combine methodologies on a real feature

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->
## Agenda

- Recap: the whole methodology toolkit, side by side
- One worked example — CSV export — all five techniques applied in sequence
- Synthesis: what each technique caught (and what none alone would have)
- The capstone assignment: your own feature, same discipline
- Deliverable, retro, and rubric
- Lab: build it

---

<!-- Slide 3 -->
## Learning objectives

By the end of this module you can:

1. Choose *which combination* of methodologies a real feature needs —
   not just reach for one habit
2. Walk the DDD → plan → TDD → review → spec-update loop end to end
3. Identify what each technique catches that the others miss
4. Produce a full deliverable set: spec, plan, tests, review notes, retro

---

<!-- Slide 4 -->
## Recap: the whole toolkit, side by side

| Methodology | Best for | Weak for | Artifact left behind |
|---|---|---|---|
| DDD (spec-first) | Ambiguous, multi-person features | Tiny fixes (overhead) | Durable spec doc |
| Plan-first | Refactors, risky multi-file changes | Fast exploration | Ephemeral plan (or ADR) |
| TDD-with-agent | Bug fixes, well-defined logic | Vague/exploratory UI work | Test suite |
| Conversational | Prototypes, one-off scripts | Anything needing a paper trail | None (chat history only) |
| Multi-agent review | High-stakes, security-sensitive code | Low-stakes/small changes | Review transcript |

This module is not a new technique — it's using several of these, on purpose, on one feature.

---

<!-- Slide 5 -->
## Today's feature: CSV export with a date-range filter

- Add an "Export CSV" button to the reports dashboard
- Export respects the date range already selected on screen
- Small enough to walk start-to-finish in one session
- Real enough to touch a UI element, a data boundary, *and* an edge case worth testing
- Threads Modules 6, 7, 8, 9, and 12 together — one continuous example

---

<!-- Slide 6 -->
## Step 1 — Spec it (Module 6, DDD)

```markdown
## Goal
Let a user export the currently filtered report rows to a CSV file,
matching the date range they've already selected on the dashboard.

## Non-goals
- No new file formats (CSV only, not XLSX/PDF)
- No server-side scheduled/emailed exports — synchronous, on-click only

## Interface
- A button labeled "Export CSV" next to the date-range picker
- Downloads `report_<start>_<end>.csv`
- Columns match the visible table columns, same order
```

---

<!-- Slide 7 -->
## Step 1 — Edge cases & acceptance criteria

```markdown
## Edge cases
- No rows in range → header-only CSV, not an error
- Range spans a DST transition → use UTC dates everywhere, to avoid
  off-by-one-day bugs
- An active column filter is applied too → export respects it, not
  just the date range

## Acceptance criteria
- A known 3-row range → CSV with exactly those 3 rows + header
- An empty range → header-only CSV, not a 500 or a blank file
- Filename uses UTC dates
```

Left open on purpose: disable vs. hide the button when there's nothing to export — a minor UI call, not core behavior.

---

<!-- Slide 8 -->
## Why this spec is sized right

- Names the **DST edge case** explicitly — exactly the kind of thing
  that gets missed when a feature is requested conversationally
- Names "**respects other filters too**" explicitly — not just the
  obvious date-range case
- Leaves one genuinely minor question open instead of over-specifying
- A stranger could implement this without a single follow-up question
  on the *behavior* — only on the one flagged open question

---

<!-- Slide 9 -->
## Step 2 — Check the design system (Module 7)

The repo's `CLAUDE.md` rule fires automatically, before any UI code is written:

> Before any UI/styling work, read `design/tokens.css` and
> `design/system.md`. Do not introduce new colors, fonts, or spacing
> values outside the tokens file.

- New button uses existing `--color-accent` / `--space-unit` tokens
- Nothing to *do* here — just confirm it happened (check the diff for
  raw hex values)
- Zero extra effort, because the repo rule already existed

---

<!-- Slide 10 -->
## Step 3 — Plan before building (Module 8)

Spec goes in as the task; plan mode used because this spans frontend and backend:

```
1. Add GET /api/reports/export — same query params as /api/reports
2. Reuse existing filter-building logic from ReportsQuery (don't
   duplicate it)
3. Serialize rows to CSV using the existing column config
4. Frontend: add the button, wire it to trigger the download
5. Open question from spec: propose DISABLING (not hiding) the button
   when the result set is empty — flagging for approval
```

---

<!-- Slide 11 -->
## Step 3 — The approval gate catches something

- Point 2 — **reuse the filter logic** — is exactly the kind of thing
  worth catching *before* code exists
- Left alone, this becomes a second, subtly different copy of the
  filtering logic that drifts apart over time
- Human review: approved as proposed, including the disabled-button call
- Cost of catching it here: one read of a 5-line plan.
  Cost of catching it in review after the fact: a second diff.

---

<!-- Slide 12 -->
## Step 4 — TDD the core logic (Module 9): the DST bug

The risky part isn't the button — it's the date math. Test first:

```python
def test_export_filename_uses_utc_dates_across_dst_transition():
    # range crosses a US DST transition (Mar 10, 2024)
    filename = build_export_filename(start="2024-03-09", end="2024-03-11")
    assert filename == "report_2024-03-09_2024-03-11.csv"
```

**Run → fails.** Filename builder was using local server time,
producing an off-by-one date. Fix applied. Re-run → **passes.**

---

<!-- Slide 13 -->
## Step 4 — TDD the core logic: the empty-range shape

```python
def test_export_empty_range_returns_header_only_csv():
    csv_output = export_reports_csv(start="2024-01-01", end="2024-01-01", filters={})
    lines = csv_output.strip().split("\n")
    assert len(lines) == 1  # header only, no rows, no error
```

Written first, fails against the naive first implementation — which
returned a **204 with no body** instead of a header-only CSV. Exactly
the mismatch a written acceptance criterion catches before it ships.

---

<!-- Slide 14 -->
## Step 5 — Second-agent review (Module 11's pattern)

Fresh session. Given only the diff and the original spec — **no
access** to the first session's reasoning:

> - Matches spec on filename format and empty-range behavior ✓
> - The "respects other filters too" edge case isn't covered by any
>   test — the endpoint accepts a `filters` param but nothing exercises
>   it combined with a date range. Recommend adding one before merge.
> - Minor: the new endpoint doesn't share rate-limiting middleware with
>   the rest of `/api/reports/*` — confirm that's intentional.

---

<!-- Slide 15 -->
## Step 5 — Why both findings matter

- Finding 1 is a **direct spec-vs-tests gap** — the exact shape of
  thing Module 12's review habit is built to catch
- Finding 2 is a **scope question about its own work** the implementer
  had no reason to flag — it wasn't wrong, just unexamined
- Neither finding required the reviewer to re-derive the feature —
  just to check the diff against the spec, line by line

---

<!-- Slide 16 -->
## Step 6 — Close the loop: update the spec

Per Module 6's discipline — once the missing test is added and the
rate-limit question is resolved (intentional: exports are infrequent):

```markdown
## Acceptance criteria (addendum)
- Exporting with both a date range and a non-date column filter
  reflects both (added after review caught this was untested)

## Notes
- Export endpoint intentionally uses a separate, higher rate limit —
  exports are infrequent, user-triggered actions
```

The spec now matches what actually shipped — the next reader gets the real picture, not the day-one version.

---

<!-- Slide 17 -->
## Synthesis — what each technique caught

- **DDD (3)** — caught the DST and multi-filter edge cases *before any code existed*
- **Design tokens (4)** — kept the button on-palette, zero extra effort
- **Plan-first (5)** — caught a code-duplication risk before it was written
- **TDD (6)** — caught an actual bug (wrong timezone) and a wrong-shape response (204 vs. header-only CSV)
- **Review (9)** — caught a spec-to-test gap neither the spec author nor the implementer noticed
- No single technique here would have caught *everything* — each has a
  **blind spot exactly where another one is strong**

**That's Module 15 in one sentence: stop defaulting, start combining — deliberately.**

---

<!-- Slide 18 -->
## The capstone assignment

Pick a feature substantial enough to be worth a spec. Then apply the
same discipline you just watched, on your own feature:

1. **Spec it** (Module 6, DDD) — goal, non-goals, interfaces, edge cases, acceptance criteria
2. **Plan it** (Module 8) — agent proposes a plan against the spec; you review and approve first
3. **TDD the core logic** (Module 9) — at least the parts with real business logic
4. **Review it with a second agent** (Module 11) — fresh session, spec + security focus
5. **Update the spec** to match what actually got built

---

<!-- Slide 19 -->
## Picking your feature

- Substantial enough to be worth a spec — not a one-line fix
- Nothing comes to mind? Use a small end-to-end slice: a new
  authenticated API endpoint with persistence and a test suite
- Needs real business logic *somewhere* — not just CRUD scaffolding
- Bonus points if it has a genuine edge case like the DST bug —
  something a conversational request would likely have missed

---

<!-- Slide 20 -->
## Deliverable

- The repo (or diff) for the feature
- **Spec doc, plan, tests, and review notes** — as separate artifacts,
  not squashed into one commit message
- A **retro** (half to one page) — next slide

---

<!-- Slide 21 -->
## The retro question

> What would this have looked like if you'd built it solo, without an
> agent, six months ago?

- Where did the methodology choice **save time**?
- Where did it add **ceremony that didn't pay for itself**?
- Retro honesty means naming real tradeoffs — "AI is great" is not a retro

---

<!-- Slide 22 -->
## Self-assessment rubric (cohort format)

- **Spec quality** — could a stranger implement from it?
- **Plan/spec fidelity** — did implementation match the approved plan;
  were divergences documented?
- **Test quality** — do tests pin real behavior, or just the happy path?
- **Review rigor** — did the reviewer catch something real, or rubber-stamp?
- **Retro honesty** — real tradeoffs named, not just praise

---

<!-- Slide 23 -->
## Today's lab

1. Pick your feature (5 min sanity-check with a neighbor or instructor)
2. Write the spec — goal, non-goals, interfaces, edges, acceptance criteria
3. Get a plan, review it, approve it
4. TDD the riskiest piece of logic — not the boilerplate
5. Fresh-session review against spec + security
6. Close the loop: update the spec, write the retro

Work at your own pace — this is the one lab built to fill the rest of the session.

---

<!-- Slide 24 -->
## Course recap: the throughline

- **1–2**: how the agent loop works, and how to ask it for things precisely
- **3–4**: durable contracts — specs and design tokens — for ambiguity and UI drift
- **5–6**: ephemeral contracts — plans and tests — for risky approaches and core logic
- **7**: when to skip all of it and just talk to the agent
- **8–9**: composing agents, and trusting but verifying what they produce
- **10–11**: putting this into a pipeline and a team, safely
- **12**: combining all of it, deliberately, on one feature — starting now

---

<!-- Slide 25 -->
## Closing

- You now have a full toolkit, not just a favorite technique
- The skill this course actually teaches: **noticing which kind of risk
  a feature carries**, and picking the methodology that covers it
- Ship the capstone. Write the retro honestly. That's the real diploma.

**Thank you — go build something real.**
