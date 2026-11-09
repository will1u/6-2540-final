"""18 - E1 (0.35 um lift-off Au) vs E2 (6 um plated Au): one comparison table (Claude-authored).

Compares the two electrode options on what depends on the Au thickness and on the layout squares:
  Part 1  Au sheet resistance and skin depth at 28 MHz
  Part 2  squares and resistance of each Au conductor (geometry copied from gds/make_chip.py)
  Part 3  RF heating of the feed lead and one rail (upper bound)
  Part 4  SNSPD slot-lead resistance and the 50 ohm readout factor
  Part 5  screening of exposed SiO2 at the bottom of a gap (lowest-mode estimate only)
  Part 6  numbers already simulated, quoted from the design log (not recomputed here)

No electrode option is recommended here. Inputs tagged [verify] are assumptions still to be checked.
Outputs in out/18_e1_vs_e2/: compare.md (the table) and summary.json (rows, checks, verify list).
Run from design/sim: ./run.sh 18_e1_vs_e2.py
"""

import json
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "18_e1_vs_e2")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ inputs
# Au thicknesses (m). E1 = 0.35 um lift-off, E2 = 6 um electroplated (make_chip.py STACKS; LOCAL_MIRROR.md H.4)
T_AU = {"E1": 0.35e-6, "E2": 6e-6}
# Room-temperature resistivity (ohm m): bulk Au at 20 C, and a thin evaporated film [verify both]
RHO_RT = {"bulk": 2.44e-8, "film": 4.0e-8}
# Residual resistance ratio for 4 K, rho_4K = rho_RT / RRR [verify]
RRR = [2, 5, 10]
# RF drive: 28 MHz, 53 V amplitude (DESIGN_LOG step 25; sim 12)
F_RF = 28e6
V_RF = 53.0
# Chip RF capacitance has not been computed [verify]
C_RF = [1e-12, 2e-12, 5e-12]
MU0 = 4e-7 * math.pi                   # H/m
R_READ = 50.0                          # ohm, readout line

# ------------------------------------------------------------------ geometry (um), copied from gds/make_chip.py
XRF0, XRF1 = -2000.0, 2000.0           # make_chip.py XRF0, XRF1: RF rails
A_RAIL = 84.0                          # make_chip.py A: rail width
U_BAR = 60.0                           # make_chip.py U_BAR
X_RFPAD = 4700.0                       # make_chip.py X_RFPAD
W_FEED = 60.0                          # make_chip.py: RF feed lead width (path width 60.0)
X_READ = 240.0                         # make_chip.py X_READ
WIN_WX, OVH_X = 30.0, 3.0              # make_chip.py WIN_WX (A30), OVH_X
DET_WX = WIN_WX + 2 * OVH_X            # NbN line length, 36 um (A30)
X_TAB = X_READ - DET_WX / 2 - 27.0     # make_chip.py X_TAB (= 195)
X_SLOT_END = X_TAB - 20.0              # make_chip.py X_SLOT_END (= 175)
X_LEAD_END = X_SLOT_END - 5.0          # make_chip.py X_LEAD_END, G = 5 (= 170)
X_BEND = -4400.0                       # make_chip.py X_BEND: leads turn out to their pads here
W_SLOT_LEAD = 5.0                      # make_chip.py SN_W: SNSPD lead width
X_SNPAD, Y_SNPAD = -4750.0, 100.0      # make_chip.py SNSPD pad (SN pad centre at +Y_SNPAD)
C_DC, SLOT_HALF = 40.0, 12.5           # make_chip.py C, SLOT_HALF
W_CDC = C_DC / 2 - SLOT_HALF           # centre DC lead width, 7.5 um
Y_CDC = (SLOT_HALF + C_DC / 2) / 2     # 16.25, centre line of the top half of the centre DC
# Centre DC lead as drawn in make_chip.py (the path from XRF0 - 40 to the C pad)
CDC_PATH = [(-2040.0, Y_CDC), (-3600.0, Y_CDC), (-3700.0, 450.0), (-4650.0, 450.0)]

# Slot-lead tail to the pad: brief says about 300 um; the drawn path (X_BEND, then 60 um diagonal, then
# to X_SNPAD) is computed here so the table can show both.
TAIL_BRIEF = 300.0
TAIL_DRAWN = math.hypot(60.0, 95.0) + ((X_BEND - 60.0) - X_SNPAD)

