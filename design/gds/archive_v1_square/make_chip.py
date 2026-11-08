"""Full 10 mm x 10 mm chip: five-wire 138Ba+ trap with a trap-integrated NbN SNSPD (Claude-authored).

Plain square diced chip (team decision, 2026-11-02: no bowtie). To keep the 45-degree laser beams off
the surface, the trap runs parallel to the top edge, 800 um from it, and both zones sit near the
top-right corner: the beams only cross that corner (DESIGN_LOG step 8, sim/11_beam_clearance.py).

Writes (for variant A30, or B60 with --det60):
  trap_chip_v1[_B60].gds        all fab layers (layer_map.md)
  trap_chip_v1[_B60]_sim.json   gds2itvg layout of layer 50 for sim/12_final_chip_check.py
  trap_chip_v1[_B60]_pads.csv   pad list (bond-pad number, electrode, role, x, y, layer)
Coordinates in um, chip centre at (0, 0), trap axis along +x at y = Y_AX.

Topology (single Au layer, no crossings):
  - RF is a "U" closed on the RIGHT (near the corner); the RF lead runs down the right edge to a
    pad well below where the beams leave the chip.
  - The centre DC leaves through the open (left) end of the U and runs left along the axis.
  - Every outer DC electrode rises/falls to its own track and runs left. At the left edge all leads
    turn as nested L's onto one pad column (higher track -> turns closer to the column -> higher
    pad), so no two leads cross.
  - The SNSPD Ti/Au leads (layer 22, buried under D2) run under the centre DC electrode and its
    40 um wide lead all the way to two pads next to the centre-DC pad.
  - The lower half of the chip carries probe-station test structures (test_structures()).
Run from design/sim:  ./run.sh ../gds/make_chip.py [--det60]
"""

import csv
import json
import os
import sys

import gdstk
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ layers (see layer_map.md)
L_MARK, L_M1, L_NBN, L_LEAD, L_ITO, L_D2OPEN, L_AU = 1, 10, 20, 22, 30, 40, 50
L_VIA, L_ITOB = 24, 31                 # cap+spacer via to M1; buried (grounded) ITO  (log step 9b)
L_PROT = 45                            # derived: resist protect during the Au-masked D2 gap etch (step 12)
L_NOTE, L_CHIP = 100, 101

# ------------------------------------------------------------------ design parameters (um)
CHIP = 5000.0                          # half size of the 10 x 10 mm die
C, A, G = 40.0, 84.0, 5.0              # centre DC width, RF rail width, gap     (log steps 1-2)
DC_DEPTH = 150.0                       # radial extent of the outer DC segments  (log step 8)
SEG_W, N_SEG = 95.0, 15                # segment width / count per side         (log step 3)
Y_AX = 4200.0                          # trap axis, 800 um below the top edge     (log step 8)
X_READ = 4200.0                        # readout zone, 800 um from the right edge
X_LOAD = 3600.0                        # loading zone, 600 um (12 h) from readout
SEG_X0 = 3052.5                        # left edge of the first segment -> centres 3100 ... 4500
XRF0, XRF1 = 2000.0, 4700.0            # RF rails: open end (left), closed end (right)
U_BAR = 60.0                           # width of the RF U bar on the right
WIN_WX, WIN_WY = 30.0, 30.0            # readout window (axial x radial) in the centre DC Au
DET_WX, DET_WY = 30.0, 30.0            # NbN meander active area (axial x radial)  (log step 7)
VARIANT = "A30"
if "--det60" in sys.argv:              # chip B: window and detector 60 um along the axis
    WIN_WX, DET_WX, VARIANT = 60.0, 60.0, "B60"
WIRE_W, WIRE_P = 0.100, 0.200          # nanowire width, pitch
LEAD_W, LEAD_S = 6.0, 6.0              # Au lead width / spacing on the tracks
TURN_P = 24.0                          # x step between nested L turns at the pad column
CENTRE_LEAD_W = 40.0                   # centre DC lead width (SNSPD leads hide underneath)
GAP_FAR = 10.0                         # Au-Au gap away from the trap
PAD_W, PAD_H, PAD_P = 200.0, 120.0, 180.0
X_COL = -4750.0                        # pad column centre (left edge)
Y_PAD0 = 4650.0                        # first (top) pad
EDGE_AU, EDGE_M1 = 100.0, 150.0        # metal pull-back from the dicing edge

