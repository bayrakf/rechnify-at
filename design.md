# Design — rechnify.at

Locked design system for rechnify.at. Every page reads this file before emitting code.

## Genre
modern-minimal

## Macrostructure family
- **Marketing pages:** Bento Grid — category bento tiles, marquee hero, value strip
- **Tool pages:** Workbench — centered calculator card, result panel below inputs, FAQ accordion
- **Content pages:** Long Document — single reading column, breadcrumb, minimal chrome

## Theme
- `--color-paper`   oklch(98.5% 0.005 240)
- `--color-paper-2` oklch(95% 0.010 240)
- `--color-ink`     oklch(15% 0.040 255)
- `--color-ink-2`   oklch(40% 0.028 255)
- `--color-rule`    oklch(88% 0.012 240)
- `--color-accent`  oklch(48% 0.220 255)
- `--color-focus`   oklch(48% 0.220 255)

## Typography
- Display: Space Grotesk, weight 600–700, style normal
- Body: Inter, weight 400–500
- Display tracking: -0.02em on large headlines
- Type scale anchor: `--text-display` = clamp(3rem, 7vw + 1rem, 6rem)

## Spacing
4-point named scale in `tokens.css`. Use `var(--space-md)` etc., never raw px in new code.

## Motion
- Easings: `--ease-out`, `--ease-in`, `--ease-in-out`
- Reveal: fade + 8px translate on hero only; tool pages static
- Reduced-motion: opacity-only, ≤ 150ms

## Microinteractions stance
- Silent success — no celebratory toasts on calculate
- Hover delay 800ms on tooltips · focus delay 0ms
- Buttons: transform translateY on hover, instant focus ring

## CTA voice
- Primary: filled cobalt pill/rounded, white ink, verb-first ("Berechnen", "Jetzt berechnen")
- Secondary: outline cobalt, same radius

## Per-page allowances
- Marketing (`index.html`): enrichment none — typography + bento grid
- Tool pages: no enrichment — calculator IS the page
- Content (Über uns, Kontakt, Impressum, Datenschutz): typography only

## What pages MUST share
- Space Grotesk + Inter pairing
- Cobalt accent ≤ 5% per viewport
- Glass sticky header on tool/content pages
- Pill nav on homepage
- CTA shape (14px radius, 11px×18px padding rhythm)
- Dark mode via `body.dark`

## What pages MAY differ on
- Macrostructure within family (Bento vs Workbench vs Long Document)
- Footer density (statement on index · compact grid on tools)
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
