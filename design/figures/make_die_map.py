"""Annotated die map of the A30 trap for the report (Claude-authored).

Question: where are the pads, the RF electrode, the centre DC, the outer segments, the mirror and the
readout zone on the A30 die? Panel (a) is the whole 10 x 10 mm die; panel (b) is the trap region.

Inputs (read only):
  design/gds/trap_die_v4_A30.gds         layers 10 (Al mirror), 20 (NbN), 50 (Au), 101 (die outline)
  design/gds/trap_die_v4_A30_pads.csv    pad, electrode, role, x_um, y_um, layer
  design/gds/trap_die_v4_A30_sim.json    frame.origin and _zones (zone positions)
Model: layer-50 polygons are unioned with shapely. The RF electrode is the piece that contains (0, 67) um.
The ground fill is the largest piece. Nothing is simulated.
Outputs: design/figures/report/die_map.pdf, die_map.png, die_map.svg
Run:     cd design/sim && ./run.sh ../figures/make_die_map.py
Limitations: the label positions are hand-placed; the only computed anchor is the centre DC strip.
Leaders are drawn so that none crosses another leader or passes through another label.
"""

import csv
import json
import os

import gdstk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection
from matplotlib.path import Path
from matplotlib.patches import Polygon as MplPolygon
from shapely.affinity import scale as shp_scale
from shapely.geometry import Point, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
GDS = os.path.join(HERE, "..", "gds", "trap_die_v4_A30.gds")
PADS = os.path.join(HERE, "..", "gds", "trap_die_v4_A30_pads.csv")
SIMJ = os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json")

GREY = "#d6d5d0"     # Au, not the RF electrode
MIRROR = ps.ORANGE   # layer 10 outline
NBN = ps.AQUA        # layer 20
LEADER = dict(arrowstyle="-", lw=0.5, color=ps.INK, shrinkA=0, shrinkB=0)
WHITE_BOX = dict(fc="white", ec="none", alpha=0.9, pad=0.8)


def shp_to_path(geom):
    """Shapely polygon -> one matplotlib Path with holes (exterior and interiors wound oppositely)."""
    g = orient(geom, sign=1.0)
    verts, codes = [], []
    for ring in [g.exterior] + list(g.interiors):
        c = np.array(ring.coords)[:-1]
        verts.append(c)
        codes.append(np.array([Path.MOVETO] + [Path.LINETO] * (len(c) - 1)))
    return Path(np.vstack(verts), np.concatenate(codes))


def pieces_of(geom):
    return list(geom.geoms) if hasattr(geom, "geoms") else [geom]


def leader(ax, text, at, target, ha="left", color=ps.INK, bold=False, box_it=True, zorder=7):
    """Text at `at` with a plain leader line to `target`. Text bbox is white so it reads on the grey Au."""
    ax.annotate(text, xy=target, xytext=at, ha=ha, va="center", fontsize=8, color=color,
                fontweight="bold" if bold else "normal",
                bbox=WHITE_BOX if box_it else None,
                arrowprops=LEADER, zorder=zorder)


