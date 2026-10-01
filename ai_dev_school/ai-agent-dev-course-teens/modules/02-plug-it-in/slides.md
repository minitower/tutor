---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Plug It In: MCP

Module 2 — Build With AI

---

<!-- Slide 2 -->

## Today

- Why the agent lives in a bubble
- MCP: one plug for any tool
- How it works and how to connect one
- Building your own mini server
- Plugging in = trusting: a safety checklist
- Hands-on and checkpoint

---

<!-- Slide 3 -->

## The Agent Lives in a Bubble

- It sees the project folder — and nothing else
- The score table, the bot's data, the club calendar — don't exist for it
- You can paste data into chat by hand... every time
- Better: give it a **safe entrance** to what it needs

---

<!-- Slide 4 -->

## MCP Is USB for AI

- **Model Context Protocol** is an open standard for how an agent connects to outside tools and data
- Before: every "app × service" pair was its own integration
- Now: write a server once — any agent can connect
- Messages are JSON-RPC (plain JSON)

---

<!-- Slide 5 -->

## Three Roles

- **Host** — the program with the AI (Claude Code, an editor)
- **Client** — a "port" inside the host, one per server
- **Server** — your small program with tools
- Connection: local (**stdio**, the server is a child process) or over the network (**HTTP**)

---

<!-- Slide 6 -->

## What a Server Can Offer

- **Tools** — functions the agent calls (`top_scores`, `add_note`)
- **Resources** — data that can be read (a file, a schema)
- **Prompts** — ready-made requests that *you* trigger
- A tool has a **name, a description and argument types** — the agent decides from them when to call it

---

<!-- Slide 7 -->

## Connecting a Server

```bash
claude mcp add --transport stdio scores -- python scores_server.py
claude mcp list        # Connected / Failed
claude mcp remove scores
```

The shared project file is `.mcp.json` (no secrets!). The tool is named `mcp__scores__top_scores` — that's the name you use in permission rules.

---

<!-- Slide 8 -->

## Your Own Server in 10 Lines

```python
# scores_server.py   (pip install mcp)
import json
from mcp.server.mcpserver import MCPServer   # older mcp 1.x: from mcp.server.fastmcp import FastMCP

mcp = MCPServer("scores")
SCORES = json.load(open("scores.json"))       # {"ana": 120, "bo": 95, "cy": 150}

@mcp.tool()
def top_scores(n: int = 3) -> list[str]:
    """Return the top n players and their scores (read-only)."""
    best = sorted(SCORES.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [f"{name}: {score}" for name, score in best]

if __name__ == "__main__":
    mcp.run()
```

The description and types are what the agent sees. One narrow tool beats ten broad ones.

---

<!-- Slide 9 -->

## Plugging In = Trusting

- A server is a **program on your computer**: it can do whatever you can
- The model reads a tool's description — a malicious one can nudge it
- A tool's result is untrusted text: it may hide an "instruction" (Module 12)
- Someone else's `npx -y ...` command from the internet is running someone else's code

---

<!-- Slide 10 -->

## The "Can I Plug It In?" Checklist

- ☐ I know who wrote the server and I read its code (or it's an official example)
- ☐ Access is **read-only**, the data is test data
- ☐ No passwords or tokens from personal accounts
- ☐ The version is pinned, not "latest"
- ☐ I know its tool names and blocked the extra ones

---

<!-- Slide 11 -->

## Hands-On

**A.** Write a mini server with one read-only tool and check it in the Inspector

**B.** Connect it and ask the agent three questions; record the calls

**C.** Ask it to *change* the data — what happened and why?

Write your own 5-item checklist.

---

<!-- Slide 12 -->

## Checkpoint

- The server code and the call trace
- Your 5-item checklist
- One sentence: why a tool's result isn't "an order from me"

---

<!-- Slide 13 -->

## Recap

- MCP is one plug between the agent and the outside world
- A server offers tools / resources / prompts
- Plugging in is trust: read-only, vetted code, nothing personal
- Tool results are untrusted text

---

<!-- Slide 14 -->

## Next Up

**Module 3 — Give Your Agent a Memory**

How an agent remembers you and your project between sessions — and what it shouldn't remember.
