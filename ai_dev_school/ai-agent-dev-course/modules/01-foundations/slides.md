---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 1: Foundations

## How agentic loops actually work

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- What "agentic" actually means (vs. autocomplete)
- The core loop: plan → act → observe → repeat
- A worked trace, tool call by tool call
- Context windows, memory, and compaction
- Permissions & sandboxing
- Lab: trace and annotate a real agent run

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Explain the agent loop: plan → act via tools → observe → repeat
2. Distinguish autocomplete-style assistance from agentic tools
3. Explain context windows, and why long sessions get **compacted**
4. Explain why decisions belong in files, not just chat history

---

<!-- Slide 4 -->

## What does "agentic" even mean?

- Not "a smarter autocomplete"
- A program that can:
  - **act** on the world (read/write files, run commands)
  - **observe** what actually happened
  - **decide** the next step based on that observation
- The loop — not the model — is what makes it an agent

> A chat model answers questions. An agent does work and checks its work.

---

<!-- Slide 5 -->

## Autocomplete vs. Agentic

| | Autocomplete (Copilot-style) | Agentic (Claude Code-style) |
|---|---|---|
| Unit of output | Next tokens / one suggestion | A sequence of tool calls |
| Feedback loop | You are the only checker | Agent can run tests itself |
| Scope | One file, one cursor position | Whole repo, multiple files |
| Session memory | Little to none | Context window + files (CLAUDE.md) |
| Stops when | You stop typing | Task condition met, or stuck |

---

<!-- Slide 6 -->

## The Core Loop

```
   ┌─────────┐
   │  PLAN   │  "what should I do next, given the goal?"
   └────┬────┘
        ▼
   ┌─────────┐
   │   ACT   │  emit a tool call (read file, run test, edit...)
   └────┬────┘
        ▼
   ┌─────────┐
   │ OBSERVE │  tool result comes back into context
   └────┬────┘
        │
        └──────────► repeat until done (or stuck)
```

---

<!-- Slide 7 -->

## Step 1 — Plan

- Given the goal + everything in context, the model decides **one next action**
- Not a fixed script — re-planned after *every* observation
- Example internal reasoning:

  > "I need to add a `--verbose` flag. I don't know where CLI flags are
  > parsed yet — let me search for the existing flag definitions first."

- Planning is cheap to redo — that's the whole point of the loop

---

<!-- Slide 8 -->

## Step 2 — Act via Tools

- The plan becomes a **structured tool call**, not free text
- Examples: `read_file`, `grep`, `run_tests`, `edit_file`, `bash`

```json
{
  "tool": "grep",
  "input": { "pattern": "add_argument", "path": "src/cli.py" }
}
```

- The tool call is the interface between "thinking" and "doing"

---

<!-- Slide 9 -->

## Step 3 — Observe

- The tool's result (stdout, file contents, diff, error) is appended
  back into the model's context
- The agent doesn't "assume" success — it reads what actually came back

```
$ grep add_argument src/cli.py
src/cli.py:14:    parser.add_argument("--output", ...)
src/cli.py:18:    parser.add_argument("--dry-run", ...)
```

- This is the step that makes verification possible at all

---

<!-- Slide 10 -->

## Step 4 — Repeat & Stop

- Loop continues until one of:
  - the task's done-condition is met (tests pass, file changed as asked)
  - the agent gets stuck and asks the human
  - a permission gate blocks further action
  - a hard limit (turns, time, context) is hit
- Stopping correctly is *harder than it looks* — more in Module 12

---

<!-- Slide 11 -->

## The Full Loop, Annotated

Task: *"Add a `--verbose` flag to the CLI"*

```
PLAN:    find where flags are defined
ACT:     grep "add_argument" src/cli.py
OBSERVE: found 2 existing flags, same pattern
PLAN:    add the new flag using that pattern
ACT:     edit_file src/cli.py  (+1 line)
OBSERVE: diff applied cleanly
PLAN:    verify nothing broke
ACT:     run_tests
OBSERVE: 42 passed, 0 failed
PLAN:    done — summarize for the user
```

