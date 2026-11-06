#!/usr/bin/env python3
"""Validate anchors.json and build index.html from template.html.

Usage:
    python build_site.py                                   # public build: d3 from CDN
    python build_site.py --offline --draft "Team preview"  # single file that works offline
    python build_site.py --repo-url https://github.com/ORG/REPO   # enable Submit for review

Rebuild whenever anchors.json changes; the page has no other data source.
The build fails if any system lacks a score for any axis in axis_order, so a
new axis cannot be published until every listed system has been scored.
"""
import argparse
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED_AXIS_KEYS = {"name", "short", "label", "min", "max", "scale", "cbar"}
SCALES = {"linear", "diverging", "log10", "ladder"}
D3_CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>'


def validate(data):
    errors = []
    order = data.get("axis_order", [])
    axes = data.get("axes", {})
    statuses = set(data.get("statuses", {}))
    for a in order:
        if a not in axes:
            errors.append(f"axis {a} is in axis_order but has no entry in axes")
            continue
        missing = REQUIRED_AXIS_KEYS - set(axes[a])
        if missing:
            errors.append(f"axis {a} is missing {sorted(missing)}")
        if axes[a].get("scale") not in SCALES:
            errors.append(f"axis {a} scale must be one of {sorted(SCALES)}")
        if axes[a].get("min", 0) >= axes[a].get("max", 0):
            errors.append(f"axis {a} needs min < max")
    names = set()
    for s in data.get("systems", []):
        n = s.get("name", "?")
        if n in names:
            errors.append(f"duplicate system name: {n}")
        names.add(n)
        if s.get("status") not in statuses:
            errors.append(f"{n}: status '{s.get('status')}' is not in statuses")
        for a in order:
            v = s.get("scores", {}).get(a)
            if not isinstance(v, (int, float)):
                errors.append(f"{n}: no score for axis {a}")
            elif a in axes and not axes[a]["min"] <= v <= axes[a]["max"]:
                errors.append(f"{n}: axis {a} score {v} outside "
                              f"[{axes[a]['min']}, {axes[a]['max']}]")
    return errors


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument("--anchors", default=str(HERE.parent / "dt_rubric_scripts" / "anchors.json"))
ap.add_argument("--out", default=str(HERE / "index.html"))
ap.add_argument("--offline", action="store_true",
                help="inline d3 (vendor/d3.min.js) so the file works without internet")
ap.add_argument("--draft", metavar="TEXT", help="show a banner, e.g. 'Team preview: do not share'")
ap.add_argument("--repo-url", default="", help="GitHub repository for submissions")
ap.add_argument("--skill-url", default="", help="download link for digital-twin-scorer.skill")
args = ap.parse_args()

data = json.loads(Path(args.anchors).read_text())
errs = validate(data)
if errs:
    print("anchors.json failed validation:\n  " + "\n  ".join(errs))
    sys.exit(1)
page = (HERE / "template.html").read_text()
page = page.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
page = page.replace('/*REPO_URL*/""', json.dumps(args.repo_url.rstrip("/")))
page = page.replace('/*SKILL_URL*/""', json.dumps(args.skill_url))
if args.offline:
    d3 = (HERE / "vendor" / "d3.min.js").read_text()
    page = page.replace("<!--D3-->", f"<script>/* d3 v7.9.0, ISC license (vendor/d3.LICENSE) */\n{d3}\n</script>")
else:
    page = page.replace("<!--D3-->", D3_CDN)
page = page.replace("<!--BANNER-->", f'<div class="banner" role="note">{html.escape(args.draft)}</div>' if args.draft else "")
out = Path(args.out)
out.write_text(page)

# Review-and-submit page, opened in a new tab by the main page.
submit_name = "submit.html" if out.name == "index.html" else out.name.replace("index", "submit")
if submit_name == out.name:
    submit_name = out.stem + "_submit.html"
page = out.read_text().replace('/*SUBMIT_PAGE*/"submit.html"', json.dumps(submit_name))
out.write_text(page)
sub = (HERE / "submit_template.html").read_text()
sub = sub.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
sub = sub.replace('/*REPO_URL*/""', json.dumps(args.repo_url.rstrip("/")))
(out.parent / submit_name).write_text(sub)
counts = {}
for s in data["systems"]:
    counts[s["status"]] = counts.get(s["status"], 0) + 1
print(f"wrote {args.out}: rubric v{data['version']}, {len(data['axis_order'])} axes, {counts}"
      f"{', offline' if args.offline else ''}{', submissions ' + ('on' if args.repo_url else 'off')}")