y_rf0, y_rf1 = C / 2 + G, C / 2 + G + A            # 25, 109 (relative to the axis)
y_dc0, y_dc1 = y_rf1 + G, y_rf1 + G + DC_DEPTH     # 114, 264
seg_left = [SEG_X0 + k * (SEG_W + G) for k in range(N_SEG)]
seg_cent = [x + SEG_W / 2 for x in seg_left]
assert X_READ in seg_cent and X_LOAD in seg_cent, "zones must sit on segment centres"

lib = gdstk.Library(unit=1e-6, precision=1e-9)
top = lib.new_cell(f"TRAP_CHIP_V1_{VARIANT}")


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


el, seeds = {}, {}


def add(name, polys, seed=None):
    el.setdefault(name, []).extend(polys if isinstance(polys, list) else [polys])
    if seed is not None:
        seeds.setdefault(name, []).append([float(seed[0]), float(seed[1])])


# ------------------------------------------------------------------ trap core
# centre DC (2), with the readout window
centre = rect(XRF0 - 40.0, Y_AX - C / 2, XRF1 - G, Y_AX + C / 2)
win = rect(X_READ - WIN_WX / 2, Y_AX - WIN_WY / 2, X_READ + WIN_WX / 2, Y_AX + WIN_WY / 2)
add("2", gdstk.boolean(centre, win, "not"), seed=(X_LOAD, Y_AX))
# RF (1): rails + U bar on the right + lead down the right edge to its pad (one seed: one conductor)
add("1", [rect(XRF0, Y_AX + y_rf0, XRF1, Y_AX + y_rf1), rect(XRF0, Y_AX - y_rf1, XRF1, Y_AX - y_rf0),
          rect(XRF1, Y_AX - y_rf1, XRF1 + U_BAR, Y_AX + y_rf1)], seed=(X_LOAD, Y_AX + (y_rf0 + y_rf1) / 2))
X_RFPAD, Y_RFPAD = 4750.0, 2400.0
add("1", path([(XRF1 + U_BAR, Y_AX), (4810.0, Y_AX), (4810.0, Y_RFPAD)], 60.0))
add("1", rect(X_RFPAD - PAD_W / 2, Y_RFPAD - PAD_W / 2, X_RFPAD + PAD_W / 2, Y_RFPAD + PAD_W / 2))
# outer DC: segments top 3..17 (left -> right), bottom 18..32; caps 33/34 top (L/R), 35/36 bottom
n_top = [str(3 + k) for k in range(N_SEG)]
n_bot = [str(3 + N_SEG + k) for k in range(N_SEG)]
caps = {+1: ("33", "34"), -1: ("35", "36")}
for s, names in ((+1, n_top), (-1, n_bot)):
    ya, yb = Y_AX + s * y_dc0, Y_AX + s * y_dc1
    for k, xl in enumerate(seg_left):
        add(names[k], rect(xl, ya, xl + SEG_W, yb), seed=(xl + SEG_W / 2, (ya + yb) / 2))
    cl, cr = caps[s]
    add(cl, rect(XRF0, ya, seg_left[0] - G, yb), seed=(XRF0 + 300, (ya + yb) / 2))
    add(cr, rect(seg_left[-1] + SEG_W + G, ya, XRF1 + U_BAR, yb), seed=(seg_left[-1] + SEG_W + 40, (ya + yb) / 2))

