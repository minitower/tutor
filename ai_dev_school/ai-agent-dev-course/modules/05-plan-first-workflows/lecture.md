# Module 5 — Plan-First Workflows
## Lecture Script

This script is written as spoken narration. It follows `slides.md` slide by
slide — same numbers, same titles. Timing notes assume a ~70–90 minute
lecture followed by a hands-on lab (Slides 19–21), for a combined session of
roughly 2–2.5 hours.

---

## Slide 1 — Module 5 / Plan-First Workflows

**(~3 min)**

Welcome back. We're now in Module 5, and the theme is "Plan-First
Workflows." The case study we'll build around is ephemeral plans plus
approval gates — that phrase is going to make a lot more sense in about ten
minutes, so hold onto it.

Here's the one-sentence version of what this module is about: before you
let an agent touch a single file, you make it tell you *how* it intends to
do the work, and you don't let it start until you've said "yes, that's the
right approach." That's it. That's the whole idea. What we're going to
spend the next hour and a half doing is understanding exactly when that
matters, when it's overkill, what a *good* plan actually contains, and how
this connects to something you already know from Module 3 — Document-Driven
Development.

If Module 3 was about agreeing on *what* to build before anyone writes
code, Module 5 is about agreeing on *how* to build it before anyone writes
code. Same instinct — agree before you commit — pointed at a different
question. Keep that distinction in your head; we're going to come back to
it explicitly on Slide 4 and again on Slide 16.

---

## Slide 2 — Agenda

**(~2 min)**

Quick tour of where we're headed today. We'll start by placing plan-first
on the methodology map relative to what you already know — that's the
recap on Slide 4. Then we get into the actual mechanics of plan mode and
approval gates: what they are, what a real gate looks like versus a fake
one. From there we'll do a full worked example, start to finish — a
realistic refactor task, the plan an agent produces for it, a reviewer
pushing back on one part of that plan, and the agent revising before
execution starts. That worked example is the spine of the lecture; almost
everything else hangs off it.

After that we turn to ADRs — Architecture Decision Records — and how they
feed *into* an agent's planning process, which is a nice complement to the
ephemeral nature of plans. Then a direct side-by-side of plan-first versus
DDD, so you leave here able to say, out loud, in one sentence, when you'd
reach for one over the other. And finally the lab: you're going to run this
exact workflow yourselves on a refactor in your own sample repo, and there's
a concrete deliverable at the end.

---

## Slide 3 — Learning objectives

**(~3 min)**

Four things you should walk out of this session able to do.

First: separate planning from execution as two genuinely distinct phases,
so that the *scope* of a change — which files, what kind of changes, what's
explicitly off-limits — is agreed before any code changes happen. Not
"roughly agreed," not "implied by the ticket." Explicitly written down and
signed off.

Second: recognize when the risk in a task lives in the *approach* rather
than in the *requirements*. This is the diagnostic skill that tells you
when plan-first is the right tool at all. If nobody's confused about what
"done" looks like, but there are three plausible ways to get there and they
have different blast radii — that's a plan-first situation.

Third: use an approval gate as an actual checkpoint. Not a formality you
click through. We're going to look at what a rubber-stamp approval looks
like versus a real one, because in practice, most failures of this
methodology aren't failures of process design — they're failures of someone
approving a plan they didn't actually read.

Fourth, and this one matters for your own judgment as engineers: know when
plan-first is *overkill*. This methodology has a cost — writing a plan,
reading a plan, iterating on a plan all take time. If the change is small
and reversible, that cost isn't worth paying. We'll give you a concrete
rule of thumb for this on Slide 18.

---

## Slide 4 — Quick recap: Module 3 sets up the contrast

**(~5 min)**

Let's ground this in what you already know. In Module 3 we covered
Document-Driven Development — DDD. The core artifact there was the spec: a
durable document, written by a human, up front, before the agent starts
working, and it answers the question "what should this do?"

Plan-first workflows have a parallel structure, but every cell in this
table is different. The artifact is a plan, not a spec. Its lifespan is
ephemeral — you use it once, for one task, and then it's gone, versus a
spec which sticks around and gets referenced again and again. It's authored
by the agent, per task, rather than by a human up front. And critically, it
answers a different question: not "what should this do," but "how will we
get there."

