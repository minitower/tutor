# Session 1 — Doors for the Machine

## For You

Guess what? The machine lives in a room with no windows. It can only see what's inside its room. But a room can have a **door** — and then the machine can peek at exactly one thing outside: a list of your favorite animals, for example. You (with a grown-up) decide which door to open. Today we'll open one door — a "look-only" door.

## Idea Card

> The machine should know about: my favorite ______
> The door leads to: a list called ______
> This door is "look-only" 👀 — no changing, no erasing

## For the Grown-Up

1. This is the first session where the machine gets a "superpower". It comes right after Session 0. Everything stays local: no accounts, no internet, no passwords.
2. Create a separate `facts` folder inside the course folder (for example `~/kid-ideas/facts`) and, together with the kid, write three favorite animals and one fact about each into `animals.txt` (for example: "elephant — the biggest"). You type.
3. Open the "door" — connect the MCP "Filesystem" server to Claude Code, limited to that folder only: `claude mcp add --transport stdio kidfacts -- npx -y @modelcontextprotocol/server-filesystem ~/kid-ideas/facts`. Then make it look-only: deny the server's write tools in the settings — you can see the list in `/mcp` (something like `write_file`, `edit_file`, `move_file`). Check the names against the server's README — they may change.
4. Read aloud what Claude Code asks permission for. Ask: "Look through the kidfacts door and tell me which animal on the list is the biggest." Let the kid see the answer.
5. Close the door (`claude mcp remove kidfacts` or switch it off in `/mcp`) and ask the same question. The machine will say it can't see the list. The takeaway for the kid: the door decides what the machine can see.
6. If you'd rather not install a server, run the session "on paper": you are the "door", the kid asks the machine (you) questions, and you answer only with what's written on the list sheet. Same point.

## Show & Tell

Ask: "Which door did we open? What could the machine do through it — and what couldn't it do?" The kid should say in their own words: "only look, never change."
