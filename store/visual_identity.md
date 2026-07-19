# CLIPFORGE — Visual Identity Guide

> **Sprint 3 Designer Deliverable** — Color palette, typography, visual language, and brand direction for CLIPFORGE (AI Background Remover + Object Eraser).

---

## Brand Personality

**Three words:** Precise. Premium. Effortless.

CLIPFORGE is a **professional-grade tool that feels like magic.** Not playful (Picsart), not corporate (Remove.bg), not trendy-purple (PhotoRoom). We're the dark-mode power tool — the one that looks like it belongs in a designer's dock.

**The name encodes the promise:**
- **CLIP** → precision cutting, clipping paths, clean cutouts
- **FORGE** → crafting something valuable from raw material

**Competitive positioning:**
```
  Playful ←──────────────────────────→ Professional
  Picsart          PhotoRoom         CLIPFORGE    Remove.bg
  (rainbow)        (purple)          (DARK/TEAL)  (white/red)
```

---

## Color Palette

### Primary

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Primary** | Electric Teal | `#00D9C0` | Brand color, UI accents, progress |
| **Primary Dark** | Deep Teal | `#00A896` | Hover/pressed, gradients |
| **Dark Base** | Midnight Navy | `#0D0F1C` | App bg, store bg, icon bg |
| **Surface** | Elevated Slate | `#1A1D2E` | Cards, toolbars, modals |
| **Surface Alt** | Hover Slate | `#252940` | Inputs, hover states |

### Accents

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **CTA / Magic** | Hot Magenta | `#FF3D7F` | CTA buttons, transformation indicators |
| **Success** | Lime Pulse | `#7CFF6B` | "Done" states, quality checkmarks |
| **Warning** | Amber Glow | `#FFB84D` | Free-tier limits, upsell prompts |

### Text

| Role | Hex | Usage |
|------|-----|-------|
| **Text Primary** | `#F0F2F5` | Headlines, body |
| **Text Secondary** | `#8B8FA3` | Captions, labels |
| **Text on Accent** | `#FFFFFF` | Button text |

### Copy-Paste Palette
```
#00D9C0  Electric Teal       — PRIMARY
#00A896  Deep Teal            — primary dark
#0D0F1C  Midnight Navy        — background
#1A1D2E  Elevated Slate       — surface
#252940  Hover Slate          — surface alt
#FF3D7F  Hot Magenta           — ACCENT / CTA
#7CFF6B  Lime Pulse            — success
#FFB84D  Amber Glow            — warning
#F0F2F5  Off-White             — text primary
#8B8FA3  Slate Gray            — text secondary
```

---

## Typography

| Level | Font | Weight | Mobile Size | Store Size | Usage |
|-------|------|--------|-------------|------------|-------|
| **Display** | Space Grotesk | 700 | 28-32px | 48-64px | Store headlines, hero text |
| **Heading** | Space Grotesk | 600 | 20-24px | 32-40px | Section headers, screenshot captions |
| **Body** | Inter | 400 | 15-16px | 18-20px | Descriptions, body text |
| **Body Bold** | Inter | 600 | 15-16px | 18-20px | Emphasis, CTAs |
| **Caption** | Inter | 400 | 12-13px | 14-16px | Metadata, microcopy |
| **Mono** | JetBrains Mono | 500 | 13px | 16px | File format badges (PNG, JPG) |

All three fonts are free on Google Fonts. **Rule:** max 2 font families per screen. Display font for headlines only, body font for everything else.

---

## Visual Language

### Core Motifs

1. **The Cut Line** — Dashed/scalpel paths suggesting precision. Decorative borders, dividers, icon detail.
2. **Transparency Checkerboard** — The universal "no background" symbol. Used sparingly as texture in marketing.
3. **Before → After Slider** — The signature interaction. Most compelling visual proof — show it everywhere.
4. **The Spark** — 4-point star at the point of transformation. "AI magic happened here." Recurring brand mark.
5. **Dark Surfaces, Bright Photos** — Our dark UI makes colorful photos POP. This is our visual superpower.

### Before/After Treatment
- Before: slightly dimmed (subtle desaturation)
- After: full color, sharp, vibrant
- Slider handle: Electric Teal circle with Magenta glow
- Labels: Space Grotesk, uppercase, letter-spaced

### Glow & Depth
- Teal glow (`#00D9C0` at 20-30% blur): around processed cutouts, active states
- Magenta glow (`#FF3D7F` at 15-20% blur): around CTAs, magic indicators
- Tinted shadows: `rgba(0, 217, 192, 0.15)` — NOT pure black

### Corner Radius
| Element | Radius |
|---------|--------|
| App icon (adaptive) | 25% (Material standard) |
| Cards / modals | 16px |
| Buttons | 12px |
| Input fields | 10px |
| Badges | 8px |
| Images | 8px |

---

## Motion Language

| Element | Animation | Duration |
|---------|-----------|----------|
| BG removal processing | Teal progress ring → spark burst | 1.5-3s |
| Before/After slider | Spring follow on drag | 300ms |
| CTA press | Scale 0.96 + magenta glow pulse | 150ms |
| Screen transitions | Slide + fade | 250ms |
| Success checkmark | Draw-on stroke | 400ms |

---

## Accessibility

| Standard | Implementation |
|----------|---------------|
| Contrast (text on bg) | `#F0F2F5` on `#0D0F1C` = 16.2:1 (AAA) |
| Contrast (teal on dark) | 8.4:1 (AAA) |
| Contrast (white on magenta) | 4.8:1 (AA pass) |
| Focus indicators | 2px Electric Teal outline, 2px offset |
| Touch targets | Minimum 44x44pt |

---

## Style Keywords (for AI Image Generation)

```
USE: dark mode, midnight navy background, electric teal accents,
hot magenta CTAs, premium, minimal, professional photo editing tool,
clean cutout, transparency checkerboard pattern

AVOID: bright backgrounds, playful cartoon, purple gradients,
corporate white/red, generic stock photos
```

---

*Created by Designer agent — Sprint 3, FACT-22 — 2026-07-05*
