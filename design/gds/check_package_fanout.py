"""Centre-to-centre PGA84L fan-out check (Claude-authored; DESIGN_LOG step 29).

Requires pdfplumber (available in the bundled document Python runtime). Usage:
python check_package_fanout.py [path/to/pkg-pga84l-char.pdf]
Measures vector finger edges on PDF page 2; no guessed uniform finger pitch.
"""

import csv
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import sys

import pdfplumber

HERE = Path(__file__).resolve().parent
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "pkg-pga84l-char (1).pdf"
OUT = HERE.parent / "sim" / "out" / "16_pad_pitch_check"
OUT.mkdir(parents=True, exist_ok=True)
PAD_CSV = HERE / "trap_die_v4_A30_pads.csv"

with pdfplumber.open(PDF) as doc:
    page = doc.pages[1]
    # Inner cavity rounded rectangle, selected by location and overall size.
    cavity, = [c for c in page.curves if 120 < c["x0"] < 130 and 480 < c["x1"] < 490
               and 165 < c["top"] < 175 and 530 < c["bottom"] < 540]
    cx = (cavity["x0"] + cavity["x1"]) / 2
    cy = (cavity["top"] + cavity["bottom"]) / 2
    sx = 11938 / (cavity["x1"] - cavity["x0"])
    sy = 11938 / (cavity["bottom"] - cavity["top"])
    fingers = []
    for edge in ("top", "bottom", "left", "right"):
        sides = []
        for obj in page.lines + page.curves:
            for a, b in zip(obj["pts"], obj["pts"][1:]):
                x, y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
                selected = {
                    "top": 125 < y < 170 and 125 < x < 495 and 28 < dy < 32,
                    "bottom": 540 < y < 575 and 125 < x < 495 and 28 < dy < 32,
                    "left": 90 < x < 125 and 165 < y < 545 and 27 < dx < 32,
                    "right": 490 < x < 525 and 165 < y < 545 and 27 < dx < 32,
                }[edge]
                if selected:
                    sides.append((x, y))
        assert len(sides) == 42, (edge, len(sides))
        sides.sort(key=lambda p: p[0] if edge in ("top", "bottom") else p[1])
        for i in range(0, len(sides), 2):
            x, y = ((sides[i][j] + sides[i + 1][j]) / 2 for j in (0, 1))
            # PDF coordinates are x-right/y-down. Convert to y-up, rotate 90 deg
            # CCW per the drawing, then mirror x to view from the die-facing side.
            px, py = (cy - y) * sy, (x - cx) * sx
            new_edge = ("T" if py > 0 else "B") if abs(py) > abs(px) else ("R" if px > 0 else "L")
            fingers.append(dict(edge=new_edge, x_um=px, y_um=py,
                                pdf_edge=edge, pdf_x_pt=x, pdf_y_pt=y))

for edge in "TBLR":
    group = sorted((f for f in fingers if f["edge"] == edge),
                   key=lambda f: f["x_um"] if edge in "TB" else f["y_um"])
    for i, f in enumerate(group, 1):
        f["finger"] = f"{edge}{i:02}"
    assert len(group) == 21

pads = list(csv.DictReader(PAD_CSV.open(newline="")))
for p in pads:
    p["x_um"], p["y_um"] = float(p["x_um"]), float(p["y_um"])
    p["edge"] = ("T" if p["y_um"] > 0 else "B") if abs(p["y_um"]) > abs(p["x_um"]) else ("R" if p["x_um"] > 0 else "L")


def wire(p, f):
    dx, dy = f["x_um"] - p["x_um"], f["y_um"] - p["y_um"]
    normal, tangent = (abs(dy), abs(dx)) if p["edge"] in "TB" else (abs(dx), abs(dy))
    return math.degrees(math.atan2(tangent, normal)), math.hypot(dx, dy)


