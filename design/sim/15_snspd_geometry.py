"""15 - SNSPD geometry budget: collection, refraction footprint, absorption vs fill, turn crowding (Claude-authored).

Saves as a script the numbers the geometry audit computed inline
(research/reports/SNSPD geometry audit.md), so they can be rerun and checked.

A  Geometric collection. Ba+ 493 nm (P1/2 -> S1/2) emission is isotropic: a P1/2 m' = +1/2 state
   decays by pi (branching 1/3, pattern 3/(8pi) sin^2) and sigma (2/3, 3/(16pi)(1 + cos^2)), and
   (1/3)(3/8pi) sin^2 + (2/3)(3/16pi)(1 + cos^2) = 1/(4pi). Any J = 1/2 state is a spin along some
   axis, so this holds for any population or B direction [team calc; check against an atomic-physics
   text]. sim/06 used the 'sigma' pattern; both are printed here.
B  Refraction footprint. The limiting aperture is the bottom of the 6 um Au window (z = -6 um). A ray
   through it crosses 10 um D2 SiO2 + 80 nm SiO2 cap (n = 1.463) to the NbN and lands further out.
   Fraction of window photons landing on a meander that extends (ovx, ovy) past the window edges.
C  NbN absorption vs fill factor: zeroth-order effective medium (EMT) transfer matrix at oblique
   incidence, v3 stack (vacuum / D2 10 um, fringe-averaged / SiO2 cap 80 / NbN wires / SiO2 spacer 238 /
   Al 150 / SiO2 1 um / Si), same n,k as sim/09b. Averaged over the isotropic, unpolarised emission
   that passes the window. Wires run along the trap axis. EMT is the zero-pitch limit: indicative at a
   200 nm pitch; RCWA or FDTD before sign-off.
D  Current crowding at a sharp 180-degree turn: Clem & Berggren, PRB 84, 174510 (2011), Eq. 100,
   R = (3/2) (pi alpha xi / 2W)^(1/3), alpha = sqrt(1 - (W/a)^2), a = W + gap/2 (full-width end block).
   W x R = turn-limited device current relative to v3 (same Jc).
E  Kinetic inductance and reset: dirty-BCS Lk = hbar Rs / (pi * 1.76 k Tc) for 7 nm NbN
   (Rs 400 Ohm/sq, Tc 7.9 K; fab/TRAVELER.md), tau = L / 50 Ohm.

Outputs: sim/out/15_snspd_geometry/summary.json
Run:     ./run.sh 15_snspd_geometry.py
"""

import json
import os

import numpy as np

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "15_snspd_geometry")
os.makedirs(OUT, exist_ok=True)

N_SIO2 = 1.463
T_AU, T_BELOW = 6.0, 10.08               # Au thickness; D2 SiO2 + cap above the NbN (um)
# ion height over the bare-SiO2 window, v3 (design/CLAUDE.md: 50.08 - 1.38, 50.09 - 2.50; sim 04b)
WINDOWS = {"A30": dict(wx=30.0, wy=30.0, h=48.70), "B60": dict(wx=60.0, wy=30.0, h=47.59)}
res = {}

# ------------------------------------------------------------------ A: geometric collection
print("A  geometric collection (aperture = bottom of the Au window)")
res["collection_pct"] = {}
for name, w in WINDOWS.items():
    D = w["h"] + T_AU
    iso = 100 * tc.collection_fraction(D, w["wx"], w["wy"], "iso")
    sig = 100 * tc.collection_fraction(D, w["wx"], w["wy"], "sigma")
    res["collection_pct"][name] = dict(iso=iso, sigma=sig)
    print(f"   {name}: isotropic {iso:.2f} %   (sigma pattern, as in sim/06: {sig:.2f} %)")


# ------------------------------------------------------------------ B: refraction footprint
def aperture_grid(w, n=400):
    """Aperture points (x axial, y radial), isotropic weights dOmega, distance D to the ion."""
    D = w["h"] + T_AU
    x = (np.arange(n) + 0.5) / n * w["wx"] - w["wx"] / 2
    y = (np.arange(n) + 0.5) / n * w["wy"] - w["wy"] / 2
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X ** 2 + Y ** 2 + D ** 2)
    return X, Y, D / r ** 3, D


