# Module 2 — Prompting & Task Specification for Agents

## Learning objectives
- Write task descriptions that reduce the agent's need to guess
- Recognize the gap between "what I meant" and "what I typed," and close
  it before the agent starts working, not after

## Key concepts
- Context vs. instructions: what the agent needs to know vs. what you
  need it to do — conflating them produces vague tasks
- Acceptance criteria: a task without a testable definition of "done" is
  a task the agent will finish incorrectly with full confidence
- Constraints matter as much as goals: "don't touch the public API,"
  "keep it in one file," "no new dependencies" — say the boundaries, not
  just the destination
- Common anti-patterns: vague asks ("make this better"), missing
  "done" definitions, burying the real requirement in the fifth sentence

## Lab
Pick one small feature. Write three versions of the request:
1. Vague ("add pagination to the list endpoint")
2. Constrained (adds explicit limits: page size bounds, response shape)
3. Fully specified (adds acceptance criteria and edge cases)

Run each through an agent from a clean session. Diff the three outputs.

## Deliverable
The 3 prompts, the 3 resulting diffs, and a short comparison: what did
extra precision buy you, and where did it stop mattering?