# ------------------------------------------------------------------ leads: tracks + nested-L fan-out
pitch = LEAD_W + LEAD_S
LW_SN = 4.0                            # SNSPD Ti/Au lead width (layer 22)
items = []          # (name, kind, x_start, y_track, width) ordered from the TOP of the chip down
for s in (+1, -1):
    cl, cr = caps[s]
    names = n_top if s > 0 else n_bot
    y_edge = Y_AX + s * y_dc1
    # each segment (and the right cap) continues at full width as a finger up to its own track, so
    # no floating ground islands are left between neighbouring risers (only 5-6 um gaps)
    tr = [(cr, seg_left[-1] + SEG_W + 60, (seg_left[-1] + SEG_W + G, XRF1 + U_BAR))] +          [(names[k], seg_cent[k], (seg_left[k], seg_left[k] + SEG_W)) for k in reversed(range(N_SEG))]
    # outermost track = rightmost electrode (its horizontal passes over every other riser)
    side = []
    for i, (n, x0, (fx0, fx1)) in enumerate(tr):
        yt = y_edge + s * (20 + LEAD_W / 2 + (len(tr) - 1 - i) * pitch)
        add(n, rect(fx0, y_edge, fx1, yt + s * LEAD_W / 2))           # the finger
        side.append((n, "riser", fx0 + LEAD_W / 2, yt, LEAD_W))
    side.append((cl, "flat", XRF0, Y_AX + s * (y_dc0 + y_dc1) / 2, LEAD_W))
    if s > 0:
        items += side                                     # top: outermost first
        items.append(("2", "flat", XRF0 - 40.0, Y_AX, CENTRE_LEAD_W))
        items.append(("SNSPD_S", "snspd", None, None, None))
        items.append(("SNSPD_G", "snspd", None, None, None))
    else:
        items += list(reversed(side))                     # bottom: innermost first
x_inner = X_COL + PAD_W / 2 + 60
pads = []
x_turn, w_prev = x_inner - TURN_P, LEAD_W
for n_i, (name, kind, x0, yt, w) in enumerate(items):
    y_pad = Y_PAD0 - n_i * PAD_P
    w_here = w if w else 2 * 8.0 + LW_SN       # the two SNSPD leads (layer 22) ride under the centre lead
    x_turn += max(TURN_P, (w_prev + w_here) / 2 + 12.0)
    w_prev = w_here
    if kind == "snspd":
        pads.append((n_i + 1, name, X_COL, y_pad, L_LEAD))
        continue
    if kind == "riser":
        y_from = Y_AX + np.sign(yt - Y_AX) * y_dc1
        pts = [(x0, y_from), (x0, yt), (x_turn, yt), (x_turn, y_pad), (X_COL, y_pad)]
    else:
        pts = [(x0, yt), (x_turn, yt), (x_turn, y_pad), (X_COL, y_pad)]
    add(name, path(pts, w))
    add(name, rect(X_COL - PAD_W / 2, y_pad - PAD_H / 2, X_COL + PAD_W / 2, y_pad + PAD_H / 2))
    pads.append((n_i + 1, name, X_COL, y_pad, L_AU))
    if name == "2":
        x_turn_c, y_pad_c = x_turn, y_pad
pads.append(("RF", "1", X_RFPAD, Y_RFPAD, L_AU))

# ------------------------------------------------------------------ SNSPD (layers 20, 22, 30)
# Meander lines along the trap axis (as Todaro 2021). Even number of lines and turn-arounds of
# even lines on the +x side put both open ends on the -x side, towards the centre-DC lead.
nlines = int(round(DET_WY / WIRE_P))
nlines += nlines % 2


def meander(xc, yc):
    polys = []
    x0m, x1m, y0m = xc - DET_WX / 2, xc + DET_WX / 2, yc - DET_WY / 2
    for k in range(nlines):
        y = y0m + k * WIRE_P
        polys.append(rect(x0m, y, x1m, y + WIRE_W, L_NBN))
        if k < nlines - 1:
            xe = x1m if k % 2 == 0 else x0m - WIRE_W
            polys.append(rect(xe, y, xe + WIRE_W, y + WIRE_P + WIRE_W, L_NBN))
    y_last = y0m + (nlines - 1) * WIRE_P
    polys.append(rect(x0m - TAB_L, y0m - TAB_H, x0m, y0m + WIRE_W, L_NBN))            # ground end
    polys.append(rect(x0m - TAB_L, y_last, x0m, y_last + WIRE_W + TAB_H, L_NBN))    # signal end
    return polys, (x0m - 20, y_last + TAB_H / 2), (x0m - 20, y0m - TAB_H / 2)


TAB_L, TAB_H = 40.0, 3.0
mpolys, sig_tab, gnd_tab = meander(X_READ, Y_AX)
for p in mpolys:
    top.add(p)
