"""04b - 3-D finite-difference check: how much does a *finite* window pocket lower the RF null?

gds2itvg treats all electrodes as coplanar sheets, so a pocket etched 16 um deep under a window
is invisible to it if the window sits inside an RF-grounded electrode (05: no change). The 2-D
cross-section in 04 (infinitely long window = worst case) showed that the depth does matter.
This script solves Laplace's equation in 3-D around the readout zone to get the real, finite-
window effect.

Geometry (um), x radial, y axial, z height; quarter domain x>=0, y>=0 with mirror planes:
  6 um Au electrodes from z = -6 to 0; 10 um SiO2 (eps 3.9) below; grounded plane at z = -16
  (Al ground plane / grounded ITO floor). Centre DC |x| <= 20, RF rails 25..109 at 1 V,
  outer DC beyond 114 at 0 V. Window: no Au for |x| <= wy/2, |y| <= wx/2.
  'etched': SiO2 removed under the window down to the grounded floor (vacuum pocket)
  'oxide' : SiO2 left in place (floor = bare SiO2 at z = -6, ground 10 um below it)
  'ito6'  : SiO2 left in place, ITO on top of it at z = -6 tied to the centre DC (RF ground)
Boundaries: x = XM grounded (outer DC), y = YM mirror (rails continue), z top grounded (far).
Absolute heights depend on the finite box, so every case is compared with the no-window case
solved on the same grid: dh = h(window) - h(no window).

Solver: conjugate gradients with a Jacobi preconditioner on the 7-point stencil with
face-averaged permittivity (symmetric positive definite after sign flip).
Outputs: sim/out/04b_window_3d/summary.json, dh.png
"""

import json
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "04b_window_3d")
os.makedirs(OUT, exist_ok=True)

D = 1.0                                   # grid step (um)
XM, YM, ZB, ZT = 160.0, 160.0, -16.0, 130.0
C, A, G, T_AU, EPS = 40.0, 84.0, 5.0, 6.0, 3.9

xs = np.arange(0, XM + D / 2, D)
ys = np.arange(0, YM + D / 2, D)
zs = np.arange(ZB, ZT + D / 2, D)
nx, ny, nz = len(xs), len(ys), len(zs)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")


