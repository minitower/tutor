# Lecture Script — Module 1: How the Agent Thinks: The Loop

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd explain it to a smart 15-year-old who already
believes this thing isn't magic, but hasn't yet had to actually watch it
work through a multi-step task. Total lecture portion should run
**~20-25 minutes**; the rest of the 45-90 minute module is the hands-on
task and checkpoint. Slide numbers below match `slides.md` exactly.

---

## Opening (~1 min)

## Slide 1 — How the Agent Thinks: The Loop

Welcome them back. Something like:

"Last time you watched an agent do one small, tiny thing — create a
file — and you saw it happen step by step. Today we go one level
deeper. Real tasks aren't one step, they're a chain of steps, and by the
end of today you're going to be able to narrate that chain like a sports
commentator, in real time, for a task you haven't seen yet. That's the
whole goal."

---

## Slide 2 — Today

"Here's the plan. Quick recap of where we left off. Then the big idea —
there's no single leap from your request to a finished result, it's a
loop. We'll break that loop into its four pieces. Then I'll walk you
through a concrete example, a whole play-by-play, so you know exactly
what you're looking for. Then it's your turn: you give it a real
multi-step task and log every single thing it does. And we close with a
checkpoint where you show me you actually watched, not just that it
worked."

*(~3 min total so far)*

---

## Recap and the Big Idea (~5-6 min)

## Slide 3 — Quick Recap

"Quick rewind: Module 0, you typed one sentence, asked for `hello.txt`,
and watched it get created in a handful of visible steps — explain,
ask permission, write, check. That was one small loop.

Today's whole point is that most real requests aren't that small. They
involve multiple files, multiple decisions, multiple checks along the
way. You're about to learn to see the *whole* chain, not just admire the
finished result at the end."

## Slide 4 — The Big Idea: No Single Leap

"Here's the one sentence I want you to walk away with today: the agent
does not read your request and teleport to a finished result. It works
in a loop — think, do one thing, look at what happened, think again —
and it keeps going around that loop until the task looks done.

That's it. That's the whole mental model. Everything else today is just
zooming in on pieces of that sentence."

## Slide 5 — The Loop

"Let's slow it down into four pieces. Think: given everything it knows
so far, what should it do next? Act: it does exactly one thing — we
call that a tool call. Observe: it looks at what actually happened, not
what it hoped would happen. Repeat: back to thinking, except now it
knows something it didn't a second ago.

It stops when it decides the task looks done. Not before, and
importantly — not by guessing ten steps ahead and hoping. One step,
then a fresh look, every single time."

*(~9 min total so far)*

---

## Zooming In (~5-6 min)

## Slide 6 — What's a "Tool Call"?

"Quick vocabulary, because you'll hear 'tool call' a lot in this
course. Every single 'act' step is one specific, concrete action: read a
file, edit or write code, run a command, search for something. That's
the whole list — there's no fifth secret category.

And it's always *one* of these at a time, never a pile of them at once.
That's exactly why this is watchable instead of a black box — one
action, one moment, over and over."

## Slide 7 — The Cook, Not the Chaos

"Here's the analogy I want stuck in your head: picture a cook following
a recipe, but tasting as they go. They add something, taste it, and
that taste tells them what to do next. That's the loop.

Now picture the opposite: a cook who dumps every single ingredient into
the pot at once and just hopes it turns out fine. Nobody actually cooks
that way, and a good agent doesn't work that way either. Each step is
informed by the step before it — that's the entire value of stopping to
look before continuing."

## Slide 8 — Why This Matters: You Can Debug It

"Here's why I'm spending twenty minutes on what might sound obvious.
Once you can actually see this loop, something really important
happens to how you handle it going wrong.

If you can't see the loop, and something breaks, all you've got is
'it's broken' — a total, mysterious failure, nothing to grab onto. But
if you can see the loop, that same failure becomes 'step 4 read the
wrong file, and that's why step 5 wrote something wrong.' Same bug,
completely different amount of control. That difference — from
mysterious to fixable — is the entire reason this module exists."

*(~15 min total so far)*

---

