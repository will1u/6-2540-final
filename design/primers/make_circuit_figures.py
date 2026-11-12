"""Claude-authored figure script: writes the circuit diagrams for RF_PRIMER.md into design/primers/figures/.

One small schematic per primer section (1, 2, 3, 5, 6, 7 twice, 8). Standard library only, no classes.
Every label uses a value that is already printed on the primer page (from primer_numbers.py or the sim
summaries); nothing is computed here.

Run from design/sim with:  ./run.sh ../primers/make_circuit_figures.py

How the drawing works (so you can edit it):
- `part(kind, x1, y1, x2, y2)` draws one component between two points. It draws the component along the
  x axis, then rotates and moves it with an SVG transform, so one function handles horizontal, vertical
  and diagonal placement. The two wire stubs at each end are included.
- `label(x, y, text)` writes text. In the text, `C_{c}` makes a subscript.
- Each figure function returns (width, height, list of SVG strings) and main() writes the file.
- Black strokes on a white background rect, so the figures read in light and dark viewers.
"""
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

INK = "#111111"
GREY = "#777777"
BLUE = "#1f5fa8"      # currents
RED = "#b03a2e"       # things that are lossy or unwanted
FONT = "Segoe UI, Arial, Helvetica, sans-serif"


# ------------------------------------------------------------------ text
def label(x, y, text, size=14, anchor="start", color=INK, bold=False, italic=False):
    """Text at (x, y). `_{...}` in the text becomes a subscript. `\\n` starts a new line."""
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        # split into plain pieces and subscript pieces, escape each, then join
        pieces = re.split(r"_\{([^}]*)\}", line)      # even index = plain, odd index = subscript
        s = ""
        for k, piece in enumerate(pieces):
            piece = piece.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if k % 2 == 0:
                if k > 0:      # dy persists, so lift the text that follows a subscript back up
                    piece = '<tspan dy="-3">%s</tspan>' % (piece if piece else "​")
                s += piece
            else:
                s += '<tspan dy="3" font-size="%d">%s</tspan>' % (round(size * 0.72), piece)
        out.append('<text x="%g" y="%g" font-family="%s" font-size="%d" text-anchor="%s" fill="%s"%s%s>%s</text>'
                   % (x, y + i * size * 1.25, FONT, size, anchor, color,
                      ' font-weight="bold"' if bold else "", ' font-style="italic"' if italic else "", s))
    return "\n".join(out)


# ------------------------------------------------------------------ wires and symbols
def wire(*points, color=INK, dash=False):
    """Polyline through the given (x, y) points."""
    pts = " ".join("%g,%g" % p for p in points)
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="2"%s/>'
            % (pts, color, ' stroke-dasharray="6 4"' if dash else ""))


def dot(x, y):
    return '<circle cx="%g" cy="%g" r="3.5" fill="%s"/>' % (x, y, INK)


def open_dot(x, y):
    return '<circle cx="%g" cy="%g" r="4" fill="white" stroke="%s" stroke-width="2"/>' % (x, y, INK)


def ground(x, y, up=False):
    """Ground symbol whose wire end is at (x, y); three bars below (or above if up=True)."""
    s = -1 if up else 1
    g = ['<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2"/>' % (x, y, x, y + s * 10, INK)]
    for i, half in enumerate((12, 8, 4)):
        yy = y + s * (10 + 5 * i)
        g.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2"/>'
                 % (x - half, yy, x + half, yy, INK))
    return "\n".join(g)


def arrow(x1, y1, x2, y2, color=BLUE, width=2):
    """Straight arrow from (x1, y1) to (x2, y2) with a filled head."""
    ang = math.atan2(y2 - y1, x2 - x1)
    h = 9
    p1 = (x2 - h * math.cos(ang - 0.4), y2 - h * math.sin(ang - 0.4))
    p2 = (x2 - h * math.cos(ang + 0.4), y2 - h * math.sin(ang + 0.4))
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"/>'
            '<polygon points="%g,%g %g,%g %g,%g" fill="%s"/>'
            % (x1, y1, x2, y2, color, width, x2, y2, p1[0], p1[1], p2[0], p2[1], color))