I want to be precise about why this distinction matters practically, not
just academically. If you're doing DDD and the agent starts overengineering
or misunderstanding scope, the fix is: go back and clarify the spec — the
requirements were ambiguous. If you're doing plan-first and the agent picks
a risky approach, the fix is completely different: you don't touch
requirements at all, because the requirements were never in question. You
push back on the *plan* — the sequencing, the files touched, the
mechanism. Same discipline underneath — agree before code — but you're
negotiating over a different object, and if you don't know which one you're
negotiating over, you'll waste review cycles arguing about the wrong thing.

That's the whole recap. Same discipline, different object of agreement.
Let's define plan-first properly now.

---

## Slide 5 — What is a "plan-first" workflow?

**(~5 min)**

Mechanically, a plan-first workflow has three steps.

One: the agent proposes an explicit plan. Not a vague intention — an actual
artifact you can read, containing the files it plans to touch, the changes
it plans to make in each one, the sequence those changes happen in, and the
reasoning behind the choices it made.

Two: a human, or in more mature setups a reviewer agent, looks at that plan
and does one of three things — approves it as-is, amends it (asks for
changes, the agent revises, you look again), or rejects it outright and
sends the agent back to rethink the approach entirely.

Three — and this is the part that's easy to skip if you're not deliberate
about it — execution starts *only* after approval. Not "usually after."
Only after.

Here's the detail that I think is most underappreciated about this: at the
point where you're reviewing the plan, there is no code yet. No diff to
look at. No tests to run. You are reviewing a *description* of what's about
to happen, before it happens. That's a fundamentally different review
activity than code review, and it requires a different kind of attention —
you're evaluating intent and approach, not correctness of implementation.
We'll unpack what "good" looks like for that kind of review in a few
slides.

---

## Slide 6 — Plan mode / approval gates — the mechanic

**(~7 min)**

Let's get concrete about the mechanism, because "plan mode" is a specific
feature you'll actually use, not just a concept.

The core move is splitting what would otherwise be one continuous agentic
loop into two distinct turns: a "propose" turn and an "act" turn. Normally
an agent might read some files, decide on an approach, and immediately
start editing, all in one uninterrupted pass. Plan-first workflows
deliberately insert a hard stop between deciding and doing.

Concretely, in Claude Code, this is what plan mode is for. When you invoke
plan mode, the agent is restricted to read-only exploration — it can read
files, search the codebase, run read-only commands to understand context —
but it cannot make edits. Its output for that turn is a plan: a structured
description of what it intends to do. It literally cannot start editing
until you exit plan mode and approve.

Now, the approval gate itself. An approval gate is a checkpoint where a
human — or, again, a reviewer agent standing in for a human — has to
explicitly say "go." Not implicitly. Not by doing nothing. Explicitly.

And here's the sentence I want you to remember from this whole slide:
silence is not approval. If a plan sits in a chat window for thirty seconds
and then the agent starts executing because nobody objected, that is not an
approval gate — that's a agent with a suggestion box nobody's required to
read. An unread plan is not a reviewed plan, no matter how official the
pause before execution looked. The gate only does its job if a human
actually reads what's on the other side of it and makes a decision.

---

## Slide 7 — Anatomy of a good plan

**(~6 min)**

So what does a plan actually need to contain for that review to be
possible? Four things.

First: the files it intends to touch, and *why*, for each one — not a bare
file list, but a file list with a reason attached to every entry. "I'm
touching `checkout.ts` because it has a local copy of `formatCurrency` that
needs to import from the new shared module instead." That's a reviewable
statement. "Update the relevant files" is not — we'll come back to that
exact phrase in a few slides as an example of what *not* to accept.

Second: sequencing — what depends on what. If step 3 can't happen before
step 1 is done, the plan should say so, both because it helps you catch
ordering mistakes and because it tells you where the natural checkpoints
are if something needs to pause partway through.

Third: explicit call-outs of open questions or risky spots. This is the
single highest-value ingredient in a good plan, and it's the one that
agents will skip if you don't insist on it, because flagging "I'm not sure
about this" requires the agent to have actually noticed the ambiguity
rather than just plowing through it. We're going to see exactly this
happen in the worked example — a rounding behavior that's genuinely
ambiguous, and a good plan surfaces it instead of guessing.

Fourth: non-goals — what the plan will deliberately *not* touch. This is
the flip side of the file list. It's just as important to say "I am not
touching this legacy module, that's a separate concern" as it is to say
what you *are* touching, because it tells the reviewer the agent
understood the boundaries of the task, rather than just happening not to
have reached that file yet.

