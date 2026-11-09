"""Trap die v4, 10 mm x 10 mm: five-wire 138Ba+ trap with a trap-integrated NbN SNSPD (Claude-authored).

v4 = local-mirror architecture (team decision, 2026-11-08; notes/decisions.md; DESIGN_LOG step 25). Follows
Hampel 2023: no die-wide Al plane and no 10 um D2. The Au electrodes sit on the thin stack
(Si / 1 um thermal SiO2 / 238 nm spacer / 80 nm cap). The Al (layer 10) is a local mirror strip under the
centre DC only (|y| <= 20 um, never under the RF rails), from just past the SNSPD to beyond the RF open end,
grounded through one via under the Au ground fill. The v3 baseline is in archive_v3_baseline/.

Lead routing (team decision, 2026-11-08): the SNSPD leads are made in the electrode Au (layer 50), in the same
step as the electrodes, as Hampel 2023 does. Inside the trap they run in a slot along the centre DC:

    y (um)   20 ..12.5   centre DC, top half      (electrode 2)
           12.5 .. 7.5   gap
            7.5 .. 2.5   SNSPD signal lead        (ground 97 in the simulation: held at ~0 V)
            2.5 ..-2.5   gap
           -2.5 ..-7.5   SNSPD return lead        (ground 98)
           -7.5 ..-12.5  gap
          -12.5 ..-20    centre DC, bottom half   (electrode 2)

The slot runs from the left end of the centre DC to x = X_SLOT_END, 50 um before the readout window. Right of
it the centre DC is solid, so the two halves are one electrode (a U around the slot). The NbN tabs sit under
that solid part. A short Ti/Au strip (layer 22, made before the NbN, as in v3) runs from each tab into the
slot, where a layer-40 opening in the cap lets the Au lead land on it.

Floorplan as v3 (DESIGN_LOG step 18): trap on the die centre line, pads on the top/bottom edges at
|x| <= 3.5 mm and near y = 0 on the side edges. The left edge carries the SNSPD pads (now Au) and the centre DC
pad; the centre DC leaves the slot along its top half.

    y
    ^   [top-left pad row ]                                  [top-right pad row ]
    |    capL + seg0..6 leads  <- staircase fingers ->        seg7..14 + capR leads
    |   C pad / SNSPD pads = slot ======= U-shaped RF rails ======]= RF lead -> RF pad
    |    (left die edge)         zones: load x=-240, read x=+240
    |   [bottom-left pad row]                                [bottom-right pad row]
    +-----------------------------------------------------------------------> x (trap axis)

Variants:
  (default)  trap_die_v4_A30: 30 x 30 um readout window, v3.1 meander (DESIGN_LOG step 24)
  --det60    trap_die_v4_B60: 60 x 30 um window (axial x radial), 69 um lines; the slot, contacts and
             mirror move with the longer meander (B60 kept, team decision 2026-11-08)
  --nodet    trap_die_v4_NODET: no SNSPD, no window, no slot (solid centre DC), no Al, no layer 40.
             This is the R1_TRAP die: Au on SiO2 over high-resistivity Si.
  --uniform  SIMULATION REFERENCE ONLY (sim/14): NODET with equal-depth outer DC rectangles, no leads/pads.

Writes trap_die_v4_<V>.gds, <stem>_pads.csv and the gds2itvg layouts:
  <stem>_sim.json      option E2 electrodes (6 um plated Au)
  <stem>_E1_sim.json   option E1 electrodes (0.35 um lift-off Au); A30 and B60
  <stem>_simfloor.gds  A30 and B60, simulation only: layer 50 plus a grounded "floor" conductor 1 um inside the
                       readout window. The window floor is the cap 0.32 um above the grounded mirror, so it
                       sits at ~0 V; without this conductor gds2itvg would treat the 30 um hole as floating
                       dielectric. Never send this file to fab.
Run from design/sim: ./run.sh ../gds/make_chip.py [--det60 | --nodet | --uniform]
"""

import csv
import json
import os
import sys

import gdstk

