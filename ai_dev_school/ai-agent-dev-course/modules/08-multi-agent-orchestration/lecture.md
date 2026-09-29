# Module 8 — Lecture Script: Multi-Agent Orchestration

This is the full spoken script for the live session, matched slide-by-slide
to `slides.md`. Timing notes are approximate and assume a ~90-minute lecture
block followed by a lab of roughly an hour to an hour and a half — long
enough for a real implementer/reviewer run against a nontrivial change,
which is what this module's lab asks for. Adjust to your cohort's pace;
the numbers are a planning aid, not a contract.

---

## Section 1 — Framing the Problem (Slides 1–4) — ~15 min

### Slide 1 — Module 8: Multi-Agent Orchestration

Welcome back. Last module was conversational, iterative development — tight
loops, no upfront doc, you steering an agent turn by turn. That works great
for small, exploratory things. Today we're doing something almost the
opposite: instead of one agent and one human in a loop, we're going to put
*more than one agent* on the same task, and we're going to be deliberate
about why.

The case-study focus for this module is the implementer, reviewer, and
orchestrator patterns — three concrete ways of composing agent roles that
show up constantly once you start building anything beyond a toy project
with these tools. By the end of today you won't just know the vocabulary;
you'll have run a real two-agent pipeline yourselves and looked at what it
actually caught.

### Slide 2 — Agenda

