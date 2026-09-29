# Module 2 — Lecture Script: Prompting & Task Specification

*Speaker notes for a live session. Read the slide titles aloud as you land on
them, then use this script as your narration. Timing notes assume a ~60–75
minute lecture portion followed by ~60–90 minutes of hands-on lab time,
totaling the module's target 2–2.5 hour session. Adjust to your room.*

---

## Slide 1 — Module 2: Prompting & Task Specification

**~3 min**

Welcome back. Last module we cracked open the agent loop — plan, act with
tools, observe, repeat — and you watched an agent work through a small task
one tool call at a time. Today we're not looking at the loop anymore. We're
looking at what goes *into* it.

The subtitle on this slide is the whole module in four words: precision in,
precision out. Everything we cover today — context versus instructions,
acceptance criteria, constraints, the anti-patterns — is really one idea
wearing four different hats. If you remember nothing else, remember that
phrase, because by the end of the lab you're going to see it happen in front
of you, in a diff, not just as a slogan.

Quick logistics note: today's lab produces three prompts and three diffs.
Keep that in the back of your mind as we go — every example I show you today
is deliberately building toward that lab, not just illustrating a point in
isolation.

---

## Slide 2 — Agenda

**~2 min**

Here's the shape of the next hour. We start with the gap between what you
meant and what you typed — that's the diagnosis. Then three tools for
closing it: separating context from instructions, writing acceptance
criteria, and stating constraints. Then we look at the three ways people
get this wrong even when they're trying — the anti-patterns — because
knowing the right shape doesn't automatically stop you from falling into
the wrong one under deadline pressure. Then we run one feature through
three levels of precision, side by side, so you see the effect, not just
hear about it. Then the lab, then the deliverable.

Nothing here is exotic. You already know how to write a clear sentence.
Today is about noticing the specific ways clarity leaks out of a prompt
when you're moving fast, and building a habit that catches it.

---

## Slide 3 — Objectives

**~2 min**

Two objectives, and I want to be precise about them because precision is
sort of the theme of the day.

First: write task descriptions that reduce the agent's need to guess. Not
eliminate — reduce. You will never fully specify everything; that's not
the goal and it's not achievable. The goal is to spend your precision
budget on the things that matter and stop worrying about the things that
don't.

Second: recognize the gap between what you meant and what you typed, and
close it *before* the agent starts working, not after. That "before, not
after" matters more than it sounds like it should. Closing the gap after
means you're now reading a diff, figuring out where it diverged from your
intent, explaining the correction, and waiting for a second pass. Closing
it before costs you thirty seconds of extra typing. That asymmetry is the
entire economic case for this module.

---

## Slide 4 — Why this comes right after Module 1

**~5 min**

Let's connect this to what you already know. In Module 1 you traced the
agent loop: it plans, it uses tools — reading files, running greps, editing
code, running tests — it observes what happened, and it decides what to do
next. That loop is genuinely impressive. It's also completely indifferent
to whether the plan it started with was any good.

Here's the thing people get wrong about agents when they're new to them:
they expect the agent to behave like a cautious junior engineer who stops
and asks when something's unclear. Sometimes it does ask. But often — and
this is the part that bites people — it doesn't. It picks the most
plausible interpretation of what you asked for, commits to it, and starts
executing with full confidence. There's no built-in humility checkpoint
where it says "wait, this is underspecified, let me pause." It will happily
build the wrong thing extremely competently.

So if Module 1 was about understanding the engine, Module 2 is about
understanding the fuel. A powerful loop running on an ambiguous prompt
doesn't produce a powerful *correct* result — it produces a powerful,
fully-executed guess. Today is about controlling what goes into that loop
before it starts spinning.

---

## Slide 5 — The core problem

**~5 min**

Here's the core problem, and I want to say it slowly because it's doing a
lot of work: there is a gap between what you meant and what you typed, and
the agent only ever sees what you typed.

You have a mental model in your head. It includes your team's conventions,
the history of why the code looks the way it does, the unstated assumption
that of course we're not going to break the mobile client, the fact that
"pagination" in your codebase specifically means cursor-based because
that's what the last three endpoints did. None of that travels with the
words "add pagination to the list endpoint" unless you put it there.

The agent doesn't have access to your mental model. It has access to the
text you wrote, plus whatever it can discover by reading the repo — which
is sometimes a lot, and sometimes nothing, depending on how legible your
codebase is. Where there's a gap, it doesn't leave a blank. It fills the
gap with the most statistically plausible guess given everything it's ever
seen — not necessarily the guess that matches your specific situation.

