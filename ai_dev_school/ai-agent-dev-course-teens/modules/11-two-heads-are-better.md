# Module 11 — Two Heads Are Better

## Big idea

One agent can build something. A **second, completely fresh** agent —
one that wasn't involved in building it and doesn't know the first
agent's reasoning — can review it with fresh eyes. This is like swapping
papers with a classmate before turning an assignment in: the person who
wrote it is too close to see their own mistakes; someone new isn't.

## Why it matters

The agent that built something tends to assume its own choices were
reasonable — it "knows what it meant." A fresh session has no such bias
and will catch things the builder is blind to.

## Hands-on task

1. In one session, build a moderately-sized feature.
2. Start a **brand new session** with no memory of the first one. Give it
   only the diff/result and the original task — not the first agent's
   reasoning or explanations.
3. Ask it to review: does this actually do what was asked? Anything
   missing, wrong, or off?

## Checkpoint

- What did the reviewer session catch that you (and the builder session)
  missed?
- If it caught nothing — is that because the work was genuinely solid,
  or because the review wasn't looking hard enough? How would you tell
  the difference?

## Supervisor note

Standard supervision. Good discussion moment: this is exactly how code
review works on real software teams, just with an AI reviewer standing
in for a human teammate.
