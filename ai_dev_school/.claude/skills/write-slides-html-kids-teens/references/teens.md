# Teens theme (ages 14-17) — `ai-agent-dev-course-teens/assets/deck.css`

## Palette

```
--bg:       #090c16   near-black navy (deliberately a different hue
--bg-2:     #10152a   from the adult deck's #0b0d12, so it doesn't just
                       look like "the same dark mode")
--fg:       #eef0fc
--fg-dim:   #8891b5
--accent:   #7c5cff   electric violet — primary
--accent-2: #00e6a8   neon mint — success/go
--accent-3: #ff3e7f   hot pink/red — alert/emphasis
--accent-4: #00c2ff   electric cyan — secondary/info
--radius:   18px
```

Saturation is the key difference from the adult theme: adult uses muted,
desaturated accents on flat dark backgrounds with 1px borders and no
glow. Teens uses fully saturated neon accents, actual glow (`box-shadow`
/ `filter: drop-shadow`) on key elements, and gradient text more
liberally. Both are "dark mode," but they should never be mistaken for
each other at a glance.

Tone-check before adding content: this audience's own README says they
"want to be taken seriously, not talked down to" — no mascot character,
no baby-ish copy. The visual energy comes from color/glow/gamification
motifs (badges, "checkpoint" callouts), not from cute illustration.

## Components

- **`.myth-grid` + `.myth-card.myth` / `.myth-card.real`** — a two-card
  "common misconception → what's actually true" pattern, used a lot
  since the course content itself is framed as myth-busting:
  ```html
  <div class="myth-grid">
    <div class="myth-card myth"><span class="badge">Миф</span><p>...</p></div>
    <div class="myth-card real"><span class="badge">На самом деле</span><p>...</p></div>
  </div>
  ```
  Pink badge/border for the myth side, mint for the reality side — this
  is the teens-track equivalent of the adult `.compare .before/.after`,
  but don't literally reuse `.compare` here (different class, different
  visual treatment — badges instead of card headers).
- **`.checkpoint`** — a mint-glow callout box for reflection/self-check
  moments (this track has a "Чекпоинт" at the end of most modules):
  ```html
  <div class="checkpoint">
    <div class="label">✅ Проверь себя</div>
    <p>Reflection prompt text.</p>
  </div>
  ```
- **`.chip`** — a small glowing pill for inline emphasis on a single
  term (e.g. "spoken permission" mid-sentence), not a whole block:
  `<span class="chip">🔒 разрешение</span>`.
- **`<pre><code>`** — same tag as the adult deck but restyled: violet
  glow border (`box-shadow`) and mint-green code text instead of the
  adult's plain white-on-black. Good for the agent-loop diagrams this
  track presents as plain-text cycles (`ЧИТАЕТ → ПИШЕТ → ЗАПУСКАЕТ →
  ПРОВЕРЯЕТ`) — no need to redraw those as SVG loops, the glowing code
  block treatment already makes them feel distinct/technical.
- **`.svg-scene` / `.svg-scene.small`** — same wrapper concept as the
  adult deck, but icons get a `drop-shadow` glow automatically via CSS
  (`.svg-scene svg { filter: drop-shadow(...) }`) — don't add glow
  per-icon, it's already on the wrapper rule.

## Icon library

**AI-partner orb** (this track's answer to a mascot — geometric, not a
character): two concentric hexagons (outer faint, inner at 60% opacity)
around a radial-gradient-filled circle core:
```svg
<svg viewBox="0 0 200 200" width="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="orbGrad" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="var(--accent-4)"/>
      <stop offset="55%" stop-color="var(--accent)"/>
      <stop offset="100%" stop-color="var(--accent-3)"/>
    </radialGradient>
  </defs>
  <polygon points="100,20 170,60 170,140 100,180 30,140 30,60" fill="none" stroke="var(--border)" stroke-width="2"/>
  <polygon points="100,45 148,72 148,128 100,155 52,128 52,72" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".6"/>
  <circle cx="100" cy="100" r="34" fill="url(#orbGrad)"/>
  <circle cx="100" cy="100" r="34" fill="none" stroke="#fff" stroke-width="1" opacity=".3"/>
</svg>
```
**Give this an explicit `width` attribute** (as above) — it's exactly
the shape that hit the 0×0 collapse bug described in the main SKILL.md
when it only had `max-width` inside a centered title slide.

If a `<defs>` `id` (like `orbGrad` above) is reused on a second SVG in
the *same page*, IDs must be unique per document — suffix a second orb
as `orbGrad2` etc. if a module ever needs more than one on one slide.

Every component above has a full working example already in
`modules/00-meet-your-ai-partner/slides.html` — copy from there.