That's the whole game today: precision in, precision out. Ambiguity in,
you get a confident, complete, expensive-to-unwind wrong answer out. Keep
that phrase in your head as we go through the next three sections, because
each one is a specific, practical way of shrinking that gap.

---

## Slide 6 — Context vs. instructions

**~6 min**

First tool: separate context from instructions.

Context is what the agent needs to *know*. Facts about the system, existing
conventions, things that are non-negotiable, pointers to code that already
does something similar. Instructions are what you need it to *do* — the
actual task, stated once, stated plainly.

These sound like they should be easy to tell apart, but in real prompts —
the kind you type quickly in the middle of a workday — they get tangled
together constantly. You start explaining what the system does, and
halfway through that explanation you slip in the actual ask, and then you
tack on one more requirement at the end almost as an afterthought. The
agent has to do extra work just to figure out which sentence is the
instruction and which sentences are scene-setting. And when that
extraction goes wrong — when the agent treats a piece of context as
optional flavor, or treats a background fact as part of the task — you get
drift.

The fix isn't complicated: literally separate them. A short context block,
then a short task block. It feels almost too simple to be a "technique,"
but try it for a week and notice how much less back-and-forth you need.

---

## Slide 7 — Context vs. instructions — before / after

**~6 min**

Let's look at the before. "Our API uses Express and Postgres, and we use
cursor-based pagination elsewhere in the codebase, can you add pagination
to the users list endpoint, also make it fast." Read that out loud at
normal conversational speed — it sounds completely reasonable. People talk
like this all day. But look at what it's actually doing: it opens with two
facts, buries the actual instruction in the middle of a run-on sentence,
and appends a vague quality bar — "make it fast" — with no way to check it.

Now the after. Context on its own line: Express plus Postgres, existing
endpoints use cursor-based pagination, here's a file that shows the
pattern — `src/routes/orders.js`. Task on its own line: add cursor-based
pagination to `GET /api/users`, following the same pattern as
`orders.js`.

Notice what disappeared: "make it fast" is gone, and that's deliberate for
this example — it wasn't a real requirement, it was a feeling, and we'll
deal with how to turn feelings into requirements when we get to acceptance
criteria in a few minutes. What's left is something an agent can execute
against almost mechanically: go look at the named file, follow the named
pattern, apply it to the named endpoint. Notice too that pointing at a
concrete example file — `orders.js` — did more work than another paragraph
of description would have. A real file the agent can open and pattern-match
against is often worth more than prose.

---

## Slide 8 — Acceptance criteria

**~6 min**

Second tool: acceptance criteria. This is, in my experience, the single
highest-leverage change you can make to how you write tasks for agents.

Here's the principle: a task without a testable definition of "done" is a
task the agent will finish incorrectly with full confidence. Read that
again — *with full confidence*. This isn't a case where the agent throws
up its hands and asks you what "done" means. It picks a stopping point that
seems reasonable to it, declares victory, and moves on. It will stop
somewhere. Every task the agent runs has *a* stopping point. Your job is to
make sure that stopping point is the one you actually wanted, and the only
lever you have for that is stating it explicitly, in a form that can be
checked.

"Testable" is the operative word. Not "good," not "clean," not "robust" —
those are opinions, and opinions can't be checked pass or fail. "The
response includes a `next_cursor` field that is `null` on the last page"
— that's testable. You can look at a response and know, unambiguously,
whether it's true. That's the bar: could you, or a test suite, look at the
result and answer yes or no?

This is also, not coincidentally, exactly the skill you already have if
you've ever written a good bug report or a good PR description. You're not
learning a new skill today so much as applying a skill you already have to
a new audience that takes you extremely literally.

---

## Slide 9 — Acceptance criteria — before / after

**~6 min**

Before: "Add pagination to the products endpoint so it's not too slow."
"So it's not too slow" is doing the same job "make it fast" was doing a
minute ago — it's a feeling wearing the costume of a requirement. What
counts as not-too-slow? Compared to what baseline? Nobody said, so the
agent can't check it, and neither can you, later, when you're trying to
decide if the task is actually done.

After: four bullet points, and I want you to notice they're not more
*words*, they're more *structure*. `limit` defaults to 20, maxes at 100.
`cursor` is an opaque string that comes from a prior response. The response
gains a `next_cursor` field. Requesting a limit over 100 gets you a 400.
No query params at all gets you the first page, same shape as today.

Every one of those four bullets is something you could write an assertion
for. `expect(response.next_cursor).toBeDefined()`. `expect(status).toBe(400)`
when limit is 101. That's the test. If you can imagine the test, you've
written a good acceptance criterion. If you can't imagine what the test
would even check, that's a sign the criterion is still a feeling in a
trench coat.

