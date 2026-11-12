"""SNSPD-only die, snspd_die_v4, 10 x 10 mm (Claude-authored).

Eight copies of the A30 trap die's detector, with the same NbN meander, the same Ti/Au contact strips, the same
cap openings, the same Au leads and bond pads, and no trap electrodes. The Au ground fill stands in for the
centre DC over the NbN. Also: T3 (NbN four-wire bar, probe station), T11 (Au-to-Al via chain, probe station),
and four alignment-mark sites. Layer numbers as make_chip.py: 1 marks, 10 Al mirror, 20 NbN (datatype = dose),
22 Ti/Au contacts and crosses, 40 openings, 50 Au, 100 labels (not fabricated), 101 die outline (not fabricated).

Writes snspd_die_v4.gds, snspd_die_v4_pads.csv and snspd_die_v4_preview.png (after the self-check passes).
Run from design/sim:  ./run.sh ../gds/make_snspd_die.py
"""

import csv
import os

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from snspd_geom import meander  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ layers (same numbers as make_chip.py)
L_MARK, L_M1, L_NBN, L_LEAD, L_VIA, L_AU = 1, 10, 20, 22, 40, 50
L_NOTE, L_CHIP = 100, 101
CX, CY = 5000.0, 5000.0                 # die half size: die spans -5000 ... +5000
EDGE_AU = 100.0                         # Au fill keep-out from the die edge
GAP_FAR = 10.0                          # Au fill keep-out around leads and pads (outside the near boxes)
G_NEAR = 5.0                            # Au fill keep-out around leads inside a cell's near box
PAD_GAP = 30.0                          # Au fill keep-out around bond pads
PAD_Y_ROW = 4720.0                      # bond pad centres at y = +-4720
MARK_SITES = ((-4300.0, CY - 170), (4300.0, CY - 170), (-4300.0, -CY + 170), (4300.0, -CY + 170))

# Cells: name, xc, yc, direction (+1 = leads go to the top edge), layer-20 datatype, dose factor (label only)
CELLS = [
    ("D1", -2700.0, 1200.0, +1, 1, 0.80),
    ("D2", -900.0, 1200.0, +1, 2, 0.87),
    ("D3", 900.0, 1200.0, +1, 3, 0.93),
    ("D4", 2700.0, 1200.0, +1, 0, 1.00),
    ("D5", -2700.0, -1200.0, -1, 0, 1.00),
    ("D6", -900.0, -1200.0, -1, 5, 1.07),
    ("D7", 900.0, -1200.0, -1, 6, 1.13),
    ("D8", 2700.0, -1200.0, -1, 7, 1.20),
]

# ------------------------------------------------------------------ helpers
lib = gdstk.Library(unit=1e-6, precision=1e-9)
CELL_NAME = "SNSPD_DIE_V4"
top = lib.new_cell(CELL_NAME)


def rect(x0, y0, x1, y1, layer=L_AU):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def path(points, width, layer=L_AU):
    # same helper as make_chip.py: a wire of constant width along the points, as polygons
    return gdstk.FlexPath(points, width, layer=layer).to_polygons()


def union(polys, layer):
    # merge overlapping polygons into one set on the given layer
    return gdstk.boolean(polys, [], "or", layer=layer)


def area(polys):
    return sum(p.area() for p in polys)


# ------------------------------------------------------------------ what gets drawn
layers = {L_MARK: [], L_M1: [], L_NBN: [], L_LEAD: [], L_VIA: []}   # plain shapes by layer
AU = {}              # Au conductor name -> its polygons (lead + bond pad merged = one conductor)
AU_PADS = {}         # cell conductor -> bond pad
LEADS = {}           # cell conductor -> lead alone (for the 1 um inside-the-lead check)
TI_PADS = {}         # cell conductor -> Ti/Au pad under the contact (layer 22)
OPENINGS = {}        # cell conductor -> contact opening (layer 40)
PAD_CENTRE = {}      # cell conductor -> bond pad centre
PAD_ROLE = {}        # cell conductor -> text for the pads CSV
NBN = {}             # cell name -> NbN polygons (layer 20)
AL_CELL = {}         # cell name -> its Al mirror (layer 10)
VIAS = []            # mirror ground vias (layer 40), one per cell
WINDOWS = []         # 30 x 30 readout windows (holes in the Au)
LABELS = []          # (text, x, y), layer 100 only


