# BuildersVault: Victoria's Visitor Economy AI Sprint
### Hospitality Hackathon — Victoria BC — June 2026

**Kickoff:** Thursday June [DATE TBD], 5:30 PM — [HOTEL VENUE TBD], Victoria BC
**Close:** Sunday June [DATE TBD], 4:00 PM — same hotel
**Format:** Hybrid — in-person opening + closing, 3 days online build
**Register:** [REGISTRATION URL — TBD]
**Discord:** [EVENT SERVER — TBD]

---

## The pitch

> **Victoria's hotel, venue, and spa operators run on tools that don't talk to each other. This weekend, we build the connection — and prove it works before tourism season.**

Every GM, spa director, F&B manager, and tour operator in Victoria has the same Tuesday morning. The reservation system has no idea what the housekeeping board says. The post-stay survey doesn't feed into the next arrival brief. The spa booking system is completely disconnected from the guest profile in the PMS. A whale watching captain makes a $36,000 weather-cancellation decision at 6 AM with a spreadsheet and a weather app. Each tool works in isolation. Decisions get made by memory, habit, and walking the floor.

40+ builders. 3 tracks. 3 days. One connected stack.

---

## Why this matters — sourced numbers

- **79.9% year-to-date occupancy in 2025** — a 10-year high for Greater Victoria. August hit 94.3%. *(Destination Greater Victoria, Sept 2025)*
- **227,000 airport passengers in August 2025 alone** — 11.3% YoY growth. *(DGV press release)*
- **1M+ cruise passengers in the 2025 season** beginning April. *(Greater Victoria Harbour Authority)*
- **$23B in gross tourism revenue for BC in 2024** — more than forestry, agriculture, mining, and oil and gas combined. *(Destination BC, Value of Tourism 2024)*
- Victoria's mid-market hotels, independent venues, spas, and tour operators are running this growth on legacy tools. The enterprise chains solved the integration problem years ago. The independent operators have not.

---

## At a glance

| | |
|---|---|
| **Tracks** | 3 — Operations Workstation · Guest Lifecycle · Tourism Operations |
| **Teams** | 2–3 people. No solo. No teams of 4+. |
| **Builders target** | 40–50 |
| **Submission** | Devpost: public GitHub repo + 5-min live demo + 1-page technical summary |
| **Code freeze** | Sunday 2:00 PM |
| **Prizes** | Per-track winner + cross-track integration award + SOW pipeline introduction |
| **Primary operator** | Oak Bay Beach Hotel (Oracle CRM · NetSuite · Silverware POS confirmed) |
| **Tourism partners** | Prince of Whales · Eagle Wing Tours (in outreach) |
| **GitHub** | github.com/BuildersVault/hospitality-hackathon-kit |
| **Comparable events** | Cornell + Hilton *(student-only, no SOW pipeline)* · HEDNA Austin · Rosewood 2030 · Kuriftu Ethiopia |
| **Our differentiation** | First mid-market operator hackathon with post-event SOW pipeline. First to include spa and tourism as named challenge domains. |

---

## Tracks

### Track 1 — Operations Workstation
*Back-of-house: hotels, venues, F&B*

A boutique hotel GM arrives at 6:45 AM. She opens four apps before 8 AM and none of them know what the others said. The PMS shows 14 arrivals. The housekeeping board shows 11 rooms clean. She doesn't know which 11, whether any arriving guests have accessibility needs, or whether she has enough front-office staff for the 2 PM group check-in. She figures it out by walking the floor and calling the housekeeping supervisor on her mobile.

**Build the tool that replaces that walk.**

Sub-problems (pick one, go deep):
- **Housekeeping intelligence** — room priority queue, supply prediction, anomaly detection, real-time status to front desk
- **Employee scheduling** — demand-aware rosters, BC ESA compliant, staff no-show risk flagging
- **Vacancy & availability** — channel sync, gap-night recovery, OTA rate-parity monitoring
- **F&B inventory** — par-level alerts before stockout, tied to occupancy + event calendar

