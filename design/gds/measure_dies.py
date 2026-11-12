"""Measure the v4 GDS files for the fabrication documents (Claude-authored).

Read-only: reads design/gds/*.gds and writes design/gds/measured_v4.json and measured_v4.md.
It never writes or regenerates a GDS file. Run from design/sim:  ./run.sh ../gds/measure_dies.py

Method, in short
  files      SHA-256 (first 16 hex characters) and local modification time of each file.
  areas      each top cell is flattened (top.flatten()); per layer the polygons are merged with
             gdstk.boolean(polys, [], "or") and the merged area is summed. Layer 20 is also split by datatype.
  Au         layer 50 merged area in cm^2. E2 plating and E1 evaporation write the same Au pattern, so one
             number serves both. The complement is the outline box (layer 101 bbox) minus the merged Au.
  meander    the NbN lines are rectangles. A line is a polygon whose bounding box is 0.125-0.135 um tall and
             at least 10 um wide. Check: the NbN piece nearest (240, 0) is cut at x = 240 um and the
             intervals are counted (only lines cross that cut).
  inductance straight sections only (turns, tapers and tabs excluded):
             Lk = hbar * Rs / (pi * 1.76 * kB * Tc) per square, constants from sim/15_snspd_geometry.py part E
             (hbar 1.0546e-34 J s, kB 1.3807e-23 J/K, Rs 400 ohm/sq, Tc 7.9 K).
             squares = total straight length / wire width; L = squares * Lk; tau = L / 50 ohm;
             room-temperature resistance = squares * 400 ohm.
  openings   layer 40 merged connected components, classified by bounding box (see classify()).
  mirror     layer 10 merged union. Path from the Al detector end (its maximum x) to the ground via centre,
             along the strip centreline y = 0, then up the branch: |x_end - x_via| + |y_via|.
"""

import datetime
import hashlib
import json
import os
from collections import Counter

import gdstk
import numpy as np
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon as SPoly
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["trap_die_v4_A30.gds", "trap_die_v4_B60.gds", "trap_die_v4_NODET.gds", "test_die_v4.gds",
         "test_die_v4_TRAP.gds", "snspd_die_v4.gds", "run_R1_TRAP.gds", "run_R1_FULL.gds", "run_R1_ONE.gds",
         "wafer_v4.gds"]
DETECTOR = ["trap_die_v4_A30.gds", "trap_die_v4_B60.gds"]
SNSPD_DIE = "snspd_die_v4.gds"                  # eight detector cells, no trap: section 10, not the section 5 analysis
RUNS = ["run_R1_TRAP.gds", "run_R1_FULL.gds", "run_R1_ONE.gds"]
PLAIN = ["trap_die_v4_NODET.gds", "test_die_v4_TRAP.gds", "run_R1_TRAP.gds"]   # nothing on layers 10, 20, 22, 40
FAB_LAYERS = [1, 10, 20, 22, 40, 50]
EMPTY_LAYERS = [24, 30, 31, 45]
READ_X = 240.0                                  # readout zone x (layer_map.md), um

HBAR, KB = 1.0546e-34, 1.3807e-23               # sim/15_snspd_geometry.py part E
RS, TC, Z0 = 400.0, 7.9, 50.0                   # ohm/sq, K, ohm
LK = HBAR * RS / (np.pi * 1.76 * KB * TC)       # H per square
RUN_EBL_MM2_MAKE_RUN = 0.0502                   # printed by make_run.py for run_R1_FULL
RUN_EBL_MM2_MAKE_RUN_ONE = 0.0378               # printed by make_run.py R1_ONE (raw sum over die cells)

EXPECT_DIE = {"trap_die_v4_A30.gds": {"lines": 160, "straight_mm": 5.76, "L_uH": 3.10, "tau_ns": 62.0},
              "trap_die_v4_B60.gds": {"lines": 160, "straight_mm": 11.04, "L_uH": 5.94, "tau_ns": 118.8}}


