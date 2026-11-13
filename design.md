# Design — rechnify.at

/* anchor: Stripe-data / Linear-dense, diverge: Austrian & German legal calculator workbench */
Locked design system for rechnify.at. Combines product-ui-design (Floor/Ceiling restraint), genjutsu (native 60fps motion & micro-interactions), no-slop-ui (banned AI-tells), and hallmark (OKLCH precision tokens).

## Genre & Archetype
- **Genre:** modern-minimal / utility-first
- **Floor (Tool Pages):** Workbench — high-density input/output split, 1px crisp borders, `tabular-nums` for all financial figures.
- **Ceiling (Index / Hero):** Clean Bento Grid — solid app-bar header, clear typographic hierarchy, zero fuzzy radial halos.

## AI-Tells Explicitly Banned
- ❌ No floating detached pill-nav with heavy blur on homepage (use anchored crisp app-bar).
- ❌ No radial gradient color halos / glowing auras on `body`.
- ❌ No card hover translations (`translateY(-4px)` is banned on cards; hover is 1px border/highlight only).
- ❌ No decorative mono eyebrow tags or badge clusters without functional data.
- ❌ No generic 4-cell metric stat strips.
- ❌ No celebratory confetti or toast popups on calculate (Silent Success).

## Theme (OKLCH)
- `--color-paper`   oklch(98.5% 0.005 240)
- `--color-paper-2` oklch(96%   0.008 240)
- `--color-paper-3` oklch(92%   0.012 240)
- `--color-ink`     oklch(15%   0.040 255)
- `--color-ink-2`   oklch(38%   0.025 255)
- `--color-ink-3`   oklch(58%   0.018 255)
- `--color-rule`    oklch(88%   0.012 240)
- `--color-rule-2`  oklch(80%   0.014 240)
- `--color-accent`  oklch(48%   0.220 255)
- `--color-focus`   oklch(48%   0.220 255)

## Typography & Numbers
- Display: Space Grotesk, weight 600–700
- Body: system-ui, -apple-system, 'Segoe UI', Roboto, Inter, sans-serif
- Figures: `font-variant-numeric: tabular-nums lining-nums` for all currencies, percentages, and inputs.
- Scale: `--text-xs` (0.75rem) to `--text-display` (clamp(2.5rem, 5vw + 1rem, 4.5rem)).

## Genjutsu Motion & Micro-interactions
- Interaction Thesis: Every transition communicates state change or hierarchy.
- Durations: `--dur-micro` (120ms), `--dur-short` (180ms).
- Easings: `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`.
- Calculation Update: `@keyframes value-pulse` (120ms subtle contrast pulse on updated figures).
- Focus Ring: 2px solid `var(--color-focus)`, 1px offset, 0px blur.
- Reduced Motion: Respect `@media (prefers-reduced-motion: reduce)` — instant switch, no transitions.

## What pages MUST share
- Consistent solid/subtle-glass sticky header (anchored, not floating).
- Space Grotesk headline + clean sans body.
- Cobalt accent ≤ 5% of viewport.
- 1px crisp rule borders, 8px input radius, 10px card radius.
- Tabular alignment on all calculated outputs.
- Breadcrumb on tool/content pages only

## Exports

### tokens.css
See `/tokens.css` at project root — source of truth.

### Tailwind v4 `@theme`
```css
@theme {
  --color-paper:   oklch(98.5% 0.005 240);
  --color-ink:     oklch(15% 0.040 255);
  --color-accent:  oklch(48% 0.220 255);
  --font-display:  "Space Grotesk", sans-serif;
  --font-body:     "Inter", sans-serif;
  --spacing-md:    1.5rem;
  --text-md:       1.125rem;
  --ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
}
```

### DTCG `tokens.json`
```json
{
  "color": {
    "paper":  { "$value": "oklch(98.5% 0.005 240)", "$type": "color" },
    "ink":    { "$value": "oklch(15% 0.040 255)", "$type": "color" },
    "accent": { "$value": "oklch(48% 0.220 255)", "$type": "color" }
  },
  "font": {
    "display": { "$value": "Space Grotesk", "$type": "fontFamily" },
    "body":    { "$value": "Inter", "$type": "fontFamily" }
  },
  "space": {
    "md": { "$value": "1.5rem", "$type": "dimension" }
  }
}
```

### shadcn/ui CSS variables
```css
:root {
  --background:         98.5% 0.005 240;
  --foreground:         15% 0.040 255;
  --primary:            48% 0.220 255;
  --primary-foreground: 100% 0 0;
  --muted:              88% 0.012 240;
  --muted-foreground:   52% 0.020 255;
  --border:             88% 0.012 240;
  --input:              98.5% 0.005 240;
  --ring:               48% 0.220 255;
  --radius:             14px;
}
```