Here's the rule I'd leave you with: a plan missing any of these four things
is a plan you haven't finished reviewing. If you read a plan and can't
point to where it addresses sequencing, or where it flags its risky
assumptions, that's not a green flag — that's a sign you need to ask for
more detail before you approve anything.

---

## Slide 8 — Worked example — the task

**(~5 min)**

Let's make all of this concrete with a full example we'll carry through
several slides.

The task: extract the `formatCurrency` logic, which is currently duplicated
across three modules — `invoice.ts`, `checkout.ts`, and `reports.ts` — into
a single shared `lib/format.ts`.

Notice something about this task already: the *requirement* is completely
unambiguous. Nobody needs to argue about what "done" looks like — there
should be one canonical `formatCurrency` function, three call sites should
use it, and the duplication should go away. This is exactly the profile we
described in the learning objectives: requirements clear, risk lives
elsewhere.

Where does the risk actually live? In the *approach*. If you just tell an
agent "consolidate this duplicated logic" and let it run unsupervised, here
are three ways that goes wrong. It could touch the three call sites
inconsistently — update two of them cleanly and leave the third in some
half-migrated state. It could rename the export as part of "cleaning up,"
breaking anything else that imports the old name. Or — and this is the one
that's genuinely dangerous because it's silent — it could quietly change
rounding behavior while unifying the three copies, because the three
existing copies might not actually be identical.

That last one is not hypothetical for this example. Let's see the plan the
agent actually produces and whether it catches it.

---

## Slide 9 — Worked example — the agent's plan

**(~7 min)**

Here's the plan, and I want to walk through it line by line against the
anatomy checklist from Slide 7, because this is a genuinely well-formed
plan and it's worth seeing why.

Step one: create `lib/format.ts`, move `formatCurrency()` there unchanged —
and notice the parenthetical: byte-for-byte, no behavior change in this
step. That's a plan being explicit about isolating a pure "move" from any
"change," which is exactly the kind of thing that makes a diff easy to
review later — if something breaks, you know it's not from this step.

Steps two and three: update `invoice.ts` and `checkout.ts` to import from
the new shared location and remove their local copies. Straightforward,
mechanical, matches the task.

Step four is where this plan earns its keep. Update `reports.ts` — same
pattern as the others — but then a note: reports.ts's copy rounds to zero
decimals for summary rows, and the plan explicitly says "confirm before
removing whether that's a bug or intentional." This is exactly the
call-out-risky-spots item from the anatomy checklist, and it's exactly the
danger we described on the previous slide. The agent noticed the three
copies aren't actually identical, and instead of picking one behavior and
hoping, it flagged the discrepancy for a human to resolve.

Step five: will *not* touch `billing/invoice-legacy.ts`, because it's
deprecated and tracked under a separate ticket. That's the non-goals item —
an explicit statement of what's out of scope and why, which tells you the
agent understood the boundary rather than just not having gotten to that
file yet.

So: files and reasons, check. Sequencing — move first, then update callers
one by one — check. Risky spot flagged instead of silently resolved,
check. Non-goal stated, check. This plan hits all four items from Slide 7.
Now let's watch the approval gate actually function.

---

## Slide 10 — Approval gate in action

**(~6 min)**

This is what a real approval gate looks like in practice — not a rubber
stamp, an actual back-and-forth.

The reviewer reads the plan and responds to exactly one point: "Point 4 —
don't guess. Check with the reports owner about the zero-decimal rounding
before merging behavior." Notice what the reviewer is *not* doing here.
They're not rewriting the plan themselves. They're not saying "looks
good." They're identifying the one place where the plan's proposed
resolution — which, to be fair, was already "confirm before removing" —
still leaves room for the agent to guess if nobody answers in time. The
reviewer tightens that.

The agent amends the plan. Step four now proposes something more
conservative than "ask and then unify": preserve the zero-decimal rounding
as a documented parameter rather than silently unifying the behavior across
all three call sites. That's a meaningfully different implementation — it
means `reports.ts` will call the shared function with an explicit
`precision` argument instead of everyone converging on one implicit
default, and that difference is now visible in the code rather than buried
in institutional memory.

