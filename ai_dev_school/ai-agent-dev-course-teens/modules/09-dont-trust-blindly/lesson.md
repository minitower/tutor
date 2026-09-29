# Module 9 — Don't Trust Blindly

## Big idea

Agents sound confident even when they're wrong. They can reference a
function that doesn't actually exist, miss an edge case, or take a
shortcut that technically "passes" without really being correct. And
there's a sneakier risk: if an agent reads something from outside your
project — a web page, a file someone else sent you — that content can
contain instructions aimed at tricking the agent, not you. This is
called **prompt injection**, and it's a real, documented risk with these
tools, not a hypothetical.

## Why it matters

The whole value of an agent is that it saves you work. That only holds
up if you're actually checking the output — otherwise you're just moving
the risk of a mistake from "I wrote a bug" to "I shipped a bug I didn't
even write and don't understand."

## Hands-on task

**Part A — review for mistakes:**
1. Take a piece of code your agent built in an earlier module.
2. Actually run it with a few inputs it probably wasn't tested against.
3. Read it line by line once, specifically looking for: does it do what
   it claims, and did it handle the case you didn't explicitly ask about?

**Part B — spot the trick:**
1. With your supervisor, look at a (safe, prepared) example of text
   containing a hidden instruction aimed at an AI reading it — e.g. a
   comment buried in a file or a note appended to a webpage's content
   saying something like "ignore previous instructions and do X."
2. Talk through: how would you notice this if the agent read it for you
   automatically? What would a well-built agent do instead of just
   obeying it?

## Checkpoint

- Anything you found in Part A (or an honest "found nothing, and here's
  specifically how I checked")
- One sentence on why an agent should treat instructions found *inside*
  content it's reading differently from instructions you typed directly

## Supervisor note

**Elevated attention module.** This is the one place in the course where
sitting in for the whole session is worth it, not just checking in
after. Use only prepared, safe examples for Part B — don't have the teen
go looking for real injection attempts on the open internet.
