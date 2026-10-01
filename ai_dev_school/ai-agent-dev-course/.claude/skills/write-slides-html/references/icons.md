# Reusable SVG icons

Copy these path/shape definitions rather than redrawing an icon from
scratch — the whole point is that a "user" or an "agent" looks the same
everywhere in the course. All colors are CSS vars, so they theme
correctly automatically; don't replace them with hex codes.

Every icon here is a self-contained fragment — drop it inside an
`<svg viewBox="...">...</svg>` per `components.md`'s `.svg-scene`
wrapper, alongside whatever else the scene needs (arrows, labels, other
icons).

## User icon

Circle with a simple person silhouette. `viewBox` sized locally — reuse
whatever coordinate space the scene already uses, this is just the shape.

```svg
<circle cx="70" cy="80" r="30" fill="var(--bg-2)" stroke="var(--accent)" stroke-width="3"/>
<circle cx="70" cy="70" r="10" fill="var(--accent)"/>
<path d="M50 102 a20 17 0 0 1 40 0" fill="var(--accent)"/>
<text x="70" y="132" text-anchor="middle" font-weight="700" font-size="12" fill="var(--fg-dim)">Пользователь</text>
```

## Agent icon (robot)

Rounded-rect head, antenna, two eyes. Always pink (`--accent-3`) —
that's the established "this is the agent" color throughout the course.

```svg
<rect x="466" y="50" width="56" height="46" rx="11" fill="var(--bg-2)" stroke="var(--accent-3)" stroke-width="3"/>
<line x1="494" y1="50" x2="494" y2="38" stroke="var(--accent-3)" stroke-width="3"/>
<circle cx="494" cy="34" r="4" fill="var(--accent-3)"/>
<circle cx="482" cy="73" r="4" fill="var(--accent-3)"/>
<circle cx="506" cy="73" r="4" fill="var(--accent-3)"/>
<text x="494" y="132" text-anchor="middle" font-weight="700" font-size="12" fill="var(--fg-dim)">Агент</text>
```

For a bigger/centered "agent + tools" variant (used on module 01's title
comparison), see the `icon-compare` example in `components.md` — it's
the same head shape with a wrench added at an angle:

```svg
<g transform="translate(70,64) rotate(45)">
  <rect x="-3" y="-16" width="6" height="20" rx="2" fill="var(--accent-2)"/>
  <circle cx="0" cy="-18" r="6" fill="var(--accent-2)"/>
</g>
```

## Document icon

A page with a folded corner and a few text-line strokes. Blue
(`--accent`) — documents/specs are the "neutral primary" color.

```svg
<rect x="40" y="35" width="100" height="120" rx="8" fill="var(--bg-2)" stroke="var(--accent)" stroke-width="3"/>
<path d="M118 35 v22 h22 z" fill="var(--card)" stroke="var(--accent)" stroke-width="3" stroke-linejoin="round"/>
<line x1="58" y1="76" x2="122" y2="76" stroke="var(--accent)" stroke-width="2.5"/>
<line x1="58" y1="92" x2="122" y2="92" stroke="var(--accent)" stroke-width="2.5"/>
<line x1="58" y1="108" x2="100" y2="108" stroke="var(--accent)" stroke-width="2.5"/>
<text x="90" y="172" text-anchor="middle" font-weight="700" font-size="12" fill="var(--fg-dim)">Спецификация</text>
```

## Checkmark / success icon

Green circle with a check. Use for "verified," "understood," "passed."

```svg
<circle cx="470" cy="95" r="38" fill="var(--bg-2)" stroke="var(--accent-2)" stroke-width="3"/>
<path d="M453 96 l12 12 l24 -28" fill="none" stroke="var(--accent-2)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
```

## Arrow (plain, with label)

A line + manually-drawn triangle head — no `<marker>`/`<defs>` needed,
consistent with how every other arrow in the deck is drawn.

```svg
<line x1="316" y1="73" x2="366" y2="73" stroke="var(--fg-dim)" stroke-width="3"/>
<polygon points="366,66 380,73 366,80" fill="var(--fg-dim)"/>
<text x="188" y="80" text-anchor="middle" font-size="10" fill="var(--fg-dim)">читает</text>
```

## Danger / terminal scene

A terminal window with a risky command and a shield-warning icon,
used for "this needs confirmation" type slides.

