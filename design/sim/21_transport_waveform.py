"""21 - Playable transport waveform (Claude-authored).

Question: can the 10 um static DC table of sim 12 become a voltage-versus-time waveform that a
DAC could play, and what motional energy does the move leave in the ion (classical model)?

Steps:
  1. Static DC solves every DY um along the trap axis (the sim 12 transport solve, zero tilt).
  2. One cubic spline through them, per electrode.
  3. Checks: (A) agreement with sim 12's own table; (B) interpolation error at the midpoints,
     evaluated from the Taylor expansion of the potential; (C) tilt hand-off at both zones, a
     blend from the transport set to the regular (tilted) zone set.
  4. Minimum-jerk move with an un-tilt at loading and a tilt at readout, quantised to a 16 bit DAC.
  5. DAC update-rate table and the classical axial energy left after the move (as sim 20).

Model: gds2itvg unit potentials on layer 50 of the v4 die named by the *_sim.json (sim-only
floor files are used when the layout names one). trapcalc.py gives the Taylor expansion and the DC
solve. The RF null comes from gds2itvg rf_null.
Inputs: gds/<json>; out/12_final_chip/<TAG>/waveforms.csv and summary.json (reference);
out/12_final_chip/<stem>/summary.json (regular zone sets); out/20_transport_timing/summary.json (x0).
Outputs: out/21_transport_waveform/<TAG>/ (static_fine.csv, static_fine_info.csv, check_interp.png,
waveform.csv, waveform.png, summary.json).
Usage: ./run.sh 21_transport_waveform.py [path/to/_sim.json] [--centre-dc-zero]
Limitations: classical motion only; the electrode filter corners and the DAC parameters are
[verify]; the staircase and filter model are [inference] (same as sim 20); no trajectory optimisation.
"""

import csv
import json
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.signal import lfilter
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
JS = ARGS[0] if ARGS else os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json")
LAYOUT = json.load(open(JS))
GDS = os.path.join(os.path.dirname(JS), LAYOUT["_gds"]) if "_gds" in LAYOUT else JS.replace("_sim.json", ".gds")
# --centre-dc-zero: electrode 2 held at 0 V (same as sim 12)
FIX2 = "--centre-dc-zero" in sys.argv
STEM = os.path.basename(JS).replace("_sim.json", "")
TAG = STEM + ("_V2zero" if FIX2 else "")
OUT = os.path.join(HERE, "out", "21_transport_waveform", TAG)
OUT12 = os.path.join(HERE, "out", "12_final_chip", TAG)
OUT12_REG = os.path.join(HERE, "out", "12_final_chip", STEM)   # regular zone sets (no flag)
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- constants
V_RF, F_RF = 53.0, tc.F_RF            # as sim 12
F_AX = 0.8e6                          # Hz
DC_LIMIT = 10.0                       # V, DAC range
N_ACTIVE = 14                         # zone solves, as sim 12
ZONES = LAYOUT["_zones"]
X_LOAD, X_READ = ZONES["loading_itvg_y"], ZONES["readout_itvg_y"]   # ITVG y, um
D_UM = X_READ - X_LOAD                # 480 um move
TILT_DEG = 10.0
DY = 2.0                              # um, static solve spacing (DY_FALLBACK only if the estimate is > 40 min)
DY_FALLBACK = 5.0
T_MOVE = 1e-3                         # s  [inference] sim 20: minimum-jerk leaves < 0.1 quanta above 44 us
T_TILT = 100e-6                       # s  [inference] time to ramp the tilt in or out
F_DAC = 1e6                           # Hz update rate            [verify] lab DAC hardware not confirmed
DAC_BITS, DAC_RANGE = 16, 20.0        # 16 bit over -10..+10 V    [verify]
LSB = DAC_RANGE / 2 ** DAC_BITS
F_FILT = (50e3, 200e3)                # Hz first-order filter corners to try [verify]
SCAN_T = (100e-6, 300e-6, 1e-3)       # s
SCAN_F = (100e3, 1e6)                 # Hz

M = tc.M_BA138                        # kg
HBAR = 1.054571817e-34                # J s
W = 2 * np.pi * F_AX                  # rad/s
EQ = HBAR * W                         # J
DT_MAX = 1.0 / (400 * F_AX)           # s, same time step rule as sim 20
D20 = 480e-6                          # m, sim 20 move (used only by its analytic staircase formula)

