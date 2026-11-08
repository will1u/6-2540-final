"""Trap die v3, 10 mm x 10 mm: five-wire 138Ba+ trap with a trap-integrated NbN SNSPD (Claude-authored).

Floorplan (team decision, 2026-11-07: 1 cm x 1 cm die, trap centred, bond pads at the die edges; DESIGN_LOG
step 18). The trap runs along the die centre line. Pads sit in four rows along the top and bottom die
edges at |x| <= 3.5 mm, and on the left/right edges near y = 0, so they stay clear of where the 45-degree
beams through the zones leave the die (top/bottom edges at |x| ~ 4.7 mm, side edges at |y| ~ 4.7 mm).
On a 10 mm die about 1.7e-2 of a 493 nm beam clips the surface (sim/11_beam_clearance.py, step 4).

No ITO (team decision, 2026-11-07; DESIGN_LOG step 17): the readout window is a 30 um opening in the centre
DC Au over bare D2 SiO2; the NbN sits under cap + 10 um D2 only. Layers 24, 30 and 31 are empty.

SNSPD v3.1 (DESIGN_LOG step 24): 130 nm NbN lines on a 200 nm pitch, longer and wider than the window so the
rounded end blocks and the tapered tabs sit outside the light footprint (gds/snspd_geom.py).

Ground (DESIGN_LOG step 22): eight 150 um L40 vias under the Au ground fill tie the fill to the Al M1
plane on chip, as Hampel 2023 grounds its mirror. The M1-1..4 bond openings stay as a backup.

    y
    ^   [top-left pad row ]                                  [top-right pad row ]
    |    capL + seg0..6 leads  <- staircase fingers ->        seg7..14 + capR leads
    |   centre DC + SNSPD ===== U-shaped RF rails ============]= RF lead -> RF pad
    |    (left die edge)         zones: load x=-300, read x=+300
    |   [bottom-left pad row]                                [bottom-right pad row]
    +-----------------------------------------------------------------------> x (trap axis)

Topology (single Au layer, no crossings): every outer DC electrode continues at its full width
as a finger up to its own track (no floating ground islands between fingers), then runs along the
track towards its end of the trap and turns out (~4.4 mm) to a pad on the top or bottom die edge. On each side the
electrode farthest from its pad row takes the outermost track and the pad nearest the trap.
The SNSPD Ti/Au leads (layer 22, under D2) run under the centre DC electrode and its lead to two
pads on the left die edge.

--nodet builds a plain trap die (trap_die_v3_NODET): same electrodes and pads, but no SNSPD, no window
(solid centre DC) and nothing on layers 20, 22, 24, 30, 31 (DESIGN_LOG step 14).

Writes trap_die_v3_A30.gds (or _B60 with --det60, _NODET with --nodet), *_sim.json (gds2itvg layout of
layer 50 for sim/12_final_chip_check.py) and *_pads.csv.
Run from design/sim: ./run.sh ../gds/make_chip.py [--det60 | --nodet]
"""

import csv
import json
import os
import sys

import gdstk

from snspd_geom import meander

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ layers (see layer_map.md)
L_MARK, L_M1, L_NBN, L_LEAD, L_D2OPEN, L_PROT, L_AU = 1, 10, 20, 22, 40, 45, 50   # no ITO / via layers (step 17)
L_NOTE, L_CHIP = 100, 101

# ------------------------------------------------------------------ design parameters (um)
CX, CY = 5000.0, 5000.0                # half size of the 10 x 10 mm die (step 18)
C, A, G = 40.0, 84.0, 5.0              # centre DC width, RF rail width, gap      (log steps 1-2)
DC_DEPTH = 200.0                       # radial extent of the outer DC segments
SEG_W, N_SEG = 95.0, 15                # segment width / count per side          (log step 3)
X_LOAD, X_READ = -300.0, 300.0         # loading and readout zones, 600 um = 12 h apart
SEG_X0 = -747.5                        # left edge of the first segment -> centres -700 ... +700
XRF0, XRF1 = -2000.0, 2000.0           # RF rails: open end (left), closed end (right)
U_BAR = 60.0
WIN_WX, WIN_WY = 30.0, 30.0            # readout window (axial x radial) in the centre DC Au
# v3.1 meander (DESIGN_LOG step 24; sim/15, sim/10 v3.1 scan): lines run OVH_X past each axial window edge
# so the end blocks sit outside the refracted light footprint (window + 2.6 um A30 / 3.9 um B60), and
# OVH_Y past each radial edge to catch the refracted rim.
OVH_X, OVH_Y = 3.0, 1.0                # OVH_Y: sim/10 v3.1 scan, largest overhang with C_RN <= 1.2x (1 um: 1.19x; 2 um: 1.40x)
VARIANT, HAS_DET = "A30", True
if "--det60" in sys.argv:
    WIN_WX, OVH_X, VARIANT = 60.0, 4.5, "B60"
