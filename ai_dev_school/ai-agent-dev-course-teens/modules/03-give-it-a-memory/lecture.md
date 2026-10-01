# Lecture Script — Module 3: Give Your Agent a Memory

Facilitator notes: this is a spoken script, not something to read word for word. Say it like you'd explain it to a smart teen who can already code and wants to know what actually matters here. The lecture portion should run **~20-25 minutes**; the rest of the module is the hands-on task and checkpoint. Slide numbers below match `slides.md` exactly. Keep the tone practical, not preachy: "here's why this protects you".

---

## Opening (~2 min)

## Slide 1 — Give Your Agent a Memory

"We've taught the agent to read, write code and reach outside through MCP. But every morning it again knows nothing about you. Today is about memory."

---

## Slide 2 — Today

"The plan: context versus memory, memory in files, what to remember, how memory breaks, your own memory in Python and a test. Note: the test isn't a bonus, it's part of the topic."

---

## The Idea (~6 min)

## Slide 3 — The Goldfish Problem

"Close the session — the agent forgets everything, like a goldfish. The context window is RAM, not long-term storage. If you re-explain code style and names every day, you waste time. You need long-term memory — what survives the session."

---

## Slide 4 — Kinds of Memory

"Kinds of memory. Episodes — what happened. Facts — what's known about you and the project. Procedures — how to do things; Module 4 is about them. And working memory — what's in the window now. When people say 'the agent has no memory' they usually mean facts and episodes."

---

## Memory in Files (~7 min)

## Slide 5 — Memory in Files

"The simplest way is files the agent reads at start: CLAUDE.md, MEMORY.md, notes. You see them, edit them, delete them and keep them in git. The downside — files load whole and don't scale. A good entry is a fact, why it matters and how to apply it. And mark contradictions with a date."

---

## Slide 6 — A Helper's "Soul": SOUL.md

"A role file, a helper's 'soul'. It holds role, tone, values and 'never' boundaries. Honestly: SOUL.md isn't a standard, it's one project's convention, OpenClaw; other systems, like TencentDB Agent Memory, have no such file — there a user profile is stored as a layer. What matters is the function: a stable role and boundaries. Facts about the user go separately, procedures in skills."

---

## What to Remember and How It Breaks (~6 min)

## Slide 7 — What to Remember — and What Never

"What to remember: code style, project decisions and why, your corrections, links. What never: passwords and tokens, real names, address, school, phone, other people's personal data, unverified guesses. And the trust rule: memory isn't the source of truth. Does it say there's a function parse_level? Check it still exists."

---

## Slide 8 — How Memory Breaks

"How memory breaks. Poisoning: text from a web page got into memory with a hidden instruction — and now it works in every session. Prompt injection (Module 12), only permanent. Staleness. A leak — a secret in a file you pushed to GitHub. Bloat. Defense: a source and date, don't write to memory from untrusted text unchecked, and be able to delete."

---

## Code and Tests (~5 min)

## Slide 9 — Your Own Memory in Python

"Your own memory is fifteen lines. A SQLite table with full-text search, remember, recall filtered by user, and forget. Isolation and deletion here aren't 'later', they're in the first version. And a link to the last module: wrap remember and recall in MCP tools and any agent gets memory."

---

## Slide 10 — A Test for Memory

"The test. Store an entry; it's recalled; others' entries aren't visible; after deletion it's not found. Four lines that catch the nastiest bugs. Add a fourth property: new supersedes old."

---

## Slide 11 — Bigger Systems

"If you want more, there are ready-made systems. For example TencentDB Agent Memory: chats stored in layers from raw to profile, search by words and by meaning, entries with access rights, and the agent connects just by changing the API address. But it's one more service with your data — the same privacy questions. First read where your data goes."

---

## Hands-on and Recap (~3 min, then practice)

## Slide 12 — Hands-On

"Hands-on: CLAUDE.md and two sessions in a row; a role file; SQLite memory with a test; a write policy. Every item in the policy needs a 'why'."

---

## Slide 13 — Checkpoint

"Checkpoint: memory files and proof the agent used them in the second session, the code with a green test, the write policy with reasons."

---

## Slide 14 — Recap

"Recap: context isn't memory, it has to be designed. Files are transparent, systems scale but need trust. Memory is data about people. And it has to be tested."

---

## Slide 15 — Next Up

"Next — skills: how to package a procedure you repeat so the agent does it the same way every time."
