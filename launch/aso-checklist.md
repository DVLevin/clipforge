# CLIPFORGE - ASO Optimization Checklist (First 30 Days)

> Scope: Sprint 4 (Stage 15). App Store Optimization for Google Play (Android-first assumption).
> Author: Growth (FACT-23). iOS App Store checklist appended at the end if iOS ships.

---

## 0. What ASO actually does (the one-paragraph mental model)

ASO has two jobs that share one listing: (1) make CLIPFORGE SHOW UP when someone searches
"background remover" / "remove object from photo" (DISCOVERY), and (2) make them TAP INSTALL once
they see it (CONVERSION). Most founders obsess over keywords (discovery) and ignore the screenshot
gallery (conversion) - but a #1 ranking with bad screenshots installs fewer people than a #8
ranking with great screenshots. This checklist weights both. Google Play weights the listing's
text metadata heavily for search (more than Apple does), so get the words right.

Sources (2025-2026 best practice):
- https://www.appalize.com/blog/aso-strategies/the-ultimate-aso-checklist-for-app-store-google-play
- https://www.awesomeaso.com/blog/08-first-app-launch-aso-checklist
- https://www.apptweak.com/en/aso-blog/app-store-optimization-aso-checklist-for-google-play
- https://cliffex.com/product-engineering/app-development/google-play-store-optimization-guide-2025-aso-best-practices/

---

## PHASE 1 - PRE-LAUNCH (days -7 to 0): get the listing right BEFORE publish

### 1.1 Title (50 chars max) - THE highest-weight keyword field
- [ ] Front-load the #1 keyword. Lead with "Background Remover" or "Photo Background Eraser",
      not "CLIPFORGE" (brand has zero search volume at launch).
- [ ] Format: "[Primary keyword] - [secondary]: [brand]". Example:
      "Background Remover & Eraser - CLIPFORGE" or "Remove BG & Objects - Photo Eraser".
- [ ] Include ONE secondary high-intent term ("Object Eraser", "Cutout", "PNG maker").
- [ ] Confirm under 50 chars (Play truncates after ~30 on mobile, so the first 30 must sell).

### 1.2 Short description (80 chars) - second-highest keyword weight, shows in all lists
- [ ] This is the ELEVATOR PITCH + keyword. It appears in every search result and list view.
- [ ] Example: "Remove photo backgrounds & erase objects in 1 tap. Free AI photo editor."
- [ ] Include primary keyword ("background") + action ("remove/erase") + "free".
- [ ] A/B test 2-3 variants after launch (Play Console native experiment tool).

### 1.3 Full description (4000 chars) - keyword-rich, human-readable
- [ ] First 3 lines matter most (the "read more" fold) - put the value prop + primary keywords there.
- [ ] Naturally weave 8-15 relevant keywords: background remover, remove bg, object eraser,
      photo cutout, transparent png, erase person from photo, product photo, photo editor,
      magic eraser, delete unwanted objects, change background.
- [ ] Use formatting: short paragraphs, bullet lists of features/use-cases, ALL-CAPS section headers.
- [ ] Include concrete use-case sections: "For sellers" / "For creators" / "For memories"
      (matches the TikTok Concept 1/2/5 audiences).
