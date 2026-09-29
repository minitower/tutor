# Module 12 — Capstone: Lecture Script

Full spoken narration for a live session, slide by slide. Timing notes
are suggestions for a ~2.5–3 hour session that ends in an open-ended
lab — trim the walkthrough discussion if your cohort is fast, or let
it run long if the room is asking good questions, since the lab at the
end is designed to absorb whatever time remains.

---

## Slide 1 — Module 12 / Capstone

**(~5 min — framing, not content)**

Welcome to the last module. Before we start, I want to say plainly
what today is and isn't. Today is not a new technique. There's no
Module 12 methodology you haven't seen before. Everything we do today
is stuff you already know how to do — spec writing from Module 3,
plan mode from Module 5, TDD from Module 6, a second reviewing agent
from Module 8. What's new is doing all of them, in sequence, on
purpose, on one feature, and noticing what each one catches that the
others don't.

That's the actual skill this course has been building toward. Not
"know five techniques" — "know which combination a given feature
needs." So today has two halves. In the first half, I'm going to walk
you through one worked example end to end — a small, realistic
feature, built with the full toolkit — and we're going to stop after
every step and ask "what did that step just catch, that we would have
missed otherwise?" In the second half, you do it yourselves, on a
feature you pick, and that lab is going to take up most of the
remaining time.

## Slide 2 — Agenda

**(~2 min)**

Here's the shape of the session. We'll start with a quick recap of
the whole methodology comparison table — think of it as the entire
course compressed onto one slide. Then we walk through one worked
example, the CSV export feature, applying five different techniques
in sequence. After that we pause for a synthesis — what did each
technique actually catch. Then I hand you the capstone assignment
itself, the deliverable you're producing, the retro question you're
answering, and a rubric if you're running this as a cohort. And then
the lab, which is the rest of the session.

## Slide 3 — Learning objectives

**(~2 min)**

Four things by the end of today. First, you can choose *which
combination* of methodologies a feature needs — that's the whole
point, not defaulting to your favorite. Second, you can walk the full
loop: spec, plan, TDD, review, spec update. Third, you can name what
each technique catches that the others miss — that's not trivia, it's
the actual judgment call you'll be making on every future feature.
And fourth, you'll walk out with a real deliverable set: a spec, a
plan, tests, review notes, and a retro. Not a slide deck about the
idea — the actual artifacts.

---

### Recap of the toolkit (~10 min)

## Slide 4 — Recap: the whole toolkit, side by side

This table should look familiar — it's an expanded version of the one
from Module 11's appendix. I want to spend a minute on it because
today's whole argument depends on you actually internalizing this,
not just having seen it once.

Read down the "best for" column: DDD for ambiguous, multi-person
features. Plan-first for refactors and risky multi-file changes.
TDD-with-agent for bug fixes and well-defined logic. Conversational
for prototypes and one-off scripts. Multi-agent review for high-stakes
or security-sensitive code. Now read down "weak for" — and notice
something important: every technique's weakness is exactly another
technique's strength. DDD is overhead for a tiny fix — but that's
fine, because you wouldn't spec a tiny fix, you'd just do it
conversationally. TDD is weak for vague, exploratory UI work — but
that's fine too, because that's what plan-first or just talking to the
agent is for.

The mistake this whole course has been trying to train out of you is
picking one of these as your default and running everything through
it. A spec-first person specs everything, even the trivial fix — and
burns time on ceremony. A TDD purist tries to test-drive UI layout
decisions that don't have a "correct" answer to pin down — and gets
frustrated when the tests don't clarify anything. Today's feature is
deliberately picked to need *several* of these at once, because real
features usually do — they have an ambiguous part, a risky-approach
part, a logic-with-real-bugs part, and a "did we actually build what
we said we would" part, all in the same twenty-line diff.

## Slide 5 — Today's feature: CSV export with a date-range filter

Here's the feature we're using for the walkthrough: add an "Export
CSV" button to a reports dashboard, and make sure the export respects
whatever date range the user already has selected on screen. If
you've read `example-workflow.md` before class, this will look
familiar — we're walking through that document live, slide by slide,
because it's the best single illustration this course has of the
whole toolkit working together.

