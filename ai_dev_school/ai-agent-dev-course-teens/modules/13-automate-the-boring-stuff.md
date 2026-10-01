# Module 13 — Automate the Boring Stuff

## Big idea

Once something works and you find yourself doing it by hand over and
over — running your tests, checking your code style, repeating the same
small routine — you can often set the agent up to do it automatically
from then on. The important part is deciding, on purpose, what it's
allowed to do without asking versus what always needs your okay first.

## Why it matters

Automation is a multiplier — it multiplies good habits *and* mistakes
equally. Something that quietly does the wrong thing automatically, over
and over, is worse than something that does it once by hand. The
approval-gate habit from Module 8 matters even more here.

## Hands-on task

1. Pick one small, repeated chore in your project — e.g. "run all my
   tests and tell me what failed" or "check my code follows the style
   rules from Module 7."
2. Set it up as something you can trigger easily (a saved routine, a
   hook, whatever your tool supports) rather than re-explaining it every
   time.
3. Explicitly decide: does this need your approval every time it runs,
   or can it just run and report back? Write down why.
4. Test it a few times, including once on purpose with something that
   should fail, to confirm it actually catches problems instead of
   always saying "looks good."

## Checkpoint

- What does the automation do fully on its own, and what does it still
  ask you about?
- Why did you draw that line where you did? What would make you move it
  in either direction?

## Supervisor note

Standard supervision, but review the "runs without asking" list
together once — this is the module most likely to quietly expand scope
over time if left unchecked.
