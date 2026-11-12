"""Checks a wafer-run layout (Claude-authored).

Usage (from design/sim):  ./run.sh ../gds/check_run.py [R1_ONE]      (default R1_ONE; also works on R1_FULL)
Reads run_<name>.gds, run_<name>_map.csv and the die GDS files on disk. Read-only.

The die types and their cell names are copied here on purpose, so this checker does not import make_run.py.
Units um. Every check prints one PASS or FAIL line; indented lines under a FAIL give the offending items.
R7 prints INFO lines (not pass/fail). Exit code 1 if any check fails.

  R1  top cell is RUN_<NAME>; its references match the map CSV one to one (origin and cell name); no rotation or mirror
  R2  counts per die type (EXPECT dict, keyed by run name; skipped with a note for other runs)
  R3  die size (10000 x 10000; 2500 tall is also allowed when the run holds test dies); no overlap; neighbours
      10 mm apart by a 200 um street; for a run of one die size, centres on a grid of pitch 10200 um
  R4  every die corner within 45 mm of the wafer centre
  R5  freshness: for each die type, the cell in the run equals the die file on disk (merged area and polygon count
      on layers 1, 10, 20, 22, 40, 50)
  R6  layers 24, 30, 31, 45 empty in the flattened run; no text labels on layers 1, 10, 20, 22, 40, 50
  R7  INFO: saw-cut lines (street centres, and 100 um outside the outer dies); layer-20 area; Au area
"""

import csv
import os
import sys
from collections import Counter

import gdstk

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = sys.argv[1] if len(sys.argv) > 1 else "R1_ONE"
DIE, TEST_H, STREET = 10000.0, 2500.0, 200.0
PITCH = DIE + STREET
WAFER_R, EXCL = 50000.0, 45000.0
TOL = 1e-3
CHECK_LAYERS = [1, 10, 20, 22, 40, 50]
EMPTY_LAYERS = [24, 30, 31, 45]
TEXT_BAN = [1, 10, 20, 22, 40, 50]
EXPECT = {"R1_ONE": {"A30": 4, "B60": 1, "SNSPD": 2, "NODET": 2}}
TYPES = {"A30": ("trap_die_v4_A30.gds", "TRAP_DIE_V4_A30"),
         "B60": ("trap_die_v4_B60.gds", "TRAP_DIE_V4_B60"),
         "NODET": ("trap_die_v4_NODET.gds", "TRAP_DIE_V4_NODET"),
         "TEST": ("test_die_v4.gds", "TEST_DIE_V4"),
         "TEST_TRAP": ("test_die_v4_TRAP.gds", "TEST_DIE_V4_TRAP"),
         "SNSPD": ("snspd_die_v4.gds", "SNSPD_DIE_V4")}
CELL_TYPE = {v[1]: k for k, v in TYPES.items()}
N_FAIL = 0


def report(ok, msg, detail=()):
    global N_FAIL
    if not ok:
        N_FAIL += 1
    print(("PASS " if ok else "FAIL ") + msg)
    for s in detail:
        if s:
            print("     " + s)


def finish():
    print("ALL CHECKS PASS" if N_FAIL == 0 else f"{N_FAIL} CHECK(S) FAILED")
    sys.exit(0 if N_FAIL == 0 else 1)


def merged_area(polys):
    if not polys:
        return 0.0
    return sum(p.area() for p in gdstk.boolean(polys, [], "or"))


def on_layer(polys, layer):
    return [p for p in polys if p.layer == layer]


def outline(cell):
    """Bounding box (x0, y0, x1, y1) of the layer-101 outline of a cell, in the cell's own frame."""
    boxes = [p.bounding_box() for p in cell.get_polygons() if p.layer == 101]
    if not boxes:
        return None
    return (min(b[0][0] for b in boxes), min(b[0][1] for b in boxes),
            max(b[1][0] for b in boxes), max(b[1][1] for b in boxes))


def gap_centre(a0, a1, b0, b1):
    """Centre of the gap between two intervals that do not overlap."""
    return (min(a1, b1) + max(a0, b0)) / 2


# ---------------------------------------------------------------- load
run_lib = gdstk.read_gds(os.path.join(HERE, f"run_{NAME}.gds"))
cells = {c.name: c for c in run_lib.cells}
tops = run_lib.top_level()
top_name = f"RUN_{NAME}"
with open(os.path.join(HERE, f"run_{NAME}_map.csv"), newline="") as fh:
    rows = list(csv.DictReader(fh))
print(f"== run {NAME}: {len(rows)} CSV rows, top cells {[c.name for c in tops]}")

# ---------------------------------------------------------------- R1
print("-- R1 top cell, references, CSV")
top = cells.get(top_name)
report(len(tops) == 1 and tops[0].name == top_name, f"R1 top cell is {top_name} (top cells found {[c.name for c in tops]})")
if top is None:
    finish()
