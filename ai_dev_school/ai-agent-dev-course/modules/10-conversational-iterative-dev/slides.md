---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 10
## Conversational / Iterative Development

**Case study focus:** Tight loops, no upfront doc

*Agentic Software Development: From Specs to Shipped Code*

---

<!-- Slide 2 -->

## Agenda

- Where conversational work sits among the methodologies so far
- Incremental correction — fixing course without restarting
- Agent drift — what it looks like, how to catch it, how to recover
- Session/context management on long conversations
- The no-paper-trail cost, and how to offset it
- Lab: rebuild Module 6's feature, purely conversationally

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

- Run a tight feedback loop for a small or exploratory task with **no**
  spec doc
- Recognize agent drift before it compounds across several turns
- Correct an agent with a short, targeted message instead of restating
  the whole task
- Decide when to keep patching a session vs. start a fresh one
- Name what this mode costs you later, and mitigate it cheaply

---

<!-- Slide 4 -->

## Where this fits

| Methodology | Best for | Weak for | Artifact left behind |
|---|---|---|---|
| DDD (spec-first) | Real ambiguity, multi-person context | Tiny fixes | Durable spec doc |
| Plan-first | Refactors, risky multi-file changes | Fast exploration | Ephemeral plan/ADR |
| TDD-with-agent | Bug fixes, well-defined logic | Vague/exploratory UI | Test suite |
| **Conversational** | **Prototypes, one-offs, exploration** | **Anything needing a paper trail** | **None (chat only)** |

Every other module front-loads structure. This one deliberately doesn't.

---

<!-- Slide 5 -->

## What "conversational / iterative" means

- No spec, no plan doc, no test-first contract — just you and the agent,
  turn by turn
- You react to what the agent just did instead of specifying everything
  up front
- The task description **is** the conversation — nothing gets written
  down beside it
- This is the default mode most people fall into by accident. The goal
  here is to do it **on purpose, and well**

---

<!-- Slide 6 -->

## When to reach for it (and when not to)

**Good fit:**
- Small, well-bounded tasks where writing a spec would cost more than
  the task itself
- Exploration — you don't know the shape of the solution yet
- Throwaway scripts, spikes, "just try three approaches and show me"

**Bad fit:**
- Anything a teammate (or you, in six months) will need to understand
  without you in the room
- Multi-file changes with real ambiguity — that's Module 6 or 8's job

---

<!-- Slide 7 -->

## Key concept: Incremental correction

The core skill of this mode: **short, specific course-corrections beat
restating the whole task.**

- Restating the task from scratch throws away everything the agent
  already got right
- A precise correction narrows the search space; a vague one widens it
- Point at the **symptom and the boundary** — what's wrong, and what
  must *not* change

---

<!-- Slide 8 -->

## Incremental correction — example

**Weak correction:**
> "That's not quite right, the export should also handle empty
> ranges and the filters properly, can you redo it"

**Strong correction:**
> "Don't touch the button or the endpoint route — just the
> `export_reports_csv` function. An empty date range should return a
> header-only CSV, not a 500. Revert the retry-loop you added, that's
> unrelated."

Strong version names the file, the exact behavior, and what to leave alone.

---

<!-- Slide 9 -->

## Key concept: Agent drift

**Agent drift:** the agent quietly wanders from the actual goal while
still producing plausible-looking work, turn after turn.

Common causes:
- The original ask was ambiguous, and an early wrong guess compounds
- The agent "solves" a nearby problem instead of the real one
- A constraint you stated 15 turns ago scrolled out of active context
- It fixates on the wrong root cause and keeps patching symptoms

---

<!-- Slide 10 -->

## Detecting drift — signals

- The diff touches files or areas you never mentioned
- The agent's explanation of *what it did* no longer matches *what you
  asked for*
- You've said "no, that's not what I meant" more than once about the
  same request
- The agent claims something works, but you haven't verified it
  yourself — and when you do, it doesn't
- Confidence language ("this should now work") standing in for evidence

---

<!-- Slide 11 -->

## Recovering from drift

1. **Name the exact deviation** — not "this is wrong," but "you
   changed the auth middleware, I only asked about the CSV serializer"
