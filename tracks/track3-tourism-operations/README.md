# Track 3: Tourism Operations

A Victoria whale watching operator runs 6 daily departures on a peak summer day. At 6 AM, the captain checks Environment Canada's marine forecast and sees a small craft advisory posted for 2 PM. She has 180 bookings across four afternoon departures — roughly $36,000 of scheduled revenue. She must decide: cancel now (90 rebooking emails, refund processing, Viator reviews), wait and see if the advisory lifts (safety and regulatory risk), or move guests to morning slots already approaching capacity. She makes a version of this decision every operating day from April to October using a weather app and a spreadsheet.

That is the Track 3 problem. A financially significant, time-sensitive, safety-constrained decision made daily by every marine tour operator in Victoria — without any decision-support tooling.

**Your job: build the tool that gives her a defensible, revenue-aware answer at 6 AM.**

## Quickstart

```bash
pip install -r requirements.txt
python tracks/track3-tourism-operations/generator/generate.py
jupyter lab tracks/track3-tourism-operations/notebooks/00_quickstart.ipynb
```

> **Status:** Generator in development. Seasonal model grounded in public DGV data. ERD, field dictionary, and problem framing are final. Tourism data partner outreach in progress — Prince of Whales, Eagle Wing Tours.

## Data at a glance

| Table | Target rows | What it is |
|---|---|---|
| tour_operators | 1 | Victoria marine tour operator profile (20-vessel fleet) |
| vessels | 20 | Vessel inventory: capacity, type (catamaran/Zodiac), certification, maintenance schedule |
| tour_departures | ~8,760 | Departure slots across 24 months: 6 daily × operating days. Weather cancel flag, advisory level, actual vs. scheduled. |
| tour_bookings | ~48,000 | Individual bookings: party_size, booking_channel, lead_time_days, no_show_flag, rebooking_id |
| guide_shifts | ~5,200 | Guide scheduling: guide_id, vessel_id, certification_type, scheduled vs. actual |
| equipment_inventory | ~2,400 | Safety gear inspections: vessel_id, safety_gear_type, pass/fail, next_service_due |
| weather_marine | ~730 | Daily: sea_state, swell_height_m, wind_speed_knts, visibility_km, advisory_level |
| cross_dataset_groundtruth | ~400 | Fuzzy-match candidates between tour bookings and hotel stays. ~60 confirmed true matches labeled. |

## Domain anchors

- **Tour booking:** Viator / FareHarbor / Rezdy booking channel structure — Prince of Whales confirmed using Viator for OTA distribution
- **Marine weather:** Environment Canada forecast schema (weather.gc.ca/marine) — small craft advisory and gale warning levels for Salish Sea and Juan de Fuca Strait
- **Guide certification:** Transport Canada certified marine naturalist requirements
- **Vessel operations:** Standard BC coastal marine tour operator operational patterns
- **Seasonal demand:** Grounded in DGV public data — see `docs/overview.md` for full seasonal model

## Seasonal demand model

Sourced from Destination Greater Victoria public data:

| Month | Demand index | Approx. daily departures at capacity |
|---|---|---|
| Jan–Mar | 0.15 | 1–2 |
| Apr | 0.35 | 3–4 (cruise season opens) |
| May | 0.55 | 4 |
| Jun | 0.80 | 5 |
| Jul | 0.95 | 5–6 |
| Aug | 1.00 | 6 (full capacity — 94.3% hotel occupancy in Aug 2025) |
| Sep | 0.65 | 4–5 |
| Oct | 0.40 | 2–3 (season ends Oct 31) |
| Nov–Dec | 0.10 | 1 (minimal) |

Weather cancellation rate: **estimated 10–15% shoulder season, 3–5% peak summer.** Labeled as estimated in documentation — not sourced from operator data.

## Golden join

`tour_departures ⋈ tour_bookings ⋈ weather_marine ⋈ guide_shifts` filtered by departure date and vessel. Notebook cell 6 builds this as `departure_state`. SQLite view: `v_departure_state`. Start here.

## Cross-dataset join — technically honest

**There is no direct foreign key between `tour_bookings` and hotel stays (Track 1/Track 2).** A Viator booking and a Booking.com hotel reservation share no common identifier in any real system. The cross-dataset join is a probabilistic fuzzy match on:

```
(guest_first_name, guest_last_name, tour_departure_date, hotel_checkin_date)
```

