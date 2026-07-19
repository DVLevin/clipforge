# CLIPFORGE — Sprint 1: Product Specification

> **App idea:** AI Background Remover + Object Eraser (iOS-first)
> **Sprint:** 1 (Product Spec)
> **Persona:** Strategist (Pieter Levels + Tony Dinh + Tabunov DNA)
> **Date:** July 5, 2026
> **Status:** DRAFT — awaiting Dima review

---

## Executive Summary

**The bottom line:** Build a *zero-server-cost*, on-device AI photo editor that removes backgrounds and erases objects in under 1 second — with no upload, no watermark, no waiting. The unit economics are absurd (cost = $0 per use), the market is proven ($3M/month for Photoroom alone), and the competitive wedge is simple: everyone else runs on servers and pays per image. We don't.

**Confidence: High (>80%)** on tech feasibility and market demand. Medium (60%) on hitting conversion targets as a new unknown brand in a 240+ app category.

---

## 1. The ONE Core Feature — The Magic Moment

### The Magic Moment

> **User opens a photo → taps "Remove Background" → the background is GONE in under 1 second. Hair, fur, mesh — perfect. No upload bar. No spinner. No watermark. Done.**

Then the second beat:

> **They notice a stranger in the background. They brush over the person with their finger → the person vanishes, filled in seamlessly. Still on-device. Still instant.**

### Why This Is the "Holy Shit" Moment

Three things compound into the reaction:

| Factor | Competitors (remove.bg, Photoroom, Erase.bg) | CLIPFORGE |
|--------|----------------------------------------------|-----------|
| **Speed** | 2–10 seconds (upload → process → download) | **<1 second** (on-device Neural Engine) |
| **Watermark** | Free tier adds watermark or downgrades quality | **No watermark, ever** |
| **Privacy** | Photos uploaded to unknown servers | **Never leaves the phone** |
| **Cost ceiling** | Per-image credits or server-bounded subscriptions | **$0 unit cost → unlimited use** |

The "holy shit" isn't any single feature — it's the **speed × quality × no-watermark combo**. Users have been trained to accept: upload → wait → get a watermarked preview → pay to remove watermark. We break that entire pattern.

### Core Feature Definition (MVP)

**Background Removal** is the hook. **Object Erasure** is the retention driver.

- **Feature 1 (Hook):** One-tap background removal. U2Net model running on Apple Neural Engine via CoreML. Output: transparent PNG or solid-color replacement.
- **Feature 2 (Retention):** Brush-to-erase object removal. LaMa inpainting model via CoreML. User paints over unwanted objects/people → AI fills the gap.
- **Feature 3 (Delight):** One-tap background swap. After removal, user picks from preset backgrounds (solid colors, gradients, studio scenes) or their own photo.

**What we explicitly DON'T build in v1:**
- ❌ Batch processing (add in v2 if requested)
- ❌ Video background removal (complex, add later)
- ❌ AI-generated backgrounds via text prompts (server cost, add later)
- ❌ Social sharing / community features (distraction)
- ❌ Account/login system (not needed for on-device app)

---

## 2. Tech Stack Decision

### Recommendation: 100% On-Device (Self-Hosted Models via CoreML)

**This is the single most important decision in this spec, and the answer is clear.**

### Why On-Device Wins

