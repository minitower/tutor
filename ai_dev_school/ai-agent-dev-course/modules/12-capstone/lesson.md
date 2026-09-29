# Module 12 — Capstone

## Objective
Combine methodologies deliberately on one real feature, rather than
defaulting to whichever one you're most comfortable with.

## Format
Pick a feature substantial enough to be worth a spec (if you can't think
of one, use a small end-to-end slice: e.g., a new authenticated API
endpoint with persistence and a test suite). Then:

1. **Spec it** (Module 3, DDD) — goal, non-goals, interfaces, edge cases,
   acceptance criteria
2. **Plan it** (Module 5) — have the agent propose a plan against the
   spec; review and approve before implementation
3. **TDD the core logic** (Module 6) — at least the parts with real
   business logic, not boilerplate
4. **Review it with a second agent** (Module 8) — fresh session, no
   access to the implementer's reasoning, review against spec + security
5. **Update the spec** to match what was actually built, closing any
   gaps found along the way

## Deliverable
- The repo (or diff) for the feature
- Spec doc, plan, tests, and review notes as separate artifacts
- A retro (half to one page): what would this have looked like if you'd
  built it solo, without an agent, six months ago? Where did the
  methodology choice save time, and where did it add ceremony that
  didn't pay for itself?

## Grading / self-assessment rubric (if run as a cohort)
- Spec quality: is it something a stranger could implement from?
- Plan/spec fidelity: did implementation match the approved plan, and
  were divergences documented?
- Test quality: do the tests actually pin the behavior in the spec, or
  just exercise the happy path?
- Review rigor: did the reviewer pass catch anything real, or was it a
  rubber stamp?
- Retro honesty: does it name real tradeoffs, not just "AI is great"?
