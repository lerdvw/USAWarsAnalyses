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

    conflict(
        name="Gulf of Sidra Incident",
        theatre="Libya, Su-22 shootdown",
        start=date(1981, 8, 19),
        end=date(1981, 8, 19),
        era="Cold War",
        presidents="Reagan",
        conflict_type="Freedom of passage",
        reason=(
            "Assert navigation rights in waters Libya claimed as territorial; US "
            "aircraft returned fire when engaged."
        ),
        summary=(
            "Two Navy F-14s shot down two Libyan Su-22s that fired on them during a "
            "freedom-of-navigation exercise in the gulf Qaddafi claimed as Libyan "
            "waters. The whole engagement lasted under a minute."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Standing rules of engagement during a freedom-of-navigation exercise."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=5,
        cost_text="Negligible",
        cost_year=1981,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Multinational Force in Lebanon",
        theatre="Beirut",
        start=date(1982, 8, 25),
        end=date(1984, 2, 26),
        era="Cold War",
        presidents="Reagan",
        conflict_type="Humanitarian",
        reason=(
            "Peacekeeping: oversee the PLO withdrawal from Beirut and stabilise the "
            "city after the Sabra and Shatila massacres."
        ),
        summary=(
            "Marines went in to supervise the PLO's evacuation, left, and returned "
            "after the massacres. As they were drawn into supporting the Lebanese "
            "government against Druze and Shia militias they became a target: the "
            "embassy was bombed in April 1983 and the Marine barracks in October, "
            "killing 241 in the deadliest day for the Corps since Iwo Jima. Reagan "
            "withdrew the force in February 1984."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Deployed under Article II; PL 98-119 authorised 18 months in October 1983 "
            "- the only pre-1991 use of War Powers Resolution s.5(b)."
        ),
        kia=256,
        deaths=266,
        wounded=169,
        losses_text=(
            "266 dead, 241 of them in the barracks bombing; roughly 169 wounded"
        ),
        cost_m=1500,
        cost_text="About $1.5bn (estimate)",
        cost_year=1983,
        cost_year_note="Midpoint of the deployment",
        sources=[4, 5],
        combat=60,
        flag="†",
    ),

    conflict(
        name="Urgent Fury",
        theatre="Grenada invasion",
        start=date(1983, 10, 25),
        end=date(1983, 12, 15),
        era="Cold War",
        presidents="Reagan",
        conflict_type="Offensive",
        reason=(
            "Stated: protect US medical students and restore order after a Marxist "
            "coup. OECS invitation cited; the UN General Assembly deplored it 108-9."
        ),
        summary=(
            "Six days after a hardline faction murdered Grenada's prime minister, "
            "7,000 US troops invaded, defeated the Grenadian army and Cuban "
            "construction workers, and evacuated the students. Planning was hasty and "
            "inter-service coordination poor; the operation spurred the "
            "Goldwater-Nichols reforms. It was the first major US combat operation "
            "since Vietnam."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="OECS invitation cited; UN General Assembly deplored it 108-9.",
        kia=19,
        deaths=19,
        wounded=116,
        losses_text="19 killed, 116 wounded",
        cost_m=76,
        cost_text="About $76m",
        cost_year=1983,
        cost_year_note="Year of the operation",
        sources=[4, 5],
        combat=4,
    ),

    conflict(
        name="El Dorado Canyon",
        theatre="Libya airstrikes",
        start=date(1986, 4, 15),
        end=date(1986, 4, 15),
        era="Cold War",
        presidents="Reagan",
        conflict_type="Offensive",
        reason=(
            "Retaliation for the Berlin discotheque bombing attributed to Libyan "
            "agents."
        ),
        summary=(
            "Air Force F-111s flying from Britain around France, which refused "
            "overflight, and Navy aircraft struck Tripoli and Benghazi. One F-111 was "
            "lost with its crew. Qaddafi's compound was hit; he survived. "
            "Libyan-sponsored attacks continued, including Pan Am 103 two years later."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Article 51 self-defence claimed after the Berlin discotheque bombing."
        ),
        kia=2,
        deaths=2,
        wounded=0,
        losses_text="2 killed, the lost F-111 crew",
        cost_m=100,
        cost_text="About $100m (estimate)",
        cost_year=1986,
        cost_year_note="Year of the operation",
        sources=[4, 5],
        flag="†",
    ),

    conflict(
        name="Earnest Will and Praying Mantis",
        theatre="Persian Gulf tanker escort",
        start=date(1987, 7, 24),
        end=date(1988, 9, 26),
        era="Cold War",
        presidents="Reagan",
        conflict_type="Freedom of passage",
        reason=(
            "Reflag and escort Kuwaiti tankers through the Gulf during the Iran-Iraq "
            "tanker war."
        ),
        summary=(
            "The largest naval convoy operation since World War II. An Iraqi Exocet "
            "hit the USS Stark before it began, killing 37; the frigate Samuel B. "
            "Roberts struck an Iranian mine in April 1988, and the Navy's retaliation, "
            "Praying Mantis, sank half of Iran's operational navy in a day. In July "
            "the cruiser Vincennes shot down Iran Air 655, killing 290 civilians."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Congress debated invoking the War Powers Resolution and never did.",
        kia=39,
        deaths=39,
        wounded=31,
        losses_text="39 dead, 37 of them aboard USS Stark; roughly 31 wounded",
        cost_m=1000,
        cost_text="About $1bn (estimate)",
        cost_year=1988,
        cost_year_note="Bulk of the operation",
        sources=[4, 5],
        combat=10,
        flag="†",
    ),

    conflict(
        name="Just Cause",
        theatre="Panama invasion",
        start=date(1989, 12, 20),
        end=date(1990, 1, 31),
        era="Cold War",
        presidents="G.H.W. Bush",
        conflict_type="Offensive",
        reason=(
            "Stated: protect US nationals, secure the canal treaties, arrest Noriega "
            "on drug charges and install the elected government. The OAS condemned it "
            "20-1."
        ),
        summary=(
            "Twenty-seven thousand troops attacked Panamanian Defence Force targets "
            "across the country in a single night. Noriega took refuge in the Vatican "
            "embassy and surrendered after ten days; he was tried in Miami. Several "
            "hundred Panamanian civilians died in the fighting in El Chorrillo. The "
            "elected government of Guillermo Endara was sworn in on a US base."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="OAS condemned it 20-1, the US the lone no vote.",
        kia=23,
        deaths=23,
        wounded=325,
        losses_text="23 killed, 325 wounded",
        cost_m=163,
        cost_text="About $163m",
        cost_year=1990,
        cost_year_note="Most costs fell in FY1990",
        sources=[4, 5],
        combat=5,
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
