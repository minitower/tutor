# Lecture Script — Module 5: Instructions That Actually Work

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd explain it to a smart 15-year-old who's already
sat through Module 0 and 1 and is starting to get comfortable with the
tool — comfortable enough that they're tempted to get lazy with what they
type. Total lecture portion should run **~20-25 minutes**; the rest of
the 45-90 minute module is the hands-on task and checkpoint. Slide
numbers below match `slides.md` exactly.

---

## Opening (~1 min)

## Slide 1 — Instructions That Actually Work

Welcome them back in. Something like:

"Last time you watched the agent work in a loop — read, write, run,
check — on one small task, and you logged every step of it. Today we're
going up one level: before that loop even starts, something has to
trigger it. That something is what you typed. Today's whole module is
about the fact that what you typed and what you meant are not always
the same thing — and the agent only ever sees the first one."

---

## Slide 2 — Today

"Here's the plan. Quick recap of the loop from last time. Then the big
idea for today, in one line. Then we're going to take one single
feature and ask for it three different ways — vague, specific, very
specific — and look hard at what changes. Then you do the same
experiment yourselves, on your own project. Then a checkpoint where you
figure out which version actually worked and, more importantly, *why*."

*(~3 min total so far)*

---

## The Big Idea (~6-7 min)

## Slide 3 — Last Time: The Loop

"Quick refresher. The agent doesn't leap straight from your request to
a finished result. It works in a loop — think, act, check, think again
— and when something goes wrong, you can always trace it back to one
specific step in that loop. That's what you were logging last time.

Today's question is different, though. It's not 'what happens inside
the loop' — it's 'what happens *before* the loop even starts?' Because
something has to kick it off, and that something is entirely up to
you."

## Slide 4 — The Agent Can't Read Your Mind

"Here's the thing that's easy to forget once you've used this tool a
few times and it starts feeling like it 'gets you': it can only work
with what you actually say. It doesn't know your taste, it doesn't know
what you pictured in your head, it doesn't know what 'good' looks like
to you unless you've told it.

Take a phrase like 'make it better.' Ask ten different people what that
means and you'll get ten different answers. Ask the agent the same
vague thing twice, in two different sessions, and you might get two
different answers *from the same model* — because with nothing concrete
to anchor on, it's filling in the blanks itself, and there's more than
one reasonable way to fill them.

So here's the rule, plain and simple: vague ask, the agent guesses.
Clear ask, the agent builds what you actually meant. Everything today
is about that one line."

## Slide 5 — The Highest-Leverage Skill Here

"I want to slow down on this slide because it matters more than it
looks like it should. Of everything in this entire course, getting good
at *this* — at saying clearly what you want — is the single
highest-leverage skill you'll build. It's not tied to one module. Every
module after today gets easier once you're good at this, because you'll
spend less time getting things you didn't ask for.

And here's the part that surprises people: the gap between 'what I
meant' and 'what I typed' is where most bad results come from. Not
because the agent is bad at coding — it usually isn't. It's because it
built exactly what you said, and what you said wasn't quite what you
meant. That's a you-and-your-words problem, not an it-can't-code
problem, and the good news is that's a completely fixable problem."

*(~10 min total so far)*

---

## The Experiment (~7-8 min)

## Slide 6 — Let's Test This: One Feature, Three Ways

"Let's stop talking about this abstractly and actually test it. Same
feature, asked for three different times, at three different levels of
detail. And here's the important condition: each version runs in its
own fresh session — no shared history, no memory of the earlier
attempts. Otherwise we're not testing what our words produce, we're
testing what the agent remembers, which is a different experiment
entirely.

The feature we'll use as our example: add a leaderboard."

## Slide 7 — Version 1: Vague

"Version one, as vague as a real request often actually is:
'Add a leaderboard.'

Think about everything that's *not* in that sentence. How many scores
should it show? Sorted which way — highest first, most recent first,
something else? Where on the page does it even go? None of that is
specified, so the agent has to guess at all three. Not because it's
careless — there's simply nothing in the request to tell it otherwise."

## Slide 8 — Version 2: Specific

"Version two, more specific:
'Add a leaderboard showing the top 5 scores, sorted highest first.'

Now two of those questions are answered — how many, and what order.
That's real progress. But notice what's still open: what happens on a
tie? What if the player has fewer than 5 scores total? And where in the
layout does this actually live? Being specific about *some* things
doesn't mean you've been specific about *all* things — this version
still leaves real gaps."

## Slide 9 — Version 3: Very Specific

