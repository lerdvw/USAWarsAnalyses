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
# Scales
# ---------------------------------------------------------------------------

# Eras, oldest first.
ERAS = [
    "Founding",
    "Expansion",
    "Imperial and World Wars",
    "Cold War",
    "Post-Cold War",
    "Post-9/11",
]

# A conflict's principal *stated* rationale. Assigning one is a judgment.
TYPES = ["Defensive", "Offensive", "Humanitarian", "Freedom of passage", "Other"]

# Authorization strength: a number that sorts, and the label shown for it.
LV_LABEL = {
    5: "Declared war",     # Congress declared war
    4: "Congress + UN",    # a statute and a Security Council resolution
    3: "Congress",         # a statute or joint resolution, even after the fact
    2: "UN only",          # a Security Council resolution, no statute
    1: "Standing law",     # an existing statute or AUMF, invoked again
    0: "Executive only",   # the President acting alone
}


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

# Every source a row cites, by number: (number, title, link or None).
REFS = [
    # 1-10: primary government and academic sources
    (1, "CRS, Costs of Major U.S. Wars (RS22926, Daggett, June 2010)",
        "https://www.everycrsreport.com/files/20100629_RS22926_c0d01061e4f8188ae928d0890ee9df2da193d06a.pdf"),
    (2, "Department of Veterans Affairs, America's Wars (casualty summary)",
        "https://department.va.gov/americas-wars/"),
    (3, "CRS, American War and Military Operations Casualties: Lists and Statistics (RL32492)",
        "https://www.congress.gov/crs-product/RL32492"),
    (4, "CRS, Instances of Use of United States Armed Forces Abroad, 1798-2023 (R42738)",
        "https://www.congress.gov/crs-product/R42738"),
    (5, "DoD Defense Casualty Analysis System (DCAS)",
        "https://dcas.dmdc.osd.mil/dcas/conflictCasualties/oir"),
    (6, "Brown University, Costs of War Project - Findings",
        "https://costsofwar.watson.brown.edu/findings"),
    (7, "Federal Reserve Bank of Minneapolis, Consumer Price Index 1800-",
        "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-"),
    (8, "US Bureau of Labor Statistics, Consumer Price Index news release",
        "https://www.bls.gov/news.release/cpi.htm"),
    (9, "NDU Press, The Human and Financial Costs of Operations in Afghanistan and Iraq",
        "https://ndupress.ndu.edu/Portals/68/Documents/Books/lessons-encountered/lessons-encountered_AnnexA.pdf"),
    (10, "Naval History and Heritage Command, Barbary Wars",
         "https://www.history.navy.mil/content/history/nhhc/browse-by-topic/wars-conflicts-and-operations/barbary-wars.html"),
    # 11-20: conflicts before 1945
    (11, "Britannica, Philippine-American War",
         "https://www.britannica.com/event/Philippine-American-War"),
    (12, "Naval History and Heritage Command, The Boxer Rebellion 1900-1901",
         "https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/early-20th-century-conflicts/boxer-rebellion.html"),
    (13, "Naval History and Heritage Command, The Occupation of Veracruz, 1914",
         "https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/early-20th-century-conflicts/veracruz-1914.html"),
    (14, "Smithsonian, The Forgotten Story of the American Troops Who Got Caught Up in the Russian Civil War",
         "https://www.smithsonianmag.com/history/forgotten-doughboys-who-died-fighting-russian-civil-war-180971470/"),
    (15, "USNI Naval History, U.S. Marines in Nicaragua, 1927-1932",
         "https://www.usni.org/magazines/naval-history-magazine/2021/december/us-marines-nicaragua-1927-1932"),
    (16, "Britannica, Seminole Wars", "https://www.britannica.com/topic/Seminole-Wars"),
    (17, "Britannica, Saint Clair's Defeat",
         "https://www.britannica.com/event/Saint-Clairs-Defeat"),
    (18, "Wikipedia, United States military casualties of war",
         "https://en.wikipedia.org/wiki/United_States_military_casualties_of_war"),
    (19, "Wikipedia, Great Sioux War of 1876",
         "https://en.wikipedia.org/wiki/Great_Sioux_War_of_1876"),
    (20, "Wikipedia, Nez Perce War", "https://en.wikipedia.org/wiki/Nez_Perce_War"),
    # 21-30: the Cold War
    (21, "Wikipedia, Mayaguez incident", "https://en.wikipedia.org/wiki/Mayaguez_incident"),
    (22, "Wikipedia, Cambodian campaign", "https://en.wikipedia.org/wiki/Cambodian_campaign"),
    (23, "Air & Space Forces Magazine, Airpower at the Bay of Pigs",
         "https://www.airandspaceforces.com/article/airpower-at-the-bay-of-pigs/"),
    (24, "Office of the Historian, Taiwan Strait Crises",
         "https://history.state.gov/milestones/1953-1960/taiwan-strait-crises"),
    (25, "CBS News, How many Americans died in Korea",
         "https://www.cbsnews.com/news/how-many-americans-died-in-korea"),
    (26, "Wikipedia, Pancho Villa Expedition",
         "https://en.wikipedia.org/wiki/Pancho_Villa_Expedition"),
    (27, "Wikipedia, United States occupation of Haiti",
         "https://en.wikipedia.org/wiki/United_States_occupation_of_Haiti"),
    (28, "Wikipedia, Timeline of United States military operations",
         "https://en.wikipedia.org/wiki/Timeline_of_United_States_military_operations"),
    (29, "Wikipedia, Dakota War of 1862", "https://en.wikipedia.org/wiki/Dakota_War_of_1862"),
    (30, "Wikipedia, Red Cloud's War", "https://en.wikipedia.org/wiki/Red_Cloud's_War"),
    # 31-45: 1980-2026
    (31, "DoD, Conduct of the Persian Gulf War: Final Report to Congress (1992)", None),
    (32, "CSIS, The War May Be Ending. What Did Epic Fury Cost?",
         "https://www.csis.org/analysis/war-may-be-ending-what-did-epic-fury-cost"),
    (33, "Military Times, 13 US troops killed, 346 wounded in Operation Epic Fury",
         "https://www.militarytimes.com/news/your-military/2026/04/08/pentagon-data-13-us-troops-killed-346-wounded-in-operation-epic-fury/"),
    (34, "CRS, U.S. Aircraft Combat Losses in Operation Epic Fury (IN12692)",
         "https://www.congress.gov/crs-product/IN12692"),
    (35, "USNI News, Pentagon Inspector General Report on Operation Epic Fury",
         "https://news.usni.org/2026/09/16/pentagon-inspector-general-report-on-operation-epic-fury"),
    (36, "Washington Examiner, Operation Southern Spear price tag up to $820 million",
         "https://www.washingtonexaminer.com/policy/defense/4669181/operation-southern-spear-latest-price-tag-820-million-drug-boats-quarter/"),
    (37, "USNI News, At Least 200 People Killed in U.S. Strikes on Suspected Drug Boats",
         "https://news.usni.org/2026/06/01/at-least-200-people-killed-in-u-s-strikes-on-suspected-drug-boats"),
    (38, "Costs of War, Budgetary Costs of U.S. Military Operations in Venezuela and the Caribbean",
         "https://costsofwar.watson.brown.edu/sites/default/files/Homestead%20and%20Kavanagh_Costs%20of%20War_Operations%20in%20Venezuela%20and%20Caribbean.pdf"),
    (39, "CNBC, Seven U.S. troops injured in Venezuela raid that captured Maduro",
         "https://www.cnbc.com/2026/01/07/us-venezuela-military-operation-maduro-injuries-casualties.html"),
    (40, "CTC West Point, An Assessment of Operation Rough Rider",
         "https://ctc.westpoint.edu/feature-commentary-an-assessment-of-operation-rough-rider/"),
    (41, "The Center Square, Operation Midnight Hammer likely cost taxpayers at least $200M",
         "https://www.thecentersquare.com/national/article_d8b141f3-4bfb-4832-bc6d-25fe5f86da66.html"),
    (42, "CRS, Assessing Recent U.S. Airstrikes in the Middle East Under the War Powers Framework (LSB11157)",
         "https://www.congress.gov/crs-product/LSB11157"),
    (43, "CRS, U.S. Conflict with Iran (R48887)", "https://www.congress.gov/crs-product/R48887"),
    (44, "U.S. Department of State, Operation Epic Fury and International Law",
         "https://www.state.gov/releases/office-of-the-legal-adviser/2026/04/operation-epic-fury-and-international-law"),
    (45, "Wikipedia, Operation Project Freedom",
         "https://en.wikipedia.org/wiki/Operation_Project_Freedom"),
    # 46-50: 2025-2026, continued
    (46, "Brookings, Making sense of the US military operation in Venezuela",
         "https://www.brookings.edu/articles/making-sense-of-the-us-military-operation-in-venezuela/"),
    (47, "H.Con.Res. 38, 119th Congress, and House Roll Call 85 (5 March 2026)",
         "https://www.congress.gov/bill/119th-congress/house-concurrent-resolution/38"),
    (48, "The Hill, House passes war powers resolution to limit military action in Iran",
         "https://thehill.com/homenews/house/6091940-house-iran-war-powers-resolution/"),
    (49, "CBS News, Senate votes down war powers resolution on drug boat strikes",
         "https://www.cbsnews.com/news/senate-war-powers-trump-venezuela-boat-strikes/"),
    (50, "WOLA, Killing Spree: Extrajudicial Executions in the U.S. Boat Strikes Campaign",
         "https://www.wola.org/analysis/killing-spree-extrajudicial-executions-in-the-u-s-boat-strikes-campaign/"),
]


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
    row["auth_label"] = LV_LABEL[row["auth_level"]]

# No misspelt era or type.
assert all(row["era"] in ERAS and row["conflict_type"] in TYPES for row in ROWS)