Then: re-approved, execution begins. I want to emphasize the shape of this
exchange, because it's the whole point of the mechanic. One round of
feedback, targeted at a specific point, produced a concrete change in the
plan, and only then did any code get touched. If this had been "approved"
on the first pass, that rounding ambiguity would have been resolved by
whatever the agent happened to guess — probably reasonably, but silently,
and you'd have found out about it (if ever) much later, in production,
looking at a report total that's suddenly off by a few cents.

---

## Slide 11 — What the approval gate is actually for

**(~5 min)**

Let's zoom out from the example and generalize what this checkpoint buys
you. Four things.

Catching scope creep *before* it's code. It is dramatically cheaper to
strike a file off a plan than to revert a change to it. Reviewing a
sentence costs seconds; reviewing and reverting a diff costs the rest of
your afternoon.

Catching duplicated or conflicting logic getting silently merged. This is
exactly our rounding example — three implementations that look similar but
aren't identical, and an agent that's optimizing for "reduce duplication"
has every incentive to just pick one and move on unless something makes it
stop and ask.

Confirming that risky files are touched only when truly necessary. Some
files in every codebase are landmines — legacy code, files with subtle
cross-team dependencies, anything touching billing or auth. A plan lets you
say "no, don't touch that" before the agent has any reason to have opened
it.

And this last point is important enough that I want to say it as clearly
as I can: an approval gate is **not** a substitute for reviewing the diff
afterward. Approving the plan tells you the *intended* approach is sound.
It tells you nothing about whether the *execution* actually matched the
plan, or whether some detail went sideways along the way. You still review
the diff. Plan-first adds a review step; it does not remove one.

---

## Slide 12 — Common plan failure modes

**(~6 min)**

Let's talk about how this goes wrong in practice, because it does go wrong,
and it goes wrong in predictable ways.

Too vague. "Update the relevant files." I flagged this phrase back on
Slide 7 and I'm calling it out again here deliberately, because it's the
single most common failure mode you'll see. That sentence is not a plan.
It's a promise to produce a plan later, dressed up as if the work of
planning had already happened. If you see something like this, the correct
response is not to approve it and hope — it's to send it back and ask
"which files, specifically, and why."

Silent scope creep. A plan that omits a file it will actually end up
touching. This is insidious because it's not something you can catch by
reading the plan harder — by definition, the plan doesn't mention it. The
defense here is mostly on the back end: this is exactly why you still
review the diff afterward, per the previous slide, and why the lab you'll
do today explicitly asks you to note any divergence between plan and
execution.

Rubber-stamp approval. Clicking "approve" without actually reading step
four. We built the entire worked example around a case where step four was
the one part of the plan that actually mattered — if a reviewer skims past
it, the whole value of the gate evaporates. The gate is only as good as the
attention applied to it.

Undocumented drift. Execution departs from the plan partway through, and
nobody notes why. Sometimes deviation is legitimate — the agent discovers
something mid-execution that changes the picture — but if that happens
silently, you've lost the entire audit trail this methodology exists to
create. If the plan changes mid-flight, that change needs to be visible,
the same way the Slide 10 amendment was visible before execution started.

---

## Slide 13 — ADRs — Architecture Decision Records

**(~6 min)**

Let's shift gears slightly and talk about a companion artifact: the
Architecture Decision Record, or ADR.

An ADR is a durable document — note the contrast with the plan we've spent
this whole lecture on, which is ephemeral — and it captures exactly *one*
decision: the context that led to it, the alternatives that were
considered, and the consequences of having made it.

Here's a concrete one, and notice it's the natural next artifact after our
worked example. ADR-0007: "Centralize currency formatting in
`lib/format.ts`." Status: accepted. Context: three divergent copies of
`formatCurrency`, one of which had a silent rounding difference discovered
during this exact refactor. Decision: one canonical implementation, and
callers pass a `precision` parameter instead of hand-rolling their own
rounding. Consequences: reports' zero-decimal behavior is now explicit
in the code, not an implicit accident of a copy-pasted implementation.

Read that context line again: "discovered during Module 5's refactor."
That's not incidental — that's the entire connective tissue between plans
and ADRs. The plan caught a real discrepancy during a task. The ADR is
where that discovery gets written down permanently, so it isn't
rediscovered — or worse, silently overwritten — the next time someone
touches this code.

---

## Slide 14 — ADRs as agent input

**(~6 min)**

Now, why does this matter specifically for *agent* workflows, as opposed
to just being generally good practice for any engineering team?

