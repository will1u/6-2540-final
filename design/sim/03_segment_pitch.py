"""03 - Outer DC segment pitch: how wide should the segments be for control at h = 50 um?

For several segment widths (pitch = width + 5 um gap), the ion is put above the middle of one
segment (y = 0) and the DC problem is solved with all DC electrodes (segments, centre DC, caps):

  confinement set : E = 0, d2phi/dxdz = 0, axial f = 1 MHz        -> max |V|
  shim sets       : uniform 100 V/m along x, y or z, with no change of curvature -> max |V|
  tilt set        : d2phi/dxdz giving a 10 deg rotation of the radial axes (for cooling both
                    radial modes with an in-plane beam) -> max |V|
  conditioning    : normalised singular values of the 5-row control matrix

Gapless 'midline' model (step 2 showed < 0.1 um difference to the device stack) to keep it fast.
Outputs: sim/out/03_segment_pitch/summary.json, pitch.png
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes

import trapcalc as tc
import trapgeom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "03_segment_pitch")
os.makedirs(OUT, exist_ok=True)
V_RF, F_RF, F_AX = 53.0, tc.F_RF, 1.0e6
m = tc.M_BA138


def rows_of(T, names):
    return np.array([[T[n][1][0], T[n][1][1], T[n][1][2], T[n][2][0, 2], T[n][2][1, 1]]
                     for n in names]).T                        # (5, n), per-um units


def solve(A, b):
    """Minimum-norm voltages for A v = b (rows normalised)."""
    rs = np.linalg.norm(A, axis=1)
    return np.linalg.lstsq(A / rs[:, None], b / rs, rcond=None)[0]


results = []
for seg_w in (45.0, 70.0, 95.0, 145.0, 195.0):
    pitch = seg_w + 5.0
    n_seg = 9
    P = dict(seg_w=seg_w, n_seg=n_seg, seg_x0=-(n_seg * pitch - 5.0) / 2, half_len=1500.0)
    stem = os.path.join(OUT, f"pitch{int(pitch)}")
    gds, js, info = trapgeom.write(stem, P, gap_model="midline")
    els = build_electrodes(gds, Layout.from_json(js), ion_box=(-20, 20, -300, 300), ion_z=(30, 80))
    p = np.array([0.0, 0.0, 50.0])
    from gds2itvg.analysis import rf_null
    r = rf_null(els, ["1"], y=0.0, z_range=(20, 150))
    p = np.array([r["x"], 0.0, r["z"]])
    T = tc.taylor_all(els, p)
    dc = [n for n in els if n != "1"]
    A = rows_of(T, dc)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    _, _, Kpsi = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    curv_ax = (m * (2 * np.pi * F_AX) ** 2 - Kpsi[1, 1]) / tc.E / 1e12   # V/um^2 needed
    sv = np.linalg.svd(A / np.linalg.norm(A, axis=1)[:, None], compute_uv=False)
    v_conf = solve(A, np.array([0, 0, 0, 0, curv_ax]))
    shim = {}
    for i, ax in enumerate("xyz"):
        b = np.zeros(5)
        b[i] = -100e-6        # E = -grad(phi): 100 V/m = 1e-4 V/um
        shim[ax] = float(np.abs(solve(A, b)).max())
    # tilt: in the x-z block of the total Hessian, rotate by 10 deg -> off-diagonal needed
    K_rad = Kpsi[np.ix_([0, 2], [0, 2])] + tc.E * 1e12 * np.array(
        [[sum(v * T[n][2][0, 0] for v, n in zip(v_conf, dc)), 0], [0, sum(v * T[n][2][2, 2] for v, n in zip(v_conf, dc))]])
    dk = K_rad[1, 1] - K_rad[0, 0]
    kxz = 0.5 * np.tan(2 * np.deg2rad(10)) * dk / tc.E / 1e12       # V/um^2
    v_tilt = solve(A, np.array([0, 0, 0, kxz, 0]))
    res = dict(pitch=pitch, seg_w=seg_w, null_z=r["z"], sv_norm=(sv / sv.max()).round(4).tolist(),
               vmax_confine_1MHz=float(np.abs(v_conf).max()), vmax_shim_100Vpm=shim,
               vmax_tilt_10deg=float(np.abs(v_tilt).max()))
    results.append(res)
    print(f"pitch {pitch:5.0f} um: |V| 1 MHz axial {res['vmax_confine_1MHz']:.2f} V; shim x/y/z "
          f"{shim['x']:.3f}/{shim['y']:.3f}/{shim['z']:.3f} V; tilt {res['vmax_tilt_10deg']:.2f} V; "
          f"sigma_min/max {sv.min()/sv.max():.3f}")

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(results, fh, indent=1)
pp = [r["pitch"] for r in results]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(pp, [r["vmax_confine_1MHz"] for r in results], "o-", label="1 MHz axial confinement")
ax.plot(pp, [r["vmax_tilt_10deg"] for r in results], "s-", label="10 deg radial tilt")
for k, mk in zip("xyz", "^v<"):
    ax.plot(pp, [10 * r["vmax_shim_100Vpm"][k] for r in results], mk + "--", label=f"{k} shim 1 kV/m")
ax.set(xlabel="outer segment pitch (um)", ylabel="max |V| (V)", yscale="log",
       title="DC voltage needed vs segment pitch (h = 50 um, 138Ba+)")
ax.legend(fontsize=7)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pitch.png"), dpi=150)