Operator tech stack confirmed at Oak Bay Beach Hotel: **Silverware POS · NetSuite ERP · [PMS TBC]**

→ See `tracks/track1-operations-workstation/`

---

### Track 2 — Guest Lifecycle Integration
*Front-of-house: hotels, spas, post-stay*

She has stayed at this hotel four times this year. She always requests the same room type. She books the Boathouse Spa on the morning of day two and always requests the same therapist. She left a 9 NPS after her last stay and mentioned the spa team by name. The front desk agent checking her in today has no idea who she is. The booking came through Booking.com with an obfuscated email alias and a different name spelling. The spa system is a completely separate platform. The post-stay survey is in a folder nobody opened this week.

**Build the tool that makes her feel recognized the moment she walks through the door.**

Sub-problems (pick one, go deep):
- **Arrival prep brief** — 5 bullets per arriving guest, scannable in 20 seconds
- **Spa & wellness personalization** — therapist brief, treatment history, product sensitivity flags (safety constraint, not preference)
- **Upgrade decisioning** — when, to whom, at what price or free
- **Customer satisfaction → action** — NPS/review routed to a specific staff action with SLA
- **Post-stay management** — review prompt, re-engagement, win-back, or nothing (CASL-compliant)

Operator tech stack confirmed at Oak Bay Beach Hotel: **Oracle CRM · Silverware POS · Boathouse Spa system [TBC]**

→ See `tracks/track2-guest-lifecycle/`

---

### Track 3 — Tourism Operations
*Victoria's visitor economy: marine tours, private operators*

A Victoria whale watching operator runs 6 daily departures on a peak summer day. At 6 AM, the captain checks Environment Canada's marine forecast and sees a small craft advisory posted for 2 PM. She has 180 bookings across four afternoon departures — roughly $36,000 of scheduled revenue. She must decide: cancel now (90 rebooking emails, refund processing, Viator reviews), wait and see if the advisory lifts (safety and regulatory risk), or move guests to morning slots already approaching capacity. She makes a version of this decision every operating day from April to October using a weather app and a spreadsheet.

**Build the tool that gives her a defensible, revenue-aware decision at 6 AM.**

Sub-problems (pick one, go deep):
- **Weather-adjusted departure decision** — cancel/hold/reshift with revenue impact and rebooking automation
- **Capacity allocation** — seat distribution across 6 daily departure windows based on demand forecast
- **Guide & vessel scheduling** — demand-aware, Transport Canada certified guide requirements, vessel maintenance windows
- **Victoria visitor journey** — fuzzy-match a whale watching booking with a hotel stay (Viator booking + Booking.com booking, no shared identifier) to build a cross-operator guest profile

Sources: DGV Sept 2025 press release · Eagle Wing Tours (eaglewingtours.com) · Prince of Whales (princeofwhales.com) · Environment Canada marine forecast schema

→ See `tracks/track3-tourism-operations/`

---

### Cross-track integration award
The hardest angle in the event and the highest ceiling. Example: a returning VIP hotel guest who also booked a whale watch tour → Track 2 arrival brief updated + Track 1 housekeeping prioritized + Track 3 tour operator notified of hotel-guest status. Show the full chain from one person's signal to three operator decisions. This is the "Victoria's tools don't talk to each other" problem solved end-to-end.

---

## Judges — 4 seats, one hospitality, three different domains

A panel of four hotel people produces groupthink and misses the technology and commercial angles that make a prototype pilotable.

