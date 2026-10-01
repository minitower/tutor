# Lecture Script — Module 2: Plug It In: MCP

Facilitator notes: this is a spoken script, not something to read word for word. Say it like you'd explain it to a smart teen who can already code and wants to know what actually matters here. The lecture portion should run **~20-25 minutes**; the rest of the module is the hands-on task and checkpoint. Slide numbers below match `slides.md` exactly. Keep the tone practical, not preachy: "here's why this protects you".

---

## Opening (~2 min)

## Slide 1 — Plug It In: MCP

"So far everything the agent did happened inside the project folder. Today: how to let it reach outside without opening a hole — and so that you understand exactly what you're allowing."

---

## Slide 2 — Today

"The plan: why the agent is in a bubble, what MCP is, how to connect one and write your own, and above all a safety checklist. At the end you'll write your own mini server and try to break it."

---

## The Idea (~8 min)

## Slide 3 — The Agent Lives in a Bubble

"Imagine a bot for your club. The agent writes code fine, but doesn't know who signed up today. You can paste the data into chat every time — that works. But it's better to give it a safe entrance to that data. The word 'safe' is the key of the whole lesson."

---

## Slide 4 — MCP Is USB for AI

"MCP is like USB-C for AI. Before, every 'app plus service' pair needed its own integration. Now a service writes a server once and any agent connects. Inside it's ordinary JSON messages, nothing mystical."

---

## Slide 5 — Three Roles

"Three roles. The host is the program with the AI, like Claude Code. The client is a port inside it, one per server. The server is a small program with tools. The connection may be local — the server runs as a child process — or over the network via HTTP. Remember: a local server is code that runs on your machine."

---

## Slide 6 — What a Server Can Offer

"A server can offer three kinds of things. Tools — functions the agent calls. Resources — data that can be read. Prompts — templates that you trigger. A tool has a name, a description and argument types, and the agent decides from them when to call it. So the description is part of the prompt."

---

## How It's Done (~8 min)

## Slide 7 — Connecting a Server

"How to connect: claude mcp add, the stdio transport, two dashes and the launch command. claude mcp list shows the status. The project-shared file is .mcp.json, but it must hold no secrets. The tool name comes out as mcp, server, tool — that's how permission rules are written."

---

## Slide 8 — Your Own Server in 10 Lines

"Your own server is ten lines. We read scores.json, one tool top_scores, a docstring. Note the comment: in the new SDK version the class was renamed, in the old one the import differs. The tool only reads — that's deliberate. And one narrow tool beats ten broad ones."

---

## Safety (~5 min)

## Slide 9 — Plugging In = Trusting

"Now the price. A server is a program on your computer and it can do whatever you can. The model reads a tool's description. And the result is text the agent reads as data, but an instruction may hide in it: we'll dig into this in Module 12: And an npx -y command from a random article is running someone else's code. Plugging in means trusting."

---

## Slide 10 — The "Can I Plug It In?" Checklist

"Here's the checklist. I know the author and read the code; read-only and test data; no tokens from personal accounts; version pinned; extra tools blocked. No item takes more than a minute, but each closes a real hole."

---

## Hands-on and Recap (~3 min, then practice)

## Slide 11 — Hands-On

"Hands-on. Part A — a mini server with one read-only tool, checked in the Inspector. Part B — connect it and ask three questions. Part C — ask the agent to change the data and understand why it can't. And write your own five-item checklist."

---

## Slide 12 — Checkpoint

"Checkpoint: the code and call trace, your checklist and one sentence on why a tool's result can't be treated as an order from you. If that sentence won't come — go back to slide 9."

---

## Slide 13 — Recap

"To sum up: MCP is one plug. A server offers tools, resources and prompts. Plugging in is trust, so read-only, vetted code and nothing personal. Tool results are untrusted text."

---

## Slide 14 — Next Up

"Next — memory. How an agent remembers you and your project between sessions, and why remembering everything is a bad idea."
