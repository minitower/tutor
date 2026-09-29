# Module 1 — Foundations: How Agentic Coding Actually Works

## Learning objectives
- Explain the agent loop: plan → act via tools → observe result → repeat
  until done
- Distinguish autocomplete-style assistance (single-shot suggestions)
  from agentic tools that read files, run commands, and iterate on their
  own output
- Understand what a context window is, why long sessions get summarized
  ("compaction"), and why that matters for how you work

## Key concepts
- Tool-use loop: the agent doesn't just generate text, it generates tool
  calls (read file, run test, edit file), observes the result, and
  decides the next step
- Why this is qualitatively different from Copilot-style completion —
  the agent can verify its own work (run the test it just wrote) instead
  of you being the only feedback loop
- Context limits and memory: what the agent "remembers" within a session,
  what gets summarized away, and why that means important decisions
  belong in files, not just chat history
- The role of permissions/sandboxing: why agents ask before risky actions

## Lab
Run an agent on a small, unfamiliar toy repo with a single task ("add a
CLI flag that does X"). Log every tool call it makes (file reads, greps,
edits, test runs) and, next to each one, write one sentence on why you
think the agent did it.

## Deliverable
Annotated tool-call trace + a half-page writeup: where did the agent
spend most of its "effort" — reading/understanding, or writing code?
