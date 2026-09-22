# -*- coding: utf-8 -*-
"""
Sanity checks for the dataset and everything built from it.

    python3 build.py && python3 check.py

Prints a summary, then every failed check; exits with status 1 if any failed.
Outputs not built yet are skipped.
"""

import os

import data
from data import ROWS

HERE = os.path.dirname(os.path.abspath(__file__))
FAILED = []


def check(ok, message):
    """Record a failure; the run carries on, so every failure gets listed."""
    if not ok:
        FAILED.append(message)


def total(key):
    """A field summed over every conflict, skipping blanks."""
    return sum(row[key] for row in ROWS if row[key] is not None)


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


def scales():
    """Every authorization level has a label; print how many conflicts have each."""
    for row in ROWS:
        check(row["auth_level"] in data.LV_LABEL, f"{row['name']}: unknown authorization level {row['auth_level']}")
    counts = [f"{data.LV_LABEL[level]} {sum(row['auth_level'] == level for row in ROWS)}"
              for level in sorted(data.LV_LABEL, reverse=True)]
    print(f"authorization   {', '.join(counts)}")


def sources():
    """Sources are numbered 1..n, linked securely, and every citation exists."""
    numbers = [number for number, label, url in data.REFS]
    check(numbers == list(range(1, len(numbers) + 1)), "REFS is not numbered 1..n")
    for number, label, url in data.REFS:
        check(url is None or url.startswith("https://"), f"source {number} is not an https link")
    for row in ROWS:
        check(row["sources"] and all(1 <= n <= len(numbers) for n in row["sources"]),
              f"{row['name']}: cites a source that is not in REFS")
    cited = {n for row in ROWS for n in row["sources"]}
    print(f"sources         {len(numbers)} listed, {len(cited)} cited")


def totals():
    """Print the headline totals and how many rows lack a figure."""
    blank = sum(row["kia"] is None or row["cost_m"] is None for row in ROWS)
    print(f"KIA + MIA       {total('kia'):,}")
    print(f"casualties      {total('casualties'):,}")
    print(f"cost, then-year ${total('cost_m'):,}m")
    print(f"blank figures   {blank} rows lack a death count or a cost")


def inflation():
    """No cost is dated to a year dearer than the base month."""
    for row in ROWS:
        check(row["factor"] >= 1, f"{row['name']}: {row['cost_year']} prices sit above the base month")
    print(f"cost, {data.CPI_BASE_LABEL} ${total('cost_adj'):,.0f}m")


def crs():
    """Compare CRS's constant-dollar figures with the CPI method, war by war."""
    check(set(data.CRS_FY2011) <= {row["name"] for row in ROWS}, "CRS_FY2011 names a conflict not in ROWS")
    for row in ROWS:
        if row["crs_2011"] and row["cost_adj"]:
            ratio = row["crs_2011"] * data.CPI_BASE / 224.939 / row["cost_adj"]
            print(f"  CRS / CPI {ratio:5.2f}  {row['name']}")


# ---------------------------------------------------------------------------
# What build.py makes
# ---------------------------------------------------------------------------

def figures():
    """The Figures workbook holds every conflict in its own row, in order."""
    path = os.path.join(HERE, "US-Conflicts-1775-2026-Figures.xlsx")
    if not os.path.exists(path):
        print("figures.xlsx    not built; run build.py first")
        return
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    wb = load_workbook(path)
    ws = wb["Figures"]
    first, last = 6, 5 + len(ROWS)
    headers = [cell.value for cell in ws[5] if cell.value]
    column = {header: get_column_letter(n) for n, header in enumerate(headers, 1)}
    check(ws.tables["Figures"].ref == f"A5:{get_column_letter(len(headers))}{last}",
          "the Figures table does not cover every row and column")
    for row in ROWS:
        name = ws[f"{column['Conflict']}{5 + row['idx']}"].value.replace(" ‡", "")
        check(name == row["name"], f"Figures row {5 + row['idx']} holds {name}, not {row['name']}")
    # Each total sums every conflict's row.
    for header in headers:
        if header in ("Combat Days", "All Conflict Days", "KIA + MIA", "All Casualties") or header.startswith("Net Cost"):
            letter = column[header]
            check(ws[f"{letter}{last + 1}"].value == f"=SUM({letter}{first}:{letter}{last})",
                  f"the {header} total misses rows")
    # Each conflict is priced by its own row of the deflator sheet.
    deflator = wb["CPI_Deflator"]
    cost = column[next(h for h in headers if h.startswith("Net Cost to"))]
    adjusted = column[next(h for h in headers if h.startswith("Net Cost in"))]
    for row in ROWS:
        r = 5 + row["idx"]
        check(deflator[f"B{r}"].value == row["name"], f"CPI_Deflator row {r} is not {row['name']}")
        check(ws[f"{adjusted}{r}"].value == f'=IF({cost}{r}="","",{cost}{r}*CPI_Deflator!F{r})',
              f"Figures row {r} is priced from another conflict's deflator row")
    print(f"figures.xlsx    {len(wb.sheetnames)} sheets, {last - first + 1} rows")


if __name__ == "__main__":
    rows()
    scales()
    sources()
    totals()
    inflation()
    crs()
    figures()
    for message in FAILED:
        print("FAIL", message)
    print("\nall checks pass" if not FAILED else f"\n{len(FAILED)} check(s) failed")
    raise SystemExit(1 if FAILED else 0)