# ---------------------------------------------------------------- setup (as sim 12)
lay = Layout.from_json(JS)
els, gnd = build_electrodes(GDS, lay, ion_box=(-20, 20, -900, 350), ion_z=(25, 90), return_ground=True)
dc_z = sorted([n for n in els if n != "1"], key=int)                       # zone electrodes
dc_t = [n for n in dc_z if not (FIX2 and n == "2")]                        # transport electrodes
zi = [dc_z.index(n) for n in dc_t]                                        # dc_t inside dc_z order


def to_z(vec_t):
    """Put a vector over dc_t into dc_z order (electrode 2, when held, stays 0)."""
    out = np.zeros(len(dc_z))
    out[zi] = vec_t
    return out


def zone(y_ion, tilt_deg=TILT_DEG, active=None):
    """DC set at one axial position (sim 12 zone()). active=None: the N_ACTIVE strongest electrodes."""
    r = rf_null(els, ["1"], y=float(y_ion), z_range=(15, 150))
    p = np.array([r["x"], y_ion, r["z"]])
    T = tc.taylor_all(els, p)
    if active is None:
        phi_ion = {n: abs(T[n][0]) for n in dc_z}
        active = sorted(dc_z, key=lambda n: -phi_ion[n])[:N_ACTIVE]
    if tilt_deg == 0.0:
        kxz = 0.0            # the first solve of sim 12 only supplies K for the tilt; zero tilt needs none
    else:
        _, info0 = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT)
        dk = info0["K"][2, 2] - info0["K"][0, 0]
        kxz = 0.5 * np.tan(2 * np.deg2rad(tilt_deg)) * dk / tc.E / 1e12
    V, info = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT,
                          tilt_xz=kxz)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    f_rf, q, _ = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    ev, evec = np.linalg.eigh(info["K"][np.ix_([0, 2], [0, 2])])
    ang = np.degrees(np.arctan2(evec[1, 0], evec[0, 0]))
    return dict(y=y_ion, p=p, z=r["z"], x=r["x"], V={n: V.get(n, 0.0) for n in dc_z}, info=info,
                f_rf=np.sort(f_rf), q=q.max(), tilt_angle=ang)


def nbar_from_integral(I):
    """nbar = (m/2) |I|^2 / (hbar w), with I = integral of s'' exp(i w t) dt (sim 20)."""
    return 0.5 * M * np.abs(I) ** 2 / EQ


def trapz_uniform(y, dt):
    """Trapezoid rule on a uniform grid (as sim 20)."""
    return dt * (np.sum(y) - 0.5 * (y[0] + y[-1]))


def staircase_nbar_analytic(N, T, f_filt):
    """Closed form of sim 20 (copied): exact jump times t_k = k T/N, d = D20/N."""
    d = D20 / N
    tau = 1.0 / (2 * np.pi * f_filt)
    S = np.sum(np.exp(1j * W * np.arange(N) * T / N))
    return float(0.5 * M * W ** 2 * d ** 2 * np.abs(S) ** 2 / (EQ * (1 + (W * tau) ** 2)))


def nbar_held(s_um, F, f_filt):
    """Positions s_um[k] are applied at t = k/F and held until the next update (last one held on).
    Filtered by a first-order low-pass of corner f_filt (exact discrete form, grid dt = 1/(F K) so the
    update times fall on the grid). Returns nbar of the axial motion left after the sequence.
    [inference] same assumptions as sim 20: the well centre follows the filtered voltage linearly."""
    dt_u = 1.0 / F
    K = int(np.ceil(dt_u / DT_MAX))
    dt = dt_u / K
    tau = 1.0 / (2 * np.pi * f_filt)
    a = np.exp(-dt / tau)
    t_end = (len(s_um) - 1) / F + 10 * tau
    pad = 4                                              # zero samples before t = 0
    n = pad + int(np.ceil(t_end / dt)) + 1
    t = (np.arange(n) - pad) * dt
    idx = np.clip(np.floor(t * F + 1e-9).astype(int), 0, len(s_um) - 1)
    x = np.where(t >= 0, s_um[idx], 0.0) * 1e-6          # um -> m
    s = lfilter([1.0 - a], [1.0, -a], x)
    s2 = np.gradient(np.gradient(s, dt), dt)
    return float(nbar_from_integral(trapz_uniform(s2 * np.exp(1j * W * t), dt)))


def mj(u):
    """Minimum-jerk shape: 0 at u = 0, 1 at u = 1."""
    return 10 * u ** 3 - 15 * u ** 4 + 6 * u ** 5


