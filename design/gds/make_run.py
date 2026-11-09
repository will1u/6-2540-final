"""Small R&D run layouts for MIT.nano (Claude-authored; DESIGN_LOG step 15).

Each run processes a full 100 mm wafer but writes only a small block of dies at the wafer centre, so
spin coating, PECVD and plating behave as on a full wafer while MLA/EBL write time stays short.
Trap dies are v4 (local mirror, 10 x 10 mm; DESIGN_LOG step 25); test dies are still v3 (10 x 2.5 mm,
baseline die-wide Al + D2 test structures, not yet reworked for v4). Each column stacks its dies with
200 um streets, using each die's own height (from its cell outline), as in wafer_v4.gds.
The die long axis runs along wafer x; align wafer x to the primary flat so the streets follow the
Si <110> cleave directions [verify the orientation the MLA and the saw expect].

A run is a list of columns, each a list of die types from bottom to top:
    A30 / B60  trap die with the 30 x 30 / 60 x 30 um SNSPD     (make_chip.py, --det60)
    NODET      plain trap die, no SNSPD, no Al                    (make_chip.py --nodet)
    TEST       test-structure die, incl. the T8 EBL dose array    (make_test_die.py)
    TEST_TRAP  test die for trap-only runs: T1, T2, T6 only       (make_test_die.py --trap-only)

Presets (edit RUNS to make another):
    R1_TRAP  staged run 1 (SIMPLIFICATIONS.md S2): trap process only (v4: Au on SiO2 over HR Si, no Al)
    R1_FULL  full stack: 2 A30 + 2 B60 + 2 NODET + 2 test dies

Writes run_<name>.gds (top cell RUN_<NAME>), run_<name>_map.csv and run_<name>_map.png, and prints
the die count and layer-20 (EBL) area. Re-run make_chip.py (A30, --det60, --nodet) and make_test_die.py
first so the die cells are current.
Run from design/sim:  ./run.sh ../gds/make_run.py [R1_TRAP | R1_FULL]   (no argument: all presets)
"""

import csv
import os
import sys

import gdstk
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R_WAFER = 50000.0
DIE_X, STREET = 10000.0, 200.0         # every die is 10 mm wide; heights differ (read from the cells)
PX = DIE_X + STREET
SOURCES = {"A30": ("trap_die_v4_A30.gds", "TRAP_DIE_V4_A30"), "B60": ("trap_die_v4_B60.gds", "TRAP_DIE_V4_B60"),
           "NODET": ("trap_die_v4_NODET.gds", "TRAP_DIE_V4_NODET"), "TEST": ("test_die_v3.gds", "TEST_DIE_V3"),
           "TEST_TRAP": ("test_die_v3_TRAP.gds", "TEST_DIE_V3_TRAP")}
RUNS = {
    "R1_TRAP": [["NODET", "TEST_TRAP", "NODET", "NODET"], ["NODET", "TEST_TRAP", "NODET", "NODET"]],
    "R1_FULL": [["A30", "TEST", "B60", "NODET"], ["NODET", "TEST", "A30", "B60"]],
}
COLORS = {"A30": "#d4a017", "B60": "#2a6fb0", "NODET": "#7f8c8d", "TEST": "#8e44ad", "TEST_TRAP": "#b07cc6"}

names = [a for a in sys.argv[1:] if a in RUNS] or list(RUNS)
for name in names:
    cols = RUNS[name]
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    cells, l20, hgt = {}, {}, {}
    for kind in {k for col in cols for k in col}:
        fname, cname = SOURCES[kind]
        c = {cc.name: cc for cc in gdstk.read_gds(os.path.join(HERE, fname)).cells}[cname]
        lib.add(c)
        cells[kind] = c
        l20[kind] = sum(p.area() for p in c.get_polygons() if p.layer == 20)
        (x0, y0), (x1, y1) = c.bounding_box()
        hgt[kind] = y1 - y0
    run = lib.new_cell(f"RUN_{name}")
    run.add(gdstk.ellipse((0, 0), R_WAFER, layer=101, tolerance=5))      # wafer outline (not written)
    rows, n = [], 0
    col_h = [sum(hgt[k] for k in col) + STREET * (len(col) - 1) for col in cols]
    # the saw cuts straight across the wafer, so every column must stack the same die heights
    assert len({tuple(round(hgt[k]) for k in col) for col in cols}) == 1, f"{name}: columns differ in die heights"
    for i, col in enumerate(cols):
        xc = (i - (len(cols) - 1) / 2) * PX
        yb = -col_h[i] / 2                       # bottom edge of the column, centred on the wafer
        for j, kind in enumerate(col):
            yc = yb + hgt[kind] / 2
            yb += hgt[kind] + STREET
            run.add(gdstk.Reference(cells[kind], (xc, yc)))
            n += 1
            rows.append((f"{name}-{n:02d}", kind, xc, yc, j, i))
    for p in gdstk.text(f"RUN_{name} Ba+ trap", 800, (-6000, -max(col_h) / 2 - 3000), layer=100):
        run.add(p)
    lib.write_gds(os.path.join(HERE, f"run_{name}.gds"))
    with open(os.path.join(HERE, f"run_{name}_map.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["die", "type", "x_centre_um", "y_centre_um", "row", "col"])
        w.writerows(rows)

    counts = {k: sum(1 for r in rows if r[1] == k) for k in SOURCES if any(r[1] == k for r in rows)}
    ebl = sum(l20[r[1]] for r in rows)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.add_patch(plt.Circle((0, 0), R_WAFER / 1000, fill=False))
    for d, kind, xc, yc, *_ in rows:
        ax.add_patch(plt.Rectangle(((xc - DIE_X / 2) / 1000, (yc - hgt[kind] / 2) / 1000), DIE_X / 1000, hgt[kind] / 1000,
                                   color=COLORS[kind], alpha=0.8))
        ax.text(xc / 1000, yc / 1000, f"{d}\n{kind}", ha="center", va="center", fontsize=6)
    ax.set(xlim=(-52, 52), ylim=(-52, 52), aspect="equal", xlabel="mm", ylabel="mm",
           title=f"run_{name}: " + ", ".join(f"{k} x{v}" for k, v in counts.items()))
    fig.savefig(os.path.join(HERE, f"run_{name}_map.png"), dpi=120)
    plt.close(fig)
    has_det = "A30" in counts or "B60" in counts
    print(f"wrote run_{name}.gds: {n} dies {counts}; block {(len(cols) * PX - STREET) / 1000:.1f} x "
          f"{max(col_h) / 1000:.1f} mm; layer-20 (EBL) area {ebl / 1e6:.4f} mm^2"
          + ("" if ebl or has_det else " (trap-only run: no EBL, no layer 20-22 jobs)"))
