# USA Wars Analyses

Every overt US conflict from the Revolutionary War to September 2026, 75 in
all, as one Python dataset. It is built into two Excel workbooks and two web
pages whose tables scroll sideways and sort and filter on every column.

## Published pages

- [War by the Numbers](https://claude.ai/artifact/FDhjXEvzACXqbdoQZWFmEv):
  duration, casualties, and cost in then-year and August 2026 dollars
- [Wars of the Republic](https://claude.ai/artifact/C6ByzNyvwmCyCHJ9UMfXsq):
  who ordered each conflict, on what authority, why, and what happened

The links open only for people each page has been shared with.

## Files

| File | What it holds |
|---|---|
| `data.py` | The dataset: one record per conflict, CPI tables and sources |
| `build.py` | Builds the workbooks and pages from `data.py` |
| `web/` | The pages' template, stylesheet and script, which `build.py` inlines |
| `check.py` | Sanity checks on the data and on everything `build.py` makes |
| `project_conventions.md` | How this repo is worked on |

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python check.py
```

`build.py xlsx` or `build.py pages` builds one half. To link the two pages to
each other, pass their published URLs: `build.py pages <record-url>
<figures-url>`. The workbooks carry live formulas; Excel and LibreOffice
calculate them on open.

## Method

Casualties follow the Department of Veterans Affairs and DoD's Defense
Casualty Analysis System; costs before Vietnam are CRS estimates. Costs are
restated in August 2026 dollars with CPI-U from each conflict's cost-centre
year. The workbooks' Method & Sources sheet and both pages list every caveat.
