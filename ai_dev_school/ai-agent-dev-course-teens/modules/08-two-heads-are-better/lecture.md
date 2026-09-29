# Lecture Script — Module 8: Two Heads Are Better

Facilitator notes: this is a spoken script, not a script to read word for
word. This module introduces one clean mechanic — a second, uninvolved
agent reviewing the first agent's work — so keep the lecture focused and
let the hands-on task carry the rest of the teaching. Total lecture
portion should run **~20-25 minutes**; the rest of the 45-90 minute
module is the hands-on build-then-review task and the checkpoint
conversation. Slide numbers below match `slides.md` exactly.

---

## Opening (~1-2 min)

## Slide 1 — Two Heads Are Better

Welcome them in. Something like:

"Every module so far, you've been working with one agent, solo, on one
task at a time. Today that changes a little. You're going to build
something with one agent, and then bring in a second, completely
different agent — one that had no part in building it — to check the
work. By the end of today you'll know exactly why that second, fresh set
of eyes catches things the first agent, and even you, walked right past."

---

## Slide 2 — Today

"Here's the shape of today. Quick rewind on something you already know
from doing this course solo. Then the actual problem we're solving: why
the agent that built something is bad at spotting its own mistakes. Then
the big idea and exactly what 'fresh' has to mean for this to work. Then
you do it yourself — build, then review with a brand new session. And we
close with a checkpoint comparing what the reviewer caught against what
you and the builder missed."

*(~3 min total so far)*

---

## The Problem (~5-6 min)

## Slide 3 — The Problem: Builder Bias

"Let's name the actual problem before we fix it. When an agent builds
something, it tends to assume its own choices were reasonable — because
it made them. It 'knows what it meant' by that variable name, that
shortcut, that assumption about the input. It's not being dishonest.
It's just standing too close to its own work to see it clearly.

And before you think this is some AI-specific quirk — it isn't. You do
this too, with your own writing, your own code, your own anything.
You've re-read your own essay five times and missed the same typo five
times, and then handed it to a friend who caught it in ten seconds. Same
mechanism. Closeness creates blindness. That's true whether the thing
doing the writing is you or an agent."

## Slide 4 — The Classroom Analogy

"Which is exactly why teachers make you swap papers before you turn
things in. You've probably done this: trade with the person next to you,
read theirs, they read yours, mark anything that looks off. It works
because the person reading your paper wasn't in your head while you
wrote it. They don't know what you *meant* — they only see what's
actually on the page. That gap between what you meant and what you
actually wrote is exactly where mistakes hide, and it's exactly what a
fresh reader exposes.

Today, an AI reviewer plays the role of that classmate."

*(~9 min total so far)*

---

## The Big Idea (~5-6 min)

## Slide 5 — The Big Idea

"Here's the sentence I want you to remember: **a second, completely
fresh agent — one that didn't build it and doesn't know the first
agent's reasoning — can review the work with genuinely fresh eyes.**

Two words are doing all the work in that sentence: 'completely fresh.'
Fresh means no memory of the build process and no access to the
builder's explanations. It gets the result, and it gets the original
task you asked for. That's it. Nothing else."

## Slide 6 — Why It Matters

"Why does that restriction matter so much? Because the builder agent —
same as you, same as anyone — tends to assume its own choices were
reasonable. It's not going to flag its own assumption as questionable,
because from the inside, it doesn't look like an assumption — it looks
like just how things are. A fresh session was never inside that
assumption in the first place. It has nothing to defend, nothing it
already decided was fine. That's not the fresh agent being smarter. It's
the fresh agent having zero investment in the first agent having been
right."

*(~15 min total so far)*

---

## Making "Fresh" Actually Work (~6-7 min)

## Slide 7 — What "Fresh" Actually Means

"Let's get precise, because it's easy to fake this without meaning to.
Fresh means a brand new session — not scrolling up in the same chat, not
saying 'okay now review what you just did.' A genuinely separate
session, with no memory of the first one.

And it only gets two things: the diff or the result, and the original
task. It does *not* get 'here's how I built it' or 'here's why I made
this choice here.' The moment you hand the reviewer the builder's
explanation for a weird decision, you've told it that decision was
already thought through — and it'll believe you instead of checking for
itself. That's the whole trick undone in one sentence."

## Slide 8 — This Is Real Code Review

