"""Test-structure die, 10 mm x 2.5 mm (Claude-authored). Probe-station structures that check each
process module of the trap die (traveler sections A/E, test_plan.md (a)); same layer stack and
layer numbers as make_chip.py. Nothing here is wire bonded.

  T1  Au comb, 5 um gaps (DC leakage / flashover across the trap gap; Dietl 2025, Sterling 2013)
  T2  Au / D2 / M1 capacitor 0.8 x 0.8 mm + M1 contact (D2 integrity, leakage, ~2.2 pF)
  T3  NbN 4-wire bar 10 x 200 um with Ti/Au pads (R_sq, Tc of the patterned film)
  T4  spare SNSPD = trap meander (30 x 30 um) with buried ITO + via + top ITO (cold test, no trap)
  T4b spare SNSPD, 60 x 30 um (B60 meander)
  T5  top-ITO 4-wire bar 20 x 400 um on D2 with Au contacts (R_sq, ITO/Au contact)
  T6  Au continuity loop, 6 um line (Dietl 2025 two-pad loop)
  T7  buried-ITO -> Al via chain, 14 vias (grounding of the buried ITO; traveler item A5)
  T8  EBL dose array: seven copies of the 30 x 30 um trap meander, no ITO, each on its own layer-20
      datatype 1..7 so the EBL job can give each a different dose (DOSE_FACTORS below, x the nominal
      dose of datatype 0). SEM linewidth after step 7, then 2-wire R at room temperature and cold.
--trap-only writes test_die_v2_TRAP.gds for trap-only runs (run_R1_TRAP, traveler steps 4-8b and 10
skipped): only T1, T2 and T6, and nothing on layers 20-31, so no D2 opening lands on bare oxide.
Run from design/sim:  ./run.sh ../gds/make_test_die.py [--trap-only]
"""

import os
import sys

import gdstk

HERE = os.path.dirname(os.path.abspath(__file__))
L_MARK, L_M1, L_NBN, L_LEAD, L_VIA, L_ITO, L_ITOB, L_D2OPEN, L_PROT, L_AU = 1, 10, 20, 22, 24, 30, 31, 40, 45, 50
L_NOTE, L_CHIP = 100, 101
CX, CY = 5000.0, 1250.0
WIRE_W, WIRE_P, TAB_L, TAB_H = 0.100, 0.200, 40.0, 3.0
P = 150.0                                          # probe pad size
DOSE_FACTORS = (0.80, 0.87, 0.93, 1.00, 1.07, 1.13, 1.20)   # T8, datatypes 1..7 (mask_list.md L20)

lib = gdstk.Library(unit=1e-6, precision=1e-9)
TRAP_ONLY = "--trap-only" in sys.argv
STEM, CELL = ("test_die_v2_TRAP", "TEST_DIE_V2_TRAP") if TRAP_ONLY else ("test_die_v2", "TEST_DIE_V2")
top = lib.new_cell(CELL)
au, other, d2, boxes, prot, m1_cut, m1_extra, labels = {}, [], [], [], [], [], [], []


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


def pad(x, y, layer=L_AU):
    return rect(x - P / 2, y - P / 2, x + P / 2, y + P / 2, layer)


def meander(xc, yc, wx, wy):
    polys, n = [], int(round(wy / WIRE_P))
    n += n % 2
    x0m, x1m, y0m = xc - wx / 2, xc + wx / 2, yc - wy / 2
    for k in range(n):
        y = y0m + k * WIRE_P
        polys.append(rect(x0m, y, x1m, y + WIRE_W, L_NBN))
        if k < n - 1:
            xe = x1m if k % 2 == 0 else x0m - WIRE_W
            polys.append(rect(xe, y, xe + WIRE_W, y + WIRE_P + WIRE_W, L_NBN))
    yl = y0m + (n - 1) * WIRE_P
    polys += [rect(x0m - TAB_L, y0m - TAB_H, x0m, y0m + WIRE_W, L_NBN), rect(x0m - TAB_L, yl, x0m, yl + WIRE_W + TAB_H, L_NBN)]
    return polys, (x0m - 20, yl + TAB_H / 2), (x0m - 20, y0m - TAB_H / 2)


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


def t4(x0, y0, wx, name):
    polys, stab, gtab = meander(x0, y0, wx, 30.0)
    other.extend(polys)
    for tab, py in ((stab, 250), (gtab, -250)):
        other.extend(path([tab, (x0 - wx / 2 - 280, tab[1]), (x0 - wx / 2 - 280, y0 + py)], 4.0, L_LEAD))
        other.append(pad(x0 - wx / 2 - 280, y0 + py, L_LEAD))
        d2.append(rect(x0 - wx / 2 - 335, y0 + py - 55, x0 - wx / 2 - 225, y0 + py + 55, L_D2OPEN))
    other.append(rect(x0 - wx / 2 - 5, y0 - 18, x0 + wx / 2 + 5, y0 + 18, L_ITO))
    other.append(rect(x0 - wx / 2 - 8, y0 - 18, x0 + wx / 2 + 57, y0 + 18, L_ITOB))
    other.append(rect(x0 + wx / 2 + 40, y0 - 5, x0 + wx / 2 + 50, y0 + 5, L_VIA))
    box = rect(x0 - wx / 2 - 400, y0 - 370, x0 + wx / 2 + 120, y0 + 370)
    boxes.append(box); prot.append(box)
    m1_cut.append(rect(x0 - wx / 2 - 400, y0 - 330, x0 - wx / 2 - 160, y0 + 330))
    labels.append((f"{name} spare SNSPD {wx:.0f}x30", x0 - wx / 2 - 380, y0 - 450))


