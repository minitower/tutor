# Module 4 — Skills: Agent Capabilities

## Learning objectives
- Write, test and safely use skills — an agent's reusable procedures

## Key concepts
- A skill = a folder with `SKILL.md` (frontmatter + instructions) and supporting files; three-level progressive disclosure
- Who invokes: `/name` or the model via `description`; `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context: fork`, `paths`, `hooks`
- Arguments, dynamic context, scripts; locations (personal / project / plugin / enterprise)
- Skill vs. CLAUDE.md vs. hook vs. MCP vs. subagent; the open Agent Skills standard
- Security (`allowed-tools`, third-party skills, `Skill(...)` rules) and testing (triggering, with/without baseline)

## Lab
Package a repeated procedure as a skill, write a should / shouldn't-trigger prompt set, compare with a no-skill baseline and write a security note.

## Deliverable
The skill folder, a 10-prompt set with a results table and a security note.