"I want you to know this isn't a classroom invention — this is exactly
how real software teams operate. Nobody on a real engineering team
merges their own pull request without someone else looking at it first.
And crucially, that second engineer reviews the *diff* — they don't sit
there while the first engineer narrates every decision out loud. They
read it cold, the same way your reviewer session is about to.

Today, an AI reviewer is standing in for that second engineer. Same
mechanic, same reason it works: distance catches what closeness misses.
This is a professional habit you're building on day one, not a toy
exercise."

*(~22 min total so far)*

---

## Setting Up the Hands-On (~3-4 min)

## Slide 9 — The Setup: Two Sessions, One Task

"Here's the shape of what you're about to do. Session A — your regular
session — builds a moderately-sized feature, same as you've done all
course. Session B is a completely new session that had zero part in
building it. Session B gets only the diff or result, plus the original
task you gave Session A. Two sessions, one task, one clean handoff."

## Slide 10 — What NOT to Hand the Reviewer

"This slide might be the most important one today, honestly. Do not
hand the reviewer the builder's reasoning. Not 'here's what I was trying
to do in this part,' not an explanation of a weird-looking choice,
nothing. Just the task, and the finished result. Any of that other
context is exactly what would let the reviewer's judgment get anchored
to the builder's — and the second it's anchored, it's not fresh anymore,
it's just an echo."

## Slide 11 — What to Ask the Reviewer

"When you hand it over, keep the ask simple: 'Here's the original task
and the resulting code. Does this actually do what was asked? Is
anything missing, wrong, or off?' Let it actually look — don't steer it
toward specific lines or concerns you already have, or you're just
telling it what to find instead of letting it find something. And if it
comes back with a quick 'looks good' — don't accept that as a pass. Push
it: what specifically did you check? A real review has specifics behind
it."

*(~28 min — trimming pace here to land total lecture near 20-25 min;
compress Slides 7-8 if running long)*

---

## Handing Off to the Hands-On Task (~2 min)

## Slide 12 — Your Turn: Hands-On

"Okay, your turn. Four steps: build a moderately-sized feature in one
session. Start a genuinely brand new session with no memory of the
first. Give it only the diff or result and the original task — nothing
from the builder's explanation. Ask it to review: does this do what was
asked, and is anything missing, wrong, or off?"

## Slide 13 — While You Compare

"While you're working through this, two habits. Read the reviewer's
findings before you decide whether you agree with them — don't dismiss
something just because it wasn't on your radar. And for each thing it
flags, sort it: is this a real issue, a nitpick, or is the reviewer
actually wrong here? Then go back to the builder session and tell it
what the reviewer found — does it agree, or does it push back? That
exchange is often where the most interesting learning happens today."

*(~24-25 min total so far — hands-on task happens now, live, not
scripted here)*

---

## Checkpoint and Wrap-Up (~3 min, after hands-on is done)

## Slide 14 — Checkpoint

"Here's your checkpoint, and actually do this one, don't skim past it.
What did the reviewer session catch that you and the builder session
both missed? And if it caught nothing at all — sit with that for a
second before you celebrate. Was the work genuinely solid, or was the
review not looking hard enough? How would you even tell those two apart?
A real answer to that last question means going back and checking
whether the reviewer actually exercised any edge cases, or just skimmed
and said it looked fine."

## Slide 15 — Recap

"Let's lock in today. The agent that built something is biased toward
its own choices — it can't help that, same as you can't fully see your
own typos. A fresh, uninvolved session reviews with none of that bias.
The trick only works if you give the reviewer the result and the task —
never the builder's reasoning. And this isn't a course gimmick — it's
exactly how code review works on real software teams, with an AI
reviewer standing in for the second engineer."

## Slide 16 — Next Up

"Next time, Module 9: Don't Trust Blindly. Today you learned that a
fresh reviewer catches things the builder can't see. Next module is the
uncomfortable follow-up: agents — including your reviewer — can sound
completely confident while still being wrong, missing an edge case, or
technically passing without being correct. And there's a sharper edge to
it too: if an agent reads something written by someone else, that
content can carry instructions aimed at tricking the agent, not you.
You're going to learn to catch both."

---

*(Total lecture time: roughly 22-25 minutes as scripted, leaving the
remainder of the module for the hands-on build-and-review task and the
checkpoint conversation.)*
