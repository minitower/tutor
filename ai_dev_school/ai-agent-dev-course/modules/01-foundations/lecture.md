# Module 1 — Lecture Script: Foundations

*How agentic loops actually work*

This script is written as spoken narration. Read it as a guide, not a
teleprompter — adapt the asides and rhetorical questions to the room.
Section timings assume a live 2–3 hour session that includes the lab;
roughly 100–120 minutes of lecture plus 60–90 minutes of hands-on lab
and discussion.

---

## Slide 1 — Module 1: Foundations
*~3 min*

Welcome to Module 1. Before we write a single prompt or touch a single
repo, we need to build a shared mental model of what's actually
happening when you run an agent like Claude Code against your codebase.

Here's the thing — most people who've used ChatGPT or Copilot think
they already understand "AI coding tools." And they're partially
right: the underlying model is doing similar next-token prediction
either way. But the *system* built around that model — the thing that
lets it read your files, run your tests, and iterate — that's a
different animal entirely. That system is what we mean by "agentic,"
and understanding its mechanics, not just its vibes, is the entire
point of today.

By the end of this module you won't just have a definition of "agent"
you can recite — you'll have watched one work, tool call by tool call,
and you'll know exactly why it did what it did.

---

## Slide 2 — Agenda
*~1 min*

Quick roadmap. We'll start conceptual — what "agentic" means and how
it differs from autocomplete — then get mechanical: the actual loop,
step by step, with a worked trace you could reproduce yourself. Then
we'll talk about the two things that make agents behave differently
in short sessions versus long ones: context windows and memory. We'll
close with permissions — why the agent keeps asking you "can I run
this?" — and then hand you the lab, which is: go watch one do this for
real, on your own machine, and write down what you see.

---

## Slide 3 — Objectives
*~2 min*

Four concrete things you should be able to do after this module.
Explain the loop. Tell autocomplete and agentic tools apart — not by
vibes, but by mechanism. Explain what a context window is and why
compaction happens. And explain *why* — not just "you should" but
*why* — decisions belong in files rather than chat history. That last
one seems like a small point now; it's going to come back constantly
for the rest of the course, especially in Module 6 when we talk about
Document-Driven Development.

---

## Slide 4 — What does "agentic" even mean?
*~8 min*

Let's get precise about a word that gets used loosely. "Agentic" does
not mean "a smarter model." GPT-3 versus GPT-4 versus Claude Opus
versus Claude Sonnet — that's a difference in *capability*. Agentic is
a difference in *architecture*: it's about whether the system around
the model can act, observe the result of that action, and decide what
to do next based on what it actually observed.

Think about the difference between asking a very smart colleague a
question over email, versus having that same colleague sit down at
your terminal, run a command, look at the output, and then decide what
to do next based on what actually happened. Same intelligence. Wildly
different amount of *work* they can reliably do, because in the second
case they're not guessing what's in your codebase — they're looking.

Here's a framing I want you to hold onto for the whole course: a chat
model answers questions. An agent does work and checks its work. That
second half — checks its work — is doing almost all of the heavy
lifting in why these tools are useful for real software engineering
and not just snippets.

I'll throw a question at the room: when you've used a plain chat
model to help with code before — paste in a function, ask "why is this
broken" — what did you have to do that the model couldn't? ... Right,
you had to run it. You had to be the feedback loop. Today we're
talking about what happens when the tool can be its own feedback loop,
at least partially.

---

## Slide 5 — Autocomplete vs. Agentic
*~7 min*

Let's make that concrete with a comparison, because "autocomplete vs.
agentic" is a distinction people nod along to without really absorbing.

Look at the "unit of output" row first. Copilot-style tools produce
the next few tokens, or one suggestion at your cursor. An agentic tool
produces a *sequence* of tool calls — read this, then run that, then
edit this — that can span the whole session.

The feedback loop row is the one I think matters most. With
autocomplete, you are the only thing checking whether the suggestion
is any good. You read it, you decide, you accept or reject. With an
agentic tool, the agent itself can run the test suite it just touched
and see whether it's green — before it ever shows you anything. That
doesn't mean it's always right. It means the *loop* includes a
verification step that plain autocomplete structurally cannot have,
because autocomplete doesn't have hands.