One more thing worth calling out: none of these four bullets mention
performance at all. That's fine — "so it's not too slow" wasn't actually
specific enough to be worth preserving. If speed genuinely mattered here,
the fix isn't a vague adjective, it's a number: "must return within 200ms
for a page of 20 items on the staging dataset." Same discipline, applied to
the one requirement that was real.

---

## Slide 10 — Constraints matter as much as goals

**~6 min**

Third tool, and this is the one people skip most often because it feels
like it should be implied: constraints.

A goal tells the agent where to go. A constraint tells it what not to break
on the way there. And here's the part that's easy to underestimate: if you
don't state a constraint, it doesn't default to "off" — it defaults to
"the agent is free to do whatever gets the goal satisfied most cheaply."
Cheaply from the agent's perspective usually means: fewest tool calls,
least exploration, most direct path. That path frequently walks straight
through something you assumed was obviously off-limits.

"Don't touch the public API." "Keep it in one file." "No new dependencies."
Say these out loud and they sound almost too obvious to need saying. But
they're not obvious to something that has no idea your team had a six-month
debate last year about dependency bloat, or that three other services
import that function signature you're about to casually change.

The mental shift I want you to make: goals describe the destination.
Constraints describe the walls of the corridor you're allowed to walk
through to get there. Without walls, "get to the destination" and "get to
the destination by any route" are the same instruction to an agent — and
the second one is rarely what you meant.

---

## Slide 11 — Constraints — before / after

**~6 min**

Before: "Refactor the auth module to be cleaner." This is a goal with zero
walls. "Cleaner" is subjective, and with no constraints, the agent might
decide the cleanest solution involves renaming exported functions,
changing their signatures, pulling in a new validation library it likes,
and touching every file that imports from this module. Technically it
satisfied "cleaner." It also potentially broke three other services that
depend on those signatures, none of which were mentioned, none of which
the agent had any way of knowing about unless you told it.

After: same goal, four walls. Don't change exported signatures in
`auth/index.js` — and notice we say *why*: three other services import
them. That "why" isn't decoration; when an agent understands the reason
for a constraint, it tends to generalize it correctly to adjacent
decisions you didn't explicitly cover. No new dependencies. Diff under
roughly 150 lines — that one caps the blast radius of "cleaner" so it
doesn't turn into a rewrite. And all existing tests pass unmodified — which
is a constraint *and* a de facto acceptance criterion, and that overlap is
completely fine. These categories aren't mutually exclusive; they're lenses
on the same prompt.

Same destination, same underlying ask. Wildly different set of possible
outcomes, because now the corridor has walls.

---

## Slide 12 — Anti-pattern #1 — the vague ask

**~5 min**

Now let's talk about how this goes wrong even for people who've heard
everything I just said. Three anti-patterns. First: the vague ask.

"Make this better." "Clean up the error handling." "Optimize this." These
show up constantly, and they show up because they're *fast to type* and
they feel like they communicate something. They don't, not to an agent.
"Better" has no shared definition between the two of you. You have one in
your head. The agent will construct its own, commit to it fully, and
execute against it with the same confidence it would bring to a perfectly
specified task — because from its side, there's no signal that this
definition is shakier than any other.

The fix isn't "write a five-page spec every time." Sometimes "clean up the
error handling" is genuinely fine — for a tiny, low-stakes, easily-reverted
change, in a codebase you'll review carefully anyway. The fix is
*noticing* when you've typed a vague ask, and asking yourself one question:
if the agent came back with three wildly different interpretations of this,
would I be equally happy with all three? If not, you have more precision to
spend, and it's cheap to spend it now.

---

## Slide 13 — Anti-pattern #2 — missing "done"

**~5 min**

Second anti-pattern: missing "done." This one's sneakier than the vague
ask, because the request itself can sound perfectly concrete.

"Add rate limiting to the API." That's not a vague verb like "improve" —
"add rate limiting" sounds like an engineering task with a clear shape.
But sit with it for ten seconds and the questions pile up. Rate limiting on
which endpoints — all of them, just the expensive ones, just the public
ones? Per user, per IP, per API key? What's the actual limit — ten requests
a second, a hundred a minute? And when someone exceeds it, what happens —
a 429 status, a `Retry-After` header, a queued request, a silently dropped
one?

None of those are exotic questions. They're the first four questions any
competent engineer would ask before touching this ticket. The difference
is a human engineer sitting next to you will usually walk over and ask
them before writing code. An agent, much more often, will pick reasonable-
sounding defaults for all four and ship a fully working implementation of
a rate limiter you didn't quite ask for. Every one of those unanswered
questions is a decision that got made — just not by you.

