# CLIPFORGE — Onboarding Screen Copy

> **Deliverable:** First 3 onboarding screens (first-run experience)
> **Tone:** Precise. Premium. Effortless. — confident, direct, a touch of personality
> **Design context:** Dark theme (Midnight Navy #0D0F1C), Electric Teal #00D9C0 accents, Hot Magenta #FF3D7F CTAs
> **Visual language:** Before → After slider as the signature interaction; 4-point spark at the transformation point

---

## Design Notes

Each screen follows the same structure:
- **Visual zone** (top 60%): animated demo showing the feature in action
- **Headline** (Space Grotesk 700, 28-32px): the core promise
- **Body** (Inter 400, 15-16px): one sentence expanding the promise
- **CTA button** (Hot Magenta #FF3D7F, 12px radius): advance to next screen

**Copy principles:**
- Headlines lead with the verb and the result — not the feature
- Body text is one sentence, max two
- No jargon, no technical terms — users don't care about "neural engine" or "inpainting"
- The word "magic" appears once (Screen 2), not repeated — keeps it earned, not gimmicky
- Privacy is a Screen 3 closer, not Screen 1 — we earn trust by showing value first

---

## Screen 1 — The Hook: Background Removal

**Visual:** Before → After slider. A portrait photo with a messy background slides to reveal a clean, transparent cutout. Spark animation at the transition point.

**Headline:**
Remove any background. In one tap.

**Body:**
Our AI cuts out your subject in under a second — hair, fur, fine edges, all perfect. No upload, no watermark.

**CTA button:**
Try it free

**Microcopy (skip link, bottom-left):**
Skip

---

## Screen 2 — The Retention Driver: Object Eraser

**Visual:** A photo with an unwanted object (e.g., a person photobombing a sunset). A finger brushes over the object → it vanishes, filled in seamlessly. Before → After slider.

**Headline:**
Erase anything. Like it was never there.

**Body:**
Brush over unwanted objects, people, or blemishes. The AI fills the gap — seamlessly, instantly.

**CTA button:**
See the magic

**Microcopy (skip link, bottom-left):**
Skip

---

## Screen 3 — The Closer: Privacy + Export + Start

**Visual:** Three quick icons animate in sequence: (1) a lock with a teal glow, (2) a transparent PNG badge, (3) a "5 free edits today" badge in Amber Glow #FFB84D. Then a clean cutout appears with export format options.

**Headline:**
Your photos. Your device. Always private.

**Body:**
Everything happens on your phone — no uploads, no servers, no tracking. Export as transparent PNG, swap backgrounds, and share anywhere. Five edits free, every day.

**CTA button:**
Get started

**Microcopy (below CTA, Text Secondary #8B8FA3):**
No signup required · No watermark · Works offline

---

## Character Counts

| Screen | Headline | Body | CTA |
|--------|----------|------|-----|
| 1 | 38 chars | 94 chars | 11 chars |
| 2 | 42 chars | 81 chars | 13 chars |
| 3 | 46 chars | 156 chars | 12 chars |

All headlines fit within mobile display width at 28-32px Space Grotesk 700.
All bodies fit within 3 lines at 15-16px Inter 400 on standard phone widths.

---

## Localization Notes

The onboarding copy should be localized for the same 5 languages as the store listings (EN, ES, RU, PT, DE). Key translation considerations:

- **"One tap"** → ES: "un toque" / RU: "один тап" / PT: "um toque" / DE: "ein Tipp"
- **"Watermark"** → ES: "marca de agua" / RU: "водяной знак" / PT: "marca d'água" / DE: "Wasserzeichen"
- **"Magic"** (Screen 2 CTA) → Keep culturally appropriate; ES: "mágico" / RU: "магия" / PT: "mágico" / DE: "Magie"
- **"No signup required"** → ES: "sin registro" / RU: "без регистрации" / PT: "sem cadastro" / DE: "ohne Registrierung"

Localized onboarding strings should be generated once the UI is wired and exact pixel constraints are known (SwiftUI `.lineLimit` settings may require trimming body text in German, which runs ~30% longer).

---

*CLIPFORGE — AI Background Remover & Object Eraser | Sprint 3 Copywriter | FACT-25 | 2026-07-05*
