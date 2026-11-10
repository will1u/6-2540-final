"""28 - Fixed-split radial tilt on 3-D (gds2itvg) potentials for several electrode geometry variants
(Claude-authored).

Sim 25's fixed-split analysis, run on each geometry written by trapgeom.py (stack "v4"), one variant per run.
Question: which electrode geometry gives a radial-mode tilt above 20 deg at a radial split >= 0.2 MHz with
DC within +-10 V, at 0.8 MHz axial (or the --fax value)?

Usage (from design/sim):
  ./run.sh run_cached_geometry.py 28_tilt_geometry_3d.py G0
  ./run.sh run_cached_geometry.py 28_tilt_geometry_3d.py G1_gap5 --window
  ./run.sh 28_tilt_geometry_3d.py --collect
Outputs: out/28_tilt_geometry_3d/<TAG>/ (geom.gds, geom.json, summary.json), TAG = variant, plus _fax<f>
and _win when given. --collect writes out/28_tilt_geometry_3d/frontier.png and frontier.json.

Method (copied from sim 25, not imported): every DC electrode is active (every name except the RF "1" and
the ground keys 97, 98, 99; no n14 set). fbar = mean radial frequency of the untilted clipped solve.
Fixed split: total K_xx - K_zz = dK cos(2 theta), K_xz = dK sin(2 theta) / 2, dK from f1, f2 = fbar +- df/2.
Clipped solves at +-10 V; vmax_unclipped is the minimum-norm solve without the clip.
theta_max: bisection on vmax_unclipped <= 10 V over [0, 45] deg tilt from the surface axes, from both ends.
"""

import glob
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null

import trapcalc as tc
import trapgeom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "out", "28_tilt_geometry_3d")
SIM25_UNIFORM = os.path.join(HERE, "out", "25_radial_tilt_sweep", "trap_die_v4_UNIFORM", "summary.json")

ARGV = sys.argv[1:]
FAX_ARG = [a for a in ARGV if a.startswith("--fax=")]
F_AX = float(FAX_ARG[0].split("=")[1]) * 1e6 if FAX_ARG else 0.8e6
WINDOW = "--window" in ARGV
ARGS = [a for a in ARGV if not a.startswith("--")]

# common geometry (all variants start from V4)
V4 = dict(c=40.0, a=84.0, g=5.0, half_len=2000.0, dc_depth=200.0, seg_w=115.0, n_seg=15, seg_x0=-897.5)
VARIANTS = {
    "G0": {},
    "G1_gap5": dict(c_split_gap=5.0),
    "G1s_slot": dict(c_split_gap=25.0, c_split_leads=True),
    "G2_local": dict(c_split_x=[(-300.0, -180.0), (180.0, 300.0)]),
    "G3_d0.3": dict(a_top=121.44, a_bot=65.39),
    "G3_d0.5": dict(a_top=175.17, a_bot=58.39),
    "G4_c60_gap5": dict(c=60.0, a=39.42, c_split_gap=5.0),
    "G4_c30_gap5": dict(c=30.0, a=120.36, c_split_gap=5.0),
    "G5_p60": dict(seg_w=55.0, n_seg=31, seg_x0=-927.5),
    "G5_p96": dict(seg_w=91.0, n_seg=20, seg_x0=-957.5),
    "G5_p160": dict(seg_w=155.0, n_seg=12, seg_x0=-957.5),
    "G5_p240": dict(seg_w=235.0, n_seg=9, seg_x0=-1077.5),
}

V_RF, F_RF = 53.0, tc.F_RF
DC_LIMIT = 10.0
M = tc.M_BA138
KHAT = np.array([1.0, 1.0, 0.0]) / np.sqrt(2.0)
ZONE_Y = {"loading": -240.0, "readout": 240.0}      # ITVG y = GDS x
DFS = [0.1, 0.2, 0.3, 0.5]                          # MHz
ROB_DFS = [0.1, 0.2]
EXCLUDE = ("1", "97", "98", "99")                   # RF, SNSPD lead strips (ground), ground


def fl(x):
    return None if x is None else float(x)