Scope: one file and one cursor position, versus a whole repository,
potentially dozens of files. Session memory: autocomplete tools
mostly don't carry state between suggestions in any deep way; agentic
tools carry a context window forward and, as we'll see, can read
durable files like CLAUDE.md at the start of a session. And "stops
when" is subtle but important — autocomplete stops when *you* stop
typing. An agentic tool has to decide for itself when the task
condition is met, or when it's stuck. That's a genuinely hard problem
and we'll come back to it on Slide 10.

---

## Slide 6 — The Core Loop
*~10 min*

Here is the whole mental model for this module, in one diagram. Plan.
Act. Observe. Repeat.

Walk through it with me before we zoom into each piece. The agent
starts with a goal — something you gave it — and whatever's currently
in its context. It **plans**: decides, given everything it currently
knows, what the single next useful action is. Not the whole solution.
Just the next step. It then **acts** — that plan gets turned into an
actual tool call, a structured request like "read this file" or "run
this command." The tool executes, and whatever happens — success,
failure, some file contents, an error message — gets fed back in as
the **observation**. And then the loop goes back to planning, now with
one more piece of information than it had before.

This keeps going until the agent decides the task is done, or it gets
stuck and needs you, or something blocks it — we'll get to permissions
— or it hits a hard limit.

I want to emphasize something that's easy to miss: this is not "the
model writes an essay describing a plan, and then separately writes
code." Planning happens at *every single step*, re-evaluated in light
of the latest observation. That's what makes it adaptive instead of
scripted. If step 2 reveals something surprising — say, the file
doesn't have the structure the agent expected — the *next* plan
reflects that surprise. A fixed script can't do that. A loop can.

This four-step loop is going to be the skeleton for literally
everything else in this course. Every methodology we cover in later
modules — TDD with agents, plan-first workflows, multi-agent
orchestration — is a way of *shaping* this loop, not replacing it.

---

## Slide 7 — Step 1: Plan
*~6 min*

Let's slow down and look at each stage on its own, starting with
planning.

At this step, the model has some goal — "add a `--verbose` flag" — and
whatever's currently sitting in its context window: your instructions,
maybe some files it's already read, maybe some previous tool outputs.
From all of that, it has to pick exactly one next action.

Look at the example reasoning on the slide: "I need to add a
`--verbose` flag. I don't know where CLI flags are parsed yet — let me
search for the existing flag definitions first." Notice what's *not*
happening there. The model isn't trying to write the whole feature in
its head first and then execute a checklist. It's identifying the one
piece of missing information that would most reduce its uncertainty,
and going to get exactly that.

Why does this matter pedagogically? Because when you watch a trace
later in the lab and you see the agent do something that looks
indirect — read a file you didn't ask about, run a search that seems
unrelated — the question to ask isn't "why didn't it just do the
task." It's "what uncertainty was it resolving right there." Almost
always, there's an answer, and finding that answer is literally your
lab deliverable.

One more thing worth saying out loud: planning is cheap to redo. That
sounds like a throwaway line but it's actually the entire justification
for the loop's design. Because re-planning after every observation is
computationally cheap relative to, say, writing wrong code and having
to unwind it, the system is *biased toward frequent, small
course-corrections* rather than committing early to a long plan and
hoping it holds up. That's a very different posture than traditional
programming, where planning up front is expensive and we try to get it
right the first time.

---

## Slide 8 — Step 2: Act via Tools
*~7 min*

The plan by itself doesn't do anything — it has to become an actual
action. And critically, it becomes a **structured** action, not
another paragraph of prose.

Look at the JSON snippet. `{"tool": "grep", "input": {"pattern":
"add_argument", "path": "src/cli.py"}}`. That's not flavor text — that
is, roughly, the actual shape of what gets sent to execute. It names a
specific tool and gives it specific, typed parameters. This matters
because it's what makes the action *reliable and inspectable*. The
model isn't asking a human to interpret "please look for where
arguments get added" — it's issuing something a program can execute
deterministically and something you, the developer, can look at
afterward and know exactly what ran.

