# CLIPFORGE - Reddit Launch Plan

> Scope: Sprint 4 (Stage 15 - First Traffic). Which subreddits, post templates, timing.
> Author: Growth (FACT-23). Copywriter drafts the actual post copy separately (see copywriter/).

---

## 0. The one rule that decides everything

r/Android and r/Apple will delete or downvote self-promo into oblivion. Do not post there.
Multiple 2025-2026 guides confirm it: r/Android, r/Apple, and r/apps have strict no-promotion rules
and hostile communities (RedditGrow 2026, MediaFast 2026).

The winning pattern for indie app launches is the OPPOSITE of "go big":
start in small, forgiving, self-promo-friendly subs, refine the pitch, then
gradually move to larger, pickier communities once the messaging converts.
A Jan-2026 Medium case study (100 installs in 3 days via Reddit) found:
"smaller engaged communities (1,000-10,000 members) often converted better than huge ones."

Sources:
- https://redditgrow.ai/use-cases/promote-app
- https://www.mediafa.st/how-to-promote/mobile-app-on-reddit
- https://medium.com/launchmyapp/how-i-got-my-first-100-installs-in-3-days-using-reddit-a-complete-marketing-strategy-for-app
- https://www.reddit.com/r/alphaandbetausers/comments/1pdqkgx/ (curated list of 1000+ promo-friendly subs)

---

## 1. Subreddit tier list

### Tier 1 - Launch here FIRST (forgiving, self-promo allowed)

| Sub | Size (approx) | Why | Post type |
|-----|---------------|-----|-----------|
| r/SideProject | 600k | THE indie launch sub. Welcomes self-promo with a build story. Forgiving of rough edges. ALWAYS launch here first. | Build-story post |
| r/alphaandbetausers | 150k | Literally exists for "test my app" posts. Mega-list of 1000+ promo subs pinned. | "Looking for beta testers / feedback" |
| r/IMadeThis | 300k | "I made this" culture. Story over sales. | Build-story post |
| r/androidapps | 250k | Android app discovery, allows dev posts with flair. | App announcement |
| r/appdev | 120k | Developer community, sympathetic to launches. | Build-story / dev post |

### Tier 2 - Niche (higher conversion, smaller)

| Sub | Size (approx) | Angle | Risk |
|-----|---------------|-------|------|
| r/photography | 4.5M | Only if CLIPFORGE has a genuine workflow angle (product photographers, real estate). NOT a promo dump - share a technique/tip that uses the app. | Strict on promo; lead with value |
| r/postprocessing | 600k | Photo editing crowd. Object removal / bg cutout is a real workflow here. | Lead with a tutorial, not an ad |
| r/Entrepreneur | 2.2M | For the indie FOUNDER story, not the app. "Built this in X days, here's what I learned." | Story angle only |
| r/SaaS | 250k | If positioning skews prosumer/B2B (e.g., ecom sellers removing backgrounds). | Business-story angle |
| r/Flipping / r/EtsySellers | 600k / 400k | HIGH-INTENT niche: ecom/poshmark/etsy sellers NEED clean product cutouts. Highest-converting niche for a bg remover. Read each sub's self-promo rules first. | "Tool that saves me 20 min/product shoot" |

### Tier 3 - AVOID for direct promo (engage as a member only)

- r/Android (5M), r/Apple, r/apps, r/iphone - NO self-promo. You may comment helpfully if someone asks "how do I remove a background" and your app genuinely fits, but never link-drop a fresh launch.

### Niche photo subs to monitor (value-first engagement)
r/AnalogCommunity, r/photocritique, r/PhotoshopTutorials, r/GIMP - show up, answer questions about object removal / masking, build reputation over weeks before ever mentioning your tool.

---

## 2. Launch sequence and timing

