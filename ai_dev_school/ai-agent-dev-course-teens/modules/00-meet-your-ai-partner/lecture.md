# Lecture Script — Module 0: Meet Your AI Coding Partner

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd explain it to a smart 15-year-old who's a little
skeptical that this is anything more than a fancy autocomplete. Total
lecture portion should run **~20-25 minutes**; the rest of the 45-90
minute module is the hands-on task and checkpoint. Slide numbers below
match `slides.md` exactly.

---

## Opening (~1 min)

## Slide 1 — Meet Your AI Coding Partner

Welcome them in. Something like:

"Today we're starting the thing this whole course is built around: you,
directing an actual AI coding agent, to build actual things. Before we
touch the keyboard, I want fifteen-ish minutes to make sure we have the
same honest picture of what this tool actually is — because if you walk
in thinking it's magic, you're going to get surprised later, and not in
a good way. If you walk in thinking it's a glorified autocomplete,
you're going to undersell what it can do and get frustrated when you
try to use it like one. Neither of those is right."

---

## Slide 2 — Today

"Quick roadmap. We'll bust two wrong mental models, land on the right
one, talk about what this thing can actually do and what it needs from
you to do it well, walk through one concrete example together, and then
you're doing it yourself — one tiny task, on your own machine, in your
own sandboxed folder. Then a short reflection where you explain back to
me what actually happened. That last part matters more than it sounds
like it should — we'll get to why."

*(~4 min total so far)*

---

## The Big Idea (~6-7 min)

## Slide 3 — Myth #1: It's Not Autocomplete

"First wrong model: 'it's just autocomplete, like when your phone
guesses the next word in a text.' I get why people think this — it *is*
built on the same underlying kind of model, predicting text. But here's
the difference that actually matters: autocomplete predicts one word at
a time and stops. It has no idea what your sentence means, it's not
tracking a goal, and it definitely isn't going to go open your camera
roll and pick a photo for you.

An agent reads your *entire* request, figures out a plan that might have
several steps, and then goes and *does things* — for real, on your
actual computer. Creates files. Runs programs. That's a completely
different category of thing from 'guess the next word.'"

## Slide 4 — Myth #2: It's Not Magic

"Second wrong model, and this one's just as common: 'it's magic, I ask
for a thing and it appears, don't ask questions.' This is the more
dangerous myth, honestly, because it means when something goes wrong —
and it will — you won't know where to even start looking, and you won't
notice smaller things going wrong until they've piled up.

Here's the truth: there is no mystery box. Every single thing the agent
does is one specific, visible action — read this file, write that file,
run this command, check whether it worked. You are going to *watch*
those actions happen, one at a time, later today. Nothing about this is
hidden from you unless you stop paying attention."

## Slide 5 — So What Is It?

"So if it's not autocomplete and it's not magic, what is it? Here's the
one sentence I want you to actually remember from today:

**It's a partner that can take real actions in a loop, until it thinks
the task is done.**

Four things it can actually do: read your files, write new code, run
commands, and check whether what it did worked. That last one — check —
is honestly the most important and the most underrated. It's not just
firing off actions blind. It looks at what happened and adjusts. That
loop is what separates it from a search engine, which just hands you
information, or a chatbot, which just talks to you. This thing acts."

## Slide 6 — The Loop, One More Time

"Let's slow that loop down: read, write, run, check. Read — it looks at
what's already there before touching anything. Write — it makes a
change. Run — it actually executes that change, a script, a command,
whatever the task needs. Check — did that actually do what it was
supposed to? And then, if not done, it goes around again. This can
happen many times for one request you typed once. It is *not* one big
leap from your sentence straight to a finished result — it's this loop,
repeated, usually invisible to you unless you're watching closely,
which — starting today — you are."

*(~11 min total so far)*

---

## What It Needs From You (~5-6 min)

## Slide 7 — It Only Does What You Tell It

"Now — the flip side of 'it can take real actions' is that it needs
direction, same as any partner you'd hand real work to. Two categories
here. Explicit instruction: you say 'create a file called hello.txt,'
it does exactly that. Reasonable inference: you didn't specify every
tiny detail — say, exactly where in the folder to put it — so it fills
that gap with a sensible default. That's normal and fine.