def sha16(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def bbox_of(polys):
    pts = np.concatenate([np.array(p.points) for p in polys])
    return [[float(pts[:, 0].min()), float(pts[:, 1].min())], [float(pts[:, 0].max()), float(pts[:, 1].max())]]


def merged(polys):
    return gdstk.boolean(polys, [], "or") if polys else []


def area(polys):
    return float(sum(p.area() for p in polys))


def shapely_parts(polys):
    """Shapely union of polygons, as a list of connected pieces."""
    if not polys:
        return []
    u = unary_union([SPoly(np.array(p.points)).buffer(0) for p in polys])
    return list(u.geoms) if hasattr(u, "geoms") else [u]


def classify(x0, x1, y0, y1):
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    if x0 <= 170 and x1 >= 140 and abs(cy) < 10:
        return "SNSPD contact"
    if abs(w - 100) <= 1 and abs(h - 100) <= 1:
        return "mirror ground via"
    if (abs(w - 60) <= 1 and abs(h - 24) <= 1) or (abs(w - 24) <= 1 and abs(h - 60) <= 1):
        return "mark cross"
    return "unclassified"


def meander(p20):
    lines = []
    for p in p20:
        (x0, y0), (x1, y1) = p.bounding_box()
        if 0.125 <= y1 - y0 <= 0.135 and x1 - x0 >= 10.0:
            lines.append((x0, y0, x1, y1, len(p.points)))
    if not lines:
        return {"lines": 0}
    lengths = [b - a for a, _, b, _, _ in lines]
    hs = [d - c for _, c, _, d, _ in lines]
    cys = sorted((c + d) / 2 for _, c, _, d, _ in lines)
    diffs = np.diff(cys)
    total = float(sum(lengths))
    w_um = float(np.median(hs))
    # cross-check: cut the NbN piece nearest the readout zone at x = READ_X
    pieces = shapely_parts(p20)
    piece = min(pieces, key=lambda g: g.distance(Point(READ_X, 0.0)))
    cut = LineString([(READ_X, -100.0), (READ_X, 100.0)]).intersection(piece)
    n_cut = 0 if cut.is_empty else (len(cut.geoms) if hasattr(cut, "geoms") else 1)
    inside = sum(1 for a, c, b, d, _ in lines if piece.buffer(0.01).contains(Point((a + b) / 2, (c + d) / 2)))
    squares = total / w_um
    L_H = squares * LK
    return {
        "lines": len(lines),
        "rectangles": sum(1 for *_, npts in lines if npts == 4),
        "length_um_min": float(min(lengths)), "length_um_max": float(max(lengths)),
        "width_um_min": float(min(hs)), "width_um_max": float(max(hs)), "width_um": w_um,
        "pitch_um_median": float(np.median(diffs)), "pitch_um_min": float(diffs.min()),
        "pitch_um_max": float(diffs.max()),
        "radial_span_um": float(max(d for *_, d, _ in lines) - min(c for _, c, _, _, _ in lines)),
        "x_range_um": [float(min(a for a, *_ in lines)), float(max(b for _, _, b, _, _ in lines))],
        "straight_total_um": total, "straight_total_mm": total / 1000.0,
        "squares": squares, "Lk_pH_per_sq": LK * 1e12, "L_uH": L_H * 1e6,
        "tau_ns": L_H / Z0 * 1e9, "R_room_ohm": squares * RS,
        "cut_x_um": READ_X, "cut_intervals": n_cut,
        "lines_inside_nbn_piece": inside,
        "nbn_piece_area_um2": float(piece.area), "nbn_piece_pieces_in_layer20": len(pieces),
        "nbn_piece_bounds_um": [float(v) for v in piece.bounds],
    }


def measure(name):
    path = os.path.join(HERE, name)
    st = os.stat(path)
    lib = gdstk.read_gds(path)
    tops = lib.top_level()
    assert len(tops) == 1, f"{name}: {len(tops)} top cells"
    top = tops[0]
    refs = dict(Counter(getattr(r.cell, "name", str(r.cell)) for r in top.references))
    top.flatten()
    polys = top.get_polygons()
    by_layer = {}
    for p in polys:
        by_layer.setdefault(p.layer, []).append(p)
    rec = {
        "file": name, "sha256_16": sha16(path), "bytes": st.st_size,
        "mtime_local": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "top_cell": top.name, "direct_references_before_flatten": refs,
    }
    outline = by_layer.get(101) or [p for L in FAB_LAYERS for p in by_layer.get(L, [])]
    rec["outline_bbox_um"] = bbox_of(outline)
    rec["outline_source"] = "layer 101 polygons" if by_layer.get(101) else "fab layers 1-50"
    rec["outline_area_um2"] = (rec["outline_bbox_um"][1][0] - rec["outline_bbox_um"][0][0]) * \
                              (rec["outline_bbox_um"][1][1] - rec["outline_bbox_um"][0][1])
    rec["layers_present"] = sorted(int(L) for L in by_layer)
    rec["layers"] = {}
    for L in sorted(set(by_layer) | set(FAB_LAYERS) | set(EMPTY_LAYERS)):
        ps = by_layer.get(L, [])
        m = merged(ps)
        a = area(m)
        d = {"polygons": len(ps), "merged_um2": a, "merged_mm2": a * 1e-6}
        if L == 20:
            d["datatypes"] = {}
            for dt in sorted(set(p.datatype for p in ps)):
                sub = [p for p in ps if p.datatype == dt]
                d["datatypes"][str(dt)] = {"polygons": len(sub), "merged_um2": area(merged(sub))}
        if L == 50:
            d["Au_cm2"] = a * 1e-8
            if m:
                box = gdstk.rectangle(tuple(rec["outline_bbox_um"][0]), tuple(rec["outline_bbox_um"][1]))
                d["complement_in_outline_cm2"] = area(gdstk.boolean([box], m, "not")) * 1e-8
            else:
                d["complement_in_outline_cm2"] = rec["outline_area_um2"] * 1e-8
        if L == 40:
            d["openings"] = []
            for g in shapely_parts(ps):
                x0, y0, x1, y1 = g.bounds
                d["openings"].append({"class": classify(x0, x1, y0, y1),
                                      "centre_um": [round((x0 + x1) / 2, 3), round((y0 + y1) / 2, 3)],
                                      "size_um": [round(x1 - x0, 3), round(y1 - y0, 3)]})
        rec["layers"][str(L)] = d
    if name in DETECTOR:
        rec["meander"] = meander(by_layer[20])
        ms = rec["meander"]
        # the Al mirror and ground via
        al = shapely_parts(by_layer[10])
        al_u = unary_union(al)
        via = [o for o in rec["layers"]["40"]["openings"] if o["class"] == "mirror ground via"]
        b = al_u.bounds
        mir = {"bbox_um": [float(v) for v in b],
               "strip_width_um_at_x0": float(LineString([(0, -500), (0, 500)]).intersection(al_u).length),
               "strip_width_um_at_via": None, "via_centre_um": None, "path_um": None}
        if via:
            vx, vy = via[0]["centre_um"]
            mir["strip_width_um_at_via"] = float(LineString([(vx, -500), (vx, 500)]).intersection(al_u).length)
            mir["via_centre_um"] = [vx, vy]
            mir["path_um"] = float((b[2] - vx) + abs(vy))
            mir["path_from_x_um"] = float(b[2])
        rec["mirror"] = mir
    if name in RUNS:
        ebl = area(merged(by_layer.get(20, [])))
        rec["run"] = {
            "ebl_merged_mm2": ebl * 1e-6,
            "ebl_raw_sum_mm2": float(sum(p.area() for p in by_layer.get(20, []))) * 1e-6,
            "au_cm2": rec["layers"]["50"]["Au_cm2"],
            "dies_expected_by_make_run": dict(refs),
        }
    return rec


def acceptance(recs):
    rows = []

    def add(item, expected, measured, ok):
        rows.append({"item": item, "expected": expected, "measured": measured, "pass": bool(ok)})

    for n in DETECTOR:
        m, e = recs[n]["meander"], EXPECT_DIE[n]
        add(f"{n}: meander lines", e["lines"], m["lines"], m["lines"] == e["lines"])
        add(f"{n}: meander cut at x = 240 um", e["lines"], m["cut_intervals"], m["cut_intervals"] == e["lines"])
        add(f"{n}: total straight length (mm, 1 %)", e["straight_mm"], round(m["straight_total_mm"], 4),
            abs(m["straight_total_mm"] / e["straight_mm"] - 1) < 0.01)
        add(f"{n}: L (uH, 1 %)", e["L_uH"], round(m["L_uH"], 4), abs(m["L_uH"] / e["L_uH"] - 1) < 0.01)
        add(f"{n}: tau (ns, 1 %)", e["tau_ns"], round(m["tau_ns"], 3), abs(m["tau_ns"] / e["tau_ns"] - 1) < 0.01)
    r = recs["run_R1_FULL.gds"]["run"]["ebl_merged_mm2"]
    add("run_R1_FULL EBL area (mm^2, 2 % of make_run 0.0502)", RUN_EBL_MM2_MAKE_RUN, round(r, 6),
        abs(r / RUN_EBL_MM2_MAKE_RUN - 1) < 0.02)
    r1 = recs["run_R1_ONE.gds"]["run"]["ebl_merged_mm2"]
    add("run_R1_ONE EBL area (mm^2, 2 % of make_run 0.0378)", RUN_EBL_MM2_MAKE_RUN_ONE, round(r1, 6),
        abs(r1 / RUN_EBL_MM2_MAKE_RUN_ONE - 1) < 0.02)
    for n in FILES:
        bad = [L for L in EMPTY_LAYERS if recs[n]["layers"][str(L)]["polygons"]]
        add(f"{n}: layers 24, 30, 31, 45 empty", "0 polygons", f"{bad if bad else 0} non-empty", not bad)
    for n in PLAIN:
        bad = [L for L in (10, 20, 22, 40) if recs[n]["layers"][str(L)]["polygons"]]
        add(f"{n}: nothing on layers 10, 20, 22, 40", "0 polygons", f"{bad if bad else 0} non-empty", not bad)
    return rows


def fmt(x, nd=3):
    return "-" if x is None else f"{x:.{nd}f}"


def write_md(recs, acc, path):
    out = ["> **Claude-authored.** Written by gds/measure_dies.py; regenerate, do not edit.", "",
           "Read-only measurement of the v4 GDS files (no GDS was written). Units are given in each header. "
           "Top cells are flattened before measuring. Areas are merged per layer (gdstk boolean OR).", ""]
    out += ["## 1. Files", "", "| File | SHA-256 (first 16) | Modified (local) | Bytes | Top cell | Outline bbox, um (source) |",
            "|---|---|---|---:|---|---|"]
    for n in FILES:
        r = recs[n]
        b = r["outline_bbox_um"]
        out.append(f"| {n} | {r['sha256_16']} | {r['mtime_local']} | {r['bytes']} | {r['top_cell']} | "
                   f"({b[0][0]:.0f}, {b[0][1]:.0f}) to ({b[1][0]:.0f}, {b[1][1]:.0f}) ({r['outline_source']}) |")
    out += ["", "## 2. Merged area per layer", "", "Cell = polygon count / merged area in mm^2.", "",
            "| Layer | " + " | ".join(FILES) + " |", "|---|" + "---|" * len(FILES)]
    for L in FAB_LAYERS + [100, 101] + EMPTY_LAYERS:
        cells = []
        for n in FILES:
            d = recs[n]["layers"].get(str(L))
            cells.append("-" if d is None else f"{d['polygons']} / {d['merged_mm2']:.4f}")
        out.append(f"| {L} | " + " | ".join(cells) + " |")
    out += ["", "## 3. Au (layer 50) and the plating mold", "",
            "E2 plated area = E1 evaporated area (same Au pattern). Complement = outline box minus Au, i.e. the area "
            "exposed in inverted-exposure plating-mold lithography.", "",
            "| File | Au written, cm^2 | Complement in outline, cm^2 | Outline area, cm^2 |", "|---|---:|---:|---:|"]
    for n in FILES:
        d = recs[n]["layers"]["50"]
        out.append(f"| {n} | {d['Au_cm2']:.5f} | {d['complement_in_outline_cm2']:.4f} | "
                   f"{recs[n]['outline_area_um2'] * 1e-8:.4f} |")
    out += ["", "## 4. Layer 20 (EBL) by datatype", "", "| File | Datatype | Polygons | Merged area, um^2 |", "|---|---:|---:|---:|"]
    for n in FILES:
        for dt, v in recs[n]["layers"]["20"]["datatypes"].items():
            out.append(f"| {n} | {dt} | {v['polygons']} | {v['merged_um2']:.1f} |")
    for n in DETECTOR:
        m = recs[n]["meander"]
        out += ["", f"## 5. Detector meander, {n}", "", "| Quantity | Value |", "|---|---:|",
                f"| Lines (polygons 0.125-0.135 um tall, >= 10 um long) | {m['lines']} |",
                f"| Lines that are plain rectangles | {m['rectangles']} |",
                f"| Cut check at x = {READ_X:.0f} um: intervals | {m['cut_intervals']} |",
                f"| Lines inside the NbN piece nearest (240, 0) | {m['lines_inside_nbn_piece']} of {m['lines']} |",
                f"| Line length, um (min / max) | {m['length_um_min']:.3f} / {m['length_um_max']:.3f} |",
                f"| Wire width, um (median; min / max) | {m['width_um']:.3f} ({m['width_um_min']:.3f} / {m['width_um_max']:.3f}) |",
                f"| Pitch, um (median; min / max) | {m['pitch_um_median']:.3f} ({m['pitch_um_min']:.3f} / {m['pitch_um_max']:.3f}) |",
                f"| Radial span, um | {m['radial_span_um']:.2f} |",
                f"| Straight total, um / mm | {m['straight_total_um']:.1f} / {m['straight_total_mm']:.4f} |",
                f"| Squares = total / width | {m['squares']:.1f} |",
                f"| Lk, pH/sq | {m['Lk_pH_per_sq']:.2f} |",
                f"| L, uH | {m['L_uH']:.4f} |",
                f"| tau = L/50 ohm, ns | {m['tau_ns']:.2f} |",
                f"| Room-temperature R of straight sections, ohm | {m['R_room_ohm']:.0f} |"]
    out += ["", "Excluded from L and tau: turns, tapers, tabs and connections. Lk = hbar Rs / (pi 1.76 kB Tc) with "
            "hbar 1.0546e-34 J s, kB 1.3807e-23 J/K (sim/15_snspd_geometry.py part E), Rs 400 ohm/sq, Tc 7.9 K.", ""]
    out += ["## 6. Layer 40 openings", "", "| File | Class | Count |", "|---|---|---:|"]
    for n in FILES:
        cnt = Counter(o["class"] for o in recs[n]["layers"]["40"]["openings"])
        for c, k in sorted(cnt.items()):
            out.append(f"| {n} | {c} | {k} |")
    out += ["", "Detail for the detector dies (centre and size, um):", "", "| File | Class | Centre | Size |", "|---|---|---|---|"]
    for n in DETECTOR:
        for o in recs[n]["layers"]["40"]["openings"]:
            out.append(f"| {n} | {o['class']} | ({o['centre_um'][0]}, {o['centre_um'][1]}) | "
                       f"{o['size_um'][0]} x {o['size_um'][1]} |")
    out += ["", "## 7. Local Al mirror (layer 10), detector dies", "",
            "| Quantity | " + " | ".join(DETECTOR) + " |", "|---|" + "---:|" * len(DETECTOR)]
    mm = [recs[n]["mirror"] for n in DETECTOR]
    out.append("| Bbox, um (x0, y0) to (x1, y1) | " + " | ".join(
        f"({m['bbox_um'][0]:.1f}, {m['bbox_um'][1]:.1f}) to ({m['bbox_um'][2]:.1f}, {m['bbox_um'][3]:.1f})" for m in mm) + " |")
    out.append("| Strip width at x = 0, um | " + " | ".join(f"{m['strip_width_um_at_x0']:.2f}" for m in mm) + " |")
    out.append("| Strip width at the via, um | " + " | ".join(fmt(m['strip_width_um_at_via'], 2) for m in mm) + " |")
    out.append("| Ground via centre, um | " + " | ".join(str(m['via_centre_um']) for m in mm) + " |")
    out.append("| Path, Al detector end to via, um | " + " | ".join(fmt(m['path_um'], 1) for m in mm) + " |")
    out.append("")
    out.append("Path = (x_end - x_via) + |y_via| along the strip centreline, with x_end the Al maximum x (detector end).")
    out += ["", "## 8. Runs and wafer: totals", "", "| File | Direct references (die cell: count) | EBL layer 20, mm^2 (merged) | EBL, mm^2 (raw sum) | Au layer 50, cm^2 |",
            "|---|---|---:|---:|---:|"]
    for n in RUNS + ["wafer_v4.gds"]:
        r = recs[n]
        if n in RUNS:
            out.append(f"| {n} | {r['direct_references_before_flatten']} | {r['run']['ebl_merged_mm2']:.5f} | "
                       f"{r['run']['ebl_raw_sum_mm2']:.5f} | {r['run']['au_cm2']:.4f} |")
        else:
            out.append(f"| {n} | {r['direct_references_before_flatten']} | {r['layers']['20']['merged_mm2']:.4f} | "
                       f"- | {r['layers']['50']['Au_cm2']:.4f} |")
    out += ["", "make_run.py printed 0.0502 mm^2 for run_R1_FULL: the sum over die cells (raw, not merged) is compared above.", ""]
    out += ["## 9. Acceptance", "", "| Check | Expected | Measured | Pass |", "|---|---|---|---|"]
    for a in acc:
        out.append(f"| {a['item']} | {a['expected']} | {a['measured']} | {'PASS' if a['pass'] else 'FAIL'} |")
    s = recs[SNSPD_DIE]
    out += ["", "## 10. SNSPD-only die (snspd_die_v4.gds)", "",
            "Eight detector cells, no trap. Section 5 (single-meander analysis) does not apply to it.", "",
            "| Quantity | Value |", "|---|---:|",
            f"| Layer-20 datatypes present | {len(s['layers']['20']['datatypes'])} |"]
    for dt, v in s["layers"]["20"]["datatypes"].items():
        out.append(f"| Layer 20, datatype {dt}: merged area, um^2 (polygons) | {v['merged_um2']:.1f} ({v['polygons']}) |")
    out += [f"| Au (layer 50), cm^2 | {s['layers']['50']['Au_cm2']:.5f} |", "",
            "Layer-40 openings by size (um):", "", "| Size | Count |", "|---|---:|"]
    sizes = Counter(f"{o['size_um'][0]} x {o['size_um'][1]}" for o in s["layers"]["40"]["openings"])
    for sz, k in sorted(sizes.items()):
        out.append(f"| {sz} | {k} |")
    out.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    recs = {n: measure(n) for n in FILES}
    acc = acceptance(recs)
    out_json = os.path.join(HERE, "measured_v4.json")
    doc = {"generated_by": "design/gds/measure_dies.py (Claude-authored)",
           "constants": {"hbar_J_s": HBAR, "kB_J_K": KB, "Rs_ohm_per_sq": RS, "Tc_K": TC, "Z0_ohm": Z0,
                         "Lk_H_per_sq": LK, "Lk_formula": "hbar Rs / (pi * 1.76 * kB * Tc) (sim/15 part E)",
                         "readout_x_um": READ_X, "make_run_ebl_mm2": RUN_EBL_MM2_MAKE_RUN,
                         "make_run_ebl_mm2_R1_ONE": RUN_EBL_MM2_MAKE_RUN_ONE},
           "files": recs, "acceptance": acc}
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1)
    write_md(recs, acc, os.path.join(HERE, "measured_v4.md"))
    print(f"Lk = {LK * 1e12:.2f} pH/sq")
    for n in FILES:
        r = recs[n]
        print(f"{n:24s} sha {r['sha256_16']}  Au {r['layers']['50']['Au_cm2']:.5f} cm^2  "
              f"EBL {r['layers']['20']['merged_mm2']:.5f} mm^2")
    for n in DETECTOR:
        m = recs[n]["meander"]
        print(f"{n}: lines {m['lines']} (cut {m['cut_intervals']}), length {m['straight_total_mm']:.4f} mm, "
              f"L {m['L_uH']:.3f} uH, tau {m['tau_ns']:.1f} ns, R {m['R_room_ohm']:.0f} ohm")
    for a in acc:
        print(("PASS " if a["pass"] else "FAIL ") + a["item"] + f" | expected {a['expected']} | measured {a['measured']}")


if __name__ == "__main__":
    main()