def _body(kind, b, dash):
    """Component body drawn along +x from 0 to b, centred on y = 0 (local coordinates)."""
    st = 'fill="none" stroke="%s" stroke-width="2"%s' % (RED if dash else INK, ' stroke-dasharray="5 3"' if dash else "")
    if kind == "res":          # zigzag: 6 teeth
        n = 6
        pts = [(0, 0)]
        for i in range(n):
            pts.append(((i + 0.5) * b / n, -7 if i % 2 == 0 else 7))
        pts.append((b, 0))
        return '<polyline points="%s" %s/>' % (" ".join("%g,%g" % p for p in pts), st)
    if kind == "cap":          # two plates
        c = b / 2
        return ('<line x1="%g" y1="-11" x2="%g" y2="11" %s/><line x1="%g" y1="-11" x2="%g" y2="11" %s/>'
                % (c - 4, c - 4, st, c + 4, c + 4, st))
    if kind == "ind":          # four humps
        n = 4
        r = b / n / 2
        d = "M0,0 " + " ".join("a%g,%g 0 0 1 %g,0" % (r, r, 2 * r) for _ in range(n))
        return '<path d="%s" %s/>' % (d, st)
    if kind == "box":          # unnamed impedance
        return '<rect x="0" y="-9" width="%g" height="18" %s/>' % (b, st)
    if kind == "ac":           # circle with a sine wave
        c = b / 2
        return ('<circle cx="%g" cy="0" r="%g" %s/><path d="M%g,0 q4.5,-10 9,0 t9,0" %s/>'
                % (c, c, st, c - 9, st))
    if kind == "cs":           # circle with an arrow (direction x1 -> x2)
        c = b / 2
        return ('<circle cx="%g" cy="0" r="%g" %s/><line x1="%g" y1="0" x2="%g" y2="0" %s/>'
                '<polygon points="%g,0 %g,-5 %g,5" fill="%s"/>'
                % (c, c, st, c - 9, c + 8, st, c + 10, c + 2, c + 2, INK))
    if kind == "dc":           # battery-like DC source: long and short plate
        c = b / 2
        return ('<line x1="%g" y1="-12" x2="%g" y2="12" %s/><line x1="%g" y1="-6" x2="%g" y2="6" %s/>'
                % (c - 4, c - 4, st, c + 4, c + 4, st))
    raise ValueError(kind)


BODY = {"res": 42, "cap": 12, "ind": 44, "box": 40, "ac": 34, "cs": 34, "dc": 12}


def part(kind, x1, y1, x2, y2, dash=False, body=None):
    """Component between (x1, y1) and (x2, y2): lead, body centred, lead."""
    length = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    b = body if body else BODY[kind]
    lead = (length - b) / 2
    col = RED if dash else INK
    g = ['<g transform="translate(%g,%g) rotate(%g)">' % (x1, y1, ang)]
    g.append('<line x1="0" y1="0" x2="%g" y2="0" stroke="%s" stroke-width="2"/>' % (lead, col))
    g.append('<line x1="%g" y1="0" x2="%g" y2="0" stroke="%s" stroke-width="2"/>' % (lead + b, length, col))
    g.append('<g transform="translate(%g,0)">%s</g>' % (lead, _body(kind, b, dash)))
    g.append("</g>")
    return "".join(g)


def svg(w, h, parts):
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<rect width="%d" height="%d" fill="white"/>' % (w, h, w, h, w, h))
    return head + "\n".join(parts) + "</svg>\n"


def panel_title(x, y, text):
    return label(x, y, text, size=15, bold=True)


