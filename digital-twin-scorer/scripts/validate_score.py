#!/usr/bin/env python3
"""Check a score file against the rubric before it is shared or submitted.

Usage: python validate_score.py score.json [--anchors ../assets/anchors.json] [--check-doi]
Exits 0 when valid; prints every problem otherwise. --check-doi also asks
doi.org (and Crossref/DataCite for the title) whether the DOI is registered. The same rules are
applied by the website and by add_submission.py.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASIS = {"E", "I", "T", "U"}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")   # bare DOI, no https://doi.org/ prefix


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "digital-twin-scorer/1.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def check_doi_online(doi):
    """Return (ok, message). ok is None when the network check could not be done."""
    q = urllib.parse.quote(doi, safe="/")
    try:
        h = fetch_json(f"https://doi.org/api/handles/{q}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, f"DOI {doi} is not registered at doi.org"
        return None, f"doi.org check failed (HTTP {e.code})"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, f"could not reach doi.org ({e})"
    if h.get("responseCode") != 1:
        return False, f"DOI {doi} is not registered at doi.org"
    for api, get in (("Crossref", lambda d: d["message"]["title"][0]),
                     ("DataCite", lambda d: d["data"]["attributes"]["titles"][0]["title"])):
        url = (f"https://api.crossref.org/works/{q}" if api == "Crossref"
               else f"https://api.datacite.org/dois/{q}")
        try:
            return True, f"DOI resolves ({api}): {get(fetch_json(url))}"
        except Exception:
            continue
    return True, "DOI resolves, but no title metadata was found"


def check(score, data):
    errs, warns = [], []
    axes, order = data["axes"], data["axis_order"]
    for field in ("name", "ref", "doi", "scores", "evidence", "rubric_version"):
        if field not in score:
            errs.append(f"missing field '{field}'")
    if errs:
        return errs, warns
    if not DOI_RE.match(str(score["doi"]).strip()):
        errs.append("doi must be a bare DOI such as 10.1038/s41586-023-06734-w "
                    "(no https://doi.org/ prefix)")
    if score["rubric_version"] != data["version"]:
        warns.append(f"scored with rubric v{score['rubric_version']}, "
                     f"current is v{data['version']}")
    for a in order:
        v = score["scores"].get(a)
        if not isinstance(v, (int, float)):
            errs.append(f"axis {a}: score missing or not a number")
            continue
        lo, hi = axes[a]["min"], axes[a]["max"]
        if not lo <= v <= hi:
            errs.append(f"axis {a}: {v} outside [{lo}, {hi}]")
        if round(v, 1) != v:
            warns.append(f"axis {a}: {v} has more than one decimal place")
        ev = score["evidence"].get(a)
        if not isinstance(ev, dict):
            errs.append(f"axis {a}: no evidence entry")
            continue
        if ev.get("basis") not in BASIS:
            errs.append(f"axis {a}: basis must be one of {sorted(BASIS)}")
        if not ev.get("rationale"):
            errs.append(f"axis {a}: empty rationale")
        if ev.get("basis") == "E" and not ev.get("location"):
            warns.append(f"axis {a}: basis E but no location in the paper")
        if ev.get("basis") == "T" and a != "3":
            errs.append(f"axis {a}: basis T is only allowed on Axis 3")
    # R4: no virtual model means zero on Axes 1, 2 and 4
    if score.get("no_virtual_model"):
        for a in ("1", "2", "4"):
            if score["scores"].get(a, 0) != 0:
                errs.append(f"R4: no_virtual_model is true but axis {a} is not 0")
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("score")
    ap.add_argument("--check-doi", action="store_true", help="look the DOI up at doi.org")
    ap.add_argument("--anchors", default=str(HERE.parent / "assets" / "anchors.json"))
    args = ap.parse_args()
    data = json.loads(Path(args.anchors).read_text())
    score = json.loads(Path(args.score).read_text())
    errs, warns = check(score, data)
    if args.check_doi and not any("doi" in e for e in errs):
        ok, msg = check_doi_online(score["doi"].strip())
        if ok is False:
            errs.append(msg)
        elif ok is None:
            warns.append(msg)
        else:
            print(msg)
    for w in warns:
        print("warning:", w)
    for e in errs:
        print("error:", e)
    print("valid" if not errs else f"{len(errs)} error(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
