# Module 14 — Governance, Safety & Team Adoption

## Learning objectives
- Decide, as a team rather than an individual, when a given methodology
  (from Modules 6–10) is required vs. optional for a given kind of task
- Understand what to measure to know if agent-driven development is
  actually helping

## Key concepts
- Disclosure norms: does the team need to know a PR was agent-assisted,
  and does the review bar change based on that?
- Review requirements by risk tier: e.g., DDD + reviewer agent required
  for anything touching auth/billing/data migrations; conversational mode
  fine for internal tooling and prototypes
- A decision framework: task type → recommended methodology (build this
  from the comparison matrix in [syllabus.md](../syllabus.md))
- Metrics: cycle time, revert/rollback rate, review comment volume on
  agent-assisted vs. human-only PRs — and the trap of only measuring
  speed while quality regresses
- Common team-level failure modes: methodology chosen by habit rather
  than fit, specs written and never updated, review fatigue from too much
  agent output too fast

## Lab
Using the comparison matrix, build a one-page decision tree: given a task
description, which methodology (or combination) does this team default
to, and what's the required review bar at each risk tier?

## Deliverable
The team policy doc (decision tree + review requirements + disclosure
norm), written so a new team member could follow it without this course.
