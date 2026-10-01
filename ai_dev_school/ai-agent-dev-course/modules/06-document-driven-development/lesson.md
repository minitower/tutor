# Module 6 — Document-Driven Development (DDD)

## Why this module exists

The single biggest source of wasted agent turns is ambiguity: the agent
guesses at intent, builds the wrong thing, and you spend more time
correcting than you would have spent writing the intent down once. DDD
front-loads that cost into a document instead of a conversation — and
gets a durable artifact (a spec) out of the deal, instead of a chat log
nobody will reread.

**Document-Driven Development, as used here:** a written spec is the
primary interface between the human and the agent for a piece of work.
The agent reads it, plans against it, implements against it, and — this
is the part teams skip — the doc gets *updated* when reality diverges
from the plan, so it stays trustworthy for the next person (human or
agent) who reads it.

## Learning objectives

- Write a spec that is complete enough for an agent to implement from
  with minimal clarifying back-and-forth
- Recognize the difference between a spec that's too vague (agent
  guesses) and one that's over-specified (agent has no room to make
  reasonable implementation calls, and the doc is expensive to maintain)
- Run the full loop: spec → agent plan → implementation → spec correction
- Know when DDD is the wrong tool (see comparison table in the syllabus
  appendix)

## Anatomy of a spec an agent can execute against

1. **Goal** — one paragraph, plain language, what problem this solves
2. **Non-goals** — explicitly out of scope (this is what saves you from
   silent scope creep)
3. **Interfaces / contracts** — function signatures, API shapes, data
   models — whatever the agent must not invent on its own
4. **Edge cases** — the ones you already know about; don't make the
   agent discover them by shipping bugs
5. **Acceptance criteria** — testable, ideally literally "these
   commands/tests should pass"
6. **Open questions** — things you're deliberately leaving for the agent
   to propose an answer to (marking these explicitly is what keeps the
   doc from becoming a straitjacket)

## The loop

```
write spec  →  agent proposes a plan against it  →  human approves/edits plan
    →  agent implements  →  verify against acceptance criteria
    →  update spec to match what was actually built (or fix the build to match spec)
```

The last step is the one that makes this "document-driven" rather than
just "written a doc once." A spec that silently drifts from the code is
worse than no spec — it actively misleads the next reader.

## Repo-level agent docs vs. feature specs

Don't confuse two different documents:
- **Repo-level agent instructions** (`CLAUDE.md`, `AGENTS.md`, etc.) —
  standing context every agent session should have: conventions, how to
  run tests, architectural constraints. Read once per session, rarely
  changes.
- **Feature spec** — scoped to one piece of work, written for this task,
  archived or deleted once shipped (or kept as an ADR-style record).

DDD in this course refers to the second kind, though good repo-level docs
make every feature spec shorter.

## Common pitfalls

- **Stale docs**: spec says one thing, code does another, nobody notices
  until it causes a bug. Mitigation: treat "update the spec" as part of
  done, same as tests.
- **Over-specifying**: dictating implementation details that don't
  matter, which makes the doc expensive to write and to keep in sync.
  Mitigation: specify contracts and behavior, not internals, unless the
  internals are the point.
- **Under-specifying edge cases you already know**: if you know about
  them and don't write them down, you're not saving time, you're moving
  the cost from "writing" to "debugging."
- **Treating the spec as a one-way handoff**: the value of DDD comes from
  the agent's plan being checked against the spec *before* implementation
  starts, not after.

## Lab

1. Pick a real, small-to-medium feature in a sample repo (provided
   separately, or bring your own).
2. Write a one-page spec using the anatomy above. Time yourself.
3. Give the agent *only* the spec as the task description — no extra
   verbal context.
4. Have the agent propose a plan first; review it against the spec before
   allowing implementation.
5. After implementation, check actual behavior against acceptance
   criteria. Note every place the agent had to guess, or where the spec
   was wrong/incomplete.
6. Update the spec to close those gaps.

## Deliverable

- The spec document
- The agent's plan (if plan mode was used)
- The resulting diff
- A short list: "places the spec was wrong or incomplete, and what I
  changed"

## Tools

[spec-kit](https://github.com/github/spec-kit) is GitHub's open-source
implementation of this workflow: `/specify`, `/plan`, and `/tasks` slash
commands that turn a feature description into the same
spec → plan → implement loop described above, wired into Claude Code,
Copilot, Cursor, and other agent CLIs.

## Discussion questions for a cohort setting

- At what task size does writing a spec stop paying for itself?
- Who owns keeping feature specs in sync with code — is this different
  from who owns repo-level agent docs?
- How does DDD change (or not) when the "reader" of the spec is another
  agent rather than a human reviewer?