# ------------------------------------------------------------------ figure 1: the chip is a capacitor
def fig_chip_capacitor():
    p = []
    p.append(panel_title(20, 28, "The RF source sees a capacitor"))
    # source, top wire, chip capacitor, return wire with ground
    p.append(part("ac", 140, 215, 140, 95))
    p.append(wire((140, 95), (320, 95)))
    p.append(part("cap", 320, 95, 320, 215))
    p.append(wire((140, 215), (320, 215)))
    p.append(ground(230, 215))
    p.append(dot(230, 215))
    p.append(label(116, 150, "RF source\n53 V, 28 MHz", anchor="end"))
    p.append(label(340, 150, "C_{chip} = 2.59 pF\n(A30, E2)"))
    p.append(arrow(180, 80, 280, 80))
    p.append(label(230, 64, "I = ωCV = 24.1 mA", anchor="middle", color=BLUE, bold=True))
    # the two alternatives from section 1
    p.append(panel_title(470, 28, "Same source, other loads"))
    p.append(wire((470, 70), (680, 70)))
    p.append(label(470, 58, "RF rail", size=12, color=GREY))
    p.append(part("cap", 520, 70, 520, 190))
    p.append(ground(520, 190))
    p.append(part("cap", 640, 70, 640, 190))
    p.append(ground(640, 190))
    p.append(label(520, 225, "die-wide Al plane\n(dropped)\n127 pF → 1.18 A", size=13, anchor="middle", color=RED))
    p.append(label(640, 225, "10 µm D2 baseline (v3)\n2.9 pF → 27.0 mA", size=13, anchor="middle"))
    return 720, 290, p


# ------------------------------------------------------------------ figure 2: resonator
def fig_resonator():
    p = []
    p.append(panel_title(20, 28, "Resonator: the source only replaces the loss"))
    p.append(part("ac", 110, 220, 110, 80))
    p.append(wire((110, 80), (240, 80)))
    p.append(wire((110, 220), (520, 220)))
    p.append(ground(300, 220))
    p.append(dot(300, 220))
    p.append(label(92, 155, "RF source", anchor="end"))
    # tank: three parallel branches
    p.append(wire((240, 80), (520, 80)))
    for x in (300, 400, 500):
        p.append(dot(x, 80))
    p.append(part("ind", 300, 80, 300, 220))
    p.append(part("cap", 400, 80, 400, 220))
    p.append(part("box", 500, 80, 500, 220, dash=True))
    p.append(label(285, 150, "L", anchor="end", bold=True))
    p.append(label(385, 150, "C_{tot}", anchor="end", bold=True))
    p.append(label(515, 150, "R_{loss}", color=RED, bold=True))
    p.append(label(515, 170, "(sets Q)", color=RED, size=12))
    # energy swap
    p.append(arrow(318, 105, 382, 105, color=BLUE, width=1.5))
    p.append(arrow(382, 195, 318, 195, color=BLUE, width=1.5))
    p.append(label(350, 62, "W = CV²/2 swaps between C and L", size=12, anchor="middle", color=BLUE))
    p.append(label(20, 262, "ω₀ = 1/√(LC), P = ωCV²/(2Q).  Example C_{tot} = 10 pF, Q = 100: L = 3.23 µH, P = 24.7 mW.", size=13))
    p.append(label(20, 282, "C_{tot} contains the chip (2.59 pF on E2); a 1 pF error shifts the resonance by 1.40 MHz.", size=13))
    return 600, 300, p


