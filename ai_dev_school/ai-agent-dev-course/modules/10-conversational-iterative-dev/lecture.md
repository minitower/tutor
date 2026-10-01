# Module 10 — Lecture Script: Conversational / Iterative Development

Instructor notes: this script is written as spoken narration. Read it as
a guide, not a teleprompter — your own phrasing will land better than a
verbatim recitation. Timing notes assume a live 2–3 hour session where
this lecture is followed by hands-on lab time; total spoken material
here runs roughly 90–100 minutes, leaving the remainder of the session
for the lab and discussion.

---

## Slide 1 — Module 10: Conversational / Iterative Development

**~3 min**

Welcome back. We're on Module 10 now, and I want to start with a
confession: this is the module that describes what most of you were
already doing before you took this course.

Think about the last time you sat down with an AI coding agent for
something small — "add a loading spinner here," "why is this test
flaky," "clean up this function." You didn't write a spec. You didn't
open a plan-mode session. You just talked to it, looked at what it did,
and told it what to fix. That's conversational development. It's the
default mode, the one everybody falls into without deciding to.

The last few modules have all been about adding structure before you
start: a spec in Module 6, a design system in Module 7, an approved plan
in Module 8, a failing test in Module 9. Structure that front-loads the
thinking so the agent has less room to go sideways.

This module is different on purpose. We're not going to add structure.
We're going to get good at *not having it* — because sometimes that's
the right call, and the skill isn't "avoid conversational mode," it's
"know when to use it, and do it well when you do." That's today's case
study focus: tight loops, no upfront doc.

---

## Slide 2 — Agenda

**~2 min**

Here's the shape of the next hour and a half. We'll place conversational
work among the methodologies you've already learned, so you have a
mental map of when to reach for it. Then we'll spend the bulk of our
time on the two skills that actually make this mode work well instead of
badly: incremental correction — how you talk to an agent turn by turn —
and detecting and recovering from agent drift, which is the single
biggest way this mode goes wrong. We'll cover session and context
management for when conversations run long. Then we'll talk honestly
about what this mode costs you — no paper trail — and how to soften
that cost without abandoning the mode entirely. And we'll close with the
lab, where you'll rebuild the same feature from Module 6, but this time
purely by talking to the agent.

---

## Slide 3 — Objectives

**~2 min**

By the end of today, you should be able to do five concrete things.
Run a tight feedback loop on a small task with nothing written down
beforehand. Notice when an agent has quietly drifted off your actual
goal — and notice it early, not five turns later. Correct an agent with
a short, targeted message instead of re-explaining the whole task from
scratch, which — spoiler — is the single most common mistake people
make in this mode. Make a deliberate call about when to keep working in
a session versus closing it and starting fresh. And be honest with
yourself about what this approach costs you down the line, so you can
decide, task by task, whether that cost is worth paying.

Notice none of these are about writing better prompts up front. They're
all about what you do *during* the conversation. That's the whole game
here.

---

## Slide 4 — Where this fits

**~6 min**

Let's ground this against the comparison table from the syllabus
appendix, because I think this table is the single most useful thing to
internalize in this whole course.

Document-Driven Development is best when there's real ambiguity and
more than one person needs to agree on what's being built — and it's
overkill for a five-line fix. Plan-first is for refactors and risky
multi-file changes, weak for fast exploration because writing a plan for
something you're still discovering is backwards. TDD-with-agents is
great for bug fixes and well-defined logic, weak for vague or
exploratory UI work where you don't know what "correct" looks like yet.

And then there's conversational — us, today. Best for prototypes,
one-off scripts, exploration. Weak for anything that needs a paper
trail. And look at that last column: artifact left behind. DDD leaves a
spec. Plan-first leaves a plan or an ADR. TDD leaves a test suite. We
leave... nothing. Chat history only.

That's not a criticism baked into the table by accident — it's the
entire tradeoff of this module, stated as plainly as it can be stated.
Every other module you've taken front-loads some kind of structure.
This one deliberately trades that structure away for speed. Whether
that's a good trade depends entirely on the task in front of you, and a
big part of today is building your judgment for that call.

---

## Slide 5 — What "conversational / iterative" means

**~5 min**

Let's be precise about what we mean, because "just talk to it" sounds
simple but has real content underneath it.

There's no spec. No plan doc. No test-first contract establishing what
"done" looks like before you start. It's you and the agent, turn by
turn: you say something, the agent acts, you look at the result, you
respond to *that*, not to some pre-written description of the ideal end
state.

