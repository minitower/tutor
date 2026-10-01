---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# MCP

## Model Context Protocol: the agent's hands

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- What problem MCP solves and how it is built
- Protocol primitives, transports, the call format
- Practice: a database, open servers, your own server
- MCP vs. CLI vs. Skill — how to choose
- MCP history, connecting in KiloCode, MCP over FastAPI
- RAG and MCP: classic vs. agentic RAG
- MCP security and running inside an agent system
- Lab: a read-only DB through MCP + a mini server

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Explain what problem MCP solves and describe host / client / server
2. Name the three primitives and two transports, read `.mcp.json`
3. Safely connect a ready-made server (a DB) and write a simple one of your own
4. Vet a server with a security checklist and choose between MCP, CLI and Skill

---

<!-- Slide 4 -->

## The Problem: N × M Integrations

- Every agent needs a DB, a tracker, monitoring, a browser…
- Without a standard every agent × system pair is a separate integration

---

<!-- Slide 5 -->

## What Is MCP

- **Model Context Protocol** is an open protocol that standardizes how an LLM application gets context and tools from external systems
- Messages are **JSON-RPC 2.0**
- The idea is borrowed from the Language Server Protocol: one standard instead of wiring every editor to every language
- Three roles: **host** (the LLM app), **client** (a connector inside the host), **server** (provides context and capabilities)

> A layer of access to systems — separate from the model and the agent.

---

<!-- Slide 6 -->

## Where MCP Came From

- **Before 2024:** every chat app and IDE wired itself to every data source by hand — the N × M problem
- The model: the **Language Server Protocol** (Microsoft, 2016) — one standard between editors and languages
- **5 Nov 2024:** first spec revision (`2024-11-05`); **25 Nov 2024:** Anthropic announces MCP as open source
- Day one: Python and TypeScript SDKs plus reference servers (Google Drive, Slack, GitHub, Git, Postgres, Puppeteer)

---

<!-- Slide 7 -->

## From Experiment to Standard

| When | What happened |
|---|---|
| Mar 2025 | OpenAI adds MCP to its Agents SDK; spec `2025-03-26`: Streamable HTTP and OAuth |
| Apr–May 2025 | Google DeepMind and Microsoft announce support |
| Jun 2025 | spec `2025-06-18`: structured tool output, elicitation |
| Sep 2025 | MCP Registry (preview) |
| Nov 2025 | spec `2025-11-25`: tasks, further auth work |
| Dec 2025 | MCP moves to the **Agentic AI Foundation** (Linux Foundation) next to AGENTS.md and goose |

Takeaway: a vendor protocol became a neutral standard in a year — but the spec still changes fast, so pin versions and check the changelog.

---

<!-- Slide 8 -->

## Architecture and Transports

**Host** → **Client** → **Server**

| Transport | How it works | When |
|---|---|---|
| **stdio** | server is a child process, newline-delimited JSON over stdin/stdout | local tools |
| **Streamable HTTP** | each message is an HTTP POST; reply is JSON or an SSE stream | remote and cloud servers, OAuth |

The old SSE transport is deprecated. The recent spec revision made requests self-contained (no `initialize` session); clients and servers keep a fallback to older versions.

---

<!-- Slide 9 -->

## What a Server Offers: Three Primitives

- **Tools** — Functions the **model** calls: query a DB, create an issue, search. The main primitive for agents
- **Resources** — Data and context — files, schemas, records — read by the user or the model
- **Prompts** — Templated messages and workflows the **user** triggers (slash commands in Claude Code)

On the client side: **elicitation** — the server asks the user for missing information. Optional extensions: Tasks (long operations), MCP Apps (interactive UI), Skills over MCP.

---

<!-- Slide 10 -->

## What a Tool Call Looks Like

```json
→ {"jsonrpc":"2.0","id":7,"method":"tools/list"}
← {"result":{"tools":[{"name":"query","description":"Run a read-only SQL query",
     "inputSchema":{"type":"object","properties":{"sql":{"type":"string"}},"required":["sql"]}}]}}

→ {"jsonrpc":"2.0","id":8,"method":"tools/call",
   "params":{"name":"query","arguments":{"sql":"SELECT count(*) FROM users"}}}
← {"result":{"content":[{"type":"text","text":"count\n42"}]}}
```

- The model sees the **name, description and JSON schema** of the arguments — that is how it decides to call the tool
- The example is simplified: `_meta` fields and the handshake are omitted

---

<!-- Slide 11 -->

## Connecting in Claude Code

```bash
# локальный stdio-сервер (после -- идёт команда запуска)
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "$DB_READONLY_DSN"
# удалённый HTTP-сервер; OAuth: затем /mcp -> войти в браузере
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp list           # Connected / Needs authentication / Failed
claude mcp get sentry ; claude mcp remove sentry
```