| Seat | Profile | Scores | Candidates |
|---|---|---|---|
| **1 — Hospitality** | Hotel Operations Manager or F&B Director | Problem Fit + Domain Grounding for Track 1 | Shane Gould (Oak Bay, Dir. Ops) · Christian Sealey (Oak Bay, F&B Dir.) · Amy Leonard (Sandman, GM) |
| **2 — System Builder** | Hospitality tech vendor — track-split rule applies | Technical Merit + Production Readiness for assigned track only. Conflict disclosed at registration. | Silverware Solutions (Track 2 judge — no F&B conflict) · Mews/Cloudbeds (Track 1 judge) |
| **3 — Tourism/Visitor Economy** | Tour operator GM or DGV representative | Problem Fit for Track 3 and cross-track submissions only | Prince of Whales · Eagle Wing Tours · Destination Greater Victoria |
| **4 — AI/Pipeline** | Applied AI practitioner or BV representative | Production Readiness both tracks — evaluates SOW pipeline readiness | Lautaro Cepeda · Victoria Data Society network · Prior BV builder (Healthcare event) |

**Conflict rule:** A system builder who supplies tools to Track 1 operators judges Track 2 only. Conflict disclosed to builders publicly at registration. No exceptions.

---

## Judging rubric

| Criterion | Track 1 weight | Track 2 weight | Track 3 weight |
|---|---|---|---|
| Problem Fit | 22% | 25% | 30% |
| **Technical Merit** | **35%** ← weighted up | 22% | 25% |
| Domain Grounding | 22% | 28% | 25% |
| Production Readiness | 21% | 25% | 20% |

Track 1 Technical Merit is weighted higher because back-of-house operational builds demo less impressively than guest-facing ones. Judges will look past the UI to the underlying model and constraint enforcement.

**Tie-breaker:** show of hands from operator audience — "would you pilot this?"

---

## Format

| When | Where | What |
|---|---|---|
| Thu 5:30–8:30 PM | Hotel ballroom (in-person) | Kickoff: dinner + networking. Three operator problem owners introduce tracks live. Dataset revealed. Team formation. Data in hand before you leave. |
| Fri full day | Online | Build Day 1. Async standup. Operator office hours: housekeeping + front desk (midday, 1 hr). Evening voice check-in. |
| Sat full day | Online | Build Day 2. Async standup. Operator office hours: spa + F&B + tour operator (midday, 1 hr). Evening check-in. Heaviest build day. |
| Sun 9 AM–2 PM | Online | Final build window. 1-page technical summary submitted at code freeze 2 PM. |
| Sun 4–8 PM | Hotel ballroom (in-person) | Closing: live demos, judges, operator audience, awards, SOW pipeline introductions. |

---

## Venue options (5 evaluated)

| Venue | Verdict | Notes |
|---|---|---|
| **Oak Bay Beach Hotel** | ★ Recommended | Oracle CRM + Silverware confirmed. In-kind hosting in exchange for co-branding + first-look at winning prototypes. Sequoia Ballroom + waterfront terrace. In active outreach. |
| Sandman Hotel Victoria | △ Fallback | Amy Leonard (GM) is community-active. Downtown. Good AV. |
| Hotel Grand Pacific | △ Fallback | 3,000 sq ft waterfront ballroom. InnVest ownership adds approval layer. |
| Save-On-Foods Arena | △ Strong BV brand | Matt Cooke relationship. Manage conflict if he is also a judge. |
| UVIC (ECS Building) | ✗ Not recommended | Academic tone mismatch for a commercial-vertical event. No catering. |

---

## The SOW pipeline — how it actually works

The prize is the introduction. Here's the exact process:

1. **Sunday evening** — top 1–2 prototypes per track introduced to operators in the room. BuildersVault facilitates a structured 30-minute conversation.
2. **Within 5 business days** — BV produces a 1-page scope-of-work outline if both sides want to proceed.
3. **Direct negotiation** — builder team and operator negotiate and sign directly. BV is not a party to the contract.
4. **BV earns a 10% referral fee** on signed, paid engagements only. Disclosed to operators at introduction.

Builders own all IP. BuildersVault does not claim ownership of anything built during the event.

---

## What to submit

By **Sunday 2:00 PM (code freeze)**:
- [ ] Public GitHub repo with working code and a README explaining how to run it
- [ ] Devpost submission: repo link + track declaration + sub-problem declaration
- [ ] 1-page technical summary (PDF or Markdown): problem, approach, what works, what doesn't, what ships next
- [ ] Operator-fit statement: which specific operator role uses this Monday morning, and how
- [ ] Constraints statement: how your solution respects the operational/safety/legal constraints for your track