That last point is the important one — you're reacting to what actually
happened, not specifying everything in advance. This is fundamentally
an emergent process. The shape of the final solution isn't decided at
turn one; it's negotiated turn by turn between what you ask for and what
the agent produces.

And here's the thing I want you to sit with: the task description *is*
the conversation. There's no artifact sitting next to it capturing the
intent. If you closed the chat right now, the only record of what you
were trying to do and why is... gone, except for whatever ended up in
the code. We'll come back to that cost later, but I want you to notice
it now, while we're still defining terms, because it's not a side
effect — it's baked into the definition of this mode.

---

## Slide 6 — When to reach for it (and when not to)

**~5 min**

So when is this actually the right call?

Good fit: small, well-bounded tasks where writing a spec would cost more
than just doing the task. If the whole feature is smaller than the spec
would be, the spec is pure overhead. Good fit: genuine exploration,
where you don't yet know the shape of the solution — you can't write an
acceptance criterion for something you haven't figured out yet. Good
fit: throwaway scripts, spikes, "try three different approaches and show
me the results" — things that exist to answer a question, not to become
production code.

Bad fit: anything a teammate, or you in six months, will need to
understand without you personally in the room to explain the backstory.
Bad fit: multi-file changes with real ambiguity about intent — that's
squarely Module 6 or Module 8 territory, where getting the direction
wrong costs a lot more than the up-front cost of writing it down.

The test I'd suggest: if you can't imagine anyone ever asking "why does
this code look like this," conversational is probably fine. If you can
easily imagine that question being asked next quarter, you need one of
the other methodologies, or at minimum you need to do the mitigation
we'll cover in a few slides.

---

## Slide 7 — Key concept: Incremental correction

**~6 min**

Now we get into the actual craft. The single most important skill for
making this mode work is what I'm calling incremental correction: short,
specific course-corrections beat restating the whole task.

Here's why this matters so much. When something comes back wrong and
your instinct is to retype the entire original request with one more
clause tacked on — "build the export feature, and also handle empty
results, and also don't break the existing filters" — you're not
correcting, you're starting over. And starting over throws away
everything the agent got right the first time. It also doesn't tell the
agent what specifically was wrong; it just gives it a new, longer prompt
to guess against, and it might guess wrong in a completely different
direction this time.

A precise correction does the opposite: it narrows the search space
instead of widening it. If you say "the CSV export is failing on empty
date ranges, fix just that," the agent has almost nowhere left to guess.
The two words that matter most in any correction are the symptom — what
is actually wrong, concretely — and the boundary — what must *not*
change while you fix it. Say both, every time, and you'll spend far
fewer turns getting to a working result.

---

## Slide 8 — Incremental correction — example

**~6 min**

Let's make this concrete with a side-by-side.

Weak correction: "That's not quite right, the export should also
handle empty ranges and the filters properly, can you redo it." Read
that again as if you were the agent receiving it. What's "not quite
right" — the whole thing? Which filters? What does "properly" mean?
"Redo it" invites a full rewrite, which risks losing the parts that were
already fine. This message is guessable in at least four different
directions, and there's a real chance the agent picks a fifth one you
didn't consider.

Strong correction: "Don't touch the button or the endpoint route — just
the `export_reports_csv` function. An empty date range should return a
header-only CSV, not a 500. Revert the retry-loop you added, that's
unrelated." Notice what's doing the work here. It names the file or
function — no ambiguity about *where* to look. It states the exact
expected behavior for the specific broken case — a header-only CSV, not
"handle it properly." And it explicitly calls out something to *undo* —
the retry loop — rather than just leaving it and hoping the agent
notices it's unwanted.

This is a learnable habit, not a personality trait. Before you send a
correction, ask yourself: if I only got to say one sentence, which
sentence actually points at the bug? Send that one.

---

## Slide 9 — Key concept: Agent drift

**~7 min**

Now the concept I think is the most important one in this whole module:
agent drift. Definition — the agent quietly wanders away from the
actual goal while still producing plausible-looking work, turn after
turn. The word doing the heavy lifting there is "quietly." Drift doesn't
announce itself. The agent doesn't say "I'm now solving a different
problem." Every individual turn looks reasonable in isolation. It's only
when you zoom out across several turns that you see the trajectory has
left the goal behind.