def main():
    ps.apply()
    lib = gdstk.read_gds(GDS)
    top = lib.top_level()[0]

    # layer 50: union, then pick RF (contains (0, 67)) and ground (largest)
    au = [Polygon(p.points).buffer(0) for p in top.get_polygons(depth=None, layer=50, datatype=0)]
    parts = pieces_of(unary_union(au))
    rf_idx = [i for i, p in enumerate(parts) if p.contains(Point(0, 67))]
    assert len(rf_idx) == 1, rf_idx
    rf_idx = rf_idx[0]
    gnd_idx = max(range(len(parts)), key=lambda i: parts[i].area)
    print(f"layer 50 pieces: {len(parts)}; RF piece {rf_idx} (area {parts[rf_idx].area:.0f} um2); "
          f"ground piece {gnd_idx} (area {parts[gnd_idx].area:.0f} um2)")
    centre_dc = parts[7]          # electrode 2 on A30: a U around the lead slot (|y| < 20 um; slot |y| < 12.5 um, to x = X_SLOT_END, 175 um; make_chip.py)

    die = np.array(top.get_polygons(depth=None, layer=101, datatype=0)[0].points)
    with open(SIMJ) as fh:
        sim = json.load(fh)
    # ITVG y = GDS x - origin, so GDS x = ITVG y + origin
    x_read = sim["_zones"]["readout_itvg_y"] + sim["frame"]["origin"][0]
    x_load = sim["_zones"]["loading_itvg_y"] + sim["frame"]["origin"][0]
    print(f"zones from sim JSON: loading GDS x = {x_load:g}, readout GDS x = {x_read:g}")
    assert x_load == -240.0 and x_read == 240.0

    pads = []
    with open(PADS, newline="") as fh:
        for row in csv.DictReader(fh):
            pads.append((row["pad"], row["electrode"], row["role"], float(row["x_um"]), float(row["y_um"])))
    pad = {p[0]: p for p in pads}

    # equal-width panels: both axes span the same horizontal extent
    W = ps.W2
    H = 8.7
    left, width = 0.09, 0.88
    fig = plt.figure(figsize=(W, H))

    # ---- panel (a): whole die, mm; xlim/ylim give room for the labels in both margins ----
    ax_w = width * W                        # inches
    a_h = ax_w * (11.2 / 15.0)              # ylim +-5.6, xlim +-7.5: equal aspect
    axa = fig.add_axes([left, 1 - 0.25 / H - a_h / H, width, a_h / H])
    paths = [shp_to_path(shp_scale(p, 0.001, 0.001, origin=(0, 0))) for p in parts]
    cols = [ps.BLUE if i == rf_idx else GREY for i in range(len(parts))]
    axa.add_collection(PathCollection(paths, facecolors=cols, edgecolors="none", zorder=1))
    axa.add_patch(MplPolygon(die / 1000.0, closed=True, fill=False, ec=ps.INK, lw=0.6, zorder=3))
    axa.plot([-5, 5], [0, 0], ls=(0, (3, 2)), color=ps.INK, lw=0.5, zorder=4)
    for name, el, role, x, y in pads:
        axa.plot(x / 1000.0, y / 1000.0, "s", ms=2.2, color=ps.INK, mec="none", zorder=5)
    axa.set_xlim(-7.5, 7.5)
    axa.set_ylim(-5.6, 5.6)
    axa.set_aspect("equal")
    axa.set_xticks([-5, -2.5, 0, 2.5, 5])
    axa.set_yticks([-5, -2.5, 0, 2.5, 5])
    axa.set_xlabel("x (mm)")
    axa.set_ylabel("y (mm)")
    axa.grid(False)

    def mm(p):
        return p[3] / 1000.0, p[4] / 1000.0

    # right margin: RF pad at the same height (y = 0); ground pad at upper right
    gnd_ur = [p for p in pads if p[1] == "ground fill" and p[3] > 0 and p[4] > 0][0]
    leader(axa, "RF pad", (6.2, 0.0), mm(pad["RF"]), box_it=False)
    leader(axa, "ground pads", (6.2, 2.9), mm(gnd_ur), box_it=False)
    # left margin: DC rows, trap axis, SNSPD pads
    leader(axa, "DC pad rows\n(top and bottom)", (-7.3, 4.3), mm(pad["TL2"]), box_it=False)
    leader(axa, "trap axis", (-7.3, 1.0), (-0.5, 0.0), box_it=False)
    leader(axa, "SNSPD pads\n(SNS, SNG)", (-7.3, -1.9), mm(pad["SNG"]), box_it=False)

    # ---- panel (b): trap region, um; same width as panel (a) ----
    b_h = ax_w * (800.0 / 1800.0)
    axb = fig.add_axes([left, 0.55 / H, width, b_h / H])
    polys = [shp_to_path(p) for p in parts]
    pc_cols = [ps.BLUE if i == rf_idx else GREY for i in range(len(parts))]
    axb.add_collection(PathCollection(polys, facecolors=pc_cols, edgecolors="none", zorder=1))
    for p in top.get_polygons(depth=None, layer=20, datatype=0):
        axb.add_patch(MplPolygon(np.array(p.points), closed=True, fc=NBN, ec="none", zorder=2))
    for p in top.get_polygons(depth=None, layer=10, datatype=0):
        axb.add_patch(MplPolygon(np.array(p.points), closed=True, fill=False, ec=MIRROR, lw=0.9, zorder=3))
    axb.axhline(0, ls=(0, (3, 2)), color=ps.INK, lw=0.5, zorder=4)
    axb.set_xlim(-900, 900)
    axb.set_ylim(-400, 400)
    axb.set_aspect("equal")
    axb.set_xlabel("x (µm)")
    axb.set_ylabel("y (µm)")
    axb.grid(False)

    # zone markers with vertical leaders up to labels at y = 330
    for x, name in [(x_load, "loading zone"), (x_read, "readout zone / SNSPD")]:
        axb.plot(x, 0, "o", ms=3.5, mfc="white", mec=ps.INK, mew=0.8, zorder=6)
        axb.annotate(name, xy=(x, 10), xytext=(x, 330), ha="center", va="center", fontsize=8,
                     bbox=WHITE_BOX, arrowprops=LEADER, zorder=7)

    # 480 um double arrow below the zones
    axb.annotate("", xy=(x_read, -330), xytext=(x_load, -330),
                 arrowprops=dict(arrowstyle="<->", lw=0.6, color=ps.INK, shrinkA=0, shrinkB=0), zorder=7)
    axb.text((x_load + x_read) / 2, -370, f"{x_read - x_load:g} µm", ha="center", va="center", fontsize=8,
             bbox=WHITE_BOX, zorder=7)

    # RF rails: white bold text placed on the upper rail, no leader
    axb.text(-650, 67, "RF rails", ha="left", va="center", fontsize=8, fontweight="bold", color="white",
             zorder=7)
    # outer DC segments: plain text on the lower band of segments, no leader
    axb.text(-430, -250, "outer DC segments (15 per side, 120 µm pitch)", ha="left", va="center", fontsize=8,
             bbox=WHITE_BOX, zorder=7)
    # centre DC: below the lower rail, leader up to the centre DC strip (anchor computed from layer 50)
    dc_box = centre_dc.intersection(box(-900, -20, -500, 20))
    dc_xy = tuple(dc_box.representative_point().coords[0])
    leader(axb, "centre DC", (-700, -170), (-700, dc_xy[1] - 1.0), ha="center")
    print("centre DC anchor (um):", tuple(round(v, 1) for v in dc_xy))
    # lead slot: to a point in the slot
    leader(axb, "lead slot", (520, -170), (100, 0.0))
    # Al mirror outline (orange text) and NbN meander (aqua text)
    leader(axb, "Al mirror (outline)", (520, 170), (268, 14), color=MIRROR)   # the outline's right end
    leader(axb, "NbN meander", (420, -60), (240, -6.0), color=NBN)

    os.makedirs(ps.OUT, exist_ok=True)
    fig.savefig(os.path.join(ps.OUT, "die_map.svg"), bbox_inches="tight")
    ps.save(fig, "die_map")
    print("wrote", os.path.join(ps.OUT, "die_map.pdf"), "and .png, .svg")


if __name__ == "__main__":
    main()
