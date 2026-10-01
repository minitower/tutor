# Module 2 — Lecture Script: MCP: Connecting Agents to External Systems

*Speaking notes for the instructor. Slide numbers match `slides.md` exactly.
Timing notes are suggestions for a live 2–2.5 hour session (lecture + lab).*

---

## Opening (Slides 1–3) — ~10 min

### Slide 1 — Model Context Protocol: the agent's hands

Welcome to Module 2. In Module 1 we saw the agent loop: plan, act, observe. For now the agent works inside the repository: reading files, running commands, editing code. Real tasks run into systems beyond it: a database, a tracker, monitoring, a browser. Today: how to give the agent access to them through a standard rather than one-off hacks — and how not to turn that access into a hole.

### Slide 2 — Agenda

In order: the problem and the protocol, then practice — a DB, open servers, your own server. Then an honest talk about when you don't need MCP, and a big security block, because every server is code that executes at a model's request. The lab is a read-only database through MCP. Note: the module points ahead to verification, CI/CD and hooks — those are pointers to topics we cover in full later.

### Slide 3 — Objectives

Four objectives. Note the last one: not "connect everything available" but being able to vet a server and pick the right tool — sometimes that's a plain CLI or a skill. A good engineer knows when MCP isn't needed.

---

## The Problem and the Protocol (Slides 4–8) — ~25 min

### Slide 4 — The Problem: N × M Integrations

Look at the diagram. On the left is the world without a standard: three apps and three systems give nine integrations, each with its own auth, formats and bugs. On the right, with MCP: each app implements a client once, each system a server once, and they are compatible. N times M becomes N plus M. The analogy is the Language Server Protocol: editors used to support each language separately; now a language server is written once.

### Slide 5 — What Is MCP

MCP is an open protocol; messages are encoded in JSON-RPC 2.0. Three roles. The host is the application with the model: Claude Code, an IDE, your own agent. The client is a connector inside the host, one per server. The server is a program that provides context and capabilities. The key idea of the slide: this is an access layer separate from both the model and the agent. That's why permissions, audit and limits can hang on the server — more on that later.

### Slide 6 — Architecture and Transports

Two standard transports. Stdio — the server runs as a child process, messages go line by line over the standard streams: ideal for local tools. Streamable HTTP — each message is an HTTP POST to one endpoint, the reply comes as JSON or an SSE stream: this is how remote servers with OAuth work. The former SSE transport is deprecated. For the instructor: the recent spec revision made requests self-contained, with no initialize session — but clients keep compatibility with earlier versions, so students only need to know "the protocol evolves, check the spec".

### Slide 7 — What a Server Offers: Three Primitives

Three primitives, and who controls them matters. Tools are functions the model calls; for agents this is the main one. Resources are data and context read by the user or the model. Prompts are templates the user triggers; in Claude Code they are slash commands. On the client side there is elicitation: a server can ask the user to clarify. Among extensions are Tasks for long operations and Skills over MCP: delivering skills through MCP — we'll meet that in Module 4.

### Slide 8 — What a Tool Call Looks Like

Here's what a call looks like on the wire. The client asks tools/list and gets a list: name, description, JSON schema of the arguments. Then tools/call with arguments and a result. The takeaway: the model decides whether to call a tool from its name, description and schema. So the description is part of your prompt, written by someone you trust… or don't — we return to that in security. The example is simplified: metadata fields and the handshake are omitted.

---

## Practice: Connecting and Examples (Slides 9–12) — ~30 min

### Slide 9 — Connecting in Claude Code

Practice in Claude Code. A local server: claude mcp add with the stdio transport, then a double dash and the launch command — the dashes are required, otherwise Claude parses the server's flags itself. A remote one: the http transport and a URL; for OAuth you then open /mcp and sign in in the browser. claude mcp list shows the status. Three scopes: local — personal to the project, project — the .mcp.json file in git for the team, user — for all your projects. Remember the tool name mcp double-underscore server double-underscore tool — you need it for permissions and hooks.

### Slide 10 — Example 1: A Database Through MCP

The classic first MCP case is a database. The agent reads the schema, writes queries itself, analyzes the result — a junior analyst. But rule number one: a read-only role. Don't rely on the agent "not writing" — make it unable to. Preferably a replica or staging. The DSN goes in an environment variable, and .mcp.json lands in git. Add limits on the DB side. And a note: the reference PostgreSQL and SQLite servers are now archived, so use maintained ones — DBHub or vendor servers.

