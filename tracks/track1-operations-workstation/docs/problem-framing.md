# Track 1: Operations Workstation

## The Problem

A housekeeping supervisor at a Victoria boutique hotel gets to work at 6:45 AM. Her job for the next 90 minutes is to figure out which rooms need to be turned first, who is cleaning what, whether there are enough supplies on the carts, and which rooms need an inspection before a guest can check in. She does this using a paper rounding board, a walkie-talkie, and years of accumulated memory about her property.

In conversations with housekeeping staff at Victoria mid-market hotels, the same three needs come up every time. They want to know which arriving guests have accessibility needs before assigning a room attendant. They want to know which rooms are going to take twice as long because of the state of the checkout. And they want to know when supplies are going to run short before the cart actually runs out mid-floor.

None of that information is unavailable. It exists — in the PMS, in the supply tracking tool, in the housekeeping app. The problem is that it sits in three different systems and none of them talk to each other. The supervisor has learned to work around the fragmentation. The cost of that workaround is 90 minutes every morning and a room that is not ready when the guest arrives.

The same fragmentation appears everywhere in back-of-house operations. A restaurant F&B manager at a Victoria multi-outlet hotel group describes ordering inventory "by feel and experience" because the POS system has no connection to the hotel occupancy data. A front office manager describes copying last week's roster into the next week because the scheduling tool has no view of the booking pipeline. A revenue manager describes finding out about a rate-parity breach on Expedia at 11 AM because the channel manager and the PMS sync on a 6-hour delay.

These are not technology failures. They are integration failures. The tools exist. The data exists. The connection doesn't.

## What the data represents

Two synthetic Victoria-area properties modeled on real mid-market operations:

- **A ~100-room boutique hotel** with multiple F&B outlets (a restaurant, a pub, minibar service), an in-house spa, event space, and a 15-person operational staff across housekeeping, front office, F&B kitchen, F&B service, and maintenance.
- **An event venue with F&B** modeled on the operational pattern of a Victoria conference and events venue — concession inventory, banquet F&B, event-driven shift demand, no in-house lodging.

The schema draws from PMS lifecycle (Cloudbeds, Mews, Opera), channel-event models (SiteMinder, RateGain), HotSOS / Quore housekeeping conventions, BC ESA shift constraints, Silverware POS (confirmed at Oak Bay Beach Hotel — used for restaurant, pub, minibar, and banquet F&B), and NetSuite ERP (confirmed at Oak Bay Beach Hotel — used for inventory management, purchasing, and F&B cost of goods). The synthetic data is shaped to these specific systems so prototypes built on the kit are structurally compatible with the operator's real stack.

Twenty-four months of operational records. The data is messy on purpose: housekeeping events with start timestamps but no end timestamps because someone forgot to tap Complete. Shift records where the actual end time crosses midnight. Channel events arriving out of order due to OTA latency. Two date formats per source system. The kind of stuff every real hotel has and every demo hides.

## Ground truth seeded for scoring

- **~50 channel-parity violations** tagged in `channel_events.notes` with `DATA_QUALITY_ISSUE: parity_breach`.
- **~30 cleaning-time anomalies** where turnover took 3x the property median, tagged `ANOMALY_LONG_CLEAN` in `housekeeping_events.flags`.
- **~20 over-staffing days and ~20 under-staffing days** surfaced in the `v_shift_demand` view.
- **~15 inventory stockout events** where par-level breach preceded F&B service disruption, tagged in `inventory_movements.flags`.
- **~10 ESA-violation flags** where the published roster would breach BC rest periods, tagged `ESA_VIOLATION_PROJECTED` in `shifts.flags`.

## Four challenge angles — v1 demo target and v2 stretch

Pick one. Go deep. The v1 target is what you need to demo Sunday. The v2 stretch is what a real pilot would look like.

