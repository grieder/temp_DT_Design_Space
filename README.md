# Digital Twin Design Landscape: web page

A single static page (`index.html`) with:
- **Interactive scatter:** choose any rubric axis for X, Y, color and marker size; adjust label size and marker scale; toggle labels and candidate anchors. Hover shows all seven scores; click shows the fingerprint.
- **Fingerprint panel:** six-axis spider in the manuscript's spoke order.
- **Sortable score table.**
- **Place your system:** enter six scores by hand, or load or paste the JSON produced by the scoring skill. Added systems appear as stars. All of this runs in the visitor's browser; nothing is uploaded.

## Build
```bash
python build_site.py --anchors ../dt_rubric_scripts/anchors.json   # writes index.html
```
`anchors.json` is the single source of truth, shared with `plot_landscape.py`. Rebuild after every rubric or score change.

## Host
`index.html` is self-contained apart from two CDN requests (d3 7.9.0 from cdnjs, Inter from Google Fonts). Copy it to any static host: the group website, GitHub Pages, or Netlify. It supports light and dark mode.

## Score-file schema (what the skill should output)
```json
{"name": "My twin", "ref": "Author et al., Journal 2026",
 "scores": {"1": 1.2, "2": 1.5, "3": 0.8, "4": 1.0, "5": 2.0, "6": 1.0}}
```
A list of such objects is also accepted. Each score is checked against the axis ranges in `anchors.json`.

## Community submissions
Visitors add a system locally, then use **Submit for review**. That opens a GitHub issue (form `submit-system.yml`) with the score file filled in. Maintainers run `add_submission.py` to list it as pending (hollow triangle), then `add_submission.py --verify` after checking the scores (filled diamond). Rebuild after each change.

## Axes are data
Axis order, names, ranges, tick labels, color-bar ends, and highlight bands all come from `anchors.json`. Adding an accepted axis is a data change; `build_site.py` refuses to build until every system has a score for every axis. The axis proposal process is in `CONTRIBUTING.md`.

## Team preview (before launch)
```bash
python build_site.py --offline --draft "Team preview — please do not share outside the group" --out index_team.html
```
- **One self-contained file** (about 310 KB): d3 is embedded, so it works from a shared drive, an email attachment, or offline. Inter falls back to the system sans-serif when offline.
- **Draft banner** across the top.
- **No submissions yet:** the Submit button is hidden. Teammates use **Download score file** and send you the JSON; add it with `add_submission.py`.
- **Skill link** names the .skill file, so send `digital-twin-scorer.skill` alongside the page.

## Before launch
- Rebuild with `--repo-url https://github.com/ORG/REPO` (enables Submit for review) and `--skill-url <download link>`, without `--draft`.
- Copy `dt_repo/.github/ISSUE_TEMPLATE/` and `CONTRIBUTING.md` into that repository.
