# Module 4 — Lecture Script: Skills: Agent Capabilities

*Speaking notes for the instructor. Slide numbers match `slides.md` exactly.
Timing notes are suggestions for a live 2–2.5 hour session (lecture + lab).*

---

## Opening (Slides 1–3) — ~10 min

### Slide 1 — An Agent's Procedural Memory

The third module of this block — skills. In Module 3 we called skills procedural memory, and in Module 7 we will package design work as a skill. Now the whole mechanism: what it is, how it loads, who invokes it, how to keep it safe and how to test it.

### Slide 2 — Agenda

We start with the problem, then anatomy, progressive disclosure, invocation and location. Then practical techniques — arguments, scripts, fork. Then comparison with other mechanisms, security and testing. The lab: package a procedure from the course as a skill and test it.

### Slide 3 — Objectives

Four objectives. Note that two are about control: who invokes and how safely. A skill isn't just convenience; it's a mechanism with privileges and side effects.

---

## What a Skill Is and How It's Built (Slides 4–8) — ~30 min

### Slide 4 — The Problem: Procedures Bloat the Context

The classic situation: for the tenth time you're pasting the same checklist into chat. Or a CLAUDE.md section has grown from a fact into a whole procedure and loads every session even when not needed. A skill solves both: it's a folder with SKILL.md and supporting files, and the body loads only when the skill is used. Invoke it manually with a slash command or let the model decide from the description. The line from the quote is easy to remember: CLAUDE.md is facts that are always true; a skill is a procedure needed sometimes.

### Slide 5 — Anatomy of a Skill

Anatomy. Only SKILL.md is required: frontmatter between three dashes and instructions below. Next to it — anything: a detailed checklist, examples, scripts. The slide shows a minimal working example — the Module 12 diff review. Note three things: the description says both what it does and when to use it; the text links to security.md, which is read only if needed; allowed-tools pre-approves two safe git commands.

### Slide 6 — Frontmatter: Key Fields

The frontmatter fields. All are optional, but description is recommended — the model decides from it whether to invoke; together with when_to_use it is capped at about fifteen hundred characters. Then the control fields: disable-model-invocation, user-invocable, allowed-tools, disallowed-tools, context fork with agent, paths — activation only when working on matching files, hooks. And the open-standard fields: license, compatibility, metadata. An important detail: Claude Code ignores an unknown field without error — a typo in a field name silently disables your setting.

### Slide 7 — Progressive Disclosure: Three Levels

The key idea is progressive disclosure, three levels. First: name and description are always in context, a list of skills so the model knows what exists. Second: the SKILL.md body loads when the skill is invoked. Third: linked files are read on demand, and scripts aren't loaded at all but executed. That's why a skill is cheap: a hundred skills cost only the description listing. The flip side: with many skills some descriptions are trimmed to the budget and the model loses keywords — keep descriptions short with the main point first.

### Slide 8 — Who Invokes a Skill and When

Who invokes — an important table. By default both you and the model; the description is always in context. With disable-model-invocation only you: the description isn't even loaded. With user-invocable false only the model — for background knowledge that makes no sense as a command. The practical rule: anything with side effects — deploy, commit, send — only disable-model-invocation true. You don't want the model deciding to deploy because the code looks ready. One more nuance: an invoked skill stays in the conversation as one message, while allowed-tools applies only for that turn.

---

## Locations, Descriptions, Arguments, Scripts, Fork (Slides 9–13) — ~35 min

### Slide 9 — Where Skills Live

Where skills live. Personal — in the home directory, for all your projects. Project — in the repo's .claude/skills: commit it and the team gets it. Nested — in monorepo subdirectories, loaded when working on files there. Plugin — distribution to a team via a plugin. Enterprise — through organization managed settings. Plus claude.ai account skills. Old files in .claude/commands keep working: commands were merged into skills, and skills add supporting files and invocation control.

### Slide 10 — A Good Description

The description decides whether a skill fires. On the left, bad: "helps with review" — too vague, it fires wrongly or never. On the right, good: what it does, when to use it, the phrases people ask with. The formula: what it does plus when to use it plus real user phrases. Put the key case first. Diagnosis: fires wrongly — narrow it; doesn't fire — add real phrases, and meanwhile invoke by name.

### Slide 11 — Arguments and Dynamic Context

