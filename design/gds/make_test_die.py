"""Test-structure die, 10 mm x 2.5 mm (Claude-authored). Probe-station structures that check each
process module of the trap die (traveler sections A/E, test_plan.md (a)); same layer stack and
layer numbers as make_chip.py. Nothing here is wire bonded.

  T1  Au comb, 5 um gaps (DC leakage / flashover across the trap gap; Dietl 2025, Sterling 2013)
  T2  Au / D2 / M1 capacitor 0.8 x 0.8 mm + M1 contact (D2 integrity, leakage, ~2.2 pF)
  T3  NbN 4-wire bar 10 x 200 um with Ti/Au pads (R_sq, Tc of the patterned film)
  T4  spare SNSPD = trap meander (v3.1 A30: 130 / 200 nm, 36 x 34 um, rounded turns) under cap + D2,
      no ITO (cold test, no trap)
  T4b spare SNSPD, v3.1 B60 meander (69 x 34 um)
  T6  Au continuity loop, 6 um line (Dietl 2025 two-pad loop)
  (v3: T5 ITO bar and T7 ITO -> Al via chain removed with the ITO; DESIGN_LOG step 17)
  T8  EBL dose array: seven copies of the A30 trap meander, no ITO, each on its own layer-20
      datatype 1..7 so the EBL job can give each a different dose (DOSE_FACTORS below, x the nominal
      dose of datatype 0). SEM linewidth after step 7, then 2-wire R at room temperature and cold.
  T9  geometry array (DESIGN_LOG step 24; list T9 below): v3 sharp 100/200 control, 100/200 rounded,
      130/200 rounded, 140/200 rounded, 300/600 rounded, a short 130/200 meander (length series),
      and straight-wire Ic references at 100, 130, 140, 300 nm. Compared as ratios between neighbours.
Writes test_die_v3.gds. --trap-only writes test_die_v3_TRAP.gds for trap-only runs (run_R1_TRAP, SNSPD
steps skipped): only T1, T2 and T6, and nothing on layers 20-22, so no D2 opening lands on bare oxide.
Run from design/sim:  ./run.sh ../gds/make_test_die.py [--trap-only]
"""

import os
import sys

import gdstk

from snspd_geom import meander, straight

HERE = os.path.dirname(os.path.abspath(__file__))
L_MARK, L_M1, L_NBN, L_LEAD, L_D2OPEN, L_PROT, L_AU = 1, 10, 20, 22, 40, 45, 50   # no ITO / via layers (v3)
L_NOTE, L_CHIP = 100, 101
CX, CY = 5000.0, 1250.0
# v3.1 trap meander (make_chip.py, DESIGN_LOG step 24): 130 / 200 nm, rounded turns, lines 36 um (A30) or
# 69 um (B60) long, 32 um radial extent
WIRE_W, WIRE_P = 0.130, 0.200
DET_A30, DET_B60, DET_WY = 36.0, 69.0, 32.0
# T9 geometry array: (x0, y0, spec); spec = ('m', w, p, turn, lx, ly) or ('s', w_top, w_bottom)
T9 = [(-4380, -650, ("m", 0.100, 0.200, "sharp", 30.0, 30.0)),     # v3 control
      (-3780, -650, ("m", 0.100, 0.200, "round", DET_A30, DET_WY)),  # turn shape only
      (-3180, -650, ("m", 0.130, 0.200, "round", DET_A30, DET_WY)),  # v3.1 (= T4), paired with the two above
      (-2580, -650, ("m", 0.140, 0.200, "round", DET_A30, DET_WY)),
      (-2000, -650, ("m", 0.300, 0.600, "round", DET_A30, DET_WY)),  # Suleimen et al. 2026 width comparison
      (-100, 450, ("m", 0.130, 0.200, "round", 18.0, 17.0)),          # length series: 1/4 of the wire
      (3160, -650, ("s", 0.100, 0.130)),                             # straight Ic references
      (3760, -650, ("s", 0.140, 0.300))]
P = 150.0                                          # probe pad size
DOSE_FACTORS = (0.80, 0.87, 0.93, 1.00, 1.07, 1.13, 1.20)   # T8, datatypes 1..7 (mask_list.md L20)

lib = gdstk.Library(unit=1e-6, precision=1e-9)
TRAP_ONLY = "--trap-only" in sys.argv
STEM, CELL = ("test_die_v3_TRAP", "TEST_DIE_V3_TRAP") if TRAP_ONLY else ("test_die_v3", "TEST_DIE_V3")
top = lib.new_cell(CELL)
au, other, d2, boxes, prot, m1_cut, labels = {}, [], [], [], [], [], []


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


