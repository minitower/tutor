---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 8: Multi-Agent Orchestration

## Implementer/reviewer/orchestrator patterns

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- Why one agent, one pass, is sometimes not enough
- Pattern 1: Implementer/reviewer split
- Pattern 2: Orchestrator/worker fan-out
- Pattern 3: Critic-executor loops
- When parallelism helps vs. when it just adds coordination cost
- Lab: build a two-agent implement-then-review pipeline

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Compose more than one agent role on a single task
2. Explain three multi-agent patterns and when each applies
3. Judge when parallelism/specialization is worth its overhead —
   and when it's just theater
4. Run a real implementer → reviewer pipeline and read its output
   critically

---

<!-- Slide 4 -->

## The Blind Spot Problem

- A single agent session reviewing its own work has a structural bias:
  it already knows what it *meant* to do
- Re-reading your own diff ≠ reviewing it — you pattern-match to your
  intent, not to what's actually on the page
- This isn't specific to AI — it's why humans use code review at all
- One fix: **a second agent, with no memory of the first one's
  reasoning**

> "Looks right" is the most dangerous sentence in software.

---

<!-- Slide 5 -->

## Pattern 1 — Implementer/Reviewer Split

- Agent A implements the change, with full context: task, codebase,
  its own reasoning trail
- Agent B reviews — **fresh session**, given only:
  - the original task/spec
  - the resulting diff
- No access to Agent A's chat history or rationale
- B's job: find what A is blind to, not just restate what A already
  knows

---

<!-- Slide 6 -->

## Implementer/Reviewer — Diagram

```
   task + spec
        │
        ▼
 ┌─────────────┐
 │ Implementer │   full context, own reasoning trail
 │   Agent A   │
 └──────┬──────┘
        │  diff + original task only
        │  (reasoning does NOT cross this line)
        ▼
 ┌─────────────┐
 │  Reviewer   │   fresh session, no shared memory
 │   Agent B   │
 └──────┬──────┘
        │
        ▼
  approve / request changes → merge
```

---

<!-- Slide 7 -->

## Why "Fresh" Is the Whole Point

- If B reuses A's session, B inherits A's framing — same blind spots
- Giving B only the diff + task forces it to re-derive "does this
  actually satisfy the ask," not "did A follow their own plan"
- Practical setup: separate context window, separate prompt — think
  "new hire reviewing a PR," not "same person re-reading their own work"
- Cost: a second full read of the diff, every time — not free

---

<!-- Slide 8 -->

## Pattern 2 — Orchestrator/Worker Fan-Out

- One coordinating agent breaks a large task into **independent**
  sub-tasks
- Each sub-task goes to its own worker agent (own context, own tool
  calls)
- Orchestrator collects results and integrates them
- Works well when sub-tasks genuinely don't depend on each other's
  intermediate decisions

---

<!-- Slide 9 -->

## Orchestrator/Worker — Diagram

```
          ┌───────────────┐
          │ Orchestrator  │   splits task, tracks progress
          └───────┬───────┘
     independent sub-tasks, dispatched in parallel
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐
│Worker A│    │Worker B│    │Worker C│
│migrate │    │migrate │    │migrate │
│module 1│    │module 2│    │module 3│
└───┬────┘    └───┬────┘    └───┬────┘
    └──────────────┼──────────────┘
                    ▼
           integrate + resolve
              overlaps
```

---

<!-- Slide 10 -->

## The Hard Part Is Integration

- Fan-out is easy; **merging** independent results safely is not
- Watch for:
  - two workers touching the same shared file/interface differently
  - a shared assumption that was true for the orchestrator but false
    for one worker's slice
  - workers silently disagreeing on a convention (naming, error
    shape) because neither saw the other's output
- The orchestrator's real job is the integration pass, not the split

---

<!-- Slide 11 -->

## Pattern 3 — Critic-Executor Loops

- Executor produces an attempt; a critic agent evaluates it against
  criteria; executor revises
- Loop repeats **without a human approving every round** — human sets
  the criteria and a stopping condition up front
- Different from implementer/reviewer: same task, iterative
  convergence, not a one-shot gate before merge

---

