"""06 - Detector / window size: collection vs window perturbation vs nanowire length.

The window in the centre DC electrode (width limited to c - 2*5 um = 30 um radially so 5 um Au rims
remain) is the optical aperture. With the ITO-on-D2 window, the aperture sits 6 um below the
electrode top (bottom of the Au), so the ion-to-aperture distance is h + 6 um; light then crosses
10 um of SiO2 (n = 1.46) to the detector, which spreads the beam footprint by only ~2 um per side,
so a detector the size of the window catches all light through it.

Collection = dipole-weighted solid angle of the aperture (trapcalc.collection_fraction) x NbN
absorption (from 09, ~0.5) - here only the geometric part is computed.
Window perturbation (RF null drop, axial RF gradient) from the 3-D FD runs in 04b.
Nanowire: 100 nm wide, 200 nm pitch, Lk ~ 105 pH/sq (research report: 5 nm NbN, Rs ~ 600 Ohm/sq),
reset time tau = L / 50 Ohm.
"""

import json
import os

import numpy as np

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "06_detector_size")
os.makedirs(OUT, exist_ok=True)
H = 50.0
DEPTH_AP = 6.0
LK_SQ = 105e-12
W, P = 0.1, 0.2
FD = {(30, 30): dict(dh=-1.19, grad=1.35e-4), (30, 60): dict(dh=-2.04, grad=2.45e-4)}   # 04b, ito6

rows = []
for wy, wx in ((20, 20), (30, 30), (30, 45), (30, 60)):
    h_eff = H + FD.get((wy, wx), {}).get("dh", 0.0)
    f = tc.collection_fraction(h_eff + DEPTH_AP, wx, wy, "sigma")
    length_um = wy / P * wx
    L = length_um / W * LK_SQ
    rows.append(dict(window_axial=wx, window_radial=wy, collection_pct=100 * f,
                     wire_length_mm=length_um / 1000, L_uH=L * 1e6, tau_ns=L / 50 * 1e9,
                     dh_um=FD.get((wy, wx), {}).get("dh"), axial_grad=FD.get((wy, wx), {}).get("grad")))
    r = rows[-1]
    print(f"window {wx:3.0f} x {wy:2.0f} um: geometric collection {r['collection_pct']:.2f} %, wire "
          f"{r['wire_length_mm']:.1f} mm, L = {r['L_uH']:.1f} uH, reset ~{r['tau_ns']:.0f} ns, "
          f"dh = {r['dh_um']}, max axial grad = {r['axial_grad']}")
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(rows, fh, indent=1)