def landing(w):
    X, Y, wt, D = aperture_grid(w)
    rho = np.hypot(X, Y) + 1e-12
    sin_s = (rho / np.sqrt(rho ** 2 + D ** 2)) / N_SIO2       # Snell at the window floor
    shift = T_BELOW * sin_s / np.sqrt(1 - sin_s ** 2)
    return X * (1 + shift / rho), Y * (1 + shift / rho), wt, shift.max()


print("B  fraction of window photons landing on the NbN (meander = window + overhang)")
res["footprint"] = {}
for name, w in WINDOWS.items():
    XL, YL, wt, smax = landing(w)
    rows = {}
    for ovx, ovy in ((0, 0), (2, 0), (3, 0), (4, 0), (4.5, 0), (3, 1), (4.5, 1), (2, 2), (3, 2), (4.5, 2), (4, 2)):
        on = (np.abs(XL) <= w["wx"] / 2 + ovx) & (np.abs(YL) <= w["wy"] / 2 + ovy)
        rows[f"{ovx:g},{ovy:g}"] = 100 * float(np.sum(wt * on) / np.sum(wt))
    res["footprint"][name] = dict(max_spread_um=float(smax), on_nbn_pct=rows)
    print(f"   {name}: max outward spread {smax:.2f} um; " +
          "  ".join(f"({k}) {v:.1f} %" for k, v in rows.items()))

# ------------------------------------------------------------------ C: absorption vs fill factor
LAM = 493.0
NK = dict(SiO2=N_SIO2, Si=4.333 + 0.048j, Al=0.605 + 5.245j, NbN=2.109 + 1.997j)   # as sim/09b
D2 = 10000.0 + np.arange(12) * LAM / (2 * N_SIO2) / 12                             # one fringe


def iso_layer(n, d):
    e = n ** 2
    return (e, e, e, d)


def wire_layer(f, t):
    """EMT for wires along y: ex = harmonic (across the wires), ey = ez = arithmetic."""
    ew, eh = NK["NbN"] ** 2, NK["SiO2"] ** 2
    return (1.0 / (f / ew + (1 - f) / eh), f * ew + (1 - f) * eh, f * ew + (1 - f) * eh, t)


def kz_eta(ex, ey, ez, s, pol, plane):
    """plane 'xz': plane of incidence across the wires; 'yz': along them. s-pol E is normal to the plane."""
    et, eo = (ey, ex) if plane == "xz" else (ex, ey)
    kz = np.sqrt(et - s ** 2 + 0j) if pol == "s" else np.sqrt(eo * (1 - s ** 2 / ez) + 0j)
    kz = np.where(np.imag(kz) < 0, -kz, kz)
    return kz, (kz if pol == "s" else eo / kz)


def absorbed(layers, th_deg, pol, plane, idx):
    """Fraction of the incident power absorbed in layer idx (fringe-averaged over the D2 thickness)."""
    k0, s = 2 * np.pi / LAM, np.sin(np.radians(th_deg))
    es = NK["Si"] ** 2
    _, eta_sub = kz_eta(es, es, es, s, pol, plane)
    E = np.ones_like(D2) + 0j
    H = eta_sub * E
    flux = [np.real(E * np.conj(H))]
    for ex, ey, ez, d in reversed(layers):
        kz, eta = kz_eta(ex, ey, ez, s, pol, plane)
        c, sn = np.cos(k0 * kz * d), np.sin(k0 * kz * d)
        E, H = c * E - 1j * sn / eta * H, -1j * eta * sn * E + c * H
        flux.append(np.real(E * np.conj(H)))
    flux = flux[::-1]
    c0 = np.cos(np.radians(th_deg))
    eta0 = c0 if pol == "s" else 1 / c0
    inc = eta0 * np.abs((E + H / eta0) / 2) ** 2
    return float(np.mean((flux[idx] - flux[idx + 1]) / inc))


def stack(f, t):
    return [(N_SIO2 ** 2,) * 3 + (D2,), iso_layer(NK["SiO2"], 80.0), wire_layer(f, t), iso_layer(NK["SiO2"], 238.0),
            iso_layer(NK["Al"], 150.0), iso_layer(NK["SiO2"], 1000.0)]


