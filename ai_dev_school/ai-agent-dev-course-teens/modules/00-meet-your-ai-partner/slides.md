---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Meet Your AI Coding Partner

Module 0 — Build With AI

---

<!-- Slide 2 -->

## Today

- What an AI coding agent actually is (and isn't)
- What it can actually do
- What it needs from you
- Hands-on: get it running, give it one tiny task
- Checkpoint: explain what happened, not just that it worked

---

<!-- Slide 3 -->

## Myth #1: It's Not Autocomplete

- Autocomplete: guesses the next word, one at a time
- An agent: reads a whole request, plans multiple steps, takes real actions
- It's not just predicting text — it's *doing things* on your computer

---

<!-- Slide 4 -->

## Myth #2: It's Not Magic

- No mystery box — every action is a specific, visible step
- Reads files. Writes files. Runs commands. Checks results.
- You can watch every single one of those steps happen

---

<!-- Slide 5 -->

## So What Is It?

**A partner that can take real actions in a loop until it thinks the task is done.**

- Read your files
- Write new code
- Run commands
- Check whether what it did actually worked

That loop — do a thing, check the thing — is what makes it different from a search engine or chatbot.

---

<!-- Slide 6 -->

## The Loop, One More Time

```
READ   → understand what's there
WRITE  → make a change
RUN    → execute it
CHECK  → did that actually work?
```

Repeats until the agent thinks it's done — not one big leap from request to finished result.

---

<!-- Slide 7 -->

## It Only Does What You Tell It

- Explicit instruction: "create a file called `hello.txt`"
- Reasonable inference: it picks sensible defaults you didn't spell out (like where to put it)
- What it does *not* do: invent a task you never asked for

This whole course is about getting good at the "telling it" part.

---

<!-- Slide 8 -->

## Same Partner, Real Boundaries

- Any partner doing real work for you needs boundaries — this one's no different
- Claude Code asks permission before things like editing files or running commands
- That's not the tool being slow — that's the boundary working as designed

---

<!-- Slide 9 -->

## Example: "Create hello.txt"

You type:

> "Create a file called `hello.txt` with a short message in it."

Before you approve anything — what do you expect to see happen?

---

<!-- Slide 10 -->

## What Actually Happens

1. Agent explains what it's about to do
2. **Asks your permission** to create the file
3. You approve
4. It writes the file
5. It can check the file exists / read it back

Every step is visible. Nothing happens silently.

---

<!-- Slide 11 -->

## Your Turn: Hands-On

1. Confirm your sandboxed project folder is ready
2. Open Claude Code in that folder
3. Ask for one tiny, safe, reversible thing
4. Read what it says *before* you approve it
5. Look at the actual result when it's done

---

<!-- Slide 12 -->

## Then Ask It About Itself

Once the file exists, ask:

> "What tools do you have access to in this session, and what would you need my permission for?"

Compare its answer to what you just watched it do.

---

<!-- Slide 13 -->

## Checkpoint

In your own words, a few sentences:

- What did the agent actually *do*, step by step?
- What's one thing it needed your permission for — why does that boundary exist?

"It just did it" means: slow down, re-watch the session.

---

<!-- Slide 14 -->

## Recap

- Not autocomplete, not magic — a partner that takes real, visible actions
- The loop: read, write, run, check
- It does what you tell it (or reasonably infers) — nothing more
- Permission prompts are the boundary, not an inconvenience

---

<!-- Slide 15 -->

## Next Up

**Module 1 — How the Agent Thinks: The Loop**

You'll give it a small multi-step task and log every single action it takes, in order — a full play-by-play.

