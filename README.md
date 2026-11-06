# Digital Twin Design Landscape: web page

A single static page (`index.html`) with:
- **Interactive scatter:** choose any rubric axis for X, Y, color and marker size; adjust label size and marker scale; toggle labels and candidate anchors. Hover shows all seven scores; click shows the fingerprint.
- **Fingerprint panel:** six-axis spider in the manuscript's spoke order.
- **Sortable score table.**
- **Place your system:** enter six scores by hand, or load or paste the JSON produced by the scoring skill. Added systems appear as stars. All of this runs in the visitor's browser; nothing is uploaded.

## Build
```bash
python build_site.py --repo-url https://github.com/grieder/temp_DT_Design_Space --skill-url https://github.com/grieder/temp_DT_Design_Space/blob/main/digital-twin-scorer.skill   # writes index.html and submit.html
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
Visitors add a system locally, then use **Review and submit**. That opens `submit.html` in a new tab, which checks the fields (including that the DOI resolves at doi.org), then sends the visitor to a prefilled GitHub issue titled "Submission: ...".

The workflow `.github/workflows/submission.yml` runs when such an issue is opened. It validates the score file with `digital-twin-scorer/scripts/add_submission.py`, adds the system to `anchors.json` as `community-pending` (filled triangle), rebuilds the pages, redeploys, and comments on the issue. Invalid submissions get a comment listing the problems and a `needs-fix` label. The contact email and comments stay in the issue and are never copied into `anchors.json`.

To verify a system after re-running the skill on its paper: `python digital-twin-scorer/scripts/add_submission.py --verify "System name"`, then rebuild (filled diamond).

## Axis proposals
The **Propose a modification or new axis** button (beside the fingerprint) opens `axis.html`. Visitors choose a new axis (blank fields for everything `anchors.json` needs: name, short name, label, range, scale, ticks, color-bar ends, optional note and highlight band) or modify an existing one (prefilled; the issue lists only the differences). The page also lists open proposals, read live from GitHub issues labeled `axis-proposal`, with their 👍/👎 counts, so visitors vote on an existing issue instead of filing a duplicate. `.github/workflows/axis-proposal.yml` adds the label to new "Axis proposal ..." issues. Accepting a proposal is a manual data change to `anchors.json` plus rescoring.

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
