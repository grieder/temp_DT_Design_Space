#!/usr/bin/env python3
"""Plot the digital-twin design landscape (Figure 3).

Panel (a): the spider key sits above a scatter of coupling (Axis 1) vs
forward-model fidelity (Axis 2); points are colored by a chosen axis
(default: Axis 6, autonomy), with the color bar below.
Panel (b): six-axis spider fingerprints, normalized as in Appendix A and
filled with the same color. The decision-grade VVUQ band (VVUQ >= 3 on the
0-4 ladder) is shaded on every spider so the low VVUQ of the field stays
visible; switch it off with --no-vvuq-band.

Style follows the original Figure 3: Inter font, large bold labels, straight
polygon grids, filled fingerprints with a heavy outline.

Usage:
    python plot_landscape.py                          # anchors, colored by autonomy
    python plot_landscape.py --color-axis 3           # colored by running cost
    python plot_landscape.py --include-candidates     # add candidate anchors
    python plot_landscape.py --new my_system.json     # overlay new system(s)

A --new file uses the schema of an entry in anchors.json (object or list):
    {"name": "My twin", "scores": {"1": 1.2, "2": 1.5, "3": 0.8,
     "4": 1.0, "5": 2.0, "6": 1.0}}
"""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import font_manager
from matplotlib.patches import Polygon
import numpy as np

HERE = Path(__file__).resolve().parent
HIGHLIGHT = "crimson"
# Axis order, labels, colorbar ends, and highlight bands are all read from
# anchors.json (keys: axis_order, axes[*].short/label/cbar/highlight_band), so
# adding or proposing an axis needs no change to this script.
AXIS_ORDER = []
MARKERS = {"anchor": "o", "reference": "h", "candidate": "s", "community-verified": "D",
           "community-pending": "^", "new": "*"}

FS = dict(panel=44, axis_title=32, tick=26, point=27, key=25, cbar_title=30,
          cbar_tick=26, spider_title=30)


def set_font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    family = next((f for f in ("Inter", "Helvetica", "Arial", "DejaVu Sans")
                   if f in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": family, "font.weight": "bold",
                         "axes.labelweight": "bold", "axes.linewidth": 2.0})


def normalize(axis, value, meta):
    lo, hi = meta[axis]["min"], meta[axis]["max"]
    return float(np.clip((value - lo) / (hi - lo), 0.0, 1.0))


def color_setup(axis, meta):
    lo, hi = meta[axis]["min"], meta[axis]["max"]
    cmap = plt.get_cmap("coolwarm" if lo < 0 else "viridis")
    return cmap, mcolors.Normalize(vmin=lo, vmax=hi)


def load(path, include_candidates, new_paths, include_community=False,
         include_reference=False):
    data = json.loads(Path(path).read_text())
    AXIS_ORDER[:] = data["axis_order"]
    keep = {"anchor"} | ({"reference"} if include_reference else set()) | \
        ({"candidate"} if include_candidates else set()) | \
        ({"community-verified", "community-pending"} if include_community else set())
    systems = [s for s in data["systems"] if s.get("status") in keep]
    for p in new_paths or []:
        obj = json.loads(Path(p).read_text())
        for s in (obj if isinstance(obj, list) else [obj]):
            s["status"] = "new"
            systems.append(s)
    return data["axes"], systems


# ----------------------------------------------------------------- spiders
def spoke_angles(n):
    return np.pi / 2 - 2 * np.pi * np.arange(n) / n          # clockwise


def draw_spider(ax, meta, s=None, color=None, vvuq_band=True, key=False):
    n = len(AXIS_ORDER)
    ang = spoke_angles(n)
    ux, uy = np.cos(ang), np.sin(ang)
    banded = [i for i, a in enumerate(AXIS_ORDER) if meta[a].get("highlight_band")]
    if vvuq_band:   # highlight bands (e.g. decision-grade VVUQ) from anchors.json
        half = np.pi / n * 0.55
        for i in banded:
            a = AXIS_ORDER[i]
            r0, r1 = (normalize(a, v, meta) for v in meta[a]["highlight_band"])
            a0, a1 = ang[i] - half, ang[i] + half
            band = [(r * np.cos(t), r * np.sin(t))
                    for r, t in ((r0, a0), (r1, a0), (r1, a1), (r0, a1))]
            ax.add_patch(Polygon(band, closed=True, fc=HIGHLIGHT, alpha=0.22,
                                 lw=0, zorder=0))
    for r in (0.5, 1.0):
        ax.add_patch(Polygon(np.c_[r * ux, r * uy], closed=True, fill=False,
                             ec="black", lw=2.0, zorder=1))
    for i in range(n):
        ax.plot([0, ux[i]], [0, uy[i]], color="black", lw=1.6, zorder=1)
    if s is not None:
        v = np.array([normalize(k, s["scores"][k], meta) for k in AXIS_ORDER])
        pts = np.c_[v * ux, v * uy]
        ax.add_patch(Polygon(pts, closed=True, fc=color, alpha=0.45, lw=0,
                             zorder=2))
        ax.add_patch(Polygon(pts, closed=True, fill=False, ec=color, lw=4.5,
                             joinstyle="miter", zorder=3))
    if key:
        for i in range(n):
            x, y = 1.16 * ux[i], 1.16 * uy[i]
            ha = "center" if abs(ux[i]) < 0.2 else ("left" if ux[i] > 0 else "right")
            va = "bottom" if uy[i] > 0.9 else ("top" if uy[i] < -0.9 else "center")
            is_v = i in banded
            ax.text(x, y, meta[AXIS_ORDER[i]]["short"], ha=ha, va=va,
                    fontsize=FS["key"], color=HIGHLIGHT if is_v else "black")
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.08, 1.08)
    ax.set_aspect("equal")
    ax.axis("off")


