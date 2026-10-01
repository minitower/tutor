# Module 8 — Plan Before You Build

## Big idea

For a change that touches more than one part of your project, agree on
*how* it'll get done before any code changes — like agreeing on a route
before a road trip instead of turning left because it felt right in the
moment. Claude Code has a plan mode for exactly this: the agent proposes
an approach and which files it'll touch, you review it, and only then
does it start editing.

This is different from Module 6's written plan — that one is something
*you* write up front about what you want. This one is the *agent*
proposing how it'll get there, which you check before it starts.

## Why it matters

Big changes that go wrong are expensive to undo. Catching a bad approach
in the plan, before any files change, costs you a minute. Catching it
after is a much bigger cleanup.

## Hands-on task

1. Pick a change that touches at least 2–3 files or parts of your
   project (e.g. renaming something used in several places, or adding a
   feature that needs both a new file and edits to an existing one).
2. Use plan mode — ask the agent to explain its approach before making
   any edits.
3. Read the plan. Does it make sense? Is anything missing, or is it
   planning to touch something it shouldn't?
4. Approve (or push back and ask it to revise) before letting it build.

## Checkpoint

- Did the actual result match the plan?
- Was there anything in the plan you didn't understand until you saw it
  built? That's worth asking about next time, before approving.

## Supervisor note

Standard supervision. Worth sitting in for the "read the plan before
approving" step at least once — this is the habit that matters most
here, more than the specific project.