| Scope | Where stored | Used for |
|---|---|---|
| local | `~/.claude.json` | personal servers and creds for this project |
| project | `.mcp.json` в корне | shared team servers — via git |
| user | `~/.claude.json` | your utilities across all projects |

Tools are named `mcp__<server>__<tool>` — use these names in permission rules, hooks and `allowed-tools`.

---

<!-- Slide 12 -->

## Connecting in KiloCode

Kilo Code is an open-source coding agent for VS Code / JetBrains. MCP servers live in two JSON files:

- **Global** — `mcp_settings.json` (MCP Servers → *Edit Global MCP*)
- **Project** — `.kilocode/mcp.json` in the repo root, shared via git (no secrets!); the project entry wins on a name clash

```json
{ "mcpServers": {
    "docs": { "command": "npx",
              "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"],
              "alwaysAllow": [], "disabled": false },
    "sentry": { "type": "streamable-http", "url": "https://mcp.sentry.dev/mcp" } } }
```

- `alwaysAllow` = tools that run without asking; keep it empty or read-only
- Same `mcpServers` shape in Claude Desktop and Cursor; VS Code Copilot uses `.vscode/mcp.json` with `servers`
- The Marketplace installs popular servers in one click — the security checklist still applies

---

<!-- Slide 13 -->

## Example 1: A Database Through MCP

```json
{ "mcpServers": { "db": {
    "type": "stdio", "command": "npx",
    "args": ["-y", "@bytebase/dbhub", "--dsn", "${DB_READONLY_DSN}"] } } }
```

- The agent reads the schema, writes and runs queries itself, analyzes the result
- **Rule #1: a read-only DB role**, ideally a replica or staging — not prod with write access
- The DSN goes in an environment variable (`${VAR}` is supported), not in git
- Limits on the DB side: `statement_timeout`, row caps
- The reference PostgreSQL and SQLite servers are archived — use maintained ones (DBHub, vendor servers such as Supabase or Neon)

---

<!-- Slide 14 -->

## Example 2: Open MCP Servers

| Server | What it gives | Connection |
|---|---|---|
| **Filesystem** (reference) | file operations within allowed directories | `npx -y @modelcontextprotocol/server-filesystem <dir>` |
| **Git** (reference) | read, search and operate on a repository | `uvx mcp-server-git` |
| **Fetch** (reference) | web page → markdown (watch out: injection!) | `uvx mcp-server-fetch` |
| **Memory** (reference) | a knowledge graph as persistent memory — Module 3 | `npx -y @modelcontextprotocol/server-memory` |
| **GitHub** | issues, PRs, repositories | remote: `https://api.githubcopilot.com/mcp/` + token |
| **Sentry**, **Notion**, **Stripe** | vendor remote servers with OAuth | `https://mcp.sentry.dev/mcp` etc. |
| **Playwright** (Microsoft) | browser control for UI checks | `npx @playwright/mcp@latest` (check the README) |

A catalog of published servers is the MCP Registry (`registry.modelcontextprotocol.io`). The GitHub, GitLab, Slack and Puppeteer servers from the reference repo are archived.

---

<!-- Slide 15 -->

## Your Own MCP Server in 10 Lines

```python
# server.py     pip install mcp
from mcp.server.mcpserver import MCPServer   # в mcp 1.x: from mcp.server.fastmcp import FastMCP

mcp = MCPServer("tickets")

@mcp.tool()
def count_open(project: str) -> int:
    """Сколько открытых тикетов в проекте (только чтение)."""
    return db_count(project)        # ваша реализация

if __name__ == "__main__":
    mcp.run()                       # stdio по умолчанию
```

- Connect: `claude mcp add --transport stdio tickets -- python server.py`
- Debug without an agent: `npx @modelcontextprotocol/inspector python server.py`
- The docstring and types are what the model sees. A few narrow tools beat many broad ones; keep replies short

---

<!-- Slide 16 -->

## MCP over FastAPI

Already have a FastAPI service? Expose it as MCP instead of writing a second server:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP        # pip install fastapi-mcp

app = FastAPI()

@app.get("/tickets/{project}/open", operation_id="count_open")
def count_open(project: str) -> int:
    """How many open tickets a project has (read-only)."""
    return db_count(project)

mcp = FastApiMCP(app, include_operations=["count_open"])   # whitelist
mcp.mount_http()                          # MCP at /mcp (older versions: mount())
```

- Connect: `claude mcp add --transport http tickets http://localhost:8000/mcp`
- `operation_id` → tool name, docstring → description, Pydantic models → input schema
- Auth reuses FastAPI `Depends`; **don't expose every endpoint** — whitelist read-only operations
- Alternative: `FastMCP.from_fastapi(app)` (FastMCP library). Good fit when the API already exists; a hand-written server is better when tools should be narrower than endpoints

