"""27 - Tilt geometry screen in 2-D (Claude-authored).

Fast 2-D screen of five-wire electrode geometries, using infinite gapless strips (trapcalc.strip_phi).
Frame: x = in-plane radial, z = height, trap axis out of the page. Every electrode is a list of
strips at 1 V in a grounded plane. Conventions:
- RF: both rails at 1 V (in phase, as trapcalc.fivewire_rf_phi); DC electrodes and ground at 0 V.
- "top" = +x side, "bottom" = -x side.
- Gaps are closed at their midlines. The centre DC edge is at c/2 + g/2. An outer DC strip is drawn
  from (rail outer edge + g) out to 200 um further, so it runs from the rail-gap midline to the
  midline of the gap beyond it (rail outer edge + g + 200 + g/2).
- G1 split (gs): the halves occupy gs/2 < |x| < c/2 + g/2 with real edges at gs/2; |x| < gs/2 is ground.
- G3 (asymmetric rails): both rail widths are scaled by one factor s (bisection) so the RF null is at 50 um.
- The depth is the maximum of the pseudopotential along z above the null at x = x0. For asymmetric
  rails this is an upper bound (it ignores the x-direction escape).

Ranking metric: the minimum-norm DC voltage that makes E_x = E_z = H_xx = 0 and H_xz = NEED, where NEED
is the xz curvature for a 0.1 MHz radial split at 45 deg (fbar = 3 MHz). If the 4-row system is not
exactly solvable (fewer than 4 independent electrodes), the solve without the H_xx row is also reported.
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "27_tilt_geometry_2d")
os.makedirs(OUT, exist_ok=True)

G = 5.0                  # um, RF / DC gap
C_OUT = 200.0            # um, depth of each outer DC strip
C0 = 40.0                # um, centre DC width (v4)
A0 = 84.0                # um, RF rail width (v4)
H0 = 50.0                # um, ion height
F = tc.F_RF              # Hz, RF drive
FRAD = 3.0e6             # Hz, radial frequency for the RF voltage
FBAR = 3.0e6             # Hz, centre of the split
DF = 0.1e6               # Hz, split size
NEED = 0.5 * tc.M_BA138 * (2 * np.pi) ** 2 * ((FBAR + DF / 2) ** 2 - (FBAR - DF / 2) ** 2) / (tc.E * 1e12)


# ---------------------------------------------------------------- 2-D potentials
def phi(x, z, strips):
    """Potential of strips (list of (x1, x2), each at 1 V); x, z may be arrays."""
    return sum(tc.strip_phi(x, z, a, b) for a, b in strips)


def rf_grad(x, z, rails, d=1e-3):
    gx = (phi(x + d, z, rails) - phi(x - d, z, rails)) / (2 * d)
    gz = (phi(x, z + d, rails) - phi(x, z - d, rails)) / (2 * d)
    return gx, gz


def rf_hess(x, z, rails, h=0.02):
    """2x2 Hessian (xx, zz, xz) of the RF potential, central differences."""
    p0 = phi(x, z, rails)
    hxx = (phi(x + h, z, rails) - 2 * p0 + phi(x - h, z, rails)) / h ** 2
    hzz = (phi(x, z + h, rails) - 2 * p0 + phi(x, z - h, rails)) / h ** 2
    hxz = (phi(x + h, z + h, rails) - phi(x + h, z - h, rails)
           - phi(x - h, z + h, rails) + phi(x - h, z - h, rails)) / (4 * h ** 2)
    return hxx, hzz, hxz


def null_point(rails, z_start=H0):
    """Newton iteration on grad(phi_RF) = 0, starting at (0, z_start)."""
    x, z = 0.0, z_start
    for _ in range(100):
        gx, gz = rf_grad(x, z, rails)
        if np.hypot(gx, gz) < 1e-10:
            break
        hxx, hzz, hxz = rf_hess(x, z, rails)
        dx, dz = np.linalg.solve([[hxx, hxz], [hxz, hzz]], [gx, gz])
        x, z = x - dx, z - dz
    gx, gz = rf_grad(x, z, rails)
    if np.hypot(gx, gz) > 1e-9:
        raise SystemExit(f"null search did not converge: |grad| = {np.hypot(gx, gz):.2e}")
    return float(x), float(z)


def dc_resp(strips, x0, z0, h=0.25):
    """(E_x, E_z, H_xx, H_xz) of one DC electrode at (x0, z0) per volt, central differences (step h um)."""
    f = lambda x, z: phi(x, z, strips)
    f0 = f(x0, z0)
    gx = (f(x0 + h, z0) - f(x0 - h, z0)) / (2 * h)
    gz = (f(x0, z0 + h) - f(x0, z0 - h)) / (2 * h)
    hxx = (f(x0 + h, z0) - 2 * f0 + f(x0 - h, z0)) / h ** 2
    hxz = (f(x0 + h, z0 + h) - f(x0 + h, z0 - h) - f(x0 - h, z0 + h) + f(x0 - h, z0 - h)) / (4 * h ** 2)
    return float(gx), float(gz), float(hxx), float(hxz)


def solve_rows(A, b):
    """Minimum-norm solve with row-normalised rows (as trapcalc.solve_dc). Returns (V, relative residual)."""
    rs = np.linalg.norm(A, axis=1)
    rs[rs == 0] = 1.0
    As, bs = A / rs[:, None], b / rs
    v = np.linalg.lstsq(As, bs, rcond=None)[0]
    return v, float(np.linalg.norm(As @ v - bs) / np.linalg.norm(bs))


# ---------------------------------------------------------------- geometry
def build(c, a_top, a_bot, gs=None):
    """(RF rails, DC electrodes {name: strips}) for centre DC width c and rail widths a_top (+x), a_bot (-x)."""
    x1 = c / 2 + G / 2                      # centre DC edge (inner gap midline)
    rt = c / 2 + G + a_top + G / 2          # top rail outer gap midline
    rb = c / 2 + G + a_bot + G / 2          # bottom rail outer gap midline
    rails = [(x1, rt), (-rb, -x1)]
    dc = {}
    if gs is None:
        dc["centre"] = [(-x1, x1)]
    else:
        dc["centre_top"] = [(gs / 2, x1)]
        dc["centre_bot"] = [(-x1, -gs / 2)]
    dc["outer_top"] = [(rt, rt + G + C_OUT)]
    dc["outer_bot"] = [(-(rb + G + C_OUT), -rb)]
    return rails, dc


def scale_for(d):
    """Common factor s on both rail widths a(1 +- d) so that the RF null sits at H0 (bisection)."""
    def z0_of(s):
        rails, _ = build(C0, A0 * (1 + d) * s, A0 * (1 - d) * s)
        return null_point(rails)[1]
    lo, hi = 0.5, 1.5
    if not (z0_of(lo) < H0 < z0_of(hi)):
        raise SystemExit(f"d = {d}: null height not bracketed in s = [0.5, 1.5]")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if z0_of(mid) < H0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def analyse(name, group, c, gs, a_top, a_bot):
    rails, dc = build(c, a_top, a_bot, gs)
    x0, z0 = null_point(rails)

    # RF Hessian, embedded in 3x3 (index 0 = x, 2 = z; y is the axis, zero)
    hxx, hzz, hxz = rf_hess(x0, z0, rails)
    H3 = np.zeros((3, 3))
    H3[0, 0], H3[2, 2], H3[0, 2], H3[2, 0] = hxx, hzz, hxz, hxz
    f1 = tc.rf_hessian_to_freqs(H3, 1.0, F)[0]
    fs = np.sort(f1)[-2:]
    rel = abs(fs[1] - fs[0]) / fs.mean()
    if rel > 1e-6:
        raise SystemExit(f"{name}: RF radial frequencies differ (rel {rel:.2e}); stop")
    v_rf = FRAD / fs.mean()
    fv, qv, _ = tc.rf_hessian_to_freqs(H3, v_rf, F)
    q = float(qv.max())

    # depth along z above the null at x0 (upper bound for asymmetric rails)
    zz = np.linspace(z0, 900.0, 18000)[1:]
    d = 1e-3
    gxa = (phi(x0 + d, zz, rails) - phi(x0 - d, zz, rails)) / (2 * d)
    gza = (phi(x0, zz + d, rails) - phi(x0, zz - d, rails)) / (2 * d)
    psi = tc.pseudo_eV(np.column_stack([gxa, 0 * gxa, gza]), v_rf, F)
    k = int(np.argmax(psi))
    depth = 1e3 * float(psi[k])

    # DC solves
    names = list(dc)
    resp = {n: dc_resp(dc[n], x0, z0) for n in names}
    A = np.array([[resp[n][r] for n in names] for r in range(4)])
    b = np.array([0.0, 0.0, 0.0, NEED])
    v4, r4 = solve_rows(A, b)
    v3, r3 = solve_rows(A[[0, 1, 3]], b[[0, 1, 3]])
    st4 = "ok" if r4 < 1e-6 else "cannot"

    bar = float(np.abs(v4).max()) if st4 == "ok" else float(np.abs(v3).max())
    rec = dict(name=name, group=group, c_um=c, split_gap_um=gs, a_top_um=a_top, a_bot_um=a_bot,
               x0_um=x0, z0_um=z0, V_rf_3MHz=float(v_rf), q=q, depth_meV=depth, depth_z_um=float(zz[k]),
               depth_note="upper bound for asymmetric rails" if group == "G3" else "",
               rf_freq_rel_diff=float(rel), rf_freqs_Hz=[float(x) for x in fv],
               dc={n: dict(E_x=resp[n][0], E_z=resp[n][1], H_xx=resp[n][2], H_xz=resp[n][3]) for n in names},
               solve4=dict(status=st4, vmax=float(np.abs(v4).max()), rel_residual=r4,
                           V={n: float(x) for n, x in zip(names, v4)}),
               solve_no_Hxx=dict(vmax=float(np.abs(v3).max()), rel_residual=r3,
                                 V={n: float(x) for n, x in zip(names, v3)}),
               bar_vmax=bar, bar_source="4-row" if st4 == "ok" else "no-H_xx")
    return rec


# ---------------------------------------------------------------- variants
print(f"target H_xz for 0.1 MHz split at 45 deg: {NEED:.4e} V/um^2 per V")
variants = [("G0", "G0", C0, None, A0, A0), ("G1_gap5", "G1", C0, 5.0, A0, A0),
            ("G1_gap25", "G1", C0, 25.0, A0, A0), ("G1s_slot", "G1", C0, 25.0, A0, A0)]
for d in (0.1, 0.2, 0.3, 0.5):
    s = scale_for(d)
    variants.append((f"G3_d{d}", "G3", C0, None, A0 * (1 + d) * s, A0 * (1 - d) * s))
    print(f"G3 d = {d}: common rail factor s = {s:.5f}")
for c in (20.0, 30.0, 60.0):
    x1 = c / 2 + G / 2
    x2 = H0 ** 2 / x1
    a = x2 - x1 - G
    variants.append((f"G4_c{c:g}", "G4", c, None, a, a))
for c in (20.0, 30.0, 60.0):
    x1 = c / 2 + G / 2
    a = H0 ** 2 / x1 - x1 - G
    variants.append((f"G4_c{c:g}_gap5", "G4+split", c, 5.0, a, a))

recs = [analyse(*v) for v in variants]

# ---------------------------------------------------------------- acceptance and RF checks
for r in recs:
    print(f"{r['name']:14s} RF: x0 = {r['x0_um']:+.4f} um, z0 = {r['z0_um']:.4f} um, "
          f"radial freq split rel {r['rf_freq_rel_diff']:.1e} (must be < 1e-6)")
g0 = [r for r in recs if r["name"] == "G0"][0]
print(f"\nACCEPTANCE G0: null height {g0['z0_um']:.3f} um (target 50, tol 0.5): "
      f"{'PASS' if abs(g0['z0_um'] - H0) < 0.5 else 'FAIL'}; x0 = {g0['x0_um']:.2e} um: "
      f"{'PASS' if abs(g0['x0_um']) < 1e-6 else 'FAIL'}")
g1 = [r for r in recs if r["name"] == "G1_gap5"][0]
print(f"ACCEPTANCE G1_gap5 (halves 2.5..22.5): {g1['bar_vmax']:.3f} V ({g1['bar_source']}); "
      f"G1s_slot (halves 12.5..22.5): {[r for r in recs if r['name'] == 'G1s_slot'][0]['bar_vmax']:.3f} V; "
      f"reference scratch script ~0.15 V for its 2.5..20 split (not re-run here)")

# ---------------------------------------------------------------- table
print("\nTable, sorted by V per 0.1 MHz at 45 deg (bar value)")
hdr = (f"{'variant':14s} {'c':>4s} {'gs':>4s} {'a_top':>7s} {'a_bot':>7s} {'x0':>7s} {'z0':>7s} "
       f"{'V_RF':>6s} {'q':>6s} {'depth':>7s} {'vmax4':>8s} {'st4':>7s} {'vmax_noHxx':>10s} {'bar':>8s}")
print(hdr)
for r in sorted(recs, key=lambda r: r["bar_vmax"]):
    gs = "-" if r["split_gap_um"] is None else f"{r['split_gap_um']:g}"
    print(f"{r['name']:14s} {r['c_um']:4.0f} {gs:>4s} {r['a_top_um']:7.2f} {r['a_bot_um']:7.2f} "
          f"{r['x0_um']:+7.3f} {r['z0_um']:7.3f} {r['V_rf_3MHz']:6.1f} {r['q']:6.3f} {r['depth_meV']:7.2f} "
          f"{r['solve4']['vmax']:8.3f} {r['solve4']['status']:>7s} {r['solve_no_Hxx']['vmax']:10.3f} "
          f"{r['bar_vmax']:8.3f}")
print("depth for G3 is an upper bound (depth along z at x0). bar = 4-row vmax when status ok, else no-H_xx vmax.")

# ---------------------------------------------------------------- outputs
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(dict(NEED_Hxz_V_per_um2_per_V=NEED, records=recs), fh, indent=1, default=float)

fig, ax = plt.subplots(figsize=(10, 4.8))
order = sorted(recs, key=lambda r: r["bar_vmax"])
for i, r in enumerate(order):
    hatch = "" if r["bar_source"] == "4-row" else "//"
    ax.bar(i, r["bar_vmax"], color="0.6", edgecolor="k", hatch=hatch)
ax.set_yscale("log")
ax.set_xticks(range(len(order)))
ax.set_xticklabels([r["name"] for r in order], rotation=60, ha="right", fontsize=8)
ax.set_ylabel("max |V| of DC electrodes (V)")
ax.set_title("0.1 MHz radial split at 45 deg, 2-D screen (hatched: no H_xx row)", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "ranking.png"), dpi=150)
print(f"\nwrote {os.path.join(OUT, 'summary.json')} and ranking.png")