def quant(V):
    return np.round(V / LSB) * LSB


# ---------------------------------------------------------------- time the solves, choose DY
t0 = time.time()
for y in (X_LOAD, X_LOAD + 2.0, X_LOAD + 4.0):
    zone(y, 0.0, dc_t)
per = (time.time() - t0) / 3
n_static = int(round(D_UM / DY)) + 1
est_min = per * (2 * n_static) / 60
print(f"[{TAG}] {per:.2f} s per zone solve (3 positions); DY = {DY} um gives about {est_min:.1f} min "
      f"({n_static} static solves + {n_static - 1} midpoint checks)", flush=True)
DY_USED = DY
if est_min > 40.0:
    DY_USED = DY_FALLBACK
    print(f"estimate above 40 min: using DY = {DY_USED} um instead", flush=True)
ys = np.arange(X_LOAD, X_READ + DY_USED / 2, DY_USED)

# ---------------------------------------------------------------- step 2: static solves on the fine grid
n_y = len(ys)
Vs = np.zeros((n_y, len(dc_t)))              # over dc_t
Ks = np.zeros((n_y, 3, 3))
Pts = np.zeros((n_y, 3))
fax = np.zeros(n_y)
bnd = np.zeros(n_y, dtype=bool)
for i, y in enumerate(ys):
    zr = zone(y, 0.0, dc_t)
    Vs[i] = [zr["V"][n] for n in dc_t]
    Ks[i] = zr["info"]["K"]
    Pts[i] = zr["p"]
    fax[i] = zr["info"]["f_axial"]
    bnd[i] = zr["info"]["bounded"]
print(f"static solves done: {n_y} points, DY = {DY_USED} um, any bounded: {bool(bnd.any())}", flush=True)