---

<!-- Slide 12 -->

## Worked Trace — Why Each Call Happened

| # | Tool call | Why |
|---|---|---|
| 1 | `grep add_argument` | Learn the existing convention before adding to it |
| 2 | `read_file src/cli.py` | Confirm exact insertion point + imports |
| 3 | `edit_file` | Apply the minimal change |
| 4 | `run_tests` | Verify the change didn't break anything |
| 5 | `bash: python cli.py --verbose` | Confirm the flag actually works end-to-end |

*This table is exactly the shape of your lab deliverable.*

---

<!-- Slide 13 -->

## Context Windows — What They Are

- A **context window** = everything the model can "see" for this turn:
  - system prompt / instructions
  - conversation history
  - file contents it has read
  - tool outputs it has received
- It's finite. Think of it as a **desk**, not a filing cabinet —
  only what's currently on the desk can be worked with

---

<!-- Slide 14 -->

## Context Limits in Practice

- Reading a huge file or a noisy command's full output can eat a large
  share of the available space in one step
- Effects as a session fills up:
  - earlier instructions get "crowded out" of attention
  - the agent may re-read files it already saw
  - quality can degrade near the limit
- Good agents read *narrowly* (specific lines, filtered grep) on purpose

---

<!-- Slide 15 -->

## Memory & Compaction

- When a session runs long, the tool **compacts**: older turns get
  summarized so the conversation fits back in the window
- What tends to survive compaction: the current goal, key decisions,
  file state
- What tends to get lossy: exact earlier phrasing, minor side-details,
  the *reasoning trail* behind a decision

> Compaction is a feature, not a bug — but it is lossy. Plan for it.

---

<!-- Slide 16 -->

## Decisions Belong in Files

- Chat history is not durable — it gets compacted or the session ends
- Durable memory = **files in the repo**:
  - `CLAUDE.md` / `AGENTS.md` — standing instructions for the agent
  - specs, ADRs, code comments — durable decisions
- Rule of thumb: if you'd be upset to lose it, it belongs in a file,
  not just in what you typed

---

<!-- Slide 17 -->

## Permissions & Sandboxing

- Agents ask before **risky, hard-to-reverse actions**:
  - running arbitrary shell commands
  - editing/deleting files outside the working set
  - network access, installing packages
- This isn't the model being unsure — it's a **trust boundary** by design
- Read access ≠ write access ≠ execute access

---

<!-- Slide 18 -->

## Recap — Agentic vs. Autocomplete

| Autocomplete | Agentic loop |
|---|---|
| Suggests | Plans, acts, observes, repeats |
| You verify | It can verify itself (tests, output) |
| No memory across steps | Context window + durable files |
| No permission model | Explicit trust boundaries |

---

<!-- Slide 19 -->

## Failure Modes to Watch For

- **Stuck retry loop** — same failing action, no new information
- **Silent scope creep** — "fixing" things nobody asked for
- **Context exhaustion mid-task** — losing track of the original goal
- **Over-trusting tool output** — not double-checking a "success" claim

*We'll build habits against these starting Module 5, formally in Module 12.*

---

<!-- Slide 20 -->

## Lab — Trace an Agent

1. Pick a small, unfamiliar toy repo
2. Give an agent one task: *"add a CLI flag that does X"*
3. Log **every** tool call: reads, greps, edits, test runs
4. Next to each: one sentence — *why do you think it did that?*

Goal: see the loop from Slides 6–12 happen live, in your own trace.

---

<!-- Slide 21 -->

## Deliverable

- **Annotated tool-call trace** (like the table on Slide 12)
- **Half-page writeup** answering:
  - Where did the agent spend most of its "effort" —
    reading/understanding, or writing code?
  - Did anything surprise you about the order of operations?

---

<!-- Slide 22 -->

## Recap & Next Module

- Agentic = plan → act → observe → repeat, with real verification
- Context windows are finite; compaction is lossy — write durable memory
  to files
- Permissions exist because act/observe touches the real world

**Next — Module 2: MCP**
*Hands for the agent: safe access to outside systems.*
