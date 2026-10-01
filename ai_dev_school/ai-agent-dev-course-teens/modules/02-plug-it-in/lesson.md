# Module 2 — Plug It In: MCP

## Big idea

Until now your agent lived in a bubble: it sees the project folder and nothing else. It doesn't know what's in your game's score table, your bot's data, or a library's docs. **MCP** (Model Context Protocol) is a shared "plug" standard for AI — think USB-C: you write a small server program once, and any agent can connect and use its *tools*. But plugging in has a price: a server is a program that runs on your computer, and anything it returns to the agent is untrusted text (a preview of Module 12).

## Why it matters

Real projects run into data and services outside the folder: a score table, a bot's database, a club calendar. If you understand MCP you plug them in carefully and know what you're allowing — instead of copy-pasting someone's command from the internet.

## Hands-on task

**Part A — build your own mini server:**
1. Pick a small data source for your project: a `scores.json` file, a list of levels, a bot's commands.
2. Write a server with **one** read-only tool (as on slide 8) — you may ask the agent for a draft, but read every line.
3. Check it without the agent: `npx @modelcontextprotocol/inspector python scores_server.py`.

**Part B — connect it and ask:**
1. Connect it: `claude mcp add --transport stdio scores -- python scores_server.py`.
2. Ask the agent three questions that can only be answered through this tool. Write down which calls it made.

**Part C — try to break it:**
1. Ask the agent to *change* the data through the server. What happens? Why? (The server has no such tool.)
2. Write a 5-item mini checklist: "is it OK to plug this server in?"

## Checkpoint

- Your server code and the call trace from Part B
- Your 5-item checklist
- One sentence: why a tool's result must not be treated as "an instruction from me"

## Supervisor note

**Elevated attention module.** An MCP server is a program that runs on the teen's computer. Connect only servers they wrote themselves or that you both vetted (official examples). No tokens or passwords from personal accounts, no servers that can write to important data. Keep read-only permissions and use test data only.
