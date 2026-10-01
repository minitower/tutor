# Module 10 — Conversational / Iterative Development

## Learning objectives
- Run a tight feedback loop for small or exploratory tasks without
  upfront documentation
- Recognize agent drift (quietly wandering from the actual goal) and
  correct it before it compounds

## Key concepts
- Incremental correction: short, specific course-corrections beat
  restating the whole task
- Session/context management: what happens on long conversations, when
  to start a fresh session instead of continuing a drifting one
- Why this mode has no paper trail — the chat history isn't a durable
  artifact — and what that costs when someone else needs to understand
  why the code looks the way it does

## Lab
Rebuild the same small feature from Module 6's lab, but purely
conversationally — no spec doc, just iterative back-and-forth. Track how
many turns it took and where you had to correct the agent's direction.

## Deliverable
A side-by-side comparison against the Module 6 (DDD) result: turns/time
spent, quality of the final code, and whether you'd trust either result
without a review pass.
