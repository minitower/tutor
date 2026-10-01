# Module 2 — MCP: Connecting Agents to External Systems

## Learning objectives
- Understand what problem MCP solves and connect external systems to an agent safely

## Key concepts
- Host / client / server architecture, JSON-RPC, the stdio and Streamable HTTP transports
- Primitives: tools, resources, prompts; elicitation and extensions
- Practice: `claude mcp add`, `.mcp.json`, a DB through MCP, open servers, your own Python server
- Choosing between MCP, CLI, Skill and hook
- Security: injection via tool output, tool poisoning, supply chain, permissions; MCP in CI and multi-agent systems

## Lab
Connect a read-only DB through MCP, prove writes are blocked, write a mini server and check it in the Inspector.

## Deliverable
A secret-free `.mcp.json`, the call trace, the mini-server code and a threat note with countermeasures.
