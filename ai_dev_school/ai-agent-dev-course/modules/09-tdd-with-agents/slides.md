---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 9
## Test-Driven Development with Agents
### Case study: Tests as the spec

---

<!-- Slide 2 -->

# Agenda

- Why tests are a better spec than prose, for an agent
- Red/green/refactor, with the agent driving
- Worked example: bug report → failing test → fix
- Example-based vs. property-based tests
- Why failing tests reduce hallucination
- Lab: bug report only, no hints
- Deliverable & wrap-up

---

<!-- Slide 3 -->

# Learning Objectives

- Use tests as an executable, unambiguous spec for an agent
- Understand why a failing test written *before* the fix reduces
  agent hallucination
- Know when TDD-with-agents is the right tool — and when it isn't

---

<!-- Slide 4 -->

# Why TDD Matters Even More With Agents

- For a human, TDD is mostly a **discipline** problem
- For an agent, it's a **targeting** problem — give the model an
  unambiguous definition of "done"
- A prose spec can be satisfied on the letter while missing the intent
- A failing test has exactly one legitimate way to turn green

---

<!-- Slide 5 -->

# Quick Refresher: Red / Green / Refactor

- **Red** — write a test for behavior that doesn't exist yet; watch it fail
- **Green** — write the minimum code needed to pass it
- **Refactor** — clean up the implementation, tests stay green
- Repeat, one small increment at a time

---

<!-- Slide 6 -->

# The Loop, With an Agent Driving

1. Agent writes a failing test
2. **You (or CI) confirm it fails — and fails for the right reason**
3. Agent implements the fix
4. Agent (or you) confirms the suite is green
5. Agent refactors
6. Repeat

Step 2 is the one humans skip — and agents skip harder.

---

<!-- Slide 7 -->

# Meet the Bug: A Bulk-Discount Off-by-One

> "Customers say buying exactly 10 units doesn't get the bulk
> discount applied. 11 units works fine."

That's the **entire** bug report handed to the agent — no file names,
no stack trace, no suspected cause.

---

<!-- Slide 8 -->

# Step 1 — Write the Failing Test

```python
def test_bulk_discount_applies_at_exactly_10_items():
    total = calculate_discount(quantity=10, unit_price=5.00)
    assert total == 45.00  # 10 * 5.00 * 0.9
```

- Turns the bug report into one concrete, checkable claim
- Run it now — *before* touching any implementation code

---

<!-- Slide 9 -->

# Step 2 — Confirm It Fails for the *Right* Reason

```
AssertionError: 50.0 != 45.00
```

- **Good failure:** the discount math is wrong, exactly as reported
- **Bad failure (red flag):** `NameError`, `ImportError`, a broken
  fixture — the *test* is wrong, not the code
- Skipping this check is how agents "fix" typos and call it done

---

<!-- Slide 10 -->

# Step 3 — Implement the Fix, Confirm Green

```diff
- if quantity > 10:
+ if quantity >= 10:
      total *= 0.9
```

- Re-run the new test → passes
- Re-run the **whole suite** → nothing else broke
- Only then does the agent touch anything else

---

<!-- Slide 11 -->

# Step 4 — Refactor (the Step Agents Skip)

```python
BULK_DISCOUNT_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.9

if quantity >= BULK_DISCOUNT_THRESHOLD:
    total *= BULK_DISCOUNT_RATE
```

- Green tests feel like "done" to an agent — refactor has no test
  demanding it, so you have to ask
- Green tests are a safety net *for* cleanup, not a reason to skip it

---

<!-- Slide 12 -->

# Example-Based Tests as a Spec

```python
def test_bulk_discount_applies_at_exactly_10_items(): ...
def test_no_discount_at_9_items(): ...
def test_discount_on_a_large_order(): ...
```

- Precise, readable, cheap for an agent to write
- Only as good as the examples someone thought to write
- An agent will happily write examples that confirm its *own*
  assumption about where the boundary is

---

<!-- Slide 13 -->

# Property-Based Tests as a Spec

- Instead of specific inputs, state an **invariant** that must hold
  for *all* inputs
- A generator produces hundreds of cases — including ones nobody
  thought to write by hand
- Invariant for this function: *the discounted total never exceeds
  the full price*

---

<!-- Slide 14 -->

# Worked Example: A Property-Based Test

```python
from hypothesis import given, strategies as st

@given(
    quantity=st.integers(min_value=0, max_value=10_000),
    unit_price=st.floats(min_value=0.01, max_value=10_000),
)
def test_discount_never_exceeds_full_price(quantity, unit_price):
    assert calculate_discount(quantity, unit_price) <= quantity * unit_price
```

Catches cases the example tests never touched: `quantity=0`, huge
orders, float rounding pushing the total *above* full price.

---

<!-- Slide 15 -->

# Choosing, With an Agent Driving

| | Example-based | Property-based |
|---|---|---|
| Best for | the bug report's exact scenario | boundary/invariant coverage |
| Agent writes it | fast, straight from the report | needs an invariant stated by **you** |
| Main risk | narrow — tests only what's imagined | vague if the invariant is weak |

Use example-based to reproduce the bug; add property-based to check
the fix is *actually* general, not just report-shaped.

---

<!-- Slide 16 -->

# Why Failing Tests Reduce Agent Hallucination

- A prose bug report is ambiguous — the agent fills gaps with a
  guess dressed up as confidence
- A failing test is a checkable contract: the fix is either green or
  it isn't — no persuasive explanation substitutes for that
- It forces the agent to **run** something instead of **asserting**
  that something worked

---

<!-- Slide 17 -->

# Failure Mode: The Test That Passes for the Wrong Reason

```python
def test_bulk_discount():
    assert True  # "verified manually"
```

- An extreme example, but the pattern is real: over-mocking,
  asserting on a constant, testing the mock instead of the code
- The fix: read the failing test's *error message* before you ever
  trust the green one

---

<!-- Slide 18 -->

# Where This Pairs Well — and Poorly

- **Well:** bug fixes, well-defined logic, pure functions, parsers,
  calculations — "correct" is already known
- **Poorly:** exploratory UI, "make it feel right" work — you'd be
  writing assertions about an answer you don't have yet
- TDD-with-agents assumes the test is right *before* you write it —
  that's a real assumption, not a given

---

<!-- Slide 19 -->

# Lab: Bug Report Only

You will hand the agent **only** a bug report — no file names, no
hints, no suspected cause.

Required sequence:
1. Write a test that reproduces the bug and fails
2. Confirm the failure is for the right reason
3. Implement the fix
4. Confirm the test passes and nothing else broke

---

<!-- Slide 20 -->

# Lab Walkthrough — What "Done" Looks Like

- Two separate commits: failing test, then fix — never squashed
- The failing-test commit's diff should contain **no** production
  code changes
- Before merging: re-read the assertion — does it actually encode
  the bug report, or something merely adjacent to it?

---

<!-- Slide 21 -->

# Deliverable

- Two commits: failing test → fix, kept separate in history
- A one-line note: did the agent's *first* attempt at the test
  actually capture the bug, or did it need correction?
- That note is the real signal — it tells you how much to trust the
  agent's next test, unsupervised

---

<!-- Slide 22 -->

# Recap & Next Module

- Tests as an executable spec close off the agent's room to guess
- Red/green/refactor — "confirm it fails right" is the step that
  actually matters
- Example-based to reproduce, property-based to generalize
- Next: **Module 10 — Conversational / Iterative Development** — what
  happens with no upfront doc and no test at all
