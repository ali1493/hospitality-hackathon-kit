# Track 2: Guest Lifecycle Integration

## The Problem

In conversations with front desk staff at Victoria boutique hotels, one frustration surfaces more than any other: the gap between what staff know about returning guests and what the system knows. A guest who has stayed four times in a year, who always requests the same room type and always books a spa treatment the morning of day two — that history lives in the staff member's memory, not in the system. When that staff member is off shift, the next person starts from scratch.

That is the Track 2 problem in one sentence: guest knowledge that should be institutional is personal instead.

The guest has given the hotel rich signal across every touchpoint she has touched: the booking channel she prefers, the room type she always requests, the specific therapist she asks for at the spa, the dietary restriction she mentioned at dinner eighteen months ago, the 9 she gave on the post-stay NPS survey with three paragraphs of thoughtful feedback. That signal is not missing. It is in three or four separate systems — the PMS, the spa booking platform, the post-stay survey tool, the review management platform — none of which talk to each other and none of which feed back into the front desk experience.

The result: a guest who has invested real trust and preference data with this property is treated like a stranger every time she returns. A negative review sits unread for a week. A spa appointment history that could inform a meaningful pre-arrival welcome never reaches the therapist. A 9 NPS never becomes a re-engagement message.

Mid-market Victoria hotels do not lack guest data. They lack the connection layer that turns it into a small number of specific actions: a 5-bullet arrival brief the front desk agent reads in 20 seconds, a therapist brief the spa team scans before the client walks in, a post-stay decision engine that picks the right action for each guest instead of sending everyone the same newsletter.

## What the data represents

Five thousand synthetic Victoria-area guests with multi-stay histories spanning two properties:

- **The ~100-room boutique hotel** with a full-service in-house spa (modeled on the Boathouse Spa profile — award-winning, multi-therapist, spa retail), restaurant, and returning-guest program.
- **The event venue with F&B**, where guests interact through ticketed events and banquet attendance — a different but adjacent guest profile shape.

The schema draws from:

- **PMS guest profile shape** (Cloudbeds, Mews, Opera) for the canonical guest record, contact, opt-ins, tier, and preference fields.
- **Oracle CRM** (confirmed at Oak Bay Beach Hotel) for guest segmentation, loyalty tier management, and post-stay engagement. Oak Bay runs enterprise-grade guest data infrastructure — the synthetic dataset reflects this richer profile shape rather than a generic mid-market CRM. Builders building Track 2 prototypes should treat the guest profile as Oracle CRM-shaped, not as a simple flat table.
- **Silverware POS** (confirmed at Oak Bay Beach Hotel) for F&B transaction data — restaurant, pub, minibar, and banquet. Joins to the guest profile via stay_id, enabling guest-level F&B preference inference.
- **Spa management system schemas** (Book4Time and SpaSoft conventions) for appointment bookings, therapist assignments, treatment history, product notes, and sensitivity flags. This is the first Builders Vault hackathon kit to include spa appointment data.
- **Revinate / Cendyn / TrustYou** structures for post-stay survey events, NPS scoring, sub-score categories, and guest-recovery workflows.
- **Google / TripAdvisor / Booking.com review schemas** for source platform, rating, response state, and theme tagging.
- **CASL consent semantics** with explicit opt-in scope (transactional, marketing, win-back), consent date, and revocation date.

Twenty-four months. 30,000 stays, 8,000 spa appointments, 12,000 post-stay surveys, 15,000 reviews, 50,000 post-stay engagement events.

The messiness is real and deliberate. About 8% of guests have stayed at both properties but appear as separate records because the OTA used an obfuscated email alias. Survey responses include free-text comments ranging from thoughtful paragraphs to a single emoji to nothing. Spa appointment notes include informal therapist shorthand that needs parsing. Marketing opt-in flags exist at three different granularities depending on which tool collected them. Some booking channels strip guest email addresses entirely, leaving the property with no contact for post-stay outreach.

## The spa angle — why it matters specifically

The Boathouse Spa at Oak Bay Beach Hotel has ranked among the top 25 spas in North America for multiple consecutive years. It is one of the defining features of the property. And it is running on a booking system that is completely disconnected from the hotel's PMS, CRM, and post-stay tooling.

In conversations with spa operations staff at Victoria boutique hotels, the same morning friction appears repeatedly: the appointment book shows names, but not context. Which clients are in-house hotel guests right now? Which are returning clients with a documented therapist preference? Which have product sensitivities the team needs to know before the treatment begins? Without a connected system, the answers require manual cross-referencing — checking the PMS, checking a paper file of returning client notes, calling the front desk.

That manual lookup runs 30–45 minutes on a busy morning. The information exists. It is just fragmented across systems that were never designed to share it.

Track 2's spa sub-problem is the most differentiated angle in this hackathon kit — no other hospitality hackathon has named it. Builders who choose this angle will be solving a problem that is verified by real operators, has a clear user (the spa team lead at a boutique hotel), and has a specific daily action that the solution makes better.

## Ground truth seeded for scoring