Where does it come from? Four common sources, and I want you to
recognize each of these when they happen to you, because they happen to
everyone.

One: the original ask was ambiguous, and an early wrong guess compounds.
If turn one produced a subtly wrong interpretation, turns two through
six all build on that wrong foundation, and by turn six you're deep into
a coherent-looking solution to the wrong problem.

Two: the agent "solves" a nearby problem instead of the real one. You
asked about a specific bug; it noticed something adjacent that looked
messy and "helpfully" refactored it. It's not being malicious — it's
being helpful about the wrong thing.

Three — and this connects to session management, which we'll cover
soon — a constraint you stated fifteen turns ago has scrolled out of
active context. You said "no new dependencies" at the start; by turn
twenty, that instruction may no longer be in the working context the
model is actually attending to, especially after a compaction event.

Four: it fixates on the wrong root cause and keeps patching symptoms.
You say "still broken," it tries another patch on the same wrong theory,
you say "still broken" again, and now you're four turns deep in the
wrong direction, each turn looking like reasonable debugging.

---

## Slide 10 — Detecting drift — signals

**~6 min**

So how do you actually catch this while it's happening, rather than
discovering it after the fact? Five signals, and I want these to become
reflexive checks you run without even thinking about it.

First: the diff touches files or areas you never mentioned. This is the
single most reliable signal, and it's why you should be looking at the
actual diff, not just reading the agent's summary of what it did. If you
asked about the export function and the diff includes changes to the
authentication middleware, stop right there.

Second: the agent's explanation of what it did no longer matches what
you asked for. If there's a gap between the request and the narration
of the response, that gap is information — don't let it slide past you.

Third: you've said "no, that's not what I meant" more than once about
the same request. One correction is normal. A second correction on the
same point means your first correction didn't land, or the agent is
oscillating rather than converging — either way, it's time to change
approach, not just repeat yourself louder.

Fourth: the agent claims something works, but you haven't verified it
yourself — and when you actually check, it doesn't. This is about
trusting the agent's self-report over ground truth, which is a mistake
we'll come back to.

Fifth: watch for confidence language — "this should now work," "this
fixes the issue" — standing in for actual evidence. Confident language
is not proof. It's often exactly what shows up right before a wrong
turn, because the model is expressing certainty about its own
reasoning, not reporting a verified outcome.

---

## Slide 11 — Recovering from drift

**~6 min**

Okay, you've caught it. Now what? Four steps, roughly in order.

One: name the exact deviation. Not "this is wrong" — that's a
non-correction, it gives the agent nothing to act on differently. Say
"you changed the auth middleware, I only asked about the CSV
serializer." Specificity here does the same work it does in incremental
correction generally — it collapses the space of things the agent might
try next.

Two: roll back the specific change, don't layer a fix on top of a wrong
turn. If the agent added something unwanted, the fastest path is often
to explicitly ask for that piece to be reverted before continuing —
not to ask for "the good parts" to be kept while patching around the
bad part, which usually leaves traces behind.

Three: re-anchor on ground truth. Run `git diff`, run `git status`, run
the actual application. Don't trust the agent's self-report about what
changed or what works — verify it yourself, directly. This is the
single habit that catches drift the earliest, because it doesn't depend
on the agent noticing its own mistake.

Four, and this is the one people resist because it feels like giving
up: when drift is deep — many turns have compounded on each other —
it is very often cheaper to close the session and start a fresh one
than to keep patching this one. I know that feels like throwing away
progress. But a session that has accumulated several wrong turns is now
carrying that entire messy history as context for its *next* guess. A
fresh session, primed with a short, correct summary of where things
actually stand, frequently gets to a good answer faster than untangling
five compounding mistakes in the drifted one.

---

## Slide 12 — Worked example: drift and recovery

**~6 min**

Let's walk through a concrete case, close to the feature we'll use in
the lab.

Turn four: "Add CSV export with a date-range filter." Reasonable,
small ask. Turn nine — five turns later — the agent has also refactored
the shared query builder that the export function uses, "for
consistency." Nobody asked for that. It's untested. And it's now sitting
in the diff, mixed in with the code you actually wanted.

This is textbook drift. It's not catastrophic — the agent was trying to
be thorough — but it's scope creep that happened quietly, and if you
don't catch it here, it ships alongside the feature you actually asked
for, and six months from now nobody knows why the query builder looks
different.