LW = 4.0
ys_, yg_ = Y_AX + 6.0, Y_AX - 6.0
x_s, x_g = x_turn_c - 8.0, x_turn_c + 8.0     # the left lead turns first (to the upper pad)
y_ps = [p[3] for p in pads if p[1] == "SNSPD_S"][0]
y_pg = [p[3] for p in pads if p[1] == "SNSPD_G"][0]
for pts in ([sig_tab, (sig_tab[0] - 10, sig_tab[1]), (sig_tab[0] - 10, ys_), (x_s, ys_), (x_s, y_ps), (X_COL, y_ps)],
            [gnd_tab, (gnd_tab[0] - 25, gnd_tab[1]), (gnd_tab[0] - 25, yg_), (x_g, yg_), (x_g, y_pg), (X_COL, y_pg)]):
    for p in path(pts, LW, L_LEAD):
        top.add(p)
snspd_pad_polys = [rect(X_COL - PAD_W / 2, yy - PAD_H / 2, X_COL + PAD_W / 2, yy + PAD_H / 2, L_LEAD) for yy in (y_ps, y_pg)]
for p in snspd_pad_polys:
    top.add(p)
# Buried ITO (layer 31, 60 nm on the 80 nm cap, under D2): optical matching layer + RF shield
# (log step 9b). Grounded to M1 through a 10 x 10 um via (layer 24, etched through cap + spacer)
# 60 um on the +x side (the SNSPD leads leave on the -x side). Stays within |y| <= 18 um of the
# axis, i.e. under the centre DC only, never under the RF rails (log step 10: ITO under the rails
# adds loss, no shielding).
XV = X_READ + DET_WX / 2 + 45
top.add(rect(X_READ - DET_WX / 2 - 8, Y_AX - 18, XV + 12, Y_AX + 18, L_ITOB))
top.add(rect(XV - 5, Y_AX - 5, XV + 5, Y_AX + 5, L_VIA))
# ITO patch on D2 (log step 6, decision 3): overlaps the centre-DC Au by 5 um along the axis and by
# 3 um radially, so its radial edges sit 2 um inside the Au edge (an L30-L50 overlay error then can
# not put ITO into the gap next to the RF rail; traveler item A6)
top.add(rect(X_READ - WIN_WX / 2 - 5, Y_AX - WIN_WY / 2 - 3, X_READ + WIN_WX / 2 + 5, Y_AX + WIN_WY / 2 + 3, L_ITO))

# EBL alignment marks on layer 22 (traveler item A2): 20 um crosses, 2 um arms, Ti/Au (high
# backscatter contrast), four around the readout zone inside one EBL write field, buried under D2
EBL_MARKS = [(X_READ - 300, Y_AX + 590), (X_READ + 300, Y_AX + 590),
             (X_READ - 300, Y_AX - 650), (X_READ + 300, Y_AX - 650)]
for xm, ym in EBL_MARKS:
    top.add(rect(xm - 10, ym - 1, xm + 10, ym + 1, L_LEAD), rect(xm - 1, ym - 10, xm + 1, ym + 10, L_LEAD))


