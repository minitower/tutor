# Module 6 — Test-Driven Development with Agents

## Learning objectives
- Use tests as an executable, unambiguous spec for an agent
- Understand why a failing test written *before* the fix reduces agent
  hallucination (the agent has a concrete, checkable target instead of a
  prose description it might misread)

## Key concepts
- Red/green/refactor with the agent driving: write failing test → confirm
  it fails for the right reason → implement → confirm it passes → refactor
- Example-based tests vs. property-based tests as specs for an agent —
  property-based tests catch edge cases the agent (and you) didn't think
  to write examples for
- Why this pairs well with bug fixes and well-defined logic, and pairs
  poorly with vague or exploratory UI work where "correct" isn't yet
  known

## Lab
Give the agent a bug report only — no hints about the fix. Require it to:
1. Write a test that reproduces the bug and fails
2. Confirm the failure is for the right reason (not a typo in the test)
3. Implement the fix
4. Confirm the test passes and nothing else broke

Keep the failing-test commit and the fix commit separate so the loop is
visible in history.

## Deliverable
Two commits (failing test, then fix) plus a one-line note on whether the
agent's first attempt at the test actually captured the bug, or needed
correction.
