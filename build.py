# -*- coding: utf-8 -*-
"""
Build the Figures workbook from data.py.

    python3 build.py

writes US-Conflicts-1775-2026-Figures.xlsx next to this file: the numbers,
one row per conflict.
"""

import os
from collections import namedtuple

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from data import CPI_BASE, CPI_BASE_LABEL, ERAS, LV_LABEL, REFS, ROWS, TYPES, cpi_basis

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES_FILE = "US-Conflicts-1775-2026-Figures.xlsx"


# ===========================================================================
# Shared text
# ===========================================================================

# How each measure is counted: shown on the Method & Sources sheet and pages.
METHOD = [
    ("Scope",
     "Overt uses of US armed force at the scale of a named war, campaign or operation, 1775 to 22 "
     "September 2026: 75 entries. Excludes the several hundred minor landings and shows of force "
     "in the CRS list, purely covert action (Bay of Pigs is included because US airmen died), and "
     "the smaller Indian War campaigns not listed."),
    ("KIA + MIA",
     "US military deaths from hostile action, plus those missing and presumed dead. Excludes "
     "accidents, disease and other non-hostile deaths. For the Civil War both Union and "
     "Confederate dead are counted: both were Americans."),
    ("All casualties",
     "All US deaths (hostile and non-hostile) plus wounded. Where wounded were never tallied the "
     "cell holds deaths alone and is flagged. Excludes contractors, allied forces and foreign "
     "deaths."),
    ("Combat days",
     "Days on which US forces were engaged or striking. For the major wars this is the whole war; "
     "for occupations it is the insurgency phase; for one-day strikes it is 1."),
    ("All conflict days",
     "First to last day of the named conflict, inclusive. Ongoing conflicts run to 22 September "
     "2026."),
    ("Net cost, then-year",
     "Best estimate of the US taxpayer burden in the dollars of the time, net of allied "
     "reimbursement. Pre-1991 major wars: CRS RS22926 (military operations only - no veterans' "
     "benefits, no debt interest). Afghanistan and Iraq: Costs of War full burden including "
     "veterans' care. Small operations: DoD or press estimates. Blank where no reliable figure "
     "exists."),
    ("Net cost, Aug-2026 dollars",
     f"The then-year cost restated with CPI-U to {CPI_BASE_LABEL} = {CPI_BASE}, using each "
     "conflict's cost-centre year. BLS series from 1913; Minneapolis Fed historical estimates for "
     "1800-1912; the 1770s factor is implied from CRS's own conversion. Fully auditable on the "
     "CPI_Deflator sheet, which also shows CRS's constant-dollar figures for the ten major wars as "
     "a cross-check."),
    ("Authorization strength",
     "Ordinal: 5 = declaration of war; 4 = statute plus UN Security Council resolution; 3 = "
     "statute or joint resolution (including retroactive); 2 = UN resolution only; 1 = a "
     "pre-existing statute or AUMF invoked; 0 = executive action alone."),
    ("Conflict type",
     "The conflict's principal STATED rationale: Defensive, Offensive, Humanitarian, Freedom of "
     "passage, or Other. A judgment, not a fact - see the caveats."),
]