# ------------------------------------------------------------------ test structures (lower half)
def test_structures():
    """Probe-station structures in the empty lower half (not wire bonded). Returns
    (Au polygons per name, polygons on other layers, D2 openings, labels, Au keep-out boxes)."""
    au_t, other, d2, labels, boxes = {}, [], [], [], []
    P = 150.0

    def pad(x, y, layer=L_AU):
        return rect(x - P / 2, y - P / 2, x + P / 2, y + P / 2, layer)

    # T1: Au comb, 5 um gaps, 20 fingers x 100 um (DC leakage / flashover; Dietl 2025, Sterling 2013)
    x0, y0 = -3000.0, -3000.0
    fa = [pad(x0, y0), rect(x0 + 75, y0 - 10, x0 + 520, y0 + 10)]
    fb = [pad(x0 + 700, y0 + 250), rect(x0 + 80, y0 + 240, x0 + 625, y0 + 260)]
    for k in range(20):
        xf = x0 + 100 + k * 20
        if k % 2 == 0:
            fa.append(rect(xf, y0 + 10, xf + 15, y0 + 235))
        else:
            fb.append(rect(xf, y0 + 15, xf + 15, y0 + 240))
    au_t["T1a"], au_t["T1b"] = fa, fb
    boxes.append(rect(x0 - 120, y0 - 120, x0 + 820, y0 + 370))
    labels.append(("T1 Au comb 5um", x0, y0 - 170))
    # T2: Au / D2 / M1 capacitor, 1 x 1 mm (D2 integrity, leakage, ~3.5 pF) + M1 contact opening
    x0, y0 = -1000.0, -3000.0
    au_t["T2"] = [rect(x0 - 500, y0 - 500, x0 + 500, y0 + 500)]
    d2.append(rect(x0 + 640, y0 - 70, x0 + 780, y0 + 70, L_D2OPEN))
    boxes.append(rect(x0 - 520, y0 - 520, x0 + 520, y0 + 520))
    labels.append(("T2 Au/D2/M1 cap 1mm2, M1 pad right", x0 - 500, y0 - 600))
    # T3: NbN 4-wire bar 10 x 200 um (R_sq, Tc) with Ti/Au pads (layer 22, D2 opened, no M1 below)
    x0, y0 = 1000.0, -3000.0
    other.append(rect(x0 - 100, y0 - 5, x0 + 100, y0 + 5, L_NBN))
    for xs, xp in ((-100, -300), (-40, -100), (40, 100), (100, 300)):
        other.append(rect(x0 + xs - 5, y0 - 5, x0 + xs + 5, y0 + 60, L_NBN))
        other += path([(x0 + xs, y0 + 55), (x0 + xs, y0 + 120), (x0 + xp, y0 + 250), (x0 + xp, y0 + 300)], 6.0, L_LEAD)
        other.append(pad(x0 + xp, y0 + 380, L_LEAD))
        d2.append(rect(x0 + xp - 55, y0 + 325, x0 + xp + 55, y0 + 435, L_D2OPEN))
    boxes.append(rect(x0 - 400, y0 - 60, x0 + 400, y0 + 480))
    labels.append(("T3 NbN 4-wire bar", x0 - 300, y0 - 120))
    # T4: spare SNSPD identical to the trap meander, own pads, ITO patch (cold test without a trap)
    x0, y0 = 3000.0, -3000.0
    sp, stab, gtab = meander(x0, y0)
    other += sp
    for tab, py in ((stab, 250), (gtab, -250)):
        other += path([tab, (x0 - 300, tab[1]), (x0 - 300, y0 + py)], 4.0, L_LEAD)
        other.append(pad(x0 - 300, y0 + py, L_LEAD))
        d2.append(rect(x0 - 355, y0 + py - 55, x0 - 245, y0 + py + 55, L_D2OPEN))
    other.append(rect(x0 - DET_WX / 2 - 5, y0 - DET_WY / 2 - 5, x0 + DET_WX / 2 + 5, y0 + DET_WY / 2 + 5, L_ITO))
    other.append(rect(x0 - DET_WX / 2 - 8, y0 - 18, x0 + DET_WX / 2 + 57, y0 + 18, L_ITOB))
    other.append(rect(x0 + DET_WX / 2 + 40, y0 - 5, x0 + DET_WX / 2 + 50, y0 + 5, L_VIA))
    boxes.append(rect(x0 - 420, y0 - 370, x0 + 120, y0 + 370))
    labels.append(("T4 spare SNSPD", x0 - 300, y0 - 450))
    # T5: ITO 4-wire bar 20 x 400 um on D2, contacted by Au fingers (sheet resistance, ITO/Au contact)
    x0, y0 = 1000.0, -1500.0
    other.append(rect(x0 - 200, y0 - 10, x0 + 200, y0 + 10, L_ITO))
    for k, xp in enumerate((-195, -60, 60, 195)):
        au_t[f"T5{k}"] = [rect(x0 + xp - 5, y0 - 15, x0 + xp + 5, y0 + 200), pad(x0 + xp * 1.6, y0 + 300)] + \
            path([(x0 + xp, y0 + 195), (x0 + xp * 1.6, y0 + 230)], 10.0)
    boxes.append(rect(x0 - 420, y0 - 40, x0 + 420, y0 + 400))
    labels.append(("T5 ITO 4-wire", x0 - 200, y0 - 120))
    # T6: continuity loop: 6 um Au line, ~4 mm meander, two pads (Dietl 2025 two-pad loop)
    x0, y0 = -3000.0, -1500.0
    pts = [(x0 + 75, y0)]
    for k in range(8):
        xk = x0 + 150 + k * 60
        pts += [(xk, y0 + (0 if k % 2 == 0 else 500)), (xk, y0 + (500 if k % 2 == 0 else 0))]
    pts += [(x0 + 680, y0)]
    au_t["T6"] = path(pts, 6.0) + [pad(x0, y0), pad(x0 + 755, y0)]
    boxes.append(rect(x0 - 100, y0 - 100, x0 + 855, y0 + 530))
    labels.append(("T6 Au continuity loop", x0 - 70, y0 - 140))
    # T7: buried-ITO -> Al via chain (traveler item A5): 6 isolated Al islands + 2 Al pad islands
    # (cut out of the ground plane), joined by 30 um wide L31 ITO strips through 14 L24 vias.
    # 2-terminal R between the two pads = 14 via contacts + 7 ITO strips. Probe through D2 openings.
    x0, y0 = -1500.0, -1300.0
    xs_isl = [x0] + [x0 + 200 + k * 120 for k in range(6)] + [x0 + 200 + 6 * 120 + 100]
    m1_isl = []
    for k, xi in enumerate(xs_isl):
        half = 100.0 if k in (0, len(xs_isl) - 1) else 30.0
        m1_isl.append(rect(xi - half, y0 - half, xi + half, y0 + half, L_M1))
        if half > 50:
            d2.append(rect(xi - 85, y0 - 85, xi + 85, y0 + 85, L_D2OPEN))
    for k in range(len(xs_isl) - 1):
        xa_ = xs_isl[k] + (85 if k == 0 else 15)
        xb_ = xs_isl[k + 1] - (85 if k + 1 == len(xs_isl) - 1 else 15)
        other.append(rect(xa_ - 10, y0 - 15, xb_ + 10, y0 + 15, L_ITOB))
        other += [rect(xa_ - 5, y0 - 5, xa_ + 5, y0 + 5, L_VIA), rect(xb_ - 5, y0 - 5, xb_ + 5, y0 + 5, L_VIA)]
    t7_cut = rect(x0 - 130, y0 - 130, xs_isl[-1] + 130, y0 + 130)
    boxes.append(rect(x0 - 140, y0 - 140, xs_isl[-1] + 140, y0 + 140))
    labels.append(("T7 ITO-Al via chain (14 vias)", x0 - 100, y0 - 200))
    return au_t, other, d2, labels, boxes, m1_isl, t7_cut


