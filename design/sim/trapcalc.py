"""Shared physics helpers for the design scripts (Claude-authored).

Everything here is plain numpy. The gds2itvg-based helpers evaluate unit potentials directly at
points (no grid files), using finite differences for gradients and Hessians. The formulas are the
same ones used in electrode/workflow.ipynb (sections 7-9), lifted out so every script uses one copy.

Units: positions in um, potentials in V per V (unit potentials), energies in eV unless noted.
Frame: ITVG frame of gds2itvg -> y is the trap axis, x is radial in-plane, z is height.
"""

import numpy as np

E = 1.602176634e-19        # C
AMU = 1.66053906660e-27    # kg
M_BA138 = 137.905247 * AMU

# Default drive for 138Ba+ (chosen in 01_analytic_fivewire.py; see DESIGN_LOG.md)
F_RF = 28e6                # Hz
V_RF = 120.0               # V, zero-to-peak (set per design in 01)


# ---------------------------------------------------------------- analytic (gapless, 2-D) model
def strip_phi(x, z, x1, x2):
    """Potential of an infinitely long strip x1<x<x2 held at 1 V in a grounded plane (z>0).
    Standard result, e.g. House PRA 78, 033402 (2008) Eq. 2 / Wesenberg PRA 78, 063410 (2008)."""
    return (np.arctan2(x2 - x, z) - np.arctan2(x1 - x, z)) / np.pi


def fivewire_rf_phi(x, z, c, a, g=0.0):
    """Unit RF potential of a symmetric five-wire: centre DC width c (centred on x=0),
    RF rails of width a separated from it by gap g. Gaps are split at their midline (gapless model)."""
    x1 = c / 2 + g / 2            # midline of the inner gap
    x2 = c / 2 + g + a + g / 2    # midline of the outer gap
    return strip_phi(x, z, x1, x2) + strip_phi(x, z, -x2, -x1)


def fivewire_null_height(c, a, g=0.0):
    """RF null height of the symmetric five-wire, h = sqrt(x1 x2) (from dphi/dz = 0 at x = 0)."""
    x1 = c / 2 + g / 2
    x2 = c / 2 + g + a + g / 2
    return np.sqrt(x1 * x2)


# ---------------------------------------------------------------- pseudopotential helpers
def pseudo_eV(grad_phi_per_um, v_rf=V_RF, f_rf=F_RF, m=M_BA138):
    """Pseudopotential (eV) from |grad phi_RF| in V/um per V: Psi = e V^2 |grad phi|^2 / (4 m Omega^2)."""
    Om = 2 * np.pi * f_rf
    g2 = np.sum(np.asarray(grad_phi_per_um) ** 2, axis=-1) * 1e12
    return E * v_rf ** 2 * g2 / (4 * m * Om ** 2)


def rf_hessian_to_freqs(H_rf_per_um2, v_rf=V_RF, f_rf=F_RF, m=M_BA138):
    """RF-only secular frequencies (Hz) and Mathieu q from the Hessian of the unit RF potential
    at the null (V/um^2 per V). Psi Hessian = e^2 V^2/(2 m Om^2) H.H  (workflow.ipynb cell 27)."""
    Om = 2 * np.pi * f_rf
    H = np.asarray(H_rf_per_um2) * 1e12
    K = E ** 2 * v_rf ** 2 / (2 * m * Om ** 2) * (H @ H)
    ev = np.linalg.eigvalsh(K)
    f = np.sqrt(np.abs(ev) / m) / (2 * np.pi)
    q = 2 * E * v_rf * np.abs(np.linalg.eigvalsh(H)) / (m * Om ** 2)
    return f, q, K


# ---------------------------------------------------------------- finite differences on gds2itvg
def taylor_points(p, h=0.5):
    """Stencil points for value, gradient and Hessian at p (19-point central differences)."""
    p = np.asarray(p, float)
    pts = [p]
    I = np.eye(3) * h
    for i in range(3):
        pts += [p + I[i], p - I[i]]
    for i in range(3):
        for j in range(i + 1, 3):
            pts += [p + I[i] + I[j], p + I[i] - I[j], p - I[i] + I[j], p - I[i] - I[j]]
    return np.array(pts)


def taylor_from_values(v, h=0.5):
    """Value, gradient (per um), Hessian (per um^2) from values on taylor_points(p, h)."""
    f0 = v[0]
    g = np.zeros(3)
    H = np.zeros((3, 3))
    k = 1
    for i in range(3):
        fp, fm = v[k], v[k + 1]
        g[i] = (fp - fm) / (2 * h)
        H[i, i] = (fp - 2 * f0 + fm) / h ** 2
        k += 2
    for i in range(3):
        for j in range(i + 1, 3):
            pp, pm, mp, mm = v[k:k + 4]
            H[i, j] = H[j, i] = (pp - pm - mp + mm) / (4 * h ** 2)
            k += 4
    return f0, g, H


