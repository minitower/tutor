# Session 3 — Teach the Machine a Trick

## For You

There are things you always do the same way — like making a sandwich: bread, butter, cheese. We can write such a sequence on a **Trick Card**, like a recipe. Say the magic word — and the machine does it step by step, exactly as written. And later a friend can repeat the same trick too!

## Trick Card

> The trick is called: ______
> When I say the magic word ______, do this:
> Step 1: ______   Step 2: ______   Step 3: ______

## For the Grown-Up

1. In Claude Code such a card is a **skill**: a folder with a `SKILL.md` file. The machine reads it only when this trick is needed. A good first trick is a drawing, e.g. "draw a monster" (three steps: body, eyes, smile). Only safe steps — drawing and writing on the page, no commands and no files outside the course folder.
2. Help the kid fill in the card: the magic word is short (one word), three steps, each small and clear. Read it aloud.
3. Save the trick as a skill: `~/kid-ideas/.claude/skills/monster/SKILL.md`. Inside: front matter between `---` (`name: monster`, a `description:` — what it does and when, `disable-model-invocation: true`) and the kid's steps as a list. This way the trick runs only on the magic word — `/monster`.
4. Start a **new** session (a blank page) and ask the kid to say the magic word: `/monster`. Read aloud what the machine does and check together: was each step from the card done?
5. If a step came out wrong, that's normal: not "the machine is bad" but "the card wasn't exact". Fix the step's wording in the file and try again.
6. Finale: let a friend or relative say the magic word in another session — the trick works for anyone, because it's written on the card.

## Show & Tell

Ask: "How is a Trick Card different from an Idea Card?" (An Idea Card makes one thing; a Trick Card repeats the same thing again and again.)
