---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Skills

## An Agent's Procedural Memory

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- What a skill is and why, when there is `CLAUDE.md`
- Anatomy: `SKILL.md`, frontmatter, supporting files
- Progressive disclosure, who invokes a skill and when, where skills live
- Arguments, dynamic context, scripts, `context: fork`
- Skill vs. CLAUDE.md vs. hook vs. MCP vs. subagent; the open standard
- Security, testing and iteration; the lab

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Write a skill: `SKILL.md`, frontmatter, links to files and scripts
2. Explain progressive disclosure and control who invokes a skill and when
3. Choose between a skill, `CLAUDE.md`, a hook, MCP and a subagent
4. Vet a skill for security and check that it triggers and works

---

<!-- Slide 4 -->

## The Problem: Procedures Bloat the Context

- You paste the same checklist or multi-step procedure into chat again and again
- A `CLAUDE.md` section grew from a fact into a **procedure** — and loads every session whether needed or not
- A **skill** is a folder with `SKILL.md` (instructions) and supporting files; the body loads **only when the skill is used**
- Invoke it by `/name` yourself or let the model decide from the description

> `CLAUDE.md` is facts that are always true. A skill is a procedure needed sometimes.

---

<!-- Slide 5 -->

## Anatomy of a Skill

```
.claude/skills/review-diff/
├── SKILL.md         # обязательный: frontmatter + инструкции
├── security.md      # подробный чек-лист (читается по ссылке)
├── examples.md      # примеры вывода
└── scripts/
    └── scope_check.sh   # исполняется, не загружается в контекст
```

```markdown
---
name: review-diff
description: Проводит структурированное ревью диффа по чек-листу (корректность, объём, безопасность, injection, переиспользование). Используй, когда просят проверить дифф, PR или «посмотри мои изменения» перед мержем.
allowed-tools: Bash(git diff *) Bash(git log *)
---
# Ревью диффа
1. `git diff --stat` — оцени объём относительно задачи.
2. Пять проходов: корректность → объём → безопасность → injection → переиспользование.
3. Выведи находки таблицей: файл, строка, риск, предложение.
Подробный чек-лист безопасности — в [security.md](security.md).
```

---

<!-- Slide 6 -->

## Frontmatter: Key Fields

| Field | Purpose |
|---|---|
| `description` / `when_to_use` | **what it does and when to use it** — the model decides from it; capped at ~1,536 characters combined |
| `name` | the `/name` command (defaults to the folder name) |
| `disable-model-invocation` | only you can invoke (deploy, commit, send) |
| `user-invocable: false` | only the model (background knowledge) |
| `allowed-tools` / `disallowed-tools` | pre-approve / remove tools for the turn |
| `context: fork` + `agent` | run in an isolated subagent |
| `paths`, `hooks`, `model`, `effort`, `arguments` | path-based activation, hooks, model, effort, named arguments |
| `license`, `compatibility`, `metadata` | fields of the open Agent Skills standard |

All fields are optional; `description` is recommended. Claude Code silently ignores an unknown field — a typo raises no error.

---

<!-- Slide 7 -->

## Progressive Disclosure: Three Levels

That is why a skill is cheap: a hundred skills cost only the description listing. With many skills some descriptions get trimmed to the budget — keep `description` short with the key phrase first.

---

<!-- Slide 8 -->

## Who Invokes a Skill and When

| Setting | You (`/name`) | Model | In context |
|---|---|---|---|
| default | yes | yes | description always; body on invocation |
| `disable-model-invocation: true` | yes | **no** | no description; body on your invocation |
| `user-invocable: false` | no | yes | description always; body on invocation |

- Side effects (`/deploy`, `/commit`, sending messages) — only with `disable-model-invocation: true`: you don't want the model deciding to deploy "because the code looks ready"
- An invoked skill stays in the conversation as one message; `allowed-tools` applies only for that turn

---

<!-- Slide 9 -->

## Where Skills Live

| Level | Path | For whom |
|---|---|---|
| Enterprise | `.claude/skills/` in the managed settings directory | everyone on the organization's machines |
| Personal | `~/.claude/skills/<имя>/SKILL.md` | you, in all projects |
| Project | `.claude/skills/<имя>/SKILL.md` | everyone in the repo — commit it |
| Nested | `<подкаталог>/.claude/skills/` | monorepos: loads when working on files there |
| Plugin | `<plugin>/skills/<имя>/` | a team via a plugin, name `/plugin:skill` |
| claude.ai | account skills | Cowork, cloud sessions |

Old `.claude/commands/*.md` keep working — commands have been merged into skills.

---

<!-- Slide 10 -->

## A Good Description

**Bad**

"Helps with review"

**Good**

"Runs a structured diff review against a checklist (correctness, scope, security). Use when asked to check a diff, a PR or 'look at my changes' before merging."

- Formula: **what it does** + **when to use it** + **phrases the user would actually say**
- Key case first: a long description gets truncated
- Fires wrongly → narrow the description; doesn't fire → add real phrases or invoke `/name`

---

<!-- Slide 11 -->

## Arguments and Dynamic Context

```markdown
---
name: fix-issue
description: Разобрать и исправить GitHub issue по нашему стандарту
argument-hint: [номер-issue]
disable-model-invocation: true
---
Исправь issue $ARGUMENTS: сначала воспроизведи, затем тест, затем правка.

## Состояние репозитория (выполняется ДО отправки модели)
!`git status --short`
```

