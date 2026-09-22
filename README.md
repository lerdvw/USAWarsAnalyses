# USA Wars Analyses

Every US conflict from the Revolutionary War to 2026 as one Python dataset,
turned into Excel workbooks and sortable web pages.

| File | What it holds |
|---|---|
| `data.py` | The dataset: one record per conflict, CPI tables and sources |
| `build.py` | Builds the workbooks and pages from `data.py` |
| `web/` | The pages' template, stylesheet and script, which `build.py` inlines |
| `check.py` | Sanity checks on the data and on what `build.py` makes |
| `project_conventions.md` | How this repo is worked on |

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python check.py
```

The workbooks carry live formulas; Excel and LibreOffice calculate them on
open. `build.py xlsx` or `build.py pages` builds one half.
