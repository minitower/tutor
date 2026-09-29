# Module 1 — How the Agent Thinks: The Loop

## Big idea

The agent doesn't produce a finished answer in one leap. It works in a
loop: **think about what to do next → do that one thing → look at what
happened → think again** — repeating until the task looks done. Each
"do that one thing" is called a tool call: reading a file, editing code,
running a command, searching for something.

Think of it like a cook following a recipe but tasting as they go — not
dumping every ingredient in at once and hoping. Each step informs the
next one.

## Why it matters

Once you can see the loop, you can debug it. If the agent goes wrong,
it's almost always at one specific step in that loop — not a mysterious
total failure. Knowing this turns "it's broken" into "step 4 did the
wrong thing," which is a problem you can actually fix.

## Hands-on task

1. Pick a small task with a few moving parts — e.g. "add a new page to
   my site with a nav link to it" or "add a function that scores the
   player and hook it up to the display."
2. Give the agent the task.
3. As it works, keep a running list: every file it reads, every edit it
   makes, every command it runs, in order.
4. When it's done, go back through your list and write one line next to
   each step: *why* do you think it did that?

## Checkpoint

Turn in (or just talk through with your supervisor):
- The ordered play-by-play list
- One step that surprised you — either because you didn't expect it, or
  because it wasn't what you'd have done first

## Supervisor note

Low risk if the task is scoped to files you created in Module 0's
folder. This is a good module to sit through together at least once —
narrating the loop out loud ("okay, now it's reading that file, why do
you think?") builds the habit faster than doing it solo.
