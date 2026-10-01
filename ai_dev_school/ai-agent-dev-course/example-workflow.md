# Worked Example: Building One Feature With the Whole Toolkit

A single, illustrative walkthrough showing Modules 6, 7, 8, 9, and 12
used together on one real-shaped feature, start to finish. This is
written dialogue/output for teaching purposes — not a captured
transcript — but it's representative of what each step actually looks
like in practice. Use it as reference material for the Capstone
(Module 15), or read it before Module 6 to see where all the pieces
land before doing them yourself.

**The feature:** *Add a "Export to CSV" button to the reports dashboard,
with a date-range filter.* Small enough to walk through fully in one
doc, real enough to touch a UI element, a data boundary, and an edge
case worth testing.

---

## Step 1 — Write the spec (Module 6, DDD)

```markdown
# Spec: CSV Export for Reports Dashboard

## Goal
Let a user export the currently filtered report rows to a CSV file,
matching the date range they've already selected on the dashboard.

## Non-goals
- No new file formats (CSV only, not XLSX/PDF)
- No server-side scheduled/emailed exports — this is a synchronous,
  on-click download only

## Interface
- A button labeled "Export CSV" next to the existing date-range picker
- Clicking it downloads a file named `report_<start>_<end>.csv`
- Columns match the currently visible table columns, in the same order

## Edge cases
- No rows in the selected range → download a CSV with headers only, not
  an error
- Date range spans a DST transition → use UTC dates in the filename and
  in any date-valued columns, to avoid off-by-one-day bugs
- User has an active column filter (not just date range) → export
  respects it too, not just the date range

## Acceptance criteria
- Exporting a known 3-row range produces a CSV with exactly those 3 rows
  plus a header row
- Exporting an empty range produces a header-only CSV, not a 500 or a
  blank file
- Filename matches `report_<start>_<end>.csv` using UTC dates

## Open questions
- Should the export button be disabled (vs. hidden) when there's no data
  to export? Leaving this to the agent to propose in the plan step.
```

**Why this spec is sized right:** it names the DST edge case and the
"respects other filters too" case explicitly — those are exactly the
kind of things that get missed if this feature were requested
conversationally instead. It leaves the disabled-vs-hidden button
question open on purpose, because it's a minor UI call, not core
behavior.

---

## Step 2 — Check the design system (Module 7)

Before anything gets built, the repo's `CLAUDE.md` rule from Module 7
kicks in automatically:

> Before any UI/styling work, read `design/tokens.css` and
> `design/system.md`. Do not introduce new colors, fonts, or spacing
> values outside the tokens file.

So the new button uses the existing `--color-accent` / `--space-unit`
tokens rather than the agent picking its own shade of blue. Nothing to
do here except confirm it happened — check the diff for any new raw hex
values. (If this were a bigger UI addition, this step would get its own
tokens-file check in the lab, same as Module 7's exercise.)

---

## Step 3 — Plan before building (Module 8)

The spec goes in as the task; plan mode is used because this touches
both frontend (button, download trigger) and backend (query filtering,
CSV serialization):

**Agent's proposed plan (abbreviated):**
```
1. Add `GET /api/reports/export` endpoint — accepts the same query
   params as the existing `/api/reports` list endpoint
2. Reuse existing filter-building logic from ReportsQuery rather than
   duplicating it (avoids the two filters drifting apart over time)
3. Serialize rows to CSV using the existing column config so the export
   stays in sync with the table if columns change later
4. Frontend: add the button, wire it to trigger a download from the new
   endpoint
5. Open question from spec: propose disabling (not hiding) the button
   when the filtered result set is empty, so it's discoverable but
   inert — flagging for approval before implementing
```

**Human review:** point 2 (reusing filter logic) is exactly the kind of
thing worth catching *before* implementation — it prevents a second,
subtly different copy of the filtering logic from existing. Approved as
proposed, including the disabled-button call.

---

## Step 4 — TDD the core logic (Module 9)

The risky part isn't the button — it's the CSV serialization and the
date-range edge cases from the spec. Test-first, starting with the
DST/UTC case since it's the easiest one to get subtly wrong:

```python
def test_export_filename_uses_utc_dates_across_dst_transition():
    # range crosses a US DST transition (Mar 10, 2024)
    rows = query_reports(start="2024-03-09", end="2024-03-11", tz="America/New_York")
    filename = build_export_filename(start="2024-03-09", end="2024-03-11")
    assert filename == "report_2024-03-09_2024-03-11.csv"
```
Run — fails (filename builder was using local server time, producing an
off-by-one date). Fix applied. Re-run — passes.

Second test, the empty-range case from the spec's acceptance criteria:
```python
def test_export_empty_range_returns_header_only_csv():
    csv_output = export_reports_csv(start="2024-01-01", end="2024-01-01", filters={})
    lines = csv_output.strip().split("\n")
    assert len(lines) == 1  # header only, no rows, no error
```
Written first, fails against a naive first implementation that returned
a 204 with no body instead of a header-only CSV — exactly the kind of
mismatch a written acceptance criterion catches before it ships.

---

## Step 5 — Second-agent review (Module 12 / Module 11's pattern)

A fresh session, given only the diff and the original spec — no access
to the first session's reasoning:

> Reviewer's findings:
> - Matches spec on filename format and empty-range behavior ✓.
> - The "respects other filters too, not just date range" edge case
>   from the spec isn't covered by any test — the endpoint accepts a
>   `filters` param but there's no test exercising a non-date filter
>   combined with a date range. Recommend adding one before merge.
> - Minor: the new endpoint doesn't share rate-limiting middleware with
>   the rest of `/api/reports/*` — worth confirming that's intentional.

Both are real, useful catches — the first is a direct spec-vs-tests gap
(exactly the kind of thing Module 12's lab is built to practice finding),
the second is a scope question the implementer wouldn't have thought to
flag about its own work.

---

## Step 6 — Close the loop: update the spec

Per Module 6's discipline, the spec gets one addition once the missing
test was added and the rate-limiting question was resolved (it was
intentional — exports are less frequent than list views, existing limits
were too aggressive):

```markdown
## Acceptance criteria (addendum)
- Exporting with both a date range and a non-date column filter applied
  reflects both, not just the date range (added after review caught this
  was untested)

## Notes
- Export endpoint intentionally uses a separate, higher rate limit than
  /api/reports/* — exports are infrequent, user-triggered actions
```

The spec now matches what actually shipped — the next person (human or
agent) who reads it gets the real picture, not the day-one version.

---

## What this example is meant to show

Each module's technique caught something different:
- **DDD (3)** caught the DST and multi-filter edge cases *before* any
  code existed
- **Design tokens (4)** kept the button from introducing an off-palette
  color, with zero extra effort once the repo rule existed
- **Plan-first (5)** caught a code-duplication risk before it was written
- **TDD (6)** caught an actual bug (wrong timezone) and a wrong-shape
  response (204 vs. header-only CSV) that "looks right" review might
  have missed
- **Review (9)** caught a spec-to-test gap neither the spec author nor
  the implementer noticed on their own

No single technique here would have caught everything. That's the
argument for combining them deliberately (Module 15) rather than
defaulting to whichever one is most comfortable.
