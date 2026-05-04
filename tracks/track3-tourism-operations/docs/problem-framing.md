# Track 3: Tourism Operations

## The Problem

Victoria's whale watching and marine tour operators run the most weather-dependent, time-constrained business in the city's visitor economy. A marine tour operator running 6 daily departures during peak August has approximately 270 seats to fill per day. Bookings come through Viator, direct online, hotel concierge referrals, and walk-up. Revenue per departure: roughly $9,000 at an average ticket price of $200 for a 45-passenger vessel.

The constraint that makes this operationally hard: the ocean.

Environment Canada issues small craft advisories and gale warnings for the Salish Sea and Juan de Fuca Strait based on wind speed, swell height, and sea state. These advisories can change within hours. A captain who runs a departure into an advisory is in regulatory and safety violation. A captain who cancels unnecessarily has triggered 45–60 rebooking requests, a wave of Viator reviews, and a revenue hole she may not be able to fill on a shoulder-season day.

The decision — cancel, hold, or reshift — happens every operating morning at approximately 6 AM. There is no system for it. There is a weather app, a booking spreadsheet, and the captain's experience.

**Victoria's whale watching season runs April 1 to October 31** per major operators including Prince of Whales and Eagle Wing Tours. That is approximately 214 operating days per year, and on perhaps 30–40 of those days, this decision is genuinely hard — not obviously safe and not obviously dangerous. Those are the days the decision engine matters most.

## What the data represents

One synthetic Victoria marine tour operator with a mixed fleet of 20 vessels (catamarans and Zodiacs) operating from a combined departure point modeled on the Inner Harbour and Fisherman's Wharf. The operator runs multiple departure types: 3-hour whale watching (standard), 2-hour express, private Zodiac charter, and sunset tours.

Twenty-four months of operational data. Seasonal demand grounded in publicly sourced Destination Greater Victoria statistics — see `docs/overview.md` for the full seasonal model with monthly demand indices.

**The schema draws from:**

- **Booking channel shape:** Viator/TripAdvisor booking conventions (confirmed: Prince of Whales uses Viator for OTA distribution). Fields include booking_channel, viator_booking_id, party_size, lead_time_days, cancellation_policy.
- **Marine weather:** Environment Canada forecast schema (weather.gc.ca/marine). Fields include sea_state, swell_height_m, wind_speed_knts, visibility_km, advisory_level (none / small_craft / gale). Advisory levels matched to departure eligibility rules.
- **Guide certification:** Transport Canada certified marine naturalist requirements. Each vessel type requires a minimum certification level — tracked in `guide_shifts.certification_type`.
- **Vessel operations:** Standard BC coastal tour operator patterns. Vessel types: catamaran (45–60 passengers, semi-covered), Zodiac (12 passengers, open). Maintenance cycles tracked in `equipment_inventory`.

## Seasonal context — sourced numbers

Greater Victoria's visitor economy hit decade highs in 2025. August hotel occupancy reached 94.3% — the highest in 10 years. Victoria International Airport welcomed 227,000 passengers in August 2025 alone, up 11.3% year-over-year. The cruise sector brought over 1 million passengers beginning in April 2025. *(Destination Greater Victoria, September 2025 press release)*

This context matters for the dataset: the same Victoria visitors who are filling hotels in August are the primary market for whale watching departures. Tour booking volume is a same-day leading indicator for hotel afternoon F&B demand — the cross-dataset link between Track 3 and Track 1. A sold-out 2 PM whale watching departure means those 45 guests will be back at the Inner Harbour by 5 PM, likely headed to dinner at hotels near the harbour.

## Ground truth seeded for scoring

- **~150 weather-cancelled departures** seeded across the 24-month window, with `weather_marine.advisory_level` values at `small_craft` or `gale` within 6 hours of the departure slot. Tagged `WEATHER_CANCEL` in `tour_departures.flags`. A good decision engine correctly predicts cancellation-risk for the adjacent days where the advisory is borderline (advisory_level = small_craft but swell_height_m < 1.2).
- **~60 no-show pattern clusters** in `tour_bookings.no_show_flag` — concentrated in specific booking channels (same-day walk-up bookings have 3× the no-show rate of Viator advance bookings) and lead times (< 24 hours lead time = elevated no-show). Labeled by channel in `tour_bookings.no_show_risk_seed`.
- **~30 guide certification mismatches** in `guide_shifts` where the assigned guide does not hold the required certification for the vessel type. Tagged `CERTIFICATION_MISMATCH`. A correct scheduler catches all 30.
- **~15 maintenance overdue departures** — vessel with `equipment_inventory.next_service_due < tour_departures.departure_at` that still ran a trip. Tagged `MAINTENANCE_OVERDUE`. A safety-aware scheduler flags these as hard stops.
- **~60 confirmed cross-dataset hotel-tour matches** — in `cross_dataset_groundtruth.csv` with fuzzy match fields (name, date proximity, booking channel). ~340 additional unconfirmed candidate pairs for the matcher to score.

## Four challenge angles — with v1 and v2 targets

### Angle 1 — Weather-adjusted departure decision engine

The highest-value problem in this track. A 6 AM decision with $9,000–$36,000 of revenue at stake.

