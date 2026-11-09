"""15b - SNSPD collection and NbN absorption on the v4 stack (Claude-authored).

Parts A, B and C of 15_snspd_geometry.py, rerun on the v4 local-mirror stack (DESIGN_LOG, 2026-11-08,
"v4 SNSPD overhang audit"). Changes from 15:
  - stack: vacuum / SiO2 cap (80 or 160 nm) / NbN 7 nm, fill 0.65 / SiO2 238 nm / Al 450 nm / SiO2 1000 nm / Si.
    There is no D2 layer, so there is no fringe average: absorption is evaluated at the single stack given.
  - aperture = window floor; source-to-aperture distance D = ion height + Au thickness (E2 6.0 um, E1 0.35 um).
  - ion heights from sim/out/13_dc_height_tuning_v4/summary.json. E2: null + window drop. E1: the two brackets,
    null and null + drop (the drop is an upper bound from a 1 um pocket).
  - below the aperture the light crosses only the SiO2 cap (T_BELOW = cap thickness).
  - wavelength 493 nm; same n, k as 15. The aperture-grid, landing, cone-average and absorption functions
    are copied from 15, with D, window size and cap thickness passed in instead of read from globals.
Part D (sharp-turn crowding) and part E (kinetic inductance) of 15 are not included.

Outputs: sim/out/15b_collection_v4/summary.json
Run:     ./run.sh 15b_collection_v4.py
"""

import json
import os

import numpy as np

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "15b_collection_v4")
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(HERE, "out", "13_dc_height_tuning_v4", "summary.json")) as fh:
    H13 = json.load(fh)

N_SIO2 = 1.463
LAM = 493.0                                                      # nm
NK = dict(SiO2=N_SIO2, Si=4.333 + 0.048j, Al=0.605 + 5.245j, NbN=2.109 + 1.997j)   # as sim 15 / 09b
FILL, T_NBN = 0.65, 7.0                                          # NbN fill factor, thickness (nm)
T_SPACER, T_AL, T_OX = 238.0, 450.0, 1000.0                      # SiO2 spacer, Al mirror, SiO2 (nm)
AU = {"E2": 6.0, "E1": 0.35}                                     # Au electrode thickness (um)
CAPS = (80.0, 160.0)                                             # SiO2 cap over NbN (nm): drawn, design target
OVY = 1.0                                                        # meander envelope past the window, radial (um)
GEOM = {"A30": dict(wx=30.0, wy=30.0, ovx=3.0), "B60": dict(wx=60.0, wy=30.0, ovx=4.5)}   # ovx axial (um)
KEYS = [(p, pl) for p in ("s", "p") for pl in ("xz", "yz")]
TH = np.arange(0, 46, 1.0)                                       # angles in vacuum (deg)


# ------------------------------------------------------------------ geometry (from 15, D and cap as arguments)
def aperture_grid(wx, wy, D, n=400):
    """Aperture points at the window floor (x axial, y radial), isotropic weights dOmega, distance D."""
    x = (np.arange(n) + 0.5) / n * wx - wx / 2
    y = (np.arange(n) + 0.5) / n * wy - wy / 2
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X ** 2 + Y ** 2 + D ** 2)
    return X, Y, D / r ** 3


def landing(wx, wy, D, t_cap):
    """Landing points on the NbN for each aperture ray, after refraction through the cap (t_cap in um)."""
    X, Y, wt = aperture_grid(wx, wy, D)
    rho = np.hypot(X, Y) + 1e-12
    sin_s = (rho / np.sqrt(rho ** 2 + D ** 2)) / N_SIO2          # Snell at the window floor
    shift = t_cap * sin_s / np.sqrt(1 - sin_s ** 2)              # outward shift across the cap (um)
    return X * (1 + shift / rho), Y * (1 + shift / rho), wt, shift.max()


# ------------------------------------------------------------------ optics (from 15)
def iso_layer(n, d):
    e = n ** 2
    return (e, e, e, d)


def wire_layer(f, t):
    """EMT for the NbN lines: first component harmonic (across the lines), the other two arithmetic."""
    ew, eh = NK["NbN"] ** 2, NK["SiO2"] ** 2
    return (1.0 / (f / ew + (1 - f) / eh), f * ew + (1 - f) * eh, f * ew + (1 - f) * eh, t)


def kz_eta(ex, ey, ez, s, pol, plane):
    """plane 'xz': plane of incidence across the wires; 'yz': along them. s-pol E is normal to the plane."""
    et, eo = (ey, ex) if plane == "xz" else (ex, ey)
    kz = np.sqrt(et - s ** 2 + 0j) if pol == "s" else np.sqrt(eo * (1 - s ** 2 / ez) + 0j)
    kz = np.where(np.imag(kz) < 0, -kz, kz)
    return kz, (kz if pol == "s" else eo / kz)


