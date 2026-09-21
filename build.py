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
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from data import CPI_BASE_LABEL, ERAS, LV_LABEL, ROWS, TYPES

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES_FILE = "US-Conflicts-1775-2026-Figures.xlsx"


# ===========================================================================
# Shared text
# ===========================================================================

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
                f"{FLAGS}")
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


def figure_values(r):
    """One conflict's cells on the Figures sheet, keyed like FIGURE_COLUMNS."""
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
        "cost_adj": r["cost_adj"],
    }


def write_figures_table(ws):
    """The header row and one row per conflict, as an Excel table."""
    for n, column in enumerate(FIGURE_COLUMNS, 1):
        ws.cell(row=HEADER_ROW, column=n, value=column.header)
    style_header(ws, HEADER_ROW, len(FIGURE_COLUMNS), height=44)
    for r in ROWS:
        row = HEADER_ROW + r["idx"]
        values = figure_values(r)
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
    write_breakdowns(ws)
    path = os.path.join(HERE, FIGURES_FILE)
    wb.save(path)
    return path


if __name__ == "__main__":
    print(build_figures())