Two techniques. Arguments: when invoked by slash command with an issue number, the string is substituted for ARGUMENTS; there are also positional and named ones. Dynamic context: an exclamation mark and a command in backticks executes before the text goes to the model and its output is substituted — the model gets data, not the command. This works only in Claude Code: in claude.ai chat and via the API such blocks aren't executed.

### Slide 12 — Scripts: Determinism Inside a Skill

The most underrated technique is scripts. If code can compute something — a scope check, formatting, parsing — don't ask the model, put it in scripts. A script is executed, not read: it costs no context and gives the same result. The CLAUDE_SKILL_DIR variable points to the skill folder, and if the same path is in both the text and allowed-tools, the run passes without a prompt. This is determinism inside a non-deterministic system — an idea from Module 12.

### Slide 13 — context: fork — a Skill in a Subagent

Context fork runs a skill in a separate subagent with a clean context. The example is a PR summary: an Explore-type agent only reads, and the diff is substituted by dynamic context. The constraint: the subagent doesn't see your conversation, so instructions are self-contained, and by default it runs in the background. And a warning: fork suits only skills with an explicit assignment — guidelines like "use these API conventions" without a task return an empty result.

---

## Choosing a Mechanism and the Open Standard (Slides 14–15) — ~15 min

### Slide 14 — Skill, CLAUDE.md, Hook, MCP, Subagent

How to choose the mechanism. CLAUDE.md — always-true facts, always loaded; the model may ignore it. A skill — an on-demand procedure; also may be ignored. A hook — mandatory behavior, outside the model, deterministic. MCP — access to an external system. A subagent — context isolation or a role. The main takeaway in the quote: a skill is advice, a hook is law. If a rule must always hold, a skill won't save you — that's Module 13.

### Slide 15 — The Open Standard and Distribution

The open standard. Agent Skills is an open spec for the SKILL.md format, six fields. Claude Code understands more, but uploading to claude.ai or the Skills API rejects an extra field with an error — for portability stick to the standard ones. Distribution: a repo commit, a plugin, managed settings; examples — the anthropics/skills repository. There's an MCP extension, Skills over MCP — delivering skills through MCP. And the link to Module 3: memory systems like TencentDB Agent Memory go further and extract skills from completed tasks — turning experience into procedural memory.

---

## Security and Testing (Slides 16–17) — ~20 min

### Slide 16 — Skill Security

Security. A skill is instructions plus scripts, i.e. code execution with your privileges. A subtlety: allowed-tools can grant itself broad rights, and workspace trust doesn't gate this field. So for skills from foreign repos read allowed-tools before running. A third-party skill is a supply chain and prompt injection with authority: its text is taken as an instruction. Control: Skill rules in permissions — allow for specific ones, deny for dangerous ones, deny on the whole Skill disables all. Side effects — manual only. And treat skills like code: review, CODEOWNERS, pinned plugin versions.

### Slide 17 — Testing and Iteration

Testing. "The skill fired" doesn't mean "it did the right thing" — check twice. Write five prompts where the skill should fire and five where it shouldn't; run in a fresh session. Compare the same prompt with and without the skill: is it better and at what cost. Tools: the skill-creator plugin with evals and a benchmark, claude plugin eval, claude plugin validate for broken YAML, doctor and debug. And a trap: broken YAML raises no error — the skill loads with no metadata, the slash command works, but the model can't find it.

---

## Lab and Recap (Slides 18–20) — ~10 min

### Slide 18 — Lab — Package a Procedure as a Skill

The lab. Pick a repeated procedure from the course — diff review, release notes, scope-creep checklist. Build the skill: a good description, details in a separate file, the deterministic part in a script. Write ten prompts and tune the triggering. Compare with a no-skill baseline. If the skill has a side effect — disable-model-invocation, a deny rule and a security note.

### Slide 19 — Deliverable

Hand in: the skill folder, a set of ten prompts with a results table — triggering and quality with vs. without — and a security note. The results table matters more than the skill itself: it shows the student verified rather than believed.

### Slide 20 — Next: Prompting & Task Specification

Recap of Modules 2–4. MCP is hands: access to systems. Memory is what the agent remembers between sessions. Skills are procedures that load when needed. All three are advice and capability, not guarantees: pin what's mandatory with hooks and permissions, and vet everything that comes from outside like code. Next — Module 5, where we learn to write precise task specifications; you'll come back to MCP, memory and skills in the capstone.
