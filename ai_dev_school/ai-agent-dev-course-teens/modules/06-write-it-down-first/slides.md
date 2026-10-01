---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 6
## Write It Down First

Planning beats improvising — once the feature is bigger than a one-liner.

*Build With AI*

---

<!-- Slide 2 -->

## Agenda

- Quick recap of Module 5
- The big idea: write it down before the agent starts
- What actually goes in a one-page plan
- A worked example: planning a real feature
- Hands-on: write your own plan, hand it to the agent
- Checkpoint

---

<!-- Slide 3 -->

## Recap: Module 5

- The agent only works with what you actually say
- Vague → agent guesses. Specific → agent gets close.
- You tested this yourself: same feature, three tries,
  three different results

Today's problem: even a *specific* request, said out loud, has a way of
leaving stuff out. Writing it down is how you catch that.

---

<!-- Slide 4 -->

## The big idea

For anything bigger than a quick fix:

**Write down what you want *before* the agent starts building.**

Like a short game design doc, or a one-page project brief — not a
novel, one page.

You're not writing it for the agent's benefit first. You're writing it
to catch your *own* unclear thinking before it becomes the wrong code.

---

<!-- Slide 5 -->

## Why this actually saves time

- Talking it through out loud feels efficient — it isn't, it just
  *feels* faster because you're not doing the hard part yet
- Gaps in your thinking are invisible in your head. On paper, they're
  obvious — a blank space where a sentence should be
- Fixing a plan costs minutes. Fixing built code costs a lot more

This is what pro teams call **document-driven development** — the doc
is the source of truth, not a conversation that gets forgotten.

---

<!-- Slide 6 -->

## The one-page plan: four parts

1. **Goal** — what this is supposed to do, plain language
2. **Not this** — what's explicitly out of scope
3. **How it should behave** — the important cases, including the
   tricky ones you already know about
4. **Done means** — how you'll know it actually works

Four sections. One page. Let's break each one down.

---

<!-- Slide 7 -->

## Goal + Not this

**Goal** — one or two sentences, plain language. What problem does
this solve, for who?

**Not this** — the part people skip, and the one that saves you the
most grief:

> Agents are "helpful." Helpful means it might add stuff you didn't
> ask for, because it seemed like a natural fit. "Not this" is how you
> say no in advance.

---

<!-- Slide 8 -->

## How it should behave

The edge cases. The ones you *already* know about — not a brainstorm,
just the stuff sitting in your head right now.

- What happens with zero of something? Too many?
- What happens the second time, not just the first?
- What should definitely **not** happen?

You already thought of these. Writing them down costs ten seconds.
*Not* writing them down costs a debugging session later.

---

<!-- Slide 9 -->

## Done means

How do *you* check this actually works — without just eyeballing it
and hoping?

- Concrete, checkable statements, not vibes
- "Looks right" is not a done-means. "Buying the upgrade twice is not
  possible" is.

This section is what you'll test the agent's result against at the
end — so write it before you see any code, not after.

---

<!-- Slide 10 -->

## Worked example: an upgrade shop

Feature: a shop screen in a small game where the player spends coins
on upgrades.

```markdown
## Goal
Let the player spend coins earned in-game to buy one of three
upgrades (extra life, speed boost, double points) from a shop
screen opened from the pause menu.

## Not this
- No real-money purchases
- Can't sell upgrades back
- No new upgrade types beyond these three
- Don't redesign the pause menu itself
```

---

<!-- Slide 11 -->

## Worked example, continued

```markdown
## How it should behave
- Not enough coins → buy button is disabled, shows how many
  more coins are needed
- Already own an upgrade → shows "Owned" instead of a price,
  can't buy it again
- Buying an upgrade removes the coins immediately
- Closing and reopening the game keeps owned upgrades owned

## Done means
- Can buy each upgrade when I have enough coins
- Can't buy one when I'm short (button is disabled, not broken)
- Coins and owned upgrades survive a restart
```

Notice: nothing here is code. It's still just decisions.

---

<!-- Slide 12 -->

## Hands-on task

1. Pick a real feature for your project — one with at least one tricky
   edge case you can already picture
2. Write your one-page plan: Goal, Not this, How it should behave,
   Done means
3. Give the agent **only the plan** — no extra verbal explanation, no
   filling in gaps out loud
4. Check the result against your "Done means" section

---

<!-- Slide 13 -->

## Why "only the plan"

This is the part people are tempted to cheat on.

If you narrate extra context out loud while the agent works, you'll
never find out where your *plan* actually had a gap — you'll have
patched it with your voice instead. The whole point of this exercise
is to see your plan's blind spots, so let it stand on its own.

---

<!-- Slide 14 -->

## Checkpoint

- What did the agent get right, straight from the plan alone?
- What did you have to go back and add — because you'd left something
  out, or the agent guessed wrong?

That second list is the real deliverable today. It's proof of exactly
what your plan was worth.

---

<!-- Slide 15 -->

## Recap + next up

- A plan is four short sections, not an essay
- "Not this" and "Done means" are the two sections people skip — and
  the two that save the most time
- Writing it down catches *your* gaps before they become bugs

**Next — Module 7: Keep It Looking Consistent.** Same move, applied to
design: writing down colors, fonts, and spacing so the agent stops
guessing differently every session.