# Where the figures are contested, numbered in the order shown.
CAVEATS = [
    "GULF WAR NET COST REVISED. Earlier versions of these tables used ~$7bn net; DoD's own figure, "
    "cited by CRS, is $4.7bn in current-year dollars after allied contributions of about $54bn "
    "against a $61bn gross. This file uses $4.7bn.",
    "CIVIL WAR FIGURES ARE OFFICIAL RETURNS, NOT MODERN ESTIMATES. VA/DoD returns give 498,332 "
    "dead on both sides; demographic work since 2011 puts the true figure at 620,000-750,000. "
    "Confederate returns are incomplete and Confederate wounded were never tallied.",
    "PRE-1900 SMALL CONFLICTS ARE ESTIMATES. Deaths for the Indian Wars, the Quasi-War and the "
    "Barbary Wars come from regimental returns and secondary histories, not a central casualty "
    "system, and are flagged. The Apache Wars' US deaths were never reliably tallied as a series "
    "and are left blank rather than guessed.",
    "COSTS BEFORE VIETNAM WERE NEVER SEPARATELY RECORDED. CRS estimated them as the increase in "
    "Army and Navy outlays over the pre-war average. For the occupations, expeditions and Indian "
    "Wars no such figure exists; those cells are blank and the totals therefore understate.",
    "TWO DEFLATOR METHODS DIVERGE FOR THE OLDEST WARS. This file uses CPI from each conflict's "
    "cost-centre year. CRS used a hybrid (CPI before 1940, defence-specific deflators after). For "
    "the Civil War the two differ by about 30%, for World War II by about 15%. Both are shown on "
    "the CPI_Deflator sheet; neither is 'right'.",
    "AFGHANISTAN AND IRAQ ADJUSTED COSTS ARE INDICATIVE ONLY. Their totals already blend past "
    "outlays with veterans' care projected to 2050 - partly future dollars - so inflating them "
    "overstates. They are also on a broader cost basis (full burden) than every other row "
    "(operations only), which flatters the older wars by comparison.",
    "COST-CENTRE YEARS FOR LONG WARS ARE OUTLAY-WEIGHTED. Civil War 1864, WWI 1919, WWII 1944, "
    "Korea 1952, Vietnam 1968, Afghanistan 2012, Iraq 2008, Inherent Resolve 2018. Marked on the "
    "deflator sheet.",
    "CONFLICT TYPE IS A JUDGMENT. Each conflict is classed by its principal stated rationale. "
    "Reasonable people would reclassify several: the War of 1812 is 'offensive' because the plan "
    "was to invade Canada though the grievances were real; the Mexican War is 'offensive' though "
    "Polk claimed self-defence; Vietnam and Korea are 'defensive' as collective defence of an "
    "ally; Southern Spear is 'other' because the government calls it armed conflict and critics "
    "call it law enforcement.",
    "EPIC FURY'S DEATH TOLL IS UNSETTLED. Military Times reported 13 killed in April 2026; later "
    "accounting gives 7 killed in action with 417 wounded; officials alleged in September 2026 an "
    "undercount of at least four. This file uses 7 KIA and 13 total deaths.",
    "THE VENEZUELA COST IS DERIVED. DoD reported $4.7bn jointly for boat strikes and the January "
    "2026 operation; the Southern Spear campaign figure ($820m) is subtracted. The split is an "
    "inference.",
    "DAY TOTALS DOUBLE-COUNT OVERLAPS. The Creek War sits inside the War of 1812, the Cambodian "
    "Campaign inside Vietnam, and Inherent Resolve overlaps Poseidon Archer and Epic Fury. Their "
    "casualties are also included in the parent war's totals where noted.",
    "PRECISION WARNING. The deflator is precise to a tenth of an index point; the underlying "
    "figures are not. The pre-1900 rows are order-of-magnitude and the adjusted column inherits "
    "every weakness of its input.",
]

FLAGS = "† rough estimate or incomplete returns · ‡ ongoing as of 22 Sep 2026 · § disputed figure, see caveats"


# ===========================================================================
# Workbook styles and helpers
# ===========================================================================

FONT = "Arial"
INK = "FF11161B"      # body text
ACCENT = "FF2C4A63"   # header fill and section labels
MUTED = "FF64707C"    # notes and captions
INTEGER = "#,##0"
MONEY = "$#,##0"

# Authorization levels, 5 (declared war) to 0 (executive only): green
# through blue and amber to red. Fill, then text colour.
LEVEL_FILL = {5: "FFBFDCCB", 4: "FFCFE6D8", 3: "FFDCECE1", 2: "FFD9E4F2", 1: "FFF0E6CD", 0: "FFF3DCD9"}
LEVEL_FONT = {5: "FF0F4530", 4: "FF14503A", 3: "FF1F5C43", 2: "FF1E4478", 1: "FF6A5314", 0: "FF7E2F27"}

