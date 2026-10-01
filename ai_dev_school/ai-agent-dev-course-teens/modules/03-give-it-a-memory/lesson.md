# Module 3 — Give Your Agent a Memory

## Big idea

When you close a session the agent forgets everything — the context window is not memory. For an agent to remember you and your project it needs **long-term memory**: files (`CLAUDE.md`, notes), databases or whole memory systems. There are three kinds: what happened (episodes), what's known (facts about you and the project) and how to do things (procedures). Memory is **data about people**: it can be poisoned by someone's "instruction", it accumulates stale facts, and secrets in it stay put. So the key skill is deciding *what* to remember and how to verify it.

## Why it matters

Without memory every day starts from zero: the agent asks again about code style, names, "how we do things". With memory it works like a partner who remembers yesterday. But bad memory is worse than none: it stores mistakes and leaks.

## Hands-on task

**Part A — project notes:**
1. Create a `CLAUDE.md` for your project: code style, naming, what's already decided and *why*.
2. Run two sessions in a row and check that in the second the agent uses the notes.

**Part B — a helper's "soul":**
1. If your project has a helper bot, write it a role file (in the spirit of `SOUL.md`): role, tone, values, "never" boundaries. If there's no bot, write the same rules for the agent working on the project.

**Part C — a small Python memory:**
1. Implement `remember` / `recall` / `forget` on SQLite (slide 9).
2. Write a test: it recalls, it doesn't leak others' data, it deletes.

**Part D — a write policy:** make a "we remember" and a "never" list (at least 4 items each).

## Checkpoint

- Your memory files and proof the agent used them in the second session
- The memory code and a green test
- The write policy: what we remember, what never — and *why* for each item

## Supervisor note

**Privacy.** Memory files are data. Review them before committing or publishing: no real names, addresses, school, phone numbers, passwords or other people's personal data (especially other minors, if the bot has users). Agree that the teen can view, edit and delete any entry.