- `/fix-issue 123` → `$ARGUMENTS` = `123`; there are also `$0`, `$1` and named ones (`arguments:`)
- A line with an exclamation mark and a command in backticks runs **before** the model, and its output is substituted into the prompt — the model gets data, not the command
- Works only in Claude Code, not in claude.ai chat or via the API

---

<!-- Slide 12 -->

## Scripts: Determinism Inside a Skill

```markdown
---
name: render-chart
description: Строит график из CSV. Используй, когда просят визуализировать данные из CSV.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---
Запусти `${CLAUDE_SKILL_DIR}/scripts/render.sh <файл.csv>` и покажи путь к PNG.
```

- A script is **executed**, not read by the model: it costs no context and gives the same result every time
- `${CLAUDE_SKILL_DIR}` is the skill folder; the same path in the text and in `allowed-tools` allows the run without a prompt
- Anything code can compute (scope check, formatting, parsing) goes into a script

---

<!-- Slide 13 -->

## context: fork — a Skill in a Subagent

```markdown
---
name: pr-summary
description: Суммаризирует изменения в pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---
## Контекст PR
- Дифф: !`gh pr diff`
## Задача
Кратко опиши изменения и риски.
```

- The skill runs in a **separate subagent** with a clean context: it doesn't see your conversation — instructions must be self-contained
- `agent:` picks the type (e.g. `Explore` — read-only); it runs in the background by default
- Fits tasks with an explicit assignment; guidelines like "use these API conventions" are pointless in a fork

---

<!-- Slide 14 -->

## Skill, CLAUDE.md, Hook, MCP, Subagent

| Mechanism | What for | When in context | Guarantee |
|---|---|---|---|
| `CLAUDE.md` | always-true facts and conventions | always | the model may ignore it |
| **Skill** | an on-demand procedure | when used | the model may ignore it |
| **Hook** | mandatory behavior | outside the model | **deterministic** |
| **MCP** | access to an external system | tool descriptions | the server's permissions |
| **Subagent** | context isolation or a role | a separate context | tool boundaries |

> A skill is advice. A hook is law. If a rule must always hold, it's a hook (Module 13).

---

<!-- Slide 15 -->

## The Open Standard and Distribution

- **Agent Skills** (`agentskills.io`) is an open spec for the `SKILL.md` format; standard fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
- Claude Code understands more fields; but uploading to claude.ai or the Skills API rejects an extra field (`argument-hint`) with an **error** — for portability stick to the six
- Distribution: commit to `.claude/skills/`, a **plugin**, organization managed settings; examples — the `anthropics/skills` repo
- The MCP extension **Skills over MCP**: skills discovered through MCP (Module 2)
- Memory systems (Module 3, the Skill asset in TencentDB Agent Memory) go further: they **extract** skills from completed tasks

---

<!-- Slide 16 -->

## Skill Security

- A skill is **instructions + scripts**: it runs code and commands with your privileges
- `allowed-tools` can grant itself broad rights; workspace trust does **not** gate this field — read `allowed-tools` of skills in foreign repos
- A third-party skill is a supply chain and **prompt injection with authority**: its text reads as an instruction
- Control: `Skill(deploy *)` in deny, `Skill(commit)` in allow; `Skill` in deny disables all skills; side effects — `disable-model-invocation: true`
- Vet skills like code: review, `CODEOWNERS` on `.claude/skills/`, pin plugin versions

---

<!-- Slide 17 -->

## Testing and Iteration

- "The skill triggered" ≠ "it did the right thing" — check **twice**: it triggers on the right requests and the output is right
- A set: 5 prompts where it **should** fire, 5 where it **shouldn't**; run in a fresh session
- Baseline comparison: the same prompt **with** and **without** the skill — is it better and at what cost (tokens, time)
- Tools: the `skill-creator` plugin (evals, benchmark, description tuning), `claude plugin eval` for skills in a plugin, `claude plugin validate .claude/skills` for broken YAML, `/doctor` and `--debug`
- Broken YAML raises no error: the skill loads with empty metadata, `/name` works but the model can't find it

---

<!-- Slide 18 -->

## Lab — Package a Procedure as a Skill

1. Pick a repeated procedure from the course (diff review from Module 12, release-notes draft, scope-creep checklist)
2. Build the skill: `SKILL.md` with a good `description`, details in a separate file, the deterministic part in a script
3. Write a set of 5 "should" + 5 "shouldn't" prompts and run them in fresh sessions; tune until it fires right
4. Compare results with and without the skill; record the difference in quality and cost
5. For a skill with a side effect set `disable-model-invocation: true` and add a deny rule; a security note

---

<!-- Slide 19 -->

## Deliverable

- The skill folder (`SKILL.md`, supporting files, a script)
- A set of 10 prompts and a results table: triggering, quality with vs. without the skill
- A security note: permissions, `allowed-tools`, who can invoke

---

<!-- Slide 20 -->

## Next: Prompting & Task Specification

A skill is procedural memory: it loads when needed and doesn't bloat context. But it is advice, not law: pin what's mandatory with hooks, and vet foreign skills like code.

Now the agent has hands (MCP), memory and skills — next we learn to give it precise instructions.