# One hue per conflict type. Fill, then text colour.
TYPE_FILL = {
    "Defensive": "FFDCE6EF",
    "Offensive": "FFF2DEDA",
    "Humanitarian": "FFDEEBE0",
    "Freedom of passage": "FFDAE9E8",
    "Other": "FFE8E5E0",
}
TYPE_FONT = {
    "Defensive": "FF1E4478",
    "Offensive": "FF7E2F27",
    "Humanitarian": "FF1F5C43",
    "Freedom of passage": "FF1B5450",
    "Other": "FF55504A",
}


def font(size=9, color=INK, bold=False, italic=False, underline=None):
    """Arial in the given size and colour; 9pt body text by default."""
    return Font(name=FONT, size=size, color=color, bold=bold, italic=italic, underline=underline)


def style_header(ws, row, columns, height=36):
    """White bold text on the accent colour across a header row."""
    ws.row_dimensions[row].height = height
    for column in range(1, columns + 1):
        cell = ws.cell(row=row, column=column)
        cell.font = font(bold=True, color="FFFFFFFF")
        cell.fill = PatternFill("solid", fgColor=ACCENT)
        cell.alignment = Alignment(vertical="center", wrap_text=True)


def title_block(ws, title, subtitle, columns):
    """Rows 1-3: title, subtitle, and a line of provenance; row 4 is a spacer."""
    ws["A1"] = title
    ws["A1"].font = font(size=16, bold=True)
    ws["A2"] = subtitle
    ws["A2"].font = font(italic=True, color=MUTED)
    ws["A3"] = (f"Compiled 22 September 2026 · 75 conflicts, 1775-2026 · then-year dollars unless stated · "
                f"{FLAGS} · read 'Method & Sources' before quoting a number")
    ws["A3"].font = font(color=MUTED)
    for row, span in ((1, 6), (2, 9), (3, 12)):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=min(columns, span))
    ws.row_dimensions[1].height = 22
    ws.row_dimensions[4].height = 6


def add_table(ws, name, first_row, last_row, columns, style="TableStyleLight1"):
    """Make a range an Excel table: banded rows, and a filter arrow on each heading."""
    table = Table(displayName=name, ref=f"A{first_row}:{get_column_letter(columns)}{last_row}")
    table.tableStyleInfo = TableStyleInfo(name=style, showRowStripes=True, showColumnStripes=False,
                                          showFirstColumn=False, showLastColumn=False)
    ws.add_table(table)


def colour_chip(cell, kind, key):
    """Colour a cell as an authorization level (kind "level") or a conflict type."""
    if kind == "level":
        cell.fill = PatternFill("solid", fgColor=LEVEL_FILL[key])
        cell.font = font(bold=True, color=LEVEL_FONT[key])
    else:
        cell.fill = PatternFill("solid", fgColor=TYPE_FILL[key])
        cell.font = font(bold=True, color=TYPE_FONT[key])


def write_method_sheet(wb):
    """The Method & Sources sheet: definitions, caveats, then every source."""
    ws = wb.create_sheet("Method & Sources")
    ws["A1"] = "Method, caveats and sources"
    ws["A1"].font = font(size=14, bold=True)
    row = 3

    ws.cell(row=row, column=1, value="HOW THESE FIGURES ARE COUNTED").font = font(size=10, bold=True, color=ACCENT)
    row += 1
    for term, definition in METHOD:
        ws.cell(row=row, column=1, value=term).font = font(bold=True)
        cell = ws.cell(row=row, column=2, value=definition)
        cell.font = font()
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 44
        row += 1

    row += 1
    ws.cell(row=row, column=1, value="WHERE THE FIGURES ARE CONTESTED").font = font(size=10, bold=True, color="FF7E2F27")
    row += 1
    for number, caveat in enumerate(CAVEATS, 1):
        ws.cell(row=row, column=1, value=str(number)).font = font(bold=True, color=MUTED)
        cell = ws.cell(row=row, column=2, value=caveat)
        cell.font = font()
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 58
        row += 1

    row += 1
    ws.cell(row=row, column=1, value="SOURCES").font = font(size=10, bold=True, color=ACCENT)
    row += 1
    ws.cell(row=row, column=1, value="#").font = font(bold=True, color=MUTED)
    ws.cell(row=row, column=2,
            value="Reference (the 'Sources' column of the main table cites these numbers)").font = font(bold=True, color=MUTED)
    row += 1
    for number, label, url in REFS:
        ws.cell(row=row, column=1, value=number).font = font(color=MUTED)
        cell = ws.cell(row=row, column=2, value=label)
        if url:
            cell.hyperlink = url
            cell.font = font(color=ACCENT, underline="single")
        else:
            cell.font = font()
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 26
        row += 1

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 122
    ws.sheet_view.showGridLines = False


