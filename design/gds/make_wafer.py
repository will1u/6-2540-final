"""Wafer layout for MLA150 / EBL jobs (Claude-authored; traveler item A7; DESIGN_LOG steps 18, 25).

v4 trap dies (local mirror) are 10 x 10 mm and the test die (still v3) is 10 x 2.5 mm. Each wafer column
repeats the tile
    A30 trap die / B60 trap die / A30 trap die / test die      (bottom to top)
with 200 um dicing streets, each die stacked at its own height (read from its cell outline). Dies are
kept inside a 45 mm radius (5 mm edge exclusion). Die cells are imported from trap_die_v4_A30.gds,
trap_die_v4_B60.gds and test_die_v3.gds, so re-running make_chip.py / make_test_die.py and then this
script updates the wafer.

Writes wafer_v4.gds (top cell WAFER_V4), wafer_v4_map.csv (die id, type, centre), wafer_v4_map.png.
Run from design/sim:  ./run.sh ../gds/make_wafer.py
"""

import csv
import os

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R_WAFER, R_USE = 50000.0, 45000.0       # um
DIE_X, STREET = 10000.0, 200.0
PX = DIE_X + STREET                      # column pitch
TILE = ["A30", "B60", "A30", "TEST"]     # bottom to top within a tile
SOURCES = {"A30": ("trap_die_v4_A30.gds", "TRAP_DIE_V4_A30"), "B60": ("trap_die_v4_B60.gds", "TRAP_DIE_V4_B60"),
           "TEST": ("test_die_v3.gds", "TEST_DIE_V3")}

lib = gdstk.Library(unit=1e-6, precision=1e-9)
cells, hgt = {}, {}
for kind, (fname, cname) in SOURCES.items():
    src = gdstk.read_gds(os.path.join(HERE, fname))
    c = {cc.name: cc for cc in src.cells}[cname]
    lib.add(c)
    cells[kind] = c
    (x0, y0), (x1, y1) = c.bounding_box()
    hgt[kind] = y1 - y0
wafer = lib.new_cell("WAFER_V4")
wafer.add(gdstk.ellipse((0, 0), R_WAFER, layer=101, tolerance=5))           # outline (not written)
tile_h = sum(hgt[k] for k in TILE) + STREET * len(TILE)
rows, n = [], 0
nx = int(2 * R_USE // PX) + 2
for i in range(-nx // 2, nx // 2 + 1):
    xc = i * PX
    yb = -2 * tile_h                       # start well below the wafer and stack upwards
    j = 0
    while yb < R_USE:
        kind = TILE[j % len(TILE)]
        yc = yb + hgt[kind] / 2
        corners = [(xc + sx * DIE_X / 2, yc + sy * hgt[kind] / 2) for sx in (-1, 1) for sy in (-1, 1)]
        if all(x * x + y * y <= R_USE ** 2 for x, y in corners):
            wafer.add(gdstk.Reference(cells[kind], (xc, yc)))
            n += 1
            rows.append((f"D{n:03d}", kind, xc, yc, j, i))
        yb += hgt[kind] + STREET
        j += 1
for p in gdstk.text("WAFER_V3 Ba+ SNSPD trap", 800, (-15000, -48000), layer=100):
    wafer.add(p)
lib.write_gds(os.path.join(HERE, "wafer_v4.gds"))
with open(os.path.join(HERE, "wafer_v4_map.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["die", "type", "x_centre_um", "y_centre_um", "row", "col"])
    w.writerows(rows)
counts = {k: sum(1 for r in rows if r[1] == k) for k in SOURCES}
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_patch(plt.Circle((0, 0), R_WAFER / 1000, fill=False))
ax.add_patch(plt.Circle((0, 0), R_USE / 1000, fill=False, ls="--", color="0.6"))
colors = {"A30": "#d4a017", "B60": "#2a6fb0", "TEST": "#8e44ad"}
for d, kind, xc, yc, *_ in rows:
    ax.add_patch(plt.Rectangle(((xc - DIE_X / 2) / 1000, (yc - hgt[kind] / 2) / 1000), DIE_X / 1000, hgt[kind] / 1000,
                               color=colors[kind], alpha=0.7))
ax.set(xlim=(-52, 52), ylim=(-52, 52), aspect="equal", xlabel="mm", ylabel="mm",
       title="wafer_v4: " + ", ".join(f"{k} x{v}" for k, v in counts.items()))
fig.savefig(os.path.join(HERE, "wafer_v4_map.png"), dpi=120)
print(f"wrote wafer_v4.gds: {n} dies ({counts})")