rows = []
for edge in "TBLR":
    axis = "x_um" if edge in "TB" else "y_um"
    ps = sorted((p for p in pads if p["edge"] == edge), key=lambda p: p[axis])
    fs = sorted((f for f in fingers if f["edge"] == edge), key=lambda f: f[axis])
    # At most 21 choose 5 candidates here; enumerate to make the minimax choice exact.
    def score(choice):
        metrics = [wire(p, f) for p, f in zip(ps, choice)]
        return max(a for a, length in metrics), sum(length for a, length in metrics)
    chosen = min(combinations(fs, len(ps)), key=score)
    for p, f in zip(ps, chosen):
        angle, length = wire(p, f)
        rows.append(dict(pad=p["pad"], electrode=p["electrode"], edge=edge, finger=f["finger"],
                         chip_x_um=p["x_um"], chip_y_um=p["y_um"],
                         finger_x_um=f["x_um"], finger_y_um=f["y_um"],
                         projected_length_um=length, angle_deg=angle))


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


segments = [((r["chip_x_um"], r["chip_y_um"]), (r["finger_x_um"], r["finger_y_um"])) for r in rows]
for (a, b), (c, d) in combinations(segments, 2):
    assert not (cross(a, b, c) * cross(a, b, d) < 0 and cross(c, d, a) * cross(c, d, b) < 0), "Crossing wires"
assert len({r["finger"] for r in rows}) == len(rows) == len(pads)

for name, data in (("package_fingers.csv", fingers), ("fanout.csv", rows)):
    with (OUT / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
summary = dict(pdf_page=2, pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),
               pad_csv_sha256=hashlib.sha256(PAD_CSV.read_bytes()).hexdigest(),
               cavity_um=11938, pdf_cavity_bounds_pt=[cavity[k] for k in ("x0", "top", "x1", "bottom")],
               scale_um_per_pdf_point=[sx, sy], landing="finger centre; no placement sweep",
               orientation="rotate bottom-view drawing 90 deg CCW, then mirror x for die-facing view",
               finger_ids="local edge-order IDs, not package pin numbers", crossings=0,
               edges={edge: dict(wires=sum(r["edge"] == edge for r in rows),
                                worst_angle_deg=max(r["angle_deg"] for r in rows if r["edge"] == edge),
                                longest_projected_wire_um=max(r["projected_length_um"] for r in rows if r["edge"] == edge))
                      for edge in "TBLR"})
summary["top_bottom_under_45"] = all(r["angle_deg"] < 45 for r in rows if r["edge"] in "TB")
(OUT / "fanout_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

# A simple plan-view drawing; axes in um, SVG y points down.
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8200 -8200 16400 16400">',
       '<rect x="-8200" y="-8200" width="16400" height="16400" fill="white"/>',
       '<rect x="-5969" y="-5969" width="11938" height="11938" fill="none" stroke="#999" stroke-width="20"/>',
       '<rect x="-5000" y="-5000" width="10000" height="10000" fill="#eee" stroke="#555" stroke-width="20"/>']
for r in rows:
    x, y, u, v = r["chip_x_um"], -r["chip_y_um"], r["finger_x_um"], -r["finger_y_um"]
    svg.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="#276b9c" stroke-width="18"/>')
    svg.append(f'<text x="{u}" y="{v-70}" font-size="95" text-anchor="middle">{r["pad"]}/{r["finger"]}</text>')
for f in fingers:
    svg.append(f'<circle cx="{f["x_um"]}" cy="{-f["y_um"]}" r="65" fill="#b38b25"/>')
svg.append('<text x="0" y="-7650" font-size="240" text-anchor="middle">PGA84L centre-to-centre fan-out (provisional carrier)</text></svg>')
(OUT / "fanout.svg").write_text("\n".join(svg))
print(json.dumps(summary, indent=2))
if not summary["top_bottom_under_45"]:
    raise SystemExit("STOP: fan-out angle exceeds 45 deg; do not update documentation")