# ===========================================================================
# The Figures workbook
# ===========================================================================

HEADER_ROW = 5                   # rows 1-4 hold the title block
FIRST_ROW = HEADER_ROW + 1       # conflict n is on row HEADER_ROW + n
LAST_ROW = HEADER_ROW + len(ROWS)
TOTAL_ROW = LAST_ROW + 1

# The Figures sheet's columns, left to right. The key names a column in
# figure_values() and in formulas; kind sets how its cells look.
Column = namedtuple("Column", "key header width kind")
FIGURE_COLUMNS = [
    Column("idx", "#", 5, "integer"),
    Column("name", "Conflict", 30, "name"),
    Column("start", "Start", 13, "date"),
    Column("end", "End", 13, "date"),
    Column("era", "Era", 20, "text"),
    Column("presidents", "President(s)", 26, "text"),
    Column("type", "Conflict Type", 18, "text"),
    Column("reason", "Reason for the Conflict", 60, "wrap"),
    Column("authorization", "Authorization", 17, "text"),
    Column("auth_level", "Auth. strength", 12, "integer"),
    Column("combat_days", "Combat Days", 12, "integer"),
    Column("all_days", "All Conflict Days", 15, "integer"),
    Column("kia", "KIA + MIA", 12, "integer"),
    Column("casualties", "All Casualties", 14, "integer"),
    Column("cost_m", "Net Cost to US Taxpayers ($m, then-year)", 22, "money"),
    Column("cost_adj", f"Net Cost in {CPI_BASE_LABEL} Dollars ($m)", 22, "money"),
]
KEYS = [column.key for column in FIGURE_COLUMNS]
LETTER = {column.key: get_column_letter(n) for n, column in enumerate(FIGURE_COLUMNS, 1)}


def position(key):
    """The 1-based number of a Figures column."""
    return KEYS.index(key) + 1


def column_range(key):
    """An absolute reference to one column's conflict rows, e.g. $G$6:$G$80."""
    letter = LETTER[key]
    return f"${letter}${FIRST_ROW}:${letter}${LAST_ROW}"


def is_numeric(n):
    """Whether Figures column n holds a quantity (the # column does not count)."""
    column = FIGURE_COLUMNS[n - 1]
    return column.kind in ("integer", "money") and column.key != "idx"


def style_cell(cell, kind):
    """Font, number format and alignment for one Figures cell."""
    cell.font = font(bold=(kind == "name"))
    if kind == "date":
        cell.number_format = "d mmm yyyy"
        cell.alignment = Alignment(vertical="center")
    elif kind in ("integer", "money"):
        cell.number_format = INTEGER if kind == "integer" else MONEY
        cell.alignment = Alignment(horizontal="right", vertical="center")
    elif kind == "wrap":
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    else:
        cell.alignment = Alignment(vertical="center")


def figure_values(r, row):
    """One conflict's cells on the Figures sheet, keyed like FIGURE_COLUMNS."""
    cost = f"{LETTER['cost_m']}{row}"
    return {
        "idx": r["idx"],
        "name": r["name"] + (" ‡" if r["ongoing"] else ""),
        "start": r["start"],
        "end": r["end_or_today"],
        "era": r["era"],
        "presidents": r["presidents"],
        "type": r["conflict_type"],
        "reason": r["reason"],
        "authorization": r["auth_label"],
        "auth_level": r["auth_level"],
        "combat_days": r["combat_days"],
        "all_days": r["all_days"],
        "kia": r["kia"],
        "casualties": r["casualties"],
        "cost_m": r["cost_m"],
        # The then-year cost times this conflict's factor on the deflator sheet.
        "cost_adj": f'=IF({cost}="","",{cost}*CPI_Deflator!F{row})',
    }


