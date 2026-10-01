# Lecture Script — Module 6: Write It Down First

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd explain it to a smart 15-year-old who's just
figured out that talking to the agent works okay, but not great, and
wants to know why. Total lecture portion should run **~20-25 minutes**;
the rest of the 45-90 minute module is the hands-on task and checkpoint.
Slide numbers below match `slides.md` exactly.

---

## Opening (~2 min)

## Slide 1 — Module 6: Write It Down First

Welcome them in. Something like:

"Last module you learned that the agent only works with what you
actually say — vague requests get vague results, specific requests get
close ones. Today we push that one step further. Because even when
you're being specific, saying it out loud has a habit of leaving stuff
out. Today's whole idea in one sentence: for anything bigger than a
one-liner, write it down before the agent starts, and you'll save more
time than you spend."

## Slide 2 — Agenda

"Here's where we're going. Quick recap of Module 5 so this connects.
Then the big idea itself. Then what actually goes in a one-page plan —
four parts, not a novel. Then we'll work through a real example
together, start to finish. Then it's your turn: write a plan, hand it
to the agent, and nothing else. And we close with a checkpoint that's
honestly the most useful five minutes of today."

*(~3 min total so far)*

---

## The Big Idea (~7-8 min)

## Slide 3 — Recap: Module 5

"Quick reminder of where we left off. The agent only works with what
you actually say — not what you meant, not what seemed obvious to you.
You tested this yourselves last time: same feature, three different
phrasings, three different results.

So here's today's problem, and it's a little sneaky. You can be
specific and *still* leave things out — because when you're talking,
your brain quietly fills gaps as you go, and you don't notice it's
doing that. Writing it down is how you catch it, because paper doesn't
fill gaps for you."

## Slide 4 — The big idea

"Here's the rule: for anything bigger than a quick fix, write down what
you want *before* the agent starts building. Think of it like a short
game design doc, or a one-page project brief. Not a novel — one page.

And here's the part people get backwards: you are not writing this for
the agent's benefit, at least not primarily. You're writing it for
*your own* benefit — to catch your own unclear thinking while it's
still just words on a page, before it turns into actual wrong code that
someone has to undo."

## Slide 5 — Why this actually saves time

"This feels backwards to a lot of people, so let's slow down on it.
Talking it through out loud *feels* efficient — you're moving your
mouth, things are happening, it feels like progress. But that feeling
is misleading. It feels fast because you haven't done the hard part
yet — you haven't actually decided all the edge cases, you've just
skipped past them.

Here's the thing about gaps in your thinking: they're invisible inside
your head. You can hold a fuzzy, half-formed idea in your brain forever
and it never bothers you, because your brain is happy to fill in
whatever's missing without telling you. On paper, that same gap is a
blank space where a sentence should be — and blank spaces are
impossible to miss once you're staring at them.

And the math on when you catch it matters a lot. Fixing a plan costs
you a couple of minutes with a pen, or backspacing a paragraph. Fixing
code that's already built — code the agent wrote based on a gap you
didn't notice — costs way more: rereading it, figuring out what it
actually did, deciding what should change, and redoing the work. This
is what professional teams call **document-driven development** — the
doc is the source of truth, not a conversation everyone half-remembers
an hour later."

*(~11 min total so far)*

---

## The Four Parts (~5 min)

## Slide 6 — The one-page plan: four parts

"So what actually goes on this one page? Four parts. Goal — what this
is supposed to do, in plain language. Not this — what's explicitly out
of scope. How it should behave — the important cases, including the
tricky ones you already know about. And Done means — how you'll
actually know it works. That's it. Four sections, one page. Let's take
them one at a time."

## Slide 7 — Goal + Not this

"Goal is the easy one — one or two sentences, plain language, what
problem this solves and for who. Most people already write something
like this without being told.

Not this is the one people skip, and it's the one that saves you the
most grief. Here's why it matters: agents are built to be 'helpful,'
and helpful sometimes means adding something you didn't ask for,
because it seemed like a natural fit while the agent was in there
building. 'Not this' is how you say no *in advance*, instead of finding
out after the fact that it redesigned something you never asked it to
touch."

## Slide 8 — How it should behave

"This section is the edge cases — but I want to be precise about what
kind. Not a brainstorm where you sit and try to invent every possible
weird scenario. Just the stuff that's *already* sitting in your head
right now, that you'd feel dumb about later if you didn't write down.

Three questions that surface most of it: what happens with zero of
something, or way too many? What happens the *second* time something
happens, not just the first? And what should definitely never happen,
no matter what?

