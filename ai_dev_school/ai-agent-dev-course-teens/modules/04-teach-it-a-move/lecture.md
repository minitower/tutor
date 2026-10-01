# Lecture Script — Module 4: Teach It a Move

Facilitator notes: this is a spoken script, not something to read word for word. Say it like you'd explain it to a smart teen who can already code and wants to know what actually matters here. The lecture portion should run **~20-25 minutes**; the rest of the module is the hands-on task and checkpoint. Slide numbers below match `slides.md` exactly. Keep the tone practical, not preachy: "here's why this protects you".

---

## Opening (~2 min)

## Slide 1 — Teach It a Move

"The last technical module. We've connected the agent to data and taught it to remember. Today: how to teach it a move that you repeat."

---

## Slide 2 — Today

"The plan: the problem of repeated instructions, what a skill is, how the agent finds one, scripts, choosing between a skill, CLAUDE.md and a hook, safety and testing."

---

## The Idea (~6 min)

## Slide 3 — The Same Thing Again and Again

"The situation: for the fifth time you paste 'add a level like this' into chat. Or the notes in CLAUDE.md have grown and load every time whether needed or not. A skill solves both: it's a folder with an instruction the agent reads only when needed. In Module 3 terms it's procedural memory."

---

## Slide 4 — What a Skill Is Made Of

"What it's made of. Only SKILL.md is required: metadata on top, the instruction below. Next to it you can put details in a separate file and scripts. A script isn't read, it's run — we'll come back to that."

---

## Slide 5 — An Example SKILL.md

"Here's an example for a game. A name, a description and four steps: read the template, create the level, run the check, report briefly. Notice the description says both what the skill does and when to use it."

---

## How It Works (~8 min)

## Slide 6 — The Description Decides Everything

"It all hangs on the description: the agent decides from it whether to invoke the skill. The formula: what it does, when to use it and the phrases you'd say. 'Helps with levels' is too vague. If the skill fires wrongly — narrow it; if it doesn't fire — add real phrases."

---

## Slide 7 — Three Loading Levels

"Three loading levels. Always in context — only the name and description. When invoked — the SKILL.md body. On demand — supporting files, and scripts are simply run. So you can have many skills without bloating context. But long descriptions are trimmed, so write short and main point first."

---

## Slide 8 — Who Invokes a Skill

"Who invokes. By default both you, by slash command, and the agent, from the description. For anything with a side effect — publishing, sending, deploying — set disable-model-invocation true so only you invoke it. allowed-tools pre-approves the needed commands for this turn. And above all: a skill is advice. It can't forbid anything; what's mandatory is pinned with a hook from Module 13."

---

## Choosing and Safety (~6 min)

## Slide 9 — Scripts Inside a Skill

"Scripts. Whatever code can compute — format checks, parsing — put in a script. It's run, not read: it costs no context and gives the same result. The skill folder path is the CLAUDE_SKILL_DIR variable. Same 'trust but verify' principle: part of the check lives in code, not in the agent's head."

---

## Slide 10 — Skill, CLAUDE.md or Hook?

"What to choose. CLAUDE.md — always-true facts. A skill — a procedure needed sometimes. A hook — a rule that must hold, outside the agent. MCP — access to outside data. Remember the formula: a skill is advice, a hook is law."

---

## Slide 11 — A Skill Is Code With Privileges

"Safety. A skill is instructions plus possible commands. A foreign skill from the internet is like a foreign program and a foreign instruction at once. Read SKILL.md and the scripts before installing, especially allowed-tools. And remember a project from someone else's repo can carry skills too — look in .claude/skills. Permission rules can deny a specific skill."

---

## Hands-on and Recap (~3 min, then practice)

## Slide 12 — How to Test a Skill

"How to test. 'It fired' doesn't mean 'it did it right' — check twice. Five prompts where it should fire, five where it shouldn't, in a fresh session. The same request with and without the skill — is it better and at what cost. A trap: broken YAML raises no error, the slash command works but the agent can't find the skill. There's also a helper — the skill-creator plugin."

---

## Slide 13 — Hands-On

"Hands-on: package your move, write ten prompts, compare with a no-skill baseline, check safety."

---

## Slide 14 — Checkpoint

"Checkpoint: the skill folder, a table of ten prompts with the comparison and one sentence on why a skill is advice and the mandatory is a hook."

---

## Slide 15 — Recap

"Recap: a skill is a folder with SKILL.md; it all hangs on the description; scripts give repeatability, hooks give obligation; a skill is code with privileges. Next — the capstone, where you apply it all: data through MCP, memory and skills."

---

## Slide 16 — Next Up

"Next — Module 5: how to write instructions clear enough that the agent doesn't have to guess. You'll bring MCP, memory and skills back in the capstone."