from snspd_geom import meander

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ layers (see layer_map.md)
L_MARK, L_M1, L_NBN, L_LEAD, L_VIA, L_AU = 1, 10, 20, 22, 40, 50   # 10 = local mirror; 40 = cap/spacer openings
L_NOTE, L_CHIP = 100, 101

# ------------------------------------------------------------------ design parameters (um)
CX, CY = 5000.0, 5000.0                # half size of the 10 x 10 mm die (step 18)
C, A, G = 40.0, 84.0, 5.0              # centre DC width, RF rail width, gap      (log steps 1-2)
DC_DEPTH = 200.0                       # radial extent of the outer DC segments
SEG_W, N_SEG = 115.0, 15               # segment width / count per side: 120 um pitch (step 28; step 3 found
                                       # 75-150 um pitches equivalent; 120 puts both 480 um zones on segment centres)
X_LOAD, X_READ = -240.0, 240.0         # loading and readout zones, 480 um apart (team decision 2026-11-08: the
                                       # team's laser setup)
SEG_X0 = -897.5                        # left edge of the first segment -> centres -840 ... +840
XRF0, XRF1 = -2000.0, 2000.0           # RF rails: open end (left), closed end (right)
U_BAR = 60.0
WIN_WX, WIN_WY = 30.0, 30.0            # readout window (axial x radial) in the centre DC Au
# v3.1 meander (DESIGN_LOG step 24): lines run OVH_X past each axial window edge and OVH_Y past each radial edge
OVH_X, OVH_Y = 3.0, 1.0
VARIANT, HAS_DET = "A30", True
if "--det60" in sys.argv:
    WIN_WX, OVH_X, VARIANT = 60.0, 4.5, "B60"
DET_WX, DET_WY = WIN_WX + 2 * OVH_X, WIN_WY + 2 * OVH_Y   # NbN line length and radial extent
if "--nodet" in sys.argv:               # plain trap: no SNSPD, no window, solid centre DC (log step 14)
    VARIANT, HAS_DET = "NODET", False
# --uniform: SIMULATION REFERENCE ONLY, not for fab. Same as --nodet, but every outer DC electrode stops
# at y_dc1 (all the same 200 um depth) and has no lead or pad (sim/14_staircase_check.py).
UNIFORM = "--uniform" in sys.argv
if UNIFORM:
    VARIANT, HAS_DET = "UNIFORM", False
WIRE_W, WIRE_P = 0.130, 0.200         # f = 0.65 (step 24)
LEAD_W, PITCH = 6.0, 12.0              # Au track width and pitch (outer DC leads)
GAP_FAR = 10.0
PAD_GAP = 30.0                         # Au ground fill keep-out around bond pads (step 21)
pad_polys = []                         # bond pads, collected for the PAD_GAP keep-out
PAD_X, PAD_Y = 120.0, 200.0            # long-edge pads (x size, y size)
PAD_P = 360.0                          # pad pitch along the edge (step 29: was 180; measured PGA84L finger-centre
                                       # fan-out has a ~20 deg worst wire; team adoption pending beam-access review)
Y_PADROW = CY - 100.0 - 80.0 - PAD_Y / 2
X_ROW_OUT, X_ROW_IN = 3500.0, 600.0    # pad rows occupy |x| in [X_ROW_IN, X_ROW_OUT]; X_ROW_OUT keeps the beam exits clear
EDGE_AU = 100.0

