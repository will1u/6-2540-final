"""Test-structure die, 10 mm x 2.5 mm, v4 stack (Claude-authored). Probe-station structures that check each
process module of the trap die (traveler sections A/E, test_plan.md (a)); same layer numbers as make_chip.py.
Nothing here is wire bonded.

v4 stack (DESIGN_LOG step 25): Si / 1 um SiO2 / Al 100 nm, inlaid (layer 10) only as local patches / 238 nm SiO2 spacer /
NbN (layer 20) with Ti/Au contacts (layer 22) / 160 nm SiO2 cap / Au electrodes (layer 50) directly on top.
Layer 40 = openings through the thin SiO2 only: through the 160 nm cap onto a layer-22 pad, or through cap +
spacer (0.40 um) onto Al. Layer 45 is retired and stays empty. Layers 24, 30, 31 stay empty.

  T1   Au comb, 5 um gaps (DC leakage / flashover across the trap gap; Dietl 2025, Sterling 2013)
  T2v  Au / SiO2 / Al capacitor through the cap + spacer, placed where T2 was (~3.5 pF)
  T3   NbN 4-wire bar 10 x 200 um with Ti/Au pads (R_sq, Tc of the patterned film)
  T4   spare SNSPD = trap meander (v3.1 A30: 130 / 200 nm, 36 x 32 um, rounded turns), local Al mirror
  T4b  spare SNSPD, v3.1 B60 meander (69 x 32 um), local Al mirror
  T6   Au continuity loop, 6 um line (Dietl 2025 two-pad loop)
  T8   EBL dose array: seven copies of the A30 trap meander, each on its own layer-20 datatype 1..7 so the
       EBL job can give each a different dose (DOSE_FACTORS below, x the nominal dose of datatype 0).
       SEM linewidth after step 7, then 2-wire R at room temperature and cold.
  T9   geometry array (DESIGN_LOG step 24; list T9 below). Compared as ratios between neighbours.
  T10  mirror strip resistance, four-point: Al strip 40 um wide, 2510 um long (the trap's mirror ground path)
  T11  Au-to-Al via chain, four vias in series
  T12  twin Au leads over an Al strip (models the SNSPD leads in the trap's slot)

Writes test_die_v4.gds (cell TEST_DIE_V4) and test_die_v4_preview.png. --trap-only writes test_die_v4_TRAP.gds
(cell TEST_DIE_V4_TRAP) and test_die_v4_TRAP_preview.png: only T1 and T6, the layer-1 marks, the Au ground fill,
the die outline and labels. Nothing on layers 10, 20, 22, 40 (the trap-only process has no Al).
A self-check at the end raises AssertionError if the keep-out or layer rules are broken.
Run from design/sim:  ./run.sh ../gds/make_test_die.py [--trap-only]
"""

import os
import sys

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from snspd_geom import meander, straight  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
L_MARK, L_M1, L_NBN, L_LEAD, L_VIA, L_AU = 1, 10, 20, 22, 40, 50   # 10 = Al, 40 = openings through the thin SiO2
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
STEM, CELL = ("test_die_v4_TRAP", "TEST_DIE_V4_TRAP") if TRAP_ONLY else ("test_die_v4", "TEST_DIE_V4")
top = lib.new_cell(CELL)
au, other, vias, keepouts, labels = {}, [], [], [], []   # au: Au conductors (one list per conductor)


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


def pad(x, y, layer=L_AU):
    return rect(x - P / 2, y - P / 2, x + P / 2, y + P / 2, layer)


def keep(name, x0, y0, x1, y1):
    """Keep-out box of one structure: the Au ground fill stays out of it."""
    keepouts.append((name, rect(x0, y0, x1, y1)))


def al_probe(px, py):
    """100 um Al pad, a 70 um opening in the cap, and a 100 um Au probe pad covering the Al pad."""
    other.append(rect(px - 50, py - 50, px + 50, py + 50, L_M1))
    au[f"probe {px:.0f},{py:.0f}"] = [rect(px - 50, py - 50, px + 50, py + 50)]
    vias.append(rect(px - 35, py - 35, px + 35, py + 35, L_VIA))