refs = top.references
got = Counter((round(r.origin[0], 3), round(r.origin[1], 3), r.cell.name) for r in refs)
want = Counter((round(float(r["x_centre_um"]), 3), round(float(r["y_centre_um"]), 3),
                TYPES.get(r["type"], ("?", "?"))[1]) for r in rows)
miss = sorted((want - got).elements())
extra = sorted((got - want).elements())
report(got == want, f"R1 {len(refs)} references and {len(rows)} CSV rows agree one to one (origin and cell name)",
       [f"in the CSV, not in the GDS: {miss}" if miss else "", f"in the GDS, not in the CSV: {extra}" if extra else ""])
turned = [r.cell.name for r in refs if abs(r.rotation) > TOL or abs(r.magnification - 1) > TOL or r.x_reflection]
report(not turned, f"R1 no reference is rotated, mirrored or scaled ({len(turned)} are)", turned[:20])

# ---------------------------------------------------------------- R2
print("-- R2 counts")
cnt = dict(Counter(CELL_TYPE.get(r.cell.name, "?") for r in refs))
if NAME in EXPECT:
    report(cnt == EXPECT[NAME], f"R2 counts per die type {cnt} (expected {EXPECT[NAME]})")
else:
    print(f"NOTE R2 skipped: no expected counts for {NAME} (counts found {cnt})")

# ---------------------------------------------------------------- R3
print("-- R3 die size, overlap, streets, grid")
dies = []
for r in refs:
    kind = CELL_TYPE.get(r.cell.name, "?")
    ob = outline(r.cell)
    if ob is None:
        report(False, f"R3 die {kind} at {r.origin} has no layer-101 outline")
        continue
    ox, oy = r.origin
    dies.append({"kind": kind, "x0": ob[0] + ox, "y0": ob[1] + oy, "x1": ob[2] + ox, "y1": ob[3] + oy})
for d in dies:
    d["w"], d["h"] = d["x1"] - d["x0"], d["y1"] - d["y0"]
    d["cx"], d["cy"] = (d["x0"] + d["x1"]) / 2, (d["y0"] + d["y1"]) / 2
sizes = sorted(set((round(d["w"], 3), round(d["h"], 3)) for d in dies))
has_test = any(d["kind"].startswith("TEST") for d in dies)
heights_ok = [DIE] + ([TEST_H] if has_test else [])
bad_size = [f"{d['kind']} at ({d['cx']:.1f}, {d['cy']:.1f}): {d['w']:.3f} x {d['h']:.3f}" for d in dies
            if abs(d["w"] - DIE) > TOL or not any(abs(d["h"] - h) < TOL for h in heights_ok)]
report(not bad_size, f"R3 every die is {DIE:.0f} um wide and {heights_ok} um tall; sizes found {sizes}", bad_size)

overlaps, bad_street = [], []
xstreets, ystreets = [], []
nx = ny = 0
for i in range(len(dies)):
    for j in range(i + 1, len(dies)):
        a, b = dies[i], dies[j]
        ox = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
        oy = min(a["y1"], b["y1"]) - max(a["y0"], b["y0"])
        if ox > TOL and oy > TOL:
            overlaps.append(f"{a['kind']} ({a['cx']:.0f}, {a['cy']:.0f}) and {b['kind']} ({b['cx']:.0f}, {b['cy']:.0f})")
        elif ox > TOL:                                   # share an x range, so they are stacked in y
            g = max(a["y0"] - b["y1"], b["y0"] - a["y1"])
            if g < 1000:
                ny += 1
                ystreets.append(gap_centre(a["y0"], a["y1"], b["y0"], b["y1"]))
                if abs(g - STREET) > TOL:
                    bad_street.append(f"y gap {g:.3f} between {a['kind']} ({a['cx']:.0f}, {a['cy']:.0f}) and "
                                      f"{b['kind']} ({b['cx']:.0f}, {b['cy']:.0f})")
        elif oy > TOL:                                   # share a y range, so they sit side by side in x
            g = max(a["x0"] - b["x1"], b["x0"] - a["x1"])
            if g < 1000:
                nx += 1
                xstreets.append(gap_centre(a["x0"], a["x1"], b["x0"], b["x1"]))
                if abs(g - STREET) > TOL:
                    bad_street.append(f"x gap {g:.3f} between {a['kind']} ({a['cx']:.0f}, {a['cy']:.0f}) and "
                                      f"{b['kind']} ({b['cx']:.0f}, {b['cy']:.0f})")
