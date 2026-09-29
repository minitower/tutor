# Syllabus

Each module: **Objectives → Key concepts → Lab → Deliverable**. Full detail
lives in `modules/<module-name>/lesson.md` (English) and `lesson.ru.md`
(Russian), each paired with a Marp slide deck (`slides.md`/`slides.ru.md`)
and a full instructor lecture script (`lecture.md`/`lecture.ru.md`) — see
the table in [README.md](README.md) for direct links to every module's
files in both languages.

---

## Module 1 — Foundations: How Agentic Coding Actually Works
- Objectives: explain the agent loop (plan → act with tools → observe →
  repeat); distinguish autocomplete-style assistance from agentic tools
- Key concepts: context windows, tool-use loop, memory/compaction, what
  "agentic" adds over chat
- Lab: run an agent on a small toy repo, log every tool call it makes,
  annotate why each one happened
- Deliverable: annotated tool-call trace + short writeup

## Module 2 — Prompting & Task Specification for Agents
- Objectives: write task descriptions that reduce agent guesswork
- Key concepts: context vs. instructions, acceptance criteria, constraints,
  common anti-patterns (vague asks, missing "done" definition)
- Lab: write 3 versions of the same feature request (vague → constrained
  → fully specified) and diff the agent's output for each
- Deliverable: 3 prompts + 3 diffs + comparison notes

## Module 3 — Document-Driven Development (DDD)
- Objectives: use a written spec as the contract an agent implements
  against, and keep it a living artifact
- Key concepts: PRD/spec anatomy (goals, non-goals, interfaces, edge
  cases, acceptance criteria), spec → plan → implementation → spec-update
  loop, repo-level agent docs (e.g. `CLAUDE.md`/`AGENTS.md`), stale-doc risk
- Lab: write a one-page spec for a real feature, hand it to an agent
  as the only task input, iterate until acceptance criteria pass
- Deliverable: spec doc + resulting diff + list of places the spec had to
  be corrected mid-implementation

## Module 4 — Deterministic Design Systems for AI-Generated UI
- Objectives: get visually consistent, reproducible UI output across
  independent agent sessions instead of drift from vague adjectives
- Key concepts: design tokens as concrete values (not prose), a design
  system doc for patterns/rationale, a repo-level rule that forces the
  agent to check both before generating UI, packaging repeated design
  work as a Skill, closing the loop with visual (not just text) review
- Lab: build a small multi-page UI across two fresh sessions using only a
  tokens file + design doc + repo rule (no verbal design guidance);
  compare against a third, unconstrained control session
- Deliverable: tokens file + design doc + repo-doc snippet + screenshots
  from all three sessions + a writeup of where consistency held and where
  it broke down

## Module 5 — Plan-First Workflows
- Objectives: separate planning from execution so scope is agreed before
  code changes
- Key concepts: plan mode / approval gates, Architecture Decision Records
  (ADRs) as agent input, how this differs from DDD (ephemeral plan vs.
  durable doc)
- Lab: use a plan-first workflow on a multi-file refactor; require an
  explicit plan approval step before any edit
- Deliverable: approved plan + resulting diff; note any plan/execution
  divergence

## Module 6 — Test-Driven Development with Agents
- Objectives: use tests as an executable spec for an agent
- Key concepts: red/green/refactor with an agent driving, example-based vs.
  property-based tests, why failing tests reduce agent hallucination
- Lab: give an agent a bug report only; require it to write a failing
  test first, then fix
- Deliverable: failing test commit + fix commit, kept separate

## Module 7 — Conversational / Iterative Development
- Objectives: run a tight feedback loop for exploratory or small tasks
  without upfront documentation
- Key concepts: incremental correction, detecting and recovering from
  agent drift, session/context management on long conversations
- Lab: build the same small feature from Module 3 purely conversationally,
  no spec doc; compare effort and output quality
- Deliverable: side-by-side comparison vs. the Module 3 result

## Module 8 — Multi-Agent Orchestration
- Objectives: compose more than one agent role on a single task
- Key concepts: implementer/reviewer split, orchestrator/worker fan-out,
  critic-executor loops, when parallelism helps vs. adds coordination cost
- Lab: set up a two-agent pipeline — one implements, a second reviews
  before merge — on a nontrivial change
- Deliverable: pipeline transcript + list of issues the reviewer agent
  caught that the implementer missed

## Module 9 — Verification & Review of Agent Output
- Objectives: build the habit of verifying before trusting
- Key concepts: hallucinated APIs, silent scope creep, security review for
  AI-written code, prompt-injection risk from untrusted content the agent
  reads (web pages, tickets, docs)
- Lab: run a structured review pass (correctness + security) on code
  produced in an earlier module's lab
- Deliverable: review checklist filled out + findings

## Module 10 — CI/CD & Automating Agent Workflows
- Objectives: let agents participate in pipelines safely
- Key concepts: hooks, scheduled/triggered agents, agents-in-CI (auto-fix
  lint, triage issues), permission scopes and sandboxing, human-in-the-loop
  gates for irreversible actions
- Lab: wire an agent into one CI step or git hook with an explicit
  approval gate for anything destructive
- Deliverable: working pipeline config + a written note on what it's
  *not* allowed to do unattended and why

## Module 11 — Governance, Safety & Team Adoption
- Objectives: decide, as a team, when to require which methodology
- Key concepts: disclosure norms for AI-assisted commits, review
  requirements, a decision framework (task type → methodology), measuring
  velocity/quality impact, common team-level failure modes
- Lab: build a one-page team policy + decision tree from the course's
  methodology comparison matrix
- Deliverable: team policy doc

## Module 12 — Capstone
- Objectives: combine methodologies deliberately on one real feature
- Format: pick a spec-worthy feature; use DDD for the spec, plan-first for
  the approach, TDD for the core logic, and a reviewer agent before
  merge
- Deliverable: repo + spec doc + plan + tests + review notes + a retro
  comparing this to how you'd have built it solo, six months ago

---

## Appendix: Methodology Comparison (to build out in Module 11)

| Methodology | Best for | Weak for | Artifact left behind |
|---|---|---|---|
| DDD (spec-first) | Features with real ambiguity, multi-person context | Tiny fixes (overhead) | Durable spec doc |
| Plan-first | Refactors, risky multi-file changes | Fast exploration | Ephemeral plan (or ADR) |
| TDD-with-agent | Bug fixes, well-defined logic | Vague/exploratory UI work | Test suite |
| Conversational | Prototypes, one-off scripts, exploration | Anything needing a paper trail | None (chat history only) |
| Multi-agent review | High-stakes changes, security-sensitive code | Low-stakes/small changes (overhead) | Review transcript |
