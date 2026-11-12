"""Independent checker for the SNSPD-only die snspd_die_v4 (Claude-authored).

Checks the GDS against the SNSPD-die specification, checks C1 to C13. The expected coordinates are typed
in from the specification at the top of this file. The checker does not import or read the generator.

Usage (from design/sim):  ./run.sh ../gds/check_snspd_die.py

Reads design/gds/snspd_die_v4.gds (top cell SNSPD_DIE_V4), snspd_die_v4_pads.csv, and the reference
trap_die_v4_A30.gds (used by C4 only). Units um. Every check prints PASS or FAIL with the measured number.
Exit code 0 if all checks pass, 1 if any fail, 2 if the GDS file is missing.

Why the method is what it is:
- Shapes become shapely polygons, so areas, distances and containment are one call each.
- "Inside" means the leftover area of (shape minus region) is below TOL, which tolerates float rounding.
"""

import csv
import os
import sys

import gdstk
from shapely.affinity import translate
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
GDS = os.path.join(HERE, "snspd_die_v4.gds")
PADS = os.path.join(HERE, "snspd_die_v4_pads.csv")
REF = os.path.join(HERE, "trap_die_v4_A30.gds")
TOP = "SNSPD_DIE_V4"
TOL = 1e-6                                   # um^2: a leftover below this counts as zero
N_FAIL = 0

# ---- cells: name, xc, yc, dir, layer-20 datatype (spec, "Detector cells")
CELLS = [
    ("D1", -2700, 1200, +1, 1),
    ("D2", -900, 1200, +1, 2),
    ("D3", 900, 1200, +1, 3),
    ("D4", 2700, 1200, +1, 0),
    ("D5", -2700, -1200, -1, 0),
    ("D6", -900, -1200, -1, 5),
    ("D7", 900, -1200, -1, 6),
    ("D8", 2700, -1200, -1, 7),
]
# ---- pad centres (spec, "Resulting pad centres"); a name is <cell>_S (signal) or <cell>_G (return)
PAD_CENTRES = {
    "D1_S": (-3100, 4720), "D1_G": (-3460, 4720), "D2_S": (-1300, 4720), "D2_G": (-1660, 4720),
    "D3_S": (500, 4720), "D3_G": (140, 4720), "D4_S": (2300, 4720), "D4_G": (1940, 4720),
    "D5_S": (-3460, -4720), "D5_G": (-3100, -4720), "D6_S": (-1660, -4720), "D6_G": (-1300, -4720),
    "D7_S": (140, -4720), "D7_G": (500, -4720), "D8_S": (1940, -4720), "D8_G": (2300, -4720),
}
GND_SPOTS = [(4700, 1500), (4700, -1500), (-4700, 1500), (-4700, -1500)]    # spec, "Ground pads"
MARKS = [(4300, 4830), (-4300, 4830), (4300, -4830), (-4300, -4830)]        # spec, "Marks"
FAB = {1, 10, 20, 22, 40, 50}
USED = FAB | {100, 101}
EMPTY = {24, 30, 31, 45}
T11_PTS = {"P1": (-487.5, 0), "strap": (0, 0), "P2": (487.5, 0)}          # centres of the three Au pieces
T11_ISLAND_PTS = {"A": (-300, 0), "B": (300, 0)}                           # centres of the two Al islands
T11_OPEN_X = [-425, -175, 175, 425]                                        # centres of the four openings
T11_CHAIN = [  # (opening x, Au piece at that x, Al island at that x)
    (-425, "P1", "A"), (-175, "strap", "A"), (175, "strap", "B"), (425, "P2", "B"),
]


def report(ok, msg):
    global N_FAIL
    if not ok:
        N_FAIL += 1
    print(("PASS " if ok else "FAIL ") + msg)


def load(path):
    """Read a GDS file; return (top cells, top cell, dict layer -> list of (datatype, shapely polygon))."""
    if not os.path.exists(path):
        print(f"ERROR: {path} not found. Generate it first; this checker does not write GDS files.")
        sys.exit(2)
    lib = gdstk.read_gds(path)
    tops = lib.top_level()
    cell = tops[0]
    G = {}
    for p in cell.get_polygons():
        G.setdefault(p.layer, []).append((p.datatype, Polygon(p.points).buffer(0)))
    return tops, cell, G


def merged(G, layer):
    """Union of every polygon on a layer (all datatypes)."""
    gs = [g for _, g in G.get(layer, [])]
    return unary_union(gs) if gs else Polygon()


