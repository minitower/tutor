# Lecture Script — Module 7: Keep It Looking Consistent

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd explain it to a smart 15-year-old who just watched
their own project start to look like it was glued together from five
different apps. Total lecture portion should run **~20-25 minutes**; the
rest of the 45-90 minute module is the hands-on task and checkpoint. Slide
numbers below match `slides.md` exactly.

---

## Opening (~1 min)

## Slide 1 — Keep It Looking Consistent

Welcome them in. Something like:

"Today's problem is one you've probably already run into without knowing
why it was happening: you ask your AI agent to build something, it looks
great. You ask it to build something else in the same project, that also
looks great. Then you put them side by side and... they don't look like
they belong together. Different colors, different fonts, different vibe
entirely. That's not bad luck, and it's not the agent being sloppy. It's
a specific, predictable thing, and today we fix it with one file."

---

## Slide 2 — Today

"Here's the plan. We'll look at why this happens in the first place, land
on the fix, look at exactly what that fix looks like as a real file, and
then you're going to prove it to yourself — you'll build two different
pages in two totally separate sessions, using only that one file to keep
them lined up. Then we check: did it actually work?"

*(~2 min total so far)*

---

## Recap and the Problem (~4-5 min)

## Slide 3 — Recap: Module 6

"Quick callback to last time. Module 6's big idea was: write down what
you want *before* the agent builds it. A short plan beats winging it,
especially once a feature gets bigger than 'add one button.' Today is
that exact same move — write it down first — but aimed at something much
narrower. Not the whole feature. Just: what does your project actually
*look* like?"

## Slide 4 — The Problem

"Here's the specific issue. A fresh agent session has zero memory of what
happened in your last session. None. So imagine you ask for a 'clean,
modern' login page today, and then next week, in a brand new session, you
ask for a 'clean, modern' settings page. Both requests are reasonable.
Both results might genuinely look good on their own.

But here's the catch: they will not look like the same app. One might
lean dark and blue, the other might come out light and green, because
'clean and modern' doesn't pin down a single answer — it's a whole
neighborhood of possible answers, and the agent picks a fresh spot in
that neighborhood every single time you ask."

*(~6-7 min total so far)*

---

## The Big Idea (~6-7 min)

## Slide 5 — The Big Idea

"So here's the one sentence I want you to walk away with today:

**If you don't write your colors, fonts, and spacing down somewhere
real, the agent guesses — differently, every time.**

And the fix is almost annoyingly simple: one file, with real values in
it, plus a rule that tells the agent to always check that file before it
styles anything. That's it. That's the whole trick. The rest of today is
just making sure you actually do it properly."

## Slide 6 — What a Style Sheet Actually Looks Like

"Let's make 'real values' concrete, because that phrase is doing a lot of
work. Here's an actual example:

```css
:root {
  --color-background: #14161a;
  --color-accent: #ffb703;
  --font-heading: "Poppins", sans-serif;
  --space-unit: 8px;
}
```

Look at what's in there. Not 'dark background' — an actual hex code,
`#14161a`. Not 'a nice accent color' — `#ffb703`, period. Not 'a modern
font' — the actual name, Poppins. Not 'some breathing room' — `8px`, a
real number you can multiply for bigger gaps. Every single value here is
something the agent can just *read*, not something it has to
interpret. That's the entire difference."

## Slide 7 — Specific Beats Vague — Every Time

"This connects straight back to something from Module 5, and it's worth
saying out loud: 'make it look cool and modern' is a vague ask, and vague
asks get a fresh guess every time you make them. `--color-accent:
#ffb703;` is a specific value, and specific values come back identical
every single time, whether it's session two or session two hundred.
Same rule as always — vague asks get guesses, specific asks get exactly
what you meant. We're just applying it to color and spacing now instead
of feature behavior."

*(~13-14 min total so far)*

---

## Making the Rule Stick (~5-6 min)

## Slide 8 — Make the Agent Actually Use It