---

<!-- Slide 17 -->

## MCP, CLI or Skill: What to Choose

| Situation | Choice | Why |
|---|---|---|
| The tool is already in the terminal and the agent knows it (`git`, `gh`, `psql`) | CLI | no context cost for descriptions, fewer moving parts |
| An external service with OAuth, typed replies, several clients | **MCP** | standard auth and schema, one server for all |
| A repeatable procedure, a checklist, "how we do it here" | Skill | Module 4 |
| A rule that must always hold | Hook | Module 13 |

MCP tool descriptions occupy context. Claude Code loads tools on demand by default (tool search) — but still switch off servers you don't need.

---

<!-- Slide 18 -->

## RAG and MCP: Different Layers

- **RAG** is a technique: find relevant chunks → put them into the prompt → answer. It decides *what the model sees*
- **MCP** is a protocol: it decides *how the model reaches a system* — including a retriever
- They are not alternatives: wrap your vector search as a tool `search_docs(query)` in an MCP server and any agent can use it

| | Classic RAG | Agentic RAG via MCP |
|---|---|---|
| Who triggers retrieval | your code, always | the agent, when it decides |
| Sources | one index | docs + DB + tracker + web |
| Queries | one | several, reformulated |

---

<!-- Slide 19 -->

## Classic RAG or Agentic RAG

| Choose | When | Example |
|---|---|---|
| **Classic RAG** | one knowledge base, one-shot question, tight latency and cost, predictable behavior | FAQ bot, support over docs, internal wiki search |
| **Agentic RAG (MCP)** | several sources, multi-step questions, live or per-user data, the agent must verify itself | coding agent: code + tickets + DB; analyst assistant |
| **Hybrid** | pipeline covers the common path; MCP search tool as a fallback | support bot that escalates to the ticket system |

- Agentic costs more: tokens, latency, non-determinism — measure before switching
- Retrieved text is **untrusted** (Module 12); access control must be checked per user inside the server

---

<!-- Slide 20 -->

## MCP Security: Threats

- **Prompt injection through tool results** — a page, a ticket, a DB row carries an "instruction" (Module 12)
- **Tool poisoning** — a malicious tool description; per the spec descriptions are untrusted unless the server is trusted
- **Rug pull and supply chain** — a server changed its tools after approval; `npx -y` without a pinned version
- **Excess privilege** — a write/admin token where read is enough
- **Leaks** — secrets in args and logs; a remote server sees everything you send it

> An MCP tool is arbitrary code execution. User consent is mandatory.

---

<!-- Slide 21 -->

## MCP Security: Controls

```json
{ "permissions": {
    "allow": ["mcp__db__query"],
    "deny":  ["mcp__db__execute"] } }
```

- **Least privilege**: read-only creds, minimal OAuth scopes, an allow-list of tools
- **Pin versions** (`@bytebase/dbhub@X.Y.Z`) and read the server's code before connecting
- **Audit hook**: `PreToolUse` with matcher `mcp__.*` logs every call
- Project servers from `.mcp.json` require approval — don't click yes blindly
- Sandbox and egress limits for servers with internet access

---

<!-- Slide 22 -->

## MCP in an Agent System and in CI

- A `stdio` server in `.mcp.json` is a **command that runs on your machine**. A config from a foreign PR is untrusted code (Module 13, forks)
- In CI list allowed tools explicitly: `--allowedTools "mcp__db__query"`; creds are CI secrets, read-only
- In a multi-agent system each role gets **its own set of servers**: the planner reads, the implementer writes to its branch, the reviewer only comments
- MCP is a convenient policy boundary: permissions, audit and limits live in the server, not in the prompt

---

<!-- Slide 23 -->

## Lab — A Database Through MCP

1. Start a test DB (SQLite or Postgres in Docker) with a read-only user and connect it through MCP in `.mcp.json`
2. Ask the agent three analytical questions; save the tool-call trace
3. Ask it to run `UPDATE`/`DROP` and show the write is blocked (by DB permissions and `deny`)
4. Write your own mini server with one tool and check it in the Inspector
5. Fill in a threat note: five rows from slide 14 and a countermeasure for each

---

<!-- Slide 24 -->

## Deliverable

- `.mcp.json` (no secrets), working read-only DB access
- The call trace and proof that writes are blocked
- The mini-server code + an Inspector screenshot/log
- The threat note with countermeasures

---

<!-- Slide 25 -->

## Next: Long-Term Agent Memory

MCP gives an agent hands: access to systems through one protocol. But permissions, audit and boundaries are still your job: a server is code, and its output is untrusted text.

An agent also needs memory of you and the project.