def parts(g):
    """Separate pieces of a geometry (empty list if empty)."""
    if g.is_empty:
        return []
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def left(a, b):
    """Area of a that is not covered by b. Zero means a lies inside b."""
    return a.difference(b).area


def index_at(pieces, x, y):
    """Index of the piece that covers the point (x, y), or None."""
    for i, p in enumerate(pieces):
        if p.covers(Point(x, y)):
            return i
    return None


def cell_nbn(G, xc, yc):
    """All layer-20 polygons of one cell (those touching its 160 x 60 um region), any datatype."""
    r = box(xc - 80, yc - 30, xc + 80, yc + 30)
    gs = [g for _, g in G.get(20, []) if g.intersects(r)]
    return unary_union(gs) if gs else Polygon()


# ================================================================ load
tops, cell, G = load(GDS)
_, _, R = load(REF)                          # A30 reference die (C4)
print(f"== {GDS}: top cells {[c.name for c in tops]}")
report(len(tops) == 1 and tops[0].name == TOP, f"C0 single top cell named {TOP} (found {[c.name for c in tops]})")

au = merged(G, 50)                           # Au, merged: fill + leads + pads + T11 pieces
pieces = parts(au)
n_au = len(pieces)
fill_i = max(range(n_au), key=lambda i: pieces[i].area) if n_au else None
fill = pieces[fill_i] if n_au else Polygon()
al = merged(G, 10)
L22 = merged(G, 22)
L40 = merged(G, 40)
al_pieces = parts(al)

# ================================================================ C1
print("-- C1 layers, die outline, labels")
used = sorted(G.keys())
report(set(used) <= USED, f"C1 layers used {used}; unexpected {sorted(set(used) - USED)}")
empty = {n: len(G.get(n, [])) for n in sorted(EMPTY)}
report(not any(empty.values()), f"C1 layers 24, 30, 31, 45 empty: polygon counts {empty}")
outline = G.get(101, [])
ob = outline[0][1].bounds if len(outline) == 1 else None
ok_outline = ob is not None and all(abs(a - b) < 1e-6 for a, b in zip(ob, (-5000, -5000, 5000, 5000)))
report(ok_outline, f"C1 die outline on layer 101: {len(outline)} polygon(s), bounds {ob} (want -5000..5000)")
bad_text = [(l.layer, l.text) for l in cell.labels if l.layer in FAB]
report(not bad_text, f"C1 no text labels on fabricated layers ({len(bad_text)} found {bad_text[:5]})")

# ================================================================ C2
print("-- C2 distance from die edge")
inner = box(-4910, -4910, 4910, 4910)        # 90 um inside the 10 mm die
for L in (10, 22, 40, 50):
    a = merged(G, L).difference(inner).area
    report(a < TOL, f"C2 layer {L} within 90 um of the die edge: {a:.6f} um^2 (must be 0)")

# ================================================================ C3
print("-- C3 datatype and NbN height")
for name, xc, yc, d, dt in CELLS:
    r = box(xc - 70, yc - 20, xc + 25, yc + 20)
    hits = [(dd, g) for dd, g in G.get(20, []) if g.intersects(r)]
    wrong = [dd for dd, g in hits if dd != dt]
    if not hits:
        report(False, f"C3 {name}: no layer-20 polygon in its box")
        continue
    nb = unary_union([g for _, g in hits]).intersection(r)
    b = nb.bounds
    ymax = max(abs(b[1] - yc), abs(b[3] - yc))
    report(not wrong and ymax <= 17 + 1e-6,
           f"C3 {name}: {len(hits)} layer-20 polygon(s) in box, datatypes {sorted(set(dd for dd, _ in hits))} "
           f"(want {dt}), wrong {len(wrong)}; NbN max |y-yc| {ymax:.3f} um (<= 17)")

# ================================================================ C4
print("-- C4 match to the A30 detector (translated by (xc-240, yc))")
src_box = box(140, -20, 300, 20)             # A30 detector at x = 240
ref_areas = {L: merged(R, L).intersection(src_box).area for L in (20, 22, 40, 50)}
report(all(a > 0 for a in ref_areas.values()),
       "C4 A30 reference non-empty in box x 140..300, |y|<=20: "
       + " ".join(f"L{L} {a:.1f} um^2" for L, a in ref_areas.items()))
