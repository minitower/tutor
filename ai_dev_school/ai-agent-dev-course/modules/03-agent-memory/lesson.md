# Module 3 — Long-Term Agent Memory

## Learning objectives
- Design an agent system's long-term memory of the user and the project — and verify it with tests

## Key concepts
- Context vs. memory; working, episodic, semantic, procedural memory
- File memory: `SOUL.md`, `USER.md`, `MEMORY.md`, daily notes; `SOUL.md` is a convention, not a standard
- Layered memory via TencentDB Agent Memory: L0–L3 layers, Skill/Wiki/CodeGraph, MemoryProxy, ACL, BM25 + vector + RRF retrieval
- DIY memory on SQLite FTS5; a write policy: what to remember and what not
- Risks: memory poisoning, privacy, staleness; recall / isolation / deletion tests

## Lab
Build an assistant's memory (`SOUL.md`, `USER.md`, `MEMORY.md`), run three sessions, implement SQLite memory and write tests.

## Deliverable
The memory files, a session log, code and tests, and a memory-policy note.
