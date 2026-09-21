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
# Inflation
# ---------------------------------------------------------------------------

# Costs are restated in the dollars of this month (CPI-U, 1982-84 = 100).
CPI_BASE = 334.980
CPI_BASE_LABEL = "August 2026"

# CPI-U by year, 1982-84 = 100, for every year a cost is dated to:
#   1913 on     BLS annual averages; 2026 is the mean of January to August.
#   1800-1912   Federal Reserve Bank of Minneapolis estimates (1967 = 100),
#               rebased here by multiplying by 9.9 / 29.7.
CPI = {
    # Expansion
    1847: 9.3,
    1858: 8.7,
    1862: 10.0,
    1863: 12.3,
    1864: 15.7,
    1865: 15.3,
    # Imperial and world wars
    1898: 8.3,
    1900: 8.3,
    1901: 8.3,
    1913: 9.9,
    1914: 10.0,
    1916: 10.9,
    1917: 12.8,
    1918: 15.1,
    1919: 17.3,
    1920: 20.0,
    1930: 16.7,
    1941: 14.7,
    1943: 17.3,
    1944: 17.6,
    1945: 18.0,
    # Cold War
    1950: 24.1,
    1952: 26.5,
    1953: 26.7,
    1955: 26.8,
    1958: 28.9,
    1961: 29.9,
    1962: 30.2,
    1965: 31.5,
    1966: 32.4,
    1968: 34.8,
    1970: 38.8,
    1975: 53.8,
    # 1980 onward
    1980: 82.4,
    1981: 90.9,
    1983: 99.6,
    1986: 109.6,
    1988: 118.3,
    1990: 130.7,
    1991: 136.2,
    1993: 144.5,
    1995: 152.4,
    1996: 156.9,
    1998: 163.0,
    1999: 166.6,
    2008: 215.303,
    2011: 224.939,
    2012: 229.594,
    2017: 245.120,
    2018: 251.107,
    2020: 258.811,
    2021: 270.970,
    2022: 292.655,
    2024: 313.689,
    2025: 321.943,
    2026: 330.1,
}

# Where each year's index comes from, in words for the deflator sheet.
CPI_BASIS = {
    "pre1913": (
        "Minneapolis Fed historical estimate (1967=100), rebased x9.9/29.7; the Fed "
        "says pre-1913 values 'should be considered estimates'"
    ),
    "bls": "BLS CPI-U annual average",
    2026: "Mean of published Jan-Aug 2026 months; partial-year estimate",
}