au_test, other_test, d2_test, test_labels, test_boxes, t7_islands, t7_cut = test_structures()
for p in other_test:
    top.add(p)

# ------------------------------------------------------------------ D2 openings and M1 (Al)
d2_open = [rect(X_COL - PAD_W / 2 + 15, yy - PAD_H / 2 + 15, X_COL + PAD_W / 2 - 15, yy + PAD_H / 2 - 15, L_D2OPEN)
           for yy in (y_ps, y_pg)]
y_last_pad = min(p[3] for p in pads if p[0] != "RF")
m1_pads = [(X_COL, y_last_pad - 2 * PAD_P), (4750.0, 0.0), (4750.0, -3000.0), (0.0, -4750.0)]
for (xc, yc) in m1_pads:
    d2_open.append(rect(xc - 85, yc - 85, xc + 85, yc + 85, L_D2OPEN))
d2_open += d2_test
for p in d2_open:
    top.add(p)
chip_sq = rect(-CHIP, -CHIP, CHIP, CHIP, L_CHIP)
m1 = gdstk.offset(chip_sq, -EDGE_M1, layer=L_M1)
m1_cut = [rect(X_COL - 160, yy - 120, X_COL + 160, yy + 120) for yy in (y_ps, y_pg)]   # no Al under SNSPD pads
m1_cut += [rect(1000 - 420, -3000 + 300, 1000 + 420, -3000 + 470),                     # T3 pads
           rect(3000 - 420, -3000 - 330, 3000 - 200, -3000 + 330)]                       # T4 pads
MARK_SITES = ((-2000, -4780), (2000, -4780), (4780, 1000), (4780, -1500))
m1_cut += [rect(xm - 150, ym - 150, xm + 150, ym + 150) for xm, ym in MARK_SITES]   # A1: marks visible
m1_cut.append(t7_cut)
m1 = gdstk.boolean(m1, m1_cut, "not", layer=L_M1) + t7_islands
for p in m1:
    top.add(p)

