# Lecture Script — Module 10: Just Talk It Through

Facilitator notes: this is a spoken script, not a script to read word for
word. This module is lighter than most — it's a comparison exercise, not
a new mechanic — so keep the lecture tight and let the hands-on task do
most of the teaching. Total lecture portion should run **~20-25
minutes**; the rest of the module is the hands-on rebuild and the
checkpoint conversation comparing it to Module 6. Slide numbers below
match `slides.md` exactly.

---

## Opening (~1 min)

## Slide 1 — Just Talk It Through

Welcome them in. Something like:

"Last time, in Module 6, you learned to write a one-page plan before
letting the agent touch any code — goal, not-this, how it should behave,
done means. That was real, useful discipline, and I don't want you to
un-learn it today. But today we're doing the opposite on purpose: no
plan, no doc, just talking it through out loud, step by step. By the end
you're going to have done the same kind of task both ways, and you'll be
in a much better position to judge which one a given task actually
needs."

---

## Slide 2 — Today

"Here's the shape of today. Quick rewind on what the written-plan
approach actually bought you in Module 6. Then the big idea: not
everything needs that upfront doc. Then when talking it through wins,
and — just as important — when it doesn't. Then you rebuild something
small from Module 6, this time purely conversationally. And we wrap with
a checkpoint where you compare the two attempts head to head."

*(~3 min total so far)*

---

## Quick Rewind (~3-4 min)

## Slide 3 — Quick Rewind: Module 6

"Quick memory check. In Module 6, before the agent wrote a single line,
you wrote a plan with four parts: the goal in plain language, what's
explicitly *not* in scope, how it should behave including the tricky
cases you already knew about, and how you'd know it was actually done.

That plan did real work. It caught unclear thinking in *your* head
before it turned into wrong code in the agent's output. That's a genuine
win. But be honest with yourselves for a second — writing that page also
took actual minutes you spent before any code existed at all. For a big,
important feature, that trade is obviously worth it. Today we're asking:
is it *always* worth it?"

*(~7 min total so far)*

---

## The Big Idea (~6-7 min)

## Slide 4 — The Big Idea

"Here's the one sentence I want you to walk away with today: **not
everything needs a written plan.** For small stuff, or for something
you're still exploring and don't fully have a shape for yet, just
talking it through step by step — and correcting the moment you notice
it drifting — is faster than stopping to write a doc first.

I want to be careful here, because it would be easy to hear this as 'the
plan was pointless, forget Module 6.' That's not it at all. The plan
isn't the point — it never was. Getting a good result, efficiently, is
the point. The plan is one tool for getting there. Today you're learning
a second tool, and just as importantly, learning to feel *which one a
given moment is asking for.* That judgment call is its own skill, and
it's one senior engineers make dozens of times a day without even
noticing they're making it."

## Slide 5 — When Talking It Through Wins

"So when does the conversational approach actually win? A few signals.
The task is small enough you could describe the whole thing in one
sentence. You genuinely don't know what you want yet, and you're
planning to figure it out by looking at what comes back and reacting.
It's disposable — a quick experiment, a throwaway script, something you
won't look at again next week. And critically: you're actually there,
paying attention, able to notice drift the second it happens and correct
it immediately. That last one matters — this approach leans on your
attention *replacing* the plan, not on nobody watching."

## Slide 6 — When a Written Plan Still Wins

"And the flip side, because this is just as important. A written plan
still wins when the task is big, or when you can already picture the
tricky edge cases before you start — that's exactly the kind of thing
that's easy to forget mid-conversation but hard to leave out of a
written 'how it should behave' section. It wins when you're going to
keep working on this for weeks or months, because a plan is something
you can come back to. It wins when you *won't* be sitting there the
whole time to catch drift in real time. And it wins when someone else —
a teammate, your future self in three months — needs to understand *why*
you built it this way, not just what it does. A conversation evaporates.
A doc doesn't."

*(~14 min total so far)*

---

## Setting Up the Hands-On (~4-5 min)

## Slide 7 — What "Purely Conversational" Means

"Let's get concrete about what you're actually going to do, because
'just talk it through' can sound vague. It means: no written plan, no
doc, no spec you write before starting. Instead — back-and-forth. You
ask for a piece, you look at what comes back, you react, you adjust,
you ask for the next piece. The moment you notice something drifting
away from what you actually wanted, you say so immediately — you don't
wait and hope it self-corrects.

I want to push back on one misconception before you start: this is not
'be lazier' or 'put in less thought.' It's still deliberate. You're
still making every decision a plan would have made — you're just making
them out loud, one at a time, instead of all upfront on paper."

## Slide 8 — Your Turn: Hands-On

"Here's the task, three steps. One — pick a small feature, ideally
similar in size and shape to the one you built back in Module 6, so the
comparison is fair. Two — build it purely conversationally this time:
no written plan. Three — talk it out step by step, and when you notice
things drifting from what you want, correct direction right there in
the conversation instead of pushing through."

## Slide 9 — While You Work

"Two things to actually do while you're working, not just at the end.
Keep a rough count — doesn't have to be exact — of how many messages or
turns it took you to get to a result you're happy with. And notice, in
the moment, every time you have to say something like 'actually, not
like that.' Don't treat that as a failure or a sign you're doing it
wrong — that correcting-as-you-go *is* the mechanism this whole approach
runs on. If you never had to correct anything, that's worth noticing
too."

*(~19 min total so far)*

---

## Checkpoint and Wrap-Up (~4-5 min, after hands-on is done)

## Slide 10 — Checkpoint

"Once you've got a result, here's the comparison — and do this one for
real, don't skip to the next module. Which approach took more effort
overall, counting the time you spent writing the Module 6 plan against
the back-and-forth you just did? And which result would you actually
trust more if you were going to keep working on it for months? Which one
was perfectly fine because the thing was quick and disposable anyway?
There's no 'correct' answer the class is supposed to converge on here —
different features will genuinely point different directions."

## Slide 11 — The "Should've Written This Down" Moment

"One more thing to look for, and it's the subtlest part of today. Some
tasks start out feeling small and conversational, and then quietly grow
mid-session — a couple more requirements show up, an edge case you
didn't think of appears, and suddenly you're deep in a conversation that
probably should have been a plan from the start. Did that happen to you?
Was there a specific point where you felt it? Learning to notice that
feeling *as it's happening*, not in hindsight, is honestly the real
skill this module is trying to build — more than the rebuild itself."

## Slide 12 — Recap

"Let's lock in today. Not everything needs a written plan — small or
exploratory work often doesn't. Talking it through is faster and more
flexible, but it needs you actually paying attention to catch drift.
Writing it down costs more upfront but pays off on bigger or
longer-lived work. And the actual skill isn't picking one of these
forever — it's choosing correctly, task by task, and today gave you a
direct before-and-after to calibrate that judgment against."

## Slide 13 — Next Up

"Next time, Module 11: Two Heads Are Better. You've been building things
solo with your agent this whole course. Next module, a second, fresh
agent — one that had no part in building your code — checks the work.
Think of it like swapping papers with a classmate before you turn an
assignment in: a second set of eyes catches things the person who wrote
it stopped being able to see."

---

*(Total lecture time: roughly 22-24 minutes as scripted, leaving the
remainder of the module for the hands-on rebuild and the Module 6
comparison checkpoint.)*
