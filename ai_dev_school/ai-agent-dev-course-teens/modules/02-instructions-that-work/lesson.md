# Module 2 — Instructions That Actually Work

## Big idea

The agent can't read your mind — it can only work with what you actually
say. "Make it better" means something different to everyone (including
the agent, differently every time). The gap between "what I meant" and
"what I typed" is where most bad results come from — not from the agent
being bad at coding.

## Why it matters

This is the single highest-leverage skill in the whole course. Getting
better at this one thing improves every module after it.

## Hands-on task

Pick one small feature for your project. Write three versions of the
request and run each in a **separate, fresh session** (so earlier
attempts don't leak context into later ones):

1. **Vague:** e.g. "add a leaderboard"
2. **Specific:** e.g. "add a leaderboard showing the top 5 scores,
   sorted highest first"
3. **Very specific:** add exact behavior for ties, what happens with
   fewer than 5 scores, and where on the page it should appear

Compare the three results.

## Checkpoint

- Which version got closest to what you actually wanted, first try?
- Was there a point where being *more* specific stopped helping? What
  was still left for the agent to reasonably decide on its own?

## Supervisor note

Standard supervision level. Good moment to point out: writing instructions
this carefully is a transferable skill — it's the same muscle as writing
clear directions for a group project, or a clear bug report.
