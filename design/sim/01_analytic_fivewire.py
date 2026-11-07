"""01 - Analytic (gapless, infinitely long) five-wire design for 138Ba+ at h = 50 um.

What it does
  1. Height vs collection vs heating trade-off: for square SNSPDs of side s centred under the ion,
     the fraction of 493 nm photons hitting the detector vs ion height h, next to the relative
     heating rate ~ h^-4 (Brownnutt et al., RMP 87, 1419 (2015), Sec. on distance scaling).
  2. Geometry sweep at fixed h = 50 um: for each centre-DC width c, the RF rail width a that puts
     the RF null at 50 um (h = sqrt(x1 x2), x1/x2 = inner/outer RF-gap midlines), then the trap
     depth and the RF voltage needed for a chosen radial frequency at the chosen drive frequency.
     Model: strips in a grounded plane (House, PRA 78, 033402 (2008); Wesenberg PRA 78 063410).

Outputs: sim/out/01_analytic_fivewire/*.png and summary.json
Run:     <electrode env python> 01_analytic_fivewire.py
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "01_analytic_fivewire")
os.makedirs(OUT, exist_ok=True)

H_TARGET = 50.0      # um, ion height (William's choice)
GAP = 5.0            # um, electrode gap (aspect ratio >= 1 with ~6 um plated Au)
F_RF = tc.F_RF       # Hz
F_RADIAL = 3.0e6     # Hz, target RF-only radial frequency
DET_SIDES = [20.0, 30.0, 40.0, 60.0]   # um, square detector sides to compare

# ------------------------------------------------------------------ 1. height trade-off
hs = np.linspace(25, 120, 96)
fig, ax1 = plt.subplots(figsize=(6.5, 4))
coll = {}
for s in DET_SIDES:
    coll[s] = np.array([tc.collection_fraction(h, s, s, "sigma") for h in hs])
    ax1.plot(hs, 100 * coll[s], label=f"{s:.0f} um square SNSPD")
ax1.set_xlabel("ion height h (um)")
ax1.set_ylabel("photons on detector (%)  [sigma dipole, axis along z]")
ax1.axvline(H_TARGET, color="0.4", ls="--", lw=0.8)
ax2 = ax1.twinx()
ax2.semilogy(hs, (hs / H_TARGET) ** -4, color="k", lw=1.2, ls=":", label="heating ~ h^-4 (rel. to 50 um)")
ax2.set_ylabel("relative heating rate")
ax2.grid(False)
l1, n1 = ax1.get_legend_handles_labels()
l2, n2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, n1 + n2, fontsize=8, loc="upper right")
ax1.set_title("collection vs heating (dipole emission onto a square below the ion)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "height_tradeoff.png"), dpi=150)

i50 = int(np.argmin(np.abs(hs - H_TARGET)))
tradeoff = {f"{s:.0f}um": {"h40": float(np.interp(40, hs, coll[s])),
                            "h50": float(coll[s][i50]),
                            "h70": float(np.interp(70, hs, coll[s]))} for s in DET_SIDES}

# ------------------------------------------------------------------ 2. geometry sweep at h = 50
cs = np.linspace(20, 120, 101)          # centre DC metal width
rows = []
zz = np.linspace(1, 600, 6000)
for c in cs:
    x1 = c / 2 + GAP / 2
    x2 = H_TARGET ** 2 / x1             # h^2 = x1 x2
    a = x2 - x1 - GAP                   # RF metal width
    if a < 10:
        continue
    assert abs(tc.fivewire_null_height(c, a, GAP) - H_TARGET) < 1e-9
    # field along the vertical through the null (x = 0): only Ez is non-zero by symmetry
    d = 1e-3
    phi = lambda x, z: tc.fivewire_rf_phi(x, z, c, a, GAP)
    Ez = (phi(0, zz + d) - phi(0, zz - d)) / (2 * d)
    # Hessian at the null (x-z block; y has no curvature in the infinite model)
    h0 = H_TARGET
    hxx = (phi(d, h0) - 2 * phi(0, h0) + phi(-d, h0)) / d ** 2
    hzz = (phi(0, h0 + d) - 2 * phi(0, h0) + phi(0, h0 - d)) / d ** 2
    H = np.diag([hxx, 0.0, hzz])
    # V_RF giving the target radial frequency: f scales linearly with V
    f1, q1, _ = tc.rf_hessian_to_freqs(H, v_rf=1.0, f_rf=F_RF)
    v_rf = F_RADIAL / f1[np.argmax(f1)]
    f, q, _ = tc.rf_hessian_to_freqs(H, v_rf=v_rf, f_rf=F_RF)
    psi = tc.pseudo_eV(np.column_stack([np.zeros_like(zz), np.zeros_like(zz), Ez]), v_rf, F_RF)
    above = zz > h0
    k = np.argmax(np.where(above, psi, -1))
    rows.append(dict(c=c, a=a, v_rf=v_rf, q=float(q.max()), depth_meV=1e3 * float(psi[k]),
                     z_escape=float(zz[k]), depth_per_V2=float(psi[k]) / v_rf ** 2))

c_arr = np.array([r["c"] for r in rows])
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
axs[0].plot(c_arr, [r["a"] for r in rows])
axs[0].set(xlabel="centre DC width c (um)", ylabel="RF rail width a (um)", title=f"a for h = {H_TARGET:g} um, gap {GAP:g} um")
axs[1].plot(c_arr, [r["v_rf"] for r in rows])
axs[1].set(xlabel="c (um)", ylabel="V_RF (V, 0-pk)", title=f"V for f_rad = {F_RADIAL/1e6:g} MHz at {F_RF/1e6:g} MHz drive")
axs[2].plot(c_arr, [r["depth_meV"] for r in rows])
axs[2].set(xlabel="c (um)", ylabel="trap depth (meV)", title="pseudopotential depth at that V_RF")
for a_ in axs:
    a_.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "geometry_sweep.png"), dpi=150)

# Pick: the c with the largest depth at fixed f_rad, then check c leaves room for a window.
best = max(rows, key=lambda r: r["depth_meV"])
# Candidate with a wider centre electrode (room for a ~30 um window + margins)
wide = min(rows, key=lambda r: abs(r["c"] - 60.0))
summary = dict(h_target_um=H_TARGET, gap_um=GAP, f_rf_MHz=F_RF / 1e6, f_radial_MHz=F_RADIAL / 1e6,
               max_depth_design=best, c60_design=wide, tradeoff=tradeoff)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)

print(f"h = {H_TARGET} um, gap {GAP} um, drive {F_RF/1e6} MHz, radial target {F_RADIAL/1e6} MHz")
print("max-depth geometry: c = {c:.1f}, a = {a:.1f} um, V_RF = {v_rf:.1f} V, q = {q:.3f}, depth = {depth_meV:.1f} meV".format(**best))
print("c ~ 60 geometry:    c = {c:.1f}, a = {a:.1f} um, V_RF = {v_rf:.1f} V, q = {q:.3f}, depth = {depth_meV:.1f} meV".format(**wide))
for s, d in tradeoff.items():
    print(f"collection {s}: h40 {100*d['h40']:.2f}%  h50 {100*d['h50']:.2f}%  h70 {100*d['h70']:.2f}%")

print("\n   c      a    V_RF   depth(meV)")
for r in rows:
    if abs(r["c"] - round(r["c"] / 10) * 10) < 1e-6:
        print(f"{r['c']:5.0f} {r['a']:6.1f} {r['v_rf']:6.1f} {r['depth_meV']:8.1f}")
