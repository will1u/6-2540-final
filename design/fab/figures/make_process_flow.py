"""Claude-authored figure script: writes process_flow_v4.svg next to this file.

Draws the v4 fabrication flow as 18 small panels. Every panel shows the same
composite cross-section (left: detector under the readout window; middle:
SNSPD contact; right: mirror ground via under the Au ground fill). Only the
layers that exist at that step are drawn, and each panel adds to the one
before it. Standard library only, no classes.

Run from design/sim with:  ./run.sh ../fab/figures/make_process_flow.py

Coordinates: each panel is 255 x 200 px. Inside a panel, the helpers take
local coordinates (x 10-245, Si bottom at y 150) and add the panel origin.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "process_flow_v4.svg")

# ---- grid (px) ----
PW, PH = 255, 200            # panel size
GX, GY = 22, 36              # gaps between panels (x) and rows (y)
X0 = 104                     # left edge of column 0; 12-92 is the row-label gutter
Y0 = 74                      # top of row 0
PITCH_X = PW + GX
PITCH_Y = PH + GY
CANVAS_W = X0 + 3 * PITCH_X + PW + 12
CANVAS_H = Y0 + 5 * PITCH_Y + PH + 14


def col_x(c):
    return X0 + c * PITCH_X


def row_y(r):
    return Y0 + r * PITCH_Y


# ---- colours (same as architecture_crosssection.svg) ----
C_SI = "#c4c4c4"
C_D1 = "#dde7f1"
C_SPACER = "#d9e8f6"
C_CAP = "#cfe0f2"
C_SIO2_STROKE = "#9db4cc"
C_AL = "#7f8fa3"
C_NB = "#5b2a86"
C_HSQ = "#9fd3c7"
C_TIAU = "#b8860b"
C_AU = "#e3b341"
C_AU_STROKE = "#a67c00"
C_SEED = "#c9a227"
C_RESIST = "#e8a0a0"
C_RESIST_STROKE = "#b55"
C_TEXT = "#222"
C_GREY = "#555"
C_LEADER = "#888"
C_ARROW = "#999"
FONT = "\"Segoe UI\", Helvetica, Arial, sans-serif"

# ---- geometry shared by the panels (local x, y) ----
WIRE_X = [82, 87, 92, 97, 102, 107, 112, 117]     # NbN wires, 4 px wide
FOOT = [(15, 35), (60, 16), (128, 30), (168, 72)]  # Au footprints: RF, DC rim, SNSPD lead, ground fill
RESIST = [(10, 5), (50, 10), (76, 52), (158, 10), (240, 5)]  # blocks with no Au footprint
OPEN_CONTACT = (136, 93, 10, 4)                    # layer-40 SNSPD contact opening
OPEN_VIA = (180, 93, 20, 19)                       # layer-40 mirror via

OUT = []


def num(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def rect(x, y, w, h, fill, stroke=None, sw=0.5, rx=None):
    a = 'x="%s" y="%s" width="%s" height="%s" fill="%s"' % (num(x), num(y), num(w), num(h), fill)
    if stroke:
        a += ' stroke="%s" stroke-width="%s"' % (stroke, num(sw))
    if rx:
        a += ' rx="%s"' % num(rx)
    OUT.append("<rect %s/>" % a)


def text(x, y, s, size=11, weight=None, fill=C_TEXT, anchor=None):
    a = 'x="%s" y="%s" font-size="%s"' % (num(x), num(y), num(size))
    if weight:
        a += ' font-weight="%s"' % weight
    if fill != C_TEXT:
        a += ' fill="%s"' % fill
    if anchor:
        a += ' text-anchor="%s"' % anchor
    OUT.append("<text %s>%s</text>" % (a, s))


def polyline(points, stroke=C_ARROW, sw=1.0, arrow=False):
    pts = " ".join("%s,%s" % (num(x), num(y)) for x, y in points)
    a = 'points="%s" fill="none" stroke="%s" stroke-width="%s"' % (pts, stroke, num(sw))
    if arrow:
        a += ' marker-end="url(#arw)"'
    OUT.append("<polyline %s/>" % a)


# ---- the composite cross-section ----
def draw_stack(ox, oy, st):
    """Draw the layers present at this step. st is a dict of flags.

    Order: Si, thermal SiO2, recess (if flagged), Al (if flagged), spacer (if flagged), then the rest.
    """
    rect(ox + 10, oy + 130, 235, 20, C_SI)                                   # Si
    rect(ox + 10, oy + 112, 235, 18, C_D1, C_SIO2_STROKE)                    # thermal SiO2 (step 2), 1.0 um
    if st.get("recess"):
        rect(ox + 60, oy + 112, 155, 4, "#ffffff")                           # etched recess, empty (step 3b)
    if st.get("al"):
        rect(ox + 60, oy + 112, 155, 4, C_AL)                                # Al mirror (step 3c-3d), inlaid in the recess
    if st.get("spacer"):
        rect(ox + 10, oy + 104, 235, 8, C_SPACER, C_SIO2_STROKE)            # spacer (step 4), drawn after the Al
    if st.get("blanket"):
        rect(ox + 10, oy + 101, 235, 3, C_NB)                                # NbN film (step 5)
    if st.get("cap"):
        rect(ox + 10, oy + 93, 235, 11, C_CAP, C_SIO2_STROKE)                # SiO2 cap (step 8), before the wires
    if st.get("wires"):
        for wx in WIRE_X:
            rect(ox + wx, oy + 101, 4, 3, C_NB)                              # nanowires (step 7)
        rect(ox + 120, oy + 101, 12, 3, C_NB)                                # NbN tab
    if st.get("hsq"):
        for wx in WIRE_X:
            rect(ox + wx, oy + 99, 4, 2, C_HSQ)                              # HSQ caps on the wires
    if st.get("contact"):
        rect(ox + 126, oy + 97, 24, 4, C_TIAU)                               # Ti/Au contact (step 6)
    if st.get("openings"):
        x, y, w, h = OPEN_CONTACT
        rect(ox + x, oy + y, w, h, "#ffffff")
        x, y, w, h = OPEN_VIA
        rect(ox + x, oy + y, w, h, "#ffffff")


def draw_resist(ox, oy, y, h):
    for x0, w in RESIST:
        rect(ox + x0, oy + y, w, h, C_RESIST, C_RESIST_STROKE, 0.6)


def draw_au(ox, oy, y, h):
    for x0, w in FOOT:
        rect(ox + x0, oy + y, w, h, C_AU, C_AU_STROKE, 0.6)


def draw_openings_filled(ox, oy):
    x, y, w, h = OPEN_CONTACT
    rect(ox + x, oy + y, w, h, C_AU, C_AU_STROKE, 0.6)
    x, y, w, h = OPEN_VIA
    rect(ox + x, oy + y, w, h, C_AU, C_AU_STROKE, 0.6)


def draw_seed_full(ox, oy):
    rect(ox + 10, oy + 91, 235, 2, C_SEED)                                   # seed over the cap top
    for x, y, w, h in [(136, 93, 2, 4), (144, 93, 2, 4), (180, 93, 2, 19),
                       (198, 93, 2, 19), (180, 110, 20, 2)]:                 # seed lining the openings
        rect(ox + x, oy + y, w, h, C_SEED)


def draw_seed_under_au(ox, oy):
    for x0, w in FOOT:
        rect(ox + x0, oy + 91, w, 2, C_SEED)


# ---- panel frame: border, title, tag, captions ----
def frame(ox, oy, title, caps, tag=False):
    rect(ox, oy, PW, PH, "none", "#d8d8d8", 0.8, rx=4)
    text(ox + 10, oy + 30, title, size=12, weight="bold")
    if tag:
        rect(ox + 186, oy + 3, 60, 16, "#f2f2f2", "#777", 0.8, rx=8)
        text(ox + 216, oy + 15, "R1_TRAP", size=11, anchor="middle")
    for i, c in enumerate(caps):
        text(ox + 10, oy + 172 + 14 * i, c, size=11, fill=C_GREY)


def arrow_h(c, r):
    """Thin arrow from the right edge of cell c to the left edge of cell c+1 (mid panel)."""
    y = row_y(r) + 100
    polyline([(col_x(c) + PW + 2, y), (col_x(c + 1) - 2, y)], arrow=True)


# ---- state of the stack at each step (cumulative) ----
S1 = {}
S3 = {"al": True, "spacer": True}
S4 = {"al": True, "spacer": True, "blanket": True}
S5 = {"al": True, "spacer": True, "blanket": True, "contact": True}
S6 = {"al": True, "spacer": True, "wires": True, "hsq": True, "contact": True}
S7 = dict(S6, cap=True)
S8 = dict(S7, openings=True)

# Step 3 panels: recess only (3a-3b), recess plus Al (3c, 3d).
S3A = {"recess": True}
S3C = {"al": True}


def cell_origin(name):
    return {
        "P1": (0, 0), "P2": (1, 0), "P3": (2, 0), "P4": (3, 0),      # row 0: Si, step 3a-3b, 3c, 3d
        "P5": (0, 1), "P6": (1, 1), "P7": (2, 1), "P8": (3, 1),      # row 1: spacer, NbN, contacts, nanowire
        "P9": (0, 2), "P10": (1, 2),                                 # row 2: cap, openings
        "P11": (0, 3), "P12": (1, 3), "P13": (2, 3), "P14": (3, 3),  # row 3: E1 branch, P14 = R1_TRAP key
        "P15": (0, 4), "P16": (1, 4), "P17": (2, 4), "P18": (3, 4),  # row 4: E2 branch
        "P19": (0, 5),                                               # row 5: test, dice, package
    }[name]


def origin(name):
    c, r = cell_origin(name)
    return col_x(c), row_y(r)


# Leader labels for the 11 Openings panel: (text, anchor, x, row baseline, target y).
# The leader runs straight down from (x, row + 3) to (x, target).
OPENINGS_LABELS = [
    ("SiO₂ spacer", "start", 14, 42, 108),
    ("SiO₂ cap", "start", 89, 42, 96),
    ("Al mirror", "end", 74, 54, 114),
    ("NbN wires", "start", 94, 54, 101),
    ("Ti/Au contact", "start", 128, 66, 97),
    ("contact opening", "start", 137, 78, 95),
    ("mirror via", "middle", 182, 90, 100),
]


def leader_labels_openings(ox, oy):
    for label, anchor, x, row, target in OPENINGS_LABELS:
        text(ox + x, oy + row, label, anchor=anchor)
        polyline([(ox + x, oy + row + 3), (ox + x, oy + target)], stroke=C_LEADER, sw=0.6)


def centred_label(ox, oy, label, cx, row, target_x, target_y):
    """RF / DC rim / window labels: centred text with a short vertical leader."""
    text(ox + cx, oy + row, label, anchor="middle")
    polyline([(ox + target_x, oy + row + 3), (ox + target_x, oy + target_y)], stroke=C_LEADER, sw=0.6)


def draw_sketch_top_view(ox, oy):
    """Top view of the die on the frame, with bond pads and bond wires."""
    rect(ox + 30, oy + 36, 200, 124, "none", "#999", 0.8)                     # package frame
    rect(ox + 80, oy + 52, 100, 100, "#f4f4f4", "#555", 0.8)                 # die 10 x 10 mm
    for px in (90, 110, 130, 150):
        rect(ox + px, oy + 54, 8, 6, C_AU, C_AU_STROKE, 0.6)                 # top pads
        rect(ox + px, oy + 142, 8, 6, C_AU, C_AU_STROKE, 0.6)                # bottom pads
        polyline([(ox + px + 4, oy + 54), (ox + px + 4, oy + 36)], stroke="#777", sw=0.8)
        polyline([(ox + px + 4, oy + 148), (ox + px + 4, oy + 160)], stroke="#777", sw=0.8)


def draw_legend_cell(px, py):
    """Fourth cell of the E1 row: R1_TRAP key."""
    rect(px + 10, py + 8, 60, 16, "#f2f2f2", "#777", 0.8, rx=8)
    text(px + 40, py + 20, "R1_TRAP", anchor="middle")
    lines = [
        "R1_TRAP runs only the tagged steps:",
        "Au directly on thermal SiO₂",
        "(no Al, NbN, spacer, cap or openings)",
    ]
    for i, s in enumerate(lines):
        text(px + 10, py + 50 + 14 * i, s, fill=C_GREY)


def draw_branch_label(r, lines):
    py = row_y(r)
    for i, s in enumerate(lines):
        text(12, py + 92 + 12 * i, s, weight="bold" if i == 0 else None)


def draw_key_and_notes(px, py):
    text(px, py + 22, "Legend and notes", size=12, weight="bold")
    text(px, py + 42, "Steps 9, 10, 16a and 16 are removed in v4 (they were the 10 µm SiO₂ D2, "
                      "the ITO, the layer-45 protect patch and the gap etch).")
    text(px, py + 60, "Electrode Au is open: E1 (row 4) and E2 (row 5) are drawn with equal weight.")
    text(px, py + 78, "Layers accumulate from panel to panel. Captions give the process values.", fill=C_GREY)
    text(px, py + 96, "Step 3 inlays the Al mirror: recess etched and Al lifted off with one resist, "
                      "so the surface stays flat.")
    keys = [
        ("Si", C_SI), ("thermal SiO₂", C_D1), ("SiO₂ spacer", C_SPACER),
        ("SiO₂ cap", C_CAP), ("Al", C_AL), ("NbN", C_NB),
        ("HSQ", C_HSQ), ("Ti/Au contact", C_TIAU), ("Au", C_AU),
        ("Au plating seed", C_SEED), ("photoresist", C_RESIST),
    ]
    for i, (label, colour) in enumerate(keys):
        kx = px + (i % 6) * 130
        ky = py + 120 + (i // 6) * 22
        rect(kx, ky - 10, 14, 11, colour, "#999", 0.4)
        text(kx + 20, ky, label)


def main():
    OUT.append('<?xml version="1.0" encoding="UTF-8"?>')
    OUT.append("<!-- Claude-authored figure, 2026-11-09, written by make_process_flow.py. "
               "Composite schematic, not to scale. Steps from fab/TRAVELER.md and fab/process/. -->")
    OUT.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
               'font-family=\'%s\'>' % (CANVAS_W, CANVAS_H, CANVAS_W, CANVAS_H, FONT))
    OUT.append('<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
               'markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>'
               % C_ARROW)
    rect(0, 0, CANVAS_W, CANVAS_H, "#ffffff")

    # header
    text(12, 34, "v4 process flow", size=19, weight="bold")
    text(12, 54, "Composite schematic, not to scale: detector under the window (left), SNSPD contact "
                 "(middle), mirror ground via under the Au ground fill (right).", size=12, fill=C_GREY)

    # ---- row 0: Si, step 3 (three panels), P1-P4 ----
    ox, oy = origin("P1")
    frame(ox, oy, "0-2 Si, marks, thermal SiO₂",
          ["HR Si ρ > 20 kΩ·cm; layer-1 marks;", "SiO₂ 1.0 µm"], tag=True)
    draw_stack(ox, oy, S1)
    ox, oy = origin("P2")
    frame(ox, oy, "3a–3b Resist, SiO₂ recess (layer 10)",
          ["LOR + positive resist; RIE a", "100 nm recess in thermal SiO₂"])
    draw_stack(ox, oy, S3A)
    rect(ox + 10, oy + 98, 50, 14, C_RESIST, C_RESIST_STROKE, 0.6)
    rect(ox + 215, oy + 98, 30, 14, C_RESIST, C_RESIST_STROKE, 0.6)
    ox, oy = origin("P3")
    frame(ox, oy, "3c Evaporate Al",
          ["Al 100 nm, e-beam evaporated,", "through the same resist"])
    draw_stack(ox, oy, S3C)
    rect(ox + 10, oy + 98, 50, 14, C_RESIST, C_RESIST_STROKE, 0.6)
    rect(ox + 215, oy + 98, 30, 14, C_RESIST, C_RESIST_STROKE, 0.6)
    rect(ox + 10, oy + 94, 50, 4, C_AL)                                      # Al on the resist
    rect(ox + 215, oy + 94, 30, 4, C_AL)
    ox, oy = origin("P4")
    frame(ox, oy, "3d Lift-off",
          ["Al top level with the SiO₂;", "only under the centre DC"])
    draw_stack(ox, oy, S3C)
    ox, oy = origin("P5")
    frame(ox, oy, "4 SiO₂ spacer", ["PECVD SiO₂ 238 nm, ≤ 300 °C"])
    draw_stack(ox, oy, S3)
    ox, oy = origin("P6")
    frame(ox, oy, "5 NbN film", ["NbN 7 nm, sputtered"])
    draw_stack(ox, oy, S4)

    # ---- row 1: P5-P8 ----
    ox, oy = origin("P7")
    frame(ox, oy, "6 Ti/Au contacts (layer 22)", ["lift-off; contacts and", "EBL marks only"])
    draw_stack(ox, oy, S5)
    ox, oy = origin("P8")
    frame(ox, oy, "7 Nanowire (layer 20, e-beam)", ["HSQ mask, CF₄ etch;", "130 nm wires, 200 nm pitch"])
    draw_stack(ox, oy, S6)

    # ---- row 2: cap, openings ----
    ox, oy = origin("P9")
    frame(ox, oy, "8 SiO₂ cap", ["HSQ + PECVD SiO₂ = 160 ± 10 nm", "over the wires"])
    draw_stack(ox, oy, S7)
    ox, oy = origin("P10")
    frame(ox, oy, "11 Openings (layer 40)", ["contact: 160 nm;", "mirror via: ≈ 0.40 µm"])
    draw_stack(ox, oy, S8)
    leader_labels_openings(ox, oy)

    # ---- row 3: E1 branch, P11-P13, R1_TRAP key in the fourth cell ----
    ox, oy = origin("P11")
    frame(ox, oy, "12 (E1) Lift-off resist", ["LOR + positive resist,", "layer 50 drawn"], tag=True)
    draw_stack(ox, oy, S8)
    draw_resist(ox, oy, 79, 14)
    ox, oy = origin("P12")
    frame(ox, oy, "13 (E1) Evaporate Ti/Au", ["Ar pre-clean, Ti 10 nm / Au 350 nm"], tag=True)
    draw_stack(ox, oy, S8)
    draw_resist(ox, oy, 79, 14)
    for x0, w in RESIST:
        rect(ox + x0, oy + 74, w, 5, C_AU, C_AU_STROKE, 0.6)             # Au on top of the resist
    draw_au(ox, oy, 88, 5)
    draw_openings_filled(ox, oy)
    ox, oy = origin("P13")
    frame(ox, oy, "14-15 (E1) Lift-off, inspect", ["lift-off in NMP; 5 µm gaps open"], tag=True)
    draw_stack(ox, oy, S8)
    draw_au(ox, oy, 88, 5)
    draw_openings_filled(ox, oy)
    centred_label(ox, oy, "RF", 32, 82, 32, 88)
    centred_label(ox, oy, "DC rim", 66, 82, 68, 88)
    centred_label(ox, oy, "SNSPD lead", 143, 82, 143, 88)
    centred_label(ox, oy, "window", 100, 66, 100, 92)
    centred_label(ox, oy, "ground fill", 205, 66, 205, 88)
    draw_legend_cell(*origin("P14"))

    # ---- row 4: E2 branch, P15-P18 ----
    ox, oy = origin("P15")
    frame(ox, oy, "12 (E2) Plating seed", ["Ar pre-clean, Ti 15 nm / Au 50 nm"], tag=True)
    draw_stack(ox, oy, S8)
    draw_seed_full(ox, oy)
    ox, oy = origin("P16")
    frame(ox, oy, "13 (E2) Plating mold", ["AZ nLOF 2070 ≥ 8 µm,", "layer 50 inverted"], tag=True)
    draw_stack(ox, oy, S8)
    draw_seed_full(ox, oy)
    draw_resist(ox, oy, 53, 38)
    ox, oy = origin("P17")
    frame(ox, oy, "14 (E2) Au plating", ["6 µm Au"], tag=True)
    draw_stack(ox, oy, S8)
    draw_seed_full(ox, oy)
    draw_resist(ox, oy, 53, 38)
    draw_au(ox, oy, 61, 30)
    draw_openings_filled(ox, oy)
    ox, oy = origin("P18")
    frame(ox, oy, "15 (E2) Strip, seed removal", ["Ar etch of the Au seed,", "F-plasma etch of the Ti"], tag=True)
    draw_stack(ox, oy, S8)
    draw_seed_under_au(ox, oy)
    draw_au(ox, oy, 61, 30)
    draw_openings_filled(ox, oy)
    centred_label(ox, oy, "window", 100, 44, 100, 92)
    centred_label(ox, oy, "ground fill", 205, 44, 205, 61)
    centred_label(ox, oy, "RF", 32, 56, 32, 61)
    centred_label(ox, oy, "DC rim", 68, 56, 68, 61)
    centred_label(ox, oy, "SNSPD lead", 143, 56, 143, 61)

    # ---- row 5: P19 and the legend block ----
    ox, oy = origin("P19")
    frame(ox, oy, "17-19 Test, dice, package",
          ["wafer-level electrical test;", "10 × 10 mm dies; Au wire bonds"], tag=True)
    draw_sketch_top_view(ox, oy)
    draw_key_and_notes(col_x(1), row_y(5) + 22)

    # ---- branch labels (left gutter) ----
    draw_branch_label(3, ["Branch E1:", "Ti/Au", "lift-off,", "0.35 µm"])
    draw_branch_label(4, ["Branch E2:", "plated Au,", "6 µm"])

    # ---- arrows between consecutive panels in the same row ----
    for c in range(3):
        arrow_h(c, 0)
        arrow_h(c, 1)
    arrow_h(0, 2)                                    # P9 -> P10
    arrow_h(0, 3)                                    # P11 -> P12
    arrow_h(1, 3)                                    # P12 -> P13
    for c in range(3):
        arrow_h(c, 4)                                # P15 -> P16 -> P17 -> P18

    # snakes: P4 -> P5, P8 -> P9 (end of a row to the start of the next), P18 -> P19
    x_right = col_x(3) + PW / 2
    x_left = col_x(0) + PW / 2
    polyline([(x_right, row_y(0) + PH + 2), (x_right, row_y(0) + PH + 18), (x_left, row_y(0) + PH + 18),
              (x_left, row_y(1) - 2)], arrow=True)
    polyline([(x_right, row_y(1) + PH + 2), (x_right, row_y(1) + PH + 18), (x_left, row_y(1) + PH + 18),
              (x_left, row_y(2) - 2)], arrow=True)
    polyline([(x_right, row_y(4) + PH + 2), (x_right, row_y(4) + PH + 18), (x_left, row_y(4) + PH + 18),
              (x_left, row_y(5) - 2)], arrow=True)

    # ---- fork from the openings panel (P10, row 2, column 1): E1 (row 4) and E2 (row 5) ----
    x_open = col_x(1) + PW / 2
    yf = row_y(2) + PH + 18                      # middle of the gap under row 2
    polyline([(x_open, row_y(2) + PH + 2), (x_open, yf), (96, yf)])
    text(560, yf - 4, "electrode Au: choose E1 or E2 (open)", fill=C_GREY)
    polyline([(x_left, yf), (x_left, row_y(3) - 2)], arrow=True)
    polyline([(96, yf), (96, row_y(4) - 18), (x_left, row_y(4) - 18), (x_left, row_y(4) - 2)], arrow=True)

    OUT.append("</svg>")
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(OUT) + "\n")
    print("wrote", OUT_PATH, CANVAS_W, "x", CANVAS_H)


if __name__ == "__main__":
    main()