<!-- Slide 12 -->

## Critic-Executor — Diagram

```
   ┌───────────┐   produces attempt   ┌───────────┐
   │ Executor  │ ───────────────────► │  Critic   │
   └───────────┘                      └─────┬─────┘
        ▲                                   │
        │        revise per critique        │
        └───────────────────────────────────┘

   loop until: critic accepts, OR round limit hit
```

- Example: generate a migration script → critic checks it against the
  acceptance criteria → executor patches → re-check

---

<!-- Slide 13 -->

## Stopping Conditions Matter

- Without a limit, critic-executor loops can oscillate or rubber-stamp
  each other
- Set upfront:
  - a max round count (e.g., 3 revisions, then escalate to a human)
  - concrete acceptance criteria the critic checks against — not
    "does this look good"
  - what happens on non-convergence (stop and surface, don't loop
    forever)

---

<!-- Slide 14 -->

## Comparing the Three Patterns

| Pattern | Shape | Best for |
|---|---|---|
| Implementer/reviewer | Sequential, one gate | Pre-merge quality check |
| Orchestrator/worker | Parallel fan-out | Large, decomposable tasks |
| Critic-executor | Iterative loop | Converging on a spec without a human every round |

- All three trade tokens/time for a structural check a single pass
  can't give you

---

<!-- Slide 15 -->

## When Parallelism Helps

- Sub-tasks are genuinely independent (different files/modules, no
  shared decision to make)
- The task is large enough that serial execution is the bottleneck,
  not correctness
- Each worker's output can be verified in isolation before integration
- Example: applying the same mechanical refactor across N independent
  modules

---

<!-- Slide 16 -->

## When Parallelism Hurts

- Sub-tasks share a decision (a schema, a naming convention, an
  interface) that must stay consistent across all of them
- The "split" itself is the hard part — if you can't cleanly separate
  the work, you can't cleanly separate the agents either
- Coordination overhead (reconciling outputs) can exceed the time
  saved by parallel execution
- Small tasks: a second agent pass often costs more than the bug it
  might catch

---

<!-- Slide 17 -->

## A Cost/Benefit Heuristic

- Ask before adding an agent role:
  1. What specific blind spot does this extra pass address?
  2. What's the cost — tokens, wall-clock time, review effort on the
     agent's output itself?
  3. Is this change high-stakes enough that an independent check is
     worth that cost?
- Reserve multi-agent setups for changes where the answer to #3 is yes
- More in Module 9 on what "worth it" means in practice

---

<!-- Slide 18 -->

## Failure Modes to Watch For

- **Rubber-stamping** — reviewer/critic agent just agrees, adds no
  independent signal
- **Shared blind spot** — both agents trained on the same patterns,
  miss the same thing
- **Integration blindness** — orchestrator approves pieces that don't
  actually fit together
- **Cost creep** — "just add a reviewer" becomes 3x the tokens for
  marginal extra catches
- A multi-agent setup is only as good as its independence

---

<!-- Slide 19 -->

## Lab — Two-Agent Pipeline

1. Pick a nontrivial change (not a one-liner — something with a real
   edge case or design decision in it)
2. Agent A implements it, with full task context
3. Start **Agent B fresh** — give it only the original task and the
   resulting diff, nothing else
4. B reviews and reports findings before merge

Goal: see whether independent review catches something the
implementer missed — or confirms it didn't need to.

---

<!-- Slide 20 -->

## Deliverable

- The full pipeline transcript (both agents)
- A list of issues Agent B caught that Agent A missed
- **Or** — an honest note that B caught nothing new

Both outcomes are useful data: catching real issues justifies the
overhead here; catching nothing is itself a signal about when this
pattern is (and isn't) worth running.

---

<!-- Slide 21 -->

## Recap & Next Module

- Implementer/reviewer: fresh eyes catch what "I know what I meant"
  hides
- Orchestrator/worker: fan-out helps for genuinely independent work —
  integration is the real work
- Critic-executor: iterate without a human on every round, but bound
  the loop
- None of this is free — spend it on changes where it's worth the cost

**Next — Module 9: Verification & Review**
*Trust but verify.*
