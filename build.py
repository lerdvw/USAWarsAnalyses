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
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from data import CPI_BASE_LABEL, ROWS

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


def build_figures():
    """Write the Figures workbook and return its path."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Figures"
    title_block(ws, "US Conflicts, 1775-2026 - Figures",
                "Every column sorts and filters from the header arrows. Column '#' restores chronological order.",
                len(FIGURE_COLUMNS))
    write_figures_table(ws)
    path = os.path.join(HERE, FIGURES_FILE)
    wb.save(path)
    return path


if __name__ == "__main__":
    print(build_figures())