This is also the boundary where permissions live, which we'll get to
on Slide 17 — because a tool call is a concrete, nameable action
("run this shell command," "write to this file"), the system around
the model can inspect *that specific call* and decide whether to allow
it, before it happens. You can't put a permission gate around vague
prose. You can put one around `bash: rm -rf /`.

Common tools you'll see across agentic coding tools, regardless of
vendor: reading files, searching/grepping across a codebase, editing
or writing files, running shell commands, running a test suite. Some
tools also expose more specialized capabilities through protocols like
MCP — the Model Context Protocol — which lets an agent call out to
external tools and services in the same structured way. We're not
diving into MCP mechanics today, but keep the name in your head; it
comes up again later in the course when we talk about wiring agents
into CI/CD in Module 13.

---

## Slide 9 — Step 3: Observe
*~7 min*

This is, in my opinion, the most underrated step of the four, because
it's the one that makes the word "verify" mean something real instead
of aspirational.

When the tool call executes, whatever comes back — stdout, a file's
contents, a diff, a stack trace, an exit code — gets appended into the
model's context. Look at the example: `grep add_argument src/cli.py`
returns two lines showing exactly how existing flags are defined. The
agent didn't guess that pattern from general Python knowledge; it
*read it off the actual file*, in this actual repo, with this actual
codebase's conventions.

Here's the contrast I want you to sit with: a plain chat model, asked
"how do I add a flag to this CLI," will answer from its training
distribution — plausible, generic, probably syntactically fine, and
possibly wrong for *your* codebase's actual conventions. An agent in a
loop doesn't have to guess, because it looked. That's the difference
between "statistically likely" and "verified against the artifact in
front of it."

This is also where things can go wrong in instructive ways, and it's
worth naming now so you notice it in the lab: the agent has to
correctly *parse* what came back. A test runner that exits 0 but
prints "0 tests ran" is a success from one angle and a red flag from
another. We'll talk more about over-trusting tool output on Slide 19
as a named failure mode — file this away.

---

## Slide 10 — Step 4: Repeat & Stop
*~7 min*

The loop keeps going — plan, act, observe, plan, act, observe — until
one of a few things happens, and I want to go through all four because
the failure modes hide in here.

First, and best case: the task's done-condition is met. Tests pass,
the file changed the way you asked, the thing works. Second: the agent
gets stuck — it's tried a couple of approaches, none worked, and
rather than spinning forever it surfaces that to you and asks for
direction. Third: a permission gate blocks it — it wants to do
something that requires your explicit sign-off, and it's waiting on
you rather than proceeding. Fourth: it hits a hard limit — a cap on
turns, on time, or on context space — and the session has to wrap up
one way or another regardless of whether the task felt "done."

I said in the intro that stopping correctly is harder than it looks,
and here's why: an agent that stops too eagerly reports false success
— "done!" when it isn't. An agent that doesn't know how to stop can
burn an enormous number of turns retrying a broken approach, which
looks, from the outside, exactly like it's "still working" right up
until you notice nothing has actually changed in ten minutes. Getting
this right is a full topic — we're going to spend real time on
verification discipline in Module 12. For today, just internalize that
"repeat until done" is doing a lot of unstated work, and part of your
job as the human in the loop is noticing when the stopping condition
was satisfied for the wrong reasons.

---

## Slide 11 — The Full Loop, Annotated
*~5 min*

Let's put all four steps together on one concrete, small task: add a
`--verbose` flag to a CLI.

Walk the trace top to bottom with me. Plan: find where flags are
defined — the agent doesn't know yet, so that's the first uncertainty
to resolve. Act: grep for the pattern. Observe: two existing flags,
same convention. Plan: use that same convention for the new flag. Act:
edit the file, one line added. Observe: diff applied cleanly, no
conflicts. Plan: now verify nothing broke — notice this step exists at
all; the agent isn't done just because it made an edit. Act: run the
test suite. Observe: 42 passed, 0 failed. Plan: done, summarize for
the human.