# ------------------------------------------------------------------ squares
SQ_RAIL = (XRF1 - XRF0) / A_RAIL                     # one rail (two rails in the die)
SQ_FEED = (X_RFPAD - (XRF1 + U_BAR)) / W_FEED        # 2640 / 60
L_SLOT_BRIEF = (X_LEAD_END - X_BEND) + TAIL_BRIEF
L_SLOT_DRAWN = (X_LEAD_END - X_BEND) + TAIL_DRAWN
SQ_SLOT_BRIEF = L_SLOT_BRIEF / W_SLOT_LEAD
SQ_SLOT = L_SLOT_DRAWN / W_SLOT_LEAD
SQ_CDC_SPAN = (-2040.0 - (-4650.0)) / W_CDC          # span only, 2610 / 7.5
L_CDC_DRAWN = sum(math.hypot(x1 - x0, y1 - y0) for (x0, y0), (x1, y1) in zip(CDC_PATH, CDC_PATH[1:]))
SQ_CDC = L_CDC_DRAWN / W_CDC

# ------------------------------------------------------------------ table
ROWS = []


def row(part, quantity, e1, e2, unit, source):
    ROWS.append({"part": part, "quantity": quantity, "E1": e1, "E2": e2, "unit": unit, "source": source})


def fmt(x, nd=3):
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    if abs(x) < 10 ** (-nd):          # too small for fixed format
        return f"{x:.2e}"
    return f"{x:.{nd}f}"


def both(f, nd=3):
    """Format f(option) for E1 and E2."""
    return fmt(f("E1"), nd), fmt(f("E2"), nd)


# Part 1: Au resistance
P1 = "1 Au resistance"
for lab, rho in RHO_RT.items():
    e1, e2 = both(lambda o: rho / T_AU[o], 4)
    row(P1, f"Rs, room temperature, {lab} rho = {rho:.2e} ohm m", e1, e2, "ohm/sq", "[team calc] rho / t; rho [verify]")
    for n in RRR:
        e1, e2 = both(lambda o: rho / n / T_AU[o], 4)
        row(P1, f"Rs, 4 K, {lab} rho, RRR = {n}", e1, e2, "ohm/sq", "[team calc] rho / (RRR t); RRR [verify]")
row(P1, "Rs(E1) / Rs(E2) (any rho)", fmt(T_AU["E2"] / T_AU["E1"], 2), "-", "ratio", "[team calc] = t(E2) / t(E1) = 6 / 0.35")
for lab, rho in RHO_RT.items():
    delta = math.sqrt(rho / (math.pi * F_RF * MU0))
    row(P1, f"Skin depth at 28 MHz, {lab} rho", fmt(delta * 1e6, 2), fmt(delta * 1e6, 2), "um",
        "[team calc] sqrt(rho / (pi f mu0))")
    row(P1, f"t < skin depth ({lab} rho): DC sheet resistance applies", "yes" if T_AU["E1"] < delta else "no",
        "yes" if T_AU["E2"] < delta else "no", "-", "[team calc]")

# Part 2: squares and resistance of each conductor
P2 = "2 squares"
row(P2, "RF rail, one rail (two rails)", fmt(SQ_RAIL, 2), fmt(SQ_RAIL, 2), "sq", "[team calc] (XRF1 - XRF0) / A")
row(P2, "RF feed lead, 2060 to 4700 at 60 um", fmt(SQ_FEED, 2), fmt(SQ_FEED, 2), "sq", "[team calc] 2640 / 60")
row(P2, "SNSPD slot lead, brief tail (300 um)", fmt(SQ_SLOT_BRIEF, 1), fmt(SQ_SLOT_BRIEF, 1), "sq",
    "[team calc] brief geometry: about 300 um tail")
row(P2, "SNSPD slot lead, drawn tail (402 um)", fmt(SQ_SLOT, 1), fmt(SQ_SLOT, 1), "sq",
    "[team calc] make_chip.py path X_LEAD_END -> X_BEND -> X_SNPAD")
row(P2, "Centre DC lead, x-span -2040 to -4650 at 7.5 um", fmt(SQ_CDC_SPAN, 1), fmt(SQ_CDC_SPAN, 1), "sq",
    "[team calc] span only (brief)")
row(P2, "Centre DC lead, drawn polyline at 7.5 um", fmt(SQ_CDC, 1), fmt(SQ_CDC, 1), "sq",
    "[team calc] make_chip.py path (-2040 -> -3600 -> -3700,450 -> -4650,450)")
for lab, rho in RHO_RT.items():
    for name, sq in (("RF rail (one)", SQ_RAIL), ("RF feed lead", SQ_FEED),
                     ("SNSPD slot lead (drawn)", SQ_SLOT), ("centre DC lead (drawn)", SQ_CDC)):
        e1, e2 = both(lambda o: sq * rho / T_AU[o], 4)
        row(P2, f"R at room temperature, {lab} rho: {name}", e1, e2, "ohm", "[team calc] squares x Rs")

