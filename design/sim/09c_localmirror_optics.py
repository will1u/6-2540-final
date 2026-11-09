"""09c - NbN absorption at 493 nm for the v4 local-mirror stack (Claude-authored; DESIGN_LOG step 26).

v4 removes the 10 um D2, so vacuum sits directly on the SiO2 cap over the readout window:

  vacuum / SiO2 cap / NbN wires (7 nm, f = 0.65, v3.1) / SiO2 spacer / Al 150 nm / thermal SiO2 1 um / Si

With vacuum above, the cap/vacuum interface is part of the cavity again, so the cap thickness is a tuning
knob (09: the etched-window stack). This script
  1. evaluates the current v4 thicknesses (spacer 238, cap 80 nm),
  2. finds the best cap for the fixed 238 nm spacer (the spacer also sets the Al-to-NbN distance),
  3. finds the best (spacer, cap) pair for a 1st-order (40-130 nm) and 2nd-order (180-300 nm) spacer,
  4. reports the +-10 nm box mean and worst corner of each, and
  5. compares with the v3.1 baseline (10 um D2 above the cap, fringe-averaged as in 09b).
Normal incidence, unpolarised (average of E across / along the wires). 09 showed the ion's emission cone
changes the result by < 1 %. Effective-medium model, not RCWA: treat as ~10 % pessimistic (09, Hampel check).
Transfer-matrix and effective-medium functions copied from 09b (09 and 09b run their studies at import).

Outputs: sim/out/09c_localmirror_optics/summary.json, cap_scan.png
Run:     ./run.sh 09c_localmirror_optics.py
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "09c_localmirror_optics")
os.makedirs(OUT, exist_ok=True)
LAM = 493.0
NK = dict(SiO2=1.463, Si=4.333 + 0.048j, Al=0.605 + 5.245j, NbN=2.109 + 1.997j)   # same sources as 09
T_NBN, FILL, T_AL, T_THERM, T_D2 = 7.0, 0.65, 150.0, 1000.0, 10000.0


def iso(n, d):
    e = n ** 2
    return (e, e, e, d)


def wires(nw, nh, f, d):
    ew, eh = nw ** 2, nh ** 2
    return (1.0 / (f / ew + (1 - f) / eh), f * ew + (1 - f) * eh, f * ew + (1 - f) * eh, d)


def tmm_A(layers, lam, n_sub, pol_plane):
    """Normal-incidence absorbed fraction per layer, light from vacuum (copy of 09b)."""
    k0 = 2 * np.pi / lam
    pick = (lambda ex, ey: ey) if pol_plane == "xz" else (lambda ex, ey: ex)
    eta_sub = np.sqrt(n_sub ** 2 + 0j)
    E, H = 1.0 + 0j, eta_sub
    flux = [np.real(E * np.conj(H))]
    for ex, ey, ez, d in reversed(layers):
        kz = np.sqrt(pick(ex, ey) + 0j)
        kz = np.where(kz.imag < 0, -kz, kz)
        c, s = np.cos(k0 * kz * d), np.sin(k0 * kz * d)
        E, H = c * E - 1j * s / kz * H, -1j * kz * s * E + c * H
        flux.append(np.real(E * np.conj(H)))
    flux = flux[::-1]
    a_in = (E + H) / 2
    return [(flux[j] - flux[j + 1]) / np.abs(a_in) ** 2 for j in range(len(layers))]


def A_v4(t_sp, t_cap):
    """NbN absorption, vacuum directly above the cap (v4)."""
    layers = [iso(NK["SiO2"], t_cap), wires(NK["NbN"], NK["SiO2"], FILL, T_NBN), iso(NK["SiO2"], t_sp),
              iso(NK["Al"], T_AL), iso(NK["SiO2"], T_THERM)]
    return float(np.mean([tmm_A(layers, LAM, NK["Si"], p)[1] for p in ("xz", "yz")]))


def A_v3(t_sp, t_cap):
    """NbN absorption under 10 um D2 (v3.1 baseline), averaged over one D2 fringe as in 09b."""
    vals = []
    for k in range(12):
        d2 = T_D2 + k * LAM / (2 * NK["SiO2"]) / 12
        layers = [iso(NK["SiO2"], d2 + t_cap), wires(NK["NbN"], NK["SiO2"], FILL, T_NBN), iso(NK["SiO2"], t_sp),
                  iso(NK["Al"], T_AL), iso(NK["SiO2"], T_THERM)]
        vals.append(np.mean([tmm_A(layers, LAM, NK["Si"], p)[1] for p in ("xz", "yz")]))
    return float(np.mean(vals))


def tolerance(f, t_sp, t_cap):
    """+-10 nm on spacer and cap, independently: box mean (uniform errors, 5 x 5 grid) and worst corner."""
    grid = [f(t_sp + d1, t_cap + d2) for d1 in np.linspace(-10, 10, 5) for d2 in np.linspace(-10, 10, 5)]
    corners = [f(t_sp + d1, t_cap + d2) for d1 in (-10, 10) for d2 in (-10, 10)]
    return float(np.mean(grid)), float(min(corners))


res = {}
res["v3.1_baseline_238_80"] = dict(A=A_v3(238.0, 80.0), spacer=238.0, cap=80.0)
res["v4_current_238_80"] = dict(A=A_v4(238.0, 80.0), spacer=238.0, cap=80.0)
caps = np.arange(20.0, 320.0, 1.0)
scan238 = np.array([A_v4(238.0, c) for c in caps])
k = int(np.argmax(scan238))
res["v4_best_cap_spacer238"] = dict(A=float(scan238[k]), spacer=238.0, cap=float(caps[k]))
for order, sp_range in (("1st", np.arange(40.0, 131.0, 2.0)), ("2nd", np.arange(180.0, 301.0, 2.0))):
    best = (-1.0, None)
    for t_sp in sp_range:
        for t_cap in np.arange(20.0, 320.0, 2.0):
            a = A_v4(t_sp, t_cap)
            if a > best[0]:
                best = (a, (float(t_sp), float(t_cap)))
    res[f"v4_best_{order}_order"] = dict(A=best[0], spacer=best[1][0], cap=best[1][1])
for key, r in res.items():
    f = A_v3 if key.startswith("v3") else A_v4
    r["box_mean_pm10"], r["worst_pm10"] = tolerance(f, r["spacer"], r["cap"])
    print(f"{key:24s} A = {r['A']:.3f} at spacer {r['spacer']:.0f}, cap {r['cap']:.0f} nm; "
          f"+-10 nm box mean {r['box_mean_pm10']:.3f}, worst corner {r['worst_pm10']:.3f}")
# contiguous cap band around the optimum that keeps A within 0.02 of the best (A repeats every
# lambda / 2n = 168 nm of cap, so the next band sits ~168 nm higher)
ok = scan238 >= scan238.max() - 0.02
lo = hi = k
while lo > 0 and ok[lo - 1]:
    lo -= 1
while hi < len(caps) - 1 and ok[hi + 1]:
    hi += 1
res["v4_spacer238_cap_band_within_0.02"] = [float(caps[lo]), float(caps[hi])]
print(f"spacer 238: cap {caps[lo]:.0f}-{caps[hi]:.0f} nm keeps A within 0.02 of the best (repeats every 168 nm)")
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1)

plt.figure(figsize=(6.5, 4))
plt.plot(caps, scan238, label="v4: vacuum above the cap, spacer 238 nm")
plt.axhline(res["v3.1_baseline_238_80"]["A"], color="0.4", ls="--", label="v3.1: 10 um D2 above (fringe avg)")
plt.axvline(80, color="C3", lw=0.8, ls=":", label="current cap 80 nm")
plt.xlabel("SiO2 cap thickness (nm)")
plt.ylabel("NbN absorption at 493 nm")
plt.title("09c: v4 local-mirror window, f = 0.65 (EMT, normal incidence)")
plt.grid(alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cap_scan.png"), dpi=150)