# ------------------------------------------------------------------ figure 3: loss
def fig_loss():
    p = []
    p.append(panel_title(20, 28, "(a) Two lumped losses"))
    # series R_s
    p.append(label(20, 62, "series R", size=13, color=GREY))
    p.append(wire((30, 90), (60, 90)))
    p.append(part("res", 60, 90, 160, 90, dash=True))
    p.append(part("cap", 160, 90, 160, 180))
    p.append(ground(160, 180))
    p.append(label(110, 68, "R_{s}", anchor="middle", color=RED, bold=True))
    p.append(label(176, 140, "C", bold=True))
    p.append(label(20, 215, "Q = 1/(ωCR_{s})\nP = ½ I²R_{s}", size=13))
    # dielectric: C parallel R
    p.append(label(270, 62, "lossy dielectric (Si, SiO₂)", size=13, color=GREY))
    p.append(wire((280, 90), (390, 90)))
    p.append(part("cap", 320, 90, 320, 180))
    p.append(part("box", 380, 90, 380, 180, dash=True))
    p.append(wire((320, 90), (380, 90)))
    p.append(dot(320, 90))
    p.append(wire((320, 180), (380, 180)))
    p.append(dot(350, 180))
    p.append(ground(350, 180))
    p.append(label(305, 140, "C", anchor="end", bold=True))
    p.append(label(396, 140, "R_{d}", color=RED, bold=True))
    p.append(label(270, 215, "Q = 1/(p tan δ)\ntan δ (Si, 28 MHz) = 0.274", size=13))

    # (b) the rail as a ladder
    p.append(panel_title(20, 280, "(b) The RF rail is a ladder, not one resistor"))
    y0, y1 = 340, 420
    xs = [90, 220, 350, 480]
    p.append(wire((30, y0), (xs[0], y0)))
    p.append(label(30, y0 - 12, "feed", size=12, color=GREY))
    for i, x in enumerate(xs):
        p.append(dot(x, y0))
        p.append(part("cap", x, y0, x, y1))
        p.append(ground(x, y1))
        if i < len(xs) - 1:
            p.append(part("res", x, y0, xs[i + 1], y0, dash=True))
    # current arrows above the rail shrink toward the open end
    for i, x in enumerate(xs[:-1]):
        n = 4 - i
        p.append(arrow(x + 40, y0 - 22, x + 40 + 12 * n, y0 - 22, width=1.5 + 0.6 * n))
    p.append(label(500, y0 - 6, "open end:\ncurrent → 0", size=12, color=GREY))
    p.append(label(20, 462, "I falls linearly along the rail, so R_{eff} = R/3 and P = V²ω²C²R/6 (Dietl et al., App. A).", size=13))
    return 640, 480, p


# ------------------------------------------------------------------ figure 5: pickup
def fig_pickup():
    p = []
    p.append(panel_title(20, 28, "Capacitive pickup: a divider"))
    p.append(label(20, 58, "RF rail", size=12, color=GREY))
    p.append(part("ac", 60, 240, 60, 80))
    p.append(wire((60, 80), (160, 80)))
    p.append(wire((60, 240), (400, 240)))
    p.append(ground(230, 240))
    p.append(dot(230, 240))
    p.append(label(36, 165, "V", anchor="end", bold=True))
    p.append(part("cap", 160, 80, 300, 80, body=14))
    p.append(label(230, 62, "C_{c}", anchor="middle", bold=True))
    # node X
    p.append(dot(300, 80))
    p.append(part("cap", 300, 80, 300, 240))
    p.append(label(285, 165, "C_{g}", anchor="end", bold=True))
    p.append(wire((300, 80), (400, 80)))
    p.append(part("box", 400, 80, 400, 240, dash=True))
    p.append(label(414, 165, "low-Z path\nto ground", size=12, color=RED))
    p.append(label(300, 64, "conductor", size=12, color=GREY, anchor="start"))
    p.append(label(20, 285, "Tied to ground (box present):  I = ωC_{c}V flows to ground.", size=13))
    p.append(label(20, 305, "Floating (box removed):  V_{node} = V·C_{c}/(C_{c}+C_{g}).", size=13))
    # Thevenin equivalent
    p.append(panel_title(600, 28, "Thevenin equivalent"))
    p.append(part("ac", 680, 240, 680, 110))
    p.append(wire((680, 110), (730, 110)))
    p.append(part("cap", 730, 110, 860, 110, body=14))
    p.append(open_dot(860, 110))
    p.append(wire((680, 240), (860, 240)))
    p.append(open_dot(860, 240))
    p.append(label(658, 180, "V·C_{c}/(C_{c}+C_{g})", anchor="end", size=13))
    p.append(label(795, 92, "1/(jω(C_{c}+C_{g}))", anchor="middle", size=13))
    p.append(label(560, 285, "E2 slot lead: C_{c} = 4.776 fF → 44.53 µA.", size=13))
    p.append(label(560, 305, "Nanowire window: C_{RN} = 0.1029 fF → 0.9593 µA.", size=13))
    return 900, 325, p


