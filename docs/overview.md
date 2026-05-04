# Starter Kit Overview

## Why this kit exists

A builder who shows up Thursday evening and spends Friday morning reading documentation has already lost. The real work in a 3-day hackathon is talking to the operator during office hours, iterating on the feedback, and shipping something a GM would actually open Monday morning. This kit exists to compress setup from a day to an hour. You get data that carries the shape and messiness of real Victoria hospitality operations, three tracks with operator problem owners on stage Thursday night, a baseline notebook that runs out of the box, and a Streamlit scaffold you can extend or discard.

## The integration thesis

This event is not about building AI features for hospitality. It is about solving one specific, verified problem: **Victoria's mid-market operators run tools that do not share data with each other, and that fragmentation costs them money and guests every single day.**

The housekeeping board does not know the arrival manifest. The Oracle CRM guest profile does not reach the front desk agent at check-in when the booking came through an OTA alias. The spa booking system is a completely separate platform — the therapist does not know whether the client booked a harbour tour this morning or has stayed at the hotel four times this year. The tour operator's booking platform and the hotel's PMS have never spoken. The tools are not bad. The connections don't exist.

This is not a technology problem. It is an integration problem.

## Kit status at publication

| Asset | Status |
|---|---|
| Three-track structure and scope | Locked |
| Problem framings (all 3 tracks) | Final |
| Field dictionaries (all 3 tracks) | Final |
| ERDs (all 3 tracks) | Final |
| Track 1 synthetic data generator | In development |
| Track 2 synthetic data generator | In development |
| Track 3 synthetic data generator | In development — tourism seasonal model grounded in public DGV data |
| Baseline notebooks | In development |
| Streamlit explorer | In development |
| Oak Bay Beach Hotel — data partner | In active outreach |
| Prince of Whales / Eagle Wing Tours — tourism data | In active outreach |
| Venue | In active outreach — Oak Bay Beach Hotel preferred |
| Judges | In recruitment — 4 seats, one hospitality, three different domains |

Target dataset completion: 3 weeks before kickoff. Tourism dataset adds ~1 week if operator data partner confirms.

## What "real-world-shaped" means

The datasets are synthetic but carry the schema shape of real systems used by Victoria operators:

- **PMS:** Cloudbeds / Mews / Opera reservation lifecycle and room status conventions
- **Guest CRM:** Oracle CRM hospitality guest object structure — confirmed at Oak Bay Beach Hotel. Richer profile shape than generic mid-market CRM.
- **POS:** Silverware POS — confirmed at Oak Bay Beach Hotel. Used for The Dining Room, Snug Pub, FARO Pizza, minibar, and banquet.
- **F&B/ERP:** NetSuite — confirmed at Oak Bay Beach Hotel. Par-level management, purchasing, cost of goods.
- **Housekeeping:** HotSOS / Quore turnover lifecycle conventions
- **Channel management:** SiteMinder / RateGain OTA sync and parity event shapes
- **Spa:** Book4Time / SpaSoft appointment schemas — first BV hackathon kit to include spa appointment data
- **Tour booking:** Viator / Rezdy / FareHarbor booking channel structure — confirmed Prince of Whales uses Viator for OTA distribution
- **Marine weather:** Environment Canada marine forecast schema (weather.gc.ca/marine) — small craft advisory and gale warning levels for Salish Sea and Juan de Fuca Strait
- **Post-stay CRM:** Revinate / Cendyn / TrustYou post-stay engagement and NPS schemas
- **Reviews:** Google / TripAdvisor / Booking.com review structures and Viator review formats

The messiness is intentional. OTA email aliases that don't match PMS guest names. Housekeeping events where someone forgot to tap Complete. Channel events arriving out of order due to OTA latency. Survey responses ranging from three-paragraph paragraphs to a single emoji. Two date formats per source system. The kind of data every real operator has and every demo hides.

## Scale

Sized to fit on a laptop. Baseline models train in under 30 seconds.

**Track 1 (Operations Workstation):** 2 hotel/venue properties × 24 months — ~30,000 bookings, ~57,000 room nights (100-room property at ~78% occupancy), ~80,000 housekeeping events, ~25,000 shift records, ~50,000 channel events, ~40,000 F&B/inventory movements, daily weather, Victoria events calendar.

**Track 2 (Guest Lifecycle Integration):** 5,000 guests × 24 months — ~30,000 stays, ~80,000 F&B receipts, ~8,000 spa appointments, ~12,000 post-stay surveys, ~15,000 reviews, ~50,000 post-stay engagement events. Cross-property identity groundtruth: 80 confirmed matches + 30 decoy false positives.

**Track 3 (Tourism Operations):** 1 marine tour operator × 24 months — ~8,760 departure slots, ~48,000 tour bookings, ~5,200 guide shifts, ~2,400 equipment inspections, ~730 daily marine weather records. Seasonal demand grounded in DGV public data. Cross-dataset fuzzy-match groundtruth: ~400 possible hotel-stay / tour-booking pairs, ~60 confirmed true matches labeled.

## Tourism seasonal model — data sources

The Track 3 synthetic demand index is grounded in publicly sourced Victoria visitor economy data:

| Month | Demand index | Source basis |
|---|---|---|
| Jan–Mar | 0.15 | Year-round confirmed but minimal demand |
| Apr | 0.35 | Cruise season opens — 1M+ cruise passengers in 2025 (DGV) |
| May | 0.55 | Airport passenger growth: June 2025 hit 190,000 passengers |
| Jun | 0.80 | Peak ramp — 190,000+ YYJ passengers (DGV press release Sept 2025) |
| Jul | 0.95 | 207,000+ airport arrivals; daily whale watch departures at capacity |
| Aug | 1.00 | 94.3% hotel occupancy — 10-year high; 227,000 airport passengers |
| Sep | 0.65 | Season declining — whale watch window closing Oct 31 |
| Oct | 0.40 | Tail end of season |
| Nov–Dec | 0.10 | Off-season; minimal marine tour activity |

Weather cancellation rate: estimated 10–15% of departures in shoulder months, 3–5% in peak summer. Based on Salish Sea small craft advisory frequency from Environment Canada marine data. **Labeled as estimated in dataset documentation** — not sourced from operator data. If Prince of Whales or Eagle Wing confirms as a data partner, this becomes sourced.

## The cross-dataset join — technically honest

There is no direct foreign key between Track 3 tour bookings and Track 1/Track 2 hotel stays. In real systems a Viator booking and a Booking.com hotel reservation share no common identifier. The cross-dataset join is a probabilistic fuzzy match on `(guest_name, arrival_date, booking_source)`. This is intentional. It is the Victoria visitor journey identity resolution problem in its most technically interesting form — the same challenge as Track 2's guest dedup, applied cross-operator. Builders must implement probabilistic matching, not assume a clean join.

## What you are expected to ship Sunday

A working demo. A public GitHub repo. A 1-page technical summary. An operator-fit statement. A constraints statement. See `docs/submission-checklist.md`.

## IP and the SOW pipeline

Builders own everything they build. BuildersVault does not claim ownership. Operator partners may express interest in piloting through the BV SOW pipeline. BV earns a 10% referral fee on signed, paid engagements — disclosed to operators at introduction. Final IP/SOW terms published on registration page before kickoff.