def snspd(x0, y0, lx, ly, w=WIRE_W, p=WIRE_P, turn="round", datatype=0):
    """One meander (gds/snspd_geom.py) with two Ti/Au probe pads to its left, under the cap (T4, T8, T9),
    plus the v4 local Al mirror under it and a mirror contact to its right."""
    polys, stab, gtab = meander(x0, y0, lx, ly, w, p, turn=turn, layer=L_NBN)
    for q in polys:
        q.datatype = datatype
    other.extend(polys)
    xp = x0 - lx / 2 - 280
    for tab, py in ((stab, 250), (gtab, -250)):
        other.extend(path([tab, (xp, tab[1]), (xp, y0 + py)], 4.0, L_LEAD))
        other.append(pad(xp, y0 + py, L_LEAD))
        vias.append(rect(xp - 55, y0 + py - 55, xp + 55, y0 + py + 55, L_VIA))
    # local Al mirror: 160 um left of the meander to 10 um past its right end; stops before the probe pads.
    # Its y extent follows the drawn NbN (+ 4 um), not the nominal ly: the sharp-turn control is taller than ly.
    ys = [pt[1] for q in polys for pt in q.points]
    other.append(rect(x0 - lx / 2 - 160, min(ys) - 4, x0 + lx / 2 + 10, max(ys) + 4, L_M1))
    # mirror contact: Al strip touching the mirror on the right, 70 um opening, 100 um Au pad (its own conductor)
    cx0, cx1 = x0 + lx / 2 + 10, x0 + lx / 2 + 110
    other.append(rect(cx0, y0 - 50, cx1, y0 + 50, L_M1))
    au[f"mirror {x0:.0f},{y0:.0f}"] = [rect(cx0, y0 - 50, cx1, y0 + 50)]
    vias.append(rect(cx0 + 15, y0 - 35, cx1 - 15, y0 + 35, L_VIA))
    keep(f"SNSPD {x0:.0f},{y0:.0f}", x0 - lx / 2 - 400, y0 - 370, x0 + lx / 2 + 120, y0 + 370)


def straights(x0, y0, widths, lx=30.0):
    """Two straight NbN wires (Ic references), each with its own two pads: one above y0, one below (T9)."""
    for w, s in zip(widths, (+1, -1)):
        polys, ltab, rtab = straight(x0, y0 + s * 40, lx, w, layer=L_NBN)
        other.extend(polys)
        for tab, xp in ((ltab, x0 - 200), (rtab, x0 + 200)):
            other.extend(path([tab, (xp, tab[1]), (xp, y0 + s * 250)], 4.0, L_LEAD))
            other.append(pad(xp, y0 + s * 250, L_LEAD))
            vias.append(rect(xp - 55, y0 + s * 250 - 55, xp + 55, y0 + s * 250 + 55, L_VIA))
    keep(f"straights {x0:.0f},{y0:.0f}", x0 - 300, y0 - 370, x0 + 300, y0 + 370)


def t1(x0, y0):
    fa = [pad(x0, y0), rect(x0 + 75, y0 - 10, x0 + 520, y0 + 10)]
    fb = [pad(x0 + 700, y0 + 250), rect(x0 + 80, y0 + 240, x0 + 625, y0 + 260)]
    for k in range(20):
        xf = x0 + 100 + k * 20
        # each finger runs 5 um into its own bar, so the merge never depends on two edges merely touching
        (fa if k % 2 == 0 else fb).append(rect(xf, y0 + (5 if k % 2 == 0 else 15), xf + 15, y0 + (235 if k % 2 == 0 else 245)))
    au["T1a"], au["T1b"] = fa, fb
    keep("T1", x0 - 120, y0 - 120, x0 + 820, y0 + 370)
    labels.append(("T1 Au comb 5um gap", x0, y0 - 170))


