"""Design-rule, connectivity and fab-consistency checks + preview images for a trap die (Claude-authored).

Usage (from design/sim):  ./run.sh ../gds/check_chip.py trap_die_v2_A30
Reads <stem>.gds, <stem>_sim.json (seeds, die size, mark sites) and <stem>_pads.csv.

Checks
  conductors   every gds2itvg seed on its own Au conductor (no shorts), every electrode reaches a
               pad near the die edge, no floating Au islands, min spacing >= 5 um, no Au < 4.9 um wide
  layers       single top cell; no text on fab layers; all metal >= 90 um from the dicing edge
  SNSPD        leads within 19 um of the axis inside the trap (under the centre DC, never under RF);
               buried ITO within 18 um of the axis; M1 via > 20 um from the leads
               (plain die without SNSPD: nothing on layers 20-31, solid centre DC at the readout zone)
  D2 / pads    electrode Au >= 20 um from D2 openings; every bond/probe D2 opening covered by L45;
               readout window covered by L45; signal pads not on ground; GND spots on ground
  marks        L1 marks not under Al
Writes <stem>_preview_{full,trap,window,leftend}.png
"""

import csv
import json
import os
import sys

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from shapely.geometry import Point, Polygon, box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
STEM = sys.argv[1] if len(sys.argv) > 1 else "trap_die_v2_A30"
lib = gdstk.read_gds(os.path.join(HERE, STEM + ".gds"))
sim = json.load(open(os.path.join(HERE, STEM + "_sim.json")))
DIE = sim["_die"]
CX, CY = DIE["half_x"], DIE["half_y"]
x_read, y_ax = sim["frame"]["origin"]
x_rf0 = DIE["x_rf0"]
ok = True


def report(cond, msg):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + msg)


tops = lib.top_level()
report(len(tops) == 1, f"single top cell ({[c.name for c in tops]})")
cell = tops[0]
by_layer = {}
for p in cell.get_polygons():
    by_layer.setdefault(p.layer, []).append(Polygon(p.points).buffer(0))


def U(L):
    return unary_union(by_layer.get(L, []))


# ---------------------------------------------------------------- conductors on layer 50
au = U(50)
pieces = list(au.geoms) if hasattr(au, "geoms") else [au]
owner = {}
for n, pts in sim["electrodes"].items():
    for pt in pts:
        hit = [i for i, g in enumerate(pieces) if g.contains(Point(pt))]
        report(len(hit) == 1, f"seed of electrode {n} at {pt} lies on metal")
        if hit:
            owner.setdefault(hit[0], set()).add(n)
gseed = sim["ground"]["99"][0]
ghit = [i for i, g in enumerate(pieces) if g.contains(Point(gseed))]
report(len(ghit) == 1, "ground seed lies on metal")
shorted = {i: ns for i, ns in owner.items() if len(ns) > 1}
report(not shorted, f"no two electrodes share a conductor {shorted if shorted else ''}")
report(not (ghit and ghit[0] in owner), "no electrode is shorted to ground")
for i, ns in owner.items():
    b = pieces[i].bounds
    edge = min(CX - max(abs(b[0]), abs(b[2])), CY - max(abs(b[1]), abs(b[3])))
    report(edge < 400, f"electrode {sorted(ns)} reaches a pad near the die edge ({edge:.0f} um from it)")
floating = [g for i, g in enumerate(pieces) if i not in owner and i not in ghit]
report(not floating, f"no floating Au islands ({len(floating)} found"
       + (f", e.g. at ({floating[0].centroid.x:.0f}, {floating[0].centroid.y:.0f}))" if floating else ")"))
ids = list(owner) + ghit
dmin, pair = np.inf, None
for a in range(len(ids)):
    for b in range(a + 1, len(ids)):
        d = pieces[ids[a]].distance(pieces[ids[b]])
        if d < dmin:
            dmin, pair = d, (owner.get(ids[a], "gnd"), owner.get(ids[b], "gnd"))
report(dmin >= 5.0 - 1e-6, f"minimum spacing between conductors {dmin:.2f} um ({pair})")
thin = au.buffer(-2.45, join_style="mitre").buffer(2.45, join_style="mitre")
report(au.difference(thin).area < 50.0, f"features narrower than 4.9 um: {au.difference(thin).area:.1f} um^2 of Au")

# ---------------------------------------------------------------- layers, edge, text
for L in (1, 10, 20, 22, 24, 30, 31, 40, 45, 50):
    report(not [lb for lb in cell.labels if lb.layer == L], f"no text labels on fab layer {L}")
die = box(-CX, -CY, CX, CY)
for L in (10, 22, 30, 31, 40, 50):
    closer = U(L).difference(die.buffer(-90)).area
    report(closer < 1.0, f"layer {L} stays >= 90 um from the dicing edge ({closer:.1f} um^2 closer)")