def t5(x0, y0):
    other.append(rect(x0 - 200, y0 - 10, x0 + 200, y0 + 10, L_ITO))
    for k, xp in enumerate((-195, -60, 60, 195)):
        au[f"T5{k}"] = [rect(x0 + xp - 5, y0 - 15, x0 + xp + 5, y0 + 200), pad(x0 + xp * 1.6, y0 + 300)] + \
            path([(x0 + xp, y0 + 195), (x0 + xp * 1.6, y0 + 230)], 10.0)
    boxes.append(rect(x0 - 420, y0 - 40, x0 + 420, y0 + 400))
    prot.append(rect(x0 - 220, y0 - 30, x0 + 220, y0 + 30))
    labels.append(("T5 ITO 4-wire", x0 - 200, y0 - 120))


def t6(x0, y0):
    pts = [(x0 + 75, y0)]
    for k in range(8):
        xk = x0 + 150 + k * 60
        pts += [(xk, y0 + (0 if k % 2 == 0 else 500)), (xk, y0 + (500 if k % 2 == 0 else 0))]
    pts += [(x0 + 680, y0)]
    au["T6"] = path(pts, 6.0) + [pad(x0, y0), pad(x0 + 755, y0)]
    boxes.append(rect(x0 - 100, y0 - 100, x0 + 855, y0 + 530))
    labels.append(("T6 Au continuity loop", x0 - 70, y0 - 140))


def t7(x0, y0):
    xs = [x0] + [x0 + 200 + k * 120 for k in range(6)] + [x0 + 200 + 6 * 120 + 100]
    for k, xi in enumerate(xs):
        h = 100.0 if k in (0, len(xs) - 1) else 30.0
        m1_extra.append(rect(xi - h, y0 - h, xi + h, y0 + h, L_M1))
        if h > 50:
            d2.append(rect(xi - 85, y0 - 85, xi + 85, y0 + 85, L_D2OPEN))
    for k in range(len(xs) - 1):
        xa = xs[k] + (85 if k == 0 else 15)
        xb = xs[k + 1] - (85 if k + 1 == len(xs) - 1 else 15)
        other.extend([rect(xa - 10, y0 - 15, xb + 10, y0 + 15, L_ITOB), rect(xa - 5, y0 - 5, xa + 5, y0 + 5, L_VIA),
                      rect(xb - 5, y0 - 5, xb + 5, y0 + 5, L_VIA)])
    cut = rect(x0 - 130, y0 - 130, xs[-1] + 130, y0 + 130)
    m1_cut.append(cut); boxes.append(rect(x0 - 140, y0 - 140, xs[-1] + 140, y0 + 140)); prot.append(cut)
    labels.append(("T7 ITO-Al via chain (14 vias)", x0 - 100, y0 - 200))


def t8(x0, y0, pitch=600.0):
    for k, f in enumerate(DOSE_FACTORS):
        xk = x0 + k * pitch
        polys, stab, gtab = meander(xk, y0, 30.0, 30.0)
        for q in polys:
            q.datatype = k + 1
        other.extend(polys)
        for tab, py in ((stab, 250), (gtab, -250)):
            other.extend(path([tab, (xk - 15 - 280, tab[1]), (xk - 15 - 280, y0 + py)], 4.0, L_LEAD))
            other.append(pad(xk - 15 - 280, y0 + py, L_LEAD))
            d2.append(rect(xk - 15 - 335, y0 + py - 55, xk - 15 - 225, y0 + py + 55, L_D2OPEN))
        box = rect(xk - 15 - 400, y0 - 370, xk + 15 + 120, y0 + 370)
        boxes.append(box); prot.append(box)
        m1_cut.append(rect(xk - 15 - 400, y0 - 330, xk - 15 - 160, y0 + 330))
        labels.append((f"D{k + 1} x{f:.2f}", xk - 120, y0 + 60))
    labels.append(("T8 EBL dose array (datatypes 1-7)", x0 - 380, y0 - 450))


# upper row (y ~ +400) and lower row (y ~ -600)
t1(-4300, 350)
t2(-2550, 400)
t6(3500, 300)
if not TRAP_ONLY:                                  # SNSPD, ITO and via structures
    t3(-1000, 250)
    t4(600, 450, 30.0, "T4")
    t4(2300, 450, 60.0, "T4b")
    t5(-4000, -700)
    t7(-2700, -650)
    t8(-1000, -650)
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
for p in gdstk.boolean(gdstk.offset(die, -150), m1_cut, "not", layer=L_M1) + m1_extra:
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
for txt, x, y in labels + [(CELL, 3200, -700)]:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)
lib.write_gds(os.path.join(HERE, STEM + ".gds"))
print(f"wrote {STEM}.gds")