# ------------------------------------------------------------------ figure 6: DC filter
def fig_dc_filter():
    p = []
    p.append(panel_title(20, 28, "A DC line: filter and RF pickup meet at the electrode"))
    # DAC -> R -> node E
    p.append(part("dc", 70, 250, 70, 100, body=12))
    p.append(label(55, 175, "DAC\n±10 V", anchor="end"))
    p.append(wire((70, 100), (110, 100)))
    p.append(part("res", 110, 100, 260, 100))
    p.append(label(185, 82, "R", anchor="middle", bold=True))
    p.append(dot(300, 100))
    p.append(wire((260, 100), (300, 100)))
    p.append(wire((70, 250), (300, 250)))
    # C_f to ground at the chip
    p.append(part("cap", 300, 100, 300, 250))
    p.append(ground(300, 250))
    p.append(label(285, 180, "C_{f}", anchor="end", bold=True))
    p.append(dot(300, 250))
    # electrode
    p.append(wire((300, 100), (430, 100)))
    p.append('<rect x="430" y="82" width="90" height="36" fill="white" stroke="%s" stroke-width="2"/>' % INK)
    p.append(label(475, 106, "electrode", anchor="middle", size=13))
    # coupling from the rail
    p.append(part("cap", 475, 20, 475, 82, body=12))
    p.append(label(493, 56, "C_{c}", bold=True))
    p.append(label(475, 14, "RF rail, V", anchor="middle", size=12, color=GREY))
    # bracket labels
    p.append(label(20, 310, "(a) Hold at RF ground: V_{el} = V·C_{c}/(C_{c}+C_{f}+C_{g}).", size=13))
    p.append(label(20, 332, "     C_{c} = 0.414 pF, C_{g} = 3.21 pF (sim 23): 211.93 mV (100 pF), 21.88 mV (1 nF), 2.20 mV (10 nF).", size=13))
    p.append(label(20, 362, "(b) Cut noise: R and C_{f} low-pass, f_{c} = 1/(2πRC), τ = RC.", size=13))
    p.append(label(20, 384, "     1 kΩ and 1 nF: 159.15 kHz. The same filter slows the transport waveform.", size=13))
    return 640, 405, p