Why this feature, and not something bigger? Because it's small enough
to fit in one session, but it is not a toy. It touches a UI element —
the button. It touches a real data boundary — the query that filters
rows by date. And it has a genuine edge case that's easy to get wrong
— what happens when the date range crosses a daylight-saving
transition. That's exactly the shape of feature where "just wing it
with the agent" starts to show cracks, and where the discipline we've
spent eleven modules building starts to earn its keep.

---

### Step 1 — Spec it (~15 min)

## Slide 6 — Step 1 — Spec it (Module 3, DDD)

We start where Module 3 told us to start: with a spec, before any
code. Look at what's on the slide — Goal, Non-goals, Interface. This
is the DDD anatomy from Module 3, applied here.

The goal statement is one sentence and it's precise: let a user export
the *currently filtered* rows, matching the date range *already
selected*. Notice what that rules out implicitly — it's not "export
everything," it's not "export with its own separate filter UI." The
non-goals section makes two things explicit that a vague verbal
request would probably never mention: no new file formats, and no
scheduled or emailed exports — this is synchronous, click-and-download
only. If somebody six weeks from now proposes "let's also support
XLSX," this doc is the artifact that says "we explicitly decided not
to, here's why" — or at least, "here's what we'd need to revisit."

The interface section pins down exactly three things: what the button
is called, what the downloaded file is named, and that the columns
match what's on screen, in the same order. Notice the filename pattern
gets called out here as an actual interface commitment, not an
implementation detail — that's going to matter a lot in a few slides.

## Slide 7 — Step 1 — Edge cases & acceptance criteria

This is the slide that's actually doing the interesting work. Anyone
can write a goal and an interface. The edge cases section is where a
spec earns its keep, and it's also usually the part people skip when
they're asking an agent for a feature conversationally.

Three edge cases, and I want you to notice the shape of each one.
First: no rows in the selected range. The spec says explicitly —
header-only CSV, not an error. That's a one-line requirement that
prevents an entire class of "well, technically the range was empty, so
I threw a 404" behavior. Second, and this is the one to really pay
attention to: the range spans a daylight-saving transition — use UTC
dates everywhere. This is exactly the kind of bug that's invisible in
casual testing, because it only manifests on specific dates, and it's
the kind of thing a spec can name in one sentence that would take an
agent — or a human — a debugging session to discover on their own.
Third: an active column filter should still apply, not just the date
range — meaning the export can't just special-case the date filter and
ignore everything else the user has selected.

Then the acceptance criteria translate those edge cases into testable
assertions — three rows in, three rows plus a header out; empty range
in, header-only CSV out, not a 500, not a blank file; and the filename
uses UTC dates. These aren't prose anymore, they're things you can
literally write as test functions, which is exactly where we're headed
in Step 4.

And notice the very last line: one open question, left open on
purpose — should the button be disabled or hidden when there's nothing
to export? That's deliberate. A good spec doesn't try to resolve
*everything* up front. It resolves the things that are expensive to
get wrong later — the DST bug, the multi-filter interaction — and it
explicitly defers the things that are cheap to decide later, like a
minor UI behavior. Knowing which is which is a big part of the DDD
skill from Module 3.

## Slide 8 — Why this spec is sized right

Let's pause on sizing, because "how much should I put in a spec" is a
question people genuinely struggle with, and this is a good worked
answer. This spec is right-sized for two reasons.

First, it names the two edge cases that a conversational request would
almost certainly miss — the DST transition and the multi-filter
interaction. If you'd just told an agent "add a CSV export button,"
neither of those would have come up, because neither of them is
visible from looking at the UI. You only find them by thinking about
the data model and the calendar. That's the entire value proposition
of Module 3 in one sentence: naming the invisible edge cases before
code exists, when it's still cheap to name them.

Second — and this is just as important, if underrated — it doesn't try
to nail down the disabled-vs-hidden button question. That's not
laziness, it's judgment. Spending spec-writing time on a question that
has no real behavioral consequence is exactly the "ceremony that
doesn't pay for itself" that your retro is going to ask you about
later today. A stranger reading this spec could implement the feature
correctly and would only need to ask you about that one flagged
question — which is exactly the bar a spec should clear.

---

### Step 2 — Design tokens (~5 min)

## Slide 9 — Step 2 — Check the design system (Module 4)

Quick one, and I mean that literally — this step should take you
seconds in practice, which is the whole point of Module 4.