# slot and SNSPD leads (local-mirror routing, step 25)
SLOT_HALF = 12.5                       # slot |y| < 12.5: gap 5 / lead 5 / gap 5 / lead 5 / gap 5
SN_W, SN_Y = 5.0, 5.0                  # Au lead width and centre |y|
# the NbN tab centres sit 27 um left of the meander (snspd_geom: 0.5 block + 0.5 gap + 6 taper + 20 = half a
# 40 um tab); the slot ends 20 um left of them (A30: x = 235, 50 um before the window; B60: x = 218.5)
X_TAB = X_READ - DET_WX / 2 - 27.0
X_SLOT_END = X_TAB - 20.0
X_LEAD_END = X_SLOT_END - G            # lead tips, 5 um from the solid centre DC
DC_HALF_Y = (SLOT_HALF + C / 2) / 2    # 16.25: centre line of each centre-DC half (7.5 um wide)
X_CPAD, Y_CPAD = -4650.0, 450.0        # centre DC pad (left edge)
X_SNPAD, Y_SNPAD = -4750.0, 100.0      # SNSPD pads at (X_SNPAD, +-Y_SNPAD), left edge, now Au
# local mirror (LOCAL_MIRROR.md H.1): |y| <= 20 under the centre DC, x from MIR_X0 to MIR_X1
MIR_HALF, MIR_X1, MIR_X0 = 20.0, X_READ + DET_WX / 2 + 10.0, -2240.0   # 10 um past the NbN
MVIA_C, MVIA, MVIA_ENC = (-2140.0, 130.0), 100.0, 25.0   # mirror ground via (cap + spacer -> Al), under the fill,
                                       # just past the RF open end (x = -2000) to keep the mirror path short (step 28)

y_rf0, y_rf1 = C / 2 + G, C / 2 + G + A            # 25, 109
y_dc0, y_dc1 = y_rf1 + G, y_rf1 + G + DC_DEPTH     # 114, 314
seg_left = [SEG_X0 + k * (SEG_W + G) for k in range(N_SEG)]
seg_cent = [x + SEG_W / 2 for x in seg_left]
assert X_READ in seg_cent and X_LOAD in seg_cent, "zones must sit on segment centres"

lib = gdstk.Library(unit=1e-6, precision=1e-9)
CELL = f"TRAP_DIE_V4_{VARIANT}"
top = lib.new_cell(CELL)


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
if HAS_DET:
    slot = rect(XRF0 - 41.0, -SLOT_HALF, X_SLOT_END, SLOT_HALF)
    centre = gdstk.boolean(centre, [win, slot], "not")
