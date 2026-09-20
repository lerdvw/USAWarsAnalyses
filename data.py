# -*- coding: utf-8 -*-
"""
Every overt US conflict from 1775 to 2026, one record each: the single source
of truth for every table built from it.

The records are written with conflict() in ROWS below, oldest first. Fields
that follow from others (day counts, casualty totals, inflation) are added at
the bottom of the file.
"""

from datetime import date

# Conflicts still going are counted up to this day.
TODAY = date(2026, 9, 22)


# ---------------------------------------------------------------------------
# The conflicts
# ---------------------------------------------------------------------------


def conflict(name, theatre, start, end, era, presidents, conflict_type, reason, summary,
             auth_level, authority, auth_note, kia, deaths, wounded, losses_text,
             cost_m, cost_text, cost_year, cost_year_note, sources,
             combat_start=None, combat_end=None, combat=None, flag=""):
    """One conflict. ROWS passes every field by name:

    name, theatre         what it was called and where it was fought
    start, end            first and last day; end=None if it is still going
    era                   the period, e.g. "Cold War"
    presidents            who was in office while it ran
    conflict_type         its stated reason, classified: Defensive, Offensive,
                          Humanitarian, Freedom of passage or Other
    reason, summary       why it was fought, and what happened
    auth_level            authorization strength, 5 (declared war) down to
                          0 (the President acting alone)
    authority, auth_note  that authority in brief, and in full
    kia                   US dead from hostile action, plus missing
    deaths, wounded       all US dead, and all wounded
    losses_text           the losses in words, with their caveats
    cost_m, cost_text     net cost to US taxpayers in millions of dollars of
                          the time, and the same in words
    cost_year             the year whose dollars cost_m is in
    cost_year_note        why that year
    sources               the numbers of the sources it cites
    combat_start/end      when fighting began and ended, if not start and end
    combat                a fixed count of combat days, when dates can't give it
    flag                  † estimate, ‡ ongoing, § disputed

    A figure nobody knows is None; 0 means there were none.
    """
    return dict(locals())  # every argument, by name


ROWS = [
    # ---- Cold War, 1946-1989 ------------------------------------------------
    conflict(
        name="Eagle Claw",
        theatre="Iran hostage rescue",
        start=date(1980, 4, 24),
        end=date(1980, 4, 25),
        era="Cold War",
        presidents="Carter",
        conflict_type="Other",
        reason=(
            "Rescue the 52 American embassy staff held hostage in Tehran since "
            "November 1979."
        ),
        summary=(
            "Eight helicopters and six transports staged at a desert airstrip; three "
            "helicopters failed and the mission was aborted. As the force withdrew a "
            "helicopter collided with a tanker aircraft and eight men burned to death. "
            "The hostages were dispersed and held another nine months. The failure led "
            "to the creation of Special Operations Command."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Congress not consulted; War Powers report filed afterward.",
        kia=0,
        deaths=8,
        wounded=4,
        losses_text="8 killed and 4 injured, all in the collision at Desert One",
        cost_m=150,
        cost_text="About $150m (estimate, incl. aircraft lost)",
        cost_year=1980,
        cost_year_note="Year of the operation",
        sources=[4, 5],
        combat=1,
        flag="†",
    ),
]


# ---------------------------------------------------------------------------
# Derived fields
# ---------------------------------------------------------------------------


def derived(row):
    """Day counts, total casualties and whether the conflict is still going."""
    end = row["end"] or TODAY
    all_days = (end - row["start"]).days + 1
    if row["combat"] is not None:
        combat_days = row["combat"]
    elif row["combat_start"] or row["combat_end"]:
        first = row["combat_start"] or row["start"]
        last = row["combat_end"] or end
        combat_days = (last - first).days + 1
    else:
        combat_days = all_days
    if row["deaths"] is None and row["wounded"] is None:
        casualties = None
    else:
        casualties = (row["deaths"] or 0) + (row["wounded"] or 0)
    return {
        "all_days": all_days,
        "combat_days": combat_days,
        "casualties": casualties,
        "ongoing": row["end"] is None,
        "end_or_today": end,
    }


for number, row in enumerate(ROWS, 1):
    row["idx"] = number  # the # column
    row.update(derived(row))
