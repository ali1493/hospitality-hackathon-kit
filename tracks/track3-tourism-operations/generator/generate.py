"""
BuildersVault Hospitality Hackathon — Track 3 (Tourism Operations)
Synthetic data generator — final scaffold.

STATUS: Scaffold only. Full generator in development (~4 weeks total engineering,
including 1 extra week for tourism seasonal model if operator data partner confirms).

Target output when complete:
  - 8 Parquet files in data/raw/:
      tour_operators, vessels, tour_departures, tour_bookings,
      guide_shifts, equipment_inventory, weather_marine,
      cross_dataset_groundtruth
  - 1 SQLite database at data/raw/track3.sqlite with views:
      v_departure_state — tour_departures + tour_bookings + weather_marine + guide_shifts
      v_daily_capacity  — seats_available vs. seats_booked by date and tour_type
  - 8 sample CSVs in data/sample/ (first 1000 rows each)
  - Deterministic with seed=42

Seasonal demand model — grounded in public data:
  Monthly demand index derived from Destination Greater Victoria statistics:
  - Aug 1.00 (94.3% hotel occupancy, 227k YYJ passengers — DGV Sept 2025)
  - Jul 0.95 (207k YYJ passengers)
  - Jun 0.80 (190k YYJ passengers)
  - May 0.55, Apr 0.35 (cruise season opens), Mar-Jan 0.15
  - Sep 0.65, Oct 0.40 (season ends Oct 31), Nov-Dec 0.10

Weather cancellation rate: estimated 10-15% shoulder months, 3-5% peak summer.
LABELED AS ESTIMATED in data documentation — not sourced from operator data.
Source if operator confirms: first question to ask is actual cancellation rate by month.

Seeded ground truth targets:
  - ~150 weather-cancelled departures (advisory_level = small_craft or gale)
  - ~60 no-show pattern clusters (walk-up and < 24hr lead time bookings)
  - ~30 guide certification mismatches (guide cert < vessel requirement)
  - ~15 maintenance overdue departures (next_service_due < scheduled_at)
  - ~400 cross-dataset candidate pairs, ~60 labeled true matches

Cross-track integrity — CRITICAL:
  cross_dataset_groundtruth.hotel_stay_id must reference valid stay_ids
  from Track 1 (stays.stay_id) and Track 2 (stays.stay_id).
  All three generators must share the same guest pool initialization (seed=42).
  The hotel_stay_id values in this file must match Track 1 and Track 2 output.

Target generation time: under 60 seconds (larger than Track 1/2 due to
weather time-series generation and cross-dataset groundtruth computation).
"""

import sys
from pathlib import Path

SEED = 42
TRACK_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = TRACK_DIR / "data" / "raw"
DATA_SAMPLE = TRACK_DIR / "data" / "sample"


def main() -> int:
    print("=" * 70)
    print("BuildersVault Hospitality Hackathon — Track 3 Generator")
    print("Tourism Operations — Synthetic Data Generator Scaffold")
    print("=" * 70)
    print()
    print("STATUS: Scaffold only. Full data generation is in development.")
    print()
    print("When complete, this script will produce:")
    print(f"  Parquet files    → {DATA_RAW}")
    print(f"  SQLite database  → {DATA_RAW / 'track3.sqlite'}")
    print(f"  Sample CSVs      → {DATA_SAMPLE}")
    print()
    print("Seasonal model grounded in:")
    print("  - Destination Greater Victoria press release Sept 25 2025")
    print("  - DGV Tourism Indicators Dashboard (destinationgreatervictoria.com)")
    print("  - Environment Canada marine forecast schema (weather.gc.ca/marine)")
    print()
    print("Weather cancellation rate: ESTIMATED 10-15% shoulder, 3-5% peak.")
    print("Label as estimated in your documentation. Not sourced from operator.")
    print()
    print("Cross-track note (CRITICAL):")
    print("  cross_dataset_groundtruth.hotel_stay_id must match Track 1 + Track 2.")
    print("  All three generators must share the same guest pool seed.")
    print()
    print("Tourism data partner outreach: Prince of Whales, Eagle Wing Tours.")
    print("If confirmed, actual cancellation rates replace the estimated values.")
    print()
    print(f"Target completion: ~4 weeks before event kickoff.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
