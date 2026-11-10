"""25 - Can a 138Ba+ surface trap rotate its two radial mode axes by 45 deg in the x-z plane with DC
voltages within +-10 V? Also sweeps other angles and split values.

Frame: ITVG (x in-plane radial, y trap axis, z height). Laser k_hat = (1, 1, 0)/sqrt(2).
Electrode sets per zone: n14 (the 14 DC electrodes with the largest |phi| at the ion, as sim 12),
all (every DC electrode), all_no2 (all except the centre DC, electrode 2).
Two methods:
  natural     : sim 12's rule. Solve untilted, set the tilt from K[2,2] - K[0,0], re-solve.
                theta in {0, 5, 10, 15, 20, 30} deg.
  fixed split : choose the radial split df (MHz) and the angle theta of the higher-frequency mode from
                +x toward +z. With dK = M (2 pi)^2 (f1^2 - f2^2), the total targets are
                K_xx - K_zz = dK cos(2 theta) and K_xz = dK sin(2 theta) / 2. theta in {0..90} deg,
                df in {0.1, 0.2, 0.3, 0.5} MHz. The mean radial frequency is fixed by the untilted solve.
Every solve is clipped at +-10 V (bounded least squares, as in trapcalc). The unclipped minimum-norm
solution is also solved (vmax_unclipped), so a target that needs more than 10 V still gets a number.
Robustness: 10 mV Gaussian errors on every active voltage (200 draws) at 45 deg, where the clipped
solve is not bounded. theta_max_fit: bisection on vmax_unclipped <= 10 V over [0, 45] deg, where
45 deg is bounded (assumes the fit is monotonic in theta).

Usage: ./run.sh 25_radial_tilt_sweep.py [path/to/chip_sim.json] [--fax=0.6]   (default ../gds/trap_die_v4_A30_sim.json,
       0.8 MHz axial as sim 12)
Outputs: out/25_radial_tilt_sweep/<TAG>/summary.json, vmax_vs_theta.png, projection_vs_theta.png,
where TAG is the json basename without _sim.json. Prints one table row per solve.
"""

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
# --fax=0.6: axial frequency in MHz (default 0.8, as sim 12); a non-default value is added to the output tag
FAX_ARG = [a for a in sys.argv[1:] if a.startswith("--fax=")]
F_AX = float(FAX_ARG[0].split("=")[1]) * 1e6 if FAX_ARG else 0.8e6
JS = os.path.abspath(ARGS[0] if ARGS else os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json"))
LAYOUT = json.load(open(JS))
# v4 layouts name the GDS to simulate ("_gds": the A30 _simfloor.gds adds the grounded window floor)
GDS = os.path.join(os.path.dirname(JS), LAYOUT["_gds"]) if "_gds" in LAYOUT else JS.replace("_sim.json", ".gds")
TAG = os.path.basename(JS).replace("_sim.json", "") + (f"_fax{F_AX / 1e6:g}" if FAX_ARG else "")
OUT = os.path.join(HERE, "out", "25_radial_tilt_sweep", TAG)
os.makedirs(OUT, exist_ok=True)

V_RF, F_RF = 53.0, tc.F_RF
DC_LIMIT = 10.0
N_ACTIVE = 14
M = tc.M_BA138
KHAT = np.array([1.0, 1.0, 0.0]) / np.sqrt(2.0)
ZONES = LAYOUT["_zones"]
ZONE_Y = {"loading": ZONES["loading_itvg_y"], "readout": ZONES["readout_itvg_y"]}
NATURAL_THETAS = [0, 5, 10, 15, 20, 30]
# 0 = higher-frequency radial mode along x (in plane), 90 = along z (vertical). Which one the trap has naturally
# depends on the zone, so both ends are swept; the tilt away from the surface axes is min(theta, 90 - theta).
FIXED_THETAS = [0, 5, 10, 15, 20, 30, 45, 60, 70, 75, 80, 85, 90]
DFS = [0.1, 0.2, 0.3, 0.5]          # MHz

lay = Layout.from_json(JS)
els, _ = build_electrodes(GDS, lay, ion_box=(-20, 20, -900, 350), ion_z=(25, 90), return_ground=True)
dc_names = [n for n in els if n != "1"]


def radial(K):
    """Angle (deg, folded into (-90, 90]) of the higher-frequency radial mode from +x toward +z, and the
    radial split (Hz) from the x-z block of K."""
    ev, evec = np.linalg.eigh(K[np.ix_([0, 2], [0, 2])])
    v = evec[:, np.argmax(ev)]
    ang = np.degrees(np.arctan2(v[1], v[0]))
    if ang > 90:
        ang -= 180
    if ang <= -90:
        ang += 180
    f = np.sign(ev) * np.sqrt(np.abs(ev) / M) / (2 * np.pi)
    return ang, f.max() - f.min()


def projections(K):
    """(k_hat . e)^2 for the three eigenvectors of K, listed in order of increasing frequency."""
    ev, evec = np.linalg.eigh(K)
    f = np.sign(ev) * np.sqrt(np.abs(ev) / M) / (2 * np.pi)
    return [dict(f_MHz=float(f[i] / 1e6), proj=float((KHAT @ evec[:, i]) ** 2)) for i in range(3)]


def solve(T, active, tilt=0.0, extra=None, dc_limit=DC_LIMIT):
    return tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF,
                       dc_limit=dc_limit, tilt_xz=tilt, extra_rows=extra)