Here's the problem ADRs solve: plans are ephemeral. We've said that
several times now — a plan gets thrown away after the task is done. That's
fine for the plan itself, but it creates a real risk: without a durable
record of *why* a decision was made, the *next* plan — written by an agent
with no memory of this conversation — re-litigates the exact same
tradeoff. Some future agent, asked to touch currency formatting again, has
no way of knowing the rounding question was already resolved, unless
something durable tells it.

The fix is straightforward, mechanically: point the agent at a directory of
ADRs — conventionally `docs/adr/` — and make sure that location is
referenced from `CLAUDE.md` or `AGENTS.md`, whichever your project uses, so
that it's part of what the agent reads *before* it starts planning, not
something it has to stumble onto.

The payoff: with ADR-0007 sitting in `docs/adr/` and referenced from
`CLAUDE.md`, a future refactor's plan doesn't start from scratch
rediscovering the rounding bug. It starts from "use `lib/format.ts`" as a
given, because the decision is already recorded. The agent's *plan* is
ephemeral every single time; the *decision* it's built on doesn't have to
be. That's the relationship — ephemeral plans, informed by durable
decisions.

---

## Slide 15 — Plan vs. ADR — ephemeral vs. durable

**(~5 min)**

Let's make that relationship completely explicit with a direct comparison,
because it's easy to blur these two artifacts together since they can both
originate from the same piece of work.

Scope: a plan covers one task. An ADR covers one decision. Those aren't
the same unit — a single task might touch on a decision that was already
made in an earlier ADR, and a single ADR might inform many future tasks'
plans.

Lifespan: a plan is thrown away after merge — once the code lands, the
plan has done its job and there's no reason to keep it around. An ADR is
kept and referenced later, specifically because its whole value is being
available the next time someone needs it.

What each one answers: a plan answers "files plus sequence for *this*
change" — it's operational, specific, disposable. An ADR answers "why this
approach, generally" — it's the reasoning that outlives the specific
instance that prompted it.

Here's the analogy I want you to hold onto: a plan is one flight's flight
plan — routing, altitude, fuel, specific to this one trip, filed and
forgotten once the plane lands. An ADR is the airline's route policy — the
durable reasoning about why certain routes are flown certain ways, that
every future flight plan gets written against. Different documents,
different lifespans, and you shouldn't try to make one do the other's job.

---

## Slide 16 — Plan-first vs. DDD, side by side

**(~6 min)**

Let's now return to the comparison we opened with on Slide 4, but fully
fleshed out, because by this point you have enough vocabulary to make it
precise.

Durability: DDD's spec, yes — it's kept. Plan-first's plan, no — it's
ephemeral, thrown away after the task.

Authorship: DDD's spec is written by a human, up front, before the agent
sees the task at all. Plan-first's plan is proposed *by the agent*, with a
human approving — the authorship direction is essentially reversed.

And this is the row that matters most for deciding which methodology to
reach for: where does each one reduce risk? DDD reduces risk in *what* to
build — it exists because the requirements themselves are the dangerous,
ambiguous part. Plan-first reduces risk in *how* to build it safely — it
exists because the requirements are fine, but there are multiple ways to
execute them and some are much riskier than others.

Both of these require agreement before code gets written — that's the
shared DNA, and it's why they can feel similar at a glance. But they differ
in what, specifically, is being agreed to. Confusing the two costs you
review time: if you're debating requirements when you should be debating
approach, or vice versa, you're having the wrong conversation. The next two
slides give you a practical test for telling them apart in the moment.

---

## Slide 17 — When plan-first beats DDD

**(~5 min)**

So, concretely, when do you reach for plan-first specifically?

When requirements are clear, and the approach is what's risky. If nobody's
confused about what the end state should look like, DDD's spec-writing
step doesn't buy you much — there's no ambiguity in the "what" for a spec
to resolve.

Multi-file refactors, migrations, cross-cutting renames — these are the
canonical shapes of task where this applies. Our `formatCurrency` example
is exactly this: nobody disagreed about the goal, but there were three
files, a nonobvious discrepancy between them, and real decisions about
sequencing and risk.

The tell is: what needs review is the plan, not a requirements document.
If you find yourself wanting to review "how is the agent going to do this"
rather than "what exactly are we asking for," that's plan-first's territory.

And I'll draw the direct contrast back to Module 3 one more time, because
it's the cleanest way to fix this in memory: in Module 3, the requirements
were the risky part — that's why a spec, written and refined by a human up
front, was the right tool. Here, the requirements were never in question.
That's the axis this decision turns on.