Because this repo already has a `CLAUDE.md` rule saying "before any
UI work, read the tokens file and the design doc, don't introduce
colors or spacing outside of it," the new button just... uses the
existing accent color and spacing tokens. Nobody had to say "use our
brand blue" in this conversation. Nobody had to review a screenshot
and say "that shade is off." The rule already existed at the repo
level, so it fired automatically, the same way a linter fires
automatically.

The only actual human action in this step is confirming it happened —
scan the diff for a raw hex value that shouldn't be there. If you find
one, that's a signal the rule either doesn't exist yet in this repo or
isn't being followed, which is worth fixing before this becomes a
recurring problem. But for a small addition like a single button, this
step really is "did the automatic thing work — yes — moving on." Bigger
UI work would get its own tokens-file check as a more deliberate step,
same as Module 4's own lab exercise.

---

### Step 3 — Plan before building (~12 min)

## Slide 10 — Step 3 — Plan before building (Module 5)

Now we're back into real decision-making territory, which is why we
switch back to a heavier technique. This feature spans frontend and
backend — a button plus a new endpoint plus a serialization step — and
that's exactly the shape of feature Module 5 told you plan mode is
for: not because the requirements are unclear, we just wrote a spec
that nails those down, but because the *approach* has real decision
points.

Walk through the five points on the plan with me. One: a new GET
endpoint that reuses the same query params as the existing reports
list endpoint — sensible, keeps two related endpoints consistent.
Two — and I want you to hold onto this one, we're coming right back to
it — reuse the existing filter-building logic rather than write new
filtering code for the export path. Three: serialize using the
existing column config, so if columns change later, the export doesn't
silently fall out of sync with the table. Four, the frontend button
and download wiring — the boring, low-risk part. And five, the plan
explicitly surfaces the open question from the spec and proposes an
answer — disable the button, don't hide it — flagging it for approval
rather than just picking one silently.

## Slide 11 — Step 3 — The approval gate catches something

Here's the moment that actually justifies the extra step of planning
before executing. Point two — reuse the existing filter logic — sounds
obvious once it's written down. But think about the counterfactual: if
you'd just told an agent "add an export endpoint" without a plan step,
there's a real chance it writes a *second* implementation of the
filter-building logic, tailored to the export path, because that's
often the path of least resistance for a fresh implementation. Six
months later those two filter implementations have quietly drifted —
someone fixes a bug in one and not the other, and now the list view
and the export disagree about which rows match a given filter. That's
an ugly, hard-to-notice bug, and it's exactly the kind of thing a plan
review catches when the cost of catching it is reading five lines of
text, versus catching it later when the cost is a second diff, or
worse, a support ticket.

The human review here is a two-second thing to actually do — approve
the plan as written, including the disabled-button decision. But
notice what made it possible: the plan wrote *out loud* something that
would otherwise have been an invisible implementation choice made
silently, deep inside a tool call. That visibility is the entire value
of plan-first, and it's why Module 5 called it a "propose" turn
followed by an "act" turn instead of just one turn.

---

### Step 4 — TDD the core logic (~15 min)

## Slide 12 — Step 4 — TDD the core logic: the DST bug

Now we get to the part of the feature that actually has business
logic worth testing — not the button, the date math. And notice the
order here: we write the test *before* the implementation exists,
which is Module 6's whole discipline.

The test constructs a date range that crosses a real US daylight-saving
transition — March 10th, 2024 — and asserts that the filename uses UTC
dates: `report_2024-03-09_2024-03-11.csv`. Run it against the first
implementation, and it fails. Why? Because the filename builder was
using the server's local time to format the dates, and depending on
what timezone that server happens to be running in relative to UTC,
that can shift a date by exactly one day right at the DST boundary.
That's a genuinely subtle bug — it wouldn't show up in casual manual
testing unless you happened to test on exactly the right two days of
the year. It's precisely the kind of bug that a spec's edge-case
section can *name*, but only a test can actually *catch*, because
"catching" here means running real code against a real date and
checking the actual output.

Fix gets applied — use UTC consistently in the filename builder — and
the test goes green. That's a real, verified fix, not "the agent says
it fixed it."

## Slide 13 — Step 4 — TDD the core logic: the empty-range shape

Second test, same discipline: written before — or at least, before
trusting — the implementation. This one targets the empty-range
acceptance criterion straight out of the spec: an empty date range
should produce a CSV with exactly one line, the header row. No rows,
no error.

