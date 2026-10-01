---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Prove It Works

Module 9 — Build With AI

---

<!-- Slide 2 -->

## Today

- Quick recap of Module 8
- The big idea: proving code works, not just eyeballing it
- A real bug, walked through start to finish
- Hands-on: break something on purpose, then prove you fixed it
- Checkpoint: two commits, kept separate

---

<!-- Slide 3 -->

## Recap: Module 8

- Bigger changes get a plan **before** any code changes
- You reviewed the plan, then approved it — like agreeing on a route before a road trip
- This module is the next habit: once it's built, how do you know it's right?

---

<!-- Slide 4 -->

## "Looks Right" Is Not "Is Right"

- You read the code. It seems fine. You move on.
- But you only checked the inputs you happened to think of
- The bugs that bite later live in the inputs nobody tried by hand

---

<!-- Slide 5 -->

## The Big Idea

**A test is code that checks your code — instead of you eyeballing it.**

- It runs the function with a known input
- It checks the output against the answer you already know is correct
- No guessing, no "looks fine to me"

---

<!-- Slide 6 -->

## Why Fail First?

- A test that passes on the first try might be testing nothing at all
- A **failing** test, caused by a real bug, proves the test can actually catch that bug
- Only then does watching it turn green mean something

---

<!-- Slide 7 -->

## Red, Then Green

```
1. RED    → write a test, watch it fail because of the real bug
2. GREEN  → fix the bug, watch the same test pass
3. CHECK  → make sure nothing else broke
```

This order matters. Fixing first and testing after proves nothing.

---

<!-- Slide 8 -->

## Example: The Bug

A quiz-scoring function, one line off:

```js
function countCorrect(answers, key) {
  let score = 0;
  for (let i = 0; i < answers.length - 1; i++) {
    if (answers[i] === key[i]) score++;
  }
  return score;
}
```

Spot it? It never checks the last answer.

---

<!-- Slide 9 -->

## Example: The Failing Test

```js
test("counts every answer, including the last one", () => {
  const answers = ["A", "B", "C"];
  const key     = ["A", "B", "C"];
  expect(countCorrect(answers, key)).toBe(3);
});
```

Run it now: **fails**, returns `2` instead of `3`. Right reason, real bug.

---

<!-- Slide 10 -->

## Example: The Fix

```js
function countCorrect(answers, key) {
  let score = 0;
  for (let i = 0; i < answers.length; i++) {
    if (answers[i] === key[i]) score++;
  }
  return score;
}
```

One character changed. That's the whole fix.

---

<!-- Slide 11 -->

## Example: Green

- Same test, no edits to it
- Run it again: **passes**, returns `3`
- Because the test didn't change, the pass actually means the bug is gone

---

<!-- Slide 12 -->

## Your Turn: Hands-On

1. Find a small bug in your project — or make one on purpose
2. Ask the agent to write a test that **fails** because of it
3. Check the failure is real — not a typo in the test
4. Ask the agent to fix the bug
5. Confirm the test passes, and nothing else broke

---

<!-- Slide 13 -->

## Watch For This

- Did the first test actually exercise the bug, or did it pass by accident?
- If the agent's test passes immediately, that's a red flag, not a shortcut
- A test that never failed never proved anything

---

<!-- Slide 14 -->

## Checkpoint

Two separate save points, kept apart:

1. A commit with just the **failing test**
2. A commit with the **fix**

Plus one honest sentence: did the agent's first test actually catch the real bug, or did you have to fix the test itself?

---

<!-- Slide 15 -->

## Recap

- "Looks right" and "is right" are different things
- A test proves it — fail first, then fix, then pass
- Two commits, not one, so the proof is visible in your history

---

<!-- Slide 16 -->

## Next Up

**Module 10 — Just Talk It Through**

Not everything needs a written plan. You'll rebuild something small from Module 6 — this time purely conversationally, no written plan — and compare.