for name, xc, yc, d, dt in CELLS:
    res = {}
    for L in (20, 22, 40, 50):
        xmax = xc + (40 if L == 50 else 60)
        tb = box(xc - 100, yc - 20, xmax, yc + 20)
        src = translate(merged(R, L).intersection(src_box), xoff=xc - 240, yoff=yc)
        res[L] = src.intersection(tb).symmetric_difference(merged(G, L).intersection(tb)).area
    report(max(res.values()) < 0.01,
           f"C4 {name} vs A30: symmetric difference L20 {res[20]:.4f}, L22 {res[22]:.4f}, "
           f"L40 {res[40]:.4f}, L50 {res[50]:.4f} um^2 (each < 0.01)")

# ================================================================ C5
print("-- C5 readout window and NbN under Au")
for name, xc, yc, d, dt in CELLS:
    w29 = box(xc - 14.5, yc - 14.5, xc + 14.5, yc + 14.5)
    a_in = au.intersection(w29).area
    report(a_in < TOL, f"C5 {name}: Au inside the 29 x 29 um window {a_in:.6f} um^2 (must be 0)")
    w30 = box(xc - 15, yc - 15, xc + 15, yc + 15)
    nbn = cell_nbn(G, xc, yc)
    outside = nbn.difference(au.union(w30)).area
    report(outside < 1e-3 and nbn.area > 0,
           f"C5 {name}: NbN outside Au and the 30 x 30 window {outside:.6f} um^2 (< 1e-3); "
           f"NbN area {nbn.area:.1f} um^2 (must be > 0)")

# ================================================================ C6
print("-- C6 Al mirror under each cell NbN, and mirror ground via")
for name, xc, yc, d, dt in CELLS:
    nbn = cell_nbn(G, xc, yc)
    out = nbn.buffer(3, join_style="mitre").difference(al).area
    report(out < TOL and nbn.area > 0,
           f"C6 {name}: NbN (area {nbn.area:.1f} um^2) grown 3 um inside Al (layer 10), leftover {out:.6f} um^2")
    sq = [g for _, g in G.get(40, [])
          if abs(g.centroid.x - (xc - 270)) < 1 and abs(g.centroid.y - (yc - d * 130)) < 1]
    if len(sq) != 1:
        report(False, f"C6 {name}: expected one layer-40 square at ({xc - 270}, {yc - d * 130}), found {len(sq)}")
        continue
    s = sq[0]
    w = s.bounds[2] - s.bounds[0]
    h = s.bounds[3] - s.bounds[1]
    g25 = s.buffer(25, join_style="mitre")
    o_al = left(g25, al)
    o_au = left(g25, fill)
    report(abs(w - 100) < 1e-3 and abs(h - 100) < 1e-3 and o_al < TOL and o_au < TOL,
           f"C6 {name}: ground via {w:.1f} x {h:.1f} um; grown 25 um leftover in Al {o_al:.6f}, "
           f"in Au fill {o_au:.6f} um^2")

# ================================================================ C7
print("-- C7 e-beam crosses (four per cell)")
for name, xc, yc, d, dt in CELLS:
    lines = []
    ok_cell = True
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = xc + sx * 300, yc + sy * 700
            cl = L22.intersection(box(px - 15, py - 15, px + 15, py + 15))
            if cl.is_empty:
                ok_cell = False
                lines.append(f"({px},{py}) empty")
                continue
            b = cl.bounds
            w, h = b[2] - b[0], b[3] - b[1]
            if not (abs(w - 20) < 1e-3 and abs(h - 20) < 1e-3 and abs(cl.area - 76) < 0.01):
                ok_cell = False
            lines.append(f"({px},{py}) bbox {w:.2f} x {h:.2f}, area {cl.area:.3f}")
    report(ok_cell, f"C7 {name} crosses (want 20 x 20 bbox, 76 um^2): " + "; ".join(lines))

# ================================================================ C8
print("-- C8 Au conductors, pads, contact openings")
report(n_au == 20, f"C8 Au (layer 50) merged into {n_au} conductor(s) (want 20: 1 fill, 16 leads, 3 T11)")
t11_idx = {k: index_at(pieces, x, y) for k, (x, y) in T11_PTS.items()}
lead_of = {name: index_at(pieces, px, py) for name, (px, py) in PAD_CENTRES.items()}
used_idx = [i for i in lead_of.values() if i is not None]
ok_leads = (len(used_idx) == 16 and len(set(used_idx)) == 16 and fill_i not in used_idx
            and not (set(used_idx) & set(t11_idx.values())) and None not in t11_idx.values()
            and len(set(t11_idx.values())) == 3)
