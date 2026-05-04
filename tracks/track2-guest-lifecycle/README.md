# Track 2: Guest Lifecycle Integration

In conversations with front desk staff at Victoria boutique hotels, one frustration surfaces more than any other: the gap between what staff know about returning guests and what the system knows. A guest who has stayed four times in a year, who always requests the same room type and always books a spa treatment the morning of day two — that history lives in the staff member's memory, not in the system. When that staff member is off shift, the next person starts from scratch.

That is the Track 2 problem: guest knowledge that should be institutional is personal instead.

**Your job: build the tool that makes it institutional.**

## Quickstart

```bash
pip install -r requirements.txt
python tracks/track2-guest-lifecycle/generator/generate.py
jupyter lab tracks/track2-guest-lifecycle/notebooks/00_quickstart.ipynb
```

> **Status:** Generator in development. ERD, field dictionary, and problem framing are final.

## Data at a glance

| Table | Target rows | What it is |
|---|---|---|
| guests | 5,000 | Guests: name variants, contact, opt-ins, tier, churn risk flag |
| guest_preferences | 5,000 | Room type, dietary, spa therapist, communication channel |
| stays | ~30,000 | Realized stays — linked to Track 1 bookings via `booking_id` |
| fb_receipts | ~80,000 | F&B transactions: restaurant, minibar, banquet, room service |
| spa_appointments | ~8,000 | Spa: treatment, therapist, product notes, sensitivity flags |
| surveys | ~12,000 | Post-stay NPS + CSAT sub-scores + free text |
| reviews | ~15,000 | Google / TripAdvisor / Booking.com — rating, theme tags, response status |
| post_stay_events | ~50,000 | Email opens, clicks, win-back redemptions, re-bookings, unsubscribes |
| guest_identity_groundtruth | ~110 | 80 confirmed cross-property duplicate pairs + 30 decoy false positives |

## Domain anchors

- **Guest CRM:** Oracle CRM *(confirmed at Oak Bay Beach Hotel)* — richer profile than generic mid-market CRM
- **POS:** Silverware *(confirmed at Oak Bay Beach Hotel)* — joins to guest via `stay_id`
- **Spa:** Book4Time / SpaSoft appointment schemas
- **Post-stay:** Revinate / Cendyn / TrustYou engagement schemas
- **Reviews:** Google / TripAdvisor / Booking.com review structures
- **Compliance:** CASL consent semantics (transactional / marketing / win_back scopes)

## Golden join

`guests ⋈ stays ⋈ fb_receipts ⋈ spa_appointments ⋈ surveys ⋈ reviews ⋈ post_stay_events` keyed on `guest_id`. Notebook cell 6: `guest_timeline`. SQLite view: `v_guest_timeline`. Start here.

## Seeded ground truth

- **~80 cross-property duplicate guest pairs** — true positives in `guest_identity_groundtruth.csv`. ~30 decoy false positives. Note: ~400 guests total have stayed at both properties but only 80 are labeled — the rest are unlabeled, which is intentional.
- **~40 high-NPS no-follow-through** — NPS 9–10, zero re-engagement in 90 days. Tagged `RED_FLAG_HIGH_NPS_NO_FOLLOWUP`.
- **~30 negative review themes mapped to Track 1 ops patterns** — slow check-in reviews on under-staffed front-office dates. Tagged `OPS_LINKED` in `reviews.theme_tags`.
- **~50 CASL opt-outs** — seeded in `guests.marketing_opt_in = false`.
- **~25 high-LTV at-risk guests** — declining recency + negative recent signal. Tagged `AT_RISK_HIGH_LTV`.
- **~15 spa sensitivity conflicts** — `product_sensitivity_flags` not carried forward to rebooking. Tagged `DATA_QUALITY_ISSUE: sensitivity_missed`.

## Five challenge angles — pick one

### Angle 1 — Arrival prep brief
**v1:** 5 bullets per arriving guest, scannable in 20 seconds: returning guest flag, room preference, dietary note, open issues, spa appointment today. Show 10 arrivals, each brief different.
**v2:** Confidence scoring, therapist-facing spa brief generated in parallel, open issue auto-routing to department before arrival.

### Angle 2 — Spa & wellness personalization
**v1:** For each of today's spa appointments, a therapist brief: returning client flag, treatment history, product sensitivity flags (SAFETY CONSTRAINT — hard stop), last-visit notes.
**v2:** CASL-compliant pre-arrival outreach, post-treatment follow-up decision, retail product recommendation from treatment history.

### Angle 3 — Post-stay action engine
**v1:** For 10 guests in the 90-day post-stay window, pick one action: review prompt / re-engagement / win-back / nothing. Show the decision and the signal. CASL-compliant by construction.
**v2:** Full 90-day campaign sequencing, A/B framework, re-booking attribution.

### Angle 4 — Negative review router
**v1:** For 5 negative reviews (1–3 stars): route to correct department, draft public response (operator-in-the-loop), open service-recovery ticket with recommended internal action and 48-hr SLA.
**v2:** Pattern detection across reviews — 12 slow-check-in mentions in 6 weeks auto-generates a Track 1 staffing recommendation.

### Angle 5 — Cross-track integration
**v1:** Use Track 2 guest signal to improve one Track 1 operational decision. A returning VIP arriving Friday → Track 1 housekeeping prioritizes their room, Track 2 arrival brief generated.
**v2:** Full bi-directional integration. Track 1 ops events (room not ready) create Track 2 service-recovery triggers.

## Constraints — judges will check at least one

1. CASL: no marketing to `marketing_opt_in = false`. Check consent scope — not global flag.
2. Spa sensitivity: `product_sensitivity_flags` = safety constraint, hard stop.
3. Identity preference: `keep_separate` overrides match confidence.
4. Negative signal: must route to action + recovery path.
5. Operator time: tools requiring 30+ minutes/day will not be used.

## Suggested tech

- Splink or recordlinkage (identity resolution baseline)
- sentence-transformers (NLP on reviews and spa notes)
- scikit-learn (post-stay action classifier)
- Claude Haiku or GPT-4o-mini (arrival brief generation, review response drafting)
- Streamlit (operator-facing surface matters as much as the model)
- pytest (prove CASL gates reject opted-out targets and spa-safety gates reject sensitivity conflicts)