def taylor_all(electrodes, p, h=0.5):
    """{name: (phi, grad, Hessian)} for every gds2itvg electrode at point p (ITVG frame, um)."""
    from gds2itvg import unit_potentials
    pts = taylor_points(p, h)
    vals = unit_potentials(electrodes, pts)
    return {n: taylor_from_values(np.asarray(v), h) for n, v in vals.items()}


def sum_taylor(T, weights):
    """Weighted sum of taylor_all outputs: weights = {name: volts}."""
    f = sum(w * T[n][0] for n, w in weights.items())
    g = sum(w * T[n][1] for n, w in weights.items())
    H = sum(w * T[n][2] for n, w in weights.items())
    return f, g, H


# ---------------------------------------------------------------- DC solve (workflow.ipynb cell 29)
def solve_dc(T, rf_names, active, f_axial=1.0e6, v_rf=V_RF, f_rf=F_RF, m=M_BA138,
             dc_limit=10.0, extra_rows=None, tilt_xz=0.0, grad_target=(0.0, 0.0, 0.0)):
    """Minimum-norm DC voltages at one ion position.

    Constraints: grad(phi_DC) = grad_target (V/um; default 0 = no stray force at the RF null; a
    non-zero z entry pushes the ion off the null, see 13_dc_height_tuning.py), d2/dxdz = tilt_xz (radial
    mode rotation; 0 = none, non-zero tilts the radial axes away from the surface normal), and
    axial curvature giving f_axial once the RF pseudopotential's axial curvature is included.
    Returns (V dict, info dict). Falls back to bounded least squares if |V| > dc_limit.
    """
    from scipy.optimize import lsq_linear
    _, _, Hrf = sum_taylor(T, {n: 1.0 for n in rf_names})
    _, _, Kpsi = rf_hessian_to_freqs(Hrf, v_rf, f_rf, m)
    w_ax = 2 * np.pi * f_axial
    A = np.array([[T[n][1][0], T[n][1][1], T[n][1][2], T[n][2][0, 2],
                   E * T[n][2][1, 1] * 1e12] for n in active]).T
    b = np.array([grad_target[0], grad_target[1], grad_target[2], tilt_xz, m * w_ax ** 2 - Kpsi[1, 1]])
    if extra_rows is not None:
        A = np.vstack([A, extra_rows[0]])
        b = np.concatenate([b, extra_rows[1]])
    rs = np.linalg.norm(A, axis=1)
    rs[rs == 0] = 1.0
    As, bs = A / rs[:, None], b / rs
    sv = np.linalg.svd(As, compute_uv=False)
    v = np.linalg.lstsq(As, bs, rcond=None)[0]
    bounded = False
    if np.abs(v).max() > dc_limit:
        sol = lsq_linear(np.vstack([As, 1e-3 * np.eye(len(active))]),
                         np.concatenate([bs, np.zeros(len(active))]), bounds=(-dc_limit, dc_limit))
        v, bounded = sol.x, True
    V = dict(zip(active, v))
    _, g_dc, H_dc = sum_taylor(T, V)
    K = Kpsi + E * H_dc * 1e12
    ev, evec = np.linalg.eigh(K)
    f = np.sign(ev) * np.sqrt(np.abs(ev) / m) / (2 * np.pi)
    info = dict(sv=sv, bounded=bounded, residual_field=np.linalg.norm(g_dc), K=K,
                freqs=f, axes=evec, f_axial=np.sqrt(max(K[1, 1], 0) / m) / (2 * np.pi),
                vmax=float(np.abs(v).max()))
    return V, info


# ---------------------------------------------------------------- detector collection
def collection_fraction(h, sx, sy, dipole="sigma", n=200):
    """Fraction of photons emitted by an ion at height h hitting a sx*sy rectangle centred below it.

    dipole: 'iso' (isotropic), 'sigma' (dipole moment rotating in the surface plane, quantization
    axis along z), 'pi' (linear dipole along z), or 'avg' (isotropic average, same as iso).
    Pattern weights: pi: 3/(8pi) sin^2(theta); sigma: 3/(16pi)(1+cos^2(theta)); theta from z axis.
    Integrates over the rectangle directly: dOmega = h dA / r^3.
    """
    xs = (np.arange(n) + 0.5) / n * sx - sx / 2
    ys = (np.arange(n) + 0.5) / n * sy - sy / 2
    X, Y = np.meshgrid(xs, ys)
    r = np.sqrt(X ** 2 + Y ** 2 + h ** 2)
    dOm = h / r ** 3 * (sx / n) * (sy / n)
    c2 = (h / r) ** 2
    if dipole == "pi":
        w = 3 / (8 * np.pi) * (1 - c2)
    elif dipole == "sigma":
        w = 3 / (16 * np.pi) * (1 + c2)
    else:
        w = np.full_like(c2, 1 / (4 * np.pi))
    return float(np.sum(w * dOm))
