# Practice Tasks: Claude Code & Codex Craft

## Scope of this document

This is deliberately narrow. It does **not** include a sample API to
build, a tech-stack review, or any pre-written application code — that's
intentional. The point of these tasks is to practice *operating the
tools themselves* (Claude Code and/or Codex CLI). Whatever application
gets built as a side effect of a task is the learner's choice and the
learner's output, produced live during the exercise — not something
authored here in advance.

Four pillars, each with **how it works** (the mechanics) and a
**practice task** (what to actually do):

1. Technique — directing the agent well, session to session
2. Skills — packaging a repeatable capability the agent can invoke
3. Plugins — bundling and distributing skills/commands/agents as a unit
4. Docs — writing the instructions that make 1–3 actually work

Docs is listed last but is not optional or secondary — a skill or plugin
with a weak description/doc is one the agent won't reliably invoke, or a
teammate won't be able to use without you in the room. Every task below
ends with a documentation deliverable, not just working code.

---

## 1. Technique

### How it works
Claude Code and Codex are both agentic loops: you give a task, the agent
reads/plans/acts/observes in a loop, and stops when it thinks it's done
or when it needs your input. Technique is about shaping that loop from
the outside:
- **Session scoping** — one coherent goal per session; starting fresh
  when a session has drifted is usually faster than untangling it
- **Plan-first for anything nontrivial** — both tools support a
  plan/approval step before edits happen; use it for multi-file or
  ambiguous work, skip it for a one-line fix
- **Interrupt early, not late** — correcting direction after 2 wrong
  steps costs less than after 20
- **Context hygiene** — what you put in front of the agent early
  (open files, pasted errors, prior conversation) anchors everything that
  follows; irrelevant context measurably degrades output, it doesn't just
  waste tokens