# ------------------------------------------------------------------ figure 7a: SNSPD and readout
def fig_snspd_readout():
    p = []
    p.append(panel_title(20, 28, "SNSPD and readout chain"))
    # nanowire: L_k in series with hotspot R, to ground
    p.append(wire((120, 110), (120, 110)))
    p.append(part("ind", 120, 110, 120, 200, body=44))
    p.append(part("res", 120, 200, 120, 280, dash=True, body=36))
    p.append(ground(120, 280))
    p.append(label(105, 160, "L_{k}", anchor="end", bold=True))
    p.append(label(105, 250, "hotspot\nR_{hs} (kΩ)", anchor="end", color=RED, size=12))
    p.append(label(120, 92, "nanowire", anchor="middle", size=12, color=GREY))
    # bias tee
    p.append(dot(120, 110))
    p.append(wire((120, 110), (250, 110)))
    p.append(dot(250, 110))
    p.append(part("ind", 250, 110, 250, 40, body=36))
    p.append(label(232, 78, "bias-tee L", size=12, anchor="end"))
    p.append(arrow(250, 36, 250, 20, color=INK, width=1.5))
    p.append(label(262, 22, "I_{b} (DC)", size=12))
    p.append(part("cap", 250, 110, 340, 110, body=14))
    p.append(label(295, 94, "C", anchor="middle", size=12))
    # 50 ohm line to notch, low-pass, amplifier
    p.append(wire((340, 110), (580, 110)))
    p.append(label(375, 94, "50 Ω line", size=12, color=GREY))
    p.append(dot(420, 110))
    p.append(part("ind", 420, 110, 420, 175, body=30))
    p.append(part("cap", 420, 175, 420, 250, body=12))
    p.append(ground(420, 250))
    p.append(label(436, 165, "28 MHz notch\n(series L-C)", size=12))
    p.append(part("res", 470, 110, 560, 110, body=36))
    p.append(label(515, 94, "low-pass", anchor="middle", size=12))
    p.append(dot(560, 110))
    p.append(part("cap", 560, 110, 560, 250))
    p.append(ground(560, 250))
    p.append(wire((560, 110), (620, 110)))
    p.append('<rect x="620" y="86" width="90" height="48" fill="white" stroke="%s" stroke-width="2"/>' % INK)
    p.append(label(665, 115, "amplifier", anchor="middle", size=13))
    p.append(label(20, 322, "Photon: hotspot pushes I_{b} into the line, pulse ≈ I_{b}×50 Ω (0.40 mV at 8 µA).", size=13))
    p.append(label(20, 342, "Recovery τ = L_{k}/50 Ω: A30 61.98 ns (corner 2.568 MHz), B60 118.80 ns (1.340 MHz).", size=13))
    p.append(label(20, 362, "A 1 nF bypass at the pad would low-pass the pulse at 3.18 MHz, close to the A30 corner.", size=13))
    return 740, 382, p


# ------------------------------------------------------------------ figure 7b: lead termination (sim 19)
def fig_lead_termination():
    p = []
    p.append(panel_title(20, 28, "Two leads, common-mode pickup (sim 19 model)"))
    ax, bx, ny = 160, 560, 195
    # current injections from the rail, into both nodes
    for x, name in ((ax, "A"), (bx, "B")):
        p.append(ground(x, 75, up=True))
        p.append(part("cs", x, 75, x, ny, body=34))
        p.append(label(x + 22, 140, "I_{inj}", color=BLUE, bold=True))
        p.append(dot(x, ny))
    p.append(label(ax - 14, ny - 8, "A", anchor="end", bold=True, size=15))
    p.append(label(bx + 14, ny - 8, "B", anchor="start", bold=True, size=15))
    # nanowire between A and B
    p.append(part("ind", ax, ny, 340, ny, body=44))
    p.append(part("res", 340, ny, bx, ny, dash=True, body=36))
    p.append(label(250, ny - 24, "L_{k}", anchor="middle", bold=True))
    p.append(label(450, ny - 24, "R_{pair}", anchor="middle", color=RED, bold=True))
    p.append(label(360, ny + 30, "nanowire current I_{nw}", anchor="middle", color=BLUE, bold=True))
    p.append(arrow(300, ny + 42, 420, ny + 42, width=1.5))
    # bond wire and termination to ground
    for x, name in ((ax, "A"), (bx, "B")):
        p.append(part("ind", x, ny, x, ny + 80, body=36))
        p.append(label(x + 18, ny + 46, "L_{bond}", size=12))
        p.append(part("box", x, ny + 80, x, ny + 160, body=40))
        p.append(label(x + 28, ny + 126, "Z_{term %s}" % name, bold=True, size=13))
        p.append(ground(x, ny + 160))
    p.append(label(20, 440, "Equal terminations: no current crosses the nanowire. A mismatch sends part of the pickup through it.", size=13))
    p.append(label(20, 462, "Values: I_{inj} = 44.5 µA (E2) / 28.6 µA (E1), L_{bond} = 2 nH [verify], L_{k} = 3.10 µH (A30), 5.94 µH (B60).", size=13))
    # the cases tried in sim 19
    p.append(panel_title(20, 500, "Terminations tried: Z_{term A} / Z_{term B}"))
    rows = ["case 1:  50 Ω line  /  short",
            "case 2:  50 Ω ∥ shunt C  /  short",
            "case 3:  50 Ω ∥ C  /  C·(1+m)",
            "case 4:  50 Ω ∥ series L-C trap at 28 MHz  /  short",
            "case 5:  50 Ω  /  50 Ω·(1+m)"]
    for i, r in enumerate(rows):
        p.append(label(30, 525 + 20 * i, r, size=13))
    return 720, 640, p