def t2v(x0=-2700.0, y0=400.0):
    """T2v: Au / SiO2 / Al capacitor through the v4 thin stack, where T2 was. Dielectric = 238 nm spacer + 160 nm
    cap = 0.398 um SiO2 (eps 3.9). Au top plate 200 um over the Al plate: C = eps0 * 3.9 * (200 um)^2 / 0.398 um
    = 3.5 pF (expected). Al tab to an Al pad; a 100 um opening in the cap lands the second Au pad on that Al pad."""
    xp = x0 + 300.0                                                         # -2400: Al pad and second probe
    other.append(rect(x0 - 120, y0 - 120, x0 + 120, y0 + 120, L_M1))       # Al plate 240 um
    other.append(rect(x0 + 120, y0 - 20, xp - 75, y0 + 20, L_M1))          # Al tab 40 um wide
    other.append(rect(xp - 75, y0 - 75, xp + 75, y0 + 75, L_M1))           # Al pad 150 um
    au["T2v top plate"] = [rect(x0 - 100, y0 - 100, x0 + 100, y0 + 100)]   # Au top plate 200 um: probe point 1
    au["T2v pad"] = [rect(xp - 75, y0 - 75, xp + 75, y0 + 75)]             # Au pad 150 um: probe point 2
    vias.append(rect(xp - 50, y0 - 50, xp + 50, y0 + 50, L_VIA))           # 100 um opening through the cap
    keep("T2v", x0 - 140, y0 - 140, xp + 100, y0 + 140)
    labels.append(("T2v Au/SiO2/Al cap", x0 - 120, y0 + 170))


def t3(x0, y0):
    other.append(rect(x0 - 100, y0 - 5, x0 + 100, y0 + 5, L_NBN))
    for xs, xp in ((-100, -300), (-40, -100), (40, 100), (100, 300)):
        other.append(rect(x0 + xs - 5, y0 - 5, x0 + xs + 5, y0 + 60, L_NBN))
        other.extend(path([(x0 + xs, y0 + 55), (x0 + xs, y0 + 120), (x0 + xp, y0 + 250), (x0 + xp, y0 + 330)], 6.0, L_LEAD))   # ends inside the pad
        other.append(pad(x0 + xp, y0 + 380, L_LEAD))
        vias.append(rect(x0 + xp - 55, y0 + 325, x0 + xp + 55, y0 + 435, L_VIA))
    keep("T3", x0 - 400, y0 - 60, x0 + 400, y0 + 480)
    labels.append(("T3 NbN 4-wire bar", x0 - 300, y0 - 120))


def t4(x0, y0, lx, name):
    snspd(x0, y0, lx, DET_WY)
    labels.append((f"{name} spare SNSPD {lx:.0f}x{DET_WY:.0f}", x0 - lx / 2 - 380, y0 - 450))


def t6(x0, y0):
    pts = [(x0 + 75, y0)]
    for k in range(8):
        xk = x0 + 150 + k * 60
        pts += [(xk, y0 + (0 if k % 2 == 0 else 500)), (xk, y0 + (500 if k % 2 == 0 else 0))]
    pts += [(x0 + 680, y0)]
    au["T6"] = path(pts, 6.0) + [pad(x0, y0), pad(x0 + 755, y0)]
    keep("T6", x0 - 100, y0 - 100, x0 + 855, y0 + 530)
    labels.append(("T6 Au continuity loop", x0 - 70, y0 - 140))


def t8(x0, y0, pitch=600.0):
    for k, f in enumerate(DOSE_FACTORS):
        xk = x0 + k * pitch
        snspd(xk, y0, DET_A30, DET_WY, datatype=k + 1)
        labels.append((f"D{k + 1} x{f:.2f}", xk - 120, y0 + 60))
    labels.append(("T8 EBL dose array (datatypes 1-7)", x0 - 380, y0 - 450))