### Practice task
Pick any real task you actually need done (a bug, a small feature, a
refactor — your call, don't overthink the pick). Run it twice, in two
separate sessions:
- **Run A:** direct it minimally — one-line task, no plan step, correct
  as you go
- **Run B:** same task, fresh session — scope it explicitly, use the
  plan/approval step, interrupt at the first sign of drift

**Deliverable:** a short note (not a full report) comparing turn count,
time, and whether you trusted the result enough to skip re-reading the
whole diff. No app code to hand in — the comparison *is* the deliverable.

---

## 2. Skills

### How it works
A Skill is a packaged, reusable instruction set the agent can load on
demand instead of you re-explaining a workflow every session.

- Lives as a directory with a `SKILL.md` file:
  - project-scoped: `.claude/skills/<skill-name>/SKILL.md`
  - user-scoped: `~/.claude/skills/<skill-name>/SKILL.md`
  - plugin-bundled: shipped inside a plugin (see §3), referenced as
    `<plugin-name>:<skill-name>`
- `SKILL.md` starts with YAML frontmatter — at minimum `name` and a
  `description` written so the agent can tell *when to trigger it*
  (the description is the only thing weighed to decide relevance before
  the skill's body is even loaded, so vague descriptions mean the skill
  quietly never fires)
- The body is the actual instructions/procedure — can reference sibling
  files (templates, scripts) that get pulled in only when the skill is
  used, keeping the base context window small
- Invoked either automatically (the agent matches your request against
  available skills' descriptions) or explicitly by name

### Practice task
Find a task you (or your team) does with Claude Code more than once with
roughly the same steps each time — e.g. "prep a PR description from the
diff," "run our specific lint+typecheck+test sequence and summarize
failures," "scaffold a new module following our repo's conventions."

1. Write the `SKILL.md` for it: name, a description precise enough that
   it triggers on the right requests and *not* on similar-but-different
   ones, and the procedure itself
2. Test triggering: ask for the task in normal language (not by skill
   name) and confirm it fires; then ask for something adjacent-but-
   different and confirm it does *not* fire
3. Iterate the description based on what you observe

**Deliverable:** the `SKILL.md` file, plus one line each on what request
correctly triggered it and what adjacent request you deliberately checked
did *not*.

---

## 3. Plugins

### How it works
A plugin bundles skills, custom slash commands, subagent definitions, and
hooks into one distributable, installable unit — the step up from "a
skill on my machine" to "a capability my team (or the world) can add."

- A plugin is a directory with a `.claude-plugin/plugin.json` manifest
  (name, version, description, author) plus any of: `commands/`,
  `agents/`, `skills/`, `hooks/`
- Plugins are distributed through a **marketplace** — a repo (or path)
  containing a `marketplace.json` that lists available plugins and where
  to fetch each one
- Installing: add the marketplace source, then install the specific
  plugin from it; once installed, its commands/skills/agents become
  available like built-in ones, namespaced as `<plugin>:<thing>`
- Update by re-pulling the marketplace source; uninstall removes the
  namespace cleanly — this is what makes a plugin the right unit for
  anything meant to be shared or versioned, versus a personal skill that
  just lives in your dotfiles

### Practice task
Take the skill you built in §2 (or a second small one) and package it as
a plugin:

1. Scaffold the plugin structure and manifest
2. Move the skill in under the plugin, confirm it's now addressed as
   `<your-plugin>:<skill-name>`
3. Stand up a minimal local marketplace pointing at it (a local path is
   enough — you don't need to publish anything)
4. Install it from that marketplace into a clean session and confirm it
   works exactly as it did standalone
5. Uninstall it and confirm it's fully gone (no orphaned namespace, no
   leftover behavior)

**Deliverable:** the plugin directory + marketplace file, and a one-line
note confirming the install/uninstall round-trip worked cleanly.

---

## 4. Docs

### How it works
Two different documentation surfaces matter here, and they're easy to
conflate:

- **Repo-level agent instructions** — `CLAUDE.md` (Claude Code) or
  `AGENTS.md` (Codex, also read by some other agentic tools) — standing
  context loaded every session: conventions, how to run tests, things
  the agent should never do in this repo. This is *not* a skill; it's
  ambient context with no trigger condition, so it should stay short —
  everything conditional belongs in a skill instead.
- **Skill/plugin-level docs** — the `description` field is doing double
  duty as both the trigger condition *and* the first thing a teammate
  reads to decide whether to use it. A description that's accurate for
  triggering but meaningless to a human reader (or vice versa) is a sign
  the skill is trying to do too much.

Bad docs in this context don't just confuse a human reader later — they
directly cause the artifact to misfire: a skill that under-triggers is
invisible, one that over-triggers hijacks unrelated requests, and a
`CLAUDE.md` that's stale actively steers the agent wrong.

### Practice task
Using the skill and plugin from §2–3:

1. Write or update this repo's `CLAUDE.md`/`AGENTS.md` to mention the new
   skill/plugin exists and when a session should reach for it
2. Have a fresh agent session (no memory of building it) read only the
   repo docs and attempt to use the skill/plugin correctly, purely from
   what's written — no hints from you
3. Note every point where it hesitated, guessed wrong, or needed a
   nudge — that's the gap between what you wrote and what was actually
   communicated
4. Fix the docs to close those gaps, then re-test

**Deliverable:** the doc diff (before/after) and the list of gaps found
in the cold-read test. This is the same "spec that survives contact with
an agent that didn't write it" discipline as Module 6's DDD lab, applied
to the tool's own configuration instead of a feature spec.

---

## Wrap-up

These four practice tasks can stand alone or slot into the existing
course as an added module (e.g. between Module 7, Deterministic Design
Systems, and Module 8, Plan-First Workflows, since Skills/plugins are
themselves a form of document-driven agent direction — a skill *is* a
spec the agent reads before acting). Suggest folding this in as
**Module 7.5 — Tooling Craft: Skills, Plugins, and Their Docs** if the
course runs as a cohort; as standalone practice otherwise.
