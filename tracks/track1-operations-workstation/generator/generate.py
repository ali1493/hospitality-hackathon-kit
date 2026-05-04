"""
BuildersVault Hospitality Hackathon — Track 1 (Operations Workstation)
Synthetic data generator — v2 scaffold.

STATUS: Scaffold only. Full generator is in development (~3 weeks engineering).
This file documents the target output and exits cleanly.

Target output when complete:
  - 8 Parquet files in data/raw/:
      properties, rooms, bookings, stays, housekeeping_events,
      shifts, channel_events, inventory_movements,
      weather_daily, events_calendar
  - 1 SQLite database at data/raw/track1.sqlite with views:
      v_room_state — bookings + stays + rooms + housekeeping_events (golden join)
      v_shift_demand — shifts vs. demand by department and date
  - 8 sample CSVs in data/sample/ (first 1000 rows each)
  - Deterministic with seed=42

Property profiles:
  - PROP-001: ~100-room boutique hotel with restaurant, pub, minibar, spa, event space
  - PROP-002: event venue with full F&B (banquet + concession)

Seeded ground truth (see problem-framing.md):
  - ~50 channel parity violations
  - ~30 cleaning-time anomalies
  - ~20 over-staffing days + ~20 under-staffing days
  - ~15 F&B inventory stockout events
  - ~10 ESA-violation flags on the published roster

Cross-track integrity note:
  bookings.guest_id must match guests.guest_id in Track 2.
  Both generators must be run from the same shared guest pool seed.

Target generation time: under 30 seconds on a modern laptop.
"""

import sys
from pathlib import Path

SEED = 42
TRACK_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = TRACK_DIR / "data" / "raw"
DATA_SAMPLE = TRACK_DIR / "data" / "sample"


def main() -> int:
    print("=" * 70)
    print("BuildersVault Hospitality Hackathon — Track 1 Generator (v2)")
    print("=" * 70)
    print()
    print("STATUS: Scaffold only. Full data generation is in development.")
    print()
    print("When complete, this script will produce:")
    print(f"  Parquet files    → {DATA_RAW}")
    print(f"  SQLite database  → {DATA_RAW / 'track1.sqlite'}")
    print(f"  Sample CSVs      → {DATA_SAMPLE}")
    print()
    print("Property profiles:")
    print("  PROP-001 — boutique hotel (~100 rooms, restaurant, pub, spa, event space)")
    print("  PROP-002 — event venue with F&B (banquet + concession)")
    print()
    print("Cross-track note: guest_id values must match Track 2.")
    print("Run both generators from the same guest pool seed.")
    print()
    print("Target completion: 3 weeks before event kickoff.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