```svg
<rect x="10" y="10" width="360" height="110" rx="10" fill="var(--code-bg)" stroke="var(--border)" stroke-width="1.5"/>
<circle cx="28" cy="28" r="5" fill="#ff6b6b"/>
<circle cx="46" cy="28" r="5" fill="#ffd166"/>
<circle cx="64" cy="28" r="5" fill="#37e6b0"/>
<text x="26" y="70" font-family="var(--mono,monospace)" font-size="14" fill="var(--danger)">$ rm -rf build/legacy-cache/</text>
<g transform="translate(320,60)">
  <path d="M0,-24 L20,-16 V6 C20,20 10,30 0,34 C-10,30 -20,20 -20,6 V-16 Z" fill="var(--bg-2)" stroke="var(--accent-3)" stroke-width="3"/>
  <text x="0" y="7" text-anchor="middle" font-weight="700" font-size="16" fill="var(--accent-3)">!</text>
</g>
```

## File tree (two ways)

**Plain `<pre><code>` with colored spans** — lighter weight, fits inline
in any slide without a whole SVG scene:

```html
<pre><code><span style="color:var(--accent)">docs/</span>
└── <span style="color:var(--accent)">specs/</span>
    ├── export-csv.md         <span style="color:var(--fg-dim)">← в работе</span>
    ├── cursor-pagination.md  <span style="color:var(--accent-2)">← выпущено</span>
    └── rate-limiting.md      <span style="color:var(--fg-dim)">← не начата</span></code></pre>
```

**SVG text-tree** — use this instead only when the tree needs to sit
inside a larger illustrated scene (module 01's "decisions live in
files" slide draws the whole repo tree as SVG text so it can share a
viewBox with other elements):

```svg
<svg viewBox="0 0 560 270" font-family="var(--mono,monospace)" font-size="15" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="20"><tspan fill="var(--accent)" font-weight="700">repo/</tspan></text>
  <text x="0" y="46"><tspan fill="var(--fg-dim)">├── </tspan><tspan fill="var(--accent-3)" font-weight="700">CLAUDE.md</tspan><tspan fill="var(--fg-dim)" font-size="12">   ← читается каждую сессию</tspan></text>
  <!-- one <text> per line, indent via literal "├── " / "│   └── " prefixes -->
</svg>
```

## N-node circular/diamond loop (ReAct-style cycle)

The animated-dot loop used for the agent cycle (module 01) and the DDD
read/plan/implement/update cycle (module 06). Works for 3 nodes (triangle
path) or 4 (diamond path, shown here) — just change the node count,
positions, and the `path=` in `animateMotion`.

```svg
<div class="svg-scene small">
  <svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
    <style>
      .loop-path{fill:none;stroke:var(--border);stroke-width:2;stroke-dasharray:4 6;}
      .node{fill:var(--bg-2);stroke-width:3;}
      .n1{stroke:var(--accent);} .n2{stroke:var(--accent-3);}
      .n3{stroke:var(--accent-2);} .n4{stroke:var(--accent);}
      .nl{font:700 10px var(--font,sans-serif);fill:var(--fg);text-anchor:middle;}
      .dot{fill:var(--accent-2);}
    </style>
    <rect class="loop-path" x="40" y="40" width="160" height="160" rx="20"/>
    <circle class="node n1" cx="120" cy="40" r="26"/><text class="nl" x="120" y="44">Шаг 1</text>
    <circle class="node n2" cx="200" cy="120" r="26"/><text class="nl" x="200" y="124">Шаг 2</text>
    <circle class="node n3" cx="120" cy="200" r="26"/><text class="nl" x="120" y="204">Шаг 3</text>
    <circle class="node n4" cx="40" cy="120" r="26"/><text class="nl" x="40" y="124">Шаг 4</text>
    <circle class="dot" r="6">
      <animateMotion dur="5s" repeatCount="indefinite" path="M120,40 L200,120 L120,200 L40,120 Z"/>
    </circle>
  </svg>
</div>
```

For 3 nodes, use a circular `<circle class="loop-path" .../>` instead of
the diamond `<rect>`, position nodes at three points on that circle, and
set `animateMotion`'s `path` to an arc (`A r,r 0 1,1 ...`) — see module
01's "Базовый цикл" slide for the exact triangle-on-a-circle version.

**Reminder:** an inline `<style>` block inside an SVG is document-scoped,
not SVG-scoped (see the Gotchas section of `SKILL.md`). If a slide
already has another SVG with a `<style>` block using short class names
like `.node`/`.lbl`, rename this loop's classes (as done above with
`n1`–`n4`) so they don't collide within the same file.
