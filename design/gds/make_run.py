"""Small R&D run layouts for MIT.nano (Claude-authored; DESIGN_LOG step 15).

Each run processes a full 100 mm wafer but writes only a small block of dies at the wafer centre, so
spin coating, PECVD and plating behave as on a full wafer while MLA/EBL write time stays short.
The block uses the same 10 x 2.5 mm dies and the same 10.2 x 2.7 mm pitch as wafer_v2.gds.
The die long axis runs along wafer x; align wafer x to the primary flat so the streets follow the
Si <110> cleave directions [verify the orientation the MLA and the saw expect].

A run is a list of columns, each a list of die types from bottom to top:
    A30 / B60  trap die with the 30 x 30 / 60 x 30 um SNSPD     (make_chip.py, --det60)
    NODET      plain trap die, no SNSPD                           (make_chip.py --nodet)
    TEST       test-structure die, incl. the T8 EBL dose array    (make_test_die.py)
    TEST_TRAP  test die for trap-only runs: T1, T2, T6 only       (make_test_die.py --trap-only)

Presets (edit RUNS to make another):
    R1_TRAP  staged run 1 (SIMPLIFICATIONS.md S2): trap process only, traveler steps 4-8b and 10 skipped
    R1_FULL  full stack, one of each trap variant per column plus a test die

Writes run_<name>.gds (top cell RUN_<NAME>), run_<name>_map.csv and run_<name>_map.png, and prints
the die count and layer-20 (EBL) area. Re-run make_chip.py (all three variants) and make_test_die.py
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
DIE_X, DIE_Y, STREET = 10000.0, 2500.0, 200.0
PX, PY = DIE_X + STREET, DIE_Y + STREET
SOURCES = {"A30": ("trap_die_v2_A30.gds", "TRAP_DIE_V2_A30"), "B60": ("trap_die_v2_B60.gds", "TRAP_DIE_V2_B60"),
           "NODET": ("trap_die_v2_NODET.gds", "TRAP_DIE_V2_NODET"), "TEST": ("test_die_v2.gds", "TEST_DIE_V2"),
           "TEST_TRAP": ("test_die_v2_TRAP.gds", "TEST_DIE_V2_TRAP")}
RUNS = {
    "R1_TRAP": [["NODET", "TEST_TRAP", "NODET", "NODET"], ["NODET", "NODET", "TEST_TRAP", "NODET"]],
    "R1_FULL": [["A30", "TEST", "B60", "NODET"], ["NODET", "B60", "TEST", "A30"]],
}
COLORS = {"A30": "#d4a017", "B60": "#2a6fb0", "NODET": "#7f8c8d", "TEST": "#8e44ad", "TEST_TRAP": "#b07cc6"}

names = [a for a in sys.argv[1:] if a in RUNS] or list(RUNS)
for name in names:
    cols = RUNS[name]
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    cells, l20 = {}, {}
    for kind in {k for col in cols for k in col}:
        fname, cname = SOURCES[kind]
        c = {cc.name: cc for cc in gdstk.read_gds(os.path.join(HERE, fname)).cells}[cname]
        lib.add(c)
        cells[kind] = c
        l20[kind] = sum(p.area() for p in c.get_polygons() if p.layer == 20)
    run = lib.new_cell(f"RUN_{name}")
    run.add(gdstk.ellipse((0, 0), R_WAFER, layer=101, tolerance=5))      # wafer outline (not written)
    rows, n = [], 0
    for i, col in enumerate(cols):
        xc = (i - (len(cols) - 1) / 2) * PX
        for j, kind in enumerate(col):
            yc = (j - (len(col) - 1) / 2) * PY
            run.add(gdstk.Reference(cells[kind], (xc, yc)))
            n += 1
            rows.append((f"{name}-{n:02d}", kind, xc, yc, j, i))
    for p in gdstk.text(f"RUN_{name} Ba+ trap", 800, (-6000, -len(cols[0]) * PY / 2 - 3000), layer=100):
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
        ax.add_patch(plt.Rectangle(((xc - DIE_X / 2) / 1000, (yc - DIE_Y / 2) / 1000), DIE_X / 1000, DIE_Y / 1000,
                                   color=COLORS[kind], alpha=0.8))
        ax.text(xc / 1000, yc / 1000, f"{d}\n{kind}", ha="center", va="center", fontsize=6)
    ax.set(xlim=(-52, 52), ylim=(-52, 52), aspect="equal", xlabel="mm", ylabel="mm",
           title=f"run_{name}: " + ", ".join(f"{k} x{v}" for k, v in counts.items()))
    fig.savefig(os.path.join(HERE, f"run_{name}_map.png"), dpi=120)
    plt.close(fig)
    has_det = "A30" in counts or "B60" in counts
    print(f"wrote run_{name}.gds: {n} dies {counts}; block {len(cols) * PX / 1000:.1f} x "
          f"{len(cols[0]) * PY / 1000:.1f} mm; layer-20 (EBL) area {ebl / 1e6:.4f} mm^2"
          + ("" if ebl or has_det else " (trap-only run: no EBL, no layer 20-31 jobs)"))