with open(os.path.join(OUT, "static_fine.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["y_um"] + [f"V{n}" for n in dc_t])
    for y, row in zip(ys, Vs):
        w.writerow([f"{y:g}"] + [f"{v:.7f}" for v in row])
with open(os.path.join(OUT, "static_fine_info.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["y_um", "null_x_um", "null_z_um", "f_axial_MHz", "bounded"])
    for i, y in enumerate(ys):
        w.writerow([f"{y:g}", f"{Pts[i, 0]:.6f}", f"{Pts[i, 2]:.6f}", f"{fax[i] / 1e6:.6f}", int(bnd[i])])

spl = CubicSpline(ys, Vs, axis=0)           # one spline per electrode (columns)


def V_transport(y):
    """Spline transport set at y, in dc_z order."""
    return to_z(spl(y))


# ---------------------------------------------------------------- check A: sim 12 table
ref = np.genfromtxt(os.path.join(OUT12, "waveforms.csv"), delimiter=",", names=True)
ref_names = [nm[1:] for nm in ref.dtype.names[1:]]
assert set(ref_names) == set(dc_t), (sorted(ref_names), dc_t)
ry = ref[ref.dtype.names[0]]
Vref = np.column_stack([ref[nm] for nm in ref.dtype.names[1:]])
rows = np.array([int(np.argmin(np.abs(ys - y))) for y in ry])
assert np.allclose(ys[rows], ry, atol=1e-6)
idx_ref = [dc_t.index(n) for n in ref_names]
mine = Vs[rows][:, idx_ref]
checkA_maxdiff = float(np.abs(mine - Vref).max())
rows10 = mine
checkA_maxabs = float(np.abs(Vs[rows]).max())
checkA_step10 = float(np.abs(np.diff(Vs[rows], axis=0)).max())
ref12 = json.load(open(os.path.join(OUT12, "summary.json")))["transport"]
print(f"check A: max |diff| vs sim 12 table = {checkA_maxdiff:.2e} V; max |V| = {checkA_maxabs:.4f} V "
      f"(sim 12 {ref12['max_abs_V']:.4f}); max change per 10 um = {checkA_step10:.4f} V "
      f"(sim 12 {ref12['max_step_change_V']:.4f})", flush=True)

# ---------------------------------------------------------------- check B: interpolation error at midpoints
mids = ys[:-1] + DY_USED / 2
B_rows = []
for ym in mids:
    r = rf_null(els, ["1"], y=float(ym), z_range=(15, 150))
    p = np.array([r["x"], ym, r["z"]])
    T = tc.taylor_all(els, p)
    Vi = dict(zip(dc_t, spl(ym)))
    _, g, H = tc.sum_taylor(T, Vi)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    _, _, Kpsi = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    K = Kpsi + tc.E * H * 1e12
    dy = -tc.E * g[1] * 1e6 / K[1, 1]                    # m
    B_rows.append((ym, dy, np.sqrt(K[1, 1] / M) / (2 * np.pi), np.linalg.norm(g) * 1e6))
B = np.array(B_rows)
checkB = dict(max_abs_dy_nm=float(np.abs(B[:, 1]).max() * 1e9),
              axial_freq_MHz_min=float(B[:, 2].min() / 1e6), axial_freq_MHz_max=float(B[:, 2].max() / 1e6),
              max_abs_g_V_per_m=float(B[:, 3].max()), n_midpoints=len(mids))
checkB["max_freq_dev_rel"] = float(np.abs(B[:, 2] / F_AX - 1).max())
print(f"check B: max |dy| {checkB['max_abs_dy_nm']:.3f} nm; axial {checkB['axial_freq_MHz_min']:.6f}-"
      f"{checkB['axial_freq_MHz_max']:.6f} MHz; max |g| {checkB['max_abs_g_V_per_m']:.3e} V/m", flush=True)

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(B[:, 0], B[:, 1] * 1e9, "o-", ms=2.5, lw=0.8)
ax.axhline(0, color="k", lw=0.6)
ax.set(xlabel="ion position y (um)", ylabel="axial displacement from intended point (nm)",
       title=f"{TAG}: interpolation error (DY = {DY_USED:g} um)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "check_interp.png"), dpi=140)
plt.close(fig)

# ---------------------------------------------------------------- step 6: tilt hand-off at each zone
REG = json.load(open(os.path.join(OUT12_REG, "summary.json")))
handoff = {}
zone_bounded = {}
for name, y in (("loading", X_LOAD), ("readout", X_READ)):
    i = int(np.argmin(np.abs(ys - y)))
    Va = to_z(Vs[i])
    zb = zone(y)                                          # defaults: 10 deg tilt, 14 strongest of dc_z
    Vb = np.array([zb["V"][n] for n in dc_z])
    zone_bounded[name] = bool(zb["info"]["bounded"])
    T = tc.taylor_all(els, zb["p"])
    rows_b = []
    for s in np.linspace(0.0, 1.0, 11):
        Vsv = (1 - s) * Va + s * Vb
        _, g, H = tc.sum_taylor(T, dict(zip(dc_z, Vsv)))
        _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
        _, _, Kpsi = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
        K = Kpsi + tc.E * H * 1e12
        ev_all = np.linalg.eigvalsh(K)
        ev_r, evec = np.linalg.eigh(K[np.ix_([0, 2], [0, 2])])
        ang = np.degrees(np.arctan2(evec[1, 0], evec[0, 0]))
        rows_b.append(dict(s=round(float(s), 2), g_V_per_m=float(np.linalg.norm(g) * 1e6),
                           K_eig_J_per_m2=[float(v) for v in ev_all],
                           axial_MHz=float(np.sqrt(K[1, 1] / M) / (2 * np.pi) / 1e6) if K[1, 1] > 0 else None,
                           radial_MHz=[float(np.sign(v) * np.sqrt(abs(v) / M) / (2 * np.pi) / 1e6) for v in ev_r],
                           radial_axis_deg=float(ang), max_abs_V=float(np.abs(Vsv).max())))
    handoff[name] = dict(y=float(y), Va=Va, Vb=Vb, vmax_zone=float(zb["info"]["vmax"]),
                         vmax_sim12=float(REG[name]["vmax"]), table=rows_b)
    print(f"{name}: zone vmax {zb['info']['vmax']:.3f} V (sim 12 regular {REG[name]['vmax']}); "
          f"blend min eig > 0: {all(min(r['K_eig_J_per_m2']) > 0 for r in rows_b)}; "
          f"max |g| over blend {max(r['g_V_per_m'] for r in rows_b):.3e} V/m", flush=True)

# ---------------------------------------------------------------- step 7: waveform
n_tilt = int(round(T_TILT * F_DAC))
n_move = int(round(T_MOVE * F_DAC))
n_tot = 2 * n_tilt + n_move
Va_l, Vb_l = handoff["loading"]["Va"], handoff["loading"]["Vb"]
Va_r, Vb_r = handoff["readout"]["Va"], handoff["readout"]["Vb"]
wave_t, wave_ph, wave_y, wave_V = [], [], [], []
for k in range(n_tot + 1):
    if k < n_tilt:                                        # un-tilt at loading: blend 1 -> 0
        s = 1 - mj(k / n_tilt)
        V = (1 - s) * Va_l + s * Vb_l
        ph, y = "untilt", X_LOAD
    elif k <= n_tilt + n_move:                            # move, transport set, no tilt
        u = (k - n_tilt) / n_move
        y = X_LOAD + D_UM * mj(u)
        V = V_transport(y)
        ph = "move"
    else:                                                 # tilt in at readout: blend 0 -> 1
        u = min((k - n_tilt - n_move) / n_tilt, 1.0)
        s = mj(u)
        V = (1 - s) * Va_r + s * Vb_r
        ph, y = "tilt", X_READ
    wave_t.append(k / F_DAC * 1e6)
    wave_ph.append(ph)
    wave_y.append(y)
    wave_V.append(quant(V))
wave_t = np.array(wave_t)
wave_V = np.array(wave_V)
dac_ok = bool(np.abs(wave_V).max() <= DC_LIMIT + 1e-12)
with open(os.path.join(OUT, "waveform.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["t_us", "phase", "y_um"] + [f"V{n}" for n in dc_z])
    for t, ph, y, row in zip(wave_t, wave_ph, wave_y, wave_V):
        w.writerow([f"{t:g}", ph, f"{y:.4f}"] + [f"{v:.6f}" for v in row])
print(f"waveform: {len(wave_t)} samples, phases untilt {n_tilt}, move {n_move + 1}, tilt "
      f"{n_tilt}; max |V| {np.abs(wave_V).max():.4f} V; within DAC range: {dac_ok}", flush=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
for j, n in enumerate(dc_z):
    if np.abs(wave_V[:, j]).max() > 0.05:
        ax.plot(wave_t, wave_V[:, j], lw=0.9, label=n)
ax.set(xlabel="time (µs)", ylabel="voltage (V)")
ax.legend(fontsize=6, ncol=4)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "waveform.png"), dpi=140)
plt.close(fig)

# ---------------------------------------------------------------- step 8: DAC table for the move
dac_scan = []
for T in SCAN_T:
    for F in SCAN_F:
        N = int(round(T * F))
        kk = np.arange(N + 1)
        yk = X_LOAD + D_UM * mj(np.minimum(kk / F / T, 1.0))
        Vk = quant(np.array([V_transport(y) for y in yk]))
        dV = np.abs(np.diff(Vk, axis=0)).max()
        dy_step = np.abs(np.diff(yk)).max()
        dac_scan.append(dict(T_us=T * 1e6, F_kHz=F / 1e3, n_updates=N, max_dV_per_update_V=float(dV),
                             max_abs_V=float(np.abs(Vk).max()), max_step_um=float(dy_step),
                             max_slew_V_per_us=float(dV * F / 1e6)))
        print(f"DAC T={T*1e6:g} us F={F/1e3:g} kHz: N={N}, max dV {dV:.4f} V, max dy {dy_step:.3f} um, "
              f"slew {dV * F / 1e6:.3f} V/us, max|V| {np.abs(Vk).max():.3f} V", flush=True)

# ---------------------------------------------------------------- step 9: quantisation at loading
T_load = tc.taylor_all(els, Pts[0])
K_load = Ks[0]
sens = np.array([-tc.E * T_load[n][1][1] * 1e6 / K_load[1, 1] for n in dc_t])     # m per V
quant_max_nm = float(np.abs(sens).max() * LSB * 1e9)
quant_rss_nm = float(np.sqrt(np.sum((sens * LSB) ** 2)) * 1e9)
x0_nm = float(json.load(open(os.path.join(HERE, "out", "20_transport_timing", "summary.json")))["x0_nm"])
print(f"quantisation at loading: largest |dy/dV| x lsb = {quant_max_nm:.4f} nm, RSS = {quant_rss_nm:.4f} nm "
      f"(zero-point x0 = {x0_nm:.3f} nm, sim 20)", flush=True)

# ---------------------------------------------------------------- step 10: motion left after the move
nbar_scan = {}
for T in SCAN_T:
    for F in SCAN_F:
        N = int(round(T * F))
        kk = np.arange(N + 1)
        s_um = D_UM * mj(np.minimum(kk / F / T, 1.0))
        for f in F_FILT:
            key = f"T{T*1e6:g}us_F{F/1e3:g}kHz_f{f/1e3:g}kHz"
            nbar_scan[key] = nbar_held(s_um, F, f)
            print(f"nbar {key}: {nbar_scan[key]:.4e}", flush=True)

# cross-check: uniform staircase, 480 steps of 1 um, sim 20 model
N_ST = 480
T_ST = 1e-3 + 0.3 / F_AX
F_ST = N_ST / T_ST
s_st = np.arange(1, N_ST + 1) * 1.0           # value after jump k (k = 0..N-1): (k+1) um
nb_st = nbar_held(s_st, F_ST, 50e3)
an_st = staircase_nbar_analytic(N_ST, T_ST, 50e3)
st_ok = bool(abs(nb_st - an_st) <= max(0.02 * abs(an_st), 1e-3))
print(f"staircase cross-check: routine {nb_st:.6e}, analytic {an_st:.6e}; within 2% or 1e-3: {st_ok}", flush=True)

# ---------------------------------------------------------------- acceptance and summary
blend_ok = all(min(r["K_eig_J_per_m2"]) > 0 for h in handoff.values() for r in h["table"])
zone_ok = all(abs(handoff[n]["vmax_zone"] - handoff[n]["vmax_sim12"]) <= 0.01 for n in handoff)
acc = {
    "matches_sim12_table_within_1mV": bool(checkA_maxdiff <= 1e-3),
    "max_abs_V_matches_sim12": bool(abs(checkA_maxabs - ref12["max_abs_V"]) <= 0.002),
    "max_10um_step_matches_sim12": bool(abs(checkA_step10 - ref12["max_step_change_V"]) <= 0.002),
    "no_bounded_solves": bool((not bnd.any()) and (not any(zone_bounded.values()))),
    "interp_axial_error_below_100nm": bool(checkB["max_abs_dy_nm"] < 100.0),
    "interp_axial_freq_within_1pct": bool(checkB["max_freq_dev_rel"] <= 0.01),
    "zone_sets_match_sim12_vmax": bool(zone_ok),
    "tilt_blend_all_curvatures_positive": bool(blend_ok),
    "all_voltages_within_dac_range": bool(dac_ok),
    "staircase_routine_matches_analytic": bool(st_ok),
}
for k, v in acc.items():
    print(f"  {'PASS' if v else 'FAIL'}  {k}")

summary = dict(
    TAG=TAG, layout=os.path.basename(JS), centre_dc_zero=bool(FIX2),
    constants=dict(V_RF=V_RF, F_RF_Hz=F_RF, F_AX_Hz=F_AX, DC_LIMIT_V=DC_LIMIT, N_ACTIVE=N_ACTIVE,
                   X_LOAD_um=X_LOAD, X_READ_um=X_READ, TILT_DEG=TILT_DEG, DY_um=DY_USED,
                   DY_default_um=DY, T_MOVE_s=T_MOVE, T_TILT_s=T_TILT, F_DAC_Hz=F_DAC,
                   DAC_BITS=DAC_BITS, DAC_RANGE_V=DAC_RANGE, LSB_V=LSB, F_FILT_Hz=list(F_FILT),
                   SCAN_T_s=list(SCAN_T), SCAN_F_Hz=list(SCAN_F), x0_nm_sim20=x0_nm),
    dy_choice=("DY default" if DY_USED == DY else "fallback DY (estimate above 40 min)"),
    counts=dict(static_solves=n_y, midpoints=len(mids), electrodes_dc_t=len(dc_t),
                electrodes_dc_z=len(dc_z), waveform_samples=len(wave_t), staircase_steps=N_ST),
    checkA=dict(max_abs_diff_V=checkA_maxdiff, max_abs_V=checkA_maxabs, max_10um_step_V=checkA_step10,
                sim12_max_abs_V=ref12["max_abs_V"], sim12_max_step_V=ref12["max_step_change_V"]),
    checkB=checkB,
    zone_bounded=zone_bounded,
    tilt_blend={n: dict(vmax_zone=h["vmax_zone"], vmax_sim12_regular=h["vmax_sim12"], y=h["y"], table=h["table"])
                for n, h in handoff.items()},
    dac_scan=dac_scan,
    quantisation=dict(max_dy_per_lsb_nm=quant_max_nm, rss_dy_per_lsb_nm=quant_rss_nm, x0_nm=x0_nm),
    nbar_scan=nbar_scan,
    staircase_check=dict(routine=nb_st, analytic=an_st, N=N_ST, T_s=T_ST, f_Hz=50e3),
    acceptance=acc,
)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1, default=float)
print(f"wrote {OUT}")