### Angle 1 — Housekeeping copilot
**v1 demo target:** A single-screen tool that shows the housekeeping supervisor the top 3 priority rooms at 7 AM, with a one-line reason for each (e.g., "accessible room — guest with mobility flag arriving at 2 PM"). Accept or override each priority. Beat the rule-based baseline on time-to-first-ready-room.
**v2 stretch:** Add supply prediction (flag when a cart will run short based on today's turnover load), anomaly detection (flag rooms that are taking significantly longer than expected), and real-time status sync.

### Angle 2 — Demand-aware staffing
**v1 demo target:** Take the published next-week roster. Show whether it matches the booking-pipeline demand for each department on each day. Propose the one shift change with the highest impact on the gap. Explain the cost. Bonus: flag staff members with elevated no-show risk based on historical patterns in `shifts.no_show_flag` — a supervisor who finds out at 7 AM that two attendants likely won't show is in a very different position than one who finds out at 7:15 AM when the attendants don't call.
**v2 stretch:** Full shift-generation from the booking pipeline, ESA-compliant, with fairness constraints (rotating weekend assignments, hours parity). An optimizer that proposes the cheapest legal roster that meets demand.

### Angle 3 — Channel parity and rate sanity monitor
**v1 demo target:** Detect the parity breaches seeded in the dataset. For each breach, show: which channel, what rate, which contract type is breached, and the recommended rate move to close it.
**v2 stretch:** Real-time monitoring that catches a parity drift within 30 minutes of the OTA update causing it. Sends an alert to the revenue manager with a one-click fix, not a report.

### Angle 4 — Inventory-aware F&B operations
**v1 demo target:** For each of the next 7 days, show which items are at risk of hitting a par-level breach before the next delivery, based on occupancy forecast + historical consumption patterns. Output: a one-page "this week's risk items" for the F&B director.
**v2 stretch:** Full inventory replenishment recommendation tied to the event calendar, weather, and day-part demand patterns. Connects to the purchasing workflow so the F&B director can act on the recommendation directly.

## Operational constraints your solution must respect

Judges will check at least one.

1. **BC labour standards.** A scheduler that proposes a roster violating minimum rest periods (8 hours between shifts), maximum daily hours, or overtime thresholds has a bug. Surface violations as hard stops with override-with-reason. Do not let them pass silently.
2. **Room sellability.** A room with `housekeeping.status = completed` is NOT sellable until `inspection.status = passed`. This is not a preference — it is the operational reality that the Empress room-not-ready incident illustrates. Enforce it.
3. **Cold-chain F&B.** Items with `cold_chain_required = true` must stay in cold-chain locations. A routing shortcut is a food-safety incident with regulatory consequences.
4. **Parity contracts.** Rate recommendations that would breach a parity obligation must name the breach and the contract type. A tool that recommends a rate move that kills your Expedia contract is not helpful.
5. **Cognitive load.** A boutique hotel supervisor has 8 things on her mind at 7 AM. One clear priority panel beats seven charts. Build for the person, not the investor demo.

## Suggested tech stack

- **Data:** pandas or duckdb. The golden join is large but laptop-friendly.
- **Forecasting:** Prophet or XGBoost for demand. Keep it interpretable — operators don't trust black boxes.
- **Optimization:** Google OR-Tools for shift assignment as a constraint satisfaction problem. Open-source, free.
- **UI:** Streamlit for fast, Next.js for polished. The workstation surface matters as much as the model.
- **LLM layer (optional):** Small models (Claude Haiku, GPT-4o-mini) for the "explain why room 312 is first" plain-language overlay. Don't make the LLM do the math.
- **pytest:** Tests that prove your ESA gates reject illegal rosters and cold-chain gates reject misrouted items.

## Where to go from here

- Open `notebooks/00_quickstart.ipynb` and run it end to end.
- Read `docs/erd.mmd` for the full data model.
- Read `dictionary/fields.csv` for exact field semantics and valid enumerations.
- Check the top-level `docs/submission-checklist.md` for what judges expect Sunday.

Build something a 6:45 AM housekeeping supervisor would actually open.