def solve(wy, wx, floor):
    eps = np.where(Z < -T_AU, EPS, 1.0)
    metal = (Z >= -T_AU) & (Z <= 0)
    win = (X <= wy / 2) & (Y <= wx / 2) if wx > 0 else np.zeros_like(metal)
    rf = metal & (X >= C / 2 + G) & (X <= C / 2 + G + A)
    gnd = metal & ((X <= C / 2) & ~win | (X >= C / 2 + 2 * G + A))
    if floor == "etched":
        eps = np.where(win & (Z < -T_AU), 1.0, eps)
    if floor == "ito6":
        # ITO sheet on top of the SiO2 at the bottom of the Au window, tied to the centre DC
        # electrode (RF ground): a 6 um deep pocket with a conducting floor
        gnd = gnd | (win & (np.abs(Z + T_AU) < D / 2))
    fixed = rf | gnd
    fixed[:, :, 0] = True                  # ground plane
    fixed[:, :, -1] = True                 # far top
    fixed[-1, :, :] = True                 # outer edge
    val = np.where(rf, 1.0, 0.0)
    free = ~fixed
    n = int(free.sum())
    idx = -np.ones(free.shape, int)
    idx[free] = np.arange(n)
    I, J, K = np.nonzero(free)
    rows, cols, data = [], [], []
    diag = np.zeros(n)
    b = np.zeros(n)
    for axis in range(3):
        for s in (+1, -1):
            I2, J2, K2 = I.copy(), J.copy(), K.copy()
            if axis == 0:
                I2 = I + s
                I2 = np.where(I2 < 0, 1, I2)            # mirror at x = 0
            elif axis == 1:
                J2 = J + s
                J2 = np.where(J2 < 0, 1, J2)            # mirror at y = 0
                J2 = np.where(J2 > ny - 1, ny - 2, J2)  # mirror at y = YM
            else:
                K2 = K + s
            ef = 0.5 * (eps[I, J, K] + eps[I2, J2, K2])
            diag += ef
            nb = free[I2, J2, K2]
            rows.append(idx[I, J, K][nb]); cols.append(idx[I2, J2, K2][nb]); data.append(-ef[nb])
            np.add.at(b, idx[I, J, K][~nb], ef[~nb] * val[I2, J2, K2][~nb])
    rows.append(np.arange(n)); cols.append(np.arange(n)); data.append(diag)
    M = sp.csr_matrix((np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    # mirror rows make M slightly non-symmetric at the planes; BiCGSTAB handles that
    pre = sp.diags(1.0 / diag)
    t0 = time.time()
    sol, info = spla.bicgstab(M, b, M=pre, rtol=1e-9, maxiter=20000)
    phi = val.copy()
    phi[free] = sol
    return phi, info, time.time() - t0


def null_height(phi, j):
    """RF null on the line x = 0 at axial index j (|grad phi|^2 minimum, Ex = 0 by symmetry)."""
    col = phi[0, j, :]
    gz = np.gradient(col, D)
    gy = (phi[0, min(j + 1, ny - 1), :] - phi[0, max(j - 1, 0), :]) / (2 * D) if j > 0 else 0 * col
    g2 = gz ** 2 + gy ** 2
    sel = (zs > 10) & (zs < 100)
    k = np.argmin(np.where(sel, g2, np.inf))
    y0, y1, y2 = g2[k - 1:k + 2]
    den = y0 - 2 * y1 + y2
    return zs[k] + (0.5 * D * (y0 - y2) / den if den else 0.0), g2


CASES = [("none", 0, 0, "etched"),
         ("30x30 etched", 30, 30, "etched"), ("30x30 oxide", 30, 30, "oxide"),
         ("30x60 etched", 30, 60, "etched"), ("20x20 etched", 20, 20, "etched"),
         ("50x30 cut-through etched", 50, 30, "etched"),
         ("30x30 ito6", 30, 30, "ito6"), ("30x60 ito6", 30, 60, "ito6")]
TAG = ""
if len(sys.argv) > 1:          # e.g. "ito6": run only cases whose name contains it (+ reference)
    TAG = "_" + sys.argv[1]
    CASES = [CASES[0]] + [c for c in CASES[1:] if sys.argv[1] in c[0]]

res = {}
ref = None
jy = np.arange(0, 121, 5)
for name, wy, wx, floor in CASES:
    phi, info, dt = solve(wy, wx, floor)
    hs = np.array([null_height(phi, int(j / D))[0] for j in jy])
    if name == "none":
        ref = hs
    # axial RF field along the null line ~ axial pseudopotential barrier (relative units)
    gy_line = [abs(phi[0, min(int(j / D) + 1, ny - 1), int(np.searchsorted(zs, h))]
                   - phi[0, max(int(j / D) - 1, 0), int(np.searchsorted(zs, h))]) / (2 * D)
               for j, h in zip(jy, hs)]
    res[name] = dict(wy=wy, wx=wx, floor=floor, y=jy.tolist(), h=hs.tolist(),
                     dh=(hs - ref).tolist(), max_axial_grad=float(max(gy_line)), cg_info=int(info),
                     seconds=round(dt, 1))
    print(f"{name:26s} h(0) = {hs[0]:6.2f}  dh(0) = {hs[0]-ref[0]:+6.2f} um  dh(60) = "
          f"{np.interp(60, jy, hs - ref):+5.2f}  max |dphi/dy| on null line = {max(gy_line):.2e} /um  "
          f"(solver info {info}, {dt:.0f} s)")

with open(os.path.join(OUT, f"summary{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
plt.figure(figsize=(6.5, 4))
for name, r in res.items():
    if name != "none":
        plt.plot(r["y"], r["dh"], "o-", label=name)
plt.axhline(0, color="0.5", lw=0.7)
plt.xlabel("axial distance from window centre (um)")
plt.ylabel("change in RF null height (um)")
plt.title("3-D FD: window pocket effect on ion height (h0 ~ 50 um)")
plt.legend(fontsize=7)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, f"dh{TAG}.png"), dpi=150)