Here's the shape of the next couple of hours. We'll start with the
motivating problem — why a single agent reviewing its own work has a
structural weakness, not just an occasional lapse. Then we'll walk through
three patterns in turn: implementer/reviewer, orchestrator/worker
fan-out, and critic-executor loops. For each one I want you to come away
with three things: what it looks like, what specific failure mode it's
designed to catch, and what it costs you to run it. Then we'll zoom out and
talk about when parallelism is genuinely worth that cost and when it's
just overhead with extra steps. And we'll close by setting up today's lab,
which is where the real learning happens — you're going to build one of
these pipelines yourselves and see what a second, independent agent
catches (or doesn't) on something you actually built.

### Slide 3 — Objectives

Concretely, by the end of this module you should be able to do four
things. One: compose more than one agent role on a single task — not just
know that it's possible, but actually set it up. Two: explain the three
patterns we're covering today well enough to pick the right one for a
given situation, not just recite their names. Three — and this is the one
I actually care most about — judge when parallelism or specialization is
worth its overhead, and when it's just theater that makes you feel more
rigorous without actually catching more bugs. And four: run a real
implementer-then-reviewer pipeline and read its output with a critical
eye, rather than taking "looks good to me" from an agent at face value any
more than you'd take it from a human reviewer who skimmed a diff for ten
seconds.

### Slide 4 — The Blind Spot Problem

Let's start with why any of this is necessary in the first place. Here's a
claim: an agent reviewing its own work has a structural bias, not just a
chance of missing something. And the reason is almost embarrassingly
simple — it already knows what it *meant* to do.

Think about what happens when you ask an agent, in the same session where
it just wrote a diff, "does this look right to you?" It's going to re-read
its own code through the lens of the plan it just executed. If it decided
five minutes ago that empty input should return an empty list, and it
wrote code that does that, and you ask it to check its own work — of
course it says yes, that's correct, because it's checking "did I do what I
intended" not "does this actually satisfy the original ask." Those are two
different questions, and self-review conflates them.

This is not a new problem invented by AI agents, by the way — I want to be
clear about that, because it's tempting to treat it as some quirk of LLMs.
It's exactly why humans invented code review as an industry practice
decades before any of us were using coding agents. You don't review your
own pull request and call it done — not because you're careless, but
because you're the worst-positioned person in the room to see your own
blind spots, precisely because you know what you meant. The fix humans
settled on was organizational: get someone else's eyes on it, someone who
doesn't share your assumptions. That's the whole idea we're borrowing
today, just applied to agents: get a *second* agent's eyes on it, one that
doesn't share the first one's context or reasoning trail.

And that's the phrase I want you to leave this section with, because
you'll see it on the next few slides in a very literal, mechanical form:
"looks right" is the most dangerous sentence in software. It's dangerous
precisely because it's a report on your own expectations, not a
measurement of the actual artifact.

---

## Section 2 — Pattern 1: Implementer/Reviewer Split (Slides 5–7) — ~20 min

### Slide 5 — Pattern 1: Implementer/Reviewer Split

So here's the first and, honestly, most immediately useful pattern of the
three we'll cover: split the roles. One agent — call it Agent A —
implements the change. It gets full context: the task, the codebase, and
it builds up its own reasoning trail as it works, the same way any agent
session does across a nontrivial task.

Then a second agent, Agent B, reviews it. But — and this is the part
everyone gets wrong the first time they try it — B has to start in a
**fresh session**. Not a continuation of A's conversation. Not "and now,
acting as a reviewer, check what you just wrote." A brand new context
window, given exactly two things: the original task or spec, and the
resulting diff. Nothing else. No access to A's chat history, no access to
A's intermediate reasoning about why it chose one approach over another.

Why so strict about this? Because B's entire value proposition is finding
what A is structurally blind to. If B can see A's reasoning, B inherits
A's framing along with it — and inherited framing is exactly the blind
spot we're trying to eliminate. The job of B is not to restate what A
already believes about its own work. The job of B is to independently
re-derive "does this diff actually satisfy the task," starting from
nothing but the artifact and the ask.

### Slide 6 — Implementer/Reviewer — Diagram

Let's look at this as a picture, because the shape of the information flow
is the whole mechanism here. Task and spec go in at the top. Agent A, the
implementer, has full context — the codebase, its own reasoning trail as
it works through the problem. It produces a diff.

Now look at that line between A and B on the diagram. That's not a casual
detail — that line is the entire design of this pattern. Only the diff and
the original task cross it. A's reasoning does not cross that line. It's
worth drawing this literally as a wall when you picture it: on A's side of
the wall, there's a rich reasoning trail — "I considered handling this
with a null check but decided a default value was safer because..." — and
none of that reaches B. B just sees the code and the ask.

B then reviews — again, fresh session, no shared memory — and produces
either an approval or a request for changes. Only after that does anything
merge.

If you've done code review with humans, this should feel familiar in
spirit: a good reviewer doesn't ask the author to walk them through their
reasoning before looking at the diff, because then you're reviewing the
author's story about the code instead of the code. You look at the diff
cold, against the ticket, and you form your own opinion first. This
pattern just makes that discipline mechanical instead of optional.

### Slide 7 — Why "Fresh" Is the Whole Point

I want to spend real time on this slide because it's the single most
common way people half-implement this pattern and then wonder why the
"reviewer" agent never catches anything interesting.

Here's the failure mode: you take the same agent session that just wrote
the code, and you say, "Now switch hats — review what you just wrote as if
you were a critical reviewer." This does not work, or at least, it works
far less well than people hope. Why? Because the session still has all of
A's context sitting right there in its window. It knows why it made every
choice. Asking it to "be critical" doesn't erase that knowledge — it just
adds a thin layer of performed skepticism on top of the same underlying
framing. You'll get a review that finds a typo or a missing comment, and
misses the actual conceptual gap, because the conceptual gap is invisible
from inside A's own frame of reference.

Giving B *only* the diff and the task forces a genuinely different
computation. B has to ask "does this diff satisfy the ask," from scratch,
with no shortcut available of "did A follow the plan A described to me."
That's a meaningfully different question, and it's the one that actually
catches things — a missing edge case the spec implied but the code doesn't
handle, an assumption baked into the implementation that isn't stated
anywhere in the task.

The practical setup is genuinely simple, which is nice — it's not exotic
infrastructure. In something like Claude Code, this typically just means:
close out or don't reuse the implementer's session, and start a completely
new one for review, feeding it only the diff (`git diff` or the PR) and
the task description or spec file. If your tool supports spawning a
sub-agent or a separate agent role with an isolated context — some tools
call this a "subagent" or a background task — that's an equally valid way
to get the isolation; the mechanism matters less than the guarantee: zero
shared memory of the reasoning trail. Think of it the way you'd think
about hiring: you want "a new person reviewing this PR cold," not "the
same person, five minutes later, rereading their own work and calling it
review."

And I do want to be honest about the cost here, because we're going to
come back to cost/benefit later in the module: this is not free. B has to
do a full, real read of the diff and the spec every single time. That's
tokens and wall-clock time you weren't spending before. Keep that in your
back pocket — we'll weigh it properly in a bit.

---

## Section 3 — Pattern 2: Orchestrator/Worker Fan-Out (Slides 8–10) — ~20 min

### Slide 8 — Pattern 2: Orchestrator/Worker Fan-Out

Pattern two solves a completely different problem. Implementer/reviewer is
about *quality* — catching what a single pass misses. Orchestrator/worker
is about *scale* — getting through more work by doing pieces of it at the
same time instead of one after another.

The shape: one coordinating agent, the orchestrator, looks at a large task
and breaks it into pieces that are — and this word is doing all the work
in this sentence — **independent**. Each piece goes to its own worker
agent, with its own context window and its own tool calls, working on its
slice without needing to know what the other workers are doing moment to
moment. When the workers finish, the orchestrator collects everything and
integrates it back into one coherent result.

This is the pattern people reach for instinctively when they think
"multi-agent" — it feels like the obvious productivity play, parallel
instead of serial, more agents means more throughput. And sometimes
that's exactly right. But the entire pattern lives or dies on that one
word: independent. If the sub-tasks aren't genuinely independent, fan-out
doesn't save you time, it just moves the coordination problem to later,
where it's more expensive to fix.

### Slide 9 — Orchestrator/Worker — Diagram

Picture a concrete example: you need to migrate three independent modules
in a codebase off a deprecated API to its replacement — say, module 1,
module 2, module 3, and critically, nothing in module 1's migration
depends on any decision made while migrating module 2. The orchestrator
looks at the overall task, confirms that split is real, and dispatches
three workers, one per module, in parallel. Worker A migrates module 1,
worker B migrates module 2, worker C migrates module 3 — each running its
own read-edit-test loop independently, the same core agentic loop from
Module 1, just three copies of it running at once on disjoint pieces of
the codebase.

Once all three report back, the orchestrator doesn't just concatenate the
three diffs and call it done — it runs an integration pass: does
everything still build together, did any of the three workers make an
assumption that turns out to conflict with what another one did, is
there a shared test suite that needs all three changes present to pass.

Notice this diagram looks structurally like a tree — one coordinator,
several independent branches, then a merge back to one trunk. That shape
is the tell for when this pattern is a good fit: your task should
naturally decompose into a tree like this. If you're staring at your task
and the "independent" branches keep needing to talk to each other, that's
a sign this isn't actually a fan-out-shaped problem.

### Slide 10 — The Hard Part Is Integration

Here's the thing nobody tells you when they're excited about parallel
agents: dispatching the work is the easy 20%. Integrating it safely is the
hard 80%, and it's the part that's easy to underestimate because it
doesn't show up until after all your workers report "done."

Three specific ways this bites you. First: two workers touching the same
shared file or interface differently. Say module 1 and module 2 both need
to call a shared utility function, and worker A decides — reasonably, in
isolation — to add an optional parameter to that shared function to
support its use case, while worker B, also reasonably, in isolation,
decides the cleanest fix is a different overload. Individually each
change looks fine. Together, you have two different agents' opinions
baked into one shared interface, and somebody — ideally the orchestrator,
during integration, not you discovering it in CI three days later — has
to reconcile that.

Second: a shared assumption that was true when the orchestrator planned
the split, but turns out false for one worker's slice once that worker
actually gets into the code. Maybe the orchestrator assumed all three
modules used the same internal data shape, and it turns out module 3 has
a legacy variant that doesn't. Worker C either has to notice and flag
that the assumption behind its own assignment was wrong, or it silently
does something slightly different to cope — and if it does the latter
without flagging it, that inconsistency is now baked into the result and
invisible until integration, or worse, until production.

Third, and this one is subtle: workers silently disagreeing on a
convention — variable naming, error-response shape, logging format —
purely because neither one saw what the other produced. No individual
worker did anything wrong. But you now have three inconsistent local
conventions where you wanted one.

The takeaway I want you to walk away with: the orchestrator's real job
isn't the splitting. Splitting a task that's genuinely decomposable is
almost mechanical. The orchestrator's real job — the part that actually
requires judgment and can't be skipped — is the integration pass at the
end. If you set up an orchestrator/worker pipeline and skip a deliberate
integration step, you haven't saved time, you've just deferred finding
out about the coordination cost to a worse moment.

---

## Section 4 — Pattern 3: Critic-Executor Loops (Slides 11–13) — ~15 min

### Slide 11 — Pattern 3: Critic-Executor Loops

Third pattern, and it solves yet another different problem. This one
isn't about catching blind spots in a finished piece of work, and it isn't
about doing more work in parallel — it's about converging on a good result
through iteration, without needing a human to sign off on every single
round of that iteration.

The shape: an executor agent produces an attempt at the task. A separate
critic agent evaluates that attempt against a set of criteria. If it
falls short, the executor revises based on the critique. This loops —
attempt, critique, revise, re-critique — and crucially, a human is not in
the loop approving each round. The human's job happens up front: setting
the criteria the critic checks against, and setting a stopping condition
so this doesn't run forever.

How is this different from implementer/reviewer, which also has two
roles? Good question, and it's worth being precise about it, because on
the surface they look similar — two agents, one making, one judging.
The difference is in shape and purpose. Implementer/reviewer is
sequential and terminal: one implementation pass, one review gate, then a
merge decision — done. Critic-executor is iterative and internal to the
task: the same task gets attempted, critiqued, and reattempted multiple
times, converging toward something that satisfies the criteria, and only
the final converged result is what a human (or a downstream
implementer/reviewer pipeline!) ever sees. You could, in principle, run a
critic-executor loop *and then* pass the converged result through an
implementer/reviewer gate before merge — they're not mutually exclusive,
they're solving different problems at different stages.

### Slide 12 — Critic-Executor — Diagram

Picture the loop: executor produces an attempt, hands it to the critic.
The critic evaluates it and, if it's not good enough, sends back a
critique — specific, ideally: not "this isn't great" but "this doesn't
handle the case where the input list is empty," something the executor
can actually act on. The executor revises based on that specific
critique, and the cycle repeats. This continues until one of two things
happens: the critic accepts the result, or you hit a round limit you
defined ahead of time.

A concrete example, since this is easiest to picture with something
mechanical: you ask an agent to generate a database migration script.
Executor produces a first attempt. Critic checks it against the
acceptance criteria you defined — does it handle a rollback path, does it
avoid locking the whole table during migration on a large dataset, does
it match the schema conventions used elsewhere in the codebase. Say the
critic finds it's missing a rollback path. That's a specific, actionable
critique. Executor patches the script to add one. Critic re-checks — this
time it passes. Loop ends, converged result comes out the other end,
having gone through two rounds without you needing to look at either
intermediate draft.

### Slide 13 — Stopping Conditions Matter

Here's the part of this pattern that bites people who set it up
carelessly: without an explicit limit, these loops can go wrong in two
different ways, and they're worth naming separately because they look
different in practice.

One failure mode is oscillation — executor fixes issue A but in doing so
reintroduces issue B, which the critic then flags, so the executor fixes B
but reintroduces A, and you're stuck bouncing between two states forever,
burning rounds without ever converging.

The other failure mode is more insidious: rubber-stamping. If your critic
isn't checking against something concrete, it can start agreeing with
whatever it's shown, especially after a round or two — "looks fine now" —
without there having been a real improvement. This is the same underlying
disease as the self-review blind spot from Slide 4, just showing up
inside an automated loop instead of inside one agent's own head: a vague
evaluation standard degrades into agreement rather than judgment.

So, three things to set up before you ever start the loop, not after you
notice it's misbehaving. A max round count — three revisions, say, and
then it escalates to a human rather than continuing indefinitely. Concrete
acceptance criteria for the critic to check against — the migration
example's list a moment ago is the model: specific, checkable conditions,
not "does this look good," which is exactly the kind of vague standard
that invites rubber-stamping. And a defined behavior for non-convergence —
if you hit the round limit without the critic accepting, the system
should stop and surface that to a human with the history of attempts, not
either loop forever or silently accept the last attempt anyway.

---

## Section 5 — Comparing, and the Cost/Benefit Question (Slides 14–18) — ~20 min

### Slide 14 — Comparing the Three Patterns

Let's put all three side by side, because in practice the hardest part
isn't understanding any one of these patterns individually, it's picking
the right one for the situation in front of you.

Implementer/reviewer is sequential, with a single gate — it's built for
exactly one moment: a quality check right before something merges. Use it
when you have one finished piece of work and you want an independent
check on it before it becomes permanent.

Orchestrator/worker is a parallel fan-out — it's built for scale on tasks
that decompose into genuinely independent pieces. Use it when the
bottleneck is throughput on a large but separable task, not correctness
risk on a single tricky piece of logic.

Critic-executor is an iterative loop — it's built for converging on
something that meets a bar, without a human re-checking every draft along
the way. Use it when you can state your acceptance criteria concretely
enough for an agent to check them, and you'd rather bound the iteration
automatically than watch every round yourself.

Notice the common thread underneath all three, though: every single one
of them is spending extra tokens and extra time to buy you a structural
guarantee that a single agent, single pass, cannot give you by
construction. That's not a coincidence — it's the actual mechanism by
which all three of these patterns work, and it's exactly why the next few
slides matter as much as the patterns themselves.

### Slide 15 — When Parallelism Helps

Let's get concrete about when reaching for one of these patterns —
especially the fan-out one, since that's the one people over-apply most
often — is actually the right call.

First signal: the sub-tasks are genuinely independent. Different files,
different modules, and critically, no shared decision that has to be made
consistently across all of them. Second: the task is large enough that
serial execution time is your actual bottleneck — you have real work that
would otherwise queue up one piece after another, not a task where the
risk is getting any one piece wrong. Third: each worker's output can be
verified in isolation, on its own, before you ever get to integration —
if you can't check a piece is right without also having every other
piece in hand, that's a warning sign the pieces weren't as independent as
you thought.

The clean example: applying the same mechanical refactor — a rename, an
API migration, a lint-rule fix — across N independent modules that don't
share internal decisions. That's about as textbook a fan-out case as
you'll find: the work is repetitive, the pieces genuinely don't need to
coordinate, and you can check each module's result on its own.

### Slide 16 — When Parallelism Hurts

Now the flip side, and I'd argue this slide is more important than the
last one, because the failure mode of over-applying multi-agent patterns
is far more common in practice than under-applying them — it's the
exciting new toy, so people reach for it past the point it's earning its
keep.

Parallelism hurts when the sub-tasks share a decision that has to stay
consistent across all of them — a schema, a naming convention, an
interface contract. If workers each have to independently arrive at the
same answer to a shared design question, you haven't actually
parallelized the hard part; you've just guaranteed three independent
agents will each guess, and probably guess differently.

It also hurts when the split itself is the genuinely hard part of the
problem. If you're spending more effort figuring out how to divide the
task cleanly than the task would take to just do, fan-out isn't saving
you anything — you've front-loaded a design problem and called it
orchestration.

And here's the point that matters most for the smaller, everyday case,
not just the big dramatic refactor: on small tasks, a second agent pass —
whether that's a reviewer or a critic or a parallel worker — very often
costs more, in tokens and time and your own attention reading its output,
than the bug it might occasionally catch is worth. Adding a reviewer
agent to a two-line typo fix is not rigor, it's waste with extra ceremony.

### Slide 17 — A Cost/Benefit Heuristic

So how do you actually decide, in the moment, whether to reach for one of
these patterns? Here's a concrete heuristic — three questions, in order,
before you add any extra agent role to a task.

One: what specific blind spot does this extra pass address? Not "more
checking is generally good" — name the actual failure mode you're
worried about. Is it "the implementer won't notice its own missed edge
case"? Is it "this task is big enough that serial execution is genuinely
the bottleneck"? Is it "I want to converge on a spec without babysitting
every draft"? If you can't name a specific blind spot, you probably don't
need the extra pass yet.

Two: what's the actual cost? And be honest about all of it — not just
the extra tokens and wall-clock time the second (or third) agent burns,
but also the time *you* spend reading and judging its output. A review
agent that produces ten paragraphs of commentary you have to wade through
has a real cost even if the extra tokens themselves are cheap.

Three: is this change high-stakes enough that an independent check is
worth that cost? A security-sensitive change touching auth logic:
probably yes. A one-line config tweak: almost certainly no.

The rule of thumb falling out of this: reserve multi-agent setups for
changes where the answer to question three is genuinely yes, not for
everything, by default, because it feels more thorough. And I'll flag
now — we're going to go much deeper on what "worth it" means in concrete,
measurable terms next module, in Module 9 on verification and review.
Today, hold onto the heuristic; next time we'll sharpen it into something
closer to a decision procedure.

### Slide 18 — Failure Modes to Watch For

Before we get to the lab, four specific ways multi-agent setups fail that
are worth naming explicitly, because each one looks superficially like
success if you're not watching for it.

Rubber-stamping: the reviewer or critic agent just agrees with what it's
shown, adding no independent signal at all, while looking, on the surface,
exactly like a review that happened. You'll see this especially if your
review prompt is vague — "check this over" invites agreement in a way
that "verify these five specific acceptance criteria" doesn't.

Shared blind spot: both agents were trained on similar patterns and data,
so they miss the same thing for the same underlying reason. Independence
of *session* — fresh context, no shared chat history — does not
automatically buy you independence of *judgment*. Two agents can fail to
notice the same subtle bug for the exact same reason a single agent
would, if that reason is baked into how the model reasons rather than
into what it happened to see in one particular conversation.

Integration blindness: in orchestrator/worker setups specifically, the
orchestrator approves individual pieces that each look fine on their own
but don't actually fit together — this is Slide 10's integration problem
showing up as a failure rather than a risk you managed.

And cost creep: "let's just add a reviewer agent" quietly becomes
routine, applied everywhere, and you end up paying triple the tokens for
marginal extra catches on changes that never needed the extra pass in the
first place.

The thread running through all four: a multi-agent setup is only as good
as the independence it actually achieves. Independence isn't automatic
just because you technically used two separate agent invocations — you
have to design for it, the way we did explicitly back on Slide 7 with the
fresh-session requirement.

---

## Section 6 — Lab Setup and Wrap (Slides 19–21) — ~10 min, then into the lab

### Slide 19 — Lab: Two-Agent Pipeline

Here's what you're building for the rest of this session. Pick a
nontrivial change in your working repo — and I want to be specific about
what "nontrivial" means here, because this lab teaches you nothing if you
pick a one-liner. You want something with a real edge case buried in it,
or a design decision that isn't fully spelled out — the kind of change
where a careful human reviewer might actually find something, not a
typo fix where there's structurally nothing to find.

Step one: Agent A implements it, with full task context — same as any
normal agent session you've run in previous modules.

Step two, and this is the step to get right: start Agent B completely
fresh. Not a continuation. A new session, new context window, and you
give it exactly two things — the original task description, and the
resulting diff. Resist the temptation to also hand it A's notes or
reasoning "just so it has more context" — that's exactly the shortcut
that breaks the pattern, per Slide 7.

Step three: B reviews and reports its findings before anything merges.

The goal here isn't to prove that multi-agent review always finds
something dramatic — the goal is to honestly observe whether independent
review catches something the implementer missed on *this specific
change*, or whether it confirms there was nothing to catch. Both are real
results. Go in without a thumb on the scale either way.

### Slide 20 — Deliverable

What you're handing in: the full pipeline transcript, both agents, not
just a summary — I want to see A's implementation session and B's review
session as they actually happened. Alongside that, a list of any issues
Agent B caught that Agent A missed.

And — this is worth saying plainly, because I don't want anyone to feel
like they failed the lab if this happens — if B genuinely caught nothing
new, write that down honestly instead of stretching to find something to
report. That null result is not a failure of the exercise. It's data. It
tells you something real about this specific change: maybe it was
simple enough that a second pass wasn't buying you anything, which is
itself exactly the kind of judgment call Slide 17's heuristic is asking
you to make in the future. A false "B found three things!" when it really
just restated what A already knew would be a worse deliverable than an
honest "nothing new — and here's why I think that particular change
didn't need it."

### Slide 21 — Recap & Next Module

Let's pull the thread back together before you head into the lab. Three
patterns today. Implementer/reviewer: fresh eyes catch what "I know what
I meant" structurally hides from the agent that wrote the code —
independence of context is the entire mechanism, not an incidental
detail. Orchestrator/worker: fan-out earns its keep on genuinely
independent work, but the real work you can't skip is the integration
pass at the end, not the splitting at the start. Critic-executor: you can
iterate toward a spec without a human approving every round, as long as
you bound the loop with concrete criteria and a round limit up front.

And running underneath all three, the point I want you to carry into
every future module where you're tempted to add another agent to a
pipeline: none of this is free. Every extra pass costs tokens, time, and
your own attention reading the output. Spend that cost deliberately, on
changes where an independent check is actually worth it — not as a
default habit because it feels more rigorous.

Next module, Module 9, is Verification and Review — trust but verify. If
today was about *when* and *how* to add a second agent's judgment, next
time is about what verification and review actually mean in concrete,
checkable terms: hallucinated APIs, silent scope creep, security review
for AI-written code, and prompt-injection risk when an agent reads
untrusted content. A lot of what makes today's reviewer or critic agent
actually good at its job comes from ideas we'll formalize next time — so
hold onto your Agent B transcript from today's lab; we may come back to
it.

Go build your pipeline. See you with your transcripts.