report(ok_leads, f"C8 each of the 16 pad centres lies in its own lead conductor (distinct {len(set(used_idx))}), "
                 f"fill piece {fill_i}, T11 pieces {t11_idx}")
label_of = {fill_i: "fill", t11_idx["P1"]: "T11 P1", t11_idx["strap"]: "T11 strap", t11_idx["P2"]: "T11 P2"}
for name, i in lead_of.items():
    if i is not None:
        label_of[i] = name
for name, (px, py) in PAD_CENTRES.items():
    i = lead_of[name]
    if i is None:
        report(False, f"C8 pad {name}: centre ({px}, {py}) is not on any Au conductor")
        continue
    rect = box(px - 60, py - 100, px + 60, py + 100)
    o = left(rect, pieces[i])
    report(o < TOL, f"C8 pad {name}: 120 x 200 um rectangle at ({px}, {py}) inside its conductor, leftover {o:.6f} um^2")
for name, xc, yc, d, dt in CELLS:
    for sy in (1, -1):
        pad = f"{name}_S" if sy == 1 else f"{name}_G"
        ylo, yhi = sorted([yc + sy * 3.5, yc + sy * 6.5])
        cont = box(xc - 92, ylo, xc - 74, yhi)           # contact opening (spec)
        cov = left(cont, L40)                             # must be a layer-40 opening
        grown = cont.buffer(1, join_style="mitre")
        lead_i = lead_of[pad]
        o_lead = left(grown, pieces[lead_i]) if lead_i is not None else float("inf")
        o_22 = left(grown, L22)
        report(cov < TOL and o_lead < TOL and o_22 < TOL,
               f"C8 {pad}: contact opening at x {xc - 92}..{xc - 74}, y {ylo:g}..{yhi:g}; grown 1 um: "
               f"leftover outside its lead {o_lead:.6f}, outside Ti/Au {o_22:.6f} um^2; opening missing {cov:.6f} um^2")

# ================================================================ C9
print("-- C9 spacing")
dmin, pair = None, None
for i in range(n_au):
    for j in range(i + 1, n_au):
        dd = pieces[i].distance(pieces[j])
        if dmin is None or dd < dmin:
            dmin, pair = dd, (i, j)
if pair is not None:
    a_name = label_of.get(pair[0], str(pair[0]))
    b_name = label_of.get(pair[1], str(pair[1]))
    report(dmin >= 5 - 1e-6, f"C9 smallest distance between two Au conductors {dmin:.3f} um, "
                             f"{a_name} <-> {b_name} (must be >= 5)")
else:
    report(False, "C9 fewer than two Au conductors")
pad_fill = [(name, box(px - 60, py - 100, px + 60, py + 100).distance(fill)) for name, (px, py) in PAD_CENTRES.items()]
worst = min(pad_fill, key=lambda t: t[1])
report(worst[1] >= 30 - 1e-6, f"C9 every bond pad rectangle is >= 30 um from the fill: minimum {worst[1]:.3f} um at {worst[0]}")

# ================================================================ C10
print("-- C10 layer-40 openings sit on Ti/Au or Al")
others, n_open = [], 0
for _, g in G.get(40, []):
    n_open += 1
    c = g.centroid
    if any((c.x - mx) ** 2 + (c.y - my) ** 2 <= 100 ** 2 for mx, my in MARKS):
        continue                                          # mark crosses are allowed here
    if left(g, L22) < TOL or left(g, al) < TOL:
        continue
    others.append((round(c.x, 1), round(c.y, 1)))
report(not others, f"C10 layer-40 openings: {n_open} total, {len(others)} on neither Ti/Au nor Al {others[:10]}")

# ================================================================ C11
print("-- C11 T3 (NbN bar, probe pads) and T11 (Au-to-Al via chain)")
R3 = box(-3400, -310, -2600, 230)
a3 = au.intersection(R3).area
report(a3 < TOL, f"C11 T3 keep-out box x -3400..-2600, y -310..230 has no Au: {a3:.6f} um^2")
bar_gs = [g for dd, g in G.get(20, []) if dd == 0 and g.intersects(box(-3100, -350, -2900, -150))]
if bar_gs:
    bb = unary_union(bar_gs).bounds
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    report(abs(cx + 3000) < 100 and abs(cy + 250) < 100,
           f"C11 T3 NbN bar (layer 20, datatype 0) around (-3000, -250): bbox centre ({cx:.1f}, {cy:.1f})")
else:
    report(False, "C11 T3 NbN bar (layer 20, datatype 0) not found around (-3000, -250)")