| Dimension | On-Device (CoreML) | Server-Side (rembg/Replicate API) |
|-----------|-------------------|-----------------------------------|
| **Unit cost** | **$0** | $0.01–0.05/image (Replicate) or $50–365/mo GPU |
| **Speed** | <1 second (Neural Engine) | 2–10 seconds (network round-trip) |
| **Privacy** | Photos never leave phone | Uploaded to server |
| **Scalability** | Infinite (user's phone does the work) | Linear cost scaling with users |
| **Offline** | ✅ Works without internet | ❌ Requires connection |
| **Privacy compliance** | Trivial (GDPR, CCPA, App Store privacy) | Complex (data handling disclosures) |
| **Server maintenance** | None | Ongoing DevOps burden |

### The Models

**Background Removal — U2Net**
- Origin: rembg's default model (same quality as remove.bg)
- Size: ~40MB (quantized for mobile)
- CoreML conversion: proven path (rockyshikoku's U2Net→CoreML guide)
- Performance: <0.5s inference on A14+ chips via Neural Engine
- Accuracy: handles hair, fur, mesh, transparent objects — production-grade

**Object Erasure — LaMa (Large Mask Inpainting)**
- Origin: Samsung AI's resolution-robust inpainting model
- Size: ~200MB (lazy-loaded only when user accesses eraser)
- CoreML conversion: proven path (CoreMLaMa, LaMa-Eraser-iOS)
- Performance: 1–3s per erase on A14+ depending on image size
- Quality: state-of-the-art for object removal, handles large masks

### Full Tech Stack

```
┌─────────────────────────────────────────────────┐
│                  CLIPFORGE iOS App               │
│                                                  │
│  ┌─────────────┐  ┌──────────┐  ┌────────────┐ │
│  │  SwiftUI UI │  │  CoreML  │  │ Vision FW  │ │
│  │  (interface)│  │ (models) │  │ (preproc)  │ │
│  └─────────────┘  └──────────┘  └────────────┘ │
│                                                  │
│  Models (bundled in app):                        │
│  ├── u2net_seg.mlmodelc    (~40MB, always loaded)│
│  └── lama_inpaint.mlmodelc (~200MB, lazy-loaded) │
│                                                  │
│  ┌─────────────────────────────────────────────┐│
│  │            RevenueCat (subscriptions)        ││
│  └─────────────────────────────────────────────┘│
│                                                  │
│  No backend server. No database. No API.        │
│  The app IS the backend.                        │
└─────────────────────────────────────────────────┘
```

**Stack summary:**
- **Language:** Swift / SwiftUI
- **ML:** CoreML + Vision framework (Apple Neural Engine)
- **Models:** U2Net (segmentation) + LaMa (inpainting), both pre-converted to `.mlmodelc`
- **Payments:** RevenueCat (manages StoreKit subscriptions + paywall analytics)
- **Analytics:** RevenueCat SDK + Apple Analytics (no third-party tracking needed)
- **Minimum iOS:** 16.0 (covers 95%+ of active devices, Neural Engine on A12+)
- **Backend:** None. Zero. The app is fully self-contained.

### Cost-Per-Use Estimate

| Cost Item | Per-Use Cost | Monthly Fixed |
|-----------|-------------|---------------|
| Compute | **$0.00** (user's Neural Engine) | $0 |
| Storage | **$0.00** (on-device only) | $0 |
| Bandwidth | **$0.00** (no uploads) | $0 |
| Apple Developer Program | — | $99/year |
| RevenueCat | Free under $10K MTR | $0 (until scale) |
| **Total unit cost** | **$0.00** | **$8.25/mo** |

**The only per-use cost is Apple's 30% App Store commission on revenue** — not on cost. We keep 70% of every dollar, with zero marginal cost per image processed. This is structurally impossible for server-based competitors to match.

---

## 3. Monetization Specifics

### Pricing Strategy: Weekly Subscription (Primary) + Pay-Per-Pack (A/B Test)

**Decision:** Lead with a **weekly subscription at $3.99/week** — undercutting the $4.99 industry standard while staying above the $2.99 floor where perceived value drops.

### Free Tier

| Limit | Value | Rationale |
|-------|-------|-----------|
| **3 background removals** | Enough to experience the magic, not enough to be useful long-term | Industry standard is 1–3 free uses. 3 lets users try on different photo types (portrait, product, complex) |
| **1 object erase** | One taste of the eraser | Hook for the secondary feature |
| **No watermark** | Key differentiator | Competitors watermark free output; we don't — this is the "holy shit, this is better than [competitor]" trigger |
| **Full quality export** | No resolution downgrade | We have zero server cost — no reason to cripple free tier |

After free limit → **soft paywall** with 3-day free trial of weekly plan.

### Price Points

| Plan | Price | Positioning |
|------|-------|-------------|
| **Weekly** (primary) | **$3.99/week** | 3-day free trial → auto-renew. Undercuts $4.99 competitors. Weekly cadence = higher LTV than monthly for utility apps |
| **Monthly** (alternative) | $9.99/month | For users who hate weekly subs. ~$2.50/week equivalent |
| **Yearly** (anchor) | $39.99/year | "Best value" anchor. Makes weekly look cheap. ~$0.77/week |
| **Lifetime** (v1.1) | $29.99 one-time | Add after validating sub conversion. Some users hate subs |

**A/B test in Sprint 3:** Pay-per-pack model ($4.99 for 50 removals + 20 erases) vs. weekly sub. Test which converts better for this audience. Pack model may win for low-frequency users who only need it occasionally.

### Revenue Projection — At 1,000 Downloads

This is the **floor scenario**, not the ceiling. New apps with no brand recognition typically convert 2–4% of downloads to paid in the utility category.

| Metric | Conservative (2%) | Base (3%) | Optimistic (5%) |
|--------|-------------------|-----------|-----------------|
| Paying users | 20 | 30 | 50 |
| Weekly sub price | $3.99 | $3.99 | $3.99 |
| Gross weekly revenue | $79.80 | $119.70 | $199.50 |
| Gross monthly revenue (4.3 wks) | **$343** | **$515** | **$858** |
| Apple's 30% cut | -$103 | -$154 | -$257 |
| **Net monthly revenue** | **$240** | **$360** | **$600** |

**Reality check:** 1,000 downloads is tiny. Photoroom does 800K downloads/month. The question isn't "can we make money at 1K downloads" — it's "can we get to 10K, 50K, 100K downloads." At 50K downloads with 3% conversion:

→ 1,500 paying users × $3.99/week = **~$25,700/month gross** → **~$18,000/month net**

### Unit Economics Summary

| Metric | Value |
|--------|-------|
| Revenue per paying user/week | $3.99 |
| Apple's cut (30%) | $1.20 |
| Net revenue per user/week | $2.79 |
| Marginal cost per use | $0.00 |
| **Gross margin** | **100%** (after Apple's cut) |
| CAC target (organic-first) | < $1.00 |
| Break-even users (at $8.25/mo fixed cost) | **3 paying users** |

Yes — the break-even point is 3 paying users. That's the power of zero server costs.

---

## 4. ASO Keyword Strategy (5 Languages)

### Strategy

**Primary keyword:** "background remover" (EN) and equivalents — this is the highest-intent, highest-volume search term in the category. Every top app ranks for it.

**Secondary keywords:** "remove background," "erase background," "object remover," "magic eraser"

**Long-tail wedge:** "remove background no watermark," "background remover offline," "erase objects photo"

### Keyword Matrix

| Intent | English | Spanish | Russian | Portuguese | German |
|--------|---------|---------|---------|------------|--------|
| **Primary** (highest volume) | background remover | eliminar fondo | удалить фон | removedor de fundo | hintergrund entfernen |
| **Action variant** | remove background | quitar fondo | убрать фон | remover fundo | hintergrund löschen |
| **Object eraser** | object remover | borrar objetos | удалить объекты | remover objetos | objekte entfernen |
| **Magic eraser** | magic eraser | borrador mágico | ластик магия | borrador mágico | radiergummi magisch |
| **Transparent** | transparent background | fondo transparente | прозрачный фон | fundo transparente | transparenter hintergrund |
| **Photo editor** (broad) | photo editor | editor de fotos | фоторедактор | editor de fotos | foto editor |
| **Cut out** | cut out photo | recortar foto | вырезать фото | recortar foto | ausschneiden foto |
| **PNG export** | png maker | creador png | создать png | criador png | png erstellen |
| **Product photo** | product photo | foto de producto | фото товара | foto de produto | produktfoto |
| **Offline** (wedge) | offline bg remover | sin internet fondo | без интернета фон | offline removedor | offline hintergrund |

### App Name Keyword Allocation (30 char limit)

The App Store name is the #1 ASO signal. We front-load the primary keyword:

| Language | App Name (Subtitle) |
|----------|-------------------|
| EN | CLIPFORGE — BG Remover & Eraser |
| ES | CLIPFORGE — Quitar Fondo y Borrar |
| RU | CLIPFORGE — Удалить Фон Фото |
| PT | CLIPFORGE — Remover Fundo Foto |
| DE | CLIPFORGE — Hintergrund Entfernen |

### Subtitle (30 char limit) — Secondary Keywords

| Language | Subtitle |
|----------|---------|
| EN | Remove BG, Erase Objects, PNG |
| ES | Eliminar Fondo, Borrar, PNG |
| RU | Убрать Фон, Ластик, PNG |
| PT | Remover Fundo, Apagar, PNG |
| DE | Hintergrund Löschen, PNG |

### Keyword Field (100 char limit, comma-separated)

| Language | Keywords |
|----------|---------|
| EN | remover,background,cut,erase,transparent,png,magic,object,photo,editor,stamp,watermark,crop,isolate |
| ES | eliminar,fondo,quitar,borrar,recortar,transparente,png,magico,objeto,foto,editor,sello,marca |
| RU | удалить,фон,убрать,вырезать,ластик,прозрачный,png,магия,объект,фото,редактор,вырезать |
| PT | remover,fundo,apagar,recortar,transparente,png,magico,objeto,foto,editor,carimbo,marca |
| DE | entfernen,hintergrund,löschen,ausschneiden,transparent,png,magisch,objekt,foto,bearbeiten |

---

## 5. Brand Name + Tagline (3 Options)

### Naming Criteria
- Short (1–2 words, ≤10 letters)
- Brandable (not generic like "BG Remover Pro")
- Includes or evokes the core keyword
- Available as .com domain (checkable)
- No trademark conflicts (quick USPTO check needed)

---

### Option A: CLIPFORGE (Recommended)

**Tagline:** *Remove anything. Keep everything.*

| Criterion | Assessment |
|-----------|-----------|
| Meaning | "Clip" = cut out/extract. "Forge" = craft/create. Together: forge your images by clipping what you don't need |
| Brandability | Strong — sounds like a creative tool, not a utility |
| Keyword signal | "Clip" evokes "cut out" / "clip art" — related to image editing |
| Memorability | High — two sharp consonant sounds, easy to say |
| Domain | `clipforge.app` likely available; `clipforge.com` may be taken |
| Risk | "Forge" is a common suffix (many startups use it) |

**ASO name variant:** `CLIPFORGE — BG Remover & Eraser`

---

### Option B: SNIPIT

**Tagline:** *Your background, gone in a snap.*

| Criterion | Assessment |
|-----------|-----------|
| Meaning | "Snip" = cut. Playful, action-oriented |
| Brandability | Medium — fun, but "SnipIt" sounds like a screenshot tool |
| Keyword signal | "Snip" relates to cutting/editing |
| Memorability | High — short, punchy |
| Domain | `snipit.app` likely available |
| Risk | Possible confusion with screenshot/snipping tools. Trademark risk (many "SnipIt" variants exist) |

**ASO name variant:** `SNIPIT — Background Remover`

---

### Option C: VANISH

**Tagline:** *Make backgrounds and objects disappear.*

| Criterion | Assessment |
|-----------|-----------|
| Meaning | Directly describes what the app does — things vanish |
| Brandability | Strong — single powerful word, emotional |
| Keyword signal | Indirect — doesn't contain "background" or "remove" |
| Memorability | Very high — one word, dramatic |
| Domain | `vanish.app` or `getvanish.app`; `vanish.com` definitely taken |
| Risk | "Vanish" is a cleaning product brand in many countries (stain remover). Trademark conflict likely in EU |

**ASO name variant:** `VANISH — Remove Background & Objects`

---

### Recommendation

**CLIPFORGE** is the strongest play:
1. Clean trademark profile (unlike VANISH)
2. No category confusion (unlike SNIPIT)
3. Sounds professional enough for the e-commerce/product-photo use case
4. "Forge" implies craftsmanship — positions above cheap utility apps
5. The codename is already CLIPFORGE — keep it, ship it

---

## Competitive Landscape (Context)

| Competitor | Model | Price | Downloads/mo | Revenue/mo | Key Weakness |
|-----------|-------|-------|-------------|-----------|--------------|
| **Photoroom** | Server-based, full editor | $5.99–$249/mo | 800K | **$3M** | Heavy app, needs internet, expensive |
| **remove.bg** | Server-based API | Credit-based | N/A (web) | High | Per-image cost, web-first |
| **Erase.bg** | Server-based | Free + ads | High | Ad revenue | Watermarks, quality varies |
| **Magic Eraser** (various) | Mixed | $4.99/week | Medium | Medium | Often low quality, aggressive ads |
| **Background Eraser** | Mixed | Free + IAP | High | Medium | Clunky UX, manual tools |

**Our wedge:** On-device speed + no watermark + zero server cost = we can undercut on price AND deliver a better experience. We don't need to win on features — we win on the core experience being fundamentally faster and cheaper.

---

## Sprint 2 Handoff Notes

**What Sprint 2 (Validator) should stress-test:**
1. Is on-device U2Net quality truly competitive with server-side remove.bg? (Need side-by-side test on 20 hard images — hair, fur, mesh, transparent)
2. Will LaMa inpainting fit in an app bundle without bloating past 200MB App Store cellular download limit? (The 200MB LaMa model may need to be downloaded on first use)
3. Is $3.99/week the right price, or does $2.99 convert better for an unknown brand? (A/B test needed)
4. Can we rank for "background remover" against 240+ apps with years of reviews and ratings? (ASO is a long game — need a review-generation strategy from day 1)
5. Android port: when? (CoreML is iOS-only. Android would need TensorFlow Lite / ONNX runtime. Defer to post-iOS validation)

---

## Decision Log

| # | Decision | Rationale | Confidence |
|---|----------|-----------|------------|
| 1 | On-device only (no server) | $0 unit cost, instant speed, privacy advantage, no DevOps | High (90%) |
| 2 | U2Net + LaMa via CoreML | Proven conversion paths, production-quality output, Neural Engine optimized | High (85%) |
| 3 | Weekly sub $3.99 as primary | Undercuts $4.99 standard, above $2.99 value floor, weekly cadence = higher LTV | Medium (70%) |
| 4 | No watermark on free tier | Key differentiator — we can afford it ($0 cost), competitors can't | High (85%) |
| 5 | 3 free removals + 1 free erase | Enough to hook, not enough to satisfy | Medium (65%) |
| 6 | CLIPFORGE as brand name | Clean IP, brandable, professional positioning | High (80%) |
| 7 | iOS-first, Android deferred | CoreML advantage is iOS-only; validate before porting | High (85%) |

---

*Authored by: Strategist persona (Pieter Levels + Tony Dinh + Tabunov DNA)*
*Market data sources: Sensor Tower (Photoroom $3M/mo, 800K downloads), App Store listings (competitor pricing), rembg/LaMa CoreML conversion guides*
*Sprint 0 market analysis (FACT-19) was not yet available at time of writing — this spec is grounded in independent market research.*