def write_figures_table(ws):
    """The header row and one row per conflict, as an Excel table."""
    for n, column in enumerate(FIGURE_COLUMNS, 1):
        ws.cell(row=HEADER_ROW, column=n, value=column.header)
    style_header(ws, HEADER_ROW, len(FIGURE_COLUMNS), height=44)
    for r in ROWS:
        row = HEADER_ROW + r["idx"]
        values = figure_values(r, row)
        for n, column in enumerate(FIGURE_COLUMNS, 1):
            style_cell(ws.cell(row=row, column=n, value=values[column.key]), column.kind)
        colour_chip(ws.cell(row=row, column=position("type")), "type", r["conflict_type"])
        colour_chip(ws.cell(row=row, column=position("authorization")), "level", r["auth_level"])
        ws.row_dimensions[row].height = 40
    add_table(ws, "Figures", HEADER_ROW, LAST_ROW, len(FIGURE_COLUMNS))
    for n, column in enumerate(FIGURE_COLUMNS, 1):
        ws.column_dimensions[get_column_letter(n)].width = column.width
    ws.freeze_panes = "C6"       # keep the # and Conflict columns and the headings in view
    ws.sheet_view.showGridLines = False


def write_totals(ws):
    """A SUM row under the table, then three rows giving shares of it."""
    ws.cell(row=TOTAL_ROW, column=1, value="TOTAL")
    ws.cell(row=TOTAL_ROW, column=2, value=f"{len(ROWS)} conflicts")
    for key in ("combat_days", "all_days", "kia", "casualties", "cost_m", "cost_adj"):
        letter = LETTER[key]
        cell = ws.cell(row=TOTAL_ROW, column=position(key), value=f"=SUM({letter}{FIRST_ROW}:{letter}{LAST_ROW})")
        cell.number_format = MONEY if key.startswith("cost") else INTEGER
    for n in range(1, len(FIGURE_COLUMNS) + 1):
        cell = ws.cell(row=TOTAL_ROW, column=n)
        cell.font = font(bold=True)
        cell.fill = PatternFill("solid", fgColor="FFE9ECEF")
        cell.border = Border(top=Side(style="medium", color=ACCENT))
        if is_numeric(n):
            cell.alignment = Alignment(horizontal="right")

    row_of = {r["name"]: HEADER_ROW + r["idx"] for r in ROWS}
    shares = [
        ("World War II alone", ["World War II"]),
        ("Civil War + both World Wars", ["American Civil War", "World War I", "World War II"]),
        ("Afghanistan + Iraq", ["Enduring Freedom", "Iraqi Freedom / New Dawn"]),
    ]
    for offset, (label, names) in enumerate(shares, 1):
        row = TOTAL_ROW + offset
        ws.cell(row=row, column=2, value=f"{label}, share of total")
        for key in ("kia", "casualties", "cost_m", "cost_adj"):
            letter = LETTER[key]
            part = "+".join(f"{letter}{row_of[name]}" for name in names)
            cell = ws.cell(row=row, column=position(key), value=f'=IFERROR(({part})/{letter}{TOTAL_ROW},"")')
            cell.number_format = "0.0%"
        for n in range(1, len(FIGURE_COLUMNS) + 1):
            cell = ws.cell(row=row, column=n)
            cell.font = font(italic=True, color=MUTED)
            if is_numeric(n):
                cell.alignment = Alignment(horizontal="right")