def cell(name, xc, yc, direction, datatype):
    """One detector cell: NbN meander, two Ti/Au tabs with contact openings, two Au leads with bond pads,
    a readout window, an Al mirror strip with its ground via, and four e-beam crosses."""
    # NbN meander, exactly as on the A30 die. Its datatype selects the e-beam dose.
    nbn, sig_tab, ret_tab = meander(xc, yc, 36.0, 32.0, 0.130, 0.200, turn="round", layer=L_NBN)
    for p in nbn:
        p.datatype = datatype
    NBN[name] = nbn
    layers[L_NBN].extend(nbn)

    for tab, sy, end in ((sig_tab, +1, "S"), (ret_tab, -1, "G")):
        cond = f"{name}_{end}"
        # Ti/Au strip (layer 22) from the NbN tab towards the lead tip
        layers[L_LEAD].extend(path([tab, (tab[0] - 15.0, tab[1]), (tab[0] - 27.0, yc + 5.0 * sy),
                                    (xc - 97.0, yc + 5.0 * sy)], 4.0, L_LEAD))
        # Ti/Au pad under the contact (layer 22)
        tip_pad = rect(xc - 97.0, yc + sy * 1.5, xc - 70.0, yc + sy * 8.5, L_LEAD)
        layers[L_LEAD].append(tip_pad)
        TI_PADS[cond] = tip_pad
        # Contact opening in the SiO2 cap (layer 40), where the Au lead lands on the Ti/Au pad
        opening = rect(xc - 92.0, yc + sy * 3.5, xc - 74.0, yc + sy * 6.5, L_VIA)
        layers[L_VIA].append(opening)
        OPENINGS[cond] = opening
        # Au lead (layer 50) from the lead tip to its bond pad. Inner lead (sy == direction) turns at x = xc-400,
        # outer lead at x = xc-760, so the two leads of a cell do not cross.
        inner = (sy == direction)
        xp = xc - 400.0 if inner else xc - 760.0
        yp = direction * PAD_Y_ROW
        lead = path([(xc - 70.0, yc + 5.0 * sy), (xp, yc + 5.0 * sy), (xp, yp)], 5.0, L_AU)
        bond = rect(xp - 60.0, yp - 100.0, xp + 60.0, yp + 100.0, L_AU)
        LEADS[cond] = lead
        AU_PADS[cond] = bond
        PAD_CENTRE[cond] = (xp, yp)
        PAD_ROLE[cond] = (f"SNSPD {'signal' if end == 'S' else 'return'} lead, "
                          f"{'inner' if inner else 'outer'} lead, {'top' if direction > 0 else 'bottom'} die edge")
        AU[cond] = union(lead + [bond], L_AU)              # lead and pad are one conductor

    # readout window: 30 x 30 hole in the Au, centred on the cell
    WINDOWS.append(rect(xc - 15.0, yc - 15.0, xc + 15.0, yc + 15.0, L_AU))

    # Al mirror (layer 10): strip under the NbN, and a branch that carries the ground via
    AL_CELL[name] = union([rect(xc - 370.0, yc - 20.0, xc + 28.0, yc + 20.0, L_M1),
                           rect(xc - 370.0, yc - direction * 230.0, xc - 170.0, yc + direction * 20.0, L_M1)], L_M1)
    layers[L_M1].extend(AL_CELL[name])

    # mirror ground via (layer 40): 100 x 100, under the Au fill, enclosed by the Al branch
    via = rect(xc - 320.0, yc - direction * 130.0 - 50.0, xc - 220.0, yc - direction * 130.0 + 50.0, L_VIA)
    layers[L_VIA].append(via)
    VIAS.append(via)

    # four e-beam crosses (layer 22): a 20 x 2 bar and a 2 x 20 bar each
    for dx in (-300.0, 300.0):
        for dy in (-700.0, 700.0):
            x, y = xc + dx, yc + dy
            layers[L_LEAD].append(rect(x - 10.0, y - 1.0, x + 10.0, y + 1.0, L_LEAD))
            layers[L_LEAD].append(rect(x - 1.0, y - 10.0, x + 1.0, y + 10.0, L_LEAD))