def absorbed(layers, th_deg, pol, plane, idx):
    """Fraction of the incident power absorbed in layer idx. Layers are listed top (vacuum side) to bottom."""
    k0, s = 2 * np.pi / LAM, np.sin(np.radians(th_deg))
    es = NK["Si"] ** 2
    _, eta_sub = kz_eta(es, es, es, s, pol, plane)
    E = 1.0 + 0j
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
    return float((flux[idx] - flux[idx + 1]) / inc)


def stack(f, t, t_cap):
    """v4 stack below the vacuum: SiO2 cap / NbN lines / SiO2 spacer / Al mirror / SiO2 / Si. Thicknesses in nm."""
    return [iso_layer(NK["SiO2"], t_cap), wire_layer(f, t), iso_layer(NK["SiO2"], T_SPACER),
            iso_layer(NK["Al"], T_AL), iso_layer(NK["SiO2"], T_OX)]


def normal_incidence(t_cap):
    """Unpolarised absorption in the NbN at normal incidence: mean of the two linear polarisations."""
    st = stack(FILL, T_NBN, t_cap)
    lin = {f"{p}_{pl}": absorbed(st, 0.0, p, pl, 1) for p, pl in KEYS}
    return float(np.mean(list(lin.values()))), lin


def cone_avg(t_cap, wx, wy, D):
    """Unpolarised absorption in the NbN averaged over the isotropic emission through the window (as 15)."""
    st = stack(FILL, T_NBN, t_cap)
    T = {k: np.array([absorbed(st, th, k[0], k[1], 1) for th in TH]) for k in KEYS}
    X, Y, wt = aperture_grid(wx, wy, D, 120)
    th = np.degrees(np.arctan(np.hypot(X, Y) / D))
    c2 = Y ** 2 / (X ** 2 + Y ** 2 + 1e-12)                      # radial rays weighted to the 'xz' plane (as 15)
    A = {k: np.interp(th, TH, v) for k, v in T.items()}
    a_s = A[("s", "xz")] * c2 + A[("s", "yz")] * (1 - c2)
    a_p = A[("p", "xz")] * c2 + A[("p", "yz")] * (1 - c2)
    return float(np.sum(wt * 0.5 * (a_s + a_p)) / np.sum(wt))


# ------------------------------------------------------------------ cases: ion heights from sim 13
cases = []
for geo, g in GEOM.items():
    for el in ("E2", "E1"):
        e = H13[f"{geo}_{el}"]
        z_null, drop = float(e["null"][2]), float(e["window_drop_um"])
        if el == "E2":
            brackets = [("null+drop", z_null + drop)]
        else:
            brackets = [("null", z_null), ("null+drop", z_null + drop)]
        for bname, h in brackets:
            cases.append(dict(name=f"{geo}_{el}_{bname}", wx=g["wx"], wy=g["wy"], ovx=g["ovx"],
                              h=h, t_au=AU[el]))

res = dict(cases={})
print("v4 stack, 493 nm. Aperture = window floor, D = ion height + Au thickness.")
for c in cases:
    D = c["h"] + c["t_au"]
    coll = 100 * tc.collection_fraction(D, c["wx"], c["wy"], "iso")
    print(f"{c['name']}: h {c['h']:.4f} um, D {D:.4f} um, A collection {coll:.4f} %")
    out = dict(h_um=c["h"], D_um=D, collection_pct=coll, caps={})
    for cap in CAPS:
        XL, YL, wt, smax = landing(c["wx"], c["wy"], D, cap / 1000)
        on = (np.abs(XL) <= c["wx"] / 2 + c["ovx"]) & (np.abs(YL) <= c["wy"] / 2 + OVY)
        on_pct = 100 * float(np.sum(wt * on) / np.sum(wt))
        ab = cone_avg(cap, c["wx"], c["wy"], D)
        prod = coll * ab
        out["caps"][f"{cap:g}"] = dict(max_spread_um=float(smax), envelope_pct=on_pct,
                                       absorbed_cone=ab, absorbed_of_emitted_pct=prod)
        print(f"   cap {cap:g} nm: B max spread {smax:.4f} um, window photons on envelope {on_pct:.3f} %;"
              f" C NbN absorption {ab:.4f}, absorbed of all emitted {prod:.4f} %")
    res["cases"][c["name"]] = out