**v1 (demo Sunday):** For each upcoming departure in the next 48 hours, produce one of three recommendations: Go / Hold (monitor and decide by departure minus 2 hours) / Cancel. Include with each recommendation: (a) expected revenue at risk if cancel, (b) rebooking capacity available in earlier same-day departures, (c) the weather signal driving the recommendation, (d) the confidence level. Show the decision matrix for 5 upcoming departures with meaningfully different weather profiles. Beat a naive threshold baseline (cancel if advisory_level ≥ small_craft).

**v2 (real pilot):** Automated rebooking email draft generated for each guest in a cancelled departure — personalized by booking channel, party size, and availability of alternatives. Revenue impact dashboard updated in real time as the weather forecast changes. Feedback loop from captain's actual decision vs. model recommendation for model improvement over the season.

### Angle 2 — Capacity allocation across departure windows

**v1:** Given 6 departure windows and a day's worth of bookings on a high-demand Saturday in August, produce an optimized seat allocation across windows. Objective: maximize revenue AND minimize weather-cancellation risk (morning departures have lower advisory probability). Beat the naive first-come-first-served baseline on expected revenue (accounting for cancellation probability per window).

**v2:** Dynamic rebooking suggestions — when a high-demand morning fills, the system suggests what price discount on the 4 PM departure would still maximize total-day revenue.

### Angle 3 — Guide and vessel scheduling

**v1:** Given next week's departure schedule, produce a guide-to-vessel assignment that: (a) respects Transport Canada certification requirements per vessel type, (b) minimizes overtime cost, (c) flags any CERTIFICATION_MISMATCH risks before the schedule is published. Beat the kit's naive round-robin baseline on compliance score (percentage of assignments without a certification gap).

**v2:** Predictive guide availability model using shift history. Identifies guides with elevated no-show risk based on historical patterns in `guide_shifts.actual_start` vs. `guide_shifts.scheduled_start`.

### Angle 4 — Victoria visitor journey (cross-dataset identity resolution)

The most technically ambitious angle in the event. This is where Track 3 connects to Tracks 1 and 2.

**The problem:** The same tourist books a whale watch through Viator on Monday morning and checks into Oak Bay Beach Hotel on Monday afternoon. In the tour operator's system, she is a Viator booking reference. In the hotel's PMS, she is a Booking.com alias. No shared identifier exists. Neither operator knows the other has her.

**v1:** Using the labeled pairs in `cross_dataset_groundtruth.csv` as your scoring set, implement a fuzzy match between `tour_bookings.(guest_first_name, guest_last_name, departure_date)` and Track 1/Track 2 stays `(guest_first_name, guest_last_name, checkin_date)` within a ±2 day window. Report precision and recall against the 60 labeled true matches. Show 5 matched pairs with your confidence score and the fields that drove the match.

**v2:** Full cross-operator unified visitor profile: tour booking history + hotel stay history + spa appointments + post-stay reviews, joined by probabilistic identity. This profile doesn't exist in any real system in Victoria today. A working prototype of it is the highest-ceiling demo this event can produce.

## Operational constraints — judges will check at least one

1. **Weather hard stop.** A departure with `weather_marine.advisory_level = gale` must be flagged as a hard stop regardless of booking load or revenue at stake. A tool that recommends "Go" into a gale warning is a safety failure.
2. **Guide certification.** Scheduling must respect Transport Canada certification requirements per vessel type. An unqualified guide on a licensed vessel is a regulatory violation and a safety risk.
3. **Cross-dataset join honesty.** The fuzzy match must surface a confidence score for each pair — it must not assume a direct join. Show your precision and recall against the groundtruth, not just the matched pairs.
4. **Revenue impact visibility.** A cancellation recommendation without a revenue impact estimate and a rebooking plan is incomplete. The operator needs to know the cost of the decision before she makes it, not after.
5. **Operator time budget.** The captain makes this decision at 6 AM on a marine dock with variable connectivity. The tool must produce one clear recommendation with one reason in under 10 seconds. No dashboards, no loading spinners, no 40-widget screens.

## Suggested tech stack

- **Data:** pandas or duckdb. The departure_state golden join is large but laptop-friendly.
- **Forecasting:** Prophet (demand and weather trend), XGBoost (no-show prediction on tabular features)
- **Optimization:** Google OR-Tools for guide-vessel assignment as constraint satisfaction
- **Identity resolution:** rapidfuzz or fuzzy-wuzzy for name matching; Splink for the full probabilistic record linkage (visitor journey angle)
- **UI:** Streamlit — the 6 AM decision panel must be one recommendation, one reason, one action. Designed for a marine dock, not an office.
- **pytest:** Prove your gale-warning hard stop actually prevents a Go recommendation. Prove your certification check catches the 30 seeded mismatches.

## Where to go from here

- Open `notebooks/00_quickstart.ipynb` and run it end to end
- Read `docs/erd.mmd` for the full data model
- Read `dictionary/fields.csv` for field semantics, advisory_level values, and certification_type enumerations
- Read `docs/overview.md` for the full seasonal model and data sources
- Check `docs/submission-checklist.md` for Sunday's requirements

Build something a captain would trust at 6 AM with $36,000 at stake.