t3_pads = [p for p in parts(L22) if p.intersects(R3)]
t3_open = [p for p in t3_pads if any(p.covers(g.centroid) for _, g in G.get(40, []))]
report(len(t3_pads) == 4 and len(t3_open) == 4,
       f"C11 T3 probe pads: {len(t3_pads)} layer-22 pad(s) in the T3 area, {len(t3_open)} with a layer-40 opening inside")

a_pieces = al_pieces
ia, ib = index_at(a_pieces, *T11_ISLAND_PTS["A"]), index_at(a_pieces, *T11_ISLAND_PTS["B"])
au_chain_ok = True
chain_txt = []
for xo, piece_name, island_name in T11_CHAIN:
    ap = index_at(pieces, xo, 0)
    al_i = index_at(a_pieces, xo, 0)
    want_al = ia if island_name == "A" else ib
    op = [g for _, g in G.get(40, []) if abs(g.centroid.x - xo) < 1 and abs(g.centroid.y) < 1
          and abs((g.bounds[2] - g.bounds[0]) - 100) < 1e-3 and abs((g.bounds[3] - g.bounds[1]) - 100) < 1e-3]
    good = (len(op) == 1 and ap is not None and ap == t11_idx[piece_name]
            and al_i is not None and al_i == want_al)
    au_chain_ok &= good
    chain_txt.append(f"x={xo}: opening {len(op)}, Au piece {ap} (want {piece_name}), Al {al_i} (want island {island_name})")
report(au_chain_ok, "C11 T11 openings: " + "; ".join(chain_txt))
distinct = len(set(t11_idx.values())) == 3 and ia is not None and ib is not None and ia != ib
report(distinct and fill_i not in t11_idx.values(),
       f"C11 T11 chain P1 - island A - strap - island B - P2: P1, strap, P2 distinct {distinct}, "
       f"none is the fill (fill piece {fill_i}, T11 pieces {t11_idx}, islands {ia}, {ib})")
kf = fill.intersection(box(-650, -100, 650, 100)).area
report(kf < TOL, f"C11 T11 keep-out box x -650..650, y -100..100 has no Au fill: {kf:.6f} um^2")

# ================================================================ C12
print("-- C12 marks and keep-outs")
L1 = merged(G, 1)
for xm, ym in MARKS:
    cl = L1.intersection(box(xm - 60, ym - 60, xm + 60, ym + 60))
    if cl.is_empty:
        report(False, f"C12 layer-1 mark at ({xm}, {ym}) not found")
        continue
    b = cl.bounds
    w, h = b[2] - b[0], b[3] - b[1]
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    ok_cross = abs(w - 100) < 1e-3 and abs(h - 100) < 1e-3 and abs(cx - xm) < 1 and abs(cy - ym) < 1
    keep = au.intersection(box(xm - 160, ym - 140, xm + 180, ym + 140)).area
    report(ok_cross and keep < TOL,
           f"C12 mark at ({xm}, {ym}): layer-1 cross bbox {w:.1f} x {h:.1f} centred ({cx:.1f}, {cy:.1f}); "
           f"Au in keep-out x {xm - 160}..{xm + 180}, y {ym - 140}..{ym + 140}: {keep:.6f} um^2")

# ================================================================ C13
print("-- C13 pads.csv")
if not os.path.exists(PADS):
    report(False, f"C13 {PADS} not found")
else:
    rows = list(csv.DictReader(open(PADS, newline="")))
    det = {r["pad"]: (float(r["x_um"]), float(r["y_um"])) for r in rows if r["pad"] in PAD_CENTRES}
    gnd = sorted((float(r["x_um"]), float(r["y_um"])) for r in rows if r["pad"].upper().startswith("GND"))
    det_ok = len(det) == 16 and all(abs(det[k][0] - PAD_CENTRES[k][0]) < 0.5 and
                                    abs(det[k][1] - PAD_CENTRES[k][1]) < 0.5 for k in det)
    gnd_ok = gnd == sorted(GND_SPOTS)
    report(len(rows) == 20 and det_ok and gnd_ok,
           f"C13 pads.csv: {len(rows)} rows (want 20), {len(det)} of 16 detector rows match name and "
           f"coordinates, GND rows {gnd} (want {sorted(GND_SPOTS)})")

print("ALL CHECKS PASS" if N_FAIL == 0 else f"{N_FAIL} CHECK(S) FAILED")
sys.exit(0 if N_FAIL == 0 else 1)