def t3(x0, y0):
    """T3 NbN four-wire bar: the t3() drawing of make_test_die.py (probe pad P = 150), datatype 0."""
    layers[L_NBN].append(rect(x0 - 100, y0 - 5, x0 + 100, y0 + 5, L_NBN))
    for xs, xp in ((-100, -300), (-40, -100), (40, 100), (100, 300)):
        layers[L_NBN].append(rect(x0 + xs - 5, y0 - 5, x0 + xs + 5, y0 + 60, L_NBN))
        layers[L_LEAD].extend(path([(x0 + xs, y0 + 55), (x0 + xs, y0 + 120), (x0 + xp, y0 + 250),
                                    (x0 + xp, y0 + 330)], 6.0, L_LEAD))
        layers[L_LEAD].append(rect(x0 + xp - 75, y0 + 305, x0 + xp + 75, y0 + 455, L_LEAD))   # probe pad
        layers[L_VIA].append(rect(x0 + xp - 55, y0 + 325, x0 + xp + 55, y0 + 435, L_VIA))


def t11():
    """T11 Au-to-Al via chain: P1 - via - island A - via - strap - via - island B - via - P2 (spec coordinates)."""
    layers[L_M1].append(rect(-500, -75, -100, 75, L_M1))              # Al island A
    layers[L_M1].append(rect(100, -75, 500, 75, L_M1))                # Al island B
    AU["T11_P1"] = [rect(-625, -75, -350, 75, L_AU)]
    AU["T11_strap"] = [rect(-250, -75, 250, 75, L_AU)]
    AU["T11_P2"] = [rect(350, -75, 625, 75, L_AU)]
    for xv in (-425, -175, 175, 425):
        layers[L_VIA].append(rect(xv - 50, -50, xv + 50, 50, L_VIA))


# ------------------------------------------------------------------ build the die
for name, xc, yc, direction, datatype, dose in CELLS:
    cell(name, xc, yc, direction, datatype)
    LABELS.append((f"{name} x{dose:.2f}", xc - 380.0, yc + 110.0))

T3_X0, T3_Y0 = -3000.0, -250.0
t3(T3_X0, T3_Y0)
T3_KEEP = rect(-3400.0, -310.0, -2600.0, 230.0)          # no Au fill
LABELS.append(("T3", -3400.0, -330.0))

t11()
T11_KEEP = rect(-650.0, -100.0, 650.0, 100.0)            # no Au fill
LABELS.append(("T11", -650.0, 150.0))

# alignment marks: exactly make_chip.py's MARK_SITES loop with HAS_DET true
for xm, ym in MARK_SITES:
    s = 1 if ym > 0 else -1
    layers[L_MARK].append(rect(xm - 50, ym - 2, xm + 50, ym + 2, L_MARK))
    layers[L_MARK].append(rect(xm - 2, ym - 50, xm + 2, ym + 50, L_MARK))
    layers[L_VIA].append(rect(xm - 30, ym - s * 72, xm + 30, ym - s * 68, L_VIA))
    layers[L_VIA].append(rect(xm - 2, ym - s * 84, xm + 2, ym - s * 60, L_VIA))
    layers[L_NBN].append(rect(xm + 60, ym - 8, xm + 75, ym + 7, L_NBN))      # layer-20 overlay square, datatype 0
    layers[L_LEAD].append(rect(xm + 85, ym - 8, xm + 100, ym + 7, L_LEAD))   # layer-22 overlay square
    layers[L_LEAD].append(rect(xm - 100, ym - 1, xm - 80, ym + 1, L_LEAD))   # layer-22 cross
    layers[L_LEAD].append(rect(xm - 91, ym - 10, xm - 89, ym + 10, L_LEAD))
MARK_KEEP = [rect(xm - 160, ym - 140, xm + 180, ym + 140) for xm, ym in MARK_SITES]

# bond pads (16 signal pads, one per cell conductor) and the ground-pad labels
PAD_LIST = [AU_PADS[f"{n}_{e}"] for n, *_ in CELLS for e in ("S", "G")]
GND_PADS = [(-4700.0, 1500.0), (-4700.0, -1500.0), (4700.0, 1500.0), (4700.0, -1500.0)]
for x, y in GND_PADS:
    LABELS.append(("GND", x - 45.0, y - 15.0))