What it should *not* do is invent a task you never asked for. If you ask
it to create one file and it starts restructuring your whole project,
that's not 'helpful initiative,' that's a problem — and it's exactly the
kind of thing your supervisor is going to be spot-checking for as this
course goes on. This entire course, all thirteen modules, is really
about getting good at that first category — telling it clearly enough
that it doesn't have to guess."

## Slide 8 — Same Partner, Real Boundaries

"Because it can take real actions, it needs real boundaries — same as
you wouldn't hand a friend your car keys with zero ground rules the
first time they drive. Claude Code is going to ask your permission
before it does things like editing a file or running a command. You're
about to see this firsthand in a few minutes.

I want to be really clear about something: that permission prompt is
not the tool being slow or annoying. That is the boundary *working
exactly as designed.* Later in this course, once you and your
supervisor have built up trust in how it behaves, you'll relax some of
those permissions for specific, well-understood situations. Today is
not that day — today we want to see every single prompt."

*(~16-17 min total so far)*

---

## Concrete Example (~4-5 min)

## Slide 9 — Example: "Create hello.txt"

"Let's make this concrete before you do it yourselves. Imagine you type
this exact request: 'Create a file called hello.txt with a short
message in it.'

Before I show you the next slide — actually think about it for a second.
What do you *expect* to see happen, step by step? Don't just say 'it
makes the file.' What's the order of events, in as much detail as you
can guess?"

*(Pause for a few answers if this is a live group — even a solo learner
should pause and actually think before continuing.)*

## Slide 10 — What Actually Happens

"Here's roughly what you'll see. One — the agent tells you what it's
about to do, in plain language, before doing it. Two — it asks your
permission specifically to create that file. Three — you approve it.
Four — it actually writes the file. Five — often, it'll check its own
work, like reading the file back to confirm it's really there with the
right content.

Notice what's *not* on this list: nothing silent, nothing skipped,
nothing where it just decides on its own that it doesn't need to ask.
Every step is something you can see and, before step three, something
you can say no to."

*(~21-22 min total so far)*

---

## Handing Off to the Hands-On Task (~3 min)

## Slide 11 — Your Turn: Hands-On

"Okay — that's the concept. Now it's your turn to actually do it. Five
steps: confirm your sandboxed project folder is set up — if you haven't
done that with your supervisor yet, stop here and do that first, don't
skip it. Open Claude Code in that folder. Ask for one tiny, safe,
reversible thing — the hello.txt example works great, or anything
similarly small and low-stakes. Read what it says it's about to do
*before* you approve anything — don't just reflexively hit yes. And
once it's done, actually go look at the real file it created. Open it.
Don't take its word for it."

## Slide 12 — Then Ask It About Itself

"One more thing once that's done, and don't skip this part — it's
arguably more important than the file itself. Ask it directly: 'What
tools do you have access to in this session, and what would you need my
permission for?'

Then compare what it tells you to what you actually just watched happen.
Did it match? Did it mention something you didn't see, or leave out
something you did see? That comparison is exactly the kind of
noticing this whole course is trying to build in you."

*(~25-26 min total so far — hands-on task happens now, live, not
scripted here)*

---

## Checkpoint and Wrap-Up (~2-3 min, after hands-on is done)

## Slide 13 — Checkpoint

"When you're done with the task, here's your checkpoint — and I mean
actually do this, out loud or in writing, don't skip to the next thing.
Two questions: What did the agent actually *do*, step by step, to
complete the task? And: what's one thing it needed your permission for,
and why do you think that boundary exists?

If the honest answer to the first question is 'it just did it' — that's
not a pass, that's a signal. It means you weren't watching closely
enough, and the fix is easy: go back and re-watch the session. You're
not being graded on the file. You're being checked on whether you
noticed the steps."

## Slide 14 — Recap

"Let's lock in the big things from today. Not autocomplete, not magic —
a partner that takes real, visible actions. The loop: read, write, run,
check. It does what you tell it, or reasonably infers — nothing more,
nothing invented. And the permission prompts you saw aren't friction,
they're the boundary doing its job."

## Slide 15 — Next Up

"Next time, Module 1, we go one level deeper into that loop. You're
going to give it a small task with *multiple* steps, and your job is to
log every single action it takes, in order — a full play-by-play, like
you're a sports commentator for what your AI partner is doing. Today
you watched one small loop. Next time you're going to get good at
tracking a longer one."

---

*(Total lecture time: roughly 25-28 minutes as scripted, leaving the
remainder of the 45-90 minute module for the hands-on task and
checkpoint conversation.)*
