# Supervisor Guide

Read this before Module 0. This course has a teen using a real, capable
coding agent, not a toy — the safety model is "sandboxed and supervised,"
not "the tool is inherently limited." That's a deliberate choice: the
whole point is to build real, working things, but it means a few setup
steps and ongoing checks are the supervising adult's job, not something
the course can enforce on its own.

## Before Module 0: setup

- **Dedicated project folder.** Create one folder for this course's
  projects only (e.g. `~/teen-coding-projects`). Never point the agent
  at a folder containing personal files, family documents, financial
  files, or anything unrelated — an agent can read and edit anything in
  its working directory and below.
- **A throwaway or low-stakes account for anything account-based.** If a
  project needs a GitHub account, an API key, a bot token, etc., set up
  a new one for this course rather than reusing a personal/family
  account.
- **Restrictive permission mode.** Claude Code (and similar tools) can
  run in modes that ask before every action, or modes that act more
  autonomously. Start restrictive — approval required for file edits and
  any command execution — and only relax it for specific, well-understood
  steps once you've both seen how it behaves.
- **No payment methods, no real credentials.** Nothing in this course
  should ever involve entering a real password, API billing key tied to
  a card, or personal ID information into anything the agent touches or
  can see.

## What to watch for during sessions

- **Does the teen understand what happened, not just that it worked?**
  If a module's checkpoint gets a shrug and "the AI did it," that's the
  signal to slow down and re-do the reflection step, not move on.
- **Scope creep.** Agents sometimes do more than asked. Spot-check diffs
  occasionally, especially once permissions relax — it's a good teaching
  moment either way ("look what it did that we didn't ask for").
- **Frustration vs. productive struggle.** Some confusion is the point
  (Module 12 exists because agents *do* get things wrong). Persistent
  frustration where the teen has disengaged and is just accepting
  whatever the agent outputs is the moment to step back in.
- **Anything touching the open internet.** If a task has the agent fetch
  a web page, read an external API, or post/send anything, that's a
  moment for you to be present — untrusted content the agent reads can
  contain text aimed at manipulating it, and this is covered directly in
  Module 12, but the first few times are worth watching together.

## What not to worry about

- Making mistakes in the code itself. That's normal and expected — this
  isn't a course about writing perfect code, it's about directing a tool
  well. Bugs are a feature of the learning process, not a failure.
- The teen "just copying what the agent says" early on. Module 1–5 build
  toward understanding; it's fine if the first session or two is mostly
  watching and getting oriented.

## A note on trust, not restriction, as the goal

The permission settings above are a starting point, not a permanent
cage. Part of what this course teaches (Module 12, Module 14) is how to
reason about *when* more autonomy is appropriate — the goal is a teen who
can eventually make that call themselves, the same way a driving
curriculum starts supervised and ends with an independent driver who
understands *why* the rules existed in the first place.

## Modules 2–4 (MCP, memory, skills): extra notes

- **Module 2 (MCP) is an elevated-attention module.** An MCP server is a
  program that runs on the teen's computer, and what it returns is
  untrusted text. Connect only servers the teen wrote or that you both
  read (the official reference examples). Read-only access, test data
  only; no tokens or passwords from personal accounts; never paste an
  `npx -y ...` command from a random page.
- **Module 3 (memory):** memory files are data. Review them before any
  commit or publish: no real names, addresses, school, phone numbers,
  passwords, or other people's personal data (especially other minors, if
  a bot has users). The teen should be able to view, edit and delete any
  memory entry. Treat memory systems that store data on a server as any
  other service holding personal data.
- **Module 4 (skills):** a skill can run commands. Keep the teen's skills
  to safe actions inside the project folder (no publishing, sending or
  deleting), require manual invocation for anything with a side effect,
  and read skills from the internet together — especially `allowed-tools`
  — before installing them.