LABELS.append(("SNSPD_DIE_V4 10x10 mm", -4800.0, -4700.0))

# ------------------------------------------------------------------ Au ground fill (same construction as make_chip.py)
die = rect(-CX, -CY, CX, CY, L_CHIP)
# every Au conductor (cell leads with their pads, and the T11 pieces); the pads are inside their conductors
cond_polys = [p for ps in AU.values() for p in ps]
near_boxes = [rect(xc - 380.0, yc - 100.0, xc + 100.0, yc + 100.0) for _, xc, yc, *_ in CELLS]
near = union(near_boxes, L_AU)

keep = gdstk.boolean(gdstk.offset(cond_polys, GAP_FAR, join="miter"), near, "not")
keep = gdstk.boolean(keep, gdstk.boolean(gdstk.offset(cond_polys, G_NEAR, join="miter"), near, "and"), "or")
keep = gdstk.boolean(keep, gdstk.offset(PAD_LIST, PAD_GAP, join="miter"), "or")
keep = gdstk.boolean(keep, WINDOWS + MARK_KEEP + [T3_KEEP, T11_KEEP], "or")
fill = gdstk.boolean(gdstk.offset(die, -EDGE_AU, join="miter"), keep, "not", layer=L_AU)
fill.sort(key=lambda p: p.area(), reverse=True)
dropped = area(fill[1:])
assert dropped < 1e-6, f"Au fill is not one piece: {len(fill)} pieces, dropped area {dropped:.3f} um^2"
FILL = [fill[0]]

# ------------------------------------------------------------------ assemble the top cell
for L, polys in layers.items():
    for p in polys:
        top.add(p)
for ps in AU.values():
    for p in ps:
        top.add(p)
for p in FILL:
    top.add(p)
top.add(die)
for txt, x, y in LABELS:
    for p in gdstk.text(txt, 30, (x, y), layer=L_NOTE):
        top.add(p)

# ------------------------------------------------------------------ self-check
print("running self-check ...")

# 1. retired layers stay empty
for L in (24, 30, 31, 45):
    assert not [p for p in top.polygons if p.layer == L], f"layer {L} must be empty"

# 2. layers 10, 22, 40, 50 stay >= 90 um from the die edge (all coordinates within +-4910)
for p in top.polygons:
    if p.layer in (L_M1, L_LEAD, L_VIA, L_AU):
        for x, y in p.points:
            assert abs(x) <= CX - 90 and abs(y) <= CY - 90, f"layer {p.layer} within 90 um of the die edge at ({x:.1f}, {y:.1f})"

# 3. the Au fill is one piece (asserted above when it was built; here the kept piece is checked)
assert len(FILL) == 1

# 4. 16 lead conductors, each containing exactly one bond pad (its own)
CELL_CONDS = [f"{n}_{e}" for n, *_ in CELLS for e in ("S", "G")]
assert len(CELL_CONDS) == 16
for c in CELL_CONDS:
    inside = [q for q in CELL_CONDS if area(gdstk.boolean(AU_PADS[q], AU[c], "not")) < 1e-6]
    assert inside == [c], f"conductor {c} contains pads {inside}"

# 5. every contact opening is inside its lead and inside its Ti/Au pad, by at least 1 um
for c in CELL_CONDS:
    grown = gdstk.offset([OPENINGS[c]], 1.0, join="miter")
    assert area(gdstk.boolean(grown, LEADS[c], "not")) < 1e-6, f"opening {c} not 1 um inside its lead"
    assert area(gdstk.boolean(grown, [TI_PADS[c]], "not")) < 1e-6, f"opening {c} not 1 um inside its Ti/Au pad"

# 6. every mirror ground via is enclosed by 25 um in both the Au fill and the Al
AL_ALL = [p for ps in AL_CELL.values() for p in ps]
for v in VIAS:
    grown = gdstk.offset([v], 25.0, join="round")
    assert area(gdstk.boolean(grown, FILL, "not")) < 1e-6, "mirror via not enclosed by 25 um in the Au fill"
    assert area(gdstk.boolean(grown, AL_ALL, "not")) < 1e-6, "mirror via not enclosed by 25 um in the Al"