# ------------------------------------------------------------------ labels
def place_labels(ax, fig, systems, xs, ys):
    """Greedy placement: for each point try 8 positions around it and keep
    the one that overlaps least with markers, earlier labels, and the frame."""
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    pts_disp = ax.transData.transform(np.c_[xs, ys])
    frame = ax.get_window_extent(r)
    rad = 30                                  # marker radius in display px
    dirs = [(1, 0), (-1, 0), (1, 0.6), (1, -0.6), (-1, 0.6), (-1, -0.6),
            (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1)]
    guide = ax.transData.transform([(1.0, 1.0)])[0]   # dashed guide lines
    placed = []
    for i in np.argsort(-np.array(ys)):       # top to bottom
        best = None
        for k, (dx, dy) in enumerate(dirs):
            ha = "left" if dx > 0 else ("right" if dx < 0 else "center")
            va = "center" if abs(dy) < 0.8 else ("bottom" if dy > 0 else "top")
            off = np.array([dx, dy], float) * rad * 1.15
            px, py = inv.transform(pts_disp[i] + off)
            t = ax.text(px, py, systems[i]["name"], fontsize=FS["point"],
                        ha=ha, va=va, zorder=5)
            bb = t.get_window_extent(r).expanded(1.04, 1.0)
            t.remove()
            cost = 0.2 * k                    # prefer the earlier directions
            for b in placed:
                cost += max(0, min(bb.x1, b.x1) - max(bb.x0, b.x0)) * \
                        max(0, min(bb.y1, b.y1) - max(bb.y0, b.y0))
            for j, (qx, qy) in enumerate(pts_disp):
                cx = min(max(qx, bb.x0), bb.x1)
                cy = min(max(qy, bb.y0), bb.y1)
                if math.hypot(qx - cx, qy - cy) < rad * (0.6 if j == i else 1.0):
                    cost += 5000
            if bb.x0 < guide[0] < bb.x1:         # avoid crossing the guides
                cost += 900
            if bb.y0 < guide[1] < bb.y1:
                cost += 900
            cost += 40 * max(0, bb.x1 - (frame.x1 + 90))   # small overhang ok
            cost += 40 * max(0, frame.x0 - bb.x0)
            cost += 40 * max(0, bb.y1 - frame.y1) + 40 * max(0, frame.y0 - bb.y0)
            if best is None or cost < best[0]:
                best = (cost, px, py, ha, va, bb)
        _, px, py, ha, va, bb = best
        ax.text(px, py, systems[i]["name"], fontsize=FS["point"], ha=ha,
                va=va, zorder=5,
                fontweight="heavy" if systems[i]["status"] == "new" else "bold")
        placed.append(bb)


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--anchors", default=str(HERE.parent / "assets" / "anchors.json"))
    ap.add_argument("--include-candidates", action="store_true")
    ap.add_argument("--new", nargs="*", help="JSON file(s) with new systems")
    ap.add_argument("--color-axis", default="6",
                    help="axis key from anchors.json that colors points")
    ap.add_argument("--include-reference", action="store_true",
                    help="add reference anchors (skill calibration, not in the manuscript)")
    ap.add_argument("--include-community", action="store_true",
                    help="add community submissions (verified and pending)")
    ap.add_argument("--no-vvuq-band", action="store_true")
    ap.add_argument("--out", default="figure3")
    ap.add_argument("--ncols", type=int, default=2)
    args = ap.parse_args()

    set_font()
    meta, systems = load(args.anchors, args.include_candidates, args.new,
                         args.include_community, args.include_reference)
    if args.color_axis not in AXIS_ORDER:
        ap.error(f"--color-axis must be one of {AXIS_ORDER}")
    if len(systems) > 12:          # crowded map: shrink point labels a little
        FS["point"] = 21
    cmap, cnorm = color_setup(args.color_axis, meta)
    band = not args.no_vvuq_band

    def color(s):
        return cmap(cnorm(s["scores"][args.color_axis]))

    nrows = math.ceil(len(systems) / args.ncols)
    W, H = 23.0, max(17.5, 3.3 * nrows + 0.9)

    def fx(x):           # inches from the left -> figure fraction
        return x / W

    def fy(y):           # inches from the top  -> figure fraction
        return 1 - y / H

    fig = plt.figure(figsize=(W, H))

    # ---- panel (a): key above the scatter, color bar below
    fig.text(fx(0.3), fy(0.35), "a", fontsize=FS["panel"], va="top")
    key = fig.add_axes([fx(5.7), fy(4.1), fx(3.0), 3.0 / H])
    draw_spider(key, meta, vvuq_band=band, key=True)

    sc = fig.add_axes([fx(3.0), fy(13.3), fx(8.4), 8.4 / H])
    sc.axvline(1.0, ls=(0, (4, 3)), lw=2, color="black", zorder=0)
    sc.axhline(1.0, ls=(0, (4, 3)), lw=2, color="black", zorder=0)
    xs = [s["scores"]["1"] for s in systems]
    ys = [s["scores"]["2"] for s in systems]
    for s, x, y in zip(systems, xs, ys):
        marker = MARKERS.get(s["status"], "o")
        sc.scatter(x, y, s=1500 if s["status"] == "new" else 800,
                   marker=marker, color=color(s), edgecolors="none", zorder=3)
    sc.set_xlim(-0.15, 2.15)
    sc.set_ylim(-0.15, 2.15)
    sc.set_xticks([])
    sc.set_yticks([])
    for x, lab, ha in ((-0.15, "Digital Model", "left"),
                       (1.0, "Digital Shadow", "center"),
                       (2.15, "Digital Twin", "right")):
        sc.text(x, -0.22, lab, ha=ha, va="top", fontsize=FS["tick"])
    for y, lab in ((2.15, "Faithful Mirror"), (1.0, "Hybrid"),
                   (-0.15, "Surrogate")):
        sc.text(-0.2, y, lab, ha="right", va="center", fontsize=FS["tick"])
    sc.set_xlabel("Bidirectional Coupling (Loop Closure)",
                  fontsize=FS["axis_title"], labelpad=58)
    sc.set_ylabel("Forward-Model Fidelity", fontsize=FS["axis_title"])
    sc.yaxis.set_label_coords(-0.26, 0.5)
    fig.canvas.draw()
    place_labels(sc, fig, systems, xs, ys)

    title = meta[args.color_axis]["label"]
    lo_lab, hi_lab = meta[args.color_axis]["cbar"]
    cax = fig.add_axes([fx(3.0), fy(16.2), fx(8.4), 0.38 / H])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=cnorm, cmap=cmap), cax=cax,
                      orientation="horizontal")
    cb.set_ticks([])
    cb.outline.set_linewidth(2)
    cax.set_title(title, fontsize=FS["cbar_title"], fontweight="bold",
                  pad=14, loc="left")
    cax.text(0, -0.5, lo_lab, transform=cax.transAxes, ha="left", va="top",
             fontsize=FS["cbar_tick"])
    cax.text(1, -0.5, hi_lab, transform=cax.transAxes, ha="right", va="top",
             fontsize=FS["cbar_tick"])

    # ---- panel (b): fingerprints
    x0, col_w, top = 13.4, 4.7, 0.55
    row_h = (H - 0.75) / nrows
    fig.text(fx(x0 - 0.3), fy(0.35), "b", fontsize=FS["panel"], va="top")
    size = min(col_w, row_h) * 0.64
    for i, s in enumerate(systems):
        r, c = divmod(i, args.ncols)
        cx = x0 + c * col_w + col_w / 2
        cy = top + r * row_h + row_h * 0.58
        ax = fig.add_axes([fx(cx - size / 2), fy(cy + size / 2), fx(size),
                           size / H])
        draw_spider(ax, meta, s, color(s), vvuq_band=band)
        name = s["name"]
        fig.text(fx(cx), fy(cy - size / 2 - 0.12), name, ha="center",
                 va="bottom", fontsize=FS["spider_title"])

    for ext in ("png", "pdf"):
        fig.savefig(f"{args.out}.{ext}", dpi=150 if ext == "png" else None,
                    bbox_inches="tight", pad_inches=0.3)
    print(f"wrote {args.out}.png and {args.out}.pdf ({len(systems)} systems, "
          f"colored by Axis {args.color_axis})")


if __name__ == "__main__":
    main()