def pad(x, y, layer=L_AU):
    return rect(x - P / 2, y - P / 2, x + P / 2, y + P / 2, layer)


def snspd(x0, y0, lx, ly, w=WIRE_W, p=WIRE_P, turn="round", datatype=0):
    """One meander (gds/snspd_geom.py) with two Ti/Au probe pads to its left, under cap + D2 (T4, T8, T9)."""
    polys, stab, gtab = meander(x0, y0, lx, ly, w, p, turn=turn, layer=L_NBN)
    for q in polys:
        q.datatype = datatype
    other.extend(polys)
    xp = x0 - lx / 2 - 280
    for tab, py in ((stab, 250), (gtab, -250)):
        other.extend(path([tab, (xp, tab[1]), (xp, y0 + py)], 4.0, L_LEAD))
        other.append(pad(xp, y0 + py, L_LEAD))
        d2.append(rect(xp - 55, y0 + py - 55, xp + 55, y0 + py + 55, L_D2OPEN))
    box = rect(x0 - lx / 2 - 400, y0 - 370, x0 + lx / 2 + 120, y0 + 370)
    boxes.append(box); prot.append(box)
    m1_cut.append(rect(x0 - lx / 2 - 400, y0 - 330, x0 - lx / 2 - 160, y0 + 330))


def straights(x0, y0, widths, lx=30.0):
    """Two straight NbN wires (Ic references), each with its own two pads: one above y0, one below (T9)."""
    for w, s in zip(widths, (+1, -1)):
        polys, ltab, rtab = straight(x0, y0 + s * 40, lx, w, layer=L_NBN)
        other.extend(polys)
        for tab, xp in ((ltab, x0 - 200), (rtab, x0 + 200)):
            other.extend(path([tab, (xp, tab[1]), (xp, y0 + s * 250)], 4.0, L_LEAD))
            other.append(pad(xp, y0 + s * 250, L_LEAD))
            d2.append(rect(xp - 55, y0 + s * 250 - 55, xp + 55, y0 + s * 250 + 55, L_D2OPEN))
    box = rect(x0 - 300, y0 - 370, x0 + 300, y0 + 370)
    boxes.append(box); prot.append(box)
    m1_cut.extend([rect(x0 - 300, y0 + 160, x0 + 300, y0 + 340), rect(x0 - 300, y0 - 340, x0 + 300, y0 - 160)])


def t1(x0, y0):
    fa = [pad(x0, y0), rect(x0 + 75, y0 - 10, x0 + 520, y0 + 10)]
    fb = [pad(x0 + 700, y0 + 250), rect(x0 + 80, y0 + 240, x0 + 625, y0 + 260)]
    for k in range(20):
        xf = x0 + 100 + k * 20
        (fa if k % 2 == 0 else fb).append(rect(xf, y0 + (10 if k % 2 == 0 else 15), xf + 15, y0 + (235 if k % 2 == 0 else 240)))
    au["T1a"], au["T1b"] = fa, fb
    boxes.append(rect(x0 - 120, y0 - 120, x0 + 820, y0 + 370))
    labels.append(("T1 Au comb 5um gap", x0, y0 - 170))


def t2(x0, y0, s=400.0):
    au["T2"] = [rect(x0 - s, y0 - s, x0 + s, y0 + s)]
    d2.append(rect(x0 + s + 140, y0 - 70, x0 + s + 280, y0 + 70, L_D2OPEN))
    boxes.append(rect(x0 - s - 20, y0 - s - 20, x0 + s + 20, y0 + s + 20))
    labels.append(("T2 Au/D2/M1 cap + M1 pad", x0 - s, y0 - s - 90))


def t3(x0, y0):
    other.append(rect(x0 - 100, y0 - 5, x0 + 100, y0 + 5, L_NBN))
    for xs, xp in ((-100, -300), (-40, -100), (40, 100), (100, 300)):
        other.append(rect(x0 + xs - 5, y0 - 5, x0 + xs + 5, y0 + 60, L_NBN))
        other.extend(path([(x0 + xs, y0 + 55), (x0 + xs, y0 + 120), (x0 + xp, y0 + 250), (x0 + xp, y0 + 330)], 6.0, L_LEAD))   # ends inside the pad
        other.append(pad(x0 + xp, y0 + 380, L_LEAD))
        d2.append(rect(x0 + xp - 55, y0 + 325, x0 + xp + 55, y0 + 435, L_D2OPEN))
    box = rect(x0 - 400, y0 - 60, x0 + 400, y0 + 480)
    boxes.append(box); prot.append(box); m1_cut.append(rect(x0 - 400, y0 + 300, x0 + 400, y0 + 470))
    labels.append(("T3 NbN 4-wire bar", x0 - 300, y0 - 120))


