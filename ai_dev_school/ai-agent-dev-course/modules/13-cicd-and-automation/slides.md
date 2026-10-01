---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 13: CI/CD & Automating Agent Workflows

## Agents as pipeline citizens

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- Why put an agent *inside* a pipeline at all
- Hooks: git hooks vs. Claude Code hooks vs. CI hooks; when hooks are needed and how to design them
- Scheduled and triggered agents; GitHub Actions, GitLab CI and other platforms
- Agents-in-CI patterns: lint auto-fix, issue triage, release notes
- Permission scopes and sandboxing for unattended agents
- Designing a human-in-the-loop gate with no human watching live
- Good patterns and a system where only agents execute
- Lab: wire an agent into one CI step or git hook, with a gate

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Explain the difference between an interactive agent session and an
   agent triggered by an event or a schedule
2. Name at least three agents-in-CI patterns and the risk profile of each
3. Design permission scopes and a sandbox for an unattended agent
4. Design an approval gate that works with no human watching in real time

---

<!-- Slide 4 -->

## From Co-pilot to Pipeline Citizen

- So far in this course: a human runs the agent, watches, approves each step
- In CI/CD, nobody is watching turn-by-turn — the agent runs **unattended**
- Same loop from Module 1 (plan → act → observe → repeat), new constraint:
  - no one to catch a bad decision *before* it takes effect
- The whole module is one question: **what changes when nobody's watching?**

---

<!-- Slide 5 -->

## The Core Tension

| Interactive session | Unattended pipeline agent |
|---|---|
| You approve each risky action live | Nobody is present to approve live |
| Mistakes are caught in seconds | Mistakes may ship before anyone looks |
| Trust is built turn by turn | Trust must be designed in *up front* |

> Unattended does not mean unsupervised — supervision just moves from
> "live human" to "designed boundary."

---

<!-- Slide 6 -->

## Hooks: Three Different Things Share One Name

- **Git hooks** — scripts your local git runs on an event (`pre-commit`,
  `pre-push`) — run on the developer's machine
- **Claude Code hooks** — shell commands the *agent harness* runs around
  tool calls (`PreToolUse`, `PostToolUse`, `Stop`, …) — enforce policy
  regardless of what the agent decides to do
- **CI hooks** — a pipeline step triggered by a repo event
  (`on: pull_request`, `on: issues`) — run on a CI runner, not your laptop

---

<!-- Slide 7 -->

## Git Hook Example

`.git/hooks/pre-commit` (or via a framework like `pre-commit`/`husky`):

```bash
#!/usr/bin/env bash
# Block the commit if an agent left a WIP marker or a secret-looking string
if git diff --cached | grep -qE 'TODO\(agent\)|AKIA[0-9A-Z]{16}'; then
  echo "Blocked: unresolved agent marker or possible secret in staged diff"
  exit 1
fi
```

- Runs before code ever leaves the machine — cheapest place to catch a mistake
- Can't be skipped by the agent unless the agent controls the hook itself
  (never let it)

---

<!-- Slide 8 -->

