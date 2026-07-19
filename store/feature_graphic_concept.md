# CLIPFORGE — Feature Graphic Concept (1024 x 500)

> **Sprint 3 Designer Deliverable** — Feature graphic concept for Google Play Store.

---

## What It Is

The feature graphic is the **banner image** at the top of the Play Store listing (1024 x 500 px). It's the first thing users see. It has ONE job: make them tap "Install."

---

## Concept: "The Transformation"

**Layout: Split-screen before/after with brand overlay**

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   CLIPFORGE                          ┌─────────────────┐ │
│   ══════════                         │   BEFORE        │ │
│                                      │  ┌───────────┐  │ │
│   Remove any background.             │  │ busy photo│  │ │
│   Erase any object.                  │  │ (person + │  │ │
│   One tap.                           │  │ clutter)  │  │ │
│                                      │  └───────────┘  │ │
│   ✦  AI-POWERED                      │      →→→       │ │
│                                      │   AFTER        │ │
│                                      │  ┌───────────┐  │ │
│                                      │  │ █ clean   │  │ │
│                                      │  │ █ cutout  │  │ │
│                                      │  │ █ on chk. │  │ │
│                                      │  │ █ bg      │  │ │
│                                      │  └───────────┘  │ │
│                                      └─────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
          1024 x 500 px — Midnight Navy background
```

---

## Detailed Composition

### Background
- Full-bleed **Midnight Navy** (`#0D0F1C`)
- Subtle radial gradient: slightly lighter (`#1A1D2E`) radiating from center-left, darker at edges
- Optional: very faint transparency checkerboard pattern at 3% opacity across entire bg

### Left Side (~45% width): Brand + Messaging
- **Logo/wordmark:** "CLIPFORGE" in Space Grotesk Bold, 64px, Off-White (`#F0F2F5`)
- **Underline:** Electric Teal (`#00D9C0`) accent line beneath the wordmark, 4px thick, 120px wide
- **Tagline (3 lines):**
  - "Remove any background." — Inter SemiBold, 22px, Off-White
  - "Erase any object." — Inter SemiBold, 22px, Off-White
  - "One tap." — Inter SemiBold, 22px, **Hot Magenta** (`#FF3D7F`) ← emphasis
- **AI badge:** Small pill below tagline — "✦ AI-POWERED" in JetBrains Mono, 14px, Electric Teal text on Elevated Slate (`#1A1D2E`) pill bg, 8px radius

### Right Side (~50% width): Before/After Demo
- **Container:** Rounded card (16px radius), Elevated Slate (`#1A1D2E`) background, subtle teal-tinted shadow
- **Before panel (top):** A real photo of a person/product against a busy/cluttered background, slightly dimmed
  - Label: "BEFORE" — Space Grotesk Bold, 12px, uppercase, letter-spaced, Slate Gray (`#8B8FA3`)
- **Arrow:** Vertical down-arrow in Electric Teal, 24px, centered between panels
- **After panel (bottom):** Same subject as a clean cutout on a transparency checkerboard pattern, full color, with a subtle Electric Teal glow around the edges
  - Label: "AFTER" — Space Grotesk Bold, 12px, uppercase, Electric Teal (`#00D9C0`)
- **Spark mark:** Small 4-point Electric Teal star at the cutout's edge (top-right)

### Bottom Strip (optional, ~5% height)
- Thin Electric Teal accent line at the very bottom
- Small text: "Free to try · No signup needed" — Inter Regular, 12px, Slate Gray, centered

---

## Execution Instructions

### For AI Image Generation

```
Feature graphic for Google Play Store, 1024x500 pixels, landscape orientation.
Dark midnight navy background with subtle radial gradient.
Left side: the word "CLIPFORGE" in bold modern sans-serif white text, with a teal 
underline. Below it, three short lines of white text with the third line in hot pink.
A small pill badge saying "AI-POWERED" in teal monospace text.
Right side: a before/after comparison card showing a photo of a person against a 
messy background (before), then the same person as a clean cutout on a transparency 
checkerboard pattern (after), with a teal down-arrow between them.
Style: premium dark mode, electric teal (#00D9C0) and hot magenta (#FF3D7F) accents, 
minimal, professional photo editing tool aesthetic. No Google Play badges.
```

### For a Human Designer

1. **Canvas:** 1024 x 500 px, 72 DPI minimum (higher is fine)
2. **Safe area:** Keep all text within 924 x 400 (50px margins) — Play Store crops edges on some devices
3. **Before/after photos:** Use stock photos or AI-generated images showing a clear subject (person, product, or pet) against a busy background
4. **After treatment:** Remove the background (use remove.bg or the app itself!), place on checkerboard, add teal glow
5. **Export:** JPEG (high quality, <1MB) or PNG — Play Store accepts both

### Important: Do NOT Include
- ❌ Google Play "Get it on" badges (Google provides these automatically)
- ❌ App screenshots (those are separate assets)
- ❌ Too much text (keep it to wordmark + 3-line tagline + badge)
- ❌ Competitor names or comparison claims

---

## Alternative Concept: "Minimal Mark"

If the split-screen feels too busy at 1024x500:

- Center the CLIPFORGE wordmark + icon large and bold
- Below: single tagline "AI Background Remover & Object Eraser"
- Background: Midnight Navy with a large, faint transparency checkerboard pattern filling the whole canvas
- One Electric Teal spark in the top-right corner

**Pros:** Cleaner, more premium feel. **Cons:** Less persuasive (no proof of the transformation).

**Recommendation:** Use the split-screen "Transformation" concept. Proof > polish for conversion.

---

*Created by Designer agent — Sprint 3, FACT-22 — 2026-07-05*