def radial(K):
    """Angle (deg) of the higher-frequency radial mode from +x toward +z, and the radial split (Hz)."""
    ev, evec = np.linalg.eigh(K[np.ix_([0, 2], [0, 2])])
    v = evec[:, np.argmax(ev)]
    ang = np.degrees(np.arctan2(v[1], v[0]))
    if ang > 90:
        ang -= 180
    if ang <= -90:
        ang += 180
    f = np.sign(ev) * np.sqrt(np.abs(ev) / M) / (2 * np.pi)
    return ang, f.max() - f.min()


def solve(T, active, tilt=0.0, extra=None, dc_limit=DC_LIMIT):
    return tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF,
                       dc_limit=dc_limit, tilt_xz=tilt, extra_rows=extra)


def natural_solve(T, active, theta, dc_limit=DC_LIMIT):
    # sim 12 rule: the untilted solve is always clipped
    _, info0 = solve(T, active)
    dk = info0["K"][2, 2] - info0["K"][0, 0]
    kxz = 0.5 * np.tan(2 * np.deg2rad(theta)) * dk / tc.E / 1e12
    return solve(T, active, tilt=kxz, dc_limit=dc_limit)


def fbar_of(active):
    """Mean of the two radial frequencies (Hz) from the untilted clipped solve (uses global T_ZONE)."""
    _, info0 = solve(T_ZONE, active)
    return np.sort(info0["freqs"])[1:].mean()


def fixed_solve(active, theta, df_hz, fbar, dc_limit=DC_LIMIT):
    """Fixed split solve (uses globals T_ZONE, KPSI). df_hz = 0 gives the axial-only solve."""
    f1, f2 = fbar + df_hz / 2, fbar - df_hz / 2
    dK = M * (2 * np.pi) ** 2 * (f1 ** 2 - f2 ** 2)
    th = np.deg2rad(theta)
    hxz = (0.5 * dK * np.sin(2 * th) - KPSI[0, 2]) / (tc.E * 1e12)
    hdiff = (dK * np.cos(2 * th) - (KPSI[0, 0] - KPSI[2, 2])) / (tc.E * 1e12)
    row = np.array([[T_ZONE[n][2][0, 0] - T_ZONE[n][2][2, 2] for n in active]])
    return solve(T_ZONE, active, tilt=hxz, extra=(row, np.array([hdiff])), dc_limit=dc_limit)


def rec(label, df, theta, info, vmax_unc):
    """One stored solve: clipped info (checks, angle) plus the unclipped vmax."""
    ang, split = radial(info["K"])
    return dict(label=label, df_MHz=fl(df), theta_target_deg=fl(theta), vmax_unclipped=fl(vmax_unc),
                vmax_clipped=fl(info["vmax"]), bounded_at_10V=bool(info["bounded"]),
                angle_deg=fl(ang), split_MHz=fl(split / 1e6), freqs_MHz=[fl(x) for x in np.sort(info["freqs"]) / 1e6],
                f_axial_MHz=fl(info["f_axial"] / 1e6), residual_field_V_per_um=fl(info["residual_field"]),
                all_curvatures_positive=bool(np.all(np.linalg.eigvalsh(info["K"]) > 0)))


def robustness(active, V, ang0):
    """Angle scatter (deg) for 200 draws of 10 mV Gaussian errors on every active voltage (seed 0)."""
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
    """Largest tilt t (deg from the surface axes, 0..45) with vmax_unclipped <= 10 V, by bisection (20 steps),
    from both ends (theta = t, or theta = 90 - t). Returns (t, theta used) for the larger t, or None."""
    best = None
    for side in (0.0, 90.0):
        def th_of(t, side=side):
            return t if side == 0.0 else 90.0 - t

        def fits(t):
            return fixed_solve(active, th_of(t), df_hz, fbar, dc_limit=1e9)[1]["vmax"] <= DC_LIMIT
        if not fits(0.0):
            continue
        lo, hi = 0.0, 45.0
        for _ in range(20):
            mid = 0.5 * (lo + hi)
            if fits(mid):
                lo = mid
            else:
                hi = mid
        if best is None or lo > best[0]:
            best = (lo, th_of(lo))
    return best