# Part 3: RF heating (upper bound). I = 2 pi f C V. P = 0.5 I^2 R_feed + I^2 R_rail / 12.
# I is the peak amplitude of the total RF current. The feed lead carries all of it: 0.5 I^2 R_feed.
# Each of the two rails carries I/2 at the feed end, falling linearly to 0 at the open end, so one rail
# dissipates 0.5 (I/2)^2 R_rail * integral_0^1 (1 - u)^2 du = I^2 R_rail / 24, and both give I^2 R_rail / 12.
P3 = "3 RF heating"
for c in C_RF:
    I = 2 * math.pi * F_RF * c * V_RF
    row(P3, f"RF current amplitude, C_rf = {c * 1e12:g} pF", fmt(I * 1e3, 3), fmt(I * 1e3, 3), "mA",
        "[team calc] 2 pi f C_rf V; C_rf [verify]")
    for lab, rho in RHO_RT.items():
        for n in RRR:
            cells = {}
            for o in T_AU:
                rs4 = rho / n / T_AU[o]
                p = 0.5 * I * I * SQ_FEED * rs4 + I * I * (SQ_RAIL * rs4) / 12.0
                cells[o] = fmt(p * 1e6, 2)
            row(P3, f"P upper bound, C_rf = {c * 1e12:g} pF, {lab} rho, RRR = {n}", cells["E1"], cells["E2"], "uW",
                "[team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify]")

# Part 4: SNSPD slot lead and the 50 ohm readout
P4 = "4 SNSPD slot lead"
cases = [("room temperature, bulk rho", {o: RHO_RT["bulk"] / T_AU[o] for o in T_AU}),
         ("room temperature, film rho", {o: RHO_RT["film"] / T_AU[o] for o in T_AU})]
for lab, rho in RHO_RT.items():
    for n in RRR:
        cases.append((f"4 K, {lab} rho, RRR = {n}", {o: rho / n / T_AU[o] for o in T_AU}))
for name, rs in cases:
    lead = {o: SQ_SLOT * rs[o] for o in T_AU}
    pair = {o: 2 * lead[o] for o in T_AU}
    fac = {o: R_READ / (R_READ + pair[o]) for o in T_AU}
    e1, e2 = fmt(lead["E1"], 2), fmt(lead["E2"], 2)
    row(P4, f"one lead R, {name}", e1, e2, "ohm", "[team calc] drawn lead squares x Rs")
    e1, e2 = fmt(pair["E1"], 2), fmt(pair["E2"], 2)
    row(P4, f"pair R (two in series), {name}", e1, e2, "ohm", "[team calc]")
    e1, e2 = fmt(fac["E1"], 4), fmt(fac["E2"], 4)
    row(P4, f"50 ohm line: pulse amplitude factor = reset-time factor, {name}", e1, e2, "-",
        "[team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair)")

# Part 5: screening of exposed SiO2 (lowest-mode estimate)
P5 = "5 SiO2 screening"
INF5 = "[inference]: lowest-mode estimate, not a field solve"
for g in (5.0, 10.0, 30.0):
    f = {o: math.exp(-math.pi * T_AU[o] / (g * 1e-6)) for o in T_AU}
    e1, e2 = fmt(f["E1"], 4), fmt(f["E2"], 5)
    row(P5, f"exp(-pi t/g), g = {g:g} um", e1, e2, "-", INF5)
    row(P5, f"E1/E2 ratio, g = {g:g} um", fmt(f["E1"] / f["E2"], 1), "-", "-", INF5)

# Part 6: numbers already simulated, quoted (each confirmed in DESIGN_LOG.md or fab/variants/LOCAL_MIRROR.md)
P6 = "6 quoted simulated numbers"
QUOTED = [
    ("Window null drop, A30", "<= 0.37", "1.19", "um",
     "DESIGN_LOG.md step 25 (E1 is an upper bound from a 1 um pocket)"),
    ("Window null drop, B60", "<= 0.55", "2.04", "um", "DESIGN_LOG.md step 26"),
    ("Micromotion after undoing the drop, 10 deg tilt, A30", "54.88", "173.36", "nm", "DESIGN_LOG.md step 29"),
    ("Micromotion after undoing the drop, 10 deg tilt, B60", "81.46", "290.83", "nm", "DESIGN_LOG.md step 29"),
    ("A30 geometric collection", "2.601-2.636", "2.221", "%", "DESIGN_LOG.md, v4 SNSPD overhang audit"),
    ("Nanowire RF pickup", "1.92", "0.96", "uA", "DESIGN_LOG.md step 26 (10b)"),
    ("RF pickup per slot lead", "28.3", "44.5", "uA", "DESIGN_LOG.md step 28"),
    ("SiO2 gap depth-to-width ratio", "0.07", "1.2", "-", "fab/variants/LOCAL_MIRROR.md H.4"),
    ("DC voltages for zones and transport", "same to 0.01 V", "reference", "V", "DESIGN_LOG.md step 25"),
]
for q, e1, e2, unit, src in QUOTED:
    row(P6, q, e1, e2, unit, "quoted: " + src)