KEYS = [(p, pl) for p in ("s", "p") for pl in ("xz", "yz")]
TH = np.arange(0, 46, 1.0)


def cone_avg(f, t, w):
    """Unpolarised absorption averaged over the isotropic emission through the window (wires along x)."""
    T = {k: np.array([absorbed(stack(f, t), th, k[0], k[1], 2) for th in TH]) for k in KEYS}
    X, Y, wt, D = aperture_grid(w, 120)
    th = np.degrees(np.arctan(np.hypot(X, Y) / D))
    c2 = Y ** 2 / (X ** 2 + Y ** 2 + 1e-12)        # plane of incidence across the wires (radial) weight
    A = {k: np.interp(th, TH, v) for k, v in T.items()}
    a_s = A[("s", "xz")] * c2 + A[("s", "yz")] * (1 - c2)
    a_p = A[("p", "xz")] * c2 + A[("p", "yz")] * (1 - c2)
    return float(np.sum(wt * 0.5 * (a_s + a_p)) / np.sum(wt)), T[("s", "xz")][0], T[("s", "yz")][0]


print("C  NbN absorption at 493 nm (EMT): normal-incidence TE (E along wires) / TM (E across), cone average")
res["absorption"] = {}
for t in (5.0, 7.0):
    for f in (0.4, 0.5, 0.6, 0.65, 0.7, 0.8):
        a30, te, tm = cone_avg(f, t, WINDOWS["A30"])
        b60, _, _ = cone_avg(f, t, WINDOWS["B60"])
        res["absorption"][f"t{t:g}_f{f:g}"] = dict(TE0=te, TM0=tm, unpol0=(te + tm) / 2, cone_A30=a30, cone_B60=b60)
        print(f"   t {t:g} nm f {f:.2f}: TE {te:.3f} TM {tm:.3f} unpol {(te + tm) / 2:.3f}   cone A30 {a30:.3f} B60 {b60:.3f}")

# ------------------------------------------------------------------ D: Clem & Berggren sharp-turn factor
print("D  sharp 180-degree turn, Clem & Berggren Eq. 100 (full-width end block), R at xi = 4 / 5 / 7 nm")
res["crowding"] = {}
v3_wr = None
for W, P in ((100, 200), (120, 200), (130, 200), (140, 200), (100, 150), (300, 600)):
    a = W + (P - W) / 2
    alpha = np.sqrt(1 - (W / a) ** 2)
    R = {xi: 1.5 * (np.pi * alpha * xi / (2 * W)) ** (1 / 3) for xi in (4, 5, 7)}
    v3_wr = v3_wr or W * R[5]
    res["crowding"][f"{W}/{P}"] = dict(f=W / P, R=R, WR_vs_v3=W * R[5] / v3_wr)
    print(f"   {W}/{P} nm (f {W / P:.2f}): R {R[4]:.2f} / {R[5]:.2f} / {R[7]:.2f}   W x R vs v3 {W * R[5] / v3_wr:.2f}")

# ------------------------------------------------------------------ E: kinetic inductance
HBAR, KB = 1.0546e-34, 1.3807e-23
LK = HBAR * 400.0 / (np.pi * 1.76 * KB * 7.9)
print(f"E  Lk = {LK * 1e12:.0f} pH/sq (7 nm NbN, 400 Ohm/sq, Tc 7.9 K)")
res["inductance"] = dict(Lk_pH_per_sq=LK * 1e12)
for label, lx, ly, W, P in (("v3 A30", 30, 30, 0.10, 0.2), ("v3 B60", 60, 30, 0.10, 0.2),
                            ("v3.1 A30", 36, 32, 0.13, 0.2), ("v3.1 B60", 69, 32, 0.13, 0.2)):
    n = int(round(ly / P))
    n += n % 2
    sq = n * lx / W
    L = sq * LK
    res["inductance"][label] = dict(lines=n, length_mm=n * lx / 1000, squares=sq, L_uH=L * 1e6, tau_ns=L / 50 * 1e9)
    print(f"   {label}: {n} lines, {n * lx / 1000:.1f} mm, {sq:.0f} sq, L {L * 1e6:.1f} uH, tau {L / 50 * 1e9:.0f} ns")

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