Principle: stagger posts 3-5 days apart, never the same sub twice in a month, and NEVER cross-post
the exact same title (Reddit's anti-spam downranks it).

| Day | Action | Sub | Goal |
|-----|--------|-----|------|
| D-3 (pre-launch) | Soft post in r/alphaandbetausers: "launching in 3 days, want 10 beta testers" | alphaandbetausers | Collect first feedback + warm up account karma |
| D0 (launch day) | Build-story launch post | r/SideProject | First wave of installs + honest feedback |
| D0 (+4h) | Cross-post a DIFFERENT angle (e.g., "the tech behind it") | r/androidapps or r/appdev | Second wave |
| D2 | Value-first tutorial post ("how I remove photobombers from vacation photos") | r/postprocessing | Trust-building, soft CTA in comments |
| D4 | Niche ecom post ("tool that saves me 20 min per product shoot") | r/EtsySellers / r/Flipping (check rules) | Highest-intent installs |
| D7 | Founder-story post ("built an AI bg remover in X, here's what I learned") | r/Entrepreneur | Brand + traffic |
| D10-30 | Engage as a MEMBER in r/photography, r/PhotoshopTutorials - answer questions, mention tool only when genuinely the best answer | niche photo subs | Long-tail organic |

### Timing within a day (US-centric; Reddit traffic peaks ET evening)
- Best window: Tue-Thu, 9:00-11:00 AM ET (catches US morning scroll + EU evening) OR 7:00-9:00 PM ET (peak engagement).
- Avoid: Fri afternoons, weekends for tech subs (lower engagement), and Monday morning (buried under weekend backlog).
- Spain/EU angle: if targeting Spain-first per COMPANY.md, also consider 14:00-16:00 UTC to catch the EU afternoon.

### Account karma rule
Do NOT launch from a brand-new account. Build 50+ comment karma in the target subs over the prior
2 weeks by answering questions genuinely. Reddit's spam filters shadowban low-karma self-promo
accounts silently - your post will show as "submitted" to you but be invisible to others.

---

## 3. Post templates (structure, not final copy)

Final copy is the COPYWRITER's job (copywriter/reddit-drafts.md).
Below = the structural skeleton each post must follow. Fill [BRACKETS].

### Template A - Build-story launch (r/SideProject, r/IMadeThis, r/appdev)

    Title: I built [app name] - an AI background remover + object eraser. Here's the 6-week story.

    Body structure (in this order):
    1. HOOK (1 line): the personal pain that started it.
       "I spent 20 minutes in Photoshop removing my ex from vacation photos. Thought: a phone should do this in 2 seconds."
    2. WHAT IT DOES (3 bullets, outcome not feature):
       - Remove background in 1 tap
       - Erase any object/person by brushing over it
       - [unique differentiator - ON-DEVICE? FREE? BATCH?]
    3. HOW IT WORKS (1 short paragraph, non-technical): which model, why fast.
    4. WHAT I LEARNED (2-3 honest bullets - Reddit rewards vulnerability):
       - "First version was too slow. Switched to [X]."
       - "Object eraser was hard because [Y]."
    5. FREE / PAID - be transparent. Redditors hate hidden paywalls.
       "Free to try (X edits/day). Pro = $Y/mo for unlimited + batch."
    6. ASK: "Would love brutal feedback. What's missing?"
    7. Link: Play Store or waitlist. Imgur/Gyazo GIF demo ABOVE the link.

Non-negotiables:
- A GIF/screen recording in the post body (Reddit loves visual proof for tools). Host on imgur/redgifs, embed inline.
- Disclose you're the dev in the title or first line ("I built..."). Hiding it = instant distrust.
- Reply to EVERY comment within 4 hours for the first 48h. Comment engagement is a ranking signal.

### Template B - "Looking for beta testers" (r/alphaandbetausers)

    Title: [Android] CLIPFORGE - AI bg remover + object eraser. Looking for 10 beta testers (free Pro for feedback).

    Body:
    1. One-line what + who it's for.
    2. What works now / what's rough (honesty = signups).
    3. What I need from testers (3 specific asks: "try erasing a person from a group photo, tell me if edges look right").
    4. How to join: DM or form link.
    5. What testers get: free Pro, named in credits (optional).

### Template C - Value-first tutorial (r/postprocessing, r/photography)

    Title: How I remove photobombers from photos without Photoshop (2-min workflow)

    Body:
    1. The problem (relatable).
    2. Step-by-step with screenshots - USING your tool but framed as a TECHNIQUE.
    3. Mention the tool by name once, naturally. Link only if sub rules allow; otherwise "in profile."
    4. End with a question to spark comments ("what's your go-to method?").

Why this works: value-first posts in strict subs survive moderation and build the kind of organic
mentions that drive 10x the installs of a promo post.

### Template D - Founder story (r/Entrepreneur, r/SaaS)

    Title: I built an AI background remover in 6 weeks as a solo dev. Here's what worked (and what flopped).

    Body:
    1. The decision to build it (market signal: remove.bg does $X, PhotoRoom has Y users).
    2. Tech stack + cost (Redditors love unit economics: "costs me $0.001/edit").
    3. Launch results (installs, conversion, surprises) - ONLY post with real numbers.
    4. 3 lessons.
    5. Soft link in comments.

---

## 4. Anti-patterns (will get you banned or ignored)

- Posting the SAME title to 5 subs on day 1 (anti-spam downrank).
- Using a BRAND account with 0 history -> shadowban.
- Hidden paywall discovered mid-use -> 1-star reviews + downvote brigade.
- Arguing with critics in comments. Thank them, log the feedback, fix it.
- Cross-posting (Reddit shows "crossposted" badge -> looks like spam). Write fresh posts per sub.
- Posting in r/Android / r/Apple / r/apps directly.

---

## 5. Measurement

Track per-sub (simple spreadsheet or the CLIPFORGE analytics):
- Installs attributed (use a distinct ref=reddit_SUB UTM/play-referrer per post)
- Upvote ratio + comment count (engagement signal)
- Review mentions ("saw this on r/SideProject")
- Kill signal: a sub yields fewer than 5 installs after a well-received post -> drop it from the rotation.

Target (first 30 days): 3-5 high-quality posts -> 150-400 organic installs.
Benchmark: indie launches report 100-300 installs from a single good r/SideProject post; niche ecom
subs convert higher but smaller volume.

---

## 6. Open questions for the team (block before posting)

1. Is CLIPFORGE Android-only, or iOS too? Changes which subs (r/androidapps vs r/iOSProgramming).
2. Free vs paid model + price? Must be stated transparently in posts. (Await Sprint 6 monetization.)
3. On-device or cloud? Privacy angle is a MAJOR differentiator on Reddit - lead with it if true.
4. Differentiator vs PhotoRoom / remove.bg? Every post needs one concrete "why this, not that."

These four answers feed directly into the Copywriter's reddit drafts.

---

Confidence: High on subreddit selection and sequencing (evidence-backed). Medium on install targets (benchmarks vary widely by app quality and timing).