"Here's the part people skip, and it's the part that actually makes this
work. Writing the file isn't enough by itself — you also have to tell the
agent, in your project's instructions file, to go check it. Something
like:

> 'Always check `style.css` before styling anything. Don't introduce new
> colors, fonts, or spacing outside of it — add to the file instead.'

Notice that second sentence — it's not just 'look at the file,' it's also
'if you need something new, it goes *in* the file, not off on its own.'
A file the agent doesn't know it's supposed to check is just a file
sitting there doing nothing. The instruction is what turns it into a
rule the agent actually follows."

## Slide 9 — Without the File vs. With It

"Let's picture both worlds side by side. Without the file: you say 'make
it look nice' twice, in two sessions, and you get two different color
schemes, two different fonts, spacing that doesn't line up — basically
two strangers who happen to share a project folder.

With the file: same style file, two sessions, and you get the same
colors, the same font, the same spacing rhythm — even though neither
session ever saw the other one get built. Neither session needs to
remember the other. They both just read the same file. That's the whole
mechanism."

## Slide 10 — Why It Matters

"Zoom out for a second on why this is worth doing at all. If you build a
project page by page with no shared style file, by page five it looks
stitched together from five different projects — because, in a very real
sense, each page *was* designed by a slightly different guess. One file,
written once, early, fixes that for the entire rest of the course. And I
want to push back on the idea that this is 'extra work' — it's not. It's
genuinely less work than the alternative, which is going back later and
manually fixing five pages that all disagree with each other."

*(~19-20 min total so far)*

---

## Handing Off to the Hands-On Task (~3-4 min)

## Slide 11 — Your Turn: Hands-On

"Okay, that's the idea — now you're going to go prove it works. Five
steps. One: write a real style-sheet file for your project — actual
color codes, an actual font name, actual spacing numbers, nothing vague.
Two: add that 'always check this file' rule to your project's
instructions file. Three: in one session, build one page or screen using
only that style file as your guide. Four — and this is the important
part, don't cut this corner — in a *completely fresh, separate session*,
build a second, different page or screen, following the exact same rule.
Five: put both pages side by side and actually look at them."

## Slide 12 — What to Actually Compare

"When you put them side by side, don't just eyeball it and say 'yeah,
looks fine.' Check specific things: is the accent color identical in
both? Is it the same font, and does the heading look styled the same
way? Is the spacing rhythm the same, or does one page feel cramped while
the other feels loose? And here's the important mindset shift — anywhere
they *don't* match isn't bad luck and it isn't the agent messing up.
It's a gap in your style file. Something you didn't pin down got guessed
again. That's useful information, not a failure."

*(~24-25 min total so far — hands-on task happens now, live, not
scripted here)*

---

## Checkpoint and Wrap-Up (~2-3 min, after hands-on is done)

## Slide 13 — Checkpoint

"Once you've built both pages, here's your checkpoint, and I want an
honest answer, not a quick 'yeah they match': do the two pages actually
look like they belong to the same project? Really look.

Then, for the second part — and this is the one that really drives the
lesson home — try it once more, but this time *without* pointing the
agent at your style file. Just say 'make it look nice,' plain and vague,
like before. How different does that version come out? That contrast is
the whole module in one comparison."

## Slide 14 — Recap

"Let's lock in today's big things. A fresh session has no memory, so
vague style instructions drift a little differently every single time.
Real values in a real file remove the guessing entirely — there's
nothing left to interpret. A rule in your instructions file is what
actually makes the agent open that file instead of ignoring it. And two
sessions, one shared file, matching pages — that's the entire trick we
covered today, no more, no less."

## Slide 15 — Next Up

"Next time, Module 8, we take this exact same instinct — agree on
something *before* the agent builds it — and point it somewhere bigger:
not the visuals, but the actual approach. For a bigger change, you'll
work out *how* it's going to get built before any code gets touched.
Same move as today's style file, just aimed one level up."

---

*(Total lecture time: roughly 24-26 minutes as scripted, leaving the
remainder of the 45-90 minute module for the hands-on task and
checkpoint conversation.)*