def write_breakdown(ws, top, label, match_key, groups):
    """One block of counts and sums, a row per group; returns the next free row.

    A group's row counts and sums the conflicts whose match_key cell holds
    exactly the group's name."""
    heads = ["Group", "Conflicts", "Combat days", "KIA + MIA", "All casualties",
             "Cost then-year ($m)", f"Cost {CPI_BASE_LABEL} ($m)", "Share of adj. cost"]
    ws.cell(row=top, column=2, value=label).font = font(bold=True, color=ACCENT)
    for k, head in enumerate(heads):
        cell = ws.cell(row=top + 1, column=2 + k, value=head)
        cell.font = font(bold=True, color=MUTED)
        if k:
            cell.alignment = Alignment(horizontal="right")
    match = column_range(match_key)
    for k, group in enumerate(groups):
        row = top + 2 + k
        cell = ws.cell(row=row, column=2, value=group)
        if match_key == "type":
            colour_chip(cell, "type", group)
        else:
            cell.font = font(bold=True)
        ws.cell(row=row, column=3, value=f"=COUNTIF({match},$B{row})")
        for n, key in enumerate(("combat_days", "kia", "casualties", "cost_m", "cost_adj"), 4):
            ws.cell(row=row, column=n, value=f"=SUMIF({match},$B{row},{column_range(key)})")
        ws.cell(row=row, column=9, value=f'=IFERROR(H{row}/${LETTER["cost_adj"]}${TOTAL_ROW},"")')
        for n in range(3, 10):
            cell = ws.cell(row=row, column=n)
            cell.font = font()
            cell.alignment = Alignment(horizontal="right")
            cell.number_format = "0.0%" if n == 9 else (MONEY if n in (7, 8) else INTEGER)
    return top + 2 + len(groups) + 1


def write_breakdowns(ws):
    """Totals by conflict type, era and authorization; returns the next free row."""
    row = TOTAL_ROW + 6
    row = write_breakdown(ws, row, "BY CONFLICT TYPE", "type", TYPES)
    row = write_breakdown(ws, row, "BY ERA", "era", ERAS)
    row = write_breakdown(ws, row, "BY AUTHORIZATION", "authorization",
                          [LV_LABEL[level] for level in (5, 4, 3, 2, 1, 0)])
    return row


def write_notes(ws, row):
    """Notes on reading the sheet, from the given row down."""
    notes = [
        "Note  Blank cells mean no reliable public figure exists; they are not zeros and Excel "
        "sorts them last. 0 means none.",
        "Cost is NET of allied reimbursement in then-year US$ millions; column "
        f"{LETTER['cost_adj']} restates it in {CPI_BASE_LABEL} dollars via the CPI_Deflator sheet "
        "(base index in one yellow cell).",
        "Pre-1991 major-war costs are CRS estimates of military operations only; Afghanistan and "
        "Iraq are Costs of War full burden. See caveats 4-6.",
        "Civil War casualties count Union and Confederate dead; official returns understate the "
        "true toll. See caveat 2.",
        "Full method, caveats and per-row sources: 'Method & Sources' sheet.",
    ]
    for k, text in enumerate(notes):
        ws.cell(row=row + k, column=1, value=text).font = font(color=MUTED)


def add_header_comments(ws):
    """Hover notes on the two headings most likely to be misread."""
    ws.cell(row=HEADER_ROW, column=position("cost_adj")).comment = Comment(
        f"CPI-U adjusted to {CPI_BASE_LABEL} dollars (base {CPI_BASE}). Formula multiplies the then-year cost "
        "by the factor on the CPI_Deflator sheet for each conflict's cost-centre year. Long wars use "
        "outlay-weighted years. Afghanistan and Iraq are indicative only.",
        "Compiler", height=150, width=360)
    ws.cell(row=HEADER_ROW, column=position("kia")).comment = Comment(
        "Hostile deaths plus missing presumed dead. Civil War counts both sides. Blank = never reliably tallied.",
        "Compiler", height=90, width=330)


