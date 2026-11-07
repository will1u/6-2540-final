"""Wafer layout for MLA150 / EBL jobs (Claude-authored; traveler item A7).

A 10 x 10.8 mm "tile" stacks four 10 x 2.5 mm dies with 200 um dicing streets:
    A30 trap die / B60 trap die / A30 trap die / test die
(the 1 cm^2 footprint William first asked for now holds two A30, one B60 and one test die).
Tiles are arrayed on a 100 mm wafer and kept inside a 45 mm radius (5 mm edge exclusion).
Die cells are imported from trap_die_v2_A30.gds, trap_die_v2_B60.gds and test_die_v2.gds, so
re-running make_chip.py / make_test_die.py and then this script updates the wafer.

Writes wafer_v2.gds (top cell WAFER_V2), wafer_v2_map.csv (die id, type, centre), wafer_v2_map.png.
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
DIE_X, DIE_Y, STREET = 10000.0, 2500.0, 200.0
PX, PY = DIE_X + STREET, DIE_Y + STREET  # die pitch
TILE = ["A30", "B60", "A30", "TEST"]     # bottom to top within a tile
SOURCES = {"A30": ("trap_die_v2_A30.gds", "TRAP_DIE_V2_A30"), "B60": ("trap_die_v2_B60.gds", "TRAP_DIE_V2_B60"),
           "TEST": ("test_die_v2.gds", "TEST_DIE_V2")}

lib = gdstk.Library(unit=1e-6, precision=1e-9)
cells = {}
for kind, (fname, cname) in SOURCES.items():
    src = gdstk.read_gds(os.path.join(HERE, fname))
    c = {cc.name: cc for cc in src.cells}[cname]
    lib.add(c)
    cells[kind] = c
wafer = lib.new_cell("WAFER_V2")
wafer.add(gdstk.ellipse((0, 0), R_WAFER, layer=101, tolerance=5))           # outline (not written)
rows, n = [], 0
ny = int(2 * R_USE // PY) + 2
nx = int(2 * R_USE // PX) + 2
for j in range(-ny // 2, ny // 2 + 1):
    for i in range(-nx // 2, nx // 2 + 1):
        xc, yc = i * PX, j * PY + PY / 2
        corners = [(xc + sx * DIE_X / 2, yc + sy * DIE_Y / 2) for sx in (-1, 1) for sy in (-1, 1)]
        if all(x * x + y * y <= R_USE ** 2 for x, y in corners):
            kind = TILE[j % len(TILE)]
            wafer.add(gdstk.Reference(cells[kind], (xc, yc)))
            n += 1
            rows.append((f"D{n:03d}", kind, xc, yc, j, i))
for p in gdstk.text("WAFER_V2 Ba+ SNSPD trap", 800, (-15000, -48000), layer=100):
    wafer.add(p)
lib.write_gds(os.path.join(HERE, "wafer_v2.gds"))
with open(os.path.join(HERE, "wafer_v2_map.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["die", "type", "x_centre_um", "y_centre_um", "row", "col"])
    w.writerows(rows)
counts = {k: sum(1 for r in rows if r[1] == k) for k in TILE}
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_patch(plt.Circle((0, 0), R_WAFER / 1000, fill=False))
ax.add_patch(plt.Circle((0, 0), R_USE / 1000, fill=False, ls="--", color="0.6"))
colors = {"A30": "#d4a017", "B60": "#2a6fb0", "TEST": "#8e44ad"}
for d, kind, xc, yc, *_ in rows:
    ax.add_patch(plt.Rectangle(((xc - DIE_X / 2) / 1000, (yc - DIE_Y / 2) / 1000), DIE_X / 1000, DIE_Y / 1000,
                               color=colors[kind], alpha=0.7))
ax.set(xlim=(-52, 52), ylim=(-52, 52), aspect="equal", xlabel="mm", ylabel="mm",
       title="wafer_v2: " + ", ".join(f"{k} x{v}" for k, v in counts.items()))
fig.savefig(os.path.join(HERE, "wafer_v2_map.png"), dpi=120)
print(f"wrote wafer_v2.gds: {n} dies ({counts})")