# 7. each cell's NbN lies under Au or inside its window
AU_UNION = union([p for ps in AU.values() for p in ps] + FILL, L_AU)
for n in NBN:
    nbn_u = union(NBN[n], L_NBN)
    bare = gdstk.boolean(nbn_u, AU_UNION + WINDOWS, "not")
    assert area(bare) < 1e-6, f"cell {n}: NbN not under Au or window ({area(bare):.4f} um^2)"

# 8. the Al covers each cell's NbN grown by 3 um
for n in NBN:
    grown = gdstk.offset(union(NBN[n], L_NBN), 3.0, join="round")
    assert area(gdstk.boolean(grown, AL_CELL[n], "not")) < 1e-6, f"cell {n}: Al does not cover NbN by 3 um"

# 9. no keep-out boxes overlap (windows, mark keep-outs, T3, T11)
BOXES = [("window", w) for w in WINDOWS] + [("mark", m) for m in MARK_KEEP] + [("T3", T3_KEEP), ("T11", T11_KEEP)]
for i, (na, a) in enumerate(BOXES):
    for nb, b in BOXES[i + 1:]:
        assert area(gdstk.boolean([a], [b], "and")) < 1e-6, f"keep-out boxes overlap: {na} / {nb}"

# 10. Au conductors are >= 5 um from each other (the cell leads, pads and T11 pieces)
ORDER = list(AU.keys())
GROWN = {k: gdstk.offset(AU[k], 4.999, join="miter") for k in ORDER}
for i, a in enumerate(ORDER):
    for b in ORDER[i + 1:]:
        assert area(gdstk.boolean(GROWN[a], AU[b], "and")) < 1e-6, f"Au conductors {a} and {b} closer than 5 um"

# 11. the fill is >= 30 um from every bond pad
for pad in PAD_LIST:
    assert area(gdstk.boolean(gdstk.offset([pad], PAD_GAP - 0.001, join="miter"), FILL, "and")) < 1e-6, \
        "Au fill closer than 30 um to a bond pad"

# 12. NbN |y - yc| <= 17 for every cell
for name, xc, yc, *_ in CELLS:
    ymax = max(abs(y - yc) for p in NBN[name] for _, y in p.points)
    assert ymax <= 17.0, f"cell {name}: NbN {ymax:.2f} um from its centre line"

# 13. comparison with the released A30 die (read only): the detector of D4 against A30's detector at (240, 0)
A30_PATH = os.path.join(HERE, "trap_die_v4_A30.gds")
assert os.path.exists(A30_PATH), "trap_die_v4_A30.gds not found"
a30 = gdstk.read_gds(A30_PATH).top_level()[0]


def region(polys, box, dx=0.0, dy=0.0):
    # the polygons of one layer clipped to a box, optionally translated
    clip = [gdstk.rectangle((box[0], box[1]), (box[2], box[3]))]
    out = gdstk.boolean(polys, clip, "and")
    for p in out:
        p.translate(dx, dy)
    return out


A30_BOX_WIDE = (140.0, -20.0, 300.0, 20.0)     # layers 20, 22, 40
A30_BOX_LEAD = (140.0, -20.0, 280.0, 20.0)     # layer 50
D4 = [c for c in CELLS if c[0] == "D4"][0]
DX, DY = D4[1] - 240.0, D4[2]                  # translation from the A30 detector (240, 0) to D4
D4_BOX_WIDE = (A30_BOX_WIDE[0] + DX, A30_BOX_WIDE[1] + DY, A30_BOX_WIDE[2] + DX, A30_BOX_WIDE[3] + DY)
D4_BOX_LEAD = (A30_BOX_LEAD[0] + DX, A30_BOX_LEAD[1] + DY, A30_BOX_LEAD[2] + DX, A30_BOX_LEAD[3] + DY)
COMPARE = {}
for L, abox, dbox in ((20, A30_BOX_WIDE, D4_BOX_WIDE), (22, A30_BOX_WIDE, D4_BOX_WIDE),
                      (40, A30_BOX_WIDE, D4_BOX_WIDE), (50, A30_BOX_LEAD, D4_BOX_LEAD)):
    ref = region([p for p in a30.polygons if p.layer == L], abox, DX, DY)
    mine = region([p for p in top.polygons if p.layer == L], dbox)
    COMPARE[L] = area(gdstk.boolean(ref, mine, "xor"))
    assert COMPARE[L] < 0.01, f"layer {L}: D4 differs from the A30 detector by {COMPARE[L]:.4f} um^2"