# ------------------------------------------------------------------ acceptance
rs_bulk = {o: RHO_RT["bulk"] / T_AU[o] for o in T_AU}
ratio = rs_bulk["E1"] / rs_bulk["E2"]
delta_bulk = math.sqrt(RHO_RT["bulk"] / (math.pi * F_RF * MU0))
f5 = {o: math.exp(-math.pi * T_AU[o] / 5e-6) for o in T_AU}
lead_bulk = {o: SQ_SLOT * rs_bulk[o] for o in T_AU}
CHECKS = [
    ("Rs(E1)/Rs(E2) = 17.14", abs(ratio - 17.14) < 0.01, f"{ratio:.3f}"),
    ("exp(-pi t/g), g = 5, E1 = 0.803", round(f5["E1"], 3) == 0.803, f"{f5['E1']:.4f}"),
    ("exp(-pi t/g), g = 5, E2 = 0.0230", abs(f5["E2"] - 0.0230) < 0.0002, f"{f5['E2']:.5f}"),
    ("exp ratio about 35", 33 < f5["E1"] / f5["E2"] < 37, f"{f5['E1'] / f5['E2']:.1f}"),
    ("Rs(E1) bulk RT = 0.0697 ohm/sq", round(rs_bulk["E1"], 4) == 0.0697, f"{rs_bulk['E1']:.5f}"),
    ("one slot lead E1 bulk RT roughly 65-70 ohm", 65 <= lead_bulk["E1"] <= 70, f"{lead_bulk['E1']:.2f}"),
    ("one slot lead E2 bulk RT about 4 ohm", 3.5 <= lead_bulk["E2"] <= 4.5, f"{lead_bulk['E2']:.3f}"),
    ("skin depth at 28 MHz, bulk rho = 14.9 um", abs(delta_bulk * 1e6 - 14.9) < 0.1, f"{delta_bulk * 1e6:.2f}"),
]

VERIFY = [
    "rho_RT bulk 2.44e-8 ohm m (bulk Au at 20 C)",
    "rho_RT thin evaporated film 4.0e-8 ohm m",
    "RRR = 2, 5, 10 (4 K residual resistance ratio)",
    "C_rf = 1, 2, 5 pF (chip RF capacitance not computed)",
    "Slot-lead tail: brief said about 300 um; drawn path is 402 um (both shown)",
    "Centre DC lead: brief span to -4650 (348 sq) vs drawn polyline (394 sq) (both shown)",
]

# ------------------------------------------------------------------ print one table
cols = ["part", "quantity", "E1", "E2", "unit", "source"]
widths = {"part": 22, "quantity": 70, "E1": 14, "E2": 14, "unit": 8, "source": 40}
print(" | ".join(c.ljust(widths[c]) for c in cols))
print("-+-".join("-" * widths[c] for c in cols))
for r in ROWS:
    print(" | ".join(str(r[c])[:widths[c]].ljust(widths[c]) for c in cols))

print("\nAcceptance:")
for name, ok, val in CHECKS:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}  (value {val})")
print(f"Overall: {'PASS' if all(ok for _, ok, _ in CHECKS) else 'FAIL'}")

# ------------------------------------------------------------------ save
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump({"rows": ROWS,
               "checks": [{"check": n, "pass": bool(ok), "value": v} for n, ok, v in CHECKS],
               "verify_inputs": VERIFY}, fh, indent=1)

md = ["# 18 - E1 vs E2 comparison", "",
      "Claude-authored. Written by design/sim/18_e1_vs_e2.py; regenerate rather than edit. "
      "No option is recommended here.", "",
      "| Part | Quantity | E1 | E2 | Unit | Source |", "|---|---|---|---|---|---|"]
for r in ROWS:
    cells = [r["part"], r["quantity"], r["E1"], r["E2"], r["unit"], r["source"]]
    md.append("| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |")
md += ["", "## Acceptance", ""]
md += [f"- {'PASS' if ok else 'FAIL'}: {n} (value {v})" for n, ok, v in CHECKS]
md += ["", "## Inputs tagged [verify]", ""]
md += [f"- {v}" for v in VERIFY]
with open(os.path.join(OUT, "compare.md"), "w") as fh:
    fh.write("\n".join(md) + "\n")
