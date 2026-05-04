# Track 1: Operations Workstation

In conversations with housekeeping staff at Victoria mid-market hotels, the same three needs surface every time. They want to know which arriving guests have accessibility needs before assigning a room attendant. They want to know which rooms are going to take twice as long because of the state of the checkout. And they want to know when supplies are going to run short before the cart runs out mid-floor.

None of that information is unavailable. It exists in the PMS, in the supply tracker, in the housekeeping app. The problem is that it sits in three different systems and none of them talk to each other.

**Your job: build the tool that connects them.**

## Quickstart

```bash
pip install -r requirements.txt
python tracks/track1-operations-workstation/generator/generate.py
jupyter lab tracks/track1-operations-workstation/notebooks/00_quickstart.ipynb
```

> **Status:** Generator in development. ERD, field dictionary, and problem framing are final.

## Data at a glance

| Table | Target rows | What it is |
|---|---|---|
| properties | 2 | Boutique hotel (~100 rooms, F&B, spa, event space) + event venue with F&B |
| rooms | ~100 | Room inventory: type, floor, accessibility, max occupancy |
| bookings | ~30,000 | Reservations across 24 months — channels, rate plans, lead time, status |
| stays | ~25,000 | Realized stays linked to bookings |
| housekeeping_events | ~80,000 | Room turnover lifecycle — assigned, started, completed, inspected |
| shifts | ~25,000 | Staff shifts — scheduled, actual, department, no-show flag, ESA flags |
| channel_events | ~50,000 | OTA syncs, rate updates, parity violations |
| inventory_movements | ~40,000 | F&B/minibar ins and outs, par-level breaches, waste |
| weather_daily | ~730 | Victoria daily weather joined on date |
| events_calendar | ~400 | Victoria events affecting hotel demand |

## Domain anchors

- **PMS:** Cloudbeds / Mews / Opera reservation lifecycle
- **Housekeeping:** HotSOS / Quore turnover conventions
- **POS:** Silverware *(confirmed at Oak Bay Beach Hotel)*
- **ERP/Inventory:** NetSuite *(confirmed at Oak Bay Beach Hotel)*
- **Channels:** SiteMinder / RateGain OTA sync and parity events
- **Labour:** BC Employment Standards Act shift constraints

## Golden join

`bookings ⋈ stays ⋈ rooms ⋈ housekeeping_events ⋈ shifts` filtered to a date range. Notebook cell 6 builds this as `room_state`. SQLite view: `v_room_state`. Start here.

## Seeded ground truth

- **~50 channel parity violations** — `channel_events.notes` tagged `DATA_QUALITY_ISSUE: parity_breach`
- **~30 housekeeping anomalies** — 3× property median clean time, tagged `ANOMALY_LONG_CLEAN`
- **~20 over-staffed days + ~20 under-staffed days** — surfaced in `v_shift_demand` SQLite view
- **~15 F&B inventory stockout events** — par-level breach preceded service disruption
- **~10 ESA violation flags** — published roster violates BC rest periods, tagged `ESA_VIOLATION_PROJECTED`

## Four challenge angles — pick one

### Angle 1 — Housekeeping copilot
**v1 (demo Sunday):** Top 3 priority rooms at 7 AM, one-line reason each, accept/override/ask-why. Beat the rule-based baseline on time-to-first-arrival-ready room.
**v2 (real pilot):** Supply prediction, anomaly detection on cleaning times, real-time status push to front desk.

### Angle 2 — Demand-aware staffing
**v1:** Take the published next-week roster. Show the demand gap per department per day. Propose the one shift change with the highest impact. Explain the cost.
**Bonus:** Flag staff with elevated no-show risk (`shifts.no_show_flag` history). A supervisor who knows at 7 AM that two attendants likely won't show is in a different position than one who finds out at 7:15 AM.
**v2:** Full ESA-compliant shift generation from the booking pipeline. Minimum legal roster at minimum cost.

### Angle 3 — Channel parity and rate sanity
**v1:** Detect the seeded parity breaches. For each: which channel, what rate, which contract type is breached, recommended rate move.
**v2:** Real-time monitoring — catches parity drift within 30 minutes of the OTA update, proposes one-click fix.

### Angle 4 — F&B inventory operations
**v1:** For each of the next 7 days, which items are at risk of hitting a par-level breach before the next delivery. One "this week's risk items" panel for the F&B director.
**v2:** Full replenishment recommendation tied to event calendar, weather, and day-part patterns. Connected to the purchasing workflow.

## Constraints — judges will check at least one

1. BC ESA: no ESA-illegal roster without an explicit override-with-reason
2. Room sellability: `inspection.status = passed` required — not just turnover complete
3. Cold-chain F&B: hard stop, not a warning
4. OTA parity: flag breach + contract type — no hidden breaches
5. Cognitive load: one priority panel beats seven charts

## Suggested tech

- pandas or duckdb (golden join and constraint filters)
- Prophet / XGBoost (demand forecasting)
- Google OR-Tools (shift assignment as constraint satisfaction)
- Streamlit (the workstation UI matters as much as the model)
- pytest (prove your ESA gates actually reject illegal rosters)