def t9(x0, y0, spec):
    """T9 geometry array slot: ('m', w, p, turn, lx, ly) meander or ('s', w_top, w_bottom) straight pair."""
    if spec[0] == "m":
        _, w, p, turn, lx, ly = spec
        snspd(x0, y0, lx, ly, w, p, turn)
        labels.append((f"T9 {w * 1000:.0f}/{p * 1000:.0f} {turn} {lx:g}x{ly:g}", x0 - lx / 2 - 380, y0 - 450))
    else:
        straights(x0, y0, spec[1:])
        labels.append((f"T9 straight {spec[1] * 1000:.0f} / {spec[2] * 1000:.0f} nm", x0 - 280, y0 - 450))


def t10():
    """T10 mirror strip, four-point. Al strip 40 um wide at y = -100, running between the centres of the two end
    pads (current) at x = -4570 and -1920. Two voltage taps at y = -220, each joined to the strip by a 10 um Al
    stub at x = -4455 and -1945: 2510 um between the taps = the length of the trap's mirror ground path, so the
    four-point reading is that path's resistance (62.75 squares)."""
    other.append(rect(-4570, -120, -1920, -80, L_M1))
    for px, py in ((-4570, -100), (-1920, -100), (-4455, -220), (-1945, -220)):
        al_probe(px, py)
    for xs in (-4455, -1945):
        other.append(rect(xs - 5, -175, xs + 5, -110, L_M1))              # 10 um stub, tap pad up into the strip
    keep("T10", -4650, -280, -1840, -45)
    labels.append(("T10 Al mirror strip 4pt", -4650, 20))


def t11():
    """T11 Au-to-Al via chain: Au P1 - via 1 - Al A - via 2 - Au strap - via 3 - Al B - via 4 - Au P2, all at y = -100."""
    other.append(rect(1825, -175, 2225, -25, L_M1))                       # Al island A
    other.append(rect(2425, -175, 2825, -25, L_M1))                       # Al island B
    au["T11 P1"] = [rect(1700, -175, 1975, -25)]
    au["T11 strap"] = [rect(2075, -175, 2575, -25)]
    au["T11 P2"] = [rect(2675, -175, 2950, -25)]
    for xv in (1900, 2150, 2500, 2750):
        vias.append(rect(xv - 50, -150, xv + 50, -50, L_VIA))
    keep("T11", 1675, -200, 2975, 0)
    labels.append(("T11 Au-Al via chain x4", 1700, 40))


def t12():
    """T12 twin Au leads over an Al strip: strip y = -100, x = -1400 ... 900. Au lines at y = -95 and -105
    (5 um wide, 5 um apart) run past both strip ends and through their 100 um pads, so each line meets its pads
    over its full width. The two pads at each end are 5 um apart."""
    other.append(rect(-1400, -120, 900, -80, L_M1))
    au["T12 lead y-95"] = [rect(-1600, -97.5, 1100, -92.5), rect(-1600, -97.5, -1500, 2.5), rect(1000, -97.5, 1100, 2.5)]
    au["T12 lead y-105"] = [rect(-1600, -107.5, 1100, -102.5), rect(-1600, -202.5, -1500, -102.5),
                            rect(1000, -202.5, 1100, -102.5)]
    keep("T12", -1650, -215, 1150, 15)
    labels.append(("T12 twin Au leads over Al", -1500, 40))


# upper row (y ~ +400) and lower row (y ~ -650); T10-T12 sit in the free band (y -280 ... +80) at y = -100
t1(-4300, 350)
t6(3500, 300)
if not TRAP_ONLY:                                  # SNSPD and Al structures
    t2v()
    t3(-1000, 250)
    t4(600, 450, DET_A30, "T4")
    t4(2300, 450, DET_B60, "T4b")
    t8(-1000, -650)
    for x0, y0, spec in T9:
        t9(x0, y0, spec)
    t10()
    t11()
    t12()

for p in other:
    top.add(p)
els = [p for ps in au.values() for p in gdstk.boolean(ps, [], "or", layer=L_AU)]
for p in vias:
    top.add(p)