The recovery: "Revert the query-builder refactor — out of scope. Keep
only the export function and the new route. Show me the diff before we
go further." Notice the structure again: name the exact unwanted
change, state what to keep, and — this is a nice habit to build in —
ask to see the diff before continuing, so you're verifying against
ground truth rather than trusting the next round of narration.

The reason this recovers in one turn instead of three is entirely
because the correction is specific. "Clean this up, it looks messy"
would have taken several more rounds to converge on the same outcome.

---

## Slide 13 — Key concept: Session/context management

**~6 min**

Let's talk about what happens as these conversations get long, because
drift and context management are closely related — a lot of the drift
we just discussed gets worse, not better, the longer a session runs.

The mechanical fact underneath this: long conversations fill the
context window, and agentic tools compact older turns when that happens
— they summarize or drop earlier parts of the conversation to make room
for new ones. This isn't a bug, it's a necessary tradeoff, but it has
consequences you need to plan around.

The practical symptoms of context pressure: the agent re-asks something
you already told it earlier in the same conversation. It contradicts a
decision it made — or you made — several turns back. It forgets a file
it already edited and re-derives an inconsistent version of the same
logic. None of these are the agent "being dumb" — they're the direct,
predictable result of information falling out of the working context.

And here's the compounding problem: a session that has drifted and been
corrected several times doesn't just contain the good final state — it
contains the *entire history* of wrong turns and corrections, which is
now part of what feeds the model's next guess. That messy history is
itself a source of further confusion, on top of whatever got compacted
away. This is exactly why "start a fresh session" from the last slide
isn't a cop-out — it's often the more efficient path.

---

## Slide 14 — Session/context management — practical rules

**~6 min**

So, practical rules for managing this.

When should you start fresh? Three triggers: a wrong turn has already
compounded into several dependent wrong turns; the session's own history
of mistakes is now actively feeding new bad guesses; or you're switching
to a genuinely unrelated subtask and there's no benefit to carrying the
old context forward. Any one of those is a good reason to close the
session rather than push through.

When you do start fresh, don't rely on the new session inheriting a
clean understanding of "where we left off" — it won't, and even
if you paste in the whole old transcript, that's exactly the kind of
long, noisy context we're trying to avoid. Instead, write a short
state-of-the-world recap yourself: what's already done, what's next,
and which constraints still apply. This is maybe three to five
sentences, and it's worth the two minutes it takes to write, because it
gives the fresh session exactly what it needs without the baggage of how
you got there.

And here's a connection back to Module 6: constraints that should hold
for the whole task — "no new dependencies," "don't touch the auth
module," whatever your standing rules are — belong in `CLAUDE.md` or
`AGENTS.md`, the repo-level agent docs, not buried somewhere in turn six
of a conversation. A constraint stated only in chat doesn't survive a
session reset. A constraint written into the repo-level doc survives
every session, forever, without you having to remember to restate it.
This is one of the few places where a little bit of durable
documentation pays for itself even inside an otherwise fully
conversational workflow.

---

## Slide 15 — The no-paper-trail problem

**~6 min**

Now let's be honest about the cost of this whole mode, because I don't
want anyone leaving today thinking conversational development is free.

Chat history is not a durable, reviewable artifact. There's no spec
capturing what problem you were solving. No plan capturing what
approach you chose and why. No test file capturing what "correct"
means. Everything that would normally carry *intent* forward — as
opposed to just the resulting code — lives only in a conversation that
may not even exist anymore by the time anyone needs it.

Play this forward six months. Someone — quite possibly you — is staring
at this code asking "why does this do X instead of the obvious Y?" With
DDD, the spec answers that. With TDD, the test names and assertions
often answer that. With plan-first, the ADR answers that. With
conversational development, the honest answer is: git blame, and a
guess. Or tracking down whoever had the conversation and hoping they
remember it.

This is exactly the tradeoff captured in that comparison table from
Slide 4: conversational development is weak for anything needing a
paper trail, and the artifact it leaves behind is, literally, none.
That's not a flaw to fix — it's the nature of the mode. The question is
what you do about it, which is the next slide.

---

## Slide 16 — Mitigating the paper-trail cost

**~5 min**

You cannot get the durability of a spec for free — if you could, you'd
just be doing DDD with extra steps. But you can buy back a meaningful
chunk of that durability cheaply, without abandoning the conversational
mode itself.

