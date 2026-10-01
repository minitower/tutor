# Module 13 — CI/CD & Automating Agent Workflows

## Learning objectives
- Let agents participate in pipelines and repo automation without
  giving up control over irreversible actions

## Key concepts
- Hooks and scheduled/triggered agents: running an agent in response to
  an event (PR opened, issue filed, schedule) rather than an interactive
  session
- Agents-in-CI patterns: auto-fixing lint failures, triaging incoming
  issues, drafting (not sending) release notes
- Permission scopes and sandboxing: what an unattended agent should
  never be allowed to do (force-push, delete data, send external
  messages, spend money) without an explicit human-in-the-loop gate
- Designing the gate itself: what "approval" looks like when there's no
  human watching in real time (e.g., PR review required before merge,
  even if the agent opened the PR)

## Lab
Wire an agent into one CI step or git hook (e.g., auto-fix lint on PR,
or draft a changelog entry from commits) with an explicit approval gate
before anything destructive or externally visible happens.

## Deliverable
The working pipeline config, plus a short written note enumerating what
this automation is *not* allowed to do unattended, and why each of those
boundaries was chosen.
