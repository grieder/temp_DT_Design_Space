#!/usr/bin/env python3
"""Add a community submission (from a GitHub issue body) to anchors.json.

Usage:
    python add_submission.py --body-file issue.md --issue 12 [--anchors ../assets/anchors.json] [--check-doi]
    python add_submission.py --verify "System name"      # mark a pending system as verified

The issue body is untrusted text. Only the fenced JSON block under
"### Score file" is read; it is parsed as data and validated against the
rubric before anything is written. The contact email and comments are never
copied into anchors.json. Exit code 0: added; 1: rejected (reasons on stdout).
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_score import DOI_RE, check_doi_online  # noqa: E402


def extract(body):
    m = re.search(r"### Score file\s*```(?:json)?\s*(.*?)```", body, re.S)
    if not m:
        raise ValueError("no JSON block found under '### Score file'")
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"the score file is not valid JSON: {e}")
    if not isinstance(obj, dict):
        raise ValueError("the score file must be a JSON object")
    return obj


def clean(obj, data, check_doi):
    errs = []
    axes, order = data["axes"], data["axis_order"]
    name = obj.get("name")
    ref = obj.get("ref")
    doi = obj.get("doi")
    if not isinstance(name, str) or not name.strip() or len(name) > 80:
        errs.append("name must be a non-empty string of at most 80 characters")
    if not isinstance(ref, str) or not ref.strip() or len(ref) > 300:
        errs.append("ref must be a non-empty string of at most 300 characters")
    if not isinstance(doi, str) or not DOI_RE.match(doi.strip()):
        errs.append("doi must be a bare DOI such as 10.1038/s41586-023-06734-w")
    elif check_doi:
        ok, msg = check_doi_online(doi.strip())
        if ok is False:
            errs.append(msg)
    scores = obj.get("scores")
    out = {}
    if not isinstance(scores, dict):
        errs.append("scores must be an object")
    else:
        for a in order:
            v = scores.get(a)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                errs.append(f"axis {a}: score missing or not a number")
            elif not axes[a]["min"] <= v <= axes[a]["max"]:
                errs.append(f"axis {a}: {v} outside [{axes[a]['min']}, {axes[a]['max']}]")
            else:
                out[a] = round(float(v), 1)
        if obj.get("no_virtual_model"):
            for a in ("1", "2", "4"):
                if out.get(a, 0) != 0:
                    errs.append(f"R4: no_virtual_model is true but axis {a} is not 0")
    if errs:
        return None, errs
    rec = {"name": name.strip(), "ref": ref.strip(), "doi": doi.strip(),
           "status": "community-pending", "scores": out}
    if obj.get("no_virtual_model"):
        rec["no_virtual_model"] = True
    return rec, []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--anchors", default=str(HERE.parent / "assets" / "anchors.json"))
    ap.add_argument("--body-file")
    ap.add_argument("--issue", type=int, help="issue number, stored so the entry can be traced")
    ap.add_argument("--check-doi", action="store_true")
    ap.add_argument("--verify", metavar="NAME")
    args = ap.parse_args()
    path = Path(args.anchors)
    data = json.loads(path.read_text())

    if args.verify:
        for s in data["systems"]:
            if s["name"] == args.verify and s["status"] == "community-pending":
                s["status"] = "community-verified"
                path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
                print(f"{args.verify}: marked community-verified")
                return 0
        print(f"no pending system named {args.verify!r}")
        return 1

    if not args.body_file:
        ap.error("--body-file is required")
    try:
        obj = extract(Path(args.body_file).read_text())
    except ValueError as e:
        print(f"- {e}")
        return 1
    rec, errs = clean(obj, data, args.check_doi)
    if not errs:
        for s in data["systems"]:
            if s["name"].casefold() == rec["name"].casefold():
                errs.append(f"a system named {s['name']!r} is already listed")
            if s.get("doi", "").lower() == rec["doi"].lower():
                errs.append(f"{s['name']!r} already uses DOI {rec['doi']}")
    if errs:
        print("\n".join(f"- {e}" for e in errs))
        return 1
    if args.issue:
        rec["issue"] = args.issue
    data["systems"].append(rec)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"added {rec['name']} as community-pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