First: write commit messages that explain *why*, not just what changed.
"Handle empty date ranges in CSV export" is what. "Handle empty date
ranges in CSV export — previously returned a 500, which broke the
dashboard's default view before any filter was applied" is why, and it's
maybe fifteen extra seconds to write.

Second: leave a short note — even just a code comment — for any
non-obvious call the agent made that you accepted. If the agent
proposed disabling rather than hiding a button for a good reason, and
you agreed, one sentence in a comment saves the next reader from
wondering if it was an oversight.

Third, and this is the one people forget: if a throwaway conversation
produces something that turns out to matter more than you expected —
promote it. Go back after the fact and write the two-paragraph doc you
skipped at the start. It's not as good as having written it first, but
it's far better than never having it at all, and it only takes a few
minutes once you already know what the code does.

None of this turns conversational development into DDD. It just means
you're not leaving the *entire* cost on the table for whoever reads this
next.

---

## Slide 17 — Lab: rebuild Module 6's feature, conversationally

**~5 min**

Here's the lab, and I think it's one of the more interesting ones in
the course because it's directly comparative.

You're going to rebuild the same feature you built in Module 6's lab —
in this course's worked example, that's the CSV-export-for-reports-
dashboard feature — but this time with no spec doc and no plan doc.
Just talk it into existence, turn by turn, exactly the way we've been
describing all session.

Two ground rules. React to what the agent actually produces and correct
as you go — don't pre-write a giant first message that's secretly a
spec in disguise, because that defeats the point of the exercise. And
let yourself hit at least one real drift moment. Don't over-prepare your
prompts specifically to avoid it. The value of this lab comes from
experiencing drift and practicing the recovery skills from this
session, not from executing a flawless run.

If your first attempt goes suspiciously smoothly with zero corrections,
that's worth noting too — but for most people, on a feature with any
real edge cases, drift will show up somewhere. When it does, that's the
moment to apply what we just covered.

---

## Slide 18 — Lab: what to track

**~4 min**

While you're doing this, keep a running log — it doesn't need to be
fancy, a scratch note file is fine — with five things.

Number of turns to reach a working result. Number of corrections you
had to make, and for each one, classify it: was it a targeted,
incremental correction, or did you end up restating the whole task?
Where drift happened, if it did, and specifically how you caught it —
which signal from Slide 10 tipped you off. Total time spent, including
every correction turn, not just the "productive" ones. And whether you
had to start a fresh session at any point, and why.

This log is what makes the deliverable possible — without it, you'll be
comparing your memory of how it went against a written spec and diff
from Module 6, and memory is exactly the kind of thing this module
warned you not to trust.

---

## Slide 19 — Deliverable

**~4 min**

Your deliverable is a side-by-side comparison against your Module 6
result. Three angles to cover.

Turns and time spent — this mode versus DDD. Be specific with numbers,
not vibes. Quality of the final code — does it actually meet the same
acceptance criteria Module 6's spec defined? Go back and check against
those criteria literally, line by line, not from memory.

And the question I think is most valuable to sit with honestly: would
you trust either result without a review pass? Why or why not? Notice
this question doesn't assume DDD wins. Sometimes the conversational
result is just as trustworthy for a task this size, and the spec was
overhead. Sometimes it's clearly worse. The point of the lab isn't to
prove conversational development is bad — it's to give you real data
about where the line is, on a feature you understand well because
you've now built it twice.

---

## Slide 20 — Recap

**~3 min**

Let's pull the thread back together. Incremental correction: name the
symptom and the boundary, don't restate the whole task — that's the
single highest-leverage habit from today. Agent drift is quiet by
nature; you catch it from the diff and from the running application,
not from the agent's own narration of what it did. Long sessions
degrade in predictable ways, and a short, deliberate recap can beat a
session's own drifted memory of itself. And this whole mode trades away
a paper trail in exchange for speed — that's a legitimate trade, but
only when you make it on purpose, task by task, rather than falling
into it by default.

---

## Slide 21 — Next up

**~2 min**

Next time, Module 11: Multi-Agent Orchestration. Today was about one
person and one agent in a tight loop. That works beautifully at small
scale, but it stops scaling once a task gets big enough that a single
conversational thread can't hold all of it in view — that's exactly
when drift gets worse and correction gets more expensive. Module 11 is
about splitting the work: an implementer and a separate reviewer agent,
or an orchestrator fanning tasks out to several agents at once. Go get
some hands-on time with today's lab, and I'll see you there.
