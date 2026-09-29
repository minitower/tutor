---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Two Heads Are Better

Module 8 — Build With AI

---

<!-- Slide 2 -->

## Today

- Quick rewind: you've been building solo with one agent this whole course
- The problem: the agent that built something can't see its own blind spots
- The big idea: a second, completely fresh agent reviews the work
- Hands-on: build with one session, review with a brand new one
- Checkpoint: what did the fresh eyes catch?

---

<!-- Slide 3 -->

## The Problem: Builder Bias

- The agent that wrote the code "knows what it meant"
- It assumes its own choices were reasonable — because it made them
- Not an AI-only flaw — you do this with your own writing too
- Being close to the work makes you blind to your own mistakes in it

---

<!-- Slide 4 -->

## The Classroom Analogy

- Ever swap papers with a classmate before turning an assignment in?
- The person who wrote it stopped seeing their own typos, gaps, weird phrasing
- Someone new reads it cold — and catches what you couldn't
- Same idea, with an AI reviewer standing in for the classmate

---

<!-- Slide 5 -->

## The Big Idea

**A second, completely fresh agent — one that didn't build it and doesn't know the first agent's reasoning — can review the work with genuinely fresh eyes.**

- Fresh means: no memory of the build, no access to the builder's explanations
- Just the result, and the original task

---

<!-- Slide 6 -->

## Why It Matters

- The builder agent tends to assume its own choices were reasonable
- A fresh session has no such bias
- It catches things the builder is blind to — because it never made those assumptions in the first place

---

<!-- Slide 7 -->

## What "Fresh" Actually Means

- A brand new session — not the same chat, not "continue this conversation"
- No memory of the first agent's reasoning or explanations
- It only gets: the diff/result + the original task
- Not: "here's how I built it" or "here's why I made this choice"

---

<!-- Slide 8 -->

## This Is Real Code Review

- On real software teams, nobody merges their own pull request unreviewed
- A second engineer reads the diff cold, without the first engineer narrating it
- Today, an AI reviewer stands in for that second engineer
- Same mechanic, same reason it works: distance catches what closeness misses

---

<!-- Slide 9 -->

## The Setup: Two Sessions, One Task

1. Session A builds a moderately-sized feature
2. Session B — a completely new session — reviews it
3. Session B gets only the diff/result and the original task

---

<!-- Slide 10 -->

## What NOT to Hand the Reviewer

- Not the builder's reasoning or explanations
- Not "here's what I was trying to do when I wrote this part"
- Just the task, and the finished result
- Anything else contaminates the "fresh" part

---

<!-- Slide 11 -->

## What to Ask the Reviewer

> "Here's the original task and the resulting code. Does this actually do what was asked? Is anything missing, wrong, or off?"

- Let it look for real — don't lead it toward specific concerns
- A vague "looks good" is a signal to push for detail, not a pass

---

<!-- Slide 12 -->

## Your Turn: Hands-On

1. In one session, build a moderately-sized feature
2. Start a **brand new session** with no memory of the first
3. Give it only the diff/result and the original task
4. Ask it to review: does this do what was asked? Anything missing, wrong, or off?

---

<!-- Slide 13 -->

## While You Compare

- Read the reviewer's findings *before* deciding if you agree
- For each one: real issue, nitpick, or reviewer being wrong?
- Tell the builder session what the reviewer found — does it agree or push back?

---

<!-- Slide 14 -->

## Checkpoint

- What did the reviewer session catch that you (and the builder session) missed?
- If it caught nothing — was the work genuinely solid, or was the review not looking hard enough?
- How would you tell the difference?

---

<!-- Slide 15 -->

## Recap

- The agent that built something is biased toward its own choices
- A fresh, uninvolved session reviews with no such bias
- Give the reviewer the result and the task — not the builder's reasoning
- This is exactly how code review works on real software teams

---

<!-- Slide 16 -->

## Next Up

**Module 9 — Don't Trust Blindly**

Agents sound confident even when they're wrong — and a fresh review can miss things too. Next time: reviewing code yourself, and spotting instructions hidden in content an agent reads.