def natural_solve(T, active, theta, dc_limit=DC_LIMIT):
    # sim 12 rule: the untilted solve is always clipped, as in sim 12
    _, info0 = solve(T, active)
    dk = info0["K"][2, 2] - info0["K"][0, 0]
    kxz = 0.5 * np.tan(2 * np.deg2rad(theta)) * dk / tc.E / 1e12
    return solve(T, active, tilt=kxz, dc_limit=dc_limit)


def fbar_of(active):
    """Mean of the two radial frequencies (Hz) from the untilted clipped solve."""
    _, info0 = solve(T_ZONE, active)
    return np.sort(info0["freqs"])[1:].mean()


def fixed_solve(active, theta, df_hz, fbar, dc_limit=DC_LIMIT):
    f1, f2 = fbar + df_hz / 2, fbar - df_hz / 2
    dK = M * (2 * np.pi) ** 2 * (f1 ** 2 - f2 ** 2)
    th = np.deg2rad(theta)
    hxz = (0.5 * dK * np.sin(2 * th) - KPSI[0, 2]) / (tc.E * 1e12)
    hdiff = (dK * np.cos(2 * th) - (KPSI[0, 0] - KPSI[2, 2])) / (tc.E * 1e12)
    row = np.array([[T_ZONE[n][2][0, 0] - T_ZONE[n][2][2, 2] for n in active]])
    return solve(T_ZONE, active, tilt=hxz, extra=(row, np.array([hdiff])), dc_limit=dc_limit)


def record(zone, method, setname, theta, df, info, vmax_unc):
    ang, split = radial(info["K"])
    return dict(zone=zone, method=method, set=setname, theta_target=float(theta),
                tilt_from_axes_deg=float(min(abs(theta), 90 - abs(theta))),
                df_target=None if df is None else float(df),
                vmax=float(info["vmax"]), vmax_unclipped=float(vmax_unc), bounded=bool(info["bounded"]),
                freqs_MHz=[float(x) for x in np.sort(info["freqs"]) / 1e6],
                f_axial_MHz=float(info["f_axial"] / 1e6), residual_field_V_per_um=float(info["residual_field"]),
                all_curvatures_positive=bool(np.all(np.linalg.eigvalsh(info["K"]) > 0)),
                angle_deg=float(ang), split_MHz=float(split / 1e6), projections=projections(info["K"]))


def robustness(active, V, ang0):
    """Angle scatter (deg) for 200 draws of 10 mV Gaussian errors on every active voltage."""
    rng = np.random.default_rng(0)
    noise = rng.normal(0.0, 0.010, size=(200, len(active)))
    d = []
    for e in noise:
        Vp = {n: V[n] + ei for n, ei in zip(active, e)}
        _, _, H = tc.sum_taylor(T_ZONE, Vp)
        angp, _ = radial(KPSI + tc.E * H * 1e12)
        d.append(((angp - ang0 + 90) % 180) - 90)
    d = np.array(d)
    return dict(std_deg=float(d.std()), max_abs_deg=float(np.abs(d).max()))


def theta_max(active, df_hz, fbar):
    """Largest tilt t in [0, 45] deg away from the surface axes with vmax_unclipped <= 10 V, by bisection
    (20 steps), tried from both ends (theta = t: higher mode near x; theta = 90 - t: higher mode near z).
    Returns the larger of the two, or None if neither end fits even at t = 0."""
    best = None
    for side in (0.0, 90.0):
        def fits(t):
            th = t if side == 0.0 else 90.0 - t
            return fixed_solve(active, th, df_hz, fbar, dc_limit=1e9)[1]["vmax"] <= DC_LIMIT
        if not fits(0.0):
            continue
        lo, hi = 0.0, 45.0
        for _ in range(20):
            mid = 0.5 * (lo + hi)
            if fits(mid):
                lo = mid
            else:
                hi = mid
        best = lo if best is None else max(best, lo)
    return None if best is None else float(best)