- **~80 cross-property duplicate guest pairs** in `guest_identity_groundtruth.csv` as true positives (same person at two properties, different PMS records). ~30 decoy false positives for precision testing. Note: roughly 8% of the 5,000 guests (~400) have stayed at both properties, but only 80 are labeled in the ground truth file. The remaining ~320 are unlabeled — your matcher will find candidates the ground truth does not cover, which is intentional. Focus on precision and recall against the labeled set.
- **~40 high-NPS no-follow-through cases** — NPS 9 or 10, no re-engagement event in 90 days. Tagged `RED_FLAG_HIGH_NPS_NO_FOLLOWUP`.
- **~30 negative review themes that align with Track 1 ops patterns** — e.g., clusters of "slow check-in" reviews on dates when Track 1 data shows under-staffed front-office shifts. Tagged `OPS_LINKED` in `reviews.theme_tags`.
- **~50 CASL opt-outs** seeded in `guests.marketing_opt_in = false`.
- **~25 high-LTV at-risk guests** with declining recency and a negative recent signal. Tagged `AT_RISK_HIGH_LTV`.
- **~15 spa-sensitive product conflicts** where a `product_sensitivity_flags` note in a prior appointment was not applied to a subsequent booking. Tagged `DATA_QUALITY_ISSUE: sensitivity_missed`.

## Five challenge angles — v1 demo target and v2 stretch

Pick one. The v1 target is what you need to demo Sunday. The v2 stretch is what a real pilot looks like.

### 1. Arrival prep brief
**v1 demo target:** The 7 AM workstation for the front desk lead. Five bullets per arriving guest. Returning guest flag, room preference, dietary note, open issues, spa appointment today. Scannable in 20 seconds. Show 10 arrivals, each brief different, each one drawing on real history in the dataset.
**v2 stretch:** Confidence scoring. Auto-routing of open issues to the right department before arrival. Therapist-facing spa brief generated in parallel.

### 2. Spa & wellness personalization
**v1 demo target:** For each of today's spa appointments, generate a therapist brief: returning client flag, treatment history, last-visit notes, product sensitivity flags, room-guest flag (are they an in-house hotel guest right now?). Show 5 briefs, each one different, each one acting on real history.
**v2 stretch:** Pre-arrival spa outreach (CASL-compliant). Post-treatment follow-up decision (upsell or recovery). Product retail recommendation based on treatment history. Integration with the front desk brief so the hotel and spa are looking at the same guest context.

### 3. Post-stay action engine
**v1 demo target:** For 10 guests in the 90-day post-stay window, pick one action: review prompt, re-engagement, win-back, or nothing. Show the decision and the signal that drove it. Every decision must be CASL-compliant and explainable in plain language.
**v2 stretch:** Full 90-day campaign sequencing. A/B framework for action types. Re-booking attribution back to specific actions. Connects to spa and F&B history for personalizing the content of the win-back message.

### 4. Negative review router
**v1 demo target:** For 5 negative reviews (1–3 stars) from the dataset: route to the correct department, draft a public response (operator-in-the-loop), open a service-recovery ticket with the recommended internal action and a 48-hour SLA. Demo the full chain for 5 real reviews from the data.
**v2 stretch:** Pattern detection across reviews — 12 slow-check-in mentions in 6 weeks auto-generates a staffing recommendation. Connects to Track 1 shift data for closing the loop.

### 5. Cross-track integration
**v1 demo target:** Use Track 2 guest signal to improve one Track 1 decision. A returning VIP arriving Friday at 3 PM triggers: Track 1 housekeeping prioritizes their room for 2 PM readiness; Track 1 F&B adjusts the afternoon minibar restock for their known preferences; Track 2 generates a front desk arrival brief and a spa team note. Show all three decisions from one guest-arrival event.
**v2 stretch:** Full bi-directional integration. Track 1 ops events (room not ready) create Track 2 service recovery triggers in real time.

## Operational and regulatory constraints your solution must respect

Judges will check at least one.

1. **CASL compliance.** No marketing to `marketing_opt_in = false`. No sending to a guest whose only consent scope is transactional. Check scope at action time. Hard gate, not a warning.
2. **Spa product sensitivities are safety constraints.** `product_sensitivity_flags` is not a preference field. A treatment that triggers a documented sensitivity is a safety incident. Hard stop.
3. **Identity preference overrides match confidence.** `identity_preference = keep_separate` means do not merge, regardless of similarity score. Real reasons exist — separated couples, executive aliases, personal privacy choices.
4. **Negative signal must route.** A 4-NPS or 2-star review in a feed without a routing action and recovery path is not a solution.
5. **The operator has limited time.** A post-stay marketing manager runs this program as 20% of their job. A spa team lead has 8 appointments before 10 AM. Tools that require 30 minutes a day to operate will not be used. Tools that produce 3 good decisions per day in under 30 seconds will be used.

Build these as first-class rules. Show the judges where they are enforced in code.

## Suggested tech stack

- **Data:** pandas or duckdb. The guest timeline join is large but laptop-friendly.
- **Identity resolution:** Splink or recordlinkage for the structured baseline; sentence-transformers for embedding-based name matching.
- **NLP:** Small open-source models for sentiment and theme classification; small commercial LLMs (Claude Haiku, GPT-4o-mini) for response drafting and arrival-brief generation. Do not use an LLM for compliance logic.
- **Action engine:** scikit-learn classifier on engineered features with hard CASL and spa-safety rules layered on top as pre/post-filters.
- **UI:** Streamlit for fast, Next.js for polished. The operator-facing surface matters as much as the model.
- **pytest:** Tests that prove CASL gates reject opted-out targets and spa-safety gates reject sensitivity conflicts.

## Where to go from here

- Open `notebooks/00_quickstart.ipynb` and run it end to end.
- Read `docs/erd.mmd` for the full data model.
- Read `dictionary/fields.csv` for exact field semantics, consent scopes, and spa appointment conventions.
- Check the top-level `docs/submission-checklist.md` for Sunday's requirements.

Build something the front desk lead would actually scan at 7 AM, and the spa director would actually trust with their clients.
