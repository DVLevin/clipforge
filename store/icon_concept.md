# CLIPFORGE — App Icon Concept Brief

> **Sprint 3 Designer Deliverable** — App icon concept for Google Play Store (512x512) + Android adaptive icon.
>
> **Dima:** Pick ONE concept, then generate or have a designer execute it.

---

## Design Constraints

- **Canvas:** 512 x 512 px (Play Store requirement)
- **Adaptive icon:** Must work at 48 x 48 px (smallest Android display size)
- **Safe zone:** Keep all meaningful content within inner 66% diameter (adaptive icon masking)
- **Background:** Must be opaque (no transparency in the Play Store icon)

---

## Concept A (RECOMMENDED): "The Precision Cutout"

**Visual description:**

A Midnight Navy (`#0D0F1C`) rounded-square background. Center stage: a **minimal white silhouette of a person's head and shoulders** being "lifted" or separated from the background, with a **dashed Electric Teal (`#00D9C0`) cut line** tracing its outline like a scalpel path. At the top-right of the cutout silhouette, a **small 4-point Electric Teal spark/star** — the "AI magic happened here" mark.

The silhouette sits on a subtle **transparency checkerboard pattern** (alternating `#1A1D2E` and `#252940` squares) in the lower portion, just barely visible, reinforcing "background removed."

**Why this works:**
- Instantly communicates the core function (cutting subjects out)
- The spark says "AI-powered" without words
- Dark background differentiates from every competitor (all use white/light)
- Reads clearly even at 48px because the silhouette is bold and high-contrast

**Layout (512x512):**
```
┌──────────────────────────────┐
│                              │
│         ╭─────────╮          │
│        │  ◯  head  │   ✦     │ <- spark (teal)
│        │   ▓▓▓▓▓   │         │
│        │  ▓▓▓▓▓▓▓  │         │ <- white silhouette
│         ╰─────────╯          │    with dashed teal
│        ▒▒▒▒▒▒▒▒▒▒▒          │    cut outline
│        ▒▒▒▒▒▒▒▒▒▒▒          │ <- checkerboard bg
│                              │
└──────────────────────────────┘
     Midnight Navy background
```

**Color map:**
- Background: `#0D0F1C` (Midnight Navy)
- Silhouette: `#F0F2F5` (Off-White)
- Cut line + spark: `#00D9C0` (Electric Teal)
- Checkerboard: `#1A1D2E` / `#252940`

---

## Concept B: "The Clipping Scissors"

**Visual description:**

A Midnight Navy background. Center: a **bold, stylized pair of scissors** rendered as a single continuous Electric Teal line/stroke (2-3px weight), mid-cut. The scissors are cutting through a thin white horizontal line (representing a photo/background layer). At the cut point, a small **Magenta (`#FF3D7F`) spark** where the two halves of the line separate slightly.

**Why this works:**
- Scissors = universally understood "cut" symbol
- The single-line art style is modern and premium
- Magenta spark adds energy and the "magic" element

**Trade-off vs Concept A:** More abstract — doesn't show the actual result (a cutout). Better as a brand mark, less immediately self-explanatory.

---

## Concept C: "The Transparency Reveal"

**Visual description:**

A split icon — left half shows a busy, cluttered mini-landscape (trees, sky) in muted colors. Right half shows the same scene with the subject (a tree or figure) floating on a **checkerboard transparency pattern** with a clean Electric Teal glow around the cut edge. A vertical Magenta dividing line runs down the center with a small drag-handle dot.

**Why this works:**
- Shows the actual before/after transformation
- The checkerboard immediately says "transparent background"

**Trade-off:** Too detailed for 48px. Would lose clarity at small sizes. Best as a secondary marketing asset, not the app icon.

---

## Recommendation

**Go with Concept A ("The Precision Cutout").** Reasons:

1. **Highest clarity at small sizes** — the white-on-navy silhouette is bold and readable even at 48px
2. **Self-explanatory** — anyone can tell this app removes backgrounds
3. **Most differentiated** — no competitor uses a dark icon (Remove.bg = red on white, PhotoRoom = purple gradient, Picsart = colorful)
4. **Scalable** — the silhouette + spark + checkerboard motif can extend to feature graphic, screenshots, and marketing

---

## Execution Instructions

### For AI Image Generation (DALL-E, Midjourney, etc.)

**Prompt:**
```
App icon design, 512x512, for a professional AI background remover app called CLIPFORGE.
Dark midnight navy (#0D0F1C) background. Center: a minimal, bold white silhouette 
of a person's head and shoulders being cut out from their background. A dashed 
electric teal (#00D9C0) outline traces the silhouette like a precision scalpel path. 
A small 4-point teal spark/star at the top-right of the silhouette suggesting AI magic.
Subtle dark checkerboard transparency pattern in the lower background.
Style: premium, minimal, professional, dark mode aesthetic. No text. No lettering.
Clean vector-style illustration.
```

### For a Human Designer

1. Create at 512x512 with vector tools (Figma, Illustrator, Sketch)
2. Silhouette: use a clean, universal bust/head-and-shoulders shape
3. Cut line: dashed stroke, 3px, Electric Teal, following the silhouette outline with 4px offset
4. Spark: 4-pointed star, 24px diameter, Electric Teal, top-right of silhouette
5. Checkerboard: 16x16px alternating squares at 5% opacity, bottom third only
6. Export: PNG (512x512, opaque) for Play Store + SVG source file

### Adaptive Icon Layers (for Android)

| Layer | Content | Safe Zone |
|-------|---------|-----------|
| **Background layer** | Solid `#0D0F1C` (Midnight Navy) | Full canvas |
| **Foreground layer** | Silhouette + cut line + spark | Inner 66% (centered) |

---

*Created by Designer agent — Sprint 3, FACT-22 — 2026-07-05*