def collect():
    """Read every summary.json under out/28_tilt_geometry_3d and write frontier.png / frontier.json."""
    runs = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*", "summary.json"))):
        runs.append(json.load(open(path)))
    if not runs:
        raise SystemExit("no summary.json found under " + ROOT)
    rows = []
    for s in runs:
        for zname, z in s["zones"].items():
            rows.append(dict(
                tag=s["tag"], variant=s["variant"], zone=zname, fax_MHz=s["fax_MHz"], window=s["window"],
                axial_only_V=z["axial_only"]["vmax_unclipped"],
                dV_per_0p1MHz_45=z["dV_per_0p1MHz_45"],
                theta_max_deg={k: v["theta_max_deg"] for k, v in z["df"].items()},
                null_z_um=z["null_z"], null_x_um=z["null_x"]))
    with open(os.path.join(ROOT, "frontier.json"), "w") as fh:
        json.dump(rows, fh, indent=1)

    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, zname in zip(axs, ZONE_Y):
        for s in runs:
            z = s["zones"][zname]
            ys = [np.nan if z["df"][f"{d:g}"]["theta_max_deg"] is None else z["df"][f"{d:g}"]["theta_max_deg"]
                  for d in DFS]
            ax.plot(DFS, ys, "o-", ms=3, label=s["tag"])
        ax.axhline(20.0, color="k", ls="--", lw=1)
        ax.set(xlabel="radial split df (MHz)", title=f"{zname} zone (fixed split, all DC electrodes)")
        ax.grid(alpha=0.3)
    axs[0].set(ylabel="theta_max (deg, tilt from surface axes)")
    axs[1].legend(fontsize=6, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "frontier.png"), dpi=140)

    print(f"{'variant':20s} {'zone':8s} {'axial-only V':>12s} {'V/0.1MHz@45':>11s} "
          f"{'tmax 0.1':>8s} {'tmax 0.2':>8s} {'tmax 0.3':>8s} {'tmax 0.5':>8s} {'null z':>7s} {'null x':>8s}")
    for r in rows:
        tm = r["theta_max_deg"]

        def t(k):
            return "None" if tm[k] is None else f"{tm[k]:.2f}"
        print(f"{r['tag']:20s} {r['zone']:8s} {r['axial_only_V']:12.3f} {r['dV_per_0p1MHz_45']:11.3f} "
              f"{t('0.1'):>8s} {t('0.2'):>8s} {t('0.3'):>8s} {t('0.5'):>8s} "
              f"{r['null_z_um']:7.3f} {r['null_x_um']:8.3f}")


if "--collect" in ARGV:
    collect()
    sys.exit(0)

VARIANT = ARGS[0] if ARGS else None
if VARIANT not in VARIANTS:
    raise SystemExit("usage: 28_tilt_geometry_3d.py <VARIANT> [--fax=0.6] [--window] | --collect; variants: "
                     + ", ".join(VARIANTS))
TAG = VARIANT + (f"_fax{F_AX / 1e6:g}" if FAX_ARG else "") + ("_win" if WINDOW else "")
OUT = os.path.join(ROOT, TAG)
os.makedirs(OUT, exist_ok=True)

P = {**V4, **VARIANTS[VARIANT]}
if WINDOW:
    P["window"] = dict(x=240.0, wx=30.0, wy=30.0, kind="open")
gds, js, info = trapgeom.write(os.path.join(OUT, "geom"), P, stack="v4")

# every seg centre must sit on the zones (ITVG y = GDS x = -240, +240): asserted for the G5 pitch variants
for zname, xg in (("loading", -240.0), ("readout", 240.0)):
    assert any(abs(c - xg) < 1e-6 for c in info["seg_centres"]), f"no segment centre at GDS x = {xg}"

