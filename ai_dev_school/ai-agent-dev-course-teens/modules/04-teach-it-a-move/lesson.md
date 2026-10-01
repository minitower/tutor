# Module 4 — Teach It a Move

## Big idea

If you keep pasting the same instruction to the agent ("add a level like this", "write commits in this style"), you can package it as a **skill** — a folder with a `SKILL.md` file. The agent always reads the skill's description but the full instruction only when needed, so skills cost almost nothing. You can invoke a skill yourself (`/add-level`) or let the agent decide from the description. A skill is *advice*, not law: what must always hold is enforced with hooks (Module 13). And a skill is code with privileges, so foreign skills get read before they run.

## Why it matters

Skills turn "how I do this" into a repeatable tool: the same result, less text in every request, and you can hand them to a team or club. But a bad description and the skill won't fire, and a good skill that fires at the wrong time is annoying.

## Hands-on task

**Part A — package a move:**
1. Pick a repeated task in your project (a new level, a new bot command, a commit format, a pre-merge check).
2. Create `.claude/skills/<name>/SKILL.md` with a good `description` (what it does + when to use it + phrases you'd say). Put details in a separate file and whatever code can compute in a script.

**Part B — check it triggers:**
1. Write 5 prompts where the skill *should* fire and 5 where it *shouldn't*. Run each in a fresh session.
2. Tweak the `description` until the results are right.

**Part C — compare with a baseline:**
1. Run the same request with and without the skill. Is it better? At what cost (length, time)?

**Part D — safety:**
1. If the skill has a side effect (publishing, sending, deleting), set `disable-model-invocation: true`.
2. Check `allowed-tools`: is there anything extra?

## Checkpoint

- The skill folder (`SKILL.md` + supporting files)
- A table of 10 prompts: fired / didn't, and a final "with / without the skill" comparison
- One sentence: why a skill is advice and a mandatory rule is better made a hook

## Supervisor note

**A skill = instructions + possible commands.** Let the teen write skills only for safe actions inside the project folder: no publishing, no sending messages, no deleting. Read foreign skills from the internet together before installing — especially the `allowed-tools` field. A skill with a side effect must be invoked manually only.