---

## Slide 14 — Anti-pattern #3 — burying the requirement

**~6 min**

Third anti-pattern, and this is the one I see even from people who are
otherwise very good at writing specs: burying the real requirement.

Listen to this one: "We've had this pagination discussion before, the old
approach used offsets, our DB team doesn't love that, there was a ticket
about it last quarter... anyway, this needs to ship before the 3pm demo so
please only touch the frontend, not the API." Every clause in there is true
and probably relevant to *you* — it's the story of how this task came to
exist. But the one clause that is an actual hard constraint on what the
agent is allowed to do — don't touch the API — is the very last few words
of the very last sentence.

Why does this happen? Because that's how humans naturally narrate a
decision. We build up the context, and the punchline comes last, the way
you'd tell a story to a colleague over coffee. Agents process the whole
prompt, so in principle nothing is technically lost — but the *salience*
is wrong. A constraint sitting at the end of a paragraph of backstory
competes for attention with everything before it, and things stated later
without emphasis are exactly the things that get under-weighted, by
agents and by tired humans skimming a message at 4:45pm.

The fix is structural, not about trying harder to remember to mention it
early: put constraints and acceptance criteria in their own labeled lines,
separate from the narrative. Tell the story if you want to — it can be
useful context — but don't let the hard requirement live only inside it.

---

## Slide 15 — Anatomy of a well-specified task

**~5 min**

Let's pull all of this into one shape. A well-specified task has five
parts. Context: the facts and patterns the agent needs to know. Task: one
unambiguous sentence describing what to build. Constraints: what must not
change or break along the way. Acceptance criteria: a testable definition
of done. And edge cases: what happens at the boundaries — empty results,
invalid input, the last page, the first page, the zero case.

I want to head off a misreading of this slide: I am not telling you to
fill out all five sections for every single prompt you write for the rest
of your career. A one-line fix to a typo doesn't need edge cases enumerated.
What I am telling you is that skipping a section should be a *decision* —
you looked at the task, decided constraints genuinely don't apply here, and
moved on — rather than an accident of typing quickly and not thinking about
it. The five-part shape is a checklist you run in your head in about five
seconds, not a form you fill out in triplicate.

Now let's see this shape do actual work. We're going to take one feature
and run it through three levels of this anatomy, and watch what changes.

---

## Slide 16 — Worked example: three passes, one feature

**~4 min**

Here's the setup, and it's the same setup you'll use in the lab in a few
minutes, so pay attention to the mechanics as well as the content.

The feature: add pagination to `GET /api/products`. We're going to write
three versions of the request to an agent — vague, constrained, and fully
specified — and for each one, we start from a *clean session*. That's not
a minor detail. If you run all three in the same conversation, the agent
carries context from the first attempt into the second and third, and
you're no longer measuring what the prompt alone produced — you're
measuring the prompt plus whatever it already learned from your earlier
corrections. Clean session each time is what makes this a fair comparison,
and it's exactly what you'll do in the lab.

Same feature, same starting repo, three different levels of precision.
Let's walk through what typically happens at each level.

---

## Slide 17 — V1 — Vague

**~5 min**

Version one: "Add pagination to the products list endpoint." That's it.
That's the whole prompt. It's not a strawman — this is a completely
realistic thing to type into an agent at 2pm on a Tuesday when you're
context-switching between four other things.

What tends to happen: the agent picks *a* pagination style. Very often
that's offset-and-limit — `?page=2&pageSize=20` — because that's the most
common pattern it's seen across the widest range of codebases, not
because it's necessarily the right pattern for *your* codebase. It picks
some limit, maybe unbounded, maybe an arbitrary default it invented on the
spot. It has no way of knowing your other endpoints use cursor-based
pagination unless it happens to notice by reading the code — and it might
not go looking, because nothing in the prompt suggested there was a
convention worth checking.

The output might genuinely work. Requests come in, pages come back. But
it may not match your codebase's conventions, may not have sane limits,
and you won't find out which of those problems you have until you read
the diff carefully or someone hits an edge case in production. This is
the baseline we're comparing against — hold onto what this diff looks like
when you get to the lab.

---

## Slide 18 — V2 — Constrained

**~5 min**

Version two adds the structural bullets we saw earlier: `limit` defaults
to 20 and maxes at 100, `cursor` is opaque and comes from the prior
response's `next_cursor`, and the response gains that `next_cursor` field.

This closes the biggest gap from V1. The agent now knows the *shape* of
the solution you want — cursor-based, not offset-based, with bounded page
sizes. That's a real, meaningful improvement, and if you diff this output
against V1's, you'll see it immediately in the response schema and in the
query parameter handling.