def cpi_basis(year):
    """Which series a year's CPI figure comes from, in words."""
    if year == 2026:
        return CPI_BASIS[2026]
    if year < 1913:
        return CPI_BASIS["pre1913"]
    return CPI_BASIS["bls"]


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
    # ---- Expansion, 1816-1897 -----------------------------------------------
    conflict(
        name="Mexican-American War",
        theatre="Texas, northern Mexico, California and Mexico City",
        start=date(1846, 4, 25),
        end=date(1848, 2, 2),
        era="Expansion",
        presidents="Polk",
        conflict_type="Offensive",
        reason=(
            "Stated: Mexican forces had attacked US troops on American soil. The "
            "disputed strip was claimed by both, and Polk had already resolved on "
            "acquiring California and New Mexico."
        ),
        summary=(
            "Polk sent Taylor's army into the disputed zone, and when Mexican cavalry "
            "attacked a patrol, told Congress that American blood had been shed on "
            "American soil. Taylor won in the north, Scott landed at Veracruz and took "
            "Mexico City, and the Treaty of Guadalupe Hidalgo transferred half of "
            "Mexico's territory to the US for $15m. Congressman Lincoln's 'spot "
            "resolutions' challenged Polk's account."
        ),
        auth_level=5,
        authority="Declared war",
        auth_note=(
            "Congress declared war on 13 May 1846, 174-14 and 40-2, after a two-hour "
            "debate; the declaration was bundled with the supply bill so that voting "
            "no meant refusing to supply troops already under fire."
        ),
        kia=1733,
        deaths=13_283,
        wounded=4152,
        losses_text=(
            "1,733 battle deaths; 11,550 other deaths, mostly disease; 4,152 wounded"
        ),
        cost_m=71,
        cost_text="$71m then-year (CRS)",
        cost_year=1847,
        cost_year_note="Peak year of war spending",
        sources=[1, 2],
        combat_end=date(1847, 9, 14),
    ),

    conflict(
        name="American Civil War",
        theatre="The Confederate States",
        start=date(1861, 4, 12),
        end=date(1865, 5, 26),
        era="Expansion",
        presidents="Lincoln, A. Johnson",
        conflict_type="Defensive",
        reason=(
            "Suppress the secession of eleven Southern states and preserve the Union; "
            "from 1863 also to end slavery."
        ),
        summary=(
            "The deadliest war in American history. After Fort Sumter, Lincoln called "
            "up the militia, blockaded Southern ports and suspended habeas corpus on "
            "his own authority, and Congress ratified it all in July. Four years of "
            "war ended with Lee's surrender at Appomattox; the last Confederate army "
            "surrendered in May. Modern demographic estimates put total deaths at "
            "620,000 to 750,000, above the official returns used here."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Lincoln acted under Article II for three months; Congress retroactively "
            "approved his acts in August 1861, and the Supreme Court upheld the "
            "blockade in the Prize Cases (1863). There was never a declaration of war, "
            "since the Union did not recognise the Confederacy as a state."
        ),
        kia=214_938,
        deaths=498_332,
        wounded=281_881,
        losses_text=(
            "Union: 140,414 battle deaths, 224,097 other deaths, 281,881 wounded. "
            "Confederate: 74,524 battle deaths and 59,297 other deaths on incomplete "
            "returns; wounded unknown. Both sides were Americans and both are counted"
        ),
        cost_m=3183,
        cost_text=(
            "$3,183m then-year for the Union (CRS). The Confederacy spent a further "
            "~$1,000m, not borne by US taxpayers and not counted"
        ),
        cost_year=1864,
        cost_year_note="Outlay-weighted: Union spending peaked FY1864-65",
        sources=[1, 2, 3],
        combat_end=date(1865, 4, 9),
        flag="†",
    ),

    conflict(
        name="Dakota War of 1862",
        theatre="Minnesota",
        start=date(1862, 8, 17),
        end=date(1862, 12, 26),
        era="Expansion",
        presidents="Lincoln",
        conflict_type="Defensive",
        reason=(
            "Suppress the Dakota uprising, which began after annuity payments the "
            "tribe depended on were withheld and traders refused credit during a "
            "famine."
        ),
        summary=(
            "Dakota warriors attacked settlements along the Minnesota River, killing "
            "several hundred settlers. State forces under Sibley defeated them at Wood "
            "Lake. A military commission sentenced 303 Dakota to death in trials "
            "lasting minutes; Lincoln reviewed the cases and commuted all but 38, who "
            "were hanged at Mankato - still the largest mass execution in US history."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "State militia and volunteers under the governor, with War Department "
            "support; no congressional action."
        ),
        kia=113,
        deaths=113,
        wounded=None,
        losses_text=(
            "77 soldiers and 36 militia and armed civilians killed; wounded not "
            "reliably tallied. Several hundred settlers were also killed"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1862,
        cost_year_note="No cost figure",
        sources=[29],
        flag="†",
    ),

    # ---- Imperial and world wars, 1898-1945 ---------------------------------
    conflict(
        name="Spanish-American War",
        theatre="Cuba, Puerto Rico, the Philippines and Guam",
        start=date(1898, 4, 21),
        end=date(1898, 12, 10),
        era="Imperial and World Wars",
        presidents="McKinley",
        conflict_type="Offensive",
        reason=(
            "Stated: liberate Cuba from Spanish rule and avenge the destruction of the "
            "USS Maine. The war also delivered an overseas empire."
        ),
        summary=(
            "The Maine exploded in Havana harbour in February 1898 - almost certainly "
            "an accident - and a press campaign and Congress pushed McKinley to war. "
            "Dewey destroyed the Spanish fleet at Manila Bay; the Army took Santiago; "
            "and the ten-week war ended with Spain ceding Puerto Rico, Guam and the "
            "Philippines and freeing Cuba. Disease killed five times as many Americans "
            "as combat."
        ),
        auth_level=5,
        authority="Declared war",
        auth_note=(
            "Congress declared war on 25 April 1898, backdated to 21 April, after "
            "passing the Teller Amendment disclaiming any intention to annex Cuba."
        ),
        kia=385,
        deaths=2446,
        wounded=1662,
        losses_text=(
            "385 battle deaths; 2,061 other deaths, mostly typhoid and yellow fever; "
            "1,662 wounded"
        ),
        cost_m=283,
        cost_text="$283m then-year (CRS)",
        cost_year=1898,
        cost_year_note="Year of the war",
        sources=[1, 2],
        combat_end=date(1898, 8, 13),
    ),

    conflict(
        name="Philippine-American War",
        theatre="The Philippine Islands",
        start=date(1899, 2, 4),
        end=date(1902, 7, 4),
        era="Imperial and World Wars",
        presidents="McKinley, T. Roosevelt",
        conflict_type="Offensive",
        reason=(
            "Suppress the Philippine Republic's resistance to American annexation "
            "after Spain ceded the islands."
        ),
        summary=(
            "Filipino forces that had fought Spain alongside the Americans turned "
            "against them when it became clear the US meant to keep the islands. "
            "Conventional defeat gave way to guerrilla war, concentration camps and "
            "reprisals on both sides. Roosevelt declared it over in 1902, though the "
            "Moro Rebellion in the south continued until 1913. Some 200,000 Filipino "
            "civilians died, mostly of disease and famine."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note=(
            "No separate authorisation. The Senate ratified the Treaty of Paris in "
            "February 1899 and the war was fought under the President's authority over "
            "the ceded territory; the Philippine Organic Act followed in 1902."
        ),
        kia=1020,
        deaths=4196,
        wounded=2930,
        losses_text=(
            "1,020 killed in action (some counts 1,500); 4,196 dead from all causes; "
            "2,930 wounded. The Moro Rebellion added several hundred more deaths to "
            "1913"
        ),
        cost_m=400,
        cost_text="About $400m then-year (contemporary estimate)",
        cost_year=1900,
        cost_year_note="Midpoint of the war",
        sources=[11, 18],
        flag="†",
    ),

    conflict(
        name="Boxer Rebellion",
        theatre="Tientsin and Peking, China",
        start=date(1900, 6, 20),
        end=date(1900, 9, 30),
        era="Imperial and World Wars",
        presidents="McKinley",
        conflict_type="Other",
        reason=(
            "Relieve the foreign legations besieged in Peking by the Boxers and Qing "
            "troops, and protect American nationals."
        ),
        summary=(
            "US Marines from the Philippines and the 9th Infantry joined an "
            "eight-nation relief force that fought through Tientsin and reached Peking "
            "in August, lifting the 55-day siege. The US then used its share of the "
            "indemnity to fund Chinese students' education in America. McKinley sent "
            "troops without consulting Congress, a precedent later presidents cited."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Ordered by McKinley during a congressional recess; no authorisation "
            "sought or given."
        ),
        kia=46,
        deaths=46,
        wounded=220,
        losses_text=(
            "Roughly 46 killed and 220 wounded across the Seymour expedition, "
            "Tientsin, Yangcun and Peking (compiled from engagement returns)"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1900,
        cost_year_note="No cost figure",
        sources=[12],
        combat_end=date(1900, 8, 15),
        flag="†",
    ),

    conflict(
        name="Occupation of Nicaragua",
        theatre="Nicaragua; Sandino insurgency 1927-33",
        start=date(1912, 8, 4),
        end=date(1933, 1, 2),
        era="Imperial and World Wars",
        presidents="Taft, Wilson, Harding, Coolidge, Hoover",
        conflict_type="Offensive",
        reason=(
            "Stated: protect American lives and property and guarantee a US-backed "
            "government. In practice, secure the canal route and American financial "
            "control."
        ),
        summary=(
            "Marines landed in 1912 to save the Conservative government from a revolt "
            "and stayed as a legation guard until 1925; they returned in 1926 to "
            "another civil war. Augusto Sandino's guerrillas fought them from 1927 "
            "until the last Marines left in January 1933, having trained the National "
            "Guard that Anastasio Somoza then used to seize power and murder Sandino."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="No congressional authorisation at any point in 21 years.",
        kia=47,
        deaths=136,
        wounded=66,
        losses_text=(
            "1926-33 campaign: 136 Marines died, 47 from hostile action (32 killed in "
            "action, 15 died of wounds); 66 wounded. The 1912 landing added a few more"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1930,
        cost_year_note="No cost figure",
        sources=[15, 18],
        combat_start=date(1927, 5, 1),
        combat_end=date(1933, 1, 2),
        flag="†",
    ),

    conflict(
        name="Occupation of Veracruz",
        theatre="Veracruz, Mexico",
        start=date(1914, 4, 21),
        end=date(1914, 11, 23),
        era="Imperial and World Wars",
        presidents="Wilson",
        conflict_type="Offensive",
        reason=(
            "Stated: obtain satisfaction for the arrest of US sailors at Tampico. In "
            "practice, stop a German arms shipment to Huerta and undermine his "
            "government."
        ),
        summary=(
            "Sailors and Marines seized the customs house and city in two days of "
            "street fighting. Wilson had asked Congress for approval the day before, "
            "and the House and Senate voted it the day after the landing. The "
            "occupation lasted seven months and helped topple Huerta, but it united "
            "Mexican factions against the US and was remembered there as an invasion."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Wilson requested authority on 20 April; the House approved 337-37 on the "
            "20th and the Senate 72-13 on the 22nd, after the landing had begun."
        ),
        kia=22,
        deaths=22,
        wounded=70,
        losses_text="22 killed, 70 wounded",
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1914,
        cost_year_note="No cost figure",
        sources=[13],
        combat=2,
    ),

    conflict(
        name="Occupation of Haiti",
        theatre="Haiti; Caco wars 1915 and 1918-20",
        start=date(1915, 7, 28),
        end=date(1934, 8, 1),
        era="Imperial and World Wars",
        presidents="Wilson, Harding, Coolidge, Hoover, F. Roosevelt",
        conflict_type="Offensive",
        reason=(
            "Stated: restore order after the mob killing of the president and protect "
            "foreign lives. In practice, secure US financial control and pre-empt "
            "German influence."
        ),
        summary=(
            "Marines landed the day after President Sam was dragged from the French "
            "legation and killed. They ran the country for 19 years through a client "
            "government, rewrote the constitution to permit foreign land ownership, "
            "and suppressed two Caco peasant rebellions, killing several thousand "
            "Haitians. Forced road-building labour under the corvee provoked the "
            "second rising. The occupation ended under Roosevelt's Good Neighbour "
            "policy."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "No congressional authorisation; a 1916 treaty ratified by the Senate "
            "regularised the financial control after the fact."
        ),
        kia=38,
        deaths=146,
        wounded=None,
        losses_text=(
            "146 Marines and sailors died over 19 years, roughly 38 from hostile "
            "action (estimate); wounded not reliably tallied"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1920,
        cost_year_note="No cost figure",
        sources=[27, 18],
        combat=720,
        flag="†",
    ),

    conflict(
        name="Occupation of the Dominican Republic",
        theatre="Dominican Republic",
        start=date(1916, 5, 15),
        end=date(1924, 9, 18),
        era="Imperial and World Wars",
        presidents="Wilson, Harding, Coolidge",
        conflict_type="Offensive",
        reason=(
            "Stated: end political chaos and enforce the customs receivership securing "
            "Dominican debt. In practice, install a compliant government."
        ),
        summary=(
            "When the Dominican government refused US demands, Marines occupied the "
            "country and the Navy ran it directly under a military governor. A "
            "guerrilla resistance in the east was suppressed over several years. The "
            "Marines built roads and a National Guard, which Rafael Trujillo commanded "
            "and then used to seize power in 1930."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="No congressional authorisation.",
        kia=None,
        deaths=144,
        wounded=None,
        losses_text=(
            "About 144 Marines died from all causes; hostile deaths and wounded not "
            "reliably separated in the surviving returns"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1920,
        cost_year_note="No cost figure",
        sources=[28, 18],
        combat=180,
        flag="†",
    ),

    conflict(
        name="Pancho Villa Expedition",
        theatre="Chihuahua, Mexico",
        start=date(1916, 3, 14),
        end=date(1917, 2, 7),
        era="Imperial and World Wars",
        presidents="Wilson",
        conflict_type="Defensive",
        reason=(
            "Capture or destroy Pancho Villa's force after his raid on Columbus, New "
            "Mexico killed 18 Americans on US soil."
        ),
        summary=(
            "Pershing led 10,000 troops 400 miles into Mexico without catching Villa. "
            "Two clashes with Mexican federal troops at Parral and Carrizal nearly "
            "caused a war with the Carranza government; Wilson mobilised 100,000 "
            "National Guardsmen to the border. The expedition withdrew as the US "
            "prepared to enter the European war. It was the Army's first use of "
            "aircraft and motor transport in the field."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Ordered by Wilson with Carranza's grudging acquiescence; no congressional "
            "action. The National Guard call-up used the 1916 National Defense Act."
        ),
        kia=68,
        deaths=65,
        wounded=67,
        losses_text=(
            "65 killed, 67 wounded, 3 missing and 24 captured across the raid and "
            "expedition"
        ),
        cost_m=None,
        cost_text=(
            "Not separately accounted; contemporary estimates ran to $130m with the "
            "border mobilisation"
        ),
        cost_year=1916,
        cost_year_note="No cost figure",
        sources=[26],
        combat=30,
        flag="†",
    ),

    conflict(
        name="World War I",
        theatre="Western Front, France; the Atlantic",
        start=date(1917, 4, 6),
        end=date(1918, 11, 11),
        era="Imperial and World Wars",
        presidents="Wilson",
        conflict_type="Defensive",
        reason=(
            "Stated: Germany's resumption of unrestricted submarine warfare against "
            "American ships and the Zimmermann telegram inviting Mexico to attack the "
            "US. Wilson framed it as making the world safe for democracy."
        ),
        summary=(
            "The US entered in April 1917 after three years of neutrality. Two million "
            "men of the American Expeditionary Forces reached France; they held at "
            "Belleau Wood and Chateau-Thierry, then fought the Meuse-Argonne "
            "offensive, the largest battle in US history, in the war's final seven "
            "weeks. The 1918 influenza killed almost as many soldiers as the Germans "
            "did. The Senate refused the treaty Wilson brought home."
        ),
        auth_level=5,
        authority="Declared war",
        auth_note=(
            "Congress declared war on Germany on 6 April 1917, 82-6 and 373-50, and on "
            "Austria-Hungary in December."
        ),
        kia=53_402,
        deaths=116_516,
        wounded=204_002,
        losses_text=(
            "53,402 battle deaths; 63,114 other deaths, mostly influenza; 204,002 "
            "wounded"
        ),
        cost_m=20_000,
        cost_text="$20,000m then-year (CRS; spending through 1921)",
        cost_year=1919,
        cost_year_note="Peak year of war spending",
        sources=[1, 2],
    ),

    conflict(
        name="Intervention in the Russian Civil War",
        theatre="Archangel and Murmansk; Siberia",
        start=date(1918, 9, 4),
        end=date(1920, 4, 1),
        era="Imperial and World Wars",
        presidents="Wilson",
        conflict_type="Other",
        reason=(
            "Stated: guard Allied war supplies at Archangel, rescue the Czech Legion "
            "and keep the Trans-Siberian Railway open. In practice the North Russia "
            "force fought the Bolsheviks under British command."
        ),
        summary=(
            "The 'Polar Bear' regiment from Michigan spent a winter fighting the Red "
            "Army 200 miles south of Archangel, months after the Armistice ended the "
            "war they had been sent to support, and near mutiny before withdrawal in "
            "mid-1919. The Siberian force guarded the railway, skirmished with "
            "partisans and Cossacks, and left in April 1920. Wilson never explained "
            "the mission to Congress."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Ordered by Wilson in an aide-memoire of July 1918; no congressional "
            "authorisation. Senate resolutions demanding withdrawal failed narrowly."
        ),
        kia=200,
        deaths=424,
        wounded=355,
        losses_text=(
            "North Russia: 109 killed in action, 35 died of wounds, about 30 missing, "
            "100 other deaths, 305 wounded. Siberia: 189 died from all causes. Roughly "
            "200 hostile deaths and missing in total (estimate)"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1919,
        cost_year_note="No cost figure",
        sources=[14, 18],
        combat_end=date(1919, 6, 30),
        flag="†",
    ),

    conflict(
        name="World War II",
        theatre="Europe, the Atlantic, the Pacific and Asia",
        start=date(1941, 12, 8),
        end=date(1945, 9, 2),
        era="Imperial and World Wars",
        presidents="F. Roosevelt, Truman",
        conflict_type="Defensive",
        reason=(
            "The Japanese attack on Pearl Harbor and the Philippines; Germany and "
            "Italy declared war on the US three days later."
        ),
        summary=(
            "Sixteen million Americans served. The US fought a two-ocean war, supplied "
            "the Allies through Lend-Lease, invaded North Africa, Italy and Normandy, "
            "drove across the Pacific island by island, and ended the war with two "
            "atomic bombs. It emerged as the strongest power on earth, with a "
            "permanent military establishment and global commitments it has kept ever "
            "since. The last war Congress declared."
        ),
        auth_level=5,
        authority="Declared war",
        auth_note=(
            "Congress declared war on Japan on 8 December 1941 (82-0, 388-1) and on "
            "Germany and Italy on 11 December (unanimous). Three further declarations "
            "followed in 1942."
        ),
        kia=291_557,
        deaths=405_399,
        wounded=670_846,
        losses_text="291,557 battle deaths; 113,842 other deaths; 670,846 wounded",
        cost_m=296_000,
        cost_text="$296,000m then-year (CRS)",
        cost_year=1944,
        cost_year_note="Outlay-weighted: spending peaked FY1944-45",
        sources=[1, 2],
    ),

    # ---- Cold War, 1946-1989 ------------------------------------------------
    conflict(
        name="Korean War",
        theatre="Korean peninsula",
        start=date(1950, 6, 25),
        end=date(1953, 7, 27),
        era="Cold War",
        presidents="Truman, Eisenhower",
        conflict_type="Defensive",
        reason=(
            "Repel North Korea's invasion of the South under a UN Security Council "
            "resolution, which the Soviet Union was boycotting and so could not veto."
        ),
        summary=(
            "Truman committed forces within days and called it a police action. "
            "MacArthur's landing at Inchon reversed the war; his drive to the Yalu "
            "brought China in and the front collapsed back to the 38th parallel, where "
            "it stayed for two years of attrition. The armistice, never a peace "
            "treaty, left the peninsula divided. The first war the US fought on UN "
            "rather than congressional authority."
        ),
        auth_level=2,
        authority="UN only",
        auth_note=(
            "UN Security Council Resolutions 83 and 84 (June-July 1950). Truman did "
            "not ask Congress and said he did not need to; Congress funded the war but "
            "never authorised it. The Supreme Court checked him in Youngstown (1952)."
        ),
        kia=33_739,
        deaths=36_574,
        wounded=103_284,
        losses_text=(
            "33,739 battle deaths; 2,835 other deaths in theatre; 103,284 wounded. The "
            "54,246 figure sometimes quoted included every service death worldwide in "
            "the period"
        ),
        cost_m=30_000,
        cost_text="$30,000m then-year (CRS)",
        cost_year=1952,
        cost_year_note="Peak year of war spending",
        sources=[1, 2, 25],
    ),

    conflict(
        name="First Taiwan Strait Crisis",
        theatre="Quemoy, Matsu and the Tachen Islands",
        start=date(1954, 9, 3),
        end=date(1955, 5, 1),
        era="Cold War",
        presidents="Eisenhower",
        conflict_type="Defensive",
        reason=(
            "Deter a Chinese assault on Taiwan and the offshore islands after the PLA "
            "began shelling Quemoy."
        ),
        summary=(
            "Eisenhower signed a defence treaty with Taiwan and asked Congress for "
            "advance authority to defend it, which it gave in the Formosa Resolution. "
            "The Seventh Fleet evacuated the Tachen Islands; Eisenhower and Dulles let "
            "it be known nuclear weapons were on the table. The shelling stopped in "
            "May 1955. No American forces engaged."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Formosa Resolution, January 1955 (410-3, 85-3): the first advance blanket "
            "authorisation Congress gave a president to use force at his discretion - "
            "the template for Tonkin and the AUMFs."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="No US casualties",
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1955,
        cost_year_note="No cost figure",
        sources=[24],
        combat=0,
    ),

    conflict(
        name="Second Taiwan Strait Crisis",
        theatre="Quemoy and Matsu",
        start=date(1958, 8, 23),
        end=date(1958, 12, 2),
        era="Cold War",
        presidents="Eisenhower",
        conflict_type="Defensive",
        reason=(
            "Deter a Chinese seizure of Quemoy under renewed bombardment, and keep it "
            "supplied."
        ),
        summary=(
            "China fired 400,000 shells at Quemoy in six weeks. The Seventh Fleet "
            "escorted Nationalist supply convoys to the three-mile limit; US aircraft "
            "supplied Sidewinder missiles, first used in combat here. The Joint Chiefs "
            "again discussed nuclear strikes. Beijing announced a ceasefire in "
            "October, then shelled on alternate days for twenty years. No US forces "
            "were hit."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note="Fought under the 1955 Formosa Resolution, still in force.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="No US casualties",
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1958,
        cost_year_note="No cost figure",
        sources=[24],
        combat=0,
    ),

    conflict(
        name="Lebanon Intervention",
        theatre="Beirut",
        start=date(1958, 7, 15),
        end=date(1958, 10, 25),
        era="Cold War",
        presidents="Eisenhower",
        conflict_type="Other",
        reason=(
            "Stated: protect American lives and support the Chamoun government against "
            "a Nasserist revolt after the Iraqi monarchy was overthrown."
        ),
        summary=(
            "Fourteen thousand Marines and soldiers landed on Beirut's beaches among "
            "the bathers and met no resistance. A political settlement replaced "
            "Chamoun with the army commander Chehab, and the force withdrew after "
            "three months. The first use of the Eisenhower Doctrine, which Congress "
            "had approved the year before."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note=(
            "Middle East Resolution (Eisenhower Doctrine), March 1957, authorising "
            "force against 'international communism' at a state's request."
        ),
        kia=1,
        deaths=1,
        wounded=5,
        losses_text=(
            "1 killed by a sniper, 5 wounded; a handful of accidental deaths are "
            "sometimes added"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1958,
        cost_year_note="No cost figure",
        sources=[28],
        combat=1,
    ),

    conflict(
        name="Bay of Pigs Invasion",
        theatre="Playa Giron, Cuba",
        start=date(1961, 4, 17),
        end=date(1961, 4, 20),
        era="Cold War",
        presidents="Kennedy",
        conflict_type="Offensive",
        reason=(
            "Overthrow Fidel Castro with a CIA-trained brigade of Cuban exiles, "
            "without visible US involvement."
        ),
        summary=(
            "Brigade 2506, 1,400 exiles trained in Guatemala, landed and was destroyed "
            "in three days when the expected uprising did not come and Kennedy "
            "withheld US air cover. Four Alabama Air National Guard pilots flying for "
            "the CIA were killed. Castro ransomed the prisoners for $53m in food and "
            "medicine; the fiasco pushed him toward Moscow and set up the missile "
            "crisis."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "A covert CIA operation approved by Eisenhower and Kennedy; Congress was "
            "not informed."
        ),
        kia=4,
        deaths=4,
        wounded=0,
        losses_text="4 US airmen killed; the brigade lost 118 dead and 1,200 captured",
        cost_m=46,
        cost_text="About $46m then-year (CIA operational budget)",
        cost_year=1961,
        cost_year_note="Year of the operation",
        sources=[23],
        flag="†",
    ),

    conflict(
        name="Cuban Missile Crisis",
        theatre="Naval quarantine of Cuba",
        start=date(1962, 10, 22),
        end=date(1962, 11, 20),
        era="Cold War",
        presidents="Kennedy",
        conflict_type="Defensive",
        reason=(
            "Force the removal of Soviet nuclear missiles from Cuba by a naval "
            "'quarantine' short of a declared blockade."
        ),
        summary=(
            "The closest the world has come to nuclear war. Kennedy rejected an air "
            "strike for a quarantine line 500 miles out; Soviet ships turned back. A "
            "U-2 was shot down over Cuba on 27 October and its pilot killed. "
            "Khrushchev withdrew the missiles in exchange for a no-invasion pledge and "
            "the secret removal of US missiles from Turkey. Strategic Air Command went "
            "to DEFCON 2 for the only time."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Joint Resolution on Cuba, 3 October 1962 (86-1, 384-7), authorising force "
            "to stop Cuban aggression and prevent an offensive Soviet capability; the "
            "quarantine was also framed under the OAS Rio Treaty."
        ),
        kia=1,
        deaths=1,
        wounded=0,
        losses_text=(
            "Major Rudolf Anderson, killed when his U-2 was shot down; several aircrew "
            "died in accidents during the alert"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1962,
        cost_year_note="No cost figure",
        sources=[28],
        combat=0,
    ),

    conflict(
        name="Vietnam War",
        theatre="South Vietnam, with air war over North Vietnam, Laos and Cambodia",
        start=date(1955, 11, 1),
        end=date(1975, 4, 30),
        era="Cold War",
        presidents="Eisenhower, Kennedy, L. Johnson, Nixon, Ford",
        conflict_type="Defensive",
        reason=(
            "Stated: defend South Vietnam against communist insurgency and North "
            "Vietnamese invasion, and hold the line of containment in Southeast Asia."
        ),
        summary=(
            "Advisers from 1955 became half a million troops by 1968. The Tonkin Gulf "
            "Resolution, passed on a disputed account of an attack, was the only "
            "authorisation. The Tet Offensive broke domestic support; Nixon withdrew "
            "while widening the war into Cambodia and Laos; the Paris accords ended US "
            "combat in January 1973 and Saigon fell in April 1975. Congress passed the "
            "War Powers Resolution over Nixon's veto in response."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "Gulf of Tonkin Resolution, August 1964 (416-0, 88-2), authorising 'all "
            "necessary measures'. Repealed in January 1971; the war continued for two "
            "more years on Article II and appropriations."
        ),
        kia=47_434,
        deaths=58_220,
        wounded=153_303,
        losses_text=(
            "47,434 battle deaths; 10,786 other deaths in theatre; 153,303 wounded "
            "requiring hospital care (a further 150,341 did not). Counted 1 November "
            "1955 to 15 May 1975"
        ),
        cost_m=111_000,
        cost_text="$111,000m then-year (CRS; DoD incremental cost)",
        cost_year=1968,
        cost_year_note="Peak year of war spending",
        sources=[1, 2, 3],
        combat_start=date(1964, 8, 5),
        combat_end=date(1973, 1, 27),
    ),

    conflict(
        name="Dominican Republic Intervention",
        theatre="Santo Domingo",
        start=date(1965, 4, 28),
        end=date(1966, 9, 21),
        era="Cold War",
        presidents="L. Johnson",
        conflict_type="Offensive",
        reason=(
            "Stated: protect American lives during a civil war. Johnson's real "
            "concern, stated within days, was to prevent 'another Cuba'."
        ),
        summary=(
            "Twenty-two thousand US troops landed to stop a revolt seeking to restore "
            "the elected president Juan Bosch, whom the military had deposed. The OAS "
            "was persuaded afterward to send a token inter-American force. Elections "
            "in 1966 installed Joaquin Balaguer, who ruled for most of the next three "
            "decades. Senator Fulbright's hearings on the episode began his break with "
            "Johnson over Vietnam."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "No congressional authorisation; the OAS endorsed the force a week after "
            "the landing."
        ),
        kia=27,
        deaths=44,
        wounded=172,
        losses_text="27 killed in action, 44 dead from all causes, 172 wounded",
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1965,
        cost_year_note="No cost figure",
        sources=[28],
        combat=30,
        flag="†",
    ),

    conflict(
        name="Korean DMZ Conflict",
        theatre="Demilitarised Zone, Korea",
        start=date(1966, 10, 5),
        end=date(1969, 12, 3),
        era="Cold War",
        presidents="L. Johnson, Nixon",
        conflict_type="Defensive",
        reason=(
            "Repel North Korean infiltration and ambushes along the DMZ, a campaign "
            "Pyongyang timed to the US commitment in Vietnam."
        ),
        summary=(
            "Three years of ambushes, raids and firefights along the armistice line, "
            "including the North Korean commando raid on the Blue House in Seoul and "
            "the seizure of the USS Pueblo in 1968, whose crew was held for eleven "
            "months. It is sometimes called the Second Korean War. The Pueblo has "
            "never been returned."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note=(
            "US forces served under the UN Command established in 1950; no separate "
            "authorisation."
        ),
        kia=43,
        deaths=43,
        wounded=111,
        losses_text=(
            "43 US soldiers killed, 111 wounded; the 82 Pueblo crew were held as "
            "prisoners"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1968,
        cost_year_note="No cost figure",
        sources=[28],
        combat=100,
        flag="†",
    ),

    conflict(
        name="Cambodian Campaign",
        theatre="Eastern Cambodia",
        start=date(1970, 4, 29),
        end=date(1970, 7, 22),
        era="Cold War",
        presidents="Nixon",
        conflict_type="Offensive",
        reason=(
            "Destroy North Vietnamese and Viet Cong sanctuaries and supply bases "
            "across the Cambodian border."
        ),
        summary=(
            "US and South Vietnamese forces crossed into Cambodia to attack base areas "
            "the secret bombing had failed to eliminate. Large stocks of supplies were "
            "captured but the sanctuaries were not destroyed. The invasion set off the "
            "largest protests of the war; National Guardsmen killed four students at "
            "Kent State. Congress responded with the Cooper-Church amendment cutting "
            "off funds for ground troops in Cambodia."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Ordered by Nixon under Article II without notice to Congress, which then "
            "legislated to bar future ground operations. Included in the Vietnam "
            "totals; shown separately because of its distinct authorisation history."
        ),
        kia=338,
        deaths=338,
        wounded=1525,
        losses_text="338 US killed, 1,525 wounded (included in the Vietnam War totals)",
        cost_m=None,
        cost_text="Within the Vietnam War figure",
        cost_year=1970,
        cost_year_note="No separate cost",
        sources=[22],
    ),

    conflict(
        name="Mayaguez Incident",
        theatre="Koh Tang island, Cambodia",
        start=date(1975, 5, 12),
        end=date(1975, 5, 15),
        era="Cold War",
        presidents="Ford",
        conflict_type="Other",
        reason=(
            "Recover the container ship SS Mayaguez and its crew, seized by the Khmer "
            "Rouge in international waters two weeks after the fall of Saigon."
        ),
        summary=(
            "Marines assaulted Koh Tang island, where the crew was thought to be, and "
            "met heavy fire; three helicopters were shot down. The crew had already "
            "been released by boat and was recovered by a destroyer while the battle "
            "continued. Three Marines were left behind alive on the island and later "
            "executed. The last names on the Vietnam Veterans Memorial are theirs."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Ordered by Ford under Article II; Congress was notified, not consulted, "
            "under the new War Powers Resolution."
        ),
        kia=18,
        deaths=41,
        wounded=50,
        losses_text=(
            "15 killed in action and 3 missing, presumed executed; 41 dead in all "
            "including 23 airmen killed in a helicopter crash in Thailand en route; 50 "
            "wounded"
        ),
        cost_m=None,
        cost_text="Not separately accounted",
        cost_year=1975,
        cost_year_note="No cost figure",
        sources=[21],
        combat=1,
    ),

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

    # ---- After the Cold War, 1990-2000 --------------------------------------
    conflict(
        name="Desert Shield / Desert Storm",
        theatre="Gulf War - response to Iraq's invasion of Kuwait",
        start=date(1990, 8, 7),
        end=date(1991, 2, 28),
        era="Post-Cold War",
        presidents="G.H.W. Bush",
        conflict_type="Defensive",
        reason=(
            "Collective defence: expel Iraqi forces from Kuwait after the August 1990 "
            "invasion and shield Saudi Arabia."
        ),
        summary=(
            "A 35-nation coalition of 700,000 troops, half a million of them American, "
            "deployed to Saudi Arabia over five months. A six-week air campaign was "
            "followed by a 100-hour ground war that destroyed the Iraqi army in "
            "Kuwait. Bush stopped short of Baghdad. Allies paid almost the entire "
            "bill. Both the Security Council and Congress voted before force was used "
            "- the last time that happened."
        ),
        auth_level=4,
        authority="Congress + UN",
        auth_note="UNSCR 678 and PL 102-1 - Senate 52-47, House 250-183.",
        kia=148,
        deaths=383,
        wounded=467,
        losses_text="148 battle deaths, 235 other deaths in theatre, 467 wounded",
        cost_m=7000,
        cost_text="About $7bn net after allied contributions (estimate)",
        cost_year=1991,
        cost_year_note="Combat and most outlays in 1991",
        sources=[1, 2, 31],
    ),

    conflict(
        name="Somalia Intervention",
        theatre="Restore Hope and UNOSOM II",
        start=date(1992, 12, 9),
        end=date(1994, 3, 31),
        era="Post-Cold War",
        presidents="G.H.W. Bush, Clinton",
        conflict_type="Humanitarian",
        reason=(
            "Secure famine relief deliveries during the civil war; later widened under "
            "UNOSOM II to disarming the militias."
        ),
        summary=(
            "Marines landed to protect food convoys during a famine that had killed "
            "300,000. Under the UN the mission expanded to disarming warlords, and the "
            "hunt for Mohamed Farrah Aidid ended in the Battle of Mogadishu in October "
            "1993, in which 18 US soldiers died and a pilot was captured. Clinton "
            "withdrew within six months. The episode shaped the refusal to intervene "
            "in Rwanda."
        ),
        auth_level=2,
        authority="UN only",
        auth_note=(
            "UNSCR 794 and 814; no prior congressional authorisation. Congress later "
            "set a withdrawal deadline by funding cutoff."
        ),
        kia=29,
        deaths=43,
        wounded=153,
        losses_text="43 dead, 29 from hostile action; 153 wounded",
        cost_m=1700,
        cost_text="About $1.7bn",
        cost_year=1993,
        cost_year_note="Midpoint of the deployment",
        sources=[4, 5],
        combat=15,
        flag="†",
    ),

    conflict(
        name="Iraq Intelligence HQ Strike",
        theatre="Baghdad",
        start=date(1993, 6, 26),
        end=date(1993, 6, 26),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Offensive",
        reason=(
            "Retaliation for the Iraqi plot to assassinate former President Bush in "
            "Kuwait."
        ),
        summary=(
            "Twenty-three Tomahawk missiles destroyed the Iraqi Intelligence Service "
            "headquarters at night to limit casualties. Clinton's first use of force."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Article 51 letter to the Security Council.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=50,
        cost_text="About $50m",
        cost_year=1993,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Uphold Democracy",
        theatre="Haiti",
        start=date(1994, 9, 19),
        end=date(1995, 3, 31),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Humanitarian",
        reason=(
            "Restore the elected president Aristide after the 1991 coup and end the "
            "junta's abuses."
        ),
        summary=(
            "With the invasion force airborne, a last-minute mission by Jimmy Carter, "
            "Colin Powell and Sam Nunn persuaded the junta to step down, and 20,000 "
            "troops landed unopposed. Aristide returned in October. The UN took over "
            "in March 1995. Clinton asserted he needed no congressional authorisation "
            "and did not seek it."
        ),
        auth_level=2,
        authority="UN only",
        auth_note="UNSCR 940; Clinton stated he did not need Congress.",
        kia=1,
        deaths=4,
        wounded=6,
        losses_text="4 dead, 1 from hostile action; roughly 6 wounded",
        cost_m=2000,
        cost_text="About $2bn",
        cost_year=1995,
        cost_year_note="Bulk of outlays in FY1995",
        sources=[4, 5],
        combat=1,
        flag="†",
    ),

    conflict(
        name="Deliberate Force",
        theatre="Bosnia, NATO air campaign",
        start=date(1995, 8, 30),
        end=date(1995, 9, 20),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Humanitarian",
        reason=(
            "Protect the UN-declared safe areas after the Srebrenica massacre and the "
            "Markale market shelling."
        ),
        summary=(
            "Three weeks of NATO air strikes on Bosnian Serb positions, most flown by "
            "US aircraft, combined with a Croat-Bosnian ground offensive to bring the "
            "Serbs to the table. The Dayton accords followed in November, and 20,000 "
            "US troops deployed with IFOR to enforce them."
        ),
        auth_level=2,
        authority="UN only",
        auth_note="Under UNSCR 816/836; no congressional authorisation.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=1000,
        cost_text=(
            "About $1bn (estimate); IFOR/SFOR peacekeeping after cost ~$20bn more"
        ),
        cost_year=1995,
        cost_year_note="Year of the operation",
        sources=[4],
        combat=12,
        flag="†",
    ),

    conflict(
        name="Desert Strike",
        theatre="Iraq cruise missiles",
        start=date(1996, 9, 3),
        end=date(1996, 9, 4),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Offensive",
        reason=(
            "Punish Iraqi military moves against Kurdish Irbil and extend the southern "
            "no-fly zone."
        ),
        summary=(
            "Forty-four cruise missiles struck air defences in southern Iraq after "
            "Iraqi forces entered the Kurdish zone; the no-fly zone was extended north "
            "to Baghdad's suburbs."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Response to Iraqi moves against Irbil.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=70,
        cost_text="About $70m",
        cost_year=1996,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Infinite Reach",
        theatre="Sudan and Afghanistan",
        start=date(1998, 8, 20),
        end=date(1998, 8, 20),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Offensive",
        reason=(
            "Retaliation for the al-Qaeda bombings of the US embassies in Kenya and "
            "Tanzania."
        ),
        summary=(
            "Cruise missiles struck al-Qaeda camps in Afghanistan, missing bin Laden, "
            "and the al-Shifa pharmaceutical plant in Khartoum, which the "
            "administration said made nerve-agent precursors - a claim that did not "
            "hold up."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Article 51 self-defence after the embassy bombings.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=79,
        cost_text="About $79m",
        cost_year=1998,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Desert Fox",
        theatre="Iraq",
        start=date(1998, 12, 16),
        end=date(1998, 12, 19),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Offensive",
        reason=(
            "Degrade Iraqi WMD capability after Baghdad ended cooperation with UN "
            "weapons inspectors."
        ),
        summary=(
            "Four nights of US and British air and missile strikes on some 100 "
            "targets, timed after the inspectors withdrew and ending on the eve of "
            "Ramadan - and during the House impeachment vote. Inspectors did not "
            "return until 2002."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Claimed revived authority under UNSCR 678/687; no congressional "
            "authorisation. Contested."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=750,
        cost_text="About $750m (estimate)",
        cost_year=1998,
        cost_year_note="Year of the operation",
        sources=[4],
        flag="†",
    ),

    conflict(
        name="Allied Force",
        theatre="Kosovo, NATO air war",
        start=date(1999, 3, 24),
        end=date(1999, 6, 10),
        era="Post-Cold War",
        presidents="Clinton",
        conflict_type="Humanitarian",
        reason=(
            "Stated: halt the expulsion and killing of Kosovar Albanians. No Security "
            "Council authorisation; the humanitarian basis was contested at the time."
        ),
        summary=(
            "Seventy-eight days of NATO bombing of Serbia without a ground campaign. "
            "The expulsion of Kosovar Albanians accelerated once bombing began; "
            "Milosevic conceded in June and Kosovo became a UN protectorate. The House "
            "tied 213-213 on authorising the air war and the campaign ran past the War "
            "Powers Resolution's 60-day limit."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "No Security Council resolution; House deadlocked 213-213 on authorising. "
            "Ran past the 60-day clock. Neither authority existed."
        ),
        kia=0,
        deaths=2,
        wounded=0,
        losses_text=(
            "2 dead in an Apache training crash in Albania; none from hostile action"
        ),
        cost_m=3000,
        cost_text="About $3bn",
        cost_year=1999,
        cost_year_note="Year of the operation",
        sources=[4, 5],
    ),

    # ---- After 9/11, 2001-2026 ----------------------------------------------
    conflict(
        name="Enduring Freedom",
        theatre="Afghanistan - response to 9/11",
        start=date(2001, 10, 7),
        end=date(2021, 8, 30),
        era="Post-9/11",
        presidents="G.W. Bush, Obama, Trump, Biden",
        conflict_type="Defensive",
        reason=(
            "Self-defence after the September 11 attacks: destroy al-Qaeda and remove "
            "the Taliban government sheltering it."
        ),
        summary=(
            "Special forces and air power toppled the Taliban in ten weeks; bin Laden "
            "escaped at Tora Bora. What followed was twenty years of "
            "counterinsurgency, a surge to 100,000 troops under Obama, a negotiated "
            "withdrawal under Trump, and a collapse under Biden in which the Taliban "
            "retook Kabul before the last US aircraft left. The longest war in "
            "American history."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "2001 AUMF (PL 107-40), House 420-1, Senate 98-0. UN affirmed self-defence "
            "but did not authorise the invasion."
        ),
        kia=1922,
        deaths=2459,
        wounded=20_769,
        losses_text=(
            "2,459 military dead, 1,922 from hostile action; 20,769 wounded; about "
            "3,900 US contractors also died"
        ),
        cost_m=2_300_000,
        cost_text=(
            "About $933bn direct DoD; $2.3tn full burden including veterans' care "
            "(Costs of War)"
        ),
        cost_year=2012,
        cost_year_note=(
            "OUTLAY-WEIGHTED: spending peaked with the 2010-12 surge. Indicative only"
        ),
        sources=[5, 6, 9],
    ),

    conflict(
        name="Iraqi Freedom / New Dawn",
        theatre="Iraq invasion and occupation",
        start=date(2003, 3, 20),
        end=date(2011, 12, 18),
        era="Post-9/11",
        presidents="G.W. Bush, Obama",
        conflict_type="Offensive",
        reason=(
            "Stated: eliminate weapons of mass destruction and end Saddam Hussein's "
            "regime. No such weapons were found."
        ),
        summary=(
            "Baghdad fell in three weeks; the occupation then dissolved into "
            "insurgency and sectarian civil war after the Iraqi army and Baath party "
            "were disbanded. The 2007 surge reduced the violence; US forces withdrew "
            "at the end of 2011 under a status-of-forces agreement Iraq would not "
            "extend. Congress had authorised force but the Security Council refused, "
            "and the war split the Western alliance."
        ),
        auth_level=3,
        authority="Congress",
        auth_note=(
            "2002 AUMF (PL 107-243), House 296-133, Senate 77-23. No UNSC "
            "authorisation; the revived-authority theory was widely rejected."
        ),
        kia=3481,
        deaths=4431,
        wounded=31_994,
        losses_text=(
            "4,431 military dead, 3,481 from hostile action; 31,994 wounded; about "
            "3,650 US contractors also died"
        ),
        cost_m=2_000_000,
        cost_text="About $815bn direct DoD; roughly $2.0tn full burden (Costs of War)",
        cost_year=2008,
        cost_year_note="OUTLAY-WEIGHTED: spending peaked FY2007-08. Indicative only",
        sources=[5, 6, 9],
    ),

    conflict(
        name="Odyssey Dawn / Unified Protector",
        theatre="Libya",
        start=date(2011, 3, 19),
        end=date(2011, 10, 31),
        era="Post-9/11",
        presidents="Obama",
        conflict_type="Humanitarian",
        reason=(
            "Protect civilians in Benghazi under UNSCR 1973; the mission broadened "
            "into regime change, which the resolution did not authorise."
        ),
        summary=(
            "US missiles and aircraft destroyed Libyan air defences and armour "
            "advancing on Benghazi, then handed the lead to NATO. Seven months of air "
            "strikes ended when rebels captured and killed Qaddafi. The administration "
            "argued the War Powers Resolution's 60-day clock did not apply because "
            "there were no 'hostilities'; the House rejected authorisation. Libya has "
            "been in civil war since."
        ),
        auth_level=2,
        authority="UN only",
        auth_note=(
            "UNSCR 1973. House rejected authorisation 123-295; administration argued "
            "there were no 'hostilities'."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=1100,
        cost_text="About $1.1bn",
        cost_year=2011,
        cost_year_note="Year of the operation",
        sources=[4, 42],
        combat=13,
    ),

    conflict(
        name="Inherent Resolve",
        theatre="ISIS, Iraq and Syria",
        start=date(2014, 8, 8),
        end=None,
        era="Post-9/11",
        presidents="Obama, Trump, Biden, Trump",
        conflict_type="Offensive",
        reason=(
            "Destroy the Islamic State after its capture of Mosul. Conducted in Iraq "
            "at the government's invitation, in Syria without consent."
        ),
        summary=(
            "Air strikes began to stop ISIS at Erbil and protect the Yazidis on "
            "Sinjar, then grew into a campaign of 35,000 strikes supporting Iraqi "
            "forces and Syrian Kurds, who retook Mosul in 2017 and Raqqa and the last "
            "ISIS territory in 2019. About 2,500 US troops remain in Iraq and 900 in "
            "Syria. Obama sent Congress a draft authorisation in 2015; it was never "
            "voted on."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note=(
            "2001 and 2002 AUMFs invoked; Obama's 2015 draft AUMF never voted on."
        ),
        kia=23,
        deaths=116,
        wounded=325,
        losses_text="116 dead, 23 from hostile action; roughly 325 wounded",
        cost_m=60_000,
        cost_text="About $60bn+ and rising",
        cost_year=2018,
        cost_year_note="OUTLAY-WEIGHTED midpoint of a 2014-2026 campaign",
        sources=[5, 6],
        flag="‡",
    ),

    conflict(
        name="Shayrat Strike",
        theatre="Syria",
        start=date(2017, 4, 6),
        end=date(2017, 4, 6),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason="Punitive strike for the Khan Shaykhun sarin attack.",
        summary=(
            "Fifty-nine Tomahawk missiles struck the Syrian air base from which the "
            "chemical attack was flown. The base was operating again within days."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Response to the Khan Shaykhun chemical attack; OLC opinion followed in "
            "2018."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=100,
        cost_text="About $100m",
        cost_year=2017,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Syria Strikes, Douma",
        theatre="With the UK and France",
        start=date(2018, 4, 14),
        end=date(2018, 4, 14),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason=(
            "Punitive strike for the Douma chemical attack; conducted with the UK and "
            "France."
        ),
        summary=(
            "One hundred and five missiles struck three chemical-weapons facilities "
            "near Damascus and Homs in a single night. No congressional or Security "
            "Council authorisation."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="No congressional or Security Council authorisation.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=240,
        cost_text="About $240m",
        cost_year=2018,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Soleimani Strike",
        theatre="Baghdad",
        start=date(2020, 1, 3),
        end=date(2020, 1, 3),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason=(
            "Targeted killing of the IRGC Quds Force commander. The administration "
            "cited an imminent threat it never substantiated to Congress."
        ),
        summary=(
            "A drone strike at Baghdad airport killed Qassem Soleimani and an Iraqi "
            "militia leader. Iran retaliated with ballistic missiles on US bases in "
            "Iraq; no Americans died but about 110 suffered brain injuries. Iran's air "
            "defences then shot down a Ukrainian airliner, killing 176. Both chambers "
            "passed a resolution to restrain further action; Trump vetoed it."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Article II plus a claimed 2002 Iraq AUMF basis. Both chambers passed "
            "S.J.Res. 68 to restrain him; vetoed, override failed."
        ),
        kia=0,
        deaths=0,
        wounded=110,
        losses_text=(
            "None killed; about 110 traumatic brain injuries in the Iranian "
            "retaliation"
        ),
        cost_m=75,
        cost_text="About $75m (estimate)",
        cost_year=2020,
        cost_year_note="Year of the operation",
        sources=[42, 43],
        flag="†",
    ),

    conflict(
        name="Syria Militia Strikes",
        theatre="Iran-backed militias",
        start=date(2021, 2, 25),
        end=date(2021, 2, 25),
        era="Post-9/11",
        presidents="Biden",
        conflict_type="Defensive",
        reason="Retaliation for rocket attacks on US personnel at Erbil.",
        summary=(
            "Air strikes on militia facilities at the Syria-Iraq border crossing; "
            "Biden's first use of force."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Article 51 collective self-defence asserted.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=15,
        cost_text="About $15m",
        cost_year=2021,
        cost_year_note="Year of the operation",
        sources=[42],
    ),

    conflict(
        name="al-Zawahiri Strike",
        theatre="Kabul",
        start=date(2022, 7, 31),
        end=date(2022, 7, 31),
        era="Post-9/11",
        presidents="Biden",
        conflict_type="Offensive",
        reason="Targeted killing of the al-Qaeda leader under the 2001 AUMF.",
        summary=(
            "Two Hellfire missiles killed Ayman al-Zawahiri on the balcony of a "
            "Taliban-provided safe house in Kabul, a year after the withdrawal."
        ),
        auth_level=1,
        authority="Standing law",
        auth_note="2001 AUMF, 21 years after enactment.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=2,
        cost_text="About $2m",
        cost_year=2022,
        cost_year_note="Year of the operation",
        sources=[4],
    ),

    conflict(
        name="Poseidon Archer",
        theatre="Houthi targets, Yemen",
        start=date(2024, 1, 11),
        end=date(2025, 1, 20),
        era="Post-9/11",
        presidents="Biden",
        conflict_type="Freedom of passage",
        reason=(
            "Reopen Red Sea shipping lanes after Houthi missile and drone attacks on "
            "commercial vessels."
        ),
        summary=(
            "A year of US and British strikes on Houthi launch sites and the largest "
            "sustained naval combat since World War II, with destroyers shooting down "
            "hundreds of missiles and drones. Commercial traffic through the Red Sea "
            "fell by half regardless. Three soldiers were killed at Tower 22 in Jordan "
            "in a related militia attack."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Article 51; no congressional authorisation.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text=(
            "None in the Yemen strikes; 3 killed at Tower 22 in Jordan in a related "
            "attack"
        ),
        cost_m=2500,
        cost_text="About $2.5bn",
        cost_year=2024,
        cost_year_note="Bulk of the campaign in 2024",
        sources=[42],
        combat=120,
        flag="†",
    ),

    conflict(
        name="Iraq and Syria Retaliation",
        theatre="After the Tower 22 attack",
        start=date(2024, 2, 2),
        end=date(2024, 2, 2),
        era="Post-9/11",
        presidents="Biden",
        conflict_type="Defensive",
        reason=(
            "Retaliation for the drone attack on Tower 22 in Jordan that killed three "
            "US soldiers."
        ),
        summary=(
            "Eighty-five targets struck across two countries in one night, against "
            "Iran's Quds Force and the militias it arms."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Article II; Article 51 asserted.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=50,
        cost_text="About $50m",
        cost_year=2024,
        cost_year_note="Year of the operation",
        sources=[42],
    ),

    conflict(
        name="Rough Rider",
        theatre="Yemen, 1,100+ strikes",
        start=date(2025, 3, 15),
        end=date(2025, 5, 5),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Freedom of passage",
        reason=(
            "Resume and escalate the campaign against Houthi attacks on Red Sea "
            "shipping; ended by agreement on 5 May 2025."
        ),
        summary=(
            "Fifty-two days of strikes on more than a thousand targets. Three F/A-18s "
            "were lost from carriers and some seven Reaper drones shot down. It ended "
            "with an Omani-brokered agreement that the Houthis would stop attacking US "
            "ships, though not Israeli-linked ones. The campaign's planning was "
            "discussed on a Signal group chat that included a journalist."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="War Powers letter sent 28 March, after the campaign began.",
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None; 3 F/A-18s and about 7 MQ-9s lost",
        cost_m=2000,
        cost_text="About $2bn (estimates $1-3bn)",
        cost_year=2025,
        cost_year_note="Year of the operation",
        sources=[40],
    ),

    conflict(
        name="Midnight Hammer",
        theatre="Iranian nuclear sites",
        start=date(2025, 6, 22),
        end=date(2025, 6, 22),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason=(
            "Preventive strike on the Fordow, Natanz and Isfahan nuclear facilities "
            "during the Israel-Iran war."
        ),
        summary=(
            "Seven B-2s dropped fourteen 30,000-pound bunker-busters on Fordow and "
            "Natanz while a submarine fired Tomahawks at Isfahan, twelve days into "
            "Israel's war with Iran. Iran fired missiles at the US base in Qatar in a "
            "telegraphed response, and a ceasefire followed within days. How much "
            "enriched uranium survived is disputed."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Notification sent 23 June, after the aircraft had left Iranian airspace."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None",
        cost_m=200,
        cost_text="About $200m for the strike; $4.8-7.2bn with the regional buildup",
        cost_year=2025,
        cost_year_note="Year of the operation",
        sources=[41, 42, 43],
    ),

    conflict(
        name="Southern Spear",
        theatre="Boat strikes, Caribbean and eastern Pacific",
        start=date(2025, 9, 2),
        end=None,
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Other",
        reason=(
            "Lethal interdiction of vessels alleged to carry narcotics, framed as "
            "armed conflict with designated cartels rather than law enforcement - "
            "which is the core legal dispute."
        ),
        summary=(
            "Beginning in September 2025 the military destroyed small boats in "
            "international waters that it said carried drugs, killing everyone aboard, "
            "without interdiction, boarding or arrest. By September 2026 at least 68 "
            "strikes had killed more than 230 people. The administration declared an "
            "armed conflict with designated cartels; the Senate rejected a war powers "
            "resolution 51-48, and the House defeated its own."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Senate rejected the Schiff-Kaine resolution 51-48; House versions also "
            "defeated."
        ),
        kia=0,
        deaths=0,
        wounded=0,
        losses_text="None; 230+ killed aboard the vessels",
        cost_m=820,
        cost_text="About $820m campaign-specific through July 2026",
        cost_year=2026,
        cost_year_note="Campaign centroid",
        sources=[36, 37, 49, 50],
        combat=68,
        flag="‡",
    ),

    conflict(
        name="Absolute Resolve",
        theatre="Venezuela, capture of Maduro",
        start=date(2026, 1, 3),
        end=date(2026, 1, 3),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason=(
            "Capture President Maduro on US drug-trafficking charges, followed by US "
            "direction of a political transition."
        ),
        summary=(
            "Special operations forces backed by more than 150 aircraft struck air "
            "defences and seized Nicolas Maduro and his wife from a fortified compound "
            "in Caracas in a night raid, flying them to New York to face drug charges. "
            "Around 80 to 100 Venezuelan and Cuban personnel died. Congress learned of "
            "it after it was over; the vice-president was sworn in as interim "
            "president two days later."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note="Congress learned of it after completion.",
        kia=0,
        deaths=0,
        wounded=7,
        losses_text="None killed; 7 injured. About 80-100 Venezuelan and Cuban dead",
        cost_m=3880,
        cost_text=(
            "About $3.9bn - DERIVED: $4.7bn reported jointly with Southern Spear (Aug "
            "2025-Mar 2026) less the $820m campaign figure"
        ),
        cost_year=2026,
        cost_year_note="Year of the operation",
        sources=[38, 39, 46],
        flag="†",
    ),

    conflict(
        name="Epic Fury",
        theatre="Iran, with Israel",
        start=date(2026, 2, 28),
        end=date(2026, 5, 5),
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Offensive",
        reason=(
            "Destroy Iran's nuclear, missile, naval and regime-security capacity, "
            "jointly with Israel."
        ),
        summary=(
            "A US-Israeli air and missile campaign against Iran's military, nuclear "
            "and security apparatus, the largest US combat operation since 2003. Iran "
            "struck back at US bases and shipping and closed the Strait of Hormuz. A "
            "ceasefire took hold on 7 April and the operation was declared over on 5 "
            "May, at a cost of $33bn, more than 400 wounded and dozens of aircraft. "
            "The House has since voted three times to end the hostilities; the Senate "
            "has not acted."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Gang of Eight briefed. H.Con.Res. 38 failed 212-219; the House has since "
            "passed a war powers resolution three times."
        ),
        kia=7,
        deaths=13,
        wounded=417,
        losses_text=(
            "7 killed in action, 13 dead in all (disputed; officials allege an "
            "undercount of at least four); 417 wounded; 42-52 aircraft lost"
        ),
        cost_m=33_400,
        cost_text="$33.4bn through 29 June (DoD); CSIS estimates $34-42bn",
        cost_year=2026,
        cost_year_note="Year of the operation",
        sources=[32, 33, 34, 35, 44, 47, 48],
        combat=38,
        flag="§",
    ),

    conflict(
        name="Project Freedom",
        theatre="Strait of Hormuz escort",
        start=date(2026, 5, 4),
        end=None,
        era="Post-9/11",
        presidents="Trump",
        conflict_type="Freedom of passage",
        reason=(
            "Escort merchant shipping through the Strait of Hormuz after Iranian "
            "attacks on commercial vessels."
        ),
        summary=(
            "Declared the second stage of the Iran war after Epic Fury ended: "
            "destroyers and aircraft escorting merchant ships through the strait Iran "
            "had closed. The overt phase was paused after two days; Iranian boats and "
            "missiles engaged three US destroyers on 7 May. No casualty or cost "
            "accounting has been published."
        ),
        auth_level=0,
        authority="Executive only",
        auth_note=(
            "Declared the second stage of the Iran war after Epic Fury concluded."
        ),
        kia=None,
        deaths=None,
        wounded=None,
        losses_text="Not separately reported",
        cost_m=None,
        cost_text="Not separately reported",
        cost_year=2026,
        cost_year_note="No figures",
        sources=[45],
        combat=3,
        flag="‡",
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
    row["cpi"] = CPI[row["cost_year"]]
    row["factor"] = CPI_BASE / row["cpi"]
    row["cost_adj"] = None if row["cost_m"] is None else row["cost_m"] * row["factor"]

# No misspelt era or type.
assert all(row["era"] in ERAS and row["conflict_type"] in TYPES for row in ROWS)
