---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Instructions That Actually Work

Module 5 — Build With AI

---

<!-- Slide 2 -->

## Today

- Quick recap: the agent works in a loop
- The big idea: vague ask = guess, clear ask = what you meant
- One feature, three ways — vague, specific, very specific
- Hands-on: try it yourself, compare the results
- Checkpoint: which version worked, and *why*

---

<!-- Slide 3 -->

## Last Time: The Loop

- The agent doesn't leap to a finished answer
- It works in a loop: think → act → check → think again
- When something goes wrong, it traces back to one step in that loop

Today's question: what happens *before* the loop even starts?

---

<!-- Slide 4 -->

## The Agent Can't Read Your Mind

- It can only work with what you actually say
- "Make it better" means something different to everyone — including the agent, differently every time
- **Vague ask → the agent guesses**
- **Clear ask → the agent builds what you meant**

---

<!-- Slide 5 -->

## The Highest-Leverage Skill Here

- Getting better at this improves *every* module after it
- The gap between "what I meant" and "what I typed" is where most bad results come from
- Not because the agent is bad at coding

---

<!-- Slide 6 -->

## Let's Test This: One Feature, Three Ways

- Same feature. Three levels of detail in the ask.
- Each version runs in its own **fresh session** — no shared context
- Feature for our example: add a leaderboard

---

<!-- Slide 7 -->

## Version 1: Vague

> "Add a leaderboard."

The agent has to guess:
- How many scores shown?
- Sorted how?
- Where does it go on the page?

---

<!-- Slide 8 -->

## Version 2: Specific

> "Add a leaderboard showing the top 5 scores, sorted highest first."

- Answered: how many, what order
- Still guessing: ties? fewer than 5 scores? placement on the page?

---

<!-- Slide 9 -->

## Version 3: Very Specific

> "...top 5 scores, sorted highest first. Ties break by earliest achieved. Fewer than 5 scores: show what exists, no placeholders. Place it in the sidebar, below the score display."

- Ties: handled
- Fewer than 5: handled
- Placement: handled

---

<!-- Slide 10 -->

## Same Feature, Three Results

| | Vague | Specific | Very Specific |
|---|---|---|---|
| Count / order | guessed | defined | defined |
| Ties | guessed | guessed | defined |
| Fewer than 5 | guessed | guessed | defined |
| Placement | guessed | guessed | defined |

More detail = fewer guesses = fewer surprises.

---

<!-- Slide 11 -->

## What Makes an Instruction Specific

- **Quantity** — how many, how much
- **Order** — sorted how, in what priority
- **Edge cases** — empty, tied, overflowing, first-time
- **Location** — where it lives, where it appears

You don't need to spell out everything — only what you actually care about.

---

<!-- Slide 12 -->

## Your Turn: Hands-On

1. Pick one small feature for your project
2. Write three versions: vague → specific → very specific
3. Run each one in a **separate, fresh session**
4. Compare the three results

---

<!-- Slide 13 -->

## Keep the Sessions Honest

- Fresh session = the agent has no memory of the earlier attempts
- Otherwise you're testing what it remembers, not what you wrote
- Write all three prompts down *before* you run any of them

---

<!-- Slide 14 -->

## Checkpoint

- Which version got closest to what you wanted, first try?
- Was there a point where being *more* specific stopped helping?
- What was still left for the agent to reasonably decide on its own?

---

<!-- Slide 15 -->

## Recap

- The agent works with what you say, not what you meant
- Vague → guesses. Specific → fewer guesses, closer result.
- Transferable skill: same muscle as a clear bug report or clear directions for a group project

---

<!-- Slide 16 -->

## Next Up

**Module 6 — Write It Down First**

For anything bigger than a one-liner, you'll write a short plan before the agent starts — and see what you had to fix once you saw it built.