# ------------------------------------------------------------------ alignment marks
# L1: Si-etched crosses (seen through the transparent oxides by the MLA / EBL); L40 crosses: D2-
# etched topography used to align the Au plating mold through the opaque seed. Mark sites are
# notches at the chip edge so the Au ground fill needs no holes.
mark_keepout = [rect(xm - 130, ym - 130, xm + 300, ym + 130) if xm > 4000 else
                rect(xm - 130, ym - 300, xm + 130, ym + 130) for xm, ym in MARK_SITES]
for xm, ym in MARK_SITES:
    top.add(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK), rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    top.add(rect(xm - 30, ym + 70, xm + 30, ym + 74, L_D2OPEN), rect(xm - 2, ym + 60, xm + 2, ym + 84, L_D2OPEN))
    for k, L in enumerate((L_NBN, L_LEAD, L_ITO, L_ITOB)):
        top.add(rect(xm - 90 + 40 * k, ym - 100, xm - 75 + 40 * k, ym - 85, L))
    top.add(rect(xm + 60, ym + 20, xm + 80, ym + 22, L_LEAD), rect(xm + 69, ym + 11, xm + 71, ym + 31, L_LEAD))

# ------------------------------------------------------------------ top Au: merge, ground fill
for n, ps in au_test.items():
    el[n] = ps
au = {n: gdstk.boolean(ps, [], "or", layer=L_AU) for n, ps in el.items()}
all_el = [p for ps in au.values() for p in ps]
au_area = gdstk.offset(chip_sq, -EDGE_AU)
near = rect(XRF0 - 300, Y_AX - y_dc1 - 300, XRF1 + 400, Y_AX + y_dc1 + 300)
keep = gdstk.boolean(gdstk.offset(all_el, GAP_FAR, join="miter"), near, "not")
keep = gdstk.boolean(keep, gdstk.boolean(gdstk.offset(all_el, G, join="miter"), near, "and"), "or")
keep = gdstk.boolean(keep, [win] + [gdstk.offset(p, 20)[0] for p in d2_open + snspd_pad_polys] +
                     mark_keepout + test_boxes, "or")
ground = gdstk.boolean(au_area, keep, "not", layer=L_AU)
# keep only the main (connected) ground: strips enclosed between parallel leads would be floating
# Au islands; leaving them empty exposes the Al plane at the bottom of the D2 etch instead (grounded)
ground = [max(ground, key=lambda p: p.area())]
for p in all_el + ground:
    p.layer = L_AU
    top.add(p)
# L45 PROTECT (traveler item A3, step 16a): resist kept on during the Au-masked D2 gap etch over
# every place that has no Au mask but must keep its D2: bond/probe openings (+10 um), test areas
# without Au (T3, T4, T5, T7), the readout window (+2.5 um onto the Au rim) and the stretch where
# the buried SNSPD leads leave the centre-DC lead and cross lead gaps on the way to their pads.
prot = [gdstk.offset(p, 10)[0] for p in d2_open + snspd_pad_polys]
prot += [rect(X_READ - WIN_WX / 2 - 2.5, Y_AX - WIN_WY / 2 - 2.5, X_READ + WIN_WX / 2 + 2.5, Y_AX + WIN_WY / 2 + 2.5)]
prot += [rect(1000 - 400, -3000 - 60, 1000 + 400, -3000 + 480), rect(3000 - 420, -3000 - 370, 3000 + 120, -3000 + 370),
         rect(1000 - 220, -1500 - 30, 1000 + 220, -1500 + 30), t7_cut]
prot += [rect(x_s - 20, y_pg - 20, x_g + 20, y_pad_c + 30),
         rect(X_COL, y_ps - 20, x_s + 20, y_ps + 20), rect(X_COL, y_pg - 20, x_g + 20, y_pg + 20)]
for p in gdstk.boolean(prot, [], "or", layer=L_PROT):
    top.add(p)
top.add(chip_sq)
for txt, (x, y) in [(f"TRAP_CHIP_V1 {VARIANT}  138Ba+ h50  NbN SNSPD", (-3500, 1000)),
                    ("LOAD", (X_LOAD - 50, Y_AX + 420)), ("READ", (X_READ - 50, Y_AX + 420))] + \
                   [(t, (x, y)) for t, x, y in test_labels]:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)

