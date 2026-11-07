"""02 - Baseline five-wire (no window) simulated with gds2itvg, checked against the analytic model.

Builds the trapgeom.BASE geometry (c = 40, a = 84, g = 5 um, 16+16 outer segments) and, for the
gapless 'midline' model and the device-stack 'profile' model (6 um Au, SiO2 eps 3.9, Al ground
10 um below), finds:
  - RF null height along the axis,
  - RF-only radial frequencies and Mathieu q at V_RF, F_RF,
  - pseudopotential depth (escape point straight up; the five-wire saddle sits on the vertical),
and compares with 01 (House-model numbers at c=40: h = 50 um, V ~ 53 V, depth ~ 52 meV).

Outputs: sim/out/02_baseline/  (gds, json, labels.png, null_height.png, summary.json)
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes, unit_potentials
from gds2itvg.analysis import rf_null
from gds2itvg.plot import label_map

import trapcalc as tc
import trapgeom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "02_baseline")
os.makedirs(OUT, exist_ok=True)
V_RF = 53.0
F_RF = tc.F_RF
Y_SCAN = np.linspace(-1500, 1000, 11)   # axial positions (ITVG y = GDS x)

gds, js, info = trapgeom.write(os.path.join(OUT, "baseline"))
summary = {}
for model in ("midline", "profile"):
    lay = Layout.from_json(js)
    lay.gap_model = model
    els, gnd = build_electrodes(gds, lay, ion_box=(-30, 30, -1600, 1100), ion_z=(30, 200),
                                return_ground=True)
    if model == "profile":
        label_map(els, os.path.join(OUT, "labels.png"), ground=gnd,
                  ion_box=(-30, 30, -1600, 1100), title="baseline: electrode numbers")
    nulls = [rf_null(els, ["1"], y=float(y), z_range=(20, 150)) for y in Y_SCAN]
    ion = rf_null(els, ["1"], y=0.0, z_range=(20, 150))
    p = np.array([ion["x"], 0.0, ion["z"]])
    T = tc.taylor_all(els, p)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    f, q, _ = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    # depth: pseudopotential along the vertical through the null
    zz = np.linspace(ion["z"] - 30, 400, 1500)
    d = 0.05
    pts = np.column_stack([np.full_like(zz, ion["x"]), np.zeros_like(zz), zz])
    up = unit_potentials({"1": els["1"]}, pts + [0, 0, d])["1"]
    dn = unit_potentials({"1": els["1"]}, pts - [0, 0, d])["1"]
    psi = tc.pseudo_eV(np.column_stack([0 * zz, 0 * zz, (up - dn) / (2 * d)]), V_RF, F_RF)
    k = np.argmax(np.where(zz > ion["z"], psi, -1))
    summary[model] = dict(null_z=ion["z"], null_x=ion["x"],
                          null_z_along_axis=[(float(y), r["z"]) for y, r in zip(Y_SCAN, nulls)],
                          f_rf_only_MHz=sorted((f / 1e6).round(3).tolist()), q=float(q.max()),
                          depth_meV=1e3 * float(psi[k]), z_escape=float(zz[k]))
    print(f"[{model}] null z = {ion['z']:.2f} um (x = {ion['x']:.3f}); RF-only freqs "
          f"{np.sort(f)/1e6} MHz; q = {q.max():.3f}; depth = {1e3*psi[k]:.1f} meV at z = {zz[k]:.0f}")
    plt.plot(Y_SCAN, [r["z"] for r in nulls], "o-", label=model)

plt.xlabel("axial position y (um)")
plt.ylabel("RF null height (um)")
plt.title("baseline five-wire: null height along the trap")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig(os.path.join(OUT, "null_height.png"), dpi=150)
summary["analytic_01"] = dict(h=50.0, v_rf=53.0, depth_meV=51.9)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
