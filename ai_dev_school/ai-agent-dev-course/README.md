# Agentic Software Development: From Specs to Shipped Code

A hands-on course for professional developers who want to work effectively
with AI coding agents (Claude Code, Cursor, Copilot Workspace, Devin, etc.)
on real projects — not just autocomplete, but agents that plan, write,
test, and revise code across a whole task.

The course is organized as a set of **methodology case studies**. Each
module teaches one way of directing an agent — Document-Driven Development
(DDD), plan-first workflows, TDD-with-agents, conversational iteration,
multi-agent pipelines — and asks you to build the *same kind* of feature
with each one, so you can feel the tradeoffs directly instead of taking
them on faith.

## Who this is for

Intermediate-to-senior developers already comfortable writing and
reviewing code, who are new to (or inconsistent at) directing AI agents on
non-trivial tasks. Assumes no prior agent experience; does not re-teach
programming fundamentals.

## Format (assumed — adjust to taste)

- 15 modules, ~2–3 hours each (reading + lab), self-paced or as a 6-week
  part-time cohort (2 modules/week)
- Every module ends in a hands-on lab against a shared sample repo
- Capstone project in the final module
- Tool-agnostic where possible; examples default to Claude Code but the
  concepts transfer to any agentic coding tool

## Learning outcomes

By the end, a learner can:
1. Choose the right agent-direction methodology for a given task (bug fix
   vs. greenfield feature vs. large refactor vs. exploratory prototype)
2. Write specs and plans that an agent can execute against with minimal
   back-and-forth
3. Set up TDD and review loops that catch agent mistakes before they ship
4. Compose multiple agents (implementer/reviewer, orchestrator/workers)
5. Wire agents into CI/CD and team workflows with appropriate guardrails
6. Recognize and mitigate agent-specific failure modes (hallucinated APIs,
   silent scope creep, prompt injection from untrusted content)

## Structure

See [syllabus.md](syllabus.md) for the full outline. Per-module detail
lives in [modules/](modules/). [example-workflow.md](example-workflow.md)
is a worked, illustrative example threading Modules 6–9 and 12 together
on one feature — good to read before the Capstone, or before Module 6 to
see where the pieces land.

Each module folder now bundles four things: the written lesson, a Marp
slide deck, a full instructor lecture script, and — for every one of
those — a Russian counterpart (`*.ru.md`) alongside the English original.