print("SELF-CHECK PASS")
print("A30 comparison, area of the XOR per layer (um^2, limit 0.01):")
for L in (20, 22, 40, 50):
    print(f"  layer {L}: {COMPARE[L]:.6f}")

# ------------------------------------------------------------------ outputs
lib.write_gds(os.path.join(HERE, "snspd_die_v4.gds"))

with open(os.path.join(HERE, "snspd_die_v4_pads.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["pad", "electrode", "role", "x_um", "y_um", "layer"])
    for c in CELL_CONDS:
        x, y = PAD_CENTRE[c]
        w.writerow([c, c, PAD_ROLE[c], f"{x:.0f}", f"{y:.0f}", L_AU])
    for k, (x, y) in enumerate(GND_PADS):
        w.writerow([f"GND-{k + 1}", "ground fill", "Au ground fill: bond to carrier ground", f"{x:.0f}", f"{y:.0f}", L_AU])

style = [(L_M1, "#ff7f0e", 0.9, "Al (10)"), (L_NBN, "#d62728", 0.9, "NbN (20)"),
         (L_LEAD, "#2ca02c", 0.9, "Ti/Au (22)"), (L_VIA, "#000000", 1.0, "openings (40)"),
         (L_AU, "#f2c200", 0.45, "Au (50)"), (L_MARK, "#555555", 1.0, "marks (1)")]


def draw(ax, xlim, ylim, title):
    for L, colour, alpha, _ in style:
        polys = [p.points for p in top.polygons if p.layer == L]
        ax.add_collection(PolyCollection(polys, facecolors=colour, edgecolors="none", alpha=alpha))
    ax.set(xlim=xlim, ylim=ylim, aspect="equal", title=title, xlabel="x (um)", ylabel="y (um)")


# three panels: whole die (left), one cell with its leads (top right), detector zoom (bottom right)
fig = plt.figure(figsize=(22, 13))
gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 1.0])
ax_die = fig.add_subplot(gs[:, 0])
ax_cell = fig.add_subplot(gs[0, 1])
ax_det = fig.add_subplot(gs[1, 1])
draw(ax_die, (-CX, CX), (-CY, CY), CELL_NAME)
for txt, x, y in LABELS:
    if txt.startswith("D") or txt in ("T3", "T11"):
        ax_die.text(x, y, txt, fontsize=7)
ax_die.legend(handles=[Patch(color=c, alpha=a, label=n) for _, c, a, n in style], loc="upper right", fontsize=8)
D2 = [c for c in CELLS if c[0] == "D2"][0]
draw(ax_cell, (D2[1] - 900, D2[1] + 900), (D2[2] - 900, D2[2] + 900), "D2 cell, +-900 um")
D4_CELL = [c for c in CELLS if c[0] == "D4"][0]
draw(ax_det, (D4_CELL[1] - 130, D4_CELL[1] + 60), (D4_CELL[2] - 45, D4_CELL[2] + 45),
     "D4 detector zoom (window = gap in Au)")
fig.savefig(os.path.join(HERE, "snspd_die_v4_preview.png"), dpi=110, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------ summary
au_total = area([p for p in top.polygons if p.layer == L_AU])
nbn_total = area([p for p in top.polygons if p.layer == L_NBN])
print(f"Au (layer 50) total area: {au_total:.1f} um^2 = {au_total * 1e-8:.5f} cm^2")
print(f"layer 20 total area: {nbn_total:.3f} um^2")
counts = {}
for p in top.polygons:
    counts[p.layer] = counts.get(p.layer, 0) + 1
print("polygons per layer:", ", ".join(f"{L}: {counts[L]}" for L in sorted(counts)))
print("wrote snspd_die_v4.gds, snspd_die_v4_pads.csv, snspd_die_v4_preview.png")