Run this against the naive first implementation, and it also fails —
but in an interesting way. The naive implementation returned an HTTP
204 with no body when there were no matching rows, instead of a 200
with a header-only CSV. If you'd only eyeballed this feature — clicked
the button, looked at what downloaded — you might not have caught
this, especially if your manual testing always happened to have data
in range. A 204-with-no-body versus a header-only CSV is exactly the
kind of "looks right at a glance" mismatch that survives casual review
and gets caught by an assertion that actually checks the shape of the
response. This is Module 6's whole argument in one example: tests
don't just check "did it crash," they check "does the *shape* of the
output match what we agreed to build."

---

### Step 5 — Second-agent review (~12 min)

## Slide 14 — Step 5 — Second-agent review (Module 8's pattern)

Now the implementation is done and both tests pass. Time to bring in
Module 8's pattern: a second agent, in a fresh session, that has never
seen the first agent's reasoning — only the diff and the original
spec. This matters. If the reviewer had access to the same
conversation history as the implementer, it would inherit the same
blind spots — the same unstated assumptions that felt obvious in the
moment. A cold read against the spec is what makes this catch things a
"let me just re-check my own work" pass wouldn't.

Look at what came back. First, a straightforward confirmation — the
filename format and the empty-range behavior both match spec. Good,
that's the sanity check passing.

Second finding, and this is the one I want you to sit with: the
"respects other filters too, not just the date range" edge case from
the spec — remember, that was in the edge cases section on slide 7 —
isn't covered by any test. The endpoint accepts a `filters` parameter,
so the code path probably works, but nobody wrote a test that actually
exercises a date range *combined with* a non-date filter. That's a gap
between what the spec promised and what the tests actually verify.

Third, a smaller finding: the new endpoint doesn't share rate-limiting
middleware with the rest of the reports API. Not necessarily wrong —
but worth confirming it's a deliberate choice and not an oversight.

## Slide 15 — Step 5 — Why both findings matter

Let's be precise about *why* each of these findings is valuable,
because "the reviewer found some things" undersells it.

The first finding — the untested filter-combination edge case — is a
direct spec-to-test gap. It's not a bug in the code, necessarily; the
code might work fine. It's a gap in the *evidence* that the code works.
This is exactly the shape of thing Module 9 trained you to look for:
not "does this look plausible," but "does every claim in the spec have
a test backing it up." Neither the person who wrote the spec nor the
person who implemented it noticed this gap — which is completely
normal. You're close to your own work; that's exactly why a second,
cold pass matters.

The second finding is a different flavor entirely — it's not about
correctness against the spec at all, it's a scope question about the
implementation's *own* footprint. The implementer had no particular
reason to think about whether this endpoint should share rate-limiting
with its siblings — that's not really "their" question to ask about
their own work, in the same way you don't usually audit your own blind
spots. A fresh reviewer, looking at the diff with an eye toward "what's
different about this compared to its neighbors," is well positioned to
notice it precisely because they're not the one who wrote it.

Notice too what the reviewer *didn't* have to do to find these things
— it didn't have to re-derive the feature from scratch or re-invent
the spec. It just had to check the diff against the spec, methodically,
line by line. That's a genuinely learnable, teachable skill, and it's
what Module 9's lab was training.

---

### Step 6 — Close the loop (~8 min)

## Slide 16 — Step 6 — Close the loop: update the spec

Last step, and it's the one people skip most often in practice,
which is exactly why Module 3 insisted on it: once the review findings
are addressed — the missing test gets added, and the rate-limiting
question gets resolved as intentional, because exports are infrequent
and the existing limits were tuned for the much higher-traffic list
view — the spec itself gets updated.

Look at the addendum. One new line in acceptance criteria, documenting
that both filters now have test coverage. One new line in a notes
section, documenting *why* the rate limit is different, so nobody
"fixes" that difference by accident eighteen months from now, thinking
it's a bug.

This is the step that makes the spec a living document instead of a
historical curiosity. If you skip it, the next person — human or
agent — who reads this spec before touching this code gets the day-one
version, missing exactly the two things that review caught. The spec
becomes actively misleading, which is arguably worse than having no
spec at all, because it creates false confidence. Closing this loop is
cheap — it's maybe five minutes of editing — and it's the difference
between a spec that stays trustworthy over the life of the feature and
one that quietly rots.