| # | Module | Case study focus | Lesson | Slides | Lecture |
|---|--------|-------------------|--------|--------|---------|
| 1 | Foundations | How agentic loops actually work | [EN](modules/01-foundations/lesson.md) · [RU](modules/01-foundations/lesson.ru.md) | [EN](modules/01-foundations/slides.md) · [RU](modules/01-foundations/slides.ru.md) | [EN](modules/01-foundations/lecture.md) · [RU](modules/01-foundations/lecture.ru.md) |
| 2 | MCP | Connecting agents to external systems | [EN](modules/02-mcp/lesson.md) · [RU](modules/02-mcp/lesson.ru.md) | [EN](modules/02-mcp/slides.md) · [RU](modules/02-mcp/slides.ru.md) | [EN](modules/02-mcp/lecture.md) · [RU](modules/02-mcp/lecture.ru.md) |
| 3 | Agent Memory | Long-term memory, SOUL.md, layered memory systems | [EN](modules/03-agent-memory/lesson.md) · [RU](modules/03-agent-memory/lesson.ru.md) | [EN](modules/03-agent-memory/slides.md) · [RU](modules/03-agent-memory/slides.ru.md) | [EN](modules/03-agent-memory/lecture.md) · [RU](modules/03-agent-memory/lecture.ru.md) |
| 4 | Skills | Reusable agent procedures: SKILL.md, disclosure, security | [EN](modules/04-skills/lesson.md) · [RU](modules/04-skills/lesson.ru.md) | [EN](modules/04-skills/slides.md) · [RU](modules/04-skills/slides.ru.md) | [EN](modules/04-skills/lecture.md) · [RU](modules/04-skills/lecture.ru.md) |
| 5 | Prompting & Task Specification | Precision in, precision out | [EN](modules/05-prompting-and-specs/lesson.md) · [RU](modules/05-prompting-and-specs/lesson.ru.md) | [EN](modules/05-prompting-and-specs/slides.md) · [RU](modules/05-prompting-and-specs/slides.ru.md) | [EN](modules/05-prompting-and-specs/lecture.md) · [RU](modules/05-prompting-and-specs/lecture.ru.md) |
| 6 | Document-Driven Development | Spec docs as the source of truth | [EN](modules/06-document-driven-development/lesson.md) · [RU](modules/06-document-driven-development/lesson.ru.md) | [EN](modules/06-document-driven-development/slides.md) · [RU](modules/06-document-driven-development/slides.ru.md) | [EN](modules/06-document-driven-development/lecture.md) · [RU](modules/06-document-driven-development/lecture.ru.md) |
| 7 | Deterministic Design Systems | Tokens + design docs for reproducible UI | [EN](modules/07-deterministic-design-systems/lesson.md) · [RU](modules/07-deterministic-design-systems/lesson.ru.md) | [EN](modules/07-deterministic-design-systems/slides.md) · [RU](modules/07-deterministic-design-systems/slides.ru.md) | [EN](modules/07-deterministic-design-systems/lecture.md) · [RU](modules/07-deterministic-design-systems/lecture.ru.md) |
| 8 | Plan-First Workflows | Ephemeral plans + approval gates | [EN](modules/08-plan-first-workflows/lesson.md) · [RU](modules/08-plan-first-workflows/lesson.ru.md) | [EN](modules/08-plan-first-workflows/slides.md) · [RU](modules/08-plan-first-workflows/slides.ru.md) | [EN](modules/08-plan-first-workflows/lecture.md) · [RU](modules/08-plan-first-workflows/lecture.ru.md) |
| 9 | TDD with Agents | Tests as the spec | [EN](modules/09-tdd-with-agents/lesson.md) · [RU](modules/09-tdd-with-agents/lesson.ru.md) | [EN](modules/09-tdd-with-agents/slides.md) · [RU](modules/09-tdd-with-agents/slides.ru.md) | [EN](modules/09-tdd-with-agents/lecture.md) · [RU](modules/09-tdd-with-agents/lecture.ru.md) |
| 10 | Conversational / Iterative Dev | Tight loops, no upfront doc | [EN](modules/10-conversational-iterative-dev/lesson.md) · [RU](modules/10-conversational-iterative-dev/lesson.ru.md) | [EN](modules/10-conversational-iterative-dev/slides.md) · [RU](modules/10-conversational-iterative-dev/slides.ru.md) | [EN](modules/10-conversational-iterative-dev/lecture.md) · [RU](modules/10-conversational-iterative-dev/lecture.ru.md) |
| 11 | Multi-Agent Orchestration | Implementer/reviewer/orchestrator patterns | [EN](modules/11-multi-agent-orchestration/lesson.md) · [RU](modules/11-multi-agent-orchestration/lesson.ru.md) | [EN](modules/11-multi-agent-orchestration/slides.md) · [RU](modules/11-multi-agent-orchestration/slides.ru.md) | [EN](modules/11-multi-agent-orchestration/lecture.md) · [RU](modules/11-multi-agent-orchestration/lecture.ru.md) |
| 12 | Verification & Review | Trust but verify | [EN](modules/12-verification-and-review/lesson.md) · [RU](modules/12-verification-and-review/lesson.ru.md) | [EN](modules/12-verification-and-review/slides.md) · [RU](modules/12-verification-and-review/slides.ru.md) | [EN](modules/12-verification-and-review/lecture.md) · [RU](modules/12-verification-and-review/lecture.ru.md) |
| 13 | CI/CD & Automation | Agents as pipeline citizens | [EN](modules/13-cicd-and-automation/lesson.md) · [RU](modules/13-cicd-and-automation/lesson.ru.md) | [EN](modules/13-cicd-and-automation/slides.md) · [RU](modules/13-cicd-and-automation/slides.ru.md) | [EN](modules/13-cicd-and-automation/lecture.md) · [RU](modules/13-cicd-and-automation/lecture.ru.md) |
| 14 | Governance & Team Adoption | Norms, metrics, choosing a methodology | [EN](modules/14-governance-and-adoption/lesson.md) · [RU](modules/14-governance-and-adoption/lesson.ru.md) | [EN](modules/14-governance-and-adoption/slides.md) · [RU](modules/14-governance-and-adoption/slides.ru.md) | [EN](modules/14-governance-and-adoption/lecture.md) · [RU](modules/14-governance-and-adoption/lecture.ru.md) |
| 15 | Capstone | Combine methodologies on a real feature | [EN](modules/15-capstone/lesson.md) · [RU](modules/15-capstone/lesson.ru.md) | [EN](modules/15-capstone/slides.md) · [RU](modules/15-capstone/slides.ru.md) | [EN](modules/15-capstone/lecture.md) · [RU](modules/15-capstone/lecture.ru.md) |


## Open questions to settle before running this course

- Primary agent tool for labs: Claude Code specifically, or tool-agnostic?
- Cohort vs. self-paced (affects whether labs need a shared repo + grading)
- Target seniority: does this need a "Module 0" on agent basics for
  developers who've never used one at all?