# ------------------------------------------------------------------ figure 8: grounding and return current (sim 10c)
def fig_grounding():
    p = []
    p.append(panel_title(20, 28, "Mirror strip: pickup flows to ground through its own resistance"))
    xs = [110, 230, 350, 470]
    ry, sy = 70, 190
    p.append(wire((60, ry), (xs[-1] + 40, ry)))
    p.append(label(60, ry - 12, "RF rail, V at 28 MHz", size=12, color=GREY))
    for i, x in enumerate(xs):
        p.append(part("cap", x, ry, x, sy, body=12))
        p.append(dot(x, sy))
        p.append(arrow(x + 16, sy - 40, x + 16, sy - 12, width=1.5))
    p.append(label(xs[0] - 22, 135, "c_{p} per length", anchor="end", size=12))
    for i in range(len(xs) - 1):
        p.append(part("res", xs[i], sy, xs[i + 1], sy, dash=True, body=40))
    p.append(label((xs[1] + xs[2]) / 2, sy + 28, "r_{p} per length (Al strip)", anchor="middle", size=12, color=RED))
    # tail to via
    p.append(part("res", xs[-1], sy, 600, sy, dash=True, body=30))
    p.append(label(535, sy + 28, "tail to via", anchor="middle", size=12, color=RED))
    p.append(dot(600, sy))
    p.append(label(612, sy - 10, "ground via", size=12))
    # bond wire to carrier ground
    p.append(part("ind", 600, sy, 600, sy + 80, body=34))
    p.append(label(618, sy + 46, "bond wire 2 nH\nωL = 0.352 Ω", size=12))
    p.append(ground(600, sy + 80))
    # detector end
    p.append(label(xs[0], sy + 52, "detector end", anchor="middle", size=12, bold=True))
    p.append(label(xs[0], sy + 70, "v_{m} = 30.19 mV (3e-08 Ω·m)", anchor="middle", size=12))
    p.append(label(xs[0], sy + 86, "40.25 mV (4e-08 Ω·m)", anchor="middle", size=12))
    p.append(label(20, 330, "The strip carries i_{mirror} = 3.194 mA to ground. Its resistance (T10 four-point test: 18.8 / 25.1 Ω)", size=13))
    p.append(label(20, 352, "lifts the detector end by v_{m}; dissipation 33.93 / 45.23 µW.", size=13))
    return 740, 370, p


FIGS = [
    ("01_chip_capacitor.svg", fig_chip_capacitor),
    ("02_resonator.svg", fig_resonator),
    ("03_loss.svg", fig_loss),
    ("05_pickup.svg", fig_pickup),
    ("06_dc_filter.svg", fig_dc_filter),
    ("07a_snspd_readout.svg", fig_snspd_readout),
    ("07b_lead_termination.svg", fig_lead_termination),
    ("08_grounding.svg", fig_grounding),
]

if __name__ == "__main__":
    for name, fn in FIGS:
        w, h, parts = fn()
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg(w, h, parts))
        print("wrote", path)