report(not overlaps, f"R3 no two dies overlap ({len(overlaps)} overlapping pair(s))", overlaps)
report(nx + ny > 0 and not bad_street,
       f"R3 neighbouring dies are {STREET:.0f} um apart: {nx} x-neighbour pair(s), {ny} y-neighbour pair(s)", bad_street)

if len(sizes) == 1:
    xc = sorted(set(round(d["cx"], 2) for d in dies))
    yc = sorted(set(round(d["cy"], 2) for d in dies))
    xd = sorted(set(round(b - a, 3) for a, b in zip(xc, xc[1:])))
    yd = sorted(set(round(b - a, 3) for a, b in zip(yc, yc[1:])))
    ok = all(abs(v - PITCH) < TOL for v in xd + yd)
    report(ok, f"R3 die centres on one grid: x pitch found {xd}, y pitch found {yd} (must be {PITCH:.0f})")
else:
    print(f"NOTE R3 grid pitch skipped: die heights differ (sizes {sizes})")

# ---------------------------------------------------------------- R4
print("-- R4 wafer edge")
corners = []
for d in dies:
    for x, y in ((d["x0"], d["y0"]), (d["x0"], d["y1"]), (d["x1"], d["y0"]), (d["x1"], d["y1"])):
        corners.append(((x * x + y * y) ** 0.5, d["kind"], x, y))
rmax = max(corners)
report(rmax[0] <= EXCL, f"R4 every die corner within {EXCL:.0f} um of the wafer centre; largest corner radius "
                        f"{rmax[0]:.1f} um ({rmax[1]} at ({rmax[2]:.0f}, {rmax[3]:.0f}))")

# ---------------------------------------------------------------- R5
print("-- R5 freshness of the die cells in the run")
disk_cache = {}
for kind in sorted(set(r["type"] for r in rows)):
    fname, cname = TYPES[kind]
    if fname not in disk_cache:
        disk_cache[fname] = {c.name: c for c in gdstk.read_gds(os.path.join(HERE, fname)).cells}
    if cname not in cells or cname not in disk_cache[fname]:
        report(False, f"R5 {kind}: cell {cname} missing in the run or in {fname}")
        continue
    rp = cells[cname].get_polygons()
    dp = disk_cache[fname][cname].get_polygons()
    bad = []
    for L in CHECK_LAYERS:
        a_run, a_disk = on_layer(rp, L), on_layer(dp, L)
        if len(a_run) != len(a_disk):
            bad.append(f"layer {L}: polygons {len(a_run)} in the run, {len(a_disk)} on disk")
        ar, ad = merged_area(a_run), merged_area(a_disk)
        if abs(ar - ad) > 1e-3:
            bad.append(f"layer {L}: merged area {ar:.4f} in the run, {ad:.4f} on disk")
    report(not bad, f"R5 {kind} ({cname}) in the run matches {fname} on disk on layers {CHECK_LAYERS}", bad)

# ---------------------------------------------------------------- R6
print("-- R6 layers and labels in the flattened run")
flat = top.get_polygons()
bad_empty = [f"layer {L}: {len(on_layer(flat, L))} polygons" for L in EMPTY_LAYERS if on_layer(flat, L)]
labels = top.get_labels()
bad_text = [f"label {lab.text!r} on layer {lab.layer}" for lab in labels if lab.layer in TEXT_BAN]
report(not bad_empty and not bad_text,
       f"R6 layers {EMPTY_LAYERS} empty; no text labels on layers {TEXT_BAN} ({len(labels)} labels in all)",
       bad_empty + bad_text)

# ---------------------------------------------------------------- R7
print("-- R7 information (not pass/fail)")
xs = sorted(set(round(v, 2) for v in xstreets))
ys = sorted(set(round(v, 2) for v in ystreets))
if dies:
    xs = sorted(set(xs + [round(min(d["x0"] for d in dies) - 100, 2), round(max(d["x1"] for d in dies) + 100, 2)]))
    ys = sorted(set(ys + [round(min(d["y0"] for d in dies) - 100, 2), round(max(d["y1"] for d in dies) + 100, 2)]))
print(f"INFO R7 saw-cut lines, x (um): {xs}")
print(f"INFO R7 saw-cut lines, y (um): {ys}")
l20 = on_layer(flat, 20)
dies_l20 = sum(1 for r in refs if any(p.layer == 20 for p in r.cell.get_polygons()))
print(f"INFO R7 layer-20 area {merged_area(l20) * 1e-6:.5f} mm^2 merged "
      f"(raw sum over the die cells, as make_run.py prints it: {sum(p.area() for p in l20) * 1e-6:.5f} mm^2); "
      f"dies carrying layer 20: {dies_l20} of {len(refs)}")
print(f"INFO R7 layer-50 (Au) merged area {merged_area(on_layer(flat, 50)) * 1e-8:.4f} cm^2")

finish()
