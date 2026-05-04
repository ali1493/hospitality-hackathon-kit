"""
BuildersVault Hospitality Hackathon — Track 2 (Guest Lifecycle Integration)
Synthetic data generator — v2 scaffold.

STATUS: Scaffold only. Full generator is in development (~3 weeks engineering).
This file documents the target output and exits cleanly.

Target output when complete:
  - 8 Parquet files in data/raw/:
      guests, guest_preferences, stays, fb_receipts,
      spa_appointments, surveys, reviews, post_stay_events
  - Supporting files:
      guest_identity_groundtruth.csv — cross-property dedup ground truth
  - 1 SQLite database at data/raw/track2.sqlite with views:
      v_guest_timeline — guests + stays + fb_receipts + spa + surveys + reviews + post_stay
      v_post_stay_funnel — post_stay_events with conversion attribution
  - 8 sample CSVs in data/sample/
  - Deterministic with seed=42

New in v2 — spa_appointments table:
  Modeled on Book4Time / SpaSoft schemas.
  Includes: treatment_type, therapist_id, product_sensitivity_flags,
            therapist_notes, appointment status.
  ~8,000 appointments across 24 months.
  ~15 sensitivity_missed ground truth flags seeded for scoring.

Ground truth seeded (see problem-framing.md):
  - ~80 cross-property duplicate guest pairs + ~30 decoy false positives
  - ~40 high-NPS no-follow-through cases
  - ~30 negative review themes mapped to Track 1 ops patterns (OPS_LINKED)
  - ~50 CASL opt-outs
  - ~25 high-LTV at-risk guests
  - ~15 spa sensitivity conflicts not carried forward

Cross-track integrity — CRITICAL:
  guests.guest_id must match bookings.guest_id in Track 1.
  stays.booking_id must match Track 1 bookings.booking_id.
  Both generators must share the same guest pool initialization (seed=42).
  The spa appointment therapist_id pool is internal to Track 2.

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
    print("BuildersVault Hospitality Hackathon — Track 2 Generator (v2)")
    print("=" * 70)
    print()
    print("STATUS: Scaffold only. Full data generation is in development.")
    print()
    print("When complete, this script will produce:")
    print(f"  Parquet files    → {DATA_RAW}")
    print(f"  SQLite database  → {DATA_RAW / 'track2.sqlite'}")
    print(f"  Sample CSVs      → {DATA_SAMPLE}")
    print(f"  Ground truth     → {DATA_SAMPLE / 'guest_identity_groundtruth.csv'}")
    print()
    print("New in v2: spa_appointments table (Book4Time / SpaSoft schema shape).")
    print("Includes product_sensitivity_flags — a safety constraint, not a preference.")
    print()
    print("Cross-track note (CRITICAL):")
    print("  guests.guest_id must match Track 1 bookings.guest_id.")
    print("  stays.booking_id must match Track 1 bookings.booking_id.")
    print("  Both generators must share the same guest pool seed.")
    print()
    print("Target completion: 3 weeks before event kickoff.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
