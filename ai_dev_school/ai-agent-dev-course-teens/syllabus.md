# Syllabus

Each module: **Big idea → Why it matters → Hands-on task → Checkpoint**.
Full detail in the matching file under `modules/`. Read
[SUPERVISOR-GUIDE.md](SUPERVISOR-GUIDE.md) before starting Module 0.

---

## Module 0 — Meet Your AI Coding Partner
- Big idea: an AI coding agent isn't autocomplete and isn't magic — it's
  a partner that can read files, write code, run commands, and check its
  own work, but only does what you actually tell it (or lets it infer)
- Hands-on: get the tool running in your sandboxed project folder; ask it
  to do one tiny, safe thing and watch what it actually does step by step
- Checkpoint: explain, in your own words, what the agent did and why —
  not just that it worked

## Module 1 — How the Agent Thinks: The Loop
- Big idea: the agent works in a loop — think, do a thing, look at what
  happened, think again — not one big leap from your request to a
  finished result
- Hands-on: give it a small multi-step task, and log every "thing it
  did" in order, like a play-by-play
- Checkpoint: annotated play-by-play + one sentence on which step
  surprised you

## Module 2 — Plug It In: MCP
- Big idea: MCP is a shared "plug" standard (like USB-C) that lets an agent
  use outside tools and data through small servers — and every plug is a
  trust decision, because a server is a program running on your computer
  and its results are untrusted text
- Hands-on: write a one-tool, read-only mini server for your project's
  data (Python), check it in the Inspector, connect it, then try to make
  the agent change data and see why it can't
- Checkpoint: server code + call trace + your own 5-item "can I plug it
  in?" checklist + one sentence on why tool results aren't instructions

## Module 3 — Give Your Agent a Memory
- Big idea: context isn't memory; long-term memory (files, databases,
  memory systems) makes an agent a real partner — but it is data about
  people that can be poisoned, go stale, and leak, so *what* you remember
  matters most (includes the `SOUL.md` convention and layered systems
  like TencentDB Agent Memory)
- Hands-on: project notes in `CLAUDE.md` across two sessions, a
  helper's role file, a tiny SQLite memory with a test, and a written
  write-policy
- Checkpoint: memory files + green test + write policy with a *why* for
  each rule

## Module 4 — Teach It a Move: Skills
- Big idea: package a procedure you repeat into a skill (`SKILL.md`) that
  loads only when needed; the description decides when it fires; a skill
  is advice (use hooks for "must"), and it is code with privileges
- Hands-on: build a skill for your project, test it with 5 should / 5
  shouldn't prompts, compare with/without, and lock down side effects
- Checkpoint: skill folder + 10-prompt table + one sentence on skill vs.
  hook

## Module 5 — Instructions That Actually Work
- Big idea: the agent can only work with what you actually tell it — a
  vague ask gets a guess, a clear ask gets what you meant
- Hands-on: ask for the same small feature three ways (vague → specific
  → very specific) and compare what you get each time
- Checkpoint: which version worked best, and why — not just "the last
  one," but what specifically made the difference

## Module 6 — Write It Down First
- Big idea: for anything bigger than a one-liner, writing down what you
  want *before* the agent starts (like a short game design doc) saves
  more time than it costs
- Hands-on: write a one-page plan for a real feature in your project;
  hand it to the agent as the only instructions
- Checkpoint: what did you have to fix in your written plan once you saw
  what the agent built from it?

## Module 7 — Keep It Looking Consistent
- Big idea: if you don't write down your colors, fonts, and spacing
  somewhere real, every session the agent will guess differently — and
  your project will look stitched together from different projects
- Hands-on: make a simple "style sheet" (colors, fonts, spacing) as an
  actual file, then build two different pages/screens using only that
  file as the guide
- Checkpoint: do the two pages actually match? Where did they not?

## Module 8 — Plan Before You Build
- Big idea: for a bigger change, agree on *how* it'll be done before any
  code changes — like agreeing on a route before a road trip, not
  turning left because it felt right in the moment
- Hands-on: use plan mode on a change that touches more than one file;
  review the plan before approving it
- Checkpoint: did the actual build match the plan? What changed and why?

## Module 9 — Prove It Works
- Big idea: a test is a way of proving your code does what you think it
  does, instead of trusting that it looks right
- Hands-on: describe a bug (or make one on purpose), have the agent write
  a test that fails because of it, then fix the bug so the test passes
- Checkpoint: the failing-test commit and the fix commit, kept separate

## Module 10 — Just Talk It Through
- Big idea: not everything needs a written plan — for small or
  exploratory stuff, just talking it out step by step is faster
- Hands-on: rebuild something small from Module 6, purely
  conversationally this time, no written plan
- Checkpoint: compare effort and quality against the Module 6 version —
  which would you actually use for something you cared about long-term?

## Module 11 — Two Heads Are Better
- Big idea: one agent can build something, and a *second*, fresh agent
  (that didn't build it) can check the work — like swapping papers with
  a classmate before turning them in
- Hands-on: have one session build a small feature, then a completely
  fresh session review it without being told how it was built
- Checkpoint: what did the second agent catch that you and the first
  agent missed?

## Module 12 — Don't Trust Blindly
- Big idea: agents sound confident even when they're wrong — made-up
  functions, missed edge cases, and (important) they can be tricked by
  sneaky instructions hidden in things they read off the internet
- Hands-on: review a piece of agent-built code specifically looking for
  mistakes, plus a short "spot the trick" exercise on prompt injection
- Checkpoint: list of anything you found, or an honest "found nothing,
  and here's how I checked"

## Module 13 — Automate the Boring Stuff
- Big idea: once something works, you can often get the agent to do it
  automatically going forward instead of by hand every time
- Hands-on: set up one small automation (e.g. auto-run your tests, or a
  saved routine for a repeated chore) with a clear approval step for
  anything that isn't fully reversible
- Checkpoint: what does this automation do on its own, and what does it
  still ask permission for? Why did you draw the line there?

## Module 14 — Rules of the Road
- Big idea: using AI help is normal now, but *how* you used it and
  whether you're honest about it matters — for a class project, a
  portfolio, or just your own sense of what you actually know how to do
- Hands-on: write your own short "AI use policy" for your next project or
  school assignment — when you'll use it, how you'll disclose it, what
  you'll always do yourself
- Checkpoint: the policy, plus one sentence on why each rule is there

## Module 15 — Capstone: Build & Show
- Big idea: put it all together on one real project you actually want to
  finish
- Hands-on: pick a project (site, game, bot, tool); write a short spec
  (Module 6), plan the approach (Module 8), test the core logic (Module
  9), and get a second-agent review (Module 11) before calling it done
- Checkpoint/deliverable: the finished project, your spec/plan/tests as
  artifacts, and a short walkthrough (written or spoken) explaining what
  you built and what the agent did vs. what you did

---

## Project track suggestions (pick one to carry through the course)

| Track | What Module 6's spec might cover | What Module 15's capstone could be |
|---|---|---|
| Personal site | A page layout and its content sections | A finished multi-page site with consistent design (Module 7) |
| Small game | One game mechanic (e.g. scoring, a level) | A playable mini-game with a few mechanics working together |
| Bot (Discord/Telegram) | One command's behavior | A bot with a handful of working, tested commands |
| School club tool | One piece of functionality the club needs | A working tool the club can actually use |