---

### Synthesis (~10 min)

## Slide 17 — Synthesis — what each technique caught

Let's step back and look at the whole thing at once. Five techniques,
five different catches, and I want you to notice that none of them
overlap.

DDD caught two edge cases — the DST transition and the multi-filter
interaction — before a single line of code existed. That's the
cheapest possible place to catch something: in a sentence, not in a
diff.

Design tokens caught nothing, in the sense that nothing went wrong —
which is exactly the point. The mechanism worked so quietly that there
was nothing to catch, because the constraint was structural, not a
matter of vigilance.

Plan-first caught a code-duplication risk — reusing filter logic
instead of forking it — before any code was written, at the cost of
reading five lines.

TDD caught two real, executable bugs: a wrong timezone that produces a
wrong filename, and a wrong-shaped response — 204 instead of a
header-only CSV — that "looks right" on casual inspection but fails a
precise assertion.

And review caught a spec-to-test gap that neither the spec's author
nor the implementer noticed on their own, because closeness to your
own work is exactly what makes it hard to see its own blind spots.

## Slide 18 (still synthesis, continuing on the same slide)

Here's the punchline, and I want it to land: if you'd only used one of
these five techniques on this feature, you would have shipped with at
least one of these problems still in it. Spec alone doesn't run code —
it wouldn't have caught the timezone bug. Tests alone don't ask "did
we build what we agreed to build" — a test suite that never got told
about the multi-filter requirement wouldn't have known to test it.
Review alone can't invent an edge case that was never written down
anywhere for the reviewer to check against. Each technique's blind
spot is exactly where a different technique is strong. That's not a
coincidence — it's *why* the course structured itself as five separate
case-study modules instead of one "how to prompt an agent well"
module. And it's the whole argument for Module 12: stop defaulting to
your favorite, start combining deliberately, based on what kind of
risk the feature in front of you actually carries.

---

### The capstone assignment (~10 min)

## Slide 18 — The capstone assignment

*(Note: this is the actual Slide 18 in the deck — the synthesis
argument above lives on Slide 17; deliver it as one continuous beat
before transitioning here.)*

Now it's your turn, and the instructions are almost embarrassingly
close to what you just watched. Pick a feature substantial enough to
be worth a spec. Spec it, the DDD way — goal, non-goals, interfaces,
edge cases, acceptance criteria. Get a plan from the agent against
that spec, and actually review it before anything gets implemented,
the same way we caught the filter-duplication risk a few slides ago.
TDD the parts of the logic that are actually risky — not the
boilerplate around it, the business logic, the parts most likely to
have a DST-shaped bug hiding in them. Bring in a second agent, fresh
session, no access to your reasoning, and have it review against the
spec and for security concerns. And then close the loop — update the
spec so it reflects what you actually built, not what you originally
guessed you'd build.

This is not a new checklist. It's the same five steps you just watched
me walk through, on a feature of your own choosing.

## Slide 19 — Picking your feature

A word on choosing well, because the exercise only teaches you
something if the feature has real texture to it. It needs to be
substantial enough to be worth a spec — if you can write the entire
spec in two bullet points, this isn't the right feature, pick
something with more surface area. If genuinely nothing comes to mind,
the fallback in the assignment is a good one: a new authenticated API
endpoint with persistence and a test suite. That's small enough to
finish in a lab session but has real moving parts — auth, a data
write, a test.

Somewhere in your feature there needs to be actual business logic —
not just wiring together a database call and a response serializer.
If every line of your implementation is boilerplate, TDD won't have
anything interesting to catch, and the exercise will feel hollow. And
if you can find a feature with a genuine edge case — something
DST-shaped, something that's easy to get subtly wrong and hard to
catch by eyeballing — that's the feature that'll make today's lab feel
like today's lecture instead of a formality.

## Slide 20 — Deliverable

Four things, and I want them as *separate* artifacts, not folded into
one commit message or one paragraph. The repo or the diff for the
feature itself. The spec doc. The plan you got approved. The tests.
The review notes from the second-agent pass. And the retro, which is
its own slide because it deserves its own explanation.

Why insist on separate artifacts instead of one big writeup? Because
part of what you're demonstrating is that each step left behind a
real, checkable trace — the same way the worked example we just walked
through had five distinct artifacts, one per step. If everything gets
compressed into a single summary at the end, you lose the ability to
check "did the plan actually match the diff" or "did the review
actually happen before or after the spec update" — and that
traceability is the entire point of doing this deliberately instead of
just building the feature and calling it done.