### Slide 11 — Example 2: Open MCP Servers

Open servers. The reference ones from the modelcontextprotocol repo: Filesystem, Git, Fetch, Memory — a knowledge graph as memory, we return to it in Module 3 — plus Sequential Thinking and Time. Then vendor remote servers: GitHub, Sentry, Notion, Stripe, with OAuth. And Playwright — browser control, handy so the agent checks the UI itself. Read the footnote aloud: Fetch turns a web page into markdown — a ready channel for prompt injection. And show the MCP Registry as the place to look for servers. Versions and commands change fast, always check the README.

### Slide 12 — Your Own MCP Server in 10 Lines

Your own server is ten lines. A function with a tool decorator, a docstring and types. Note: in the current Python SDK FastMCP was renamed MCPServer — in the first major version the import differs, that's in the slide comment. It runs over stdio by default. Debug in the MCP Inspector, without an agent: you see the tool list and the call result. Design advice: a few narrow tools beat many broad ones; the docstring is what the model reads; the reply must be short or it will eat the context.

---

## When MCP and When Not (Slide 13) — ~10 min

### Slide 13 — MCP, CLI or Skill: What to Choose

Not everything needs an MCP wrapper. If the tool is already in the terminal and the agent knows it — git, gh, psql — use the CLI: zero context cost for descriptions. MCP wins when you need standard OAuth, typed replies, or one server for several clients. A repeatable procedure is a skill, an "always" rule is a hook. Mind the cost too: tool descriptions occupy context; Claude Code loads them on demand by default, but still switch off unneeded servers.

---

## Security and Agent Systems (Slides 14–16) — ~25 min

### Slide 14 — MCP Security: Threats

Security. First — injection through tool results: a page, a ticket, a row in a database may contain an instruction for the agent; this is Module 12 in new wrapping. Second — tool poisoning: a malicious tool description. The spec says outright that descriptions are untrusted unless the server is trusted. Third — rug pull and supply chain: a server changed its tools after approval, or npx with -y pulls an unpinned version. Fourth — excess privilege. Fifth — leaks. And a line from the spec's principles: a tool is arbitrary code execution, user consent is mandatory.

### Slide 15 — MCP Security: Controls

Controls. Least privilege: read-only creds, minimal scopes, an allow-list of tools in permissions — the slide shows allow for query and deny for execute. Pin versions and read the server's code before connecting — yes, it's boring, but it's exactly what you do with dependencies. An audit hook: PreToolUse with matcher mcp dot star logs every call — hello Module 13. Servers from .mcp.json require approval on first use — don't click yes blindly. For servers with internet access — a sandbox and egress limits.

### Slide 16 — MCP in an Agent System and in CI

How this looks in automation. Key fact: a stdio server in .mcp.json is a command that runs on the machine. A config from a foreign PR is untrusted code, just as in Module 13 on forks. In CI list allowed tools explicitly; creds are CI secrets with read-only rights. And for agent systems with several roles a useful thought: each role gets its own set of servers. The planner reads, the implementer writes to its branch, the reviewer only comments. Policy lives in the server, not in the prompt.

---

## Lab and Recap (Slides 17–19) — ~10 min

### Slide 17 — Lab — A Database Through MCP

The lab. Start a test DB with a read-only user, connect it via .mcp.json, ask three questions, save the trace. Then ask for an UPDATE or DROP and show the write is blocked — by both DB permissions and deny. That's the key moment: protection works not because the agent is obedient. Then a mini server with one tool, a check in the Inspector, and a threat note — five rows from slide 14 with a countermeasure each.

### Slide 18 — Deliverable

What to hand in: a secret-free .mcp.json, the trace and proof the write is blocked, the mini-server code with an Inspector log, and the threat note. Check the note first: the student must tie each countermeasure to a concrete threat, not just list best practices.

### Slide 19 — Next: Long-Term Agent Memory

Recap. MCP gives an agent hands — access to systems through one protocol. But a server is code and its output is untrusted text, so permissions, audit and boundaries remain your job. Next — memory: an agent needs to remember you and the project between sessions. See you in Module 3.