print("normal incidence, unpolarised (mean of the four s/p, xz/yz linear cases), f 0.65, t 7 nm")
res["normal_incidence"] = {}
for cap in CAPS:
    avg, lin = normal_incidence(cap)
    res["normal_incidence"][f"{cap:g}"] = dict(unpol=avg, linear=lin)
    print(f"   cap {cap:g} nm: unpolarised {avg:.4f}   linear " +
          "  ".join(f"{k} {v:.4f}" for k, v in lin.items()))


# ------------------------------------------------------------------ acceptance (agreement check, no tuning)
def cv(name, cap, field):
    return res["cases"][name]["caps"][f"{cap:g}"][field]


def co(name):
    return res["cases"][name]["collection_pct"]


rows = [
    ("collection A30 E2", "overhang audit", [co("A30_E2_null+drop")], 2.221, 2.221, 0.01),
    ("collection A30 E1", "overhang audit", [co("A30_E1_null"), co("A30_E1_null+drop")], 2.601, 2.636, 0.01),
    ("collection B60 E2", "overhang audit", [co("B60_E2_null+drop")], 4.158, 4.158, 0.01),
    ("collection B60 E1", "overhang audit", [co("B60_E1_null"), co("B60_E1_null+drop")], 4.674, 4.760, 0.01),
    ("absorbed A30 E2, 80 nm", "overhang audit", [cv("A30_E2_null+drop", 80, "absorbed_of_emitted_pct")], 0.980, 0.980, 0.02),
    ("absorbed A30 E2, 160 nm", "overhang audit", [cv("A30_E2_null+drop", 160, "absorbed_of_emitted_pct")], 1.470, 1.470, 0.02),
    ("absorbed B60 E2, 80 nm", "overhang audit", [cv("B60_E2_null+drop", 80, "absorbed_of_emitted_pct")], 1.838, 1.838, 0.02),
    ("absorbed B60 E2, 160 nm", "overhang audit", [cv("B60_E2_null+drop", 160, "absorbed_of_emitted_pct")], 2.709, 2.709, 0.02),
    ("absorbed A30 E1, 80 nm", "overhang audit", [cv("A30_E1_null", 80, "absorbed_of_emitted_pct"), cv("A30_E1_null+drop", 80, "absorbed_of_emitted_pct")], 1.149, 1.164, 0.02),
    ("absorbed A30 E1, 160 nm", "overhang audit", [cv("A30_E1_null", 160, "absorbed_of_emitted_pct"), cv("A30_E1_null+drop", 160, "absorbed_of_emitted_pct")], 1.720, 1.743, 0.02),
    ("absorbed B60 E1, 80 nm", "overhang audit", [cv("B60_E1_null", 80, "absorbed_of_emitted_pct"), cv("B60_E1_null+drop", 80, "absorbed_of_emitted_pct")], 2.067, 2.105, 0.02),
    ("absorbed B60 E1, 160 nm", "overhang audit", [cv("B60_E1_null", 160, "absorbed_of_emitted_pct"), cv("B60_E1_null+drop", 160, "absorbed_of_emitted_pct")], 3.029, 3.082, 0.02),
    ("normal incidence, 160 nm", "spec", [res["normal_incidence"]["160"]["unpol"]], 0.66, 0.66, 0.01),
    ("normal incidence, 80 nm", "spec", [res["normal_incidence"]["80"]["unpol"]], 0.44, 0.44, 0.01),
    ("spread A30, 160 nm (um)", "spec", [cv("A30_E2_null+drop", 160, "max_spread_um")], 0.041, 0.044, 0.001),
    ("spread A30, 80 nm (um)", "overhang audit", [cv("A30_E2_null+drop", 80, "max_spread_um")], 0.020, 0.022, 0.001),
    ("spread B60, 160 nm (um)", "overhang audit", [cv("B60_E2_null+drop", 160, "max_spread_um")], 0.062, 0.066, 0.001),
    ("spread B60, 80 nm (um)", "overhang audit", [cv("B60_E2_null+drop", 80, "max_spread_um")], 0.031, 0.033, 0.001),
]

res["acceptance"] = []
print("ACCEPTANCE   item | source | expected | yours | PASS/FAIL  (E1 and spread-range rows: all values must lie in range +- tol)")
for item, src, vals, lo, hi, tol in rows:
    ok = all(lo - tol <= v <= hi + tol for v in vals)
    exp = f"{lo:.4f}" if lo == hi else f"{lo:.4f}-{hi:.4f}"
    mine = ", ".join(f"{v:.4f}" for v in vals)
    print(f"   {item:<26} | {src:<16} | {exp:<14} | {mine:<28} | {'PASS' if ok else 'FAIL'}")
    res["acceptance"].append(dict(item=item, source=src, expected=[lo, hi], tol=tol, yours=vals, pass_=bool(ok)))

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
print("saved", os.path.join(OUT, "summary.json"))
