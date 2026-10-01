---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# How the Agent Thinks: The Loop

Module 1 — Build With AI

---

<!-- Slide 2 -->

## Today

- Quick recap of Module 0
- The big idea: no single leap, just a loop
- The loop, broken into its four pieces
- A concrete play-by-play, step by step
- Hands-on: give it a multi-step task, log everything
- Checkpoint: your own annotated play-by-play

---

<!-- Slide 3 -->

## Quick Recap

Last time: you asked for one tiny thing (`hello.txt`), and watched it get done in a few visible steps.

Today we zoom in on that. Real tasks aren't one step — they're a *chain* of steps. You're about to learn to see the whole chain, not just the result at the end.

---

<!-- Slide 4 -->

## The Big Idea: No Single Leap

The agent does not read your request and teleport to a finished result.

It works in a loop:

**think → do one thing → look at what happened → think again**

...repeating until the task looks done. That's it. That's the whole mental model for today.

---

<!-- Slide 5 -->

## The Loop

```
THINK    → what should I do next, given everything so far?
ACT      → do exactly one thing (a "tool call")
OBSERVE  → look at what actually happened
REPEAT   → back to THINK, with new information
```

Stops when the agent thinks the task is done — not before, not by guessing ahead.

---

<!-- Slide 6 -->

## What's a "Tool Call"?

Every ACT step is one concrete, specific action:

- Read a file
- Edit or write code
- Run a command
- Search for something

One tool call = one thing. Never "a bunch of stuff at once." That's *why* the loop is watchable.

---

<!-- Slide 7 -->

## The Cook, Not the Chaos

Think of a cook following a recipe — tasting as they go, adjusting the next step based on what they just tasted.

Not a cook who dumps every ingredient in the pot at once and hopes for the best.

Read a little, act a little, check it, then decide what's next. Every step informs the next one.

---

<!-- Slide 8 -->

## Why This Matters: You Can Debug It

Once you can see the loop, "it's broken" stops being a mystery.

- No loop visible → total, unexplainable failure, nothing to fix
- Loop visible → "step 4 read the wrong file, that's why step 5 went sideways"

Same failure, completely different level of control. This is the whole reason today's module exists.

---

<!-- Slide 9 -->

## Example Task: Add a Scoreboard

Say you ask:

> "Add a scoreboard to my browser game that shows the player's points, and update it whenever they score."

Before the next slide — guess the order of steps. What would *you* check first if you were doing this by hand?

---

<!-- Slide 10 -->

## Play-by-Play, Part 1

1. **THINK** — where does the game's state currently live?
2. **ACT** — read `game.js`
3. **OBSERVE** — finds a `player` object, but no `score` field yet
4. **THINK** — score needs somewhere to live *and* somewhere to show up
5. **ACT** — read `index.html`
6. **OBSERVE** — finds the game's container div, no scoreboard element

---

<!-- Slide 11 -->

## Play-by-Play, Part 2

7. **THINK** — plan: add a `score` variable, an `updateScore()` function, and a place to display it
8. **ACT** — edit `game.js`: add the variable and function
9. **ACT** — edit `index.html`: add a `<div id="score">`
10. **ACT** — run the game to check it
11. **OBSERVE** — scoreboard shows `0`, updates when a point is scored
12. **THINK** — task looks done

---

<!-- Slide 12 -->

## What To Notice

- Twelve steps, one small request — real tasks are rarely one step
- It read *before* it wrote, both times
- It didn't touch anything outside the two relevant files
- The OBSERVE steps are what let it catch "no score field yet" *before* writing broken code

---

<!-- Slide 13 -->

## Your Turn: Hands-On

1. Pick a small task with a few moving parts:
   - Add a new page with a nav link to it, **or**
   - Add a function that scores the player and hook it up to the display
2. Give the agent the task
3. Watch it work — don't walk away

---

<!-- Slide 14 -->

## What To Log

As it works, keep a running list, in order:

- Every file it **reads**
- Every **edit** it makes
- Every **command** it runs

When it's done, go back through the list and write one line next to each step: *why* do you think it did that?

---

<!-- Slide 15 -->

## Checkpoint

Turn in, or talk through with your supervisor:

- Your ordered play-by-play list, with your "why" notes
- One step that surprised you — because you didn't expect it, or because it wasn't what *you'd* have done first

---

<!-- Slide 16 -->

## Recap

- The agent doesn't leap to a finished result — it loops
- Loop: think → act (one tool call) → observe → repeat
- A visible loop is a debuggable loop
- Reading before writing, and checking after acting, is the pattern to watch for

---

<!-- Slide 17 -->

## Next Up

**Module 2 — Plug It In: MCP**

You've learned to watch the loop. Next, you give it a safe way to reach outside data — the tools it can plug into.