But watch what's still open: what happens when someone sends a cursor
that's malformed, or expired, or simply doesn't correspond to anything in
the current dataset? What happens if someone requests a page past the
last one — do they get an error, or an empty list? Nothing in this prompt
says. So the agent decides, on its own, and it might decide to throw an
unhandled exception that surfaces as a 500, or it might silently return an
empty array, or it might do something else entirely reasonable-sounding
that nonetheless isn't what you'd have chosen. Constrained is a big step
up from vague. It is not the same as fully specified.

---

## Slide 19 — V3 — Fully specified

**~6 min**

Version three keeps everything from V2 and adds the piece that was
missing: edge cases, stated explicitly. Invalid cursor format returns a
400. A cursor pointing past the last page returns an empty `items` array
with `next_cursor: null` — not an error, an empty success. No parameters
at all gives you the first page in the same response shape the endpoint
already returns today. And critically, one more line: the existing
integration tests for this endpoint must still pass, unmodified — which
is your safety net that this whole exercise didn't quietly break backward
compatibility for existing callers.

What typically happens here: the agent handles those edge cases correctly,
because they stopped being edge cases it had to invent an answer for —
they became explicit requirements it could check itself against before
declaring the task done. This is the mechanism, not a coincidence: an
agent that has something concrete to verify against will generally verify
against it. An agent with nothing to verify against has nothing to be
wrong about, in its own estimation, no matter what it actually produces.

That's the whole lesson of this worked example in one sentence: precision
bought correctness exactly where you spent it, and nowhere else. That's
also the exact question your lab comparison notes need to answer — where
did the precision pay off, and just as importantly, where did it stop
mattering, because that's information too.

---

## Slide 20 — Lab

**~5 min**

Here's what you're doing for the next stretch of the session. Pick one
small feature — you're welcome to use the pagination example we just
walked through, or pick something from your own codebase if you'd rather
work with something you know well; either is fine, and honestly working
with your own code tends to surface more interesting surprises.

Write three versions of the request, exactly like we just did: vague,
constrained, fully specified. Then — and this part is not optional — run
each one through an agent starting from a **clean session**. Not three
messages in the same conversation. Three separate sessions, so the agent
has no memory of the previous attempt influencing this one. If you skip
this step, your comparison is contaminated and you won't be able to trust
your own diffs.

Then diff the three outputs against each other. Not just "does it work" —
actually read the diffs side by side. Look for where the implementation
approach changed, where edge case handling appeared or didn't, where the
response shape shifted.

I'll circulate to answer questions while you work. If you get stuck picking
a feature, the pagination example is sitting right there, fully worked —
use it.

---

## Slide 21 — Deliverable

**~3 min**

Your deliverable has three parts, and all three matter — this isn't just
"turn in the diffs."

One: the three prompts themselves, exactly as you sent them. Two: the
three resulting diffs. Three — and this is the part people are tempted to
skip because it feels like the "soft" part — a short written comparison
answering two questions. What did the extra precision actually buy you,
concretely, in the diff? And where did it stop mattering — where was V3
functionally identical to V2, meaning that extra effort you spent didn't
change the outcome?

That second question is just as important as the first. Precision isn't
free — it takes time to write, and the point of this exercise isn't
"always write the maximally detailed prompt." It's learning to *feel*
where the marginal sentence of precision is worth writing and where you've
already covered the ambiguity that mattered. That judgment is the actual
skill. The three-diff exercise is just how we make it visible.

---

## Slide 22 — Recap & next module

**~4 min**

Let's land the plane. Precision in, precision out — the agent fills every
gap you leave, and it fills it with its best guess, not yours, unless you
close the gap yourself. Three concrete habits that do that: separate
context from instructions so the agent knows what to check its work
against. Write acceptance criteria so "done" is something you can test,
not something you feel. State constraints so the goal doesn't get
satisfied by walking through a wall you assumed was solid.

Here's where this goes next. Today, every one of those three habits lived
inside a single prompt — you typed it, the agent read it, the task ended,
the prompt was gone. Module 3 is Document-Driven Development, and it asks
the obvious next question: what if the spec didn't disappear after one
task? What if it were a durable document — something the whole team can
read, that the agent can be pointed back at across multiple sessions, that
gets updated as you learn more instead of being retyped from scratch every
time? Everything you practiced today — context, acceptance criteria,
constraints — is about to become the anatomy of that document instead of
the anatomy of a single message.

Good work today. Get those three diffs, and I'll see you at Module 3.
