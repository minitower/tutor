# Module 1 — Project Documentation: From Idea to Spec

## Learning objectives
- Describe a product so that a developer, a tester and an AI agent all build the same thing
- Know which artifact answers which question, and which ones a small project can skip
- Keep docs in the repo in a form an agent can read and act on

## Lecture outline
1. Why document: the cost of a misunderstanding grows with every stage
2. Vision / PRD: problem, audience, goals, non-goals, success metrics
3. User story (`As a… I want… so that…`) + acceptance criteria in Given/When/Then; INVEST
4. Use case: actors, preconditions, main flow, alternative and error flows
5. Test case: steps, data, expected result; how acceptance criteria turn into tests
6. BPMN: events, tasks, gateways, pools and lanes; modeling the booking process
7. UML: use case, sequence, class, state, activity; ER diagram for the data model
8. C4 model: context → container → component → code; the most useful diagram for architecture
9. ADR (Architecture Decision Record) and API contract (OpenAPI)
10. Docs-as-code: Mermaid, PlantUML, BPMN XML, all versioned in `docs/`
11. How AI agents read docs: text beats pictures, diagrams as code, `AGENTS.md`/`CLAUDE.md`, linking specs to tests, keeping docs from going stale

## Lab
Write the "Slot" spec: vision, 8–10 user stories with acceptance criteria, 2 use cases, the booking BPMN, a C4 container diagram, an ER diagram, an OpenAPI draft, 10 test cases.
- **With an agent:** give the agent only `docs/` and ask it to list contradictions and gaps; then ask it to generate test stubs from the acceptance criteria.

## Deliverable
`docs/` folder with all artifacts + the list of gaps the agent found and how you fixed them.