summary = {}
for zname, y in ZONE_Y.items():
    r = rf_null(els, ["1"], y=float(y), z_range=(15, 150))
    p = np.array([r["x"], y, r["z"]])
    T_ZONE = tc.taylor_all(els, p)
    _, _, Hrf = tc.sum_taylor(T_ZONE, {"1": 1.0})
    _, _, KPSI = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    phi = {n: abs(T_ZONE[n][0]) for n in dc_names}
    sets = {"n14": sorted(dc_names, key=lambda n: -phi[n])[:N_ACTIVE],
            "all": dc_names,
            "all_no2": [n for n in dc_names if n != "2"]}
    recs, rob, bis = [], [], []
    for setname, active in sets.items():
        for th in NATURAL_THETAS:
            _, info = natural_solve(T_ZONE, active, th)
            _, info_u = natural_solve(T_ZONE, active, th, dc_limit=1e9)
            recs.append(record(zname, "natural", setname, th, None, info, info_u["vmax"]))
        fbar = fbar_of(active)
        for th in FIXED_THETAS:
            for df in DFS:
                _, info = fixed_solve(active, th, df * 1e6, fbar)
                _, info_u = fixed_solve(active, th, df * 1e6, fbar, dc_limit=1e9)
                recs.append(record(zname, "fixed split", setname, th, df, info, info_u["vmax"]))
        if setname in ("n14", "all"):
            for df in DFS:
                V, info = fixed_solve(active, 45, df * 1e6, fbar)
                if info["bounded"]:
                    bis.append(dict(set=setname, df_MHz=df, fits_45=False,
                                    theta_max_fit=theta_max(active, df * 1e6, fbar)))
                else:
                    rob.append(dict(set=setname, df_MHz=df, nominal_angle_deg=float(radial(info["K"])[0]),
                                    **robustness(active, V, radial(info["K"])[0])))
                    bis.append(dict(set=setname, df_MHz=df, fits_45=True, theta_max_fit=45.0))
    summary[zname] = dict(y=float(y), null_x=float(r["x"]), null_z=float(r["z"]),
                          records=recs, robustness=rob, theta_max_fit=bis)

print(f"{'zone':8s} {'set':8s} {'method':12s} {'theta':>5s} {'df':>5s} {'vmax_unc':>9s} {'bnd':>5s} "
      f"{'angle':>7s} {'split':>6s} {'f_ax':>6s}")
for zname in summary:
    for rec in summary[zname]["records"]:
        df = "-" if rec["df_target"] is None else f"{rec['df_target']:.1f}"
        print(f"{zname:8s} {rec['set']:8s} {rec['method']:12s} {rec['theta_target']:5.1f} {df:>5s} "
              f"{rec['vmax_unclipped']:9.3f} {str(rec['bounded']):>5s} {rec['angle_deg']:7.2f} "
              f"{rec['split_MHz']:6.3f} {rec['f_axial_MHz']:6.3f}")
for zname in summary:
    for rb in summary[zname]["robustness"]:
        print(f"robustness {zname} {rb['set']} df={rb['df_MHz']} MHz: nominal {rb['nominal_angle_deg']:.2f} deg, "
              f"std {rb['std_deg']:.3f} deg, max |change| {rb['max_abs_deg']:.3f} deg")
for zname in summary:
    for bm in summary[zname]["theta_max_fit"]:
        print(f"theta_max_fit {zname} {bm['set']} df={bm['df_MHz']} MHz: fits_45={bm['fits_45']}, "
              f"theta_max_fit={bm['theta_max_fit']}")

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)

# plot 1: unclipped minimum-norm vmax vs target angle, fixed split n14
fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, zname in zip(axs, ZONE_Y):
    recs = [r for r in summary[zname]["records"]
            if r["method"] == "fixed split" and r["set"] == "n14"]
    for df in DFS:
        rows = sorted([r for r in recs if abs(r["df_target"] - df) < 1e-9], key=lambda r: r["theta_target"])
        ax.plot([r["theta_target"] for r in rows], [r["vmax_unclipped"] for r in rows], "o-", ms=3,
                label=f"df = {df} MHz")
    ax.axhline(DC_LIMIT, color="k", ls="--", lw=1, label="10 V limit")
    ax.set(xlabel="theta: higher-frequency radial mode from in-plane x (deg); 90 = vertical", title=f"{zname} zone, fixed split, n14")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
axs[0].set(ylabel="max |V|, unclipped minimum norm (V)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "vmax_vs_theta.png"), dpi=140)

# plot 2: projection of k_hat on the two radial modes vs target angle, readout, df = 0.3 MHz, n14
rows = sorted([r for r in summary["readout"]["records"]
               if r["method"] == "fixed split" and r["set"] == "n14" and abs(r["df_target"] - 0.3) < 1e-9],
              key=lambda r: r["theta_target"])
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([r["theta_target"] for r in rows], [r["projections"][2]["proj"] for r in rows], "o-", ms=3,
        label=f"higher-frequency radial mode ({rows[0]['projections'][2]['f_MHz']:.2f} MHz at theta 0)")
ax.plot([r["theta_target"] for r in rows], [r["projections"][1]["proj"] for r in rows], "s-", ms=3,
        label=f"lower-frequency radial mode ({rows[0]['projections'][1]['f_MHz']:.2f} MHz at theta 0)")
ax.set(xlabel="target angle theta (deg)", ylabel="(k_hat . e)^2 (dimensionless)",
       title="readout zone, fixed split df = 0.3 MHz, n14")
ax.grid(alpha=0.3)
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "projection_vs_theta.png"), dpi=140)