# alignment marks (kept from v3, same places): layer-1 marks always; the layer-40 cross and the layer-22 cross
# only on the full die (the trap-only process has no 22 or 40)
MARK_SITES = ((-1700.0, -CY + 170), (4300.0, -CY + 170), (-1700.0, CY - 170), (4300.0, CY - 170))
for xm, ym in MARK_SITES:
    top.add(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK), rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    if not TRAP_ONLY:
        top.add(rect(xm - 30, ym + 70, xm + 30, ym + 74, L_VIA), rect(xm - 2, ym + 60, xm + 2, ym + 84, L_VIA))
        top.add(rect(xm - 100, ym - 1, xm - 80, ym + 1, L_LEAD), rect(xm - 91, ym - 10, xm - 89, ym + 10, L_LEAD))

# Au ground fill: die inset by 100 um, minus 10 um around every Au conductor, minus the keep-out boxes and the
# mark keep-outs; keep the largest piece (any enclosed fill would float)
die = rect(-CX, -CY, CX, CY, L_CHIP)
mark_keep = [rect(xm - 160, ym - 140, xm + 160, ym + 140) for xm, ym in MARK_SITES]
keep_all = gdstk.boolean(gdstk.offset(els, 10, join="miter"), [q for _, q in keepouts] + mark_keep, "or")
ground = gdstk.boolean(gdstk.offset(die, -100), keep_all, "not", layer=L_AU)
ground = [max(ground, key=lambda q: q.area())]
for p in els + ground:
    p.layer = L_AU
    top.add(p)
top.add(die)

labels.append((CELL, -1300, 1150))
for txt, x, y in labels:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)

# ------------------------------------------------------------------ self-check
for i, (na, a) in enumerate(keepouts):
    for nb, b in keepouts[i + 1:]:
        if na != nb:
            both = gdstk.boolean([a], [b], "and")
            assert sum(q.area() for q in both) < 1e-6, f"keep-out boxes overlap: {na} / {nb}"
inset = (-CX + 150, -CY + 150, CX - 150, CY - 150)
for name, q in keepouts:
    (x0, y0), (x1, y1) = q.bounding_box()
    assert x0 >= inset[0] and y0 >= inset[1] and x1 <= inset[2] and y1 <= inset[3], f"keep-out outside die inset: {name}"
for L in (24, 30, 31, 45):
    assert not [p for p in top.polygons if p.layer == L], f"layer {L} must be empty"
if TRAP_ONLY:
    for L in (10, 20, 22, 40):
        assert not [p for p in top.polygons if p.layer == L], f"layer {L} must be empty in --trap-only"
print("SELF-CHECK PASS")


def preview(png):
    """Whole-die PNG, one colour per layer. Au is drawn translucent so the Al and NbN under it show."""
    style = [(L_AU, "#f2c200", 0.45, "Au (50)"), (L_M1, "#ff7f0e", 0.9, "Al (10)"),
             (L_LEAD, "#2ca02c", 0.9, "Ti/Au (22)"), (L_NBN, "#d62728", 0.9, "NbN (20)"),
             (L_VIA, "#000000", 1.0, "openings (40)"), (L_MARK, "#555555", 1.0, "marks (1)")]
    fig, ax = plt.subplots(figsize=(18, 5.6))
    for L, colour, alpha, _ in style:
        polys = [p.points for p in top.polygons if p.layer == L]
        ax.add_collection(PolyCollection(polys, facecolors=colour, edgecolors="none", alpha=alpha))
    for txt, x, y in labels:
        ax.text(x, y, txt, fontsize=7)
    ax.set(xlim=(-CX, CX), ylim=(-CY, CY), aspect="equal", xlabel="x (um)", ylabel="y (um)", title=CELL)
    ax.legend(handles=[Patch(color=c, alpha=a, label=n) for _, c, a, n in style], loc="upper right", fontsize=7)
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)


lib.write_gds(os.path.join(HERE, STEM + ".gds"))
preview(os.path.join(HERE, STEM + "_preview.png"))
print(f"wrote {STEM}.gds and {STEM}_preview.png")