def write_deflator_sheet(wb):
    """How every inflation-adjusted cost was produced, one row per conflict.

    Rows line up with the Figures sheet (conflict n is on row 5 + n of both),
    so Figures can multiply by CPI_Deflator!F on the same row."""
    cs = wb.create_sheet("CPI_Deflator")
    cs["A1"] = "Inflation deflator - how every adjusted figure was produced"
    cs["A1"].font = font(size=13, bold=True)
    cs["A2"] = f"Base index (CPI-U, {CPI_BASE_LABEL}):"
    cs["A2"].font = font(bold=True)
    cs["B2"] = CPI_BASE                    # the one input on the sheet: blue on yellow
    cs["B2"].number_format = "0.000"
    cs["B2"].font = font(bold=True, color="FF0000FF")
    cs["B2"].fill = PatternFill("solid", fgColor="FFFFFF00")
    cs["C2"] = "<- input. Change this cell to restate every adjusted cost against a different base month."
    cs["C2"].font = font(italic=True, color=MUTED)
    cs["A3"] = "CRS FY2011 constant-dollar figures are uplifted to the base with CPI-U 2011 = 224.939."
    cs["A3"].font = font(italic=True, color=MUTED)

    headers = ["#", "Conflict", "Cost-centre year", "Why that year / index basis", "CPI-U index (1982-84=100)",
               "Factor to base", "CRS constant FY2011 $m", "CRS uplifted to base ($m)",
               "CPI-method adjusted ($m)", "CRS / CPI ratio"]
    for n, header in enumerate(headers, 1):
        cs.cell(row=HEADER_ROW, column=n, value=header)
    style_header(cs, HEADER_ROW, len(headers), height=40)

    for r in ROWS:
        row = HEADER_ROW + r["idx"]
        cs.cell(row=row, column=1, value=r["idx"])
        cs.cell(row=row, column=2, value=r["name"])
        cs.cell(row=row, column=3, value=r["cost_year"]).number_format = "0"
        cs.cell(row=row, column=4, value=f"{r['cost_year_note']}. Index: {cpi_basis(r['cost_year'])}.")
        cs.cell(row=row, column=5, value=r["cpi"]).number_format = "0.000"
        cs.cell(row=row, column=6, value=f"=$B$2/E{row}").number_format = "0.0000"
        if r["crs_2011"]:
            # CRS's own constant-dollar figure, uplifted to the base, against ours.
            cs.cell(row=row, column=7, value=r["crs_2011"]).number_format = MONEY
            cs.cell(row=row, column=8, value=f"=G{row}*$B$2/224.939").number_format = MONEY
            cs.cell(row=row, column=9, value=f"=Figures!{LETTER['cost_adj']}{row}").number_format = MONEY
            cs.cell(row=row, column=10, value=f'=IFERROR(H{row}/I{row},"")').number_format = "0.00"
        for n in range(1, len(headers) + 1):
            cell = cs.cell(row=row, column=n)
            # Green marks a figure pulled from the Figures sheet.
            cell.font = font(bold=(n == 2), color="FF008000" if n == 9 else INK)
            cell.alignment = Alignment(wrap_text=(n == 4), vertical="top",
                                       horizontal="left" if n in (2, 4) else "right")
            if "OUTLAY-WEIGHTED" in r["cost_year_note"] and n in (3, 4):
                cell.fill = PatternFill("solid", fgColor="FFF0E6CD")
        cs.row_dimensions[row].height = 30

    add_table(cs, "Deflator", HEADER_ROW, LAST_ROW, len(headers), "TableStyleLight9")
    for n, width in enumerate([5, 30, 12, 70, 14, 12, 16, 18, 18, 12], 1):
        cs.column_dimensions[get_column_letter(n)].width = width
    cs.freeze_panes = "A6"
    cs.sheet_view.showGridLines = False


def build_figures():
    """Write the Figures workbook and return its path."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Figures"
    title_block(ws, "US Conflicts, 1775-2026 - Figures",
                "Every column sorts and filters from the header arrows. Column '#' restores chronological order.",
                len(FIGURE_COLUMNS))
    write_figures_table(ws)
    write_totals(ws)
    notes_row = write_breakdowns(ws)
    write_notes(ws, notes_row)
    add_header_comments(ws)
    write_deflator_sheet(wb)
    write_method_sheet(wb)
    path = os.path.join(HERE, FIGURES_FILE)
    wb.save(path)
    return path


if __name__ == "__main__":
    print(build_figures())