Nine steps, three full plan-act-observe cycles, for what looks from
the outside like "add a flag." That's not inefficiency — that's what
verified work actually looks like when you make every step visible
instead of hiding it behind a single "here's your code" response. This
is exactly the shape you're going to be building yourself in the lab,
just on a task and repo you haven't seen before.

---

## Slide 12 — Worked Trace — Why Each Call Happened
*~6 min*

Now let's do the thing your lab deliverable is actually asking for:
take each tool call and write down, in one sentence, *why* it
happened.

`grep add_argument` — this establishes the existing convention before
adding to it; it's a reconnaissance step, not the work itself.
`read_file src/cli.py` — confirms the exact insertion point and
whatever imports the new code will need; grep tells you *that*
something is there, reading the file tells you exactly *where* and
*how*. `edit_file` — the actual change, and notice it comes only after
two information-gathering steps, not before them. `run_tests` — this
is the self-verification step we keep coming back to; the agent
doesn't take its own edit on faith. And `bash: python cli.py
--verbose` — even after tests pass, there's a final end-to-end sanity
check that the flag *actually does something* when invoked, not just
that it parses without error.

This table is your lab deliverable's skeleton. When you run your own
agent later today, you're going to build exactly this table for a
trace you generate yourself, on a repo you've never seen, for a task
you pick. The habit I want you to build here is: for every tool call
in the log, force yourself to write one real sentence about the
uncertainty it was resolving — not "it read a file" but *why that file,
why then*.

---

## Slide 13 — Context Windows — What They Are
*~7 min*

Let's shift from the loop's mechanics to a constraint that shapes
everything about how the loop behaves in practice: the context window.

Definition: the context window is everything the model can "see" for
a given turn. That includes the system prompt and standing
instructions, the conversation history so far, the contents of any
files it has read, and the output of any tool calls it has made. All
of that lives in one shared, finite space.

The analogy I want you to keep is a desk, not a filing cabinet. A
filing cabinet can hold an enormous amount, and you retrieve one
folder at a time as needed. A desk has a hard physical limit to how
much can be spread out and worked on *simultaneously*. The context
window is the desk. Everything the agent is actively reasoning about
in this step has to be on the desk at the same time. If you pile ten
enormous files onto the desk, there's less room for everything else —
your original instructions, the task goal, earlier findings.

This single idea — finite, shared workspace — explains a surprising
amount of agent behavior that otherwise looks mysterious: why an agent
sometimes seems to "forget" something you said forty messages ago, why
reading a giant log file can visibly change how the agent behaves
afterward, why some agents specifically prefer narrow, targeted reads
over dumping whole files into context.

---

## Slide 14 — Context Limits in Practice
*~7 min*

So what actually happens when that desk starts filling up?

First-order effect: reading something huge — a massive file, or a
command whose output is thousands of lines of build noise — can
consume a large fraction of the available space in a single step. It's
not "a little" cost, it can be a very large, sudden cost.

Second-order effects, as a session fills up: instructions given early
in the session effectively get "crowded" — they're technically still
there, but they're competing with a lot more material for the model's
attention on each subsequent step, and in practice, adherence to early
instructions measurably degrades the further you get from them. You
might see an agent re-read a file it already looked at ten minutes
ago, not out of forgetfulness so much as the earlier read having been
summarized away or pushed into a less salient part of the window.
Quality in general can degrade as a session approaches its limit.

The practical takeaway, and it's one you'll feel directly in the lab:
good agents — and good agent *users* — try to read narrowly. Grep for
the specific pattern rather than cat-ing the whole file. Ask for lines
50 through 80 rather than the whole 3,000-line log. It's not just
politeness to the token budget; it directly protects the quality of
everything else the agent is trying to hold onto in that session.

---

## Slide 15 — Memory & Compaction
*~8 min*

Now, what happens when a session runs long enough that even careful
reading isn't enough — the conversation itself has grown past what
fits?

The tool **compacts**: it takes the older parts of the conversation and
replaces them with a summary, so the whole thing fits back into the
window and the session can keep going instead of just failing outright.

This is worth being precise about, because "compaction" sounds like a
minor technical detail and it is actually one of the most practically
important facts in this whole module. What tends to survive
compaction reasonably well: the current goal, key decisions that were
made, the state of files as they stand now. What tends to get
lossy: the *exact* earlier phrasing of things, minor side details that
seemed unimportant at the time, and — this is the one I want you to
really internalize — the reasoning trail behind a decision. You might
retain "we chose approach B" without a crisp record of *why* B was
chosen over A, especially if that reasoning happened many turns ago
and got folded into a terse summary.

I want to head off a natural misreading here: compaction is not a bug
or a limitation someone forgot to fix. It's a deliberate, necessary
feature — without it, long sessions would simply stop working once
they outgrew the window, full stop. The point isn't "compaction is
bad." The point is "compaction is lossy, so plan for it," which is a
completely different, much more actionable takeaway. And that
takeaway leads directly into the next slide.

---

## Slide 16 — Decisions Belong in Files
*~7 min*

Given that chat history is not durable — it gets compacted mid-session,
and it evaporates entirely once the session ends — where should the
things you actually care about live?

In files. Specifically: `CLAUDE.md` or `AGENTS.md` — standing
instructions that get loaded fresh into an agent's context at the
start of a session, regardless of whether this is session one or
session fifty on this repo. And more broadly, specs, Architecture
Decision Records, code comments — anything that records a decision
durably, in the artifact itself, rather than only in the conversation
that produced it.

Here's a rule of thumb I want you to actually use, not just remember:
if you would be upset to lose it, it does not belong only in what you
typed into the chat box. It belongs in a file. If you told the agent
"always use tabs, not spaces, in this repo" and that instruction
matters for every future session, that's a `CLAUDE.md` line, not a
one-off chat message that will get compacted away in session two and
forgotten by session ten.

This idea is genuinely foundational to the rest of the course. Module
6 is going to spend an entire session on exactly this principle — using
written specs as the durable contract between you and the agent, and
treating repo-level agent docs as living artifacts rather than
one-time setup. Everything we do from here forward assumes you've
internalized: chat is ephemeral, files are durable, act accordingly.

---

## Slide 17 — Permissions & Sandboxing
*~6 min*

Last mechanical piece before we wrap the concepts and move to the lab:
why does the agent keep stopping to ask "can I run this command?"

It's not the model being unsure of itself. It's a deliberately
designed trust boundary. Certain classes of action get flagged for
explicit approval before they execute: running arbitrary shell
commands, editing or deleting files outside whatever working set
you've scoped the agent to, reaching out over the network, installing
packages. These are actions that are either hard to reverse, touch
things beyond the immediate task, or could have consequences outside
the sandbox you intended the agent to operate in.

The distinction I want you to walk away with: read access, write
access, and execute access are three different levels of trust, and a
well-designed agentic tool treats them differently. Reading a file is
low-risk and usually happens freely. Writing to a file you've scoped
the agent to is a bit more consequential but still contained. Running
an arbitrary shell command is the highest-risk category, because a
shell command can do almost anything on the machine it runs on — which
is exactly why that's the category most tightly gated behind explicit
permission.

We're going to spend a full module on this later — Module 13 covers
wiring agents into CI/CD with permission scopes and human-in-the-loop
gates for anything irreversible. For today, just notice it happening
in your own lab session, and notice which categories of action
triggered a prompt versus which ones didn't.

---

## Slide 18 — Recap — Agentic vs. Autocomplete
*~3 min*

Quick recap before we move to failure modes and the lab. We started
this module by putting autocomplete and agentic tools side by side,
and now that we've been through the whole loop, the table should read
differently than it did on Slide 5. Autocomplete suggests; the
agentic loop plans, acts, observes, and repeats. You verify
autocomplete's output; an agentic tool can verify a meaningful chunk
of its own output before you ever see it. Autocomplete has no memory
across steps; an agentic tool has a context window plus whatever
you've made durable in files. And autocomplete has no permission
model at all, because it never touches anything outside your editor
buffer; an agentic tool has explicit trust boundaries, because it can
touch real files, run real commands, and reach real systems.

---

## Slide 19 — Failure Modes to Watch For
*~6 min*

Before you go run your own agent, I want to arm you with four things
to watch for, because you will very likely see at least one of these
in your lab trace today, and naming them now means you'll recognize
them instead of just feeling vaguely confused.

**Stuck retry loop**: the agent tries the same failing action again
with no new information driving the retry — a symptom that planning
has decoupled from observation. **Silent scope creep**: the agent
starts "fixing" things adjacent to the task that nobody asked it to
touch — sometimes helpful, often not, and always worth noticing.
**Context exhaustion mid-task**: partway through a longer task, the
agent's behavior shifts in a way that suggests it's lost track of the
original goal — this connects directly back to Slides 13–15. **Over-
trusting tool output**: the agent reads a "success" signal — a zero
exit code, a green checkmark — without checking whether that signal
actually means what it appears to mean.

We're naming these today so you have a vocabulary for what you
observe. We're not solving them today — that's deliberate. Module 5
starts building the habits that reduce scope creep and ambiguity at
the prompting level, and Module 12 is entirely dedicated to
verification discipline as a formal practice. Today, just notice and
log.

---

## Slide 20 — Lab: Trace an Agent
*~5 min, then hands-on*

Here's the lab. Pick a small, unfamiliar toy repository — something
you haven't worked in before, ideally small enough to hold in your
head, and simple enough that a single feature request is meaningful.
Give an agent exactly one task: something in the shape of "add a CLI
flag that does X." Keep the task small on purpose — this exercise is
about observing the loop clearly, not about testing the agent's limits
on a hard problem.

While it runs, log **every** tool call: every file read, every grep,
every edit, every test run — the full sequence, in order. And next to
each one, write one sentence: why do you think the agent did that? Use
the worked example from Slides 11 and 12 as your template — that
exact shape, applied to your own trace.

The goal of this lab is not to produce working code — the code being
correct is almost beside the point today. The goal is to actually
*see*, with your own eyes, on your own machine, the plan-act-observe
loop we've spent the last hour talking about. Abstract diagrams are
fine for building intuition, but there's no substitute for watching it
happen and having to explain, call by call, why.

---

## Slide 21 — Deliverable
*~3 min*

Two things to hand in. First, the annotated tool-call trace itself —
the table, in the shape of Slide 12, covering every single tool call
your agent made, not a curated subset. Second, a half-page writeup
answering two questions: where did the agent spend most of its
"effort" — reading and understanding the codebase, or actually writing
code? And did anything about the order of operations surprise you?

That second question is not a throwaway — pay attention to your own
reaction here. If something surprised you, that's usually a sign your
mental model of the loop and the agent's actual behavior diverged
somewhere, and that gap is exactly the kind of thing worth
articulating in a sentence or two. It's also useful preparation for
Module 5, where we start being deliberate about what information an
agent needs up front versus what it can reasonably discover itself.

---

## Slide 22 — Recap & Next Module
*~4 min*

Let's land the plane. Agentic means plan, act, observe, repeat — with
real verification built into the loop, not bolted on afterward.
Context windows are finite, and compaction is a necessary but lossy
way of coping with that limit — which is exactly why durable decisions
belong in files, not chat history. And permissions exist precisely
because the act-and-observe half of this loop touches the real world:
real files, real commands, real systems — not just a chat buffer.

Everything from here forward in the course builds on this loop. Next
we give that loop hands, memory and skills: Module 2 is MCP — safe access
to outside systems — then how an agent remembers you (Module 3), then
reusable procedures (Module 4). After that we return to precision in
prompts (Module 5): "precision in, precision out," and after today's
lab you'll have first-hand evidence of how much of an agent's work is
spent figuring out things you didn't tell it. See you in Module 2.