DET_WX, DET_WY = WIN_WX + 2 * OVH_X, WIN_WY + 2 * OVH_Y   # NbN line length and radial extent
if "--nodet" in sys.argv:               # plain trap: no SNSPD, no window, solid centre DC (log step 14)
    VARIANT, HAS_DET = "NODET", False
# --uniform: SIMULATION REFERENCE ONLY, not for fab. Same as --nodet, but every outer DC electrode stops
# at y_dc1 (all the same 200 um depth) and has no lead or pad, so ground fill surrounds it like in an ideal
# five-wire. Compared against NODET in sim/14_staircase_check.py to isolate the staircase fingers + leads.
UNIFORM = "--uniform" in sys.argv
if UNIFORM:
    VARIANT, HAS_DET = "UNIFORM", False
WIRE_W, WIRE_P = 0.130, 0.200         # f = 0.65 (v3: 0.100 / 0.200; step 24)
LEAD_W, PITCH = 6.0, 12.0              # Au track width and pitch
CENTRE_LEAD_W = 40.0
GAP_FAR = 10.0
PAD_GAP = 30.0                         # Au ground fill keep-out around bond pads (step 21: a bond 33 um
                                       # off centre on a 10 um gap would short a pad to the fill)
pad_polys = []                         # bond pads, collected for the PAD_GAP keep-out
PAD_X, PAD_Y = 120.0, 200.0            # long-edge pads (x size, y size)
PAD_P = 180.0                          # pad pitch along the edge
Y_PADROW = CY - 100.0 - 80.0 - PAD_Y / 2   # pad-row centre: 100 um Au pull-back + 80 um (PAD_GAP + a 50 um fill strip
                                           # outboard of the rows that keeps the ground fill in one piece; step 21)
X_ROW_OUT, X_ROW_IN = 3500.0, 2000.0   # pad rows occupy |x| in [X_ROW_IN, X_ROW_OUT], clear of the beam exits
EDGE_AU, EDGE_M1 = 100.0, 150.0

y_rf0, y_rf1 = C / 2 + G, C / 2 + G + A            # 25, 109
y_dc0, y_dc1 = y_rf1 + G, y_rf1 + G + DC_DEPTH     # 114, 314
seg_left = [SEG_X0 + k * (SEG_W + G) for k in range(N_SEG)]
seg_cent = [x + SEG_W / 2 for x in seg_left]
assert X_READ in seg_cent and X_LOAD in seg_cent, "zones must sit on segment centres"

lib = gdstk.Library(unit=1e-6, precision=1e-9)
top = lib.new_cell(f"TRAP_DIE_V3_{VARIANT}")


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


el, seeds, pads = {}, {}, []


def add(name, polys, seed=None):
    el.setdefault(name, []).extend(polys if isinstance(polys, list) else [polys])
    if seed is not None:
        seeds.setdefault(name, []).append([float(seed[0]), float(seed[1])])


# ------------------------------------------------------------------ trap core
win = rect(X_READ - WIN_WX / 2, -WIN_WY / 2, X_READ + WIN_WX / 2, WIN_WY / 2)
centre = rect(XRF0 - 40.0, -C / 2, XRF1 - G, C / 2)
add("2", gdstk.boolean(centre, win, "not") if HAS_DET else centre, seed=(X_LOAD, 0.0))
add("1", [rect(XRF0, y_rf0, XRF1, y_rf1), rect(XRF0, -y_rf1, XRF1, -y_rf0),
          rect(XRF1, -y_rf1, XRF1 + U_BAR, y_rf1)], seed=(X_LOAD, (y_rf0 + y_rf1) / 2))
