# -*- coding: utf-8 -*-
"""
Sanity checks for the dataset.

    python3 check.py

Prints a summary, then every failed check; exits with status 1 if any failed.
"""

import data
from data import ROWS

FAILED = []


def check(ok, message):
    """Record a failure; the run carries on, so every failure gets listed."""
    if not ok:
        FAILED.append(message)


# ---------------------------------------------------------------------------
# The dataset
# ---------------------------------------------------------------------------

def rows():
    """Numbering, dates, day counts, and casualties that add up."""
    check([row["idx"] for row in ROWS] == list(range(1, len(ROWS) + 1)), "# does not run 1..n")
    for row in ROWS:
        name = row["name"]
        check(row["end"] is None or row["end"] >= row["start"], f"{name}: ends before it starts")
        check(0 <= row["combat_days"] <= row["all_days"], f"{name}: more combat days than conflict days")
        if row["casualties"] is not None:
            check(row["casualties"] == (row["deaths"] or 0) + (row["wounded"] or 0),
                  f"{name}: casualties are not deaths plus wounded")
    ongoing = sum(row["ongoing"] for row in ROWS)
    print(f"rows            {len(ROWS)}, {ongoing} ongoing")


if __name__ == "__main__":
    rows()
    for message in FAILED:
        print("FAIL", message)
    print("\nall checks pass" if not FAILED else f"\n{len(FAILED)} check(s) failed")
    raise SystemExit(1 if FAILED else 0)
