# Module 8 — Multi-Agent Orchestration

## Learning objectives
- Compose more than one agent role on a single task
- Judge when parallelism/specialization helps vs. when it just adds
  coordination overhead

## Key concepts
- Implementer/reviewer split: one agent writes the change, a second
  (ideally with no memory of the first's reasoning) reviews it fresh —
  catches things the implementer is blind to because it "knows what it
  meant"
- Orchestrator/worker fan-out: a coordinating agent breaks a large task
  into independent pieces and dispatches them to worker agents, then
  integrates results
- Critic-executor loops: an agent's output is critiqued and revised
  before being accepted, without a human in the loop for every pass
- Cost/benefit: extra agent passes cost time and tokens; reserve
  multi-agent setups for changes where an extra independent check is
  worth that cost (see Module 9 on what "worth it" means)

## Lab
Set up a two-agent pipeline on a nontrivial change: one agent implements,
a second — started fresh, given only the diff and original task, not the
first agent's reasoning — reviews before merge.

## Deliverable
The pipeline transcript and a list of any issues the reviewer agent
caught that the implementer missed (or a note that it caught nothing,
which is itself a data point on when this is worth the overhead).