X_RFPAD = 4700.0
add("1", path([(XRF1 + U_BAR, 0.0), (X_RFPAD, 0.0)], 60.0))
pad_polys.append(rect(X_RFPAD - 100, -100, X_RFPAD + 100, 100))
add("1", pad_polys[-1])
pads.append(("RF", "1", X_RFPAD, 0.0, L_AU))

n_top = [str(3 + k) for k in range(N_SEG)]
n_bot = [str(3 + N_SEG + k) for k in range(N_SEG)]
caps = {+1: ("33", "34"), -1: ("35", "36")}
half = N_SEG // 2                       # segments 0..6 go left, 7..14 go right
for s, names in ((+1, n_top), (-1, n_bot)):
    cl, cr = caps[s]
    # x-extent of every outer electrode on this side, left to right
    spans = [(cl, XRF0, seg_left[0] - G)] + [(names[k], seg_left[k], seg_left[k] + SEG_W) for k in range(N_SEG)] + \
            [(cr, seg_left[-1] + SEG_W + G, XRF1 + U_BAR)]
    left_group = spans[:1 + half]       # capL + seg0..6 -> left pad row
    right_group = spans[1 + half:]      # seg7..14 + capR -> right pad row
    if UNIFORM:                         # sim reference: plain rectangles of equal depth, no leads/pads
        for n, x0, x1 in spans:
            add(n, rect(x0, s * y_dc0, x1, s * y_dc1), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        continue
    # left group: leftmost electrode = innermost track = leftmost pad
    for i, (n, x0, x1) in enumerate(left_group):
        yt = y_dc1 + 20 + LEAD_W / 2 + i * PITCH
        add(n, rect(x0, s * y_dc0, x1, s * (yt + LEAD_W / 2)), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        xp = -X_ROW_OUT + i * PAD_P
        add(n, path([(x0 + LEAD_W / 2, s * yt), (xp, s * yt), (xp, s * Y_PADROW)], LEAD_W))
        pad_polys.append(rect(xp - PAD_X / 2, s * (Y_PADROW - PAD_Y / 2), xp + PAD_X / 2, s * (Y_PADROW + PAD_Y / 2)))
        add(n, pad_polys[-1])
        pads.append((f"{'T' if s > 0 else 'B'}L{i + 1}", n, xp, s * Y_PADROW, L_AU))
    # right group: rightmost electrode = innermost track = rightmost pad
    for i, (n, x0, x1) in enumerate(reversed(right_group)):
        yt = y_dc1 + 20 + LEAD_W / 2 + i * PITCH
        add(n, rect(x0, s * y_dc0, x1, s * (yt + LEAD_W / 2)), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        xp = X_ROW_OUT - i * PAD_P
        add(n, path([(x1 - LEAD_W / 2, s * yt), (xp, s * yt), (xp, s * Y_PADROW)], LEAD_W))
        pad_polys.append(rect(xp - PAD_X / 2, s * (Y_PADROW - PAD_Y / 2), xp + PAD_X / 2, s * (Y_PADROW + PAD_Y / 2)))
        add(n, pad_polys[-1])
        pads.append((f"{'T' if s > 0 else 'B'}R{i + 1}", n, xp, s * Y_PADROW, L_AU))
assert -X_ROW_OUT + half * PAD_P <= -X_ROW_IN and X_ROW_OUT - (N_SEG - half) * PAD_P >= X_ROW_IN, "pad rows overflow"

# centre DC lead to its pad on the left short end (SNSPD leads run underneath it)
X_CPAD = -4650.0
add("2", path([(XRF0 - 40.0, 0.0), (X_CPAD, 0.0)], CENTRE_LEAD_W))
pad_polys.append(rect(X_CPAD - 100, -100, X_CPAD + 100, 100))
add("2", pad_polys[-1])
pads.append(("C", "2", X_CPAD, 0.0, L_AU))

# ------------------------------------------------------------------ SNSPD (layers 20, 22; no ITO)
snspd_pad_polys = []
if HAS_DET:
    nlines = int(round(DET_WY / WIRE_P))
    nlines += nlines % 2
    # rounded end blocks + tapered tabs, both outside the light footprint (gds/snspd_geom.py)
    mpolys, sig_tab, gnd_tab = meander(X_READ, 0.0, DET_WX, DET_WY, WIRE_W, WIRE_P, turn="round", layer=L_NBN)
    for p in mpolys:
        top.add(p)
    LW_SN = 4.0
    X_SNPAD = -4750.0
    Y_SNPAD = 260.0                         # SNSPD pads at (X_SNPAD, +-Y_SNPAD), left short end
    X_BRANCH = X_CPAD + 200.0               # leads leave from under the centre lead before its pad
    for tab, dx, yl, yp in ((sig_tab, 10, 6.0, Y_SNPAD), (gnd_tab, 25, -6.0, -Y_SNPAD)):
        pts = [tab, (tab[0] - dx, tab[1]), (tab[0] - dx, yl), (X_BRANCH, yl), (X_BRANCH - 60, yp), (X_SNPAD, yp)]
        for p in path(pts, LW_SN, L_LEAD):
            top.add(p)
    # step 21: openings grown from 120 x 90 to 150 x 120 um so a wedge foot (<= 75 x 125 um) fits the 10 um well
    snspd_pad_polys = [rect(X_SNPAD - 90, yy - 75, X_SNPAD + 90, yy + 75, L_LEAD) for yy in (Y_SNPAD, -Y_SNPAD)]
    for p in snspd_pad_polys:
        top.add(p)
    pads += [("SNS", "SNSPD_S", X_SNPAD, Y_SNPAD, L_LEAD), ("SNG", "SNSPD_G", X_SNPAD, -Y_SNPAD, L_LEAD)]
    # no buried ITO, via or top ITO (step 17): the window floor is bare D2 SiO2
    # EBL alignment marks on layer 22 (traveler item A2), four around the readout zone, under ground Au
    EBL_MARKS = [(X_READ - 300, 700.0), (X_READ + 300, 700.0), (X_READ - 300, -700.0), (X_READ + 300, -700.0)]
    for xm, ym in EBL_MARKS:
        top.add(rect(xm - 10, ym - 1, xm + 10, ym + 1, L_LEAD), rect(xm - 1, ym - 10, xm + 1, ym + 10, L_LEAD))


# ------------------------------------------------------------------ D2 openings, M1, marks
d2_open = [rect(X_SNPAD - 75, yy - 60, X_SNPAD + 75, yy + 60, L_D2OPEN) for yy in (Y_SNPAD, -Y_SNPAD)] if HAS_DET else []
M1_PADS = [(-4700.0, 2000.0), (-4700.0, -2000.0), (4700.0, 2000.0), (4700.0, -2000.0)]   # side edges
for xc, yc in M1_PADS:
    d2_open.append(rect(xc - 85, yc - 85, xc + 85, yc + 85, L_D2OPEN))
MARK_SITES = ((-4300.0, CY - 170), (4300.0, CY - 170), (-4300.0, -CY + 170), (4300.0, -CY + 170))   # outboard of the pad rows
for xm, ym in MARK_SITES:
    s = 1 if ym > 0 else -1
    top.add(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK), rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    top.add(rect(xm - 30, ym - s * 72, xm + 30, ym - s * 68, L_D2OPEN), rect(xm - 2, ym - s * 84, xm + 2, ym - s * 60, L_D2OPEN))
    if HAS_DET:                          # overlay squares and lead cross for the SNSPD layers
        for k, L in enumerate((L_NBN, L_LEAD)):
            top.add(rect(xm + 60 + 25 * k, ym - 8, xm + 75 + 25 * k, ym + 7, L))
        top.add(rect(xm - 100, ym - 1, xm - 80, ym + 1, L_LEAD), rect(xm - 91, ym - 10, xm - 89, ym + 10, L_LEAD))
mark_keepout = [rect(xm - 160, ym - 140, xm + 180, ym + 140) for xm, ym in MARK_SITES]
for p in d2_open:
    top.add(p)
die = rect(-CX, -CY, CX, CY, L_CHIP)
m1 = gdstk.offset(die, -EDGE_M1, layer=L_M1)
m1_cut = [rect(X_SNPAD - 145, yy - 125, X_SNPAD + 145, yy + 125) for yy in (Y_SNPAD, -Y_SNPAD)] if HAS_DET else []  # no Al under SNSPD pads
m1_cut += [rect(xm - 150, ym - 150, xm + 150, ym + 150) for xm, ym in MARK_SITES]                  # marks visible (A1)
m1 = gdstk.boolean(m1, m1_cut, "not", layer=L_M1)
for p in m1:
    top.add(p)

# ------------------------------------------------------------------ top Au: merge, ground fill
au = {n: gdstk.boolean(ps, [], "or", layer=L_AU) for n, ps in el.items()}
all_el = [p for ps in au.values() for p in ps]
au_area = gdstk.offset(die, -EDGE_AU)
near = rect(XRF0 - 300, -y_dc1 - 300, XRF1 + 400, y_dc1 + 300)
keep = gdstk.boolean(gdstk.offset(all_el, GAP_FAR, join="miter"), near, "not")
keep = gdstk.boolean(keep, gdstk.boolean(gdstk.offset(all_el, G, join="miter"), near, "and"), "or")
keep = gdstk.boolean(keep, gdstk.offset(pad_polys, PAD_GAP, join="miter"), "or")
keep = gdstk.boolean(keep, ([win] if HAS_DET else []) + [gdstk.offset(p, 20)[0] for p in d2_open + snspd_pad_polys] + mark_keepout, "or")
ground = gdstk.boolean(au_area, keep, "not", layer=L_AU)
ground = [max(ground, key=lambda p: p.area())]       # drop any enclosed (floating) ground pieces
for p in all_el + ground:
    p.layer = L_AU
    top.add(p)
GND_PADS = [(-4700.0, 1500.0), (-4700.0, -1500.0), (4700.0, 1500.0), (4700.0, -1500.0)]   # side edges

# On-chip ground link, Au fill -> M1 (DESIGN_LOG step 22). Each via is an L40 opening through D2 + cap +
# spacer that the plated Au ground fill covers, so the Ti/Au seed and the plating land on the Al. This
# is how Hampel 2023 grounds its mirror (CHF3 vias, Au contacting the Al). Without it, M1 is grounded
# only through bond wires at M1-1..4, and a missing bond leaves the mirror floating (Hampel Fig. 3(a)).
# Kept out of d2_open on purpose: the fill must cover these openings, not keep out of them, and they
# need no L45 because the Au masks them during the gap etch.
M1_VIAS = [(-4700.0, 1000.0), (-4700.0, -1000.0), (4700.0, 1000.0), (4700.0, -1000.0),     # next to GND / M1 pads
           (-1000.0, 2500.0), (-1000.0, -2500.0), (1000.0, 2500.0), (1000.0, -2500.0)]     # spread over the die
VIA, VIA_ENC = 150.0, 25.0              # via size; Au and Al must enclose it by >= VIA_ENC
for xv, yv in M1_VIAS:
    v = rect(xv - VIA / 2, yv - VIA / 2, xv + VIA / 2, yv + VIA / 2, L_D2OPEN)
    enc = gdstk.offset(v, VIA_ENC, join="miter")
    assert not gdstk.boolean(enc, ground, "not") and not gdstk.boolean(enc, m1, "not"), f"via at {(xv, yv)} not enclosed"
    top.add(v)

# L45 PROTECT for the Au-masked D2 gap etch (traveler item A3, step 16a): every D2 opening +10 um,
# the readout window +2.5 um, and where the SNSPD leads leave the centre-DC lead. Without ITO the window
# is an opening in the Au mask, so this patch is what stops the gap etch going down toward the NbN.
prot = [gdstk.offset(p, 10)[0] for p in d2_open + snspd_pad_polys]
if HAS_DET:
    prot += [rect(X_READ - WIN_WX / 2 - 2.5, -WIN_WY / 2 - 2.5, X_READ + WIN_WX / 2 + 2.5, WIN_WY / 2 + 2.5)]
    prot += [rect(X_SNPAD, -Y_SNPAD - 20, X_BRANCH + 20, Y_SNPAD + 20)]
for p in gdstk.boolean(prot, [], "or", layer=L_PROT):
    top.add(p)
top.add(die)
labels = [(f"TRAP_DIE_V3 {VARIANT} 138Ba+ h50" + (" NbN SNSPD" if HAS_DET else " no SNSPD"), (-1800, -1000)),
          ("LOAD", (X_LOAD - 50, 450)), ("READ", (X_READ - 50, 450))] + \
         [("GND", (x - 45, y - 15)) for x, y in GND_PADS] + [("M1", (x - 30, y - 15)) for x, y in M1_PADS] + \
         [("VIA", (x - 45, y + 90)) for x, y in M1_VIAS]
for txt, (x, y) in labels:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)

STEM = f"trap_die_v3_{VARIANT}"
lib.write_gds(os.path.join(HERE, STEM + ".gds"))

# ------------------------------------------------------------------ simulation layout + pad list
sim = {
    "_comment": f"gds2itvg layout for {STEM}.gds layer 50 (gds/make_chip.py). Trap axis = GDS x -> ITVG y; "
                "origin at the readout zone. Stack: 6 um Au on 10 um SiO2 over the Al plane. The readout window is an "
                "open hole in electrode 2 over bare SiO2 (max_gap 20 < 30 um, so it fringes over the dielectric).",
    "_zones": {"readout_itvg_y": 0.0, "loading_itvg_y": X_LOAD - X_READ},
    "_die": {"half_x": CX, "half_y": CY, "mark_sites": [list(m) for m in MARK_SITES], "x_rf0": XRF0},
    "_window": {"wx": WIN_WX if HAS_DET else 0.0, "wy": WIN_WY if HAS_DET else 0.0, "floor": "oxide" if HAS_DET else None},
    "layer": L_AU, "datatype": 0, "cell": f"TRAP_DIE_V3_{VARIANT}",
    "roi_box": [XRF0 - 50, -y_dc1 - 30, XRF1 + U_BAR + 30, y_dc1 + 30],
    "frame": {"origin": [X_READ, 0.0], "quarter_turns": 1, "mirror": False},
    "max_gap": 20.0, "gap_model": "profile", "metal_thickness": 6.0, "ground_depth": 10.0,
    "epsilon_r": 3.9, "outer_ground_depth": None,
    "electrodes": {k: seeds[k] for k in sorted(seeds, key=int)},
    "ground": {"99": [[0.0, 900.0]]},
}
with open(os.path.join(HERE, STEM + "_sim.json"), "w") as fh:
    json.dump(sim, fh, indent=1)
role = {"1": "RF", "2": "centre DC", "SNSPD_S": "SNSPD signal (layer 22 pad, D2 opened)",
        "SNSPD_G": "SNSPD return (layer 22 pad, D2 opened)",
        "33": "top cap left", "34": "top cap right", "35": "bottom cap left", "36": "bottom cap right"}
role.update({n: f"top segment, centre {seg_cent[k] - X_READ:+.0f} um from readout" for k, n in enumerate(n_top)})
role.update({n: f"bottom segment, centre {seg_cent[k] - X_READ:+.0f} um from readout" for k, n in enumerate(n_bot)})
with open(os.path.join(HERE, STEM + "_pads.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["pad", "electrode", "role", "x_um", "y_um", "layer"])
    for num, name, x, y, L in pads:
        w.writerow([num, name, role.get(name, name), f"{x:.0f}", f"{y:.0f}", L])
    for k, (x, y) in enumerate(GND_PADS):
        w.writerow([f"GND-{k + 1}", "ground fill", "Au ground fill: bond to carrier ground", f"{x:.0f}", f"{y:.0f}", L_AU])
    for k, (x, y) in enumerate(M1_PADS):
        w.writerow([f"M1-{k + 1}", "ground plane", "Al M1 through D2 opening", f"{x:.0f}", f"{y:.0f}", L_D2OPEN])
print(f"wrote {STEM}.gds: {len(el)} electrodes, {len(pads)} signal pads + {len(GND_PADS)} GND + {len(M1_PADS)} M1"
      f" + {len(M1_VIAS)} fill-to-M1 vias; "
      + (f"meander {nlines} lines ({DET_WX:g} x {DET_WY:g} um)" if HAS_DET else "no SNSPD"))