"Version three, very specific:
'...top 5 scores, sorted highest first. Ties break by earliest
achieved. Fewer than 5 scores: show what exists, no placeholders. Place
it in the sidebar, below the score display.'

Now look at what's covered: the tie-break rule is explicit. The
fewer-than-5 case is explicit — no fake placeholder rows pretending
there are scores that don't exist. And the placement is explicit, down
to which panel and where in it. Every genuine ambiguity from version
one has been closed off, one at a time."

## Slide 10 — Same Feature, Three Results

"Here's the same information as a table, side by side. Count and order
— guessed in version one, defined from version two onward. Ties —
guessed in both one and two, only defined in version three. Fewer than
5 scores — same pattern. Placement — same pattern again.

The takeaway printed at the bottom is the whole lesson in one line:
more detail equals fewer guesses equals fewer surprises. That's not a
coincidence and it's not specific to leaderboards — it's just how this
works, for any feature."

*(~18 min total so far)*

---

## What Makes Detail Useful (~3-4 min)

## Slide 11 — What Makes an Instruction Specific

"So if 'be specific' is the goal, what does that actually mean in
practice? Four categories worth knowing by name, because once you have
the names you'll notice the gaps faster. Quantity — how many, how much.
Order — sorted how, prioritized how. Edge cases — what happens when
it's empty, when there's a tie, when there's overflow, the very first
time it runs with no data at all. And location — where it lives, where
it shows up.

One important caveat, though: you do not need to spell out everything.
Nobody writes a spec that covers every conceivable detail — that's
exhausting and mostly wasted effort. You only need to nail down what
you actually care about. If you genuinely don't care whether ties break
by name or by timestamp, don't waste words on it — let the agent make
a reasonable call. The skill isn't 'be maximally detailed.' It's 'be
detailed about the things that would bug you if they came out wrong.'"

*(~21-22 min total so far)*

---

## Handing Off to the Hands-On Task (~2-3 min)

## Slide 12 — Your Turn: Hands-On

"Now you run the same experiment on your own project. Four steps. Pick
one small feature — something roughly leaderboard-sized, not something
huge. Write three versions of the request: vague, specific, very
specific — same feature each time, just more detail added at each
step. Run each one in its own separate, fresh session. And then compare
the three results side by side, the same way we just did with the
leaderboard example."

## Slide 13 — Keep the Sessions Honest

"One rule that makes or breaks this experiment: fresh session means the
agent has no memory of your earlier attempts. If you run version one,
then just keep chatting in that same session for version two, the
agent already half-knows what you wanted from the first round — you're
no longer testing your wording, you're testing its memory, and you'll
get a misleading result.

So: write all three prompts down *before* you run any of them. Get them
locked in on paper or in a doc first. That way you're not tempted to
quietly improve version two just because version one's session is
still open in front of you."

*(~25 min total so far — hands-on task happens now, live, not scripted
here)*

---

## Checkpoint and Wrap-Up (~2-3 min, after hands-on is done)

## Slide 14 — Checkpoint

"Once you've run all three and looked at the results, here's your
checkpoint. Three questions, and I want real answers, not 'the last one
was best' and moving on. Which version got closest to what you actually
wanted, on the first try? Was there a point where adding *more* detail
stopped helping — where version three didn't really improve on version
two? And: what was still left for the agent to reasonably decide on its
own, even in your most detailed version?

That third question matters because 'very specific' doesn't mean
'zero decisions left for the agent' — it means the decisions that were
left were ones you were actually fine with it making."

## Slide 15 — Recap

"Let's lock in today's big things. The agent works with what you say,
not with what you meant — those are two different things and only one
of them is visible to it. Vague gets you guesses. Specific gets you
fewer guesses and a result closer to what you pictured. And this isn't
just an AI-agent skill — it's the exact same muscle as writing a clear
bug report, or clear instructions for a group project. You're not
learning a trick for this tool. You're learning a way of communicating
that pays off everywhere."

## Slide 16 — Next Up

"Next time, Module 6: Write It Down First. Today was about getting one
request right. Next time we go up a level — for anything bigger than a
one-liner, you're going to write a short plan *before* the agent starts
building anything. And then, once it's built, you'll look back at that
plan and see exactly what you had to fix once you actually saw the
thing exist. That's the next layer of this same skill."

---

*(Total lecture time: roughly 22-25 minutes as scripted, leaving the
remainder of the 45-90 minute module for the hands-on task and
checkpoint conversation.)*