# ---------------------------------------------------------------- SNSPD routing, ITO, vias
has_det = 20 in by_layer                  # False for the plain trap die (make_chip.py --nodet)
if has_det:
    leads = U(22)
    seg = leads.intersection(box(x_rf0, y_ax - 300, x_read - 60, y_ax + 300))
    ymax = max(abs(y - y_ax) for g in getattr(seg, "geoms", [seg]) for x, y in g.exterior.coords)
    report(ymax < 19.0, f"SNSPD leads stay under the centre DC inside the trap (|y - y_axis|max = {ymax:.1f} um)")
    itob = U(31)
    near_trap = [g for g in getattr(itob, "geoms", [itob]) if abs(g.centroid.y - y_ax) < 300 and g.centroid.x > x_rf0]
    report(all(abs(y - y_ax) <= 18.01 for g in near_trap for x, y in g.exterior.coords),
           "buried ITO stays within 18 um of the axis (never under RF)")
    report(U(24).distance(leads) > 20.0, f"M1 via > 20 um from SNSPD leads ({U(24).distance(leads):.1f} um)")
else:
    report(not any(L in by_layer for L in (20, 22, 24, 30, 31)), "plain die: nothing on SNSPD/ITO layers 20, 22, 24, 30, 31")
    report(au.contains(box(x_read - 15, y_ax - 15, x_read + 15, y_ax + 15)), "plain die: centre DC is solid Au at the readout zone")

# ---------------------------------------------------------------- D2 openings, protect, pads, marks
d2_big = unary_union([g for g in by_layer.get(40, []) if g.area > 2000])    # bond/probe openings
for i, ns in owner.items():
    report(pieces[i].distance(d2_big) >= 20.0, f"electrode {sorted(ns)} Au >= 20 um from D2 openings")
prot = U(45)
report(d2_big.difference(prot).area < 1.0, "every bond/probe D2 opening is covered by L45 protect")
if has_det:
    report(prot.contains(box(x_read - 15, y_ax - 15, x_read + 15, y_ax + 15)), "readout window covered by L45")
rows = list(csv.DictReader(open(os.path.join(HERE, STEM + "_pads.csv"))))
gpiece = pieces[ghit[0]] if ghit else None
for r in rows:
    pt = (float(r["x_um"]), float(r["y_um"]))
    if r["electrode"] == "ground fill":
        report(gpiece.contains(box(pt[0] - 100, pt[1] - 100, pt[0] + 100, pt[1] + 100)),
               f"GND spot {r['pad']} has 200 x 200 um of ground fill")
    elif r["electrode"] == "ground plane":
        report(d2_big.contains(Point(pt)), f"M1 pad {r['pad']} sits in a D2 opening")
    elif r["layer"] == "50":
        report(not gpiece.contains(Point(pt)), f"pad {r['pad']} ({r['electrode']}) is not on the ground fill")
m1 = U(10)
for xm, ym in DIE["mark_sites"]:
    report(not m1.intersects(box(xm - 60, ym - 60, xm + 60, ym + 60)), f"L1 mark at ({xm:.0f}, {ym:.0f}) is not under Al")
print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")

# ---------------------------------------------------------------- previews
COLORS = {10: ("#bbbbbb", 0.25), 50: ("#d4a017", 0.7), 45: ("#e74c3c", 0.12), 22: ("#c0392b", 0.9),
          20: ("#8e44ad", 1.0), 30: ("#16a085", 0.5), 31: ("#2ecc71", 0.5), 24: ("#000000", 1.0),
          40: ("#2c3e50", 0.6), 1: ("#e67e22", 1.0), 100: ("#555555", 0.8)}


def draw(tag, window, layers=(10, 50, 45, 31, 30, 22, 20, 24, 40, 1, 100)):
    W = box(*window)
    asp = (window[3] - window[1]) / (window[2] - window[0])
    fig, ax = plt.subplots(figsize=(12, max(12 * asp, 2.5) + 0.6))
    for L in layers:
        col, al = COLORS.get(L, ("#999999", 0.5))
        for g in by_layer.get(L, []):
            if not g.intersects(W):
                continue
            gi = g.intersection(W)
            for part in getattr(gi, "geoms", [gi]):
                if part.geom_type == "Polygon":
                    xs, ys = part.exterior.xy
                    ax.fill(xs, ys, color=col, alpha=al, lw=0)
    ax.plot(*die.exterior.xy, "k-", lw=1)
    ax.set_xlim(window[0], window[2])
    ax.set_ylim(window[1], window[3])
    ax.set_aspect("equal")
    ax.set_title(f"{STEM} {tag}: Au 50 gold, M1 grey, L45 protect pink, buried ITO 31 green, top ITO 30 teal, "
                 "SNSPD leads 22 red, NbN 20 purple, D2 open 40 navy", fontsize=8)
    fig.tight_layout()
    try:
        fig.savefig(os.path.join(HERE, f"{STEM}_preview_{tag}.png"), dpi=140)
    except OSError as e:                     # e.g. the PNG is open in a viewer
        print(f"note: could not write preview {tag}: {e}")
    plt.close(fig)


draw("full", (-CX - 100, -CY - 100, CX + 100, CY + 100))
draw("trap", (x_rf0 - 300, y_ax - 600, x_read + 2000, y_ax + 600))
draw("window", (x_read - 100, y_ax - 60, x_read + 100, y_ax + 60))
draw("leftend", (-CX - 50, -CY - 50, -2200, CY + 50))
sys.exit(0 if ok else 1)
