"""06 - Detector / window size: collection vs window perturbation vs nanowire length.

The window in the centre DC electrode (width limited to c - 2*5 um = 30 um radially so 5 um Au rims
remain) is the optical aperture. v3: the window floor is bare D2 SiO2 (no ITO); the aperture is the
bottom of the 6 um Au, so the ion-to-aperture distance is h + 6 um. Light then crosses 10 um of SiO2
(n = 1.46) to the NbN and spreads 2.6 um (A30) to 3.9 um (B60) past the window edge, so a window-sized
meander misses ~20 % of it (sim/15, DESIGN_LOG step 24). The v3.1 meander therefore runs past the window:
3 um axially for windows up to 30 um (4.5 um above), 1 um radially (sim/10 v3.1 scan).

Collection = isotropic solid angle of the aperture (trapcalc.collection_fraction, 'iso': Ba+ 493 nm
P1/2 -> S1/2 emission is isotropic, sim/15 part A; v3 used 'sigma', kept here as a column for
comparison) x NbN absorption (sim/15 part C: ~0.54 at f = 0.65) - here only the geometric part.
Window perturbation (RF null drop, axial RF gradient) from the 3-D FD runs in 04b, bare-SiO2 window floor
(04b_oxide_log.txt).
Nanowire: 130 nm wide, 200 nm pitch, Lk ~ 70 pH/sq (7 nm NbN, Rs ~ 400 Ohm/sq, Tc ~ 7.9 K; dirty BCS,
sim/15 part E), reset time tau = L / 50 Ohm.
"""

import json
import os

import numpy as np

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "06_detector_size")
os.makedirs(OUT, exist_ok=True)
H = 50.0
DEPTH_AP = 6.0
LK_SQ = 70e-12
W, P = 0.13, 0.2
OVH_Y = 1.0
FD = {(30, 30): dict(dh=-1.38, grad=1.55e-4), (30, 60): dict(dh=-2.50, grad=2.93e-4)}   # 04b, bare-SiO2 floor

rows = []
for wy, wx in ((20, 20), (30, 30), (30, 45), (30, 60)):
    h_eff = H + FD.get((wy, wx), {}).get("dh", 0.0)
    f = tc.collection_fraction(h_eff + DEPTH_AP, wx, wy, "iso")
    f_sigma = tc.collection_fraction(h_eff + DEPTH_AP, wx, wy, "sigma")
    lx = wx + 2 * (3.0 if wx <= 30 else 4.5)
    n = int(round((wy + 2 * OVH_Y) / P))
    n += n % 2
    length_um = n * lx
    L = length_um / W * LK_SQ
    rows.append(dict(window_axial=wx, window_radial=wy, collection_pct=100 * f, collection_sigma_pct=100 * f_sigma,
                     meander_um=[lx, wy + 2 * OVH_Y], wire_length_mm=length_um / 1000, L_uH=L * 1e6,
                     tau_ns=L / 50 * 1e9, dh_um=FD.get((wy, wx), {}).get("dh"),
                     axial_grad=FD.get((wy, wx), {}).get("grad")))
    r = rows[-1]
    print(f"window {wx:3.0f} x {wy:2.0f} um: geometric collection {r['collection_pct']:.2f} % "
          f"(sigma pattern {r['collection_sigma_pct']:.2f} %), meander {lx:g} x {wy + 2 * OVH_Y:g} um, wire "
          f"{r['wire_length_mm']:.1f} mm, L = {r['L_uH']:.1f} uH, reset ~{r['tau_ns']:.0f} ns, "
          f"dh = {r['dh_um']}, max axial grad = {r['axial_grad']}")
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(rows, fh, indent=1)