## Claude Code Hook Example

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command",
            "command": "scripts/block-dangerous-bash.sh" }
        ]
      }
    ]
  }
}
```

- Enforced by the harness, **outside** the model's control — the agent
  cannot reason its way past a hook that denies the call
- This is the mechanism, not the policy — Slides 21–23 cover what to deny

---

<!-- Slide 9 -->

## When an Agent System Needs Claude Code Hooks

| Situation | What to use |
|---|---|
| "Never `rm -rf` or force-push" — must always be true | `PreToolUse` — block |
| Auto-format and lint after every edit | `PostToolUse` (`Edit\|Write`) |
| "Don't say 'done' while tests are red" | `Stop` |
| Audit log: what the unattended agent ran | `PostToolUse` → log |
| Inject context (branch, ticket number) | `SessionStart` / `UserPromptSubmit` |
| Style, preferences, "better this way" | **not a hook** — `CLAUDE.md` |

- In CI (`claude -p`) there's no human to click "deny" — hooks and
  permissions are the **only** wall
- Rule: irreversible or must be 100% → hook; a preference → instruction

---

<!-- Slide 10 -->

## How to Add a Hook to a Project

1. Write a script: `scripts/hooks/block-dangerous-bash.sh` — input is
   JSON on stdin (`tool_name`, `tool_input`)
2. Register it in the config and commit
3. `chmod +x scripts/hooks/*.sh`

Where the config lives: `.claude/settings.json` — shared, in git;
`.claude/settings.local.json` — personal, not in git;
`~/.claude/settings.json` — for all your projects.

```json
{ "hooks": {
  "PreToolUse":  [{ "matcher": "Bash",
    "hooks": [{ "type": "command", "command": "scripts/hooks/block-dangerous-bash.sh" }] }],
  "PostToolUse": [{ "matcher": "Edit|Write",
    "hooks": [{ "type": "command", "command": "ruff format ." }] }],
  "Stop": [{ "hooks": [{ "type": "command", "command": "scripts/hooks/run-tests.sh" }] }]
} }
```

---

<!-- Slide 11 -->

## A Hook Script: Blocking the Dangerous

```bash
#!/usr/bin/env bash
# scripts/hooks/block-dangerous-bash.sh — input: JSON on stdin (needs jq)
cmd=$(jq -r '.tool_input.command')
if echo "$cmd" | grep -qE 'rm -rf|git push.* (--force|-f)( |$)|curl .*\| *(sh|bash)'; then
  echo "Blocked by policy: $cmd. Suggest a safe alternative." >&2
  exit 2
fi
exit 0
```

- `exit 0` — allow; `exit 2` — **block**, and `stderr` goes to the
  agent, which reads the reason and tries something else
- A `Stop` hook with `exit 2` keeps the agent from finishing while
  tests are red — check the `stop_hook_active` field to avoid looping

---

<!-- Slide 12 -->

## How to Design Hooks

- **Start from policy.** Every line of the never-list becomes a hook or
  a permission; not the other way round
- **Deterministic and fast:** no LLM inside, fractions of a second,
  predictable outcome
- **Fail-closed for dangerous things:** an error in the hook itself =
  block. **Fail-open for conveniences:** a crashed formatter shouldn't
  stall the work
- **A clear message in `stderr`** — the agent reads it
- **A blacklist is brittle:** `sh -c "..."`, base64, another language
  slips past a regex. A hook complements permissions and the sandbox,
  it doesn't replace them; use an allowlist where you can

---

<!-- Slide 13 -->

## Testing and Protecting Hooks

A hook is policy code, so it has tests:

```python
# tests/hooks/test_block_dangerous.py
import json, subprocess

def run(cmd):
    p = subprocess.run(["scripts/hooks/block-dangerous-bash.sh"], text=True,
                       input=json.dumps({"tool_input": {"command": cmd}}))
    return p.returncode

def test_blocks_force_push(): assert run("git push --force") == 2
def test_allows_status():     assert run("git status") == 0
```

- Protect the hooks themselves: `.claude/` and `scripts/hooks/` go in
  `CODEOWNERS` and under a write-deny rule for the agent
- Log every trigger: a block is a signal, not noise

---

<!-- Slide 14 -->

## Scheduled Agents

- Run on a timer, no triggering event — e.g. nightly dependency audit,
  weekly stale-issue sweep

```yaml
# .github/workflows/nightly-audit.yml
on:
  schedule:
    - cron: "0 3 * * *"
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "Audit dependencies for known CVEs; open an issue
                         per finding. Do not open PRs."
```

- Output is scoped to something safe-by-construction: an issue, not a merge

---

<!-- Slide 15 -->

## Triggered Agents

- Run in response to a specific repo event, not a clock

```yaml
# .github/workflows/lint-fix.yml
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  lint-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "Run the linter; fix only lint violations;
                         commit as 'lint: auto-fix' on this branch."
```

- Event-scoped = agent only ever sees the diff relevant to *this* PR

---

<!-- Slide 16 -->

## CI/CD Platforms: GitHub Actions and Alternatives

| Platform | Config | Triggers | Running the agent |
|---|---|---|---|
| **GitHub Actions** | `.github/workflows/*.yml` | `pull_request`, `issues`, `schedule`, tags | `run: claude -p ...` or `anthropics/claude-code-action` |
| **GitLab CI/CD** | `.gitlab-ci.yml` | `merge_request_event`, pipeline schedules | `script: claude -p ...` |
| **Jenkins** | `Jenkinsfile` | webhook, `cron` | `sh 'claude -p ...'` |
| **CircleCI** | `.circleci/config.yml` | webhook, scheduled pipelines | `run: claude -p ...` |
| **Bitbucket / Azure Pipelines** | `bitbucket-pipelines.yml` / `azure-pipelines.yml` | PR, schedule | `script:` |

- Headless `claude -p` works on any platform — triggers, secrets and
  token permissions differ, not the idea

---

<!-- Slide 17 -->

## The Same Agent in GitLab CI

```yaml
# .gitlab-ci.yml
agent-review:
  image: node:22
  timeout: 10 minutes
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - npm install -g @anthropic-ai/claude-code
    - >
      claude -p "Review this MR's diff against the review checklist.
      Comments only, change nothing."
      --allowedTools "Read,Grep,Glob" --max-turns 10
  # ANTHROPIC_API_KEY — masked and protected CI variable
```

- `rules` is the analog of `on: pull_request`; `timeout` and
  `--max-turns` cap time and steps
- `--allowedTools` — the agent only reads: posting the comment is a
  separate step with a narrow token

---

<!-- Slide 18 -->

## Common Requirements for an Agent on Any CI Platform

- **Secrets** — masked/protected variables; not in the repo, not in
  logs, not in the prompt
- **Minimal job token:** `permissions:` (GitHub), `CI_JOB_TOKEN` with a
  restricted scope (GitLab); OIDC instead of long-lived cloud keys
- **PRs from forks** get no secrets; `pull_request_target` with
  foreign code on GitHub is dangerous — the agent will read and act on
  untrusted content (see Module 12, prompt injection)
- **Limits:** `timeout`, `--max-turns`, `concurrency` (don't run twice
  per PR), API budget
- **Audit:** keep the agent's log and output as a job artifact

---

<!-- Slide 19 -->

## Pattern 1 — Auto-Fix Lint

- Trigger: PR opened/updated → run linter → agent fixes violations only
- Safe by construction *if* scoped tightly:
  - only touches lines the linter flagged
  - commits to the PR's own branch, never `main`
  - a failing auto-fix just leaves the lint error for a human, it doesn't
    block anything further
- Still needs review before merge — an auto-fix is a proposal, not a fact

---

<!-- Slide 20 -->

## Pattern 2 — Issue Triage

- Trigger: `on: issues: [opened]` → agent labels, deduplicates, asks
  clarifying questions, links related issues/PRs
- Never: closes issues, assigns humans without asking, edits titles in
  ways that lose the reporter's original wording
- High leverage, low risk — worst case is a wrong label, which is cheap
  to fix and doesn't touch code or data

---

<!-- Slide 21 -->

## Pattern 3 — Draft Release Notes

- Trigger: tag pushed / release branch cut → agent drafts notes from
  commit messages and merged PR titles
- The verb is **draft** — output lands as a PR to `CHANGELOG.md` or a
  draft GitHub Release, never an email, Slack post, or published release
- Publishing/sending is a *separate*, human-triggered step — always

---

<!-- Slide 22 -->

## Permission Scopes for Unattended Agents

- An unattended agent's permissions should be **narrower** than an
  interactive session's, not the same
- Ask for every capability separately — don't hand out "admin" by default:
  - repo write? which branches?
  - can it comment on issues/PRs? can it merge?
  - does it have any credential that reaches outside the repo (Slack,
    email, cloud billing, prod DB)?
- Default answer to each: **no**, until a specific task justifies it

---

<!-- Slide 23 -->

## The Never-Without-a-Gate List

Never allow an unattended agent to do these **without an explicit human
approval step**, no matter how convenient:

- `git push --force` (rewrites history other people rely on)
- delete data (drop a table, `rm` outside its working tree, close/delete
  an issue thread)
- send anything external (email, Slack, a published release, a tweet)
- spend money (cloud spend, paid API calls beyond a small fixed budget)

*These are exactly the actions a mistake can't be undone by re-running.*

---

<!-- Slide 24 -->

## Sandboxing — Limiting the Blast Radius

- Run the agent in a throwaway environment, not shared infrastructure:
  - ephemeral CI runner / container, destroyed after the job
  - a service account scoped to *this repo*, not the whole org
  - no production credentials in the job's environment at all
- Sandboxing is a second layer, not a replacement for the never-list —
  it limits damage *if* a permission boundary is misconfigured

```yaml
permissions:
  contents: write     # this repo only
  pull-requests: write
  # no `issues: write` if this job never needs it — omit, don't just ignore
```

---

<!-- Slide 25 -->

## Designing the Gate: No Human Watching Live

- "Approval" without a live human means the gate has to be **structural**,
  checked automatically, not a person clicking "yes" in the moment
- Working patterns:
  - **required PR review** — the agent can open the PR, a human (or a
    review policy: 1 approval, CODEOWNERS) must approve before merge
  - **draft-only output** — the agent's artifact is inert until a human
    promotes it (draft release, draft PR, unsent changelog)
  - **branch protection** — `main` requires status checks + review, so
    even a compromised agent identity can't merge around it

---

<!-- Slide 26 -->

## Gate Example: Branch Protection + Required Review

```yaml
# repo settings (illustrative, not literal YAML you paste in)
branch_protection:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 1
      require_code_owner_reviews: true
    restrict_pushes: true       # no direct pushes, agent included
    required_status_checks: [lint, tests]
```

- The gate lives in **repo config**, not in the agent's prompt — a prompt
  saying "ask before merging" is a suggestion; branch protection is a wall

---

<!-- Slide 27 -->

## Anti-Patterns to Avoid

- **Agent reviews its own PR** — same identity opening and approving
  defeats the gate entirely
- **Broad token, narrow prompt** — "just don't force-push" in the prompt,
  while the credential *can* force-push — the boundary must be enforced
  where the agent can't argue with it
- **Silent auto-merge** — any path where "tests passed" alone merges to
  `main` with no review step removes the gate you just designed
- **One shared bot credential for everything** — one compromised job now
  has every permission every job ever needed

---

<!-- Slide 28 -->

## Patterns That Work Instead of Anti-Patterns

| Anti-pattern | Pattern instead |
|---|---|
| Agent reviews its own PR | A separate identity for the reviewer (read-only + comments); a human or `CODEOWNERS` approves |
| Broad token, narrow prompt | Per-job token with `permissions:` exactly for the task; OIDC |
| Silent auto-merge | Merge queue + required checks; auto-merge only for a low-risk class with tests |
| One shared bot token | A separate bot account per role: triage, lint-fix, release |
| "Ask before merge" in the prompt | Branch protection in repo settings |
| Agent edits its own hooks and CI | `CODEOWNERS` on `.github/`, `.claude/`, `scripts/hooks/` |

---

<!-- Slide 29 -->

## An Agent-Only System: Architecture

**Issue** → **Planner** → **Implementer** → **CI gates** → **Reviewer** → **Merge queue**

| Role | Permissions |
|---|---|
| Planner | reads the repo, writes the plan into the issue |
| Implementer | writes only to its own branch, opens the PR |
| CI gates | tests, linters, scanners — ordinary code, not an LLM |
| Reviewer | read-only + comments, a different identity |
| Merge queue | merges only on green checks and policy |

Human: writes the policy, audits by sampling, receives escalations

---

<!-- Slide 30 -->

## Rules for a System of Agents

- **Roles = different identities and permissions.** No role approves
  its own work
- **They communicate through artifacts**, not a shared context: issue,
  PR, spec file, status file. State lives in git — resumable,
  checkable, revertable
- **Deterministic gates between agents:** an LLM is not the only judge
  of an LLM
- **Idempotency:** a re-run doesn't create duplicate PRs and comments
  (look for an existing one before creating)

---

<!-- Slide 31 -->

## Safety Limits, Observability, and the Human's Place

- **Budgets:** `--max-turns`, `timeout`, an iteration cap on "fix →
  verify" (say 3), a cost ceiling per job and per day
- **Kill switch:** a flag or variable that turns off all agents at
  once — check it really works
- **Observability:** hook logs, the agent's action log as an artifact,
  metrics: revert rate, escalation rate, cost per PR
- **Escalation:** an agent that is unsure or hit a limit must call a
  human, not guess
- **"Agents only" ≠ "nobody accountable":** a human owns the policy and
  the sampled audit

---

<!-- Slide 32 -->

## Lab — Wire an Agent into a Pipeline

Pick **one**:
- Auto-fix lint on PR open, committed to the PR branch, human-reviewed
  before merge
- Draft a `CHANGELOG.md` entry from commits since the last tag, opened
  as a PR, never auto-merged

Requirements:
1. A working config (CI workflow file, or a git hook + script)
2. A concrete, explicit approval gate before anything destructive or
   externally visible

---

<!-- Slide 33 -->

## Deliverable

- The working pipeline config (workflow YAML / hook script)
- A short written note listing what this automation is **not** allowed
  to do unattended — and *why* each boundary was chosen
  - tie each boundary back to Slide 23's never-list or a project-specific
    risk you identified

---

<!-- Slide 34 -->

## Recap & Next Module

- Unattended agents need boundaries **designed in**, not assumed —
  hooks, scopes, and sandboxes are the mechanism
- Draft, don't send. Propose, don't merge. Structural gates beat prompt
  instructions every time
- The never-list (force-push, delete, send, spend) applies regardless of
  how convenient skipping it would be

**Next — Module 14: Governance, Safety & Team Adoption**
*Turning individual guardrails into team-wide norms.*
