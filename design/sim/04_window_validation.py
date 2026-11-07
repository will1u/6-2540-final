"""04 - Independent checks of the window physics before trusting 05.

Part A: 2-D finite-difference cross-section (x-z plane, infinitely long along the axis = worst
case for a window). Real stack: 6 um Au electrodes on top of 10 um SiO2 (eps 3.9) over a grounded
plane (Al / ITO) at z = -16 um; vacuum above. RF rails at 1 V, everything else 0 V.
Cases at the readout cross-section:
  full      centre DC electrode present (= no window, or ITO flush on top tied to centre DC)
  pocket30  30 um opening inside the 40 um centre electrode, D2 etched to the grounded ITO floor
  cut_d2    centre electrode removed across its full width, SiO2 left in place (floor = SiO2 at z = -6)
  cut_etch  centre electrode removed across its full width, SiO2 etched to the grounded floor
Reports the RF null height for each (pseudopotential minimum on x = 0).
This checks the gds2itvg 'profile' model (05) against a direct solve, independent of its
gap/opening correction model.

Part B: Todaro-like RF termination (gds2itvg, 3-D): RF rails ending ~80 um past the readout
point. Todaro's thesis (Sec. 4.2.1.2, 6.3) names RF end effects as one cause of their lower ion
height over the detector; this shows the size of that effect for our geometry.

Outputs: sim/out/04_validation/
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "04_validation")
os.makedirs(OUT, exist_ok=True)

C, A, G = 40.0, 84.0, 5.0         # centre width, RF width, gap (um)
T_AU, T_OX, EPS = 6.0, 10.0, 3.9
DX = 0.5
XMAX, ZMIN, ZMAX = 400.0, -(T_AU + T_OX), 400.0


def solve_case(case):
    xs = np.arange(-XMAX, XMAX + DX / 2, DX)
    zs = np.arange(ZMIN, ZMAX + DX / 2, DX)
    nx, nz = len(xs), len(zs)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    eps = np.ones((nx, nz))
    fixed = np.zeros((nx, nz), bool)
    val = np.zeros((nx, nz))
    # dielectric layer below the electrodes, and in the gaps up to the bottom of the metal
    in_ox = (Z < -T_AU) & (Z >= ZMIN)
    eps[in_ox] = EPS
    # grounded plane at the bottom, grounded far boundary
    fixed[:, 0] = True
    fixed[:, -1] = True
    fixed[0, :] = True
    fixed[-1, :] = True
    in_metal_z = (Z >= -T_AU) & (Z <= 0)
    y_rf0, y_rf1 = C / 2 + G, C / 2 + G + A
    rf = in_metal_z & (np.abs(X) >= y_rf0) & (np.abs(X) <= y_rf1)
    outer = in_metal_z & (np.abs(X) >= y_rf1 + G)
    centre = in_metal_z & (np.abs(X) <= C / 2)
    if case == "pocket30":
        centre &= np.abs(X) > 15.0
        etched = (np.abs(X) <= 15.0) & (Z < -T_AU)
        eps[etched] = 1.0
    elif case == "cut_d2":
        centre &= False
    elif case == "cut_etch":
        centre &= False
        etched = (np.abs(X) <= C / 2 + G) & (Z < -T_AU)
        eps[etched] = 1.0
    for m, v in ((rf, 1.0), (outer, 0.0), (centre, 0.0)):
        fixed |= m
        val[m] = v
    # 5-point FD with face-averaged permittivity
    idx = -np.ones((nx, nz), int)
    free = ~fixed
    idx[free] = np.arange(free.sum())
    rows, cols, data = [], [], []
    b = np.zeros(free.sum())
    I, K = np.nonzero(free)
    for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        I2, K2 = I + di, K + dk
        ef = 0.5 * (eps[I, K] + eps[I2, K2])
        rows.append(idx[I, K]); cols.append(idx[I, K]); data.append(-ef)
        nb_free = free[I2, K2]
        rows.append(idx[I, K][nb_free]); cols.append(idx[I2, K2][nb_free]); data.append(ef[nb_free])
        np.add.at(b, idx[I, K][~nb_free], -ef[~nb_free] * val[I2, K2][~nb_free])
    M = sp.csr_matrix((np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))),
                      shape=(free.sum(), free.sum()))
    phi = val.copy()
    phi[free] = spla.spsolve(M, b)
    # RF null on x = 0
    i0 = int(np.argmin(np.abs(xs)))
    above = zs > 5.0
    Ez = np.gradient(phi[i0, :], DX)
    Ex = (phi[i0 + 1, :] - phi[i0 - 1, :]) / (2 * DX)
    g2 = Ez ** 2 + Ex ** 2
    k = np.argmin(np.where(above & (zs < 150), g2, np.inf))
    # sub-grid refine with a parabola through |grad|^2
    if 0 < k < len(zs) - 1:
        y0, y1, y2 = g2[k - 1:k + 2]
        den = y0 - 2 * y1 + y2
        zk = zs[k] + (0.5 * DX * (y0 - y2) / den if den else 0.0)
    else:
        zk = zs[k]
    # escape barrier along the vertical (relative pseudopotential ~ |grad phi|^2)
    k_esc = k + np.argmax(g2[k:np.searchsorted(zs, 300)])
    return dict(case=case, null_z=float(zk), escape_z=float(zs[k_esc]),
                rel_depth=float(g2[k_esc] - g2[k])), (xs, zs, phi)


results = {}
fig, axs = plt.subplots(1, 4, figsize=(16, 3.6))
for ax, case in zip(axs, ("full", "pocket30", "cut_d2", "cut_etch")):
    r, (xs, zs, phi) = solve_case(case)
    results[case] = r
    print(f"[2D] {case:9s} RF null z = {r['null_z']:6.2f} um; relative depth (|grad|^2 at escape) = "
          f"{r['rel_depth']:.3e}")
    sel = (np.abs(xs) < 150)
    zsel = zs < 120
    ax.contourf(xs[sel], zs[zsel], phi[np.ix_(sel, zsel)].T, levels=30, cmap="viridis")
    ax.axhline(r["null_z"], color="r", lw=0.8)
    ax.set(title=f"{case}: null {r['null_z']:.1f} um", xlabel="x (um)", ylabel="z (um)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "crosssection_2d.png"), dpi=130)

# ------------------------------------------------------------------ Part B: RF termination (3-D)
import trapcalc as tc  # noqa: E402
import trapgeom  # noqa: E402
import gdstk  # noqa: E402
from gds2itvg import Layout, build_electrodes  # noqa: E402
from gds2itvg.analysis import rf_null  # noqa: E402

X_END = 80.0          # RF rails end 80 um past the readout point at x = 0
stem = os.path.join(OUT, "rf_termination")
gds, js, info = trapgeom.write(stem, dict(half_len=1500.0, n_seg=9, seg_x0=-447.5), gap_model="profile")
lib = gdstk.read_gds(gds)
cell = lib.top_level()[0]
cut = gdstk.rectangle((X_END, -(C / 2 + G + A + 1)), (1600, C / 2 + G + A + 1))
keep = gdstk.boolean(cell.polygons, cut, "not", layer=trapgeom.LAYER_AU, datatype=0)
# the centre electrode continues; past the rail ends it is flanked by ground-level DC metal
ext = gdstk.rectangle((X_END, -(C / 2 + G + A + 1)), (1500, -(C / 2 + G)))
ext2 = gdstk.rectangle((X_END, C / 2 + G), (1500, C / 2 + G + A + 1))
polys = keep + [gdstk.rectangle((X_END, -C / 2), (1500, C / 2))]
cell.remove(*cell.polygons)
cell.add(*polys)
lib.write_gds(gds)
lay = Layout.from_json(js)
els = build_electrodes(gds, lay, ion_box=(-20, 20, -300, 100), ion_z=(15, 80))
ys = np.linspace(-300, 60, 37)
hz = [rf_null(els, ["1"], y=float(y), z_range=(10, 150))["z"] for y in ys]
results["rf_termination"] = dict(x_end=X_END, y=ys.tolist(), h=hz)
print("[3D] RF rails end at +80 um: null height at y = -300, -100, 0, +40 um: "
      + ", ".join(f"{np.interp(v, ys, hz):.1f}" for v in (-300, -100, 0, 40)))
plt.figure(figsize=(6, 3.5))
plt.plot(ys, hz, "o-")
plt.axvline(X_END, color="0.5", ls="--", label="RF rails end")
plt.xlabel("axial position (um)")
plt.ylabel("RF null height (um)")
plt.title("RF-rail termination near the readout point")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "rf_termination.png"), dpi=150)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(results, fh, indent=1)