lay = Layout.from_json(js)
els, _ = build_electrodes(gds, lay, ion_box=(-30, 30, -400, 400), ion_z=(25, 90), return_ground=True)
dc_names = [n for n in els if n not in EXCLUDE]
N = P["n_seg"]
expected = {"1"} | set(info["centre_names"]) | {str(k) for k in range(3, 2 * N + 7)}
missing = sorted(expected - set(els), key=int)
extra = sorted(set(els) - expected - {"1"}, key=lambda s: int(s))
print(f"{TAG}: {len(dc_names)} DC electrodes active; missing from build_electrodes: {missing or 'none'}; "
      f"not in expected list: {extra or 'none'}; ground keys present in els: "
      f"{[k for k in ('97', '98', '99') if k in els]}")
active = dc_names
print(f"f_axial target {F_AX / 1e6:g} MHz; window {'open 30x30 um at readout' if WINDOW else 'none'}")

summary = dict(variant=VARIANT, tag=TAG, fax_MHz=F_AX / 1e6, window=WINDOW, params=P,
               missing_electrodes=missing, zones={})
T_ZONE, KPSI = None, None
for zname, y in ZONE_Y.items():
    r = rf_null(els, ["1"], y=float(y), z_range=(15, 150))
    p = np.array([r["x"], y, r["z"]])
    T_ZONE = tc.taylor_all(els, p)
    _, _, Hrf = tc.sum_taylor(T_ZONE, {"1": 1.0})
    f_rf_only, _, KPSI = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    rf_ang, _ = radial(KPSI)
    fbar = fbar_of(active)
    z = dict(y=float(y), null_x=fl(r["x"]), null_z=fl(r["z"]), null_residual_V_per_um=fl(r["field"]),
             rf_only_freqs_MHz=[fl(x / 1e6) for x in np.sort(f_rf_only)], rf_only_angle_deg=fl(rf_ang),
             fbar_MHz=fl(fbar / 1e6), df={}, records=[])

    if VARIANT == "G0":
        _, nu = natural_solve(T_ZONE, active, 10, dc_limit=1e9)
        _, nc = natural_solve(T_ZONE, active, 10)
        z["natural10"] = rec("natural 10 deg", None, 10, nc, nu["vmax"])
        z["records"].append(z["natural10"])

    Vax, au = fixed_solve(active, 45, 0.0, fbar, dc_limit=1e9)
    _, ac = fixed_solve(active, 45, 0.0, fbar)
    z["axial_only"] = rec("axial only (df 0, 45 deg)", 0.0, 45, ac, au["vmax"])
    z["records"].append(z["axial_only"])
    ax_V = au["vmax"]

    for df in DFS:
        Vu, iu = fixed_solve(active, 45, df * 1e6, fbar, dc_limit=1e9)
        _, ic = fixed_solve(active, 45, df * 1e6, fbar)
        tm = theta_max(active, df * 1e6, fbar)
        d = dict(v45_unclipped=fl(iu["vmax"]), fits_45=bool(iu["vmax"] <= DC_LIMIT),
                 theta_max_deg=None if tm is None else fl(tm[0]),
                 theta_used_deg=None if tm is None else fl(tm[1]), robustness=None)
        if df in ROB_DFS:
            if d["fits_45"]:
                ang45 = radial(iu["K"])[0]
                d["robustness"] = dict(at="45 deg", **robustness(active, Vu, ang45), nominal_angle_deg=fl(ang45))
            elif tm is not None:
                Vt, it = fixed_solve(active, tm[1], df * 1e6, fbar, dc_limit=1e9)
                angt = radial(it["K"])[0]
                d["robustness"] = dict(at=f"theta_max, theta={tm[1]:.3f} deg", **robustness(active, Vt, angt),
                                       nominal_angle_deg=fl(angt))
        z["df"][f"{df:g}"] = d
        z["records"].append(rec("fixed split 45 deg", df, 45, ic, iu["vmax"]))
        if abs(df - 0.1) < 1e-9:
            z["dV_per_0p1MHz_45"] = fl(iu["vmax"] - ax_V)

    z["all_curvatures_positive"] = all(x["all_curvatures_positive"] for x in z["records"])
    z["max_residual_field_V_per_um"] = max(x["residual_field_V_per_um"] for x in z["records"])
    z["bounded_axial_only"] = z["axial_only"]["bounded_at_10V"]
    summary["zones"][zname] = z

    print(f"\n[{zname}] y = {y:g} um, null x = {r['x']:.3f} um, null z = {r['z']:.3f} um (target 50)")
    print(f"  RF-only radial freqs (MHz) {np.round(np.sort(f_rf_only) / 1e6, 4)}, RF-only angle {rf_ang:.2f} deg")
    print(f"  fbar = {fbar / 1e6:.4f} MHz")
    if "natural10" in z:
        print(f"  natural 10 deg: vmax_unclipped {nu['vmax']:.3f} V (clipped bounded {nc['bounded']})")
    print(f"  axial only: vmax_unclipped {ax_V:.3f} V, clipped bounded {ac['bounded']}, "
          f"f_axial {ac['f_axial'] / 1e6:.4f} MHz, residual {ac['residual_field']:.2e} V/um")
    if "dV_per_0p1MHz_45" in z:
        print(f"  V per 0.1 MHz at 45 deg (vmax_unclipped(0.1) - axial only): {z['dV_per_0p1MHz_45']:.3f} V")
    for k, d in z["df"].items():
        tmv = "None" if d["theta_max_deg"] is None else f"{d['theta_max_deg']:.3f} (theta {d['theta_used_deg']:.3f})"
        print(f"  df {k} MHz: 45 deg vmax_unclipped {d['v45_unclipped']:.3f} V, fits {d['fits_45']}, "
              f"theta_max {tmv}")
        if d["robustness"] is not None:
            rb = d["robustness"]
            print(f"    robustness at {rb['at']}: nominal {rb['nominal_angle_deg']:.2f} deg, std {rb['std_deg']:.3f}, "
                  f"max |change| {rb['max_abs_deg']:.3f} deg")
    print(f"  all curvatures positive: {z['all_curvatures_positive']}; max residual field "
          f"{z['max_residual_field_V_per_um']:.2e} V/um; axial-only bounded at 10 V: {z['bounded_axial_only']}")

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
print(f"\nwrote {os.path.join(OUT, 'summary.json')}")