## Slide 21 — The retro question

This is the part of the assignment people are tempted to skip or
phone in, and I want to push back on that in advance. The question is
specific: what would this feature have looked like if you'd built it
solo, without an agent, six months ago? Not "was AI helpful" —
everyone will say yes to that, and it tells me nothing. I want you to
actually name where the methodology choice saved you real time — maybe
the DST bug would have shipped and you'd have found it from a user bug
report three weeks later instead of from a test this afternoon. And I
want you to name, just as honestly, where it added ceremony that
didn't pay for itself — maybe writing a full plan for the frontend
button wiring was overkill, and you'd have just done it.

A retro that only says nice things about the process isn't a retro,
it's a testimonial. The honest version — the version with real
tradeoffs named — is worth more to you than a clean one, because it's
the version that actually improves your judgment about which
methodology to reach for next time.

## Slide 22 — Self-assessment rubric

If you're running this as a cohort, here's how to grade it — and
even if you're self-paced, use this as a checklist against your own
work. Spec quality: could a total stranger, with no context, implement
your feature correctly from your spec alone? Plan and spec fidelity:
did what actually got built match the approved plan, and if it
diverged, is that divergence written down somewhere, or did it just
silently happen? Test quality: do your tests actually pin down
behavior from the spec — the DST case, the multi-filter case — or do
they just exercise the happy path and call it done? Review rigor: did
your second-agent pass catch something real, the way ours caught a
genuine spec-to-test gap, or did it just say "looks good" without
actually checking anything? And retro honesty: does it name real
tradeoffs, the way we just discussed, or is it just "AI is great"?

---

### The lab (~90+ min, majority of remaining time)

## Slide 23 — Today's lab

This is the rest of the session, and I mean that literally — this lab
is built to absorb whatever time is left, so don't rush it. Step one:
pick your feature, and take five minutes to sanity-check it with a
neighbor or with me — is it substantial enough, does it have any real
logic in it. Step two: write the spec. Step three: get a plan from
your agent, actually read it, approve or amend it. Step four: TDD the
riskiest piece of logic you identified — not the boilerplate around
it. Step five: fresh session, second-agent review against your spec,
security lens included. Step six: close the loop — update your spec,
and write your retro.

I'll be walking the room. If you get stuck on spec-writing, that's
Module 3's territory and I'm happy to look at what you've got. If your
plan review feels like a rubber stamp, that's worth flagging out loud
— it usually means the plan wasn't concrete enough to actually
disagree with.

## Slide 24 — Course recap: the throughline

While you're getting started, or if we take a short break before
diving in, I want to leave you with the shape of the whole course,
because today is where all of it converges. Modules one and two gave
you the mechanics — how the agent loop actually works, and how to ask
for things precisely enough that the agent doesn't have to guess.
Modules three and four gave you durable contracts — specs for
ambiguity, design tokens for UI drift — documents that outlive a
single session. Modules five and six gave you ephemeral contracts —
plans and tests — built for a single task, thrown away or absorbed
once it's done. Module seven was the release valve: sometimes all of
this is overkill and you should just talk to the agent. Modules eight
and nine gave you composition and skepticism — more than one agent
working together, and the discipline of checking rather than trusting.
Ten and eleven took all of that out of a single session and into a
pipeline and a team. And twelve — today — is where you stop treating
these as separate tools in a toolbox and start treating the *choice*
of which ones to combine as the actual skill.

## Slide 25 — Closing

Last slide. The thing I most want you to leave with isn't any single
technique from this course — it's the instinct to ask, before you
start a feature, "what kind of risk does this actually carry?" Is the
risk that the requirements are ambiguous? Reach for a spec. Is the
risk that the approach could go sideways in a big multi-file change?
Reach for a plan. Is the risk buried in some specific piece of logic?
Reach for tests. Is the risk that nobody's checked this against the
original intent? Bring in a second reviewer. Most real features carry
more than one of these risks at once, which is exactly why today's
whole example needed five techniques, not one.

So: ship the capstone. Write the retro honestly — the honest one, not
the flattering one. That's genuinely the real diploma for this course,
more than any slide I've shown you today. Thank you all — go build
something real.
