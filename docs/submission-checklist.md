# Submission Checklist

**Code freeze:** Sunday [DATE TBD], 2:00 PM PT
**Demo night:** Sunday [DATE TBD], 4:00–8:00 PM at [HOTEL VENUE TBD], Victoria BC
**Submit via:** Devpost — link posted in event Discord

---

## Required — all teams

- [ ] **Public GitHub repo** with working code. Link on Devpost. Repo must be public by code freeze.
- [ ] **README in your repo** — what you built, which track, which sub-problem, how to run it locally.
- [ ] **1-page technical summary** (PDF or Markdown) submitted at code freeze. Judges read this before demos. Sections: problem chosen, approach, what works, what doesn't, what ships next in a real pilot.
- [ ] **Working demo.** Live preferred. Recorded fallback. 4 minutes max on stage. 3 minutes judge Q&A.
- [ ] **Track declaration.** Pick one: Track 1 Operations · Track 2 Guest Lifecycle · Track 3 Tourism.
- [ ] **Sub-problem declaration.** Name the specific sub-problem you picked within your track. One sub-problem shipped deep beats four touched shallowly.
- [ ] **Operator-fit statement.** One paragraph: which specific operator role (housekeeping supervisor at a boutique hotel, spa director, whale watching captain, front desk lead) would use this Monday morning, and how.
- [ ] **Constraints statement.** One paragraph on how your solution respects the constraints for your track.
- [ ] **Team list** — 2–3 members on Devpost. No solo entries. No teams of 4+.

## Recommended

- [ ] Hosted demo URL (Streamlit Cloud, Vercel, or Replit — all free)
- [ ] Short screen recording (Loom or OBS) in case live demo tech fails
- [ ] Before/after workflow: what does the operator do today vs. with your tool?
- [ ] Baseline improvement evidence — MAPE reduction, F1 score, time saved, revenue at risk quantified. Numbers beat adjectives.
- [ ] Attribution: `"Data: BuildersVault Hospitality Hackathon starter kit (synthetic), CC BY 4.0."`

---

## Judging rubric

Four criteria, scored independently by each judge, then averaged. Different weights per track — read carefully.

### Track 1 — Operations Workstation

| Criterion | Weight | What judges look for |
|---|---|---|
| Problem Fit | 22% | Does this solve a real Victoria operator pain a GM or housekeeping supervisor would recognize? Is the target user specific and named — not "hotel staff"? |
| **Technical Merit** | **35%** | Does it work? Does it beat the kit baseline? Are BC ESA constraints enforced in code, not comments? Can a judge read the repo and find where the operational gates live? |
| Domain Grounding | 22% | Does it reflect how a real mid-market hotel operates — not how a textbook describes it? Does it honor the integration thesis? |
| Production Readiness | 21% | Could a housekeeping supervisor or F&B director run this without a developer in the room? Is the interface one panel, not 40 widgets? |

### Track 2 — Guest Lifecycle Integration

| Criterion | Weight | What judges look for |
|---|---|---|
| Problem Fit | 25% | Does this solve a real guest experience or post-stay pain? Is the Oracle CRM or Silverware POS data shape respected? |
| Technical Merit | 22% | Are CASL gates enforced in code? Are spa product sensitivity flags treated as hard stops, not preferences? Does identity resolution beat the baseline dedup? |
| Domain Grounding | 28% | Does it reflect how a real front desk, spa director, or post-stay manager thinks? Does it understand the 20-second constraint on an arrival brief? |
| Production Readiness | 25% | Could a GM or spa team lead run this on Monday without training? Is the interface designed for someone with 8 things on their mind? |

### Track 3 — Tourism Operations

| Criterion | Weight | What judges look for |
|---|---|---|
| Problem Fit | 30% | Does this solve the weather cancellation, capacity, or cross-visitor-journey problem a Victoria tour operator faces daily from April to October? |
| Technical Merit | 25% | Does the weather-decision engine show revenue impact per option? Is the cross-dataset fuzzy match honest about confidence scores — no fake direct joins? |
| Domain Grounding | 25% | Does it reflect how a tour operator actually runs — multi-departure, weather-dependent, guide-certification-constrained? |
| Production Readiness | 20% | Could a tour operations manager use this at 6 AM on a decision with $36,000 at stake? Is the output one clear recommendation with a reason? |

### Tie-breaker

Show of hands from the operator audience: "Would you pilot this with your property or operation?" One vote per attending operator. Not scored — used only to break ties between submissions within 5% of each other.

---

## Track-specific constraints — judges will check at least one

### Track 1
1. **BC ESA compliance.** A scheduler that produces a roster violating minimum rest periods (8 hrs between shifts), maximum daily hours, or overtime thresholds without an explicit override-with-reason has a bug, not a feature.
2. **Room sellability.** `housekeeping.status = completed` is NOT sellable until `inspection.status = passed`. Enforce this in code.
3. **Cold-chain F&B.** Items with `cold_chain_required = true` must route through cold-chain locations. A shortcut is a food-safety incident.
4. **OTA parity.** Rate recommendations that would breach a parity obligation must flag the breach with the contract type — not hide it.
5. **Cognitive load.** One priority panel beats seven charts. Build for the person, not the investor demo.

### Track 2
1. **CASL.** No marketing to `marketing_opt_in = false`. Check consent scope (`transactional` / `marketing` / `win_back`) — not just the global flag. Hard gate, not a warning.
2. **Spa product sensitivities.** `product_sensitivity_flags` is a safety constraint. A treatment that matches a documented sensitivity is a hard stop — not a preference override.
3. **Identity preference.** `identity_preference = keep_separate` overrides match confidence. Do not merge profiles that guests have asked to keep separate.
4. **Negative signal routing.** A 1–3 star review or 4 NPS that surfaces in a feed without a routed action and a recovery path is not a solution.
5. **Operator time budget.** A post-stay marketing manager runs this as 20% of their job. Tools requiring 30+ minutes per day will not be used.

### Track 3
1. **Weather decision output.** A cancel/hold/reshift recommendation without a revenue impact estimate and a rebooking plan is incomplete. Show the cost of each option.
2. **Guide certification.** Scheduling must respect Transport Canada certified naturalist requirements per vessel. An unqualified guide on a licensed vessel is a regulatory violation.
3. **Cross-dataset join honesty.** The Viator-to-Booking.com fuzzy match must surface a confidence score, not assume a direct join. Fake direct joins are a fail.
4. **Vessel safety.** A departure decision that ignores a gale warning (advisory_level = gale) must flag that as a hard stop regardless of booking load.

---

## What not to do

- Don't use real PII or scraped data. Use the starter kit's synthetic data only.
- Don't build a dashboard and call it a solution. Information displayed is not the same as a decision made.
- Don't scope creep. The 4-minute limit is enforced. One tight, working thing beats five half-built things.
- Don't fake your demo with hardcoded outputs. If the model isn't ready, show the slice that works and explain the rest.
- Don't submit a deck without a repo. The repo is required.

---

## Awards

- **Track 1 top prize** — best Operations Workstation prototype
- **Track 2 top prize** — best Guest Lifecycle Integration prototype
- **Track 3 top prize** — best Tourism Operations prototype
- **Cross-track integration award** — best prototype connecting 2+ tracks with real data
- **Domain Grounding Award** — team that most clearly designed for a specific Victoria operator
- **Production Readiness Award** — team whose solution could be piloted with the least additional work

Top prize per track: guaranteed SOW pipeline introduction to a BuildersVault operator partner + **[cash amount TBD pending sponsor confirmation]**.