# ground-fill bond spots (traveler item A4): plain ground fill, 200 x 200 um kept free of features
GND_PADS = [(X_COL, y_last_pad - 4 * PAD_P), (4750.0, 1700.0), (4750.0, -500.0)]
for x, y in GND_PADS:
    for p in gdstk.text("GND", 30, (x - 45, y - 15), layer=L_NOTE):
        top.add(p)
STEM = "trap_chip_v1" if VARIANT == "A30" else "trap_chip_v1_B60"
lib.write_gds(os.path.join(HERE, STEM + ".gds"))

# ------------------------------------------------------------------ simulation layout + pad list
sim = {
    "_comment": f"gds2itvg layout for {STEM}.gds layer 50 (generated by gds/make_chip.py). Trap axis = "
                "GDS x -> ITVG y; origin at the readout zone. Stack: 6 um Au on 10 um SiO2 over Al.",
    "_zones": {"readout_itvg_y": 0.0, "loading_itvg_y": X_LOAD - X_READ},
    "layer": L_AU, "datatype": 0, "cell": f"TRAP_CHIP_V1_{VARIANT}",
    "roi_box": [XRF0 - 50, Y_AX - y_dc1 - 30, XRF1 + U_BAR + 30, Y_AX + y_dc1 + 30],
    "frame": {"origin": [X_READ, Y_AX], "quarter_turns": 1, "mirror": False},
    "max_gap": 30.0, "gap_model": "profile", "metal_thickness": 6.0, "ground_depth": 10.0,
    "epsilon_r": 3.9, "outer_ground_depth": None,
    "electrodes": {k: seeds[k] for k in sorted(seeds, key=int)},
    "ground": {"99": [[XRF0 + 600, Y_AX + y_dc1 + 300]]},
    # ITO patch on D2 is tied to the centre DC: electrostatically the window is filled at the
    # centre-DC potential (its 6 um recess is quantified separately by sim/04b, about -1.2 um)
    "fill": {"2": [[[X_READ - WIN_WX / 2, Y_AX - WIN_WY / 2], [X_READ + WIN_WX / 2, Y_AX - WIN_WY / 2],
                    [X_READ + WIN_WX / 2, Y_AX + WIN_WY / 2], [X_READ - WIN_WX / 2, Y_AX + WIN_WY / 2]]]},
}
with open(os.path.join(HERE, STEM + "_sim.json"), "w") as fh:
    json.dump(sim, fh, indent=1)
role = {"1": "RF", "2": "centre DC", "SNSPD_S": "SNSPD signal (layer 22 pad, D2 opened)",
        "SNSPD_G": "SNSPD return (layer 22 pad, D2 opened)"}
role.update({n: f"top segment, centre {seg_cent[k] - X_READ:+.0f} um from readout" for k, n in enumerate(n_top)})
role.update({n: f"bottom segment, centre {seg_cent[k] - X_READ:+.0f} um from readout" for k, n in enumerate(n_bot)})
role.update({"33": "top cap left", "34": "top cap right", "35": "bottom cap left", "36": "bottom cap right"})
with open(os.path.join(HERE, STEM + "_pads.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["pad", "electrode", "role", "x_um", "y_um", "layer"])
    for num, name, x, y, L in pads:
        w.writerow([num, name, role.get(name, name), f"{x:.0f}", f"{y:.0f}", L])
    for k, (x, y) in enumerate(GND_PADS):
        w.writerow([f"GND-{k + 1}", "ground fill", "Au ground fill: bond to carrier ground (traveler A4)",
                    f"{x:.0f}", f"{y:.0f}", L_AU])
    for k, (x, y) in enumerate(m1_pads):
        w.writerow([f"M1-{k + 1}", "ground plane", "Al M1 through D2 opening", f"{x:.0f}", f"{y:.0f}", L_D2OPEN])
n_trap = len([n for n in el if not n.startswith("T")])
print(f"wrote {STEM}.gds: {n_trap} trap electrodes, {len(pads)} bond pads + {len(m1_pads)} M1 pads, "
      f"meander {nlines} lines ({DET_WX:g} x {DET_WY:g} um, {nlines * DET_WX / 1000:.1f} mm of wire)")
