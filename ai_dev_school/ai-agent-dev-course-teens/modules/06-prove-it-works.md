# Module 6 — Prove It Works

## Big idea

A test is a small piece of code that checks whether your program does
what you think it does — instead of you just looking at it and going
"yeah, looks right." Writing a test that **fails first**, because of a
real bug, and then fixing the bug so the test **passes**, proves the fix
actually fixed something — instead of just looking like it did.

## Why it matters

"It looks right" and "it is right" are different things, and the gap
between them is where bugs hide — especially bugs that only show up with
specific inputs you didn't happen to try by hand.

## Hands-on task

1. Find (or intentionally create) a small bug in your project — something
   with a clear right answer, like a scoring function that's off by one,
   or a form that accepts something it shouldn't.
2. Ask the agent to first write a test that **fails** because of the bug
   — and check that it actually fails for the right reason, not a typo
   in the test itself.
3. Then ask it to fix the bug.
4. Confirm the test now passes, and that you didn't break anything else.

## Checkpoint

Two separate save points (commits, or just two clearly labeled saves):
one with just the failing test, one with the fix. Plus: did the agent's
first attempt at the test actually catch the real bug, or did you have
to correct it?

## Supervisor note

Standard supervision. If your project doesn't have an obvious "bug" yet,
this is a fine excuse to intentionally introduce a small one on purpose
— the point is the process, not finding a real defect.
