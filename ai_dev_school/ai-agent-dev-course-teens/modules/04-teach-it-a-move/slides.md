---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Teach It a Move

Module 4 — Build With AI

---

<!-- Slide 2 -->

## Today

- The problem: the same instruction again and again
- What a skill is and how it's built
- How the agent finds a skill — and why the description matters
- Scripts inside a skill
- Skill, `CLAUDE.md`, hook — what to choose
- Skill safety and testing

---

<!-- Slide 3 -->

## The Same Thing Again and Again

- "Add a level like this..." — pasting it into chat for the fifth time
- Or your notes grew in `CLAUDE.md` and load *every* time
- A **skill** is a folder with an instruction: the agent reads it **only when needed**
- From Module 3: this is *procedural* memory

---

<!-- Slide 4 -->

## What a Skill Is Made Of

```
.claude/skills/add-level/
├── SKILL.md          # required: description + steps
├── format.md         # details (read via a link)
└── scripts/
    └── check_level.py   # is run, not read
```

Everything is optional except `SKILL.md`: the top of the file (frontmatter) is metadata, then comes the instruction.

---

<!-- Slide 5 -->

## An Example SKILL.md

```markdown
---
name: add-level
description: Adds a new level to the game in our level format. Use when the user asks to add, create or design a new level.
---
1. Read `levels/level_template.json` and the two newest levels.
2. Create `levels/level_NN.json` in the same format, slightly harder than the last.
3. Run `python tools/check_level.py levels/level_NN.json`; fix any errors.
4. Summarize what changed in three bullets.
```

---

<!-- Slide 6 -->

## The Description Decides Everything

- The agent decides whether to invoke a skill **from its `description`**
- Formula: **what it does** + **when to use it** + **phrases you'd say**
- Bad: "helps with levels"
- Good: "Adds a level in our format. Use when asked to add or design a new level."
- Fires wrongly → narrow it; doesn't fire → add real phrases

---

<!-- Slide 7 -->

## Three Loading Levels

1. **Always in context:** only the name and description (the skill list)
2. **When the skill is invoked:** the `SKILL.md` body
3. **On demand:** supporting files; scripts are **run**, not read at all

So you can have many skills without bloating the context. But descriptions over ~1,500 characters get trimmed — write short, main point first.

---

<!-- Slide 8 -->

## Who Invokes a Skill

- By default: both **you** (`/add-level`) and the **agent** from the description
- `disable-model-invocation: true` — only you. For anything with a side effect: publishing, sending, deploying
- `allowed-tools` — pre-approve the needed commands for this turn
- A skill can't *forbid* — it's advice; pin what's mandatory with a **hook** (Module 13)

---

<!-- Slide 9 -->

## Scripts Inside a Skill

- Whatever code can compute — format checks, parsing — put in a script
- A script is **run**: it costs no context and gives the same result
- In a skill step: "run `python ${CLAUDE_SKILL_DIR}/scripts/check_level.py`"
- `${CLAUDE_SKILL_DIR}` is the path to the skill folder
- Same principle as "trust but verify": part of the check lives in code, not in the agent's head

---

<!-- Slide 10 -->

## Skill, CLAUDE.md or Hook?

- **`CLAUDE.md`** — always-true facts ("the game is on Pygame"); always loaded
- **Skill** — a procedure needed sometimes ("how to add a level")
- **Hook** — a rule that *must* hold, outside the agent
- **MCP** — access to outside data (Module 2)
- A skill is advice. A hook is law.

---

<!-- Slide 11 -->

## A Skill Is Code With Privileges

- A skill is instructions + possible commands: it can run programs
- A foreign skill from the internet is like a foreign program **and** a foreign instruction (prompt injection with authority)
- Read `SKILL.md` and the scripts **before** installing; especially `allowed-tools`
- A project from someone else's repo may carry skills too — look in `.claude/skills/`
- Permission rules can deny a specific skill: `Skill(deploy *)`

---

<!-- Slide 12 -->

## How to Test a Skill

- "It fired" ≠ "it did it right" — check **twice**
- 5 prompts where it **should** fire and 5 where it **shouldn't** — in a fresh session
- The same request **with** and **without** the skill: is it better, and at what cost
- Broken YAML raises no error: `/name` works but the agent can't find the skill — use `--debug`
- There are ready helpers: the `skill-creator` plugin (checks and a benchmark)

---

<!-- Slide 13 -->

## Hands-On

**A.** Package a repeated move as a `SKILL.md` with a good description

**B.** 5 "should" + 5 "shouldn't" prompts; tweak the description

**C.** Compare "with the skill" and "without"

**D.** Safety: `disable-model-invocation`, check `allowed-tools`

---

<!-- Slide 14 -->

## Checkpoint

- The skill folder
- A table of 10 prompts + a "with / without" comparison
- One sentence: why a skill is advice and the mandatory is a hook

---

<!-- Slide 15 -->

## Recap

- A skill = a folder with `SKILL.md`; read only when needed
- It all hangs on a good `description`
- Scripts give the same result; hooks give obligation
- A skill is code with privileges: read foreign ones, test your own

---

<!-- Slide 16 -->

## Next Up

**Module 5 — Instructions That Actually Work**

Your agent now has hands (MCP), memory and skills. Next: how to give it instructions clear enough that it doesn't have to guess.
