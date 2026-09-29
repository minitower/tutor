---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Capstone: Build & Show

Module 12 — Build With AI

---

<!-- Slide 2 -->

## Today

- A fast recap of everything this course built in you, Module 0 to 11
- The capstone assignment: one real project, spec → plan → test → review
- How to pick (or finish) a project from your track
- What you actually have to hand in
- Most of today is build time, not lecture

---

<!-- Slide 3 -->

## Recap: Where You Started (0–2)

- **Module 0** — an agent isn't autocomplete and isn't magic: a partner that takes real, visible actions in a loop
- **Module 1** — that loop, slowed down: read, write, run, check, repeat
- **Module 2** — vague asks get guesses; clear asks get what you meant

---

<!-- Slide 4 -->

## Recap: Building the Habits (3–6)

- **Module 3** — write a one-page spec before anything bigger than a quick fix
- **Module 4** — write down your colors/fonts/spacing, or every session guesses differently
- **Module 5** — for multi-file changes, review the agent's plan before it touches anything
- **Module 6** — a failing test, then a fix, proves it — "looks right" isn't "is right"

---

<!-- Slide 5 -->

## Recap: Getting Rigorous (7–9)

- **Module 7** — small stuff doesn't need a written plan, just talk it through
- **Module 8** — a fresh second agent, no memory of the build, catches what the builder can't see in itself
- **Module 9** — agents sound confident even when wrong; you're the one who checks

---

<!-- Slide 6 -->

## Recap: Owning It (10–11)

- **Module 10** — automate what's proven to work, with approval gates on anything irreversible
- **Module 11** — your own AI use policy: how you use it, how you disclose it, what you never skip understanding

---

<!-- Slide 7 -->

## The Capstone, In One Line

**One real project. Every habit from this course, used for real, on something you actually want to finish.**

- Not a new skill to learn today
- Not a toy exercise built to demonstrate a technique
- The thing itself, done the way you now know how to do it

---

<!-- Slide 8 -->

## Pick Your Project

Whatever track you picked back at the start of the course:

| Track | What "finished" looks like |
|---|---|
| Personal site | A finished multi-page site with consistent design |
| Small game | A playable mini-game with a few mechanics working together |
| Bot (Discord/Telegram) | A bot with a handful of working, tested commands |
| School club tool | A working tool the club can actually use |

The thing you've been building since Module 3 counts. A fresh start counts too, if you want one.

---

<!-- Slide 9 -->

## Finish Beats Perfect

- Pick a scope you can actually finish today, not the biggest version of the idea in your head
- A small, finished, tested thing beats a huge, half-built, untested one
- If you're not sure it fits — cut a feature before you cut testing or review
- You can always write "next up" ideas in your spec's not-this section instead of building them

---

<!-- Slide 10 -->

## The Four Moves

1. **Spec it** (Module 3)
2. **Plan it** (Module 5)
3. **Test the core logic** (Module 6)
4. **Get it reviewed** (Module 8)

Same moves you already know. Today you run all four, back to back, on one real thing.

---

<!-- Slide 11 -->

## Move 1 — Spec It

A real one-page plan, same four sections as Module 3:

- **Goal** — what this is supposed to do, in plain language
- **Not this** — what's explicitly out of scope
- **How it should behave** — the important cases, including tricky ones
- **Done means** — how you'll know it actually works

Someone who never talked to you should be able to read it and get it.

---

<!-- Slide 12 -->

## Move 2 — Plan It

- Hand the agent the spec, then use plan mode before any big edits
- Have it propose its approach — which files, what order, what it's touching
- Read the plan for real. Push back if something's missing or off.
- Only approve once it actually makes sense to you

---

<!-- Slide 13 -->

## Move 3 — Test the Core Logic

- Not boilerplate coverage — the part that actually matters if it's wrong
- The scoring function, the command parser, the thing the whole project depends on
- Bonus points if you can honestly say a test would have caught a real bug
- "It looks right" is not the same claim as "a test proves it's right"

---

<!-- Slide 14 -->

## Move 4 — Get It Reviewed

- A brand-new session — no memory of how you built it, no access to your reasoning
- Give it only the result and your spec, not the story of how you got there
- Ask it to check the build against the spec, not against what you meant
- Write down what it catches, even the small stuff

---

<!-- Slide 15 -->

## If It Has Any UI: Stay Consistent

- Module 4's rule still applies — colors, fonts, spacing from your written style sheet, not a fresh guess
- A capstone with three screens that look like three different projects is an easy, avoidable miss
- If your project has zero UI, skip this one — bots and CLI tools get a pass here

---

<!-- Slide 16 -->

## Close the Loop

- Fix whatever the review actually caught — don't rubber-stamp your own work
- If the review revealed your spec was wrong or incomplete, update the spec too
- The spec is supposed to be the truth about the project — keep it that way
- This step is often skipped under time pressure. Don't skip it.

---

<!-- Slide 17 -->

## Deliverable: Three Things

1. **The finished project** — working, not "basically working"
2. **Your artifacts** — spec, plan, tests, and review notes, saved as actual files, not just remembered
3. **A short walkthrough** — written or spoken, your choice

All three. A great project with no saved spec doesn't meet the bar today.

---

<!-- Slide 18 -->

## The Walkthrough

Cover, honestly:

- What you built
- What the agent did vs. what you did yourself
- One thing that surprised you — across this whole course, not just today

This is the same honesty your Module 11 policy asked of you. Today's the day it gets used for real.

---

<!-- Slide 19 -->

## Self-Check Before You Call It Done

- Could someone else read your spec and understand the project, with no verbal explanation?
- Did the build actually match the plan you approved — and if not, do you know why?
- Do your tests check the behavior that matters, or just the easy happy path?
- Did the review catch anything real, or did you rubber-stamp it?
- Is your walkthrough honest about what the agent did?

---

<!-- Slide 20 -->

## Your Turn: Hands-On

1. Confirm your project and scope for today
2. Write the spec — Move 1
3. Plan mode, review, approve — Move 2
4. Build, then test the core logic — Move 3
5. Fresh session, get it reviewed — Move 4
6. Fix what the review caught, update the spec if needed
7. Write your walkthrough

This can run long. That's expected — it's the capstone.

---

<!-- Slide 21 -->

## Recap

- Same four moves you already know: spec, plan, test, review — used together, for real, on one project
- Finished and honest beats big and half-built
- The deliverable is three things: the project, the saved artifacts, and an honest walkthrough
- The self-check questions are there so you catch a rubber-stamped review before someone else does

---

<!-- Slide 22 -->

## You Made It

Twelve modules ago, you weren't sure an AI agent was anything more than autocomplete. Today you spec'd, planned, tested, and got a second opinion on something real — and you can explain exactly what you did versus what it did.

That's not a small thing. That's the actual skill.

Go show someone what you built.