2. **Roll back the specific change**, don't layer a fix on top of a
   wrong turn
3. **Re-anchor on ground truth**: run `git diff` / `git status` and the
   actual app — don't trust the agent's self-report
4. **When drift is deep** (many compounding turns): it's often cheaper
   to start a **fresh session** than to keep patching this one

---

<!-- Slide 12 -->

## Worked example: drift and recovery

> Turn 4: "Add CSV export with a date-range filter."
> Turn 9: agent has also refactored the shared query builder "for
> consistency" — unrequested, untested, now part of the diff.

**Recovery:**
> "Revert the query-builder refactor — out of scope. Keep only the
> export function and the new route. Show me the diff before we go
> further."

Naming the exact unwanted change (not "this is messy") is what makes
the correction land in one turn instead of three.

---

<!-- Slide 13 -->

## Key concept: Session/context management

- Long conversations fill the context window; tools **compact** older
  turns — summarize or drop them
- Symptoms of context pressure: the agent re-asks something you already
  told it, contradicts an earlier decision, forgets a file it already
  edited
- A session that has drifted and been corrected several times now
  carries that whole messy history as context for its *next* guess

---

<!-- Slide 14 -->

## Session/context management — practical rules

- **Start fresh** when: a wrong turn has compounded, the session's
  history of mistakes is now feeding new guesses, or you're switching
  to an unrelated subtask
- Don't rely on the agent's memory of a messy history — write a short
  **state-of-the-world recap** instead: what's done, what's next, what
  constraints still apply
- Standing constraints ("no new dependencies," "don't touch auth")
  belong in `CLAUDE.md` / `AGENTS.md`, not buried in turn 6 of a chat —
  that way they survive a session reset

---

<!-- Slide 15 -->

## The no-paper-trail problem

- Chat history is not a durable, reviewable artifact — no spec, no
  plan, no test file capturing *intent*
- Six months later: "why does this code do X?" has no answer besides
  git blame and a guess, or hoping someone remembers the conversation
- This is the direct tradeoff for the syllabus row: Conversational →
  weak for "anything needing a paper trail," artifact left behind:
  **none**

---

<!-- Slide 16 -->

## Mitigating the paper-trail cost

You can't get the durability of a spec for free, but you can buy some
of it cheaply:

- **Commit messages that explain why**, not just what
- A short note (even a code comment) for any non-obvious call the
  agent made and you accepted
- If a throwaway conversation produces something that turns out to
  matter — **promote it**: write the two-paragraph doc after the fact

---

<!-- Slide 17 -->

## Lab: rebuild Module 6's feature, conversationally

Same feature as Module 6's lab (e.g. the CSV-export-for-reports-dashboard
example from this course) — but this time:

- **No spec doc.** No plan doc. Just talk it into existence, turn by turn
- React to what the agent produces; correct as you go
- Let yourself hit at least one real drift moment — don't route around
  it by over-preparing your prompts

---

<!-- Slide 18 -->

## Lab: what to track

- **Number of turns** to a working result
- **Number of corrections** — and for each, was it incremental
  (targeted) or a full restate?
- **Where drift happened**, and how you caught it
- **Total time spent**, including the correction turns
- Whether you had to start a fresh session, and why

---

<!-- Slide 19 -->

## Deliverable

A side-by-side comparison against the **Module 6 (DDD)** result:

- Turns/time spent, this mode vs. DDD
- Quality of the final code — does it meet the same acceptance criteria
  Module 6 used?
- Would you **trust either result** without a review pass? Why or why not?

---

<!-- Slide 20 -->

## Recap

- Incremental correction: name the symptom and the boundary, don't
  restate the whole task
- Agent drift is quiet — catch it from the diff and the app, not from
  the agent's own narration
- Long sessions degrade; a short recap can beat a drifted memory
- This mode trades a paper trail for speed — know when that trade is
  worth making

---

<!-- Slide 21 -->

## Next up

**Module 11 — Multi-Agent Orchestration.** Where a single conversational
loop stops scaling, split the work: an implementer and a reviewer, or an
orchestrator fanning work out to several agents at once.
