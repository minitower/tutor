---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Automate the Boring Stuff

Module 13 — Build With AI

---

<!-- Slide 2 -->

## Today

- Quick rewind: you've been re-explaining the same chores every time
- The big idea: once something works, hand it off to run on its own
- The line that matters: reversible vs. irreversible
- Hands-on: set up one small automation, with an approval gate built in
- Checkpoint: what runs free, what still asks — and why you drew it there

---

<!-- Slide 3 -->

## The Pattern So Far

- Run your tests by hand. Ask for a style check by hand. Every single time.
- Fine for a one-off. Expensive as a habit you repeat every session.
- Typing almost the same request for the fifth time? That's the signal.

---

<!-- Slide 4 -->

## The Big Idea

**Once something works and you're doing it by hand over and over, you can often set the agent up to do it automatically from then on.**

- Running your tests
- Checking your code style
- Any small routine you keep repeating

---

<!-- Slide 5 -->

## Why It Matters: Automation Is a Multiplier

- It multiplies good habits *and* mistakes — equally
- A mistake you catch once by hand: minor, fixed
- The same mistake happening silently, automatically, every time: worse
- The approval-gate habit from Module 8 matters even more here

---

<!-- Slide 6 -->

## What "Automatic" Can Mean Here

- A saved routine or custom command you trigger, instead of retyping it
- A hook — fires on its own on an event (after an edit, before a commit, etc.)
- Whatever your tool supports — the shape matters less than the decision behind it

---

<!-- Slide 7 -->

## The Line That Matters

- Not every automated action carries the same risk
- **Reversible:** running tests, checking style, reading files, reporting back
- **Hard to undo:** deleting files, overwriting work, publishing, spending money
- Same distinction behind every permission prompt you've seen since Module 0

---

<!-- Slide 8 -->

## Draw the Line on Purpose

- Decide, for *your* automation: does this need my okay every time, or can it just run and report?
- Write down the reasoning — not just the rule
- Default when you're not sure: require approval. Loosen it later, deliberately.

---

<!-- Slide 9 -->

## Concrete Example

- "After I edit a file, run my test suite and tell me what failed" — running and reporting: fully automatic
- "If tests fail, fix them" — actually changing code: still asks first
- Reporting is reversible. Editing your code on its own judgment is not "free" to undo.

---

<!-- Slide 10 -->

## Setting It Up

- A hook: configured once, fires by itself from then on
- A saved routine / custom command: still triggered by you, one word instead of a paragraph
- Either way — you build the approval line from Slide 8 into it *before* you turn it loose

---

<!-- Slide 11 -->

## Your Turn: Hands-On

1. Pick one small, repeated chore in your project
2. Set it up as a saved routine or hook — trigger it, don't re-explain it
3. Decide, explicitly: approval every time, or run-and-report? Write down why
4. Test it a few times

---

<!-- Slide 12 -->

## Prove It Actually Works

- Test it once on something that should pass
- Then test it **on purpose** with something that should fail
- If it says "looks good" when it shouldn't — it isn't catching anything, it's decoration

---

<!-- Slide 13 -->

## Checkpoint

- What does this automation do fully on its own?
- What does it still ask you about?
- Why did you draw the line there? What would move it in either direction?

---

<!-- Slide 14 -->

## Watch This Over Time

- This is the module most likely to quietly expand scope if left unchecked
- Review your "runs without asking" list with your supervisor — out loud, once
- Scope creep is easy to miss when each individual step looks small

---

<!-- Slide 15 -->

## Recap

- Once something works, you can often stop doing it by hand
- Automation multiplies whatever it repeats — good or bad
- Reversible can run free; hard-to-undo always asks first
- Draw that line on purpose, write down why, and revisit it

---

<!-- Slide 16 -->

## Next Up

**Module 14 — Rules of the Road**

Now that the agent can act on its own for some things, next time is about your own honest policy for when — and how — you use AI help at all.
