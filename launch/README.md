# CLIPFORGE - Sprint 4 Launch Package

CLIPFORGE = AI Background Remover + Object Eraser.
This folder holds the Sprint 4 (FACT-23) launch deliverables.

---

## What is DONE (Growth track - FACT-23, this issue)

| File | What | Status |
|------|------|--------|
| reddit-launch-plan.md | Subreddit tier list, 30-day post sequence, post templates, timing, anti-patterns, measurement | DONE |
| tiktok-reels-content.md | 5 video concepts (hook + visual + audio + why), production + posting cadence, measurement | DONE |
| review-collection-strategy.md | How to get first 20 five-star reviews organically (policy-safe), per-channel playbook | DONE |
| aso-checklist.md | Google Play ASO: pre-launch listing, launch week, day 7-30 optimization, 30-day paid-acquisition gate | DONE |

## What is NOT done here (Copywriter track - assign SEPARATELY)

Per the FACT-23 brief, these are a separate assignment (the issue says "Copywriter task (assign
separately)"). Placeholder stubs + briefs live in copywriter/ so a Copywriter agent can pick them up
with full context. Do NOT have Growth write these - the split was intentional.

| File | What | Owner |
|------|------|-------|
| copywriter/landing-page.md | Brief for the one-pager dark-theme mobile-first landing page HTML (deploy-ready). Stub + spec only. | Copywriter (NEW ticket) |
| copywriter/reddit-drafts.md | Brief for 3 Reddit post drafts (3 different subs). Stub + which templates to use. | Copywriter (NEW ticket) |
| copywriter/about-press-copy.md | Brief for "About" / press copy. Stub. | Copywriter (NEW ticket) |

---

## How the deliverables connect

```
reddit-launch-plan.md  ─templates─>  copywriter/reddit-drafts.md  (copywriter fills the [BRACKETS])
         │
         └─beta cohort feeds─>  review-collection-strategy.md  (Channel A = beta testers)
                                      │
                                      └─reviews + rating ─>  aso-checklist.md  (rating unlocks search ranking)
                                                                    │
tiktok-reels-content.md ─traffic─>  in-app prompt (review plan, Channel C) + ASO installs (aso plan)
```

The growth engine is a LOOP: Reddit + TikTok drive installs -> in-app prompt + beta asks drive
reviews -> reviews lift the ASO rating -> ASO ranking drives organic search installs -> more
reviews. Every plan here feeds the next.

---

## Critical assumptions (flag if wrong)

These were assumed because prior-sprint artifacts (backend/store/deploy) were empty in this
environment. If any is wrong, the relevant plan needs a small edit:

1. CLIPFORGE is Android-first (inferred from "r/Android" + "ASO" in the brief). If iOS too,
   see the iOS section of aso-checklist.md and swap r/androidapps -> r/iOSProgramming in the
   reddit plan.
2. The product genuinely removes backgrounds AND erases objects at acceptable quality
   (Concept 4 in the TikTok plan STRESS-TESTS the eraser on complex scenes - only ship that
   concept if it performs well; the review plan assumes the delight moment is real).
3. Free tier exists (freemium per the factory's product stance). The review plan's "2 edits
   before prompt" and the ASO copy's "free to try" depend on this.
4. On-device processing is POSSIBLE (this is called out as a major differentiator across all four
   plans but only LEAD with it if true).
5. Spain-first + EN/ES/RU languages (per COMPANY.md). Locale strategy in aso-checklist assumes this.

---

## Open questions consolidated (block launch execution, not plan writing)

These recur across the four plans. Resolving them unblocks the Copywriter AND the actual posting:

1. Public app name (CLIPFORGE is the codename).
2. Final free/paid model + price + free-tier edit limit.
3. On-device vs cloud processing (changes the entire trust/privacy narrative).
4. Confirmed locales at launch (EN only vs EN+ES+RU).
5. Differentiator vs PhotoRoom / remove.bg (one concrete "why this, not that").
6. Privacy policy URL (needs the landing page live first).

These are growth-blocking but NOT Sprint-4-plan-blocking. The plans above are written to be filled
in once these answers land.

---

Authored by Growth agent (FACT-23), Sprint 4. See individual files for per-plan confidence levels.
