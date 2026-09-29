# Further Themes: Agent System Development

The course so far teaches how to **direct** an agent as a developer
(Modules 1–11). This is a different layer: themes worth investigating
about how agent *systems* themselves are designed and built — relevant
if the course should grow a second track for people building agents and
agent tooling, not just people using them to write code.

Each theme below is a candidate for its own module, a guest lecture, or
just further reading — not yet scoped to lab exercises like the main
syllabus.

---

## 1. Context Engineering
What actually goes into the context window, and in what order/format.
- Static instructions vs. dynamically retrieved context — when to inject
  what, and the cost of getting it wrong (irrelevant context degrades
  output, not just wastes tokens)
- Context compaction/summarization: what's safe to lose, what must
  survive as a durable artifact instead (ties back to Module 3's DDD
  argument — files outlive context windows)
- Structuring long-lived project knowledge (`CLAUDE.md`/`AGENTS.md`-style
  files) as a design problem, not just a doc-writing exercise

## 2. Tool & Interface Design for Agents
Designing the tools an agent calls, as opposed to using existing ones.
- Granularity: one broad tool vs. many narrow ones — tradeoffs in
  reliability, discoverability, and error surface
- Error messages as a UX problem for a model, not a human: what makes an
  error recoverable by the agent vs. a dead end
- Read vs. write vs. destructive action boundaries, and how permission
  scoping should be reflected in tool design itself, not just policy
- Emerging standards (e.g. MCP) for tool interoperability across agent
  hosts

## 3. Memory Architectures
Beyond a single session's context window.
- Short-term (session) vs. long-term (cross-session) memory — what
  belongs in each
- Episodic vs. semantic memory: remembering *what happened* vs.
  remembering *facts/preferences*
- Retrieval strategies: vector search vs. structured/file-based memory
  vs. hybrid — and the failure modes of each (stale retrieval, false
  positives, retrieval that contradicts current reality)
- Memory hygiene: contradiction resolution, decay/expiry, and avoiding a
  memory store that quietly becomes an unreviewed second codebase

## 4. Planning & Reasoning Strategies
How an agent decides its next action.
- ReAct-style interleaved reasoning/action vs. plan-then-execute vs. tree
  search/best-of-N approaches — when each is worth its extra cost
- Self-critique and reflection loops: does making the agent check its
  own work actually catch errors, or just add latency and confident
  re-affirmation of the same mistake?
- Where human approval gates should sit in a plan (ties to Module 5)
  from the *system design* side: how do you build a good approval
  checkpoint, not just decide to have one?

## 5. Multi-Agent System Design
Beyond the workflow patterns in Module 8 — the underlying mechanics.
- Coordination/communication protocols between agents (shared scratch
  files, message passing, blackboard patterns)
- Conflict and race conditions when multiple agents can act concurrently
  on shared state (a codebase, a database, a document)
- Emergent/unintended behavior in agent-to-agent loops — how you'd even
  detect it
- Cost of coordination: at what point does orchestration overhead exceed
  the value of parallelism?

## 6. Evaluation of Agent Systems
Testing agents is not the same problem as testing deterministic software.
- Building eval harnesses for agentic (multi-step, tool-using) tasks
  rather than single-shot prompt evals
- Handling non-determinism: what does "regression" mean when the same
  input can produce different valid outputs?
- Benchmark design and its failure modes (overfitting to a benchmark,
  benchmarks that reward confident-but-wrong answers)
- Sandboxed/simulated environments for safely evaluating agent actions
  before granting real-world permissions

## 7. Observability & Debugging
Understanding *why* an agent did something after the fact.
- Tracing decision chains: tool calls, intermediate reasoning, and what
  actually needs to be logged for a debuggable system vs. what's noise
- Cost/latency/token telemetry as an operational concern, not an
  afterthought
- Building a failure-mode taxonomy for a given agent system (what
  actually goes wrong in production, categorized) — and feeding it back
  into tool/prompt design

## 8. Safety, Robustness & Guardrails (systems side)
Complements Module 9/10's practitioner view with the builder's view.
- Defending against prompt injection at the system level (untrusted
  content isolation, capability restrictions, output filtering) rather
  than relying on the agent "noticing"
- Blast-radius containment: sandboxing, least-privilege tool grants,
  reversibility as a design property of the action space itself
- Red-teaming an agent system deliberately — what does that process look
  like, who owns it

## 9. Human-Agent Interaction Design
The interface layer between people and the agent system.
- Calibrating trust: how does a system communicate its own uncertainty
  or the risk level of an action, so humans know when to look closely?
- Designing approval/review UX that people will actually use carefully,
  instead of rubber-stamping (a real failure mode once agents are fast)
- Explainability: how much of an agent's reasoning should be surfaced,
  and in what form, for a human to usefully audit it

## 10. Operating Agent Systems at Scale
Once past a single developer's session.
- Concurrency, rate limiting, and cost control across many simultaneous
  agent sessions
- Versioning agent behavior over time (prompt/model/tool changes) and
  regression risk when any of those change under a stable-looking
  interface
- Incident response when an agent system misbehaves in production — who
  gets paged, what gets rolled back, how fast

## 11. Domain-Specific Agent Design
How much of this generalizes vs. needs rethinking per domain.
- Coding agents vs. research/analysis agents vs. customer-facing agents
  — what design choices actually transfer, and which don't
- Vertical-specific tool and guardrail design (e.g. what a finance or
  healthcare agent's tool surface should look like vs. a coding agent's)

---

## Suggested next step

Pick 2–3 of these that best match who the course is actually for:
- If the audience stays **developers using agents**, themes 1, 6, 8, and
  9 extend the existing modules most naturally (context engineering
  deepens Module 1/3; evaluation deepens Module 9; guardrails deepens
  Module 10).
- If the course should grow a second track for **people building agent
  systems/tooling**, themes 2–5, 7, 10, and 11 are closer to a full
  syllabus of their own.
