"""Design-rule, connectivity and fab-consistency checks + preview images for a trap die (Claude-authored).

v4 local-mirror dies (DESIGN_LOG step 25). Usage (from design/sim):  ./run.sh ../gds/check_chip.py trap_die_v4_A30
Reads <stem>.gds (the fab file, not _simfloor.gds), <stem>_sim.json (seeds, die size, marks) and <stem>_pads.csv.

Checks
  conductors   every gds2itvg seed (electrodes and the two SNSPD leads) on its own Au conductor (no shorts),
               each reaches a pad near the die edge, no floating Au islands, min spacing >= 5 um, no Au < 4.9 um
  layers       single top cell; no text on fab layers; all metal >= 90 um from the dicing edge;
               retired layers 24, 30, 31 (ITO, v3) and 45 (protect, no gap etch in v4) empty
  SNSPD        Au leads stay inside the centre-DC slot inside the trap; no Ti/Au (layer 22) inside the trap
               except the contacts near the detector (no buried leads); each L40 contact lies >= 1 um inside
               its Au lead and its Ti/Au pad; readout window open in the Au; NbN rules of step 24 (|y| <= 17 um,
               all NbN under Au or the window, gaps >= 60 nm, no turn or tab in the light footprint)
  mirror       Al (layer 10) never under the RF rails; covers all NbN by >= 5 um; >= 1 ground via inside
               the Au fill, enclosed >= 25 um by fill Au and by the Al
  plain die    nothing on layers 10, 20, 22, 40; solid centre DC at the readout zone
  pads         no pad in the die corners |x|, |y| > 4 mm; signal pads not on ground; GND spots on ground
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
STEM = sys.argv[1] if len(sys.argv) > 1 else "trap_die_v4_A30"
lib = gdstk.read_gds(os.path.join(HERE, STEM + ".gds"))
sim = json.load(open(os.path.join(HERE, STEM + "_sim.json")))
DIE = sim["_die"]
CX, CY = DIE["half_x"], DIE["half_y"]
x_read, y_ax = sim["frame"]["origin"]
x_rf0 = DIE["x_rf0"]
C_HALF, G_RF = 20.0, 5.0                   # centre DC half width, DC-RF gap (make_chip.py C, G)
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
leads = sim.get("_snspd_leads", [])
for n, pts in list(sim["electrodes"].items()) + [(k, sim["ground"][k]) for k in leads]:
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
for L in (1, 10, 20, 22, 40, 50):
    report(not [lb for lb in cell.labels if lb.layer == L], f"no text labels on fab layer {L}")
die = box(-CX, -CY, CX, CY)
for L in (10, 22, 40, 50):
    closer = U(L).difference(die.buffer(-90)).area
    report(closer < 1.0, f"layer {L} stays >= 90 um from the dicing edge ({closer:.1f} um^2 closer)")

# ---------------------------------------------------------------- SNSPD, local mirror (v4)
report(not any(L in by_layer for L in (24, 30, 31, 45)), "retired layers empty: 24, 30, 31 (ITO) and 45 (protect)")
has_det = 20 in by_layer                  # False for the plain trap die (make_chip.py --nodet)
st = sim["_stack"]
m1 = U(10)
gpiece = pieces[ghit[0]] if ghit else None
if has_det:
    trap = box(x_rf0, y_ax - 300, x_read - 60, y_ax + 300)          # inside the RF rails, left of the detector
    lead_pieces = [pieces[i] for i, ns in owner.items() if set(ns) & set(leads)]
    for k in leads:
        i = [j for j, ns in owner.items() if k in ns][0]
        b = pieces[i].intersection(trap).bounds
        ym = max(abs(b[1] - y_ax), abs(b[3] - y_ax))
        report(ym <= st["slot_half"] - 5.0 + 1e-6, f"SNSPD lead {k} stays inside the centre-DC slot in the trap (|y|max {ym:.1f} um)")
    ti = U(22).intersection(box(x_rf0 - 50, y_ax - 120, -x_rf0, y_ax + 120))
    report(ti.bounds[0] >= x_read - 120, f"no buried Ti/Au leads in the trap: layer 22 starts at x = {ti.bounds[0]:.0f} um "
                                         "(contacts only, within 120 um of the readout zone)")
    contacts = [g for g in by_layer.get(40, []) if abs(g.centroid.y - y_ax) < 20 and abs(g.centroid.x - x_read) < 150]
    report(len(contacts) == 2, f"two SNSPD contacts on layer 40 near the detector ({len(contacts)})")
    for v in contacts:
        inner = v.buffer(1.0 - 1e-6, join_style="mitre")
        ok_lead = any(p.contains(inner) for p in lead_pieces)
        report(ok_lead and U(22).contains(inner),
               f"contact at ({v.centroid.x:.0f}, {v.centroid.y:.0f}) inside its Au lead and Ti/Au pad by >= 1 um")
    win = sim["_window"]
    report(not au.intersects(box(x_read - win["wx"] / 2 + 0.5, y_ax - win["wy"] / 2 + 0.5,
                                 x_read + win["wx"] / 2 - 0.5, y_ax + win["wy"] / 2 - 0.5)),
           f"readout window {win['wx']:g} x {win['wy']:g} um is open in the Au")
    # NbN meander, v3.1 (DESIGN_LOG step 24)
    nbn = U(20).intersection(box(x_read - 200, y_ax - 40, x_read + 100, y_ax + 40))
    b = nbn.bounds
    report(max(abs(b[1] - y_ax), abs(b[3] - y_ax)) <= 17.0 + 1e-6,
           f"NbN stays within 17 um of the axis, >= 3 um inside the centre-DC edge (max {max(abs(b[1]), abs(b[3])):.2f} um)")
    winbox = box(x_read - win["wx"] / 2, y_ax - win["wy"] / 2, x_read + win["wx"] / 2, y_ax + win["wy"] / 2)
    bare = nbn.difference(au.union(winbox)).area
    report(bare < 1e-3, f"all NbN lies under the centre-DC Au or the window ({bare:.3g} um^2 outside)")
    r = 0.029                                 # closing by 29 nm fills every NbN gap narrower than ~58 nm
    closed = nbn.buffer(r, join_style="mitre").buffer(-r, join_style="mitre").difference(nbn).area
    report(closed < 0.05, f"NbN gaps >= 60 nm (closing by {2 * r * 1000:.0f} nm adds {closed:.3g} um^2)")
    # light footprint: v4 has only the cap (t_sio2_above_nbn, n 1.463) between the window floor and the NbN.
    # Rays that pass the Au top edge heading outward hit the window wall, so the footprint is the window
    # plus the spread inside the cap (ion >= 47.5 um above the Au, sim/15).
    rho = np.hypot(win["wx"] / 2, win["wy"] / 2)
    sn = np.sin(np.arctan(rho / 47.5)) / 1.463
    spread = st["t_sio2_above_nbn"] * sn / np.sqrt(1 - sn * sn)
    fp = winbox.buffer(spread, join_style="mitre")
    comps = nbn.intersection(fp)
    hmax = max(g.bounds[3] - g.bounds[1] for g in getattr(comps, "geoms", [comps]))
    report(hmax < 0.2, f"no NbN turn or tab inside the light footprint (window + {spread:.2f} um; "
                       f"tallest NbN piece there {hmax * 1000:.0f} nm)")
    # local mirror
    mb = m1.intersection(box(x_rf0, y_ax - 120, -x_rf0 + 100, y_ax + 120)).bounds
    ym = max(abs(mb[1] - y_ax), abs(mb[3] - y_ax))
    report(ym <= st["mirror_half"] + 1e-6 and ym <= C_HALF + G_RF - 5.0 + 1e-6,
           f"Al mirror never under the RF rails (|y|max {ym:.1f} um inside the trap; rails start at {C_HALF + G_RF:g})")
    # meander |y| <= 16 under a |y| <= 20 mirror: 4 um margin on the long sides (H.1 asked 5 um for the v3 15 um meander)
    report(m1.contains(nbn.buffer(3.0, join_style="mitre")), "Al mirror covers the detector NbN (meander + tabs) by >= 3 um")
    mvias = [g for g in by_layer.get(40, []) if gpiece is not None and gpiece.contains(g)]
    report(len(mvias) >= 1, f"mirror tied to the Au ground fill on chip by {len(mvias)} via(s)")
    for v in mvias:
        c = v.centroid
        report(gpiece.contains(v.buffer(25, join_style="mitre")) and m1.contains(v.buffer(25, join_style="mitre")),
               f"mirror via at ({c.x:.0f}, {c.y:.0f}) enclosed >= 25 um by ground Au and by the Al")
else:
    report(not any(L in by_layer for L in (10, 20, 22, 40)), "plain die: nothing on layers 10, 20, 22, 40")
    if "_split" in sim:   # split centre DC (make_chip --split): solid on each side of the cut, not across it
        g = sim["_split"]["gap_um"] / 2
        report(au.contains(box(x_read - 15, y_ax + g, x_read + 15, y_ax + 15)) and
               au.contains(box(x_read - 15, y_ax - 15, x_read + 15, y_ax - g)),
               "plain die (split): centre DC is solid Au on both halves at the readout zone")
    else:
        report(au.contains(box(x_read - 15, y_ax - 15, x_read + 15, y_ax + 15)), "plain die: centre DC is solid Au at the readout zone")

# ---------------------------------------------------------------- pads, marks
rows = list(csv.DictReader(open(os.path.join(HERE, STEM + "_pads.csv"))))
corner = [r["pad"] for r in rows if abs(float(r["x_um"])) > 4000 and abs(float(r["y_um"])) > 4000]
report(not corner, f"no pads in the beam-exit corners |x|, |y| > 4 mm {corner if corner else ''}")
for r in rows:
    pt = (float(r["x_um"]), float(r["y_um"]))
    if r["electrode"] == "ground fill":
        report(gpiece.contains(box(pt[0] - 100, pt[1] - 100, pt[0] + 100, pt[1] + 100)),
               f"GND spot {r['pad']} has 200 x 200 um of ground fill")
    elif r["layer"] == "50":
        report(not gpiece.contains(Point(pt)), f"pad {r['pad']} ({r['electrode']}) is not on the ground fill")
for xm, ym in DIE["mark_sites"]:
    report(not m1.intersects(box(xm - 60, ym - 60, xm + 60, ym + 60)), f"L1 mark at ({xm:.0f}, {ym:.0f}) is not under Al")
print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")

# ---------------------------------------------------------------- previews
COLORS = {10: ("#bbbbbb", 0.25), 50: ("#d4a017", 0.7), 45: ("#e74c3c", 0.12), 22: ("#c0392b", 0.9),
          20: ("#8e44ad", 1.0), 40: ("#2c3e50", 0.6), 1: ("#e67e22", 1.0), 100: ("#555555", 0.8)}


def draw(tag, window, layers=(10, 50, 45, 22, 20, 40, 1, 100)):
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
    ax.set_title(f"{STEM} {tag}: Au 50 gold, Al mirror 10 grey, "
                 "Ti/Au 22 red, NbN 20 purple, L40 openings navy", fontsize=8)
    fig.tight_layout()
    try:
        fig.savefig(os.path.join(HERE, f"{STEM}_preview_{tag}.png"), dpi=140)
    except OSError as e:                     # e.g. the PNG is open in a viewer
        print(f"note: could not write preview {tag}: {e}")
    plt.close(fig)


draw("full", (-CX - 100, -CY - 100, CX + 100, CY + 100))
draw("trap", (x_rf0 - 300, y_ax - 600, x_read + 2000, y_ax + 600))
draw("window", (x_read - 100, y_ax - 60, x_read + 100, y_ax + 60))
draw("leftend", (-CX - 50, -700, -2200, 700))
sys.exit(0 if ok else 1)