---

## Slide 18 — When plan-first is overkill

**(~5 min)**

Equally important: knowing when *not* to do this, because plan-first has a
real cost, and applying it indiscriminately just slows everyone down for no
safety benefit.

Small, reversible, single-file changes are the classic case. If you're
fixing a typo, adjusting a constant, or making a change that's trivial to
revert if it's wrong, making the agent stop and produce a formal plan
before touching the file is pure overhead.

More generally: if writing and reviewing a plan costs more than just doing
the thing and checking the diff afterward, you've inverted the cost-benefit
that makes this methodology worthwhile in the first place. Plan-first only
pays for itself when the plan review is meaningfully cheaper than an
after-the-fact fix would be.

Here's the rule of thumb I want you to leave with, because it's genuinely
actionable in the moment: if you can't name two *plausibly different*
approaches to the task, skip the plan step. Think about our worked example
for a second — could you imagine a legitimately different but reasonable
way to consolidate the three `formatCurrency` copies? Yes, easily — you
could imagine unifying immediately, imagine preserving the discrepancy as a
parameter, imagine deprecating one call site rather than merging it. Multiple
plausible approaches, real branch points — that's what makes the plan worth
reviewing. If there's exactly one obvious way to make a change, there's
nothing for a plan to adjudicate, and asking for one is just ceremony.

---

## Slide 19 — Lab: a plan-gated multi-file refactor

**(~introduces ~45–60 min of hands-on lab time)**

Now it's your turn to actually run this workflow, not just watch it in a
worked example.

Pick a real multi-file refactor in your own sample repo. Two shapes that
work well for this: extracting a shared module — the same pattern as our
`formatCurrency` example — or renaming a widely-used interface, where the
risk is in catching every call site consistently.

Whatever you pick, the constraint for this lab is non-negotiable: require
an explicit plan — files, and why, for each one — before any edit happens
at all. If you're using Claude Code, this is exactly what plan mode is
built for: put the agent in plan mode, describe the refactor, and don't
let it out of that mode until you've actually reviewed what it proposes.

---

## Slide 20 — Lab steps

**(~part of the lab block above)**

Five concrete steps to work through.

One: describe the refactor to the agent, and explicitly ask for a plan
only — no edits yet. Be clear about this in your instructions; don't just
hope the agent infers it.

Two: review the plan against the anatomy checklist from Slide 7. Go
through it item by item — files and reasons, sequencing, risky spots
called out, non-goals stated. If something's missing, that's your answer
in step three.

Three: amend the plan or request changes, the way our reviewer did on
Slide 10 — targeted, specific feedback on the part that actually needs it,
not a wholesale rewrite — and then re-approve once you're satisfied.

Four: let the agent execute, now that it has an approved plan to execute
against.

Five: review the diff — the step the approval gate does not replace, per
Slide 11 — and specifically note any divergence between what the plan said
and what the execution actually did. That note is part of your
deliverable, so pay real attention here, not just a glance.

---

## Slide 21 — Deliverable

**(~part of the lab block)**

Three things to hand in at the end of this lab.

The approved plan, including any amendments — so both the original
proposal and the back-and-forth that shaped it, the same way we saw the
plan evolve in the worked example between Slides 9 and 10.

The resulting diff — the actual code change that came out of executing the
approved plan.

And a written note on any divergence between plan and execution, and why.
If there was no divergence at all, say that explicitly too — that's a
valid and useful outcome, not something to skip reporting.

---

## Slide 22 — Recap & next module

**(~4 min)**

Let's pull this all together.

Plan-first separates agreeing on approach from writing code — the same
underlying discipline as DDD, pointed at a different question, as we
established back on Slide 4 and again on Slide 16.

Approval gates only work if someone actually reads the plan. We spent a
good chunk of this lecture on failure modes precisely because the
mechanism is simple, but the discipline of actually engaging with it is
where things go wrong in practice.

ADRs make agent decisions durable across tasks, in a way plans
deliberately don't have to be — ephemeral plans, informed by durable
decisions, is the relationship to remember.

Next time, Module 6: TDD with Agents — tests as the spec. You'll notice
that's a third variation on the same theme running through this whole
course: agreeing on something before the agent writes production code.
Module 3 agreed on a written spec. This module agreed on a plan. Next time,
you'll see what it looks like when the thing you agree on *is* the test
suite itself. See you there.
