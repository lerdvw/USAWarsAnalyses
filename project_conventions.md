# Project conventions — USAWarsAnalyses

How this repo is worked on, by a person or by Claude Code. The folder-wide
`CodingProjects/CLAUDE.md` loads only on the Mac, so the rules that must hold
everywhere are repeated here.

## Git

- Commit straight to `main`. Use a branch only when the owner says a piece of
  work is on one.
- Local commits need no permission once work is at a sensible point. Pushing,
  opening pull requests and anything else outward-facing need an explicit
  request.

## Commit messages

- **Subject:** short and imperative, naming the change (`Add the 1990s
  operations`).
- **Description:** 28 words or fewer, after a blank line. Count them; do not
  round down.
- **No `Co-Authored-By:` trailers** unless the author explicitly asks for one,
  including for AI assistants.
- Any other trailer goes below the description and does not count toward the
  limit.

## Working on the data

- `data.py` is the single source of truth. Everything else is generated from
  it; never hand-edit a generated file.
- Run `python3 check.py` after every change and before every commit. Once
  `build.py` exists, run it first so the checks cover what it builds.
- Every figure cites a numbered source. A blank beats a guess: leave a cell
  empty when no reliable figure exists, and say so in the row's text.
- Generated workbooks and pages are not committed; build them when needed.

## Backups on the Mac

A global git hook archives all of `~/CodingProjects` to iCloud after every
commit and keeps the newest 50 archives. Before landing a long run of commits
in one go, ask the owner whether to skip it for all but the last
(`git -c core.hooksPath=/dev/null commit ...`), so the run does not push out
older archives.
