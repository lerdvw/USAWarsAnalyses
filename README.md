# USA Wars Analyses

Every US conflict from the Revolutionary War to 2026 as one Python dataset,
turned into Excel workbooks.

| File | What it holds |
|---|---|
| `data.py` | The dataset: one record per conflict, CPI tables and sources |
| `build.py` | Builds the workbooks from `data.py` |
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
open.