- [ ] Mention "free" + the paid upgrade honestly. Do not hide the paywall in copy.
- [ ] NO keyword stuffing (repeating "background remover" 30x) - Google penalizes. Read naturally.
- [ ] Localize: if Spain-first per COMPANY.md, ship an ES translation from day 1 (and EN, RU per
      the factory's language stance). Each locale's description is a separate keyword surface.

### 1.4 Keyword research (do this BEFORE writing 1.1-1.3)
- [ ] Use Google Play's auto-suggest: type "background ", "remove ", "erase " and capture suggestions.
- [ ] Use a free tool (AppTweak free tier / Google Keyword Planner / Sensor Tower free) to get
      search-volume estimates for: "background remover", "remove background from photo",
      "object eraser", "photo eraser", "cutout", "remove person from photo".
- [ ] Check competitors' titles+descriptions: remove.bg app, PhotoRoom, Background Eraser, Magic
      Eraser. Note which keywords the top 3 all share (those are the must-haves).
- [ ] Pick 1 primary (highest relevance x attainable volume) + 5-8 secondary keywords. Write the
      listing around those.

### 1.5 App icon - the single biggest conversion lever
- [ ] Bold, legible at 48x48px (test by zooming out - icons get tiny in lists).
- [ ] One focal element (scissors? a cutout shape? before/after split?). Avoid text in icons.
- [ ] High contrast against white AND dark Play Store backgrounds.
- [ ] Stand out from competitors: scan the top 10 "background remover" icons - if 7 are blue/green
      cutout shapes, pick a different visual cue or color to pop in the grid.
- [ ] Export at 512x512, also prepare adaptive icon (foreground + background layers) for Android.

### 1.6 Screenshot / gallery - second-biggest conversion lever, most neglected
- [ ] 5-8 screenshots MINIMUM (more = better; the gallery is where install decisions happen).
- [ ] First 3 screenshots are the only ones most people see - make them the strongest.
- [ ] Each screenshot = ONE benefit + short caption text overlay (3-5 words), NOT a raw UI dump.
      Example frames: "Erase any object", "Clean cutouts in 2 sec", "Studio-ready product photos",
      "Works on hair & fur", "100% private (on-device)".
- [ ] Show REAL before/after results in at least 2 screenshots (the transformation sells).
- [ ] Localize caption text (ES/EN/RU).
- [ ] Use a phone mockup frame; dark or brand-colored background; large legible caption font.

### 1.7 Feature graphic (1024x500) + promo video
- [ ] Feature graphic is mandatory (shows at top of listing). Reinforce the #1 benefit visually.
- [ ] If possible, add a 30-second YouTube promo video (the in-app demo / a TikTok Concept 1 cut).
      Listings with video convert meaningfully better.

### 1.8 Category, tags, content rating
- [ ] Category: Photography (correct primary category for this app).
- [ ] Tags: fill ALL relevant tags Play offers (Photo Editor, AI, Productivity).
- [ ] Content rating: complete the IARC questionnaire honestly (likely "Everyone").
- [ ] Target audience: 13+; declare ad/ data practices truthfully (privacy policy required).

### 1.9 Privacy policy + data safety form (BLOCKER - cannot publish without)
- [ ] Host a privacy policy page (can be a simple page on the landing site). REQUIRED.
- [ ] Fill the Data Safety form in Play Console accurately: what data is collected (photos? for
      processing?), is it shared, is it encrypted in transit, can users request deletion.
- [ ] If on-device processing: ADVERTISE this in the Data Safety form and the description - it is a
      major trust differentiator (no photos leaving the phone).

---

## PHASE 2 - LAUNCH WEEK (days 0-7): ship clean, watch the data

- [ ] Confirm listing is live and searchable (search incognito for your primary keyword).
- [ ] Verify all locales render (EN/ES/RU) with no broken characters.
- [ ] Set up Play Console experiments: short description (2 variants), icon (if uncertain), and
      the first screenshot. Let experiments run 7 days minimum for statistical power.
- [ ] Install a basic analytics SDK or use Play's built-in (store-performance + crashes) so you can
      attribute installs to the Reddit/TikTok channels (use the ref= params from those plans).
- [ ] Day 1-3: monitor crash rate. If crash-free users under 99 percent, FIX before any traffic push
      - a buggy launch with traffic = 1-star reviews that haunt the listing forever.
- [ ] After the first 10-20 installs from Reddit, check the "acquisition" report to confirm the
      reddit ref tags are registering.

---

## PHASE 3 - OPTIMIZE (days 7-30): iterate on real data

- [ ] Keyword positions: check Play Console "Store performance" -> search rankings for your 5-8
      target keywords weekly. Note which are climbing, which stuck.
- [ ] Conversion rate (store listing -> install): benchmark is 25-35 percent for utility photo apps.
      Below 20 percent => fix the gallery/icon/short description first, not keywords.
- [ ] Run the first A/B experiment winner live by day 14.
- [ ] Reviews: once you cross 10 reviews, the rating shows publicly. Drive the first 20 via the
      review-collection-strategy.md plan. Reply to every review within 48h.
- [ ] Retention check at day 14: D1 retention target 35 percent+, D7 15 percent+ for a utility tool.
      If D1 under 25 percent, the onboarding/first-edit experience is broken - fix before scaling.
- [ ] Add a second locale listing if only one shipped (RU or ES whichever is missing).
- [ ] Re-run competitor scan at day 21: did any competitor change their title/screenshots? Match or
      counter.

### Keyword iteration (ongoing)
- [ ] Every 2 weeks: pull the "search terms bringing installs" report from Play Console. These are
      GOLD - they tell you what people actually searched. Add the surprising high-volume ones to
      your description; drop keywords that bring zero installs after 30 days.

---

## PHASE 4 - 30-DAY REVIEW GATE (go/no-go on paid acquisition)

Before spending ANY money on ads or paid installs, the listing must pass:
- [ ] Conversion rate (listing visit -> install) at or above 25 percent.
- [ ] Average rating at or above 4.3 with at least 20 reviews.
- [ ] D1 retention at or above 30 percent.
- [ ] Crash-free users at or above 99.5 percent.

If any of these fail, paid acquisition burns money (you pay to send people to a listing that does
not convert or to an app that churns). Fix organically first. This is the most common indie mistake
and the gate exists to prevent it.

---

## iOS App Store additions (IF iOS ships - lower priority, Android-first)

Apple's ASO differs in a few ways:
- Title (30 chars) + Subtitle (30 chars) are the keyword fields; the description is NOT indexed for
  search (unlike Google). So Apple keyword strategy lives in the 100-char hidden keyword field.
- Screenshots matter even MORE on iOS (larger gallery surface). Same rules: benefit-led captions.
- No "short description" field - the subtitle fills that role.
- Apple Search Ads baseline: even a small ($50-100) ASA campaign can surface the app for branded
  searches once you have a few users. Hold until the 30-day gate passes.

---

## Open questions (block before publish)
1. Final app name in the listing (CLIPFORGE is the codename - is the public name different? The
   public name should itself be keyword-considered, e.g., "BG Eraser" vs "CLIPFORGE").
2. Confirmed free/paid model and the exact free-tier limits (must match listing copy + reviews plan).
3. On-device vs cloud processing? Determines the entire privacy/trust angle in copy + Data Safety.
4. Which locales ship at launch (EN only, or EN+ES+RU per factory stance)?
5. Privacy policy URL + domain (landing page must be live first - depends on the Copywriter's
   landing page deliverable).

---

Confidence: High on the checklist structure and field weights (standard 2025-2026 ASO practice).
Medium on the specific conversion/retention benchmarks (vary by app quality and category nuance).