add("2", centre, seed=(X_LOAD, DC_HALF_Y))
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
    spans = [(cl, XRF0, seg_left[0] - G)] + [(names[k], seg_left[k], seg_left[k] + SEG_W) for k in range(N_SEG)] + \
            [(cr, seg_left[-1] + SEG_W + G, XRF1 + U_BAR)]
    left_group = spans[:1 + half]       # capL + seg0..6 -> left pad row
    right_group = spans[1 + half:]      # seg7..14 + capR -> right pad row
    if UNIFORM:                         # sim reference: plain rectangles of equal depth, no leads/pads
        for n, x0, x1 in spans:
            add(n, rect(x0, s * y_dc0, x1, s * y_dc1), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        continue
    for i, (n, x0, x1) in enumerate(left_group):      # leftmost electrode = innermost track = leftmost pad
        yt = y_dc1 + 20 + LEAD_W / 2 + i * PITCH
        add(n, rect(x0, s * y_dc0, x1, s * (yt + LEAD_W / 2)), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        xp = -X_ROW_OUT + i * PAD_P
        add(n, path([(x0 + LEAD_W / 2, s * yt), (xp, s * yt), (xp, s * Y_PADROW)], LEAD_W))
        pad_polys.append(rect(xp - PAD_X / 2, s * (Y_PADROW - PAD_Y / 2), xp + PAD_X / 2, s * (Y_PADROW + PAD_Y / 2)))
        add(n, pad_polys[-1])
        pads.append((f"{'T' if s > 0 else 'B'}L{i + 1}", n, xp, s * Y_PADROW, L_AU))
    for i, (n, x0, x1) in enumerate(reversed(right_group)):   # rightmost electrode = innermost track
        yt = y_dc1 + 20 + LEAD_W / 2 + i * PITCH
        add(n, rect(x0, s * y_dc0, x1, s * (yt + LEAD_W / 2)), seed=((x0 + x1) / 2, s * (y_dc0 + y_dc1) / 2))
        xp = X_ROW_OUT - i * PAD_P
        add(n, path([(x1 - LEAD_W / 2, s * yt), (xp, s * yt), (xp, s * Y_PADROW)], LEAD_W))
        pad_polys.append(rect(xp - PAD_X / 2, s * (Y_PADROW - PAD_Y / 2), xp + PAD_X / 2, s * (Y_PADROW + PAD_Y / 2)))
        add(n, pad_polys[-1])
        pads.append((f"{'T' if s > 0 else 'B'}R{i + 1}", n, xp, s * Y_PADROW, L_AU))
assert -X_ROW_OUT + half * PAD_P <= -X_ROW_IN and X_ROW_OUT - (N_SEG - half) * PAD_P >= X_ROW_IN, "pad rows overflow"

# centre DC lead: leaves along the top half of the centre DC and turns up to its pad only beyond x = -3600,
# outboard of the left pad-row tracks (they run at |y| >= 334 um out to x = -3500)
add("2", path([(XRF0 - 40.0, DC_HALF_Y), (-3600.0, DC_HALF_Y), (-3700.0, Y_CPAD), (X_CPAD, Y_CPAD)], C / 2 - SLOT_HALF))
pad_polys.append(rect(X_CPAD - 100, Y_CPAD - 100, X_CPAD + 100, Y_CPAD + 100))
add("2", pad_polys[-1])
pads.append(("C", "2", X_CPAD, Y_CPAD, L_AU))

# ------------------------------------------------------------------ SNSPD: NbN, Au leads in the slot, contacts
vias, mirror = [], []
if HAS_DET:
    nlines = int(round(DET_WY / WIRE_P))
    nlines += nlines % 2
    mpolys, sig_tab, gnd_tab = meander(X_READ, 0.0, DET_WX, DET_WY, WIRE_W, WIRE_P, turn="round", layer=L_NBN)
    for p in mpolys:
        top.add(p)
    assert abs(sig_tab[0] - X_TAB) < 1e-6, "X_TAB must match snspd_geom's tab position"
    X_BEND = -4400.0                    # leads turn out to their pads here
    for name, tab, sy in (("SNSPD_S", sig_tab, +1), ("SNSPD_G", gnd_tab, -1)):
        # Au lead (layer 50) from the slot tip to its pad: a separate conductor
        add(name, path([(X_LEAD_END, sy * SN_Y), (X_BEND, sy * SN_Y), (X_BEND - 60, sy * Y_SNPAD), (X_SNPAD, sy * Y_SNPAD)],
                       SN_W), seed=(X_LOAD, sy * SN_Y))
        pad_polys.append(rect(X_SNPAD - 100, sy * Y_SNPAD - 75, X_SNPAD + 100, sy * Y_SNPAD + 75))
        add(name, pad_polys[-1])
        # Ti/Au contact (layer 22): covers the -x half of the NbN tab, steps into the slot, ends in a pad
        for p in path([tab, (tab[0] - 15, tab[1]), (tab[0] - 27, sy * SN_Y), (X_LEAD_END - 27, sy * SN_Y)], 4.0, L_LEAD):
            top.add(p)
        top.add(rect(X_LEAD_END - 27, sy * (SN_Y - 3.5), X_LEAD_END, sy * (SN_Y + 3.5), L_LEAD))
        # cap opening (layer 40) where the Au lead lands on the Ti/Au pad: 3 x 18 um, 1 um inside the lead
        vias.append(rect(X_LEAD_END - 22, sy * (SN_Y - 1.5), X_LEAD_END - 4, sy * (SN_Y + 1.5), L_VIA))
    pads += [("SNS", "SNSPD_S", X_SNPAD, Y_SNPAD, L_AU), ("SNG", "SNSPD_G", X_SNPAD, -Y_SNPAD, L_AU)]
    # EBL alignment marks on layer 22 (traveler item A2), four around the readout zone, under ground Au
    for xm, ym in [(X_READ - 300, 700.0), (X_READ + 300, 700.0), (X_READ - 300, -700.0), (X_READ + 300, -700.0)]:
        top.add(rect(xm - 10, ym - 1, xm + 10, ym + 1, L_LEAD), rect(xm - 1, ym - 10, xm + 1, ym + 10, L_LEAD))
    # local mirror (layer 10): strip under the centre DC + a branch under the ground fill for the via
    mirror = gdstk.boolean(rect(MIR_X0, -MIR_HALF, MIR_X1, MIR_HALF, L_M1),
                           rect(MVIA_C[0] - 100, -MIR_HALF, MVIA_C[0] + 100, MVIA_C[1] + 100, L_M1), "or", layer=L_M1)
    for p in mirror:
        top.add(p)

# ------------------------------------------------------------------ marks
MARK_SITES = ((-4300.0, CY - 170), (4300.0, CY - 170), (-4300.0, -CY + 170), (4300.0, -CY + 170))   # outboard of the pad rows
for xm, ym in MARK_SITES:
    s = 1 if ym > 0 else -1
    top.add(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK), rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    if HAS_DET:                          # L40 cross; overlay squares and lead cross for the SNSPD layers
        top.add(rect(xm - 30, ym - s * 72, xm + 30, ym - s * 68, L_VIA), rect(xm - 2, ym - s * 84, xm + 2, ym - s * 60, L_VIA))
        for k, L in enumerate((L_NBN, L_LEAD)):
            top.add(rect(xm + 60 + 25 * k, ym - 8, xm + 75 + 25 * k, ym + 7, L))
        top.add(rect(xm - 100, ym - 1, xm - 80, ym + 1, L_LEAD), rect(xm - 91, ym - 10, xm - 89, ym + 10, L_LEAD))
mark_keepout = [rect(xm - 160, ym - 140, xm + 180, ym + 140) for xm, ym in MARK_SITES]
die = rect(-CX, -CY, CX, CY, L_CHIP)

# ------------------------------------------------------------------ top Au: merge, ground fill
au = {n: gdstk.boolean(ps, [], "or", layer=L_AU) for n, ps in el.items()}
all_el = [p for ps in au.values() for p in ps]
au_area = gdstk.offset(die, -EDGE_AU)
near = rect(XRF0 - 300, -y_dc1 - 300, XRF1 + 400, y_dc1 + 300)
keep = gdstk.boolean(gdstk.offset(all_el, GAP_FAR, join="miter"), near, "not")
keep = gdstk.boolean(keep, gdstk.boolean(gdstk.offset(all_el, G, join="miter"), near, "and"), "or")
keep = gdstk.boolean(keep, gdstk.offset(pad_polys, PAD_GAP, join="miter"), "or")
keep = gdstk.boolean(keep, ([win] if HAS_DET else []) + mark_keepout, "or")
ground = gdstk.boolean(au_area, keep, "not", layer=L_AU)
ground = [max(ground, key=lambda p: p.area())]       # drop any enclosed (floating) ground pieces
for p in all_el + ground:
    p.layer = L_AU
    top.add(p)
GND_PADS = [(-4700.0, 1500.0), (-4700.0, -1500.0), (4700.0, 1500.0), (4700.0, -1500.0)]   # side edges

# Mirror ground via (step 22 idea, LOCAL_MIRROR H.1/H.2 step 11v): an L40 opening through cap + spacer
# (~0.32 um) onto the Al, under the Au ground fill, which lands on the Al there. The fill and the mirror
# must enclose it by >= MVIA_ENC.
if HAS_DET:
    mv = rect(MVIA_C[0] - MVIA / 2, MVIA_C[1] - MVIA / 2, MVIA_C[0] + MVIA / 2, MVIA_C[1] + MVIA / 2, L_VIA)
    enc = gdstk.offset(mv, MVIA_ENC, join="miter")
    assert not gdstk.boolean(enc, ground, "not") and not gdstk.boolean(enc, mirror, "not"), "mirror via not enclosed"
    vias.append(mv)
for p in vias:
    top.add(p)
top.add(die)
labels = [(f"TRAP_DIE_V4 {VARIANT} 138Ba+ h50" + (" NbN SNSPD local mirror" if HAS_DET else " no SNSPD"), (-1800, -1000)),
          ("LOAD", (X_LOAD - 50, 450)), ("READ", (X_READ - 50, 450))] + \
         [("GND", (x - 45, y - 15)) for x, y in GND_PADS] + ([("MIRROR VIA", (MVIA_C[0] - 120, MVIA_C[1] + 70))] if HAS_DET else [])
for txt, (x, y) in labels:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)

STEM = f"trap_die_v4_{VARIANT}"
lib.write_gds(os.path.join(HERE, STEM + ".gds"))

# simulation-only copy of layer 50 with the grounded window floor (A30): see the docstring
sim_gds = STEM + ".gds"
FLOOR_SEED = [X_READ, 0.0]
if HAS_DET:
    slib = gdstk.Library(unit=1e-6, precision=1e-9)
    scell = slib.new_cell(CELL)
    for p in top.polygons:
        if p.layer == L_AU:
            scell.add(p.copy())
    scell.add(gdstk.offset(win, -1.0, join="miter", layer=L_AU)[0])
    sim_gds = STEM + "_simfloor.gds"
    slib.write_gds(os.path.join(HERE, sim_gds))

# ------------------------------------------------------------------ simulation layouts + pad list
ground_seeds = {"99": [[0.0, 900.0]]}
if HAS_DET:
    ground_seeds.update({"97": seeds.pop("SNSPD_S"), "98": seeds.pop("SNSPD_G"), "96": [FLOOR_SEED]})
STACKS = {"E2": 6.0, "E1": 0.35} if HAS_DET else {"E2": 6.0}
for opt, t_au in STACKS.items():
    sim = {
        "_comment": f"gds2itvg layout for {STEM} layer 50 (gds/make_chip.py v4, local mirror). Trap axis = GDS x -> "
                    f"ITVG y; origin at the readout zone. Stack option {opt}: {t_au:g} um Au on ~1.3 um SiO2 over HR Si, "
                    "no buried ground plane (ground_depth null; the local Al under the centre DC is not modelled). "
                    + ("Grounds 97/98 are the SNSPD leads in the slot (~0 V); 96 is the window floor (cap over the "
                       "grounded mirror), present only in _simfloor.gds." if HAS_DET else ""),
        "_gds": sim_gds,
        "_zones": {"readout_itvg_y": 0.0, "loading_itvg_y": X_LOAD - X_READ},
        "_die": {"half_x": CX, "half_y": CY, "mark_sites": [list(m) for m in MARK_SITES], "x_rf0": XRF0},
        "_window": {"wx": WIN_WX if HAS_DET else 0.0, "wy": WIN_WY if HAS_DET else 0.0,
                    "floor": (f"mirror_t{6 if t_au > 1 else 1}" if HAS_DET else None)},
        "_stack": {"arch": "local_mirror", "option": opt, "t_au": t_au, "t_sio2_above_nbn": 0.08,
                   "slot_half": SLOT_HALF if HAS_DET else 0.0, "mirror_half": MIR_HALF if HAS_DET else 0.0},
        "_sim_only_ground": ["96"] if HAS_DET else [],
        "_snspd_leads": ["97", "98"] if HAS_DET else [],
        "layer": L_AU, "datatype": 0, "cell": CELL,
        "roi_box": [XRF0 - 50, -y_dc1 - 30, XRF1 + U_BAR + 30, y_dc1 + 30],
        "frame": {"origin": [X_READ, 0.0], "quarter_turns": 1, "mirror": False},
        "max_gap": 20.0, "gap_model": "profile", "metal_thickness": t_au, "ground_depth": None,
        "epsilon_r": 3.9, "outer_ground_depth": None,
        "electrodes": {k: seeds[k] for k in sorted(seeds, key=int)},
        "ground": ground_seeds,
    }
    name = STEM + ("_sim.json" if opt == "E2" else f"_{opt}_sim.json")
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(sim, fh, indent=1)
role = {"1": "RF", "2": "centre DC", "SNSPD_S": "SNSPD signal (Au lead in the centre-DC slot)",
        "SNSPD_G": "SNSPD return (Au lead in the centre-DC slot)",
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
print(f"wrote {STEM}.gds: {len(el)} conductors, {len(pads)} signal pads + {len(GND_PADS)} GND; "
      + (f"meander {nlines} lines ({DET_WX:g} x {DET_WY:g} um), slot leads, local mirror "
         f"{MIR_X1 - MIR_X0:.0f} x {2 * MIR_HALF:.0f} um + via" if HAS_DET else "no SNSPD, no Al"))