**Sunday 4:30 PM demos:** 4 minutes on stage + 3 minutes judge Q&A. 4-minute limit is enforced.

---

## Operational constraints — judges will check at least one per submission

**Track 1:**
- BC ESA: no roster that violates minimum rest periods or daily maximums without an explicit override-with-reason
- Room sellability: turnover completed + inspection passed. Not just turnover.
- Cold-chain F&B: hard stop, not a warning
- OTA parity: breaches must be flagged with contract type

**Track 2:**
- CASL: no marketing to `marketing_opt_in = false`. Check consent scope, not just the global flag.
- Spa product sensitivities: safety constraint, not preference. Hard stop.
- Negative signal: must route to a specific action and recovery path, not just surface in a feed
- Identity preference `keep_separate`: overrides match confidence

**Track 3:**
- Weather cancellation decisions must show revenue impact and rebooking plan, not just a binary cancel/go
- Transport Canada certified guide requirements must be respected in scheduling
- The cross-operator fuzzy match must be honest about confidence score — no fake direct joins

---

## Quickstart (when generators are ready)

```bash
# Clone
git clone https://github.com/BuildersVault/hospitality-hackathon-kit.git
cd hospitality-hackathon-kit

# Install
pip install -r requirements.txt

# Generate your track's data (pick one or all three)
python tracks/track1-operations-workstation/generator/generate.py
python tracks/track2-guest-lifecycle/generator/generate.py
python tracks/track3-tourism-operations/generator/generate.py

# Open the quickstart notebook
jupyter lab tracks/track1-operations-workstation/notebooks/00_quickstart.ipynb

# Explore visually
streamlit run shared/app/streamlit_app.py
```

**Status:** Generators are in development (~3 weeks engineering). ERDs, field dictionaries, and problem framings are final. See `docs/overview.md` for full kit status.

---

## Licensing

- **Code:** MIT — see `LICENSE`
- **Synthetic data:** CC BY 4.0 — see `DATA_LICENSE.md`. Attribution: *"BuildersVault Hospitality Hackathon starter kit (synthetic), CC BY 4.0"*
- **Builder IP:** Builders own everything they create. BuildersVault does not claim ownership.
- **IP/SOW terms:** Published on registration page before kickoff. TBD pending BV leadership sign-off.

No real PII in this repo. All guest names, emails, and identifiers are Faker-generated with `seed=42`.

---

## Data sources — public and citable

| Source | Used for |
|---|---|
| Destination Greater Victoria — 2025 Annual Report + Tourism Indicators Dashboard (tourismvictoria.com) | Monthly occupancy, visitor volume, seasonal demand index |
| DGV press release Sept 25 2025 — "Strongest Summer in 10 Years" | Airport passengers (Jun 190k · Jul 207k · Aug 227k), BC Ferries 9.4M, cruise 1M+ |
| Destination BC — Value of Tourism 2024 (destinationbc.ca) | $23B gross revenue, 113,000+ direct jobs, GDP contribution |
| Environment Canada marine forecast (weather.gc.ca/marine) | weather_marine table schema, advisory_level field, Salish Sea sea-state conventions |
| Eagle Wing Tours (eaglewingtours.com) | Year-round operations confirmed, Fisherman's Wharf, multiple daily departures, season structure |
| Prince of Whales (princeofwhales.com) | 95% sighting rate, Inner Harbour 812 Wharf St, Viator distribution confirmed |
| BC Stats Tourism Data Catalogue | Historical seasonal patterns, regional occupancy benchmarks |
| Viator / TripAdvisor | Tour booking channel structure for `tour_bookings.booking_channel` field |

---

## Support

- **Event Discord:** [TBD]
- **Kit issues:** open a GitHub issue tagged `dataset` or `generator`
- **Event host:** [TBD — BuildersVault]
- **Contact:** [TBD]