## Concrete Example (~6-7 min)

## Slide 9 — Example Task: Add a Scoreboard

"Let's make this real with an example before you go do your own. Say
you type this: 'Add a scoreboard to my browser game that shows the
player's points, and update it whenever they score.'

Pause here and actually think, don't skip ahead. If you were doing this
by hand, what would you check first? Guess the order of what happens,
in as much detail as you can."

*(Pause for actual guesses — even a solo learner should stop and write
something down before the next slide.)*

## Slide 10 — Play-by-Play, Part 1

"Here's roughly how it goes. One, it thinks: where does this game's
state even live right now? Two, it acts — reads `game.js`. Three, it
observes — finds a `player` object in there, but no `score` field yet.
That observation matters, because now it knows something it didn't a
second ago.

Four, it thinks again: score needs somewhere to *live*, and somewhere to
*show up* — two different problems. Five, it reads `index.html`. Six,
it observes: there's a container div for the game, but nothing that
looks like a scoreboard in there yet."

## Slide 11 — Play-by-Play, Part 2

"Seven, now it's got enough information to actually plan: add a `score`
variable, an `updateScore()` function, and a spot in the HTML to display
it. Eight and nine, it acts twice — edits `game.js`, then edits
`index.html`. Ten, it acts again — runs the game to actually check its
work, not just assume it's right. Eleven, it observes: the scoreboard
shows zero, and it updates when a point gets scored. Twelve, it thinks:
looks done.

Count that up — twelve steps, for one sentence you typed. That's
completely normal, and it's exactly what you should expect to see
today."

## Slide 12 — What To Notice

"Before you go do your own version, notice three things about that
example. It read both files *before* touching either of them — it
oriented first. It never touched anything outside those two files,
nothing extra, nothing unrelated. And the observe steps are what let it
catch 'there's no score field yet' *before* it wrote code that would've
broken. Skip the observing, and it's just guessing blind. Keep an eye
out for that same pattern in your own task today."

*(~22 min total so far)*

---

## Handing Off to the Hands-On Task (~2-3 min)

## Slide 13 — Your Turn: Hands-On

"Your turn. Pick a small task with a few moving parts — genuinely a few,
not one. Two good options: add a new page to your site with a nav link
pointing to it, or add a function that scores the player and hook it up
to the display. Give the agent that task, and then — this is the part
people skip — actually watch it work. Don't tab away and come back when
it's done."

## Slide 14 — What To Log

"While it's working, keep a running list, in order: every file it
reads, every edit it makes, every command it runs. Don't summarize as
you go, just capture the raw sequence.

Once it's finished, go back through that list and, next to each step,
write one line: why do you think it did that? That second pass is
where the actual learning happens — anyone can watch a screen, the
skill is explaining *why* each step happened."

*(~26 min total so far — hands-on task happens now, live, not scripted
here)*

---

## Checkpoint and Wrap-Up (~2-3 min, after hands-on is done)

## Slide 15 — Checkpoint

"Once you're done, here's your checkpoint. Turn in, or just talk through
with your supervisor, two things: your ordered play-by-play list with
your 'why' notes next to each step, and one step that surprised you —
either because you genuinely didn't expect it, or because it wasn't
what you would've done first if you were doing it by hand.

That surprise question isn't decoration. If nothing surprised you,
that's worth a second look too — it might mean you already had great
instincts, or it might mean you weren't watching closely enough to
notice."

## Slide 16 — Recap

"Let's lock in today. The agent doesn't leap to a finished result, it
loops: think, act — one tool call — observe, repeat. A loop you can see
is a loop you can debug — that's the whole payoff. And the pattern to
keep watching for, every time: read before it writes, and check after
it acts."

## Slide 17 — Next Up

"Next time, Module 2. You've spent today learning to watch the loop from the outside. Next we look at how the agent reaches beyond your project folder — plugging in outside tools and data safely — and after that, how it remembers you and learns reusable moves."

---

*(Total lecture time: roughly 22-26 minutes as scripted, leaving the
remainder of the 45-90 minute module for the hands-on task and
checkpoint conversation.)*
