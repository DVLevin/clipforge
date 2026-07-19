# CLIPFORGE - Review Collection Strategy (First 20 Five-Star Reviews)

> Scope: Sprint 4 (Stage 15). How to get the first 20 five-star reviews ORGANICALLY.
> Author: Growth (FACT-23).

---

## 0. The hard constraint: Google Play bans incentivized reviews

This is the single most important fact governing this whole plan. Google Play's policy EXPLICITLY
prohibits:
- Offering any reward, discount, or bonus in EXCHANGE for a review.
- Conditioning a reward on the review being positive (or even on a review being left at all).
- Review manipulation (buying reviews, review swaps, using review-broker services).

Violating this gets reviews purged AND can get the app suspended. Famewall (2026 guide on ethical
review incentives) and Yotpo's incentivized-review analysis both stress: the line you cannot cross
is "reward contingent on leaving a review / on the review's sentiment." Everything legal sits on
the "ask, do not pay" side.

So the strategy is NOT "how to buy/incentivize 20 reviews." It is: "how to engineer the moments
and channels where happy users NATURALLY leave a 5-star review." That is what "organically" means
here - real users, real satisfaction, well-timed asks.

Sources:
- https://famewall.io/blog/how-to-incentivize-reviews/ (2026 - what is allowed vs banned)
- https://www.yotpo.com/blog/incentivized-reviews/ (incentivized review risks and best practices)

---

## 1. The fundamental lever: ask at the moment of MAX delight

Most apps ask for a review at the wrong time (on open, or on a schedule). Reviews are an EMOTIONAL
act - people leave 5 stars when they just felt "wow that worked." The entire strategy is to detect
that emotional peak and ask then, and ONLY then.

For CLIPFORGE the delight moment is obvious and measurable: the instant a background removal or
object erase COMPLETES and the user sees the clean result. That is the peak. Ask there.

### The in-app review prompt - rules
- Use Google's native In-App Review API (com.google.android.play:review). It shows the system review
  sheet WITHOUT leaving the app, and Google rate-limits it (roughly once per year per user) so you
  cannot spam it.
- TRIGGER it ONLY when ALL of these are true:
  1. The user has successfully completed at least 2 edits (not on first use - too early, no trust).
  2. The edit just finished and the result is on screen (the delight peak).
  3. The user has NOT seen the prompt in the last 90 days.
  4. (Soft signal) the user shared or exported the result - an action indicating satisfaction.
- NEVER trigger it after an error, a slow operation, or a paywall hit.
- The API itself decides whether to actually show the sheet (Google caps frequency), so calling it
  is safe even if it does not render.

This single change typically 3-5x's review rate vs a "rate us" button in settings.

---

## 2. The 20-review playbook (channel by channel)

Target: 20 five-star reviews in the first 30 days. Here is where they come from, realistically.

### Channel A - Beta testers (5-7 reviews) - HIGHEST reliability
- From the r/alphaandbetausers beta cohort (see reddit-launch-plan.md), you will have 10-15 testers
  who opted in explicitly.
- They are pre-disposed to like the app AND to help. After they have used it for a week, send a
  personal message: "Hey - really appreciate you testing. If CLIPFORGE earned it, a quick Play Store
  rating would genuinely help a solo dev get visible. No pressure either way."
- KEY: the framing "if it earned it" + "solo dev" + "no pressure" is what keeps it organic and
  policy-safe. You are asking, not paying. Their free-Pro beta access is NOT contingent on a review
  (they get it regardless).
- Expect 40-60 percent of testers to leave a review. 10 testers -> 4-6 reviews.

### Channel B - Reddit launch supporters (3-5 reviews)
- After a well-received r/SideProject launch, add ONE soft line in a comment reply (not the post):
  "if you tried it and it earned a rating, it genuinely helps a solo dev get found."
- Do NOT put the ask in the main post (reads as begging, hurts the post). Only in a reply, only to
  people who already commented positively.
- Expect 10-15 percent of positive commenters to convert to a review.

### Channel C - The in-app prompt on real users (6-9 reviews)
- This is the passive engine. Once you have a few hundred installs (from Reddit + TikTok), the
  delight-triggered in-app prompt converts roughly 2-4 percent of active users to reviewers in the
  first month.
- Math: 300 active users x 3 percent = 9 reviews. This is your biggest source once traffic flows.
- The prompt quality (timing) is the entire lever here - see section 1.

### Channel D - Personal network (2-4 reviews) - use carefully
- Friends/family who genuinely use the app. Same rules: ask, do not pay, and ONLY people who would
  actually use a photo tool (do not ask your uncle who has no photos - fake-use reviews get flagged).
- Keep this to under 5 reviews. More than that and the "all reviews from accounts with no other
  reviews" pattern triggers Google's review-quality algorithms.

Total realistic: 5-7 (beta) + 3-5 (reddit) + 6-9 (in-app) + 2-4 (network) = 16-25 reviews.
Target of 20 is achievable within 30 days IF traffic flows and the prompt is well-timed.

---

## 3. What gets a review REMOVED (avoid these)

Google's review-spam detection flags and purges:
- Clusters of reviews from accounts with NO other reviews / no other app activity.
- Reviews posted in a short burst (same day, same hour) - looks coordinated.
- Reviews with near-identical text (copy-paste from a template you gave people).
- Reviews from accounts in a different country than the app's primary market with no plausible link.
- Any review where the reviewer later admits they were paid/rewarded.

Operational rules that follow:
- STAGGER asks - do not message all 10 beta testers on the same day asking for reviews.
- NEVER give anyone review text to copy-paste. If they ask what to write, say "just what you
  honestly felt - one sentence is fine."
- Do not ask more than ~5 personal-network people.

---

## 4. Turning the first 20 into 200 (compounding)

Once you have 20+ reviews and a 4.5+ average:
- The Play Store algorithm starts surfacing CLIPFORGE in "similar apps" and search for
  "background remover" / "object eraser" - this is where ASO (see aso-checklist.md) compounds.
- Reply to EVERY review (positive and negative) within 48h. Google rewards developer engagement,
  and public replies to negative reviews often get the user to revise their rating up.
- Feature-request replies: "Great idea - added to the roadmap, shipping in v1.2." This converts
  3-star "wish it did X" reviews into 5-star "they actually listened" reviews on the next update.

---

## 5. Measurement

- Review count + average rating (track weekly).
- Review-to-active-user conversion rate (reviews this week / active users this week). Target: 2-4 percent.
- Source attribution: ask beta testers casually which channel brought them (or just infer from timing).
- Sentiment themes: tag reviews by what they praise (speed / quality / free tier) - this feeds back
  into ASO keyword choices and Reddit/TikTok messaging.

## Kill / pivot signals
- If after 500 active users you have under 5 reviews: the in-app prompt timing is wrong (likely
  firing too early or after errors). Fix before any other growth spend.
- If average drops below 4.0: pause acquisition, fix the top complaint, then resume. Driving traffic
  to a 3.5-star app burns the listing permanently.

---

## 6. Open questions (block before launch)
1. Is the In-App Review API wired into the build? (Backend/eng task - check Sprint 2/3 deliverables.)
2. What is the delight-trigger signal available in-app? (Need eng to expose an "edit completed +
   exported" event the prompt can key off.)
3. Free-tier edit limit? Affects how many edits a free user completes before being asked (need 2+).

---

Confidence: High on the policy constraints and the "ask at delight peak" mechanism (well-established
mobile growth practice). Medium on the exact review counts per channel (depends on install volume,
which depends on Reddit/TikTok execution).