def t4(x0, y0, lx, name):
    snspd(x0, y0, lx, DET_WY)
    labels.append((f"{name} spare SNSPD {lx:.0f}x{DET_WY:.0f}", x0 - lx / 2 - 380, y0 - 450))


def t9(x0, y0, spec):
    """T9 geometry array slot: ('m', w, p, turn, lx, ly) meander or ('s', w_top, w_bottom) straight pair."""
    if spec[0] == "m":
        _, w, p, turn, lx, ly = spec
        snspd(x0, y0, lx, ly, w, p, turn)
        labels.append((f"T9 {w * 1000:.0f}/{p * 1000:.0f} {turn} {lx:g}x{ly:g}", x0 - lx / 2 - 380, y0 - 450))
    else:
        straights(x0, y0, spec[1:])
        labels.append((f"T9 straight {spec[1] * 1000:.0f} / {spec[2] * 1000:.0f} nm", x0 - 280, y0 - 450))


def t6(x0, y0):
    pts = [(x0 + 75, y0)]
    for k in range(8):
        xk = x0 + 150 + k * 60
        pts += [(xk, y0 + (0 if k % 2 == 0 else 500)), (xk, y0 + (500 if k % 2 == 0 else 0))]
    pts += [(x0 + 680, y0)]
    au["T6"] = path(pts, 6.0) + [pad(x0, y0), pad(x0 + 755, y0)]
    boxes.append(rect(x0 - 100, y0 - 100, x0 + 855, y0 + 530))
    labels.append(("T6 Au continuity loop", x0 - 70, y0 - 140))


def t8(x0, y0, pitch=600.0):
    for k, f in enumerate(DOSE_FACTORS):
        xk = x0 + k * pitch
        snspd(xk, y0, DET_A30, DET_WY, datatype=k + 1)
        labels.append((f"D{k + 1} x{f:.2f}", xk - 120, y0 + 60))
    labels.append(("T8 EBL dose array (datatypes 1-7)", x0 - 380, y0 - 450))


# upper row (y ~ +400) and lower row (y ~ -600)
t1(-4300, 350)
t2(-2550, 400)
t6(3500, 300)
if not TRAP_ONLY:                                  # SNSPD structures
    t3(-1000, 250)
    t4(600, 450, DET_A30, "T4")
    t4(2300, 450, DET_B60, "T4b")
    t8(-1000, -650)
    for x0, y0, spec in T9:
        t9(x0, y0, spec)
for p in other:
    top.add(p)
for p in d2:
    top.add(p)
MARK_SITES = ((-1700.0, -CY + 170), (4300.0, -CY + 170), (-1700.0, CY - 170), (4300.0, CY - 170))
for xm, ym in MARK_SITES:
    top.add(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK), rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    top.add(rect(xm - 30, ym + 70, xm + 30, ym + 74, L_D2OPEN), rect(xm - 2, ym + 60, xm + 2, ym + 84, L_D2OPEN))
    if not TRAP_ONLY:
        top.add(rect(xm - 100, ym - 1, xm - 80, ym + 1, L_LEAD), rect(xm - 91, ym - 10, xm - 89, ym + 10, L_LEAD))
die = rect(-CX, -CY, CX, CY, L_CHIP)
m1_cut += [rect(xm - 150, ym - 150, xm + 150, ym + 150) for xm, ym in MARK_SITES]
for p in gdstk.boolean(gdstk.offset(die, -150), m1_cut, "not", layer=L_M1):
    top.add(p)
els = [p for ps in au.values() for p in gdstk.boolean(ps, [], "or", layer=L_AU)]
keep = gdstk.boolean(gdstk.offset(els, 10, join="miter"), boxes + [rect(xm - 160, ym - 140, xm + 160, ym + 140) for xm, ym in MARK_SITES], "or")
ground = gdstk.boolean(gdstk.offset(die, -100), keep, "not", layer=L_AU)
for p in els + [max(ground, key=lambda q: q.area())]:
    p.layer = L_AU
    top.add(p)
for p in gdstk.boolean([gdstk.offset(q, 10)[0] for q in d2] + prot, [], "or", layer=L_PROT):
    top.add(p)
top.add(die)
for txt, x, y in labels + [(CELL, -1300, 1150)]:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)
lib.write_gds(os.path.join(HERE, STEM + ".gds"))
print(f"wrote {STEM}.gds")
