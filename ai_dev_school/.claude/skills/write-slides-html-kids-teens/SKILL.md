---
name: write-slides-html-kids-teens
description: >
  How to write or extend slides.html for the two younger-audience tracks
  of this course — ai_dev_school/ai-agent-dev-course-kids (ages 7-8) and
  ai_dev_school/ai-agent-dev-course-teens (ages 14-17) — each with its
  own deliberately different visual theme (deck.css) and icon/illustration
  set from the adult course and from each other. Use this skill whenever
  asked to add or restyle slides in either kids or teens module folder,
  design a mascot/icon/illustration for one of them, or pick colors for
  a kids- or teens-oriented slide. For the underlying page mechanics
  (skeleton, deck.js behavior, the local-server verification workflow,
  overflow fixes) defer to the sibling skill `write-slides-html` in
  ai-agent-dev-course/.claude/skills — this skill only covers what's
  *different* for these two audiences: palette, tone, and components.
---

# Kids and teens slide themes

Two more audience tracks exist alongside the professional course, each
with its own `assets/deck.css` + `assets/deck.js` (the JS is copied
verbatim from the adult course — it's audience-agnostic, don't touch it):

- `ai-agent-dev-course-kids/assets/` — ages 7-8, zero prior coding
  experience, 15-25 min sessions, content is sparse (one idea per slide)
- `ai-agent-dev-course-teens/assets/` — ages 14-17, "reads like a strong
  intro coding elective... teens want to be taken seriously, not talked
  down to" (their own README's words — keep that in mind before adding
  anything that reads as babyish)

**The whole point is that all three tracks (adult/kids/teens) look
unmistakably different from each other**, not just recolored. Read
`references/kids.md` or `references/teens.md` for the full palette,
tone, and component list before writing a slide for either — don't
reuse the adult `write-slides-html` component vocabulary (`.compare`,
`.trio`, the pink-robot/blue-user icons) here; these two tracks have
their own.

## Quick orientation

| | Kids | Teens | Adult (reference) |
|---|---|---|---|
| Feel | warm, bouncy, tactile | dark, neon, "gamer/creator" | dark, muted, professional |
| Default slide alignment | centered, one idea per slide | left-aligned, denser | left-aligned, denser |
| Background | warm cream + soft dot texture | near-black + violet/mint glow | flat near-black |
| Shape language | thick rounded borders, drop shadows | thin glowing borders, gradients | thin flat borders |
| Mascot/character | yes — a friendly screen-and-keyboard robot | no mascot — a geometric "AI orb" icon instead | no mascot — plain robot icon |
| Typography trick | huge weight + gradient text, no bullets-as-default | gradient glow text, badge chips | gradient text (subtler), tables |

Full palettes and component snippets are in the reference files — don't
guess colors from memory, copy the hex/var values from there so new
slides stay consistent with the ones already built (both tracks have a
finished Module 0 deck to match against:
`modules/00-meet-the-idea-machine/slides.html` for kids,
`modules/00-meet-your-ai-partner/slides.html` for teens).

## The one gotcha specific to these themes

A standalone illustration SVG (not one of the fixed-size icon-row/card
icons, which get an explicit CSS `width`) can render at **0×0** if you
only constrain it with `max-width` and it sits inside a slide that uses
`align-items: center` (the `title`/`quote`-style centered layouts both
kids and teens lean on much more than the adult deck does). A bare
`<svg viewBox="...">` has no intrinsic size of its own — only
`max-width` — so the flexbox shrink-to-fit calculation can resolve it to
zero instead of falling back to the viewBox size.

**Fix:** give any standalone scene SVG an explicit pixel `width` (either
as an SVG attribute or inline `style="width:Npx"`), not just a
`max-width` cap. The `.svg-scene`/`.svg-scene.small` wrapper classes
still work for centering — just don't rely on them alone to size the
SVG itself.

## Verification

Same mechanics as the adult skill (serve, don't open `file://` directly;
test at 1440×810; bump `?v=N` to force reload since hash-only nav
doesn't re-trigger `deck.js`). A launch config `ai-school-slides` at the
repo root's `.claude/launch.json` serves all three tracks at once
(`ai_dev_school/` as the root), so both `ai-agent-dev-course-kids/...`
and `ai-agent-dev-course-teens/...` paths are reachable on the same
server — use that instead of adding another one-off config.