if VARIANT == "G0":
    if FAX_ARG or WINDOW:
        print("ACCEPTANCE skipped: the sim 25 reference is at 0.8 MHz without the window")
    else:
        u = json.load(open(SIM25_UNIFORM))["loading"]
        ref_nat = [r for r in u["records"] if r["set"] == "all" and r["method"] == "natural"
                   and r["theta_target"] == 10][0]["vmax_unclipped"]
        ref_45 = [r for r in u["records"] if r["set"] == "all" and r["method"] == "fixed split"
                  and r["theta_target"] == 45 and r["df_target"] == 0.1][0]["vmax_unclipped"]
        ref_tm = {round(b["df_MHz"], 2): b["theta_max_fit"] for b in u["theta_max_fit"] if b["set"] == "all"}
        mine_tm = {k: v["theta_max_deg"] for k, v in summary["zones"]["loading"]["df"].items()}
        pairs = [("natural 10 deg vmax (V)", ref_nat, summary["zones"]["loading"]["natural10"]["vmax_unclipped"]),
                 ("45 deg 0.1 MHz vmax_unclipped (V)", ref_45, summary["zones"]["loading"]["df"]["0.1"]["v45_unclipped"]) ]
        pairs = [(a, b, c) for a, b, c in pairs]
        for k in ("0.1", "0.2", "0.3", "0.5"):
            pairs.append((f"theta_max df {k} MHz (deg)", ref_tm[float(k)], mine_tm[k]))
        print("\nACCEPTANCE (sim 25 UNIFORM, loading zone, set 'all' vs G0 loading):")
        bad = False
        for name, ref, mine in pairs:
            if mine is None:
                print(f"  {name:36s} ref {ref:9.3f}  G0 None  -> FAIL")
                bad = True
                continue
            dev = 100 * (mine - ref) / ref
            flag = "" if abs(dev) <= 15 else "  > 15 %"
            bad = bad or abs(dev) > 15
            print(f"  {name:36s} ref {ref:9.3f}  G0 {mine:9.3f}  {dev:+7.1f} %{flag}")
        print("ACCEPTANCE " + ("FAIL: a deviation is above 15 %, do not run the other variants" if bad
                               else "PASS (all within 15 %)"))