You already thought of these — that's the whole point. Writing them
down costs about ten seconds each. Not writing them down costs a whole
debugging session later, when the agent built something reasonable that
just wasn't what you actually needed."

## Slide 9 — Done means

"Last section: Done means. How do *you* — not the agent, you — check
that this actually works, without just eyeballing the result and
hoping it's fine?

The bar here is concrete and checkable, not vibes. 'Looks right' is not
a done-means — it's not testable by anyone including you next week.
'Buying the upgrade twice is not possible' — that's a done-means. You
can literally go try it and get a yes or no answer.

Here's why the order matters: this section is what you'll test the
agent's actual result against at the end. So you write it *before* you
see any code — otherwise you'll unconsciously grade the code you got
instead of the plan you actually wanted."

*(~16 min total so far)*

---

## Worked Example (~4-5 min)

## Slide 10 — Worked example: an upgrade shop

"Let's make this real with an example: a shop screen in a small game
where the player spends coins on upgrades. Here's the Goal and Not
this section, written out.

Goal: let the player spend coins earned in-game to buy one of three
upgrades — extra life, speed boost, double points — from a shop screen
opened from the pause menu.

Not this: no real-money purchases, can't sell upgrades back, no new
upgrade types beyond these three, and — this one's easy to forget —
don't redesign the pause menu itself just because you're touching it.

Notice how specific 'Not this' is. It's not vague caution, it's four
concrete doors closed in advance."

## Slide 11 — Worked example, continued

"Now How it should behave and Done means for the same feature.

How it should behave: not enough coins — buy button is disabled and
shows how many more coins are needed. Already own an upgrade — shows
'Owned' instead of a price, can't buy it again. Buying an upgrade
removes the coins immediately. Closing and reopening the game keeps
owned upgrades owned — that last one is the kind of thing you'd
absolutely forget to say out loud, and absolutely notice was missing
the moment you relaunched the game and lost everything.

Done means: can buy each upgrade when I have enough coins. Can't buy
one when I'm short, and the button is disabled, not silently broken.
Coins and owned upgrades survive a restart.

And here's the detail I want you to notice: there is not one line of
code anywhere in this plan. It's still entirely decisions — what should
happen, not how it gets built. That's exactly right for this stage."

*(~21 min total so far)*

---

## Handing Off to the Hands-On Task (~2-3 min)

## Slide 12 — Hands-on task

"Your turn. Four steps. Pick a real feature from your own project —
one where you can already picture at least one tricky edge case, don't
pick something trivially simple or this exercise won't teach you
anything. Write your one-page plan: Goal, Not this, How it should
behave, Done means. Give the agent *only* the plan — no extra verbal
explanation, no filling in gaps out loud while it works. Then check
what it built against your Done means section."

## Slide 13 — Why "only the plan"

"I want to flag this because it's the part people are most tempted to
cheat on. If you hand over the plan and then keep narrating extra
context while the agent works — 'oh also make sure it does this,' 'oh
wait I meant this other thing' — you will never find out where your
*plan itself* actually had a gap. You'll have patched it live with your
voice instead, and the plan will look better than it actually was.

The whole point of this exercise is to expose your plan's blind spots.
So let it stand on its own, even when it's tempting to jump in and
help."

*(~24 min total so far — hands-on task happens now, live, not scripted
here)*

---

## Checkpoint and Wrap-Up (~2-3 min, after hands-on is done)

## Slide 14 — Checkpoint

"When the hands-on is done, here's your checkpoint, and do it for
real — write it down, don't just think it. Two questions: what did the
agent get right, straight from the plan alone, with zero extra help
from you? And: what did you have to go back and add — because you'd
left something out, or the agent guessed wrong about something you
never specified?

That second list — the stuff you had to add — is the real deliverable
today. It's not a failure of the exercise. It's literal proof of what
your plan was worth, and exactly what to do better next time you write
one."

## Slide 15 — Recap + next up

"Let's lock in today. A plan is four short sections, not an essay —
Goal, Not this, How it should behave, Done means. 'Not this' and 'Done
means' are the two sections everyone's tempted to skip, and they're the
two that save the most time down the line. Writing it down catches
*your* gaps before they turn into someone's bugs.

Next time, Module 7: Keep It Looking Consistent. Same core move,
applied to design — writing down colors, fonts, and spacing so the
agent stops guessing differently every single session."

---

*(Total lecture time: roughly 24-26 minutes as scripted, leaving the
remainder of the 45-90 minute module for the hands-on task and
checkpoint conversation.)*