Where hotel_checkin_date falls within ±2 days of the tour departure date, and name similarity exceeds a threshold. `cross_dataset_groundtruth.csv` contains ~400 candidate pairs, with ~60 confirmed true matches labeled. Builders must implement probabilistic matching — not assume a clean join. This is the Victoria visitor journey identity resolution problem.

## Seeded ground truth

- **~150 weather-cancelled departures** — `tour_departures.weather_cancel_flag = true`, with adjacent `weather_marine.advisory_level` values at `small_craft` or `gale`
- **~60 no-show patterns** — `tour_bookings.no_show_flag` clusters on specific booking channels and lead times. A good no-show predictor catches 70%+ at 48-hr booking horizon.
- **~30 guide certification gaps** — `guide_shifts` where the assigned guide's certification does not match the vessel type or tour license requirement. Tagged `CERTIFICATION_MISMATCH`.
- **~15 equipment inspection overdue flags** — vessel with `next_service_due < departure_date` that still ran a departure. Tagged `MAINTENANCE_OVERDUE`.
- **~60 confirmed cross-dataset hotel/tour matches** — in `cross_dataset_groundtruth.csv`.

## Four challenge angles — pick one

### Angle 1 — Weather-adjusted departure decision engine
**v1 (demo Sunday):** For each upcoming departure in the next 48 hours, produce a recommendation: Go / Hold (monitor) / Reshift (move to earlier departure) / Cancel. Include: expected revenue at risk, rebooking capacity available, advisory forecast trend. Show the decision for 5 upcoming departures with different weather profiles.
**v2 (real pilot):** Automated rebooking email draft per guest on cancellation. Revenue impact dashboard. Feedback loop from past cancellation decisions to model improvement.

### Angle 2 — Capacity allocation
**v1:** Given 6 departure windows and 200 total bookings on a high-demand day, produce the optimal seat allocation across windows that maximizes revenue and minimizes cancellation risk from weather patterns. Show the allocation vs. the naive first-come-first-served baseline.
**v2:** Dynamic pricing recommendation per departure window based on fill rate and weather forecast.

### Angle 3 — Guide and vessel scheduling
**v1:** Given next week's departure schedule, produce a guide-to-vessel assignment that respects certification requirements, minimizes overtime cost, and flags any `CERTIFICATION_MISMATCH` risks. Beat the kit's naive round-robin baseline.
**v2:** Predictive guide availability model using shift history and no-show patterns.

### Angle 4 — Victoria visitor journey (cross-dataset)
**v1:** Using the `cross_dataset_groundtruth.csv` as your scoring set, implement a fuzzy match between tour bookings and hotel stays. Report precision and recall against the 60 labeled true matches. Show 5 matched pairs with your confidence score.
**v2:** Full cross-operator guest profile: booking history at the tour operator + stay history at the hotel + spa appointments + post-stay reviews, unified by probabilistic identity. This is the highest-ceiling angle in the entire event.

## Constraints — judges will check at least one

1. Weather decisions must show revenue impact per option — not just binary cancel/go
2. Transport Canada certification requirements must be respected in guide scheduling
3. Cross-dataset fuzzy match must surface a confidence score — no fake direct joins
4. A departure with `weather_marine.advisory_level = gale` must flag as a hard stop regardless of booking load

## Suggested tech

- pandas or duckdb (departure state golden join)
- Prophet or XGBoost (demand and no-show forecasting)
- fuzzy-wuzzy or rapidfuzz (name matching for cross-dataset join)
- Splink (probabilistic record linkage for the visitor journey angle)
- Google OR-Tools (guide-vessel assignment as constraint satisfaction)
- Streamlit (the 6 AM decision panel — one recommendation, one reason, one action)
- pytest (prove gale-warning hard stop actually prevents departure recommendation)

## Data sources

| Source | Used for |
|---|---|
| DGV press release Sept 25 2025 | Seasonal demand index (airport passengers, hotel occupancy) |
| Eagle Wing Tours — eaglewingtours.com | Year-round operations, Fisherman's Wharf, daily departure structure |
| Prince of Whales — princeofwhales.com | 95% sighting rate, Inner Harbour, Viator distribution confirmed |
| Viator / TripAdvisor | Booking channel structure for `tour_bookings.booking_channel` |
| Environment Canada marine forecast | `weather_marine` table schema, advisory_level field conventions |
| Transport Canada | Marine naturalist certification requirements |
