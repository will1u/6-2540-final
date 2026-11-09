"""20 - Transport timing: classical axial heating of a 138Ba+ ion shuttled 480 um (Claude-authored).

Model: the ion sits in a harmonic axial well (f_ax = 0.8 MHz) whose centre s(t) moves from 0 to D in
time T. Classical equation x'' + w^2 (x - s) = 0, ion at rest at the start. The energy left after the
move is E = (m/2) |integral of s''(t) exp(i w t) dt|^2, and nbar = E / (hbar w).

Part 1: smooth ramps (linear, sin^2, minimum-jerk) versus T.
Part 2: what the DAC sends: 48 (and finer: 480, 4800) held steps, each smoothed by a first-order
        electrode filter (corner f_filt).
Part 3: DAC requirements from the waveform file: largest step, update rate and slew.

Outputs (sim/out/20_transport_timing/): nbar_vs_T.png, part1_table.csv, summary.json.
Assumptions are tagged [inference] in the code.
"""

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import trapcalc as tc  # noqa: E402

OUT = os.path.join(HERE, "out", "20_transport_timing")
os.makedirs(OUT, exist_ok=True)
WAVES = os.path.join(HERE, "out", "12_final_chip", "trap_die_v4_A30_V2zero", "waveforms.csv")

M = tc.M_BA138                     # kg
HBAR = 1.054571817e-34             # J s
F_AX = 0.8e6                       # Hz, axial well frequency
W = 2 * np.pi * F_AX               # rad/s
D = 480e-6                         # m, total move
D_STEP = 10e-6                     # m, DAC step in the waveform file
N_STEPS = 48                       # 48 steps of 10 um = 480 um
F_FILTS = (10e3, 50e3, 200e3)      # Hz, electrode filter corners
T_PART2 = (100e-6, 300e-6, 1e-3, 3e-3)
DT_FINE = 1.0 / (400 * F_AX)       # s, time step for numerical integrals
T_LIST = np.logspace(np.log10(10e-6), np.log10(1e-3), 200)
THRESH = (1.0, 0.1)

X0 = np.sqrt(HBAR / (2 * M * W))   # m, zero-point size
EQ = HBAR * W                      # J, energy quantum


def nbar_from_integral(I):
    """nbar = (m/2) |I|^2 / (hbar w), with I = integral of s'' exp(i w t) dt."""
    return 0.5 * M * np.abs(I) ** 2 / EQ


def trapz_uniform(y, dt):
    """Trapezoid rule on a uniform grid (written out so it does not depend on the numpy version)."""
    return dt * (np.sum(y) - 0.5 * (y[0] + y[-1]))


# ---------------------------------------------------------------- Part 1: smooth ramps
def nbar_linear(T):
    """Closed form: s'' = (D/T)(delta(t) - delta(t - T)), so nbar = (2 m (D/T)^2 / hbar w) sin^2(wT/2)."""
    return 0.5 * M * (D / T) ** 2 * np.abs(1 - np.exp(1j * W * T)) ** 2 / EQ


def envelope_linear(T):
    return 2 * M * (D / T) ** 2 / EQ


def time_grid(T):
    n = int(np.ceil(T / DT_FINE))
    return np.linspace(0.0, T, n + 1)


def nbar_sin2(T):
    t = time_grid(T)
    s2 = (D / 2) * (np.pi / T) ** 2 * np.cos(np.pi * t / T)   # s = D sin^2(pi t / 2T), zero outside [0, T]
    return nbar_from_integral(trapz_uniform(s2 * np.exp(1j * W * t), t[1] - t[0]))


def nbar_minjerk(T):
    t = time_grid(T)
    u = t / T
    s2 = D / T ** 2 * (60 * u - 180 * u ** 2 + 120 * u ** 3)  # s = D(10u^3 - 15u^4 + 6u^5)
    return nbar_from_integral(trapz_uniform(s2 * np.exp(1j * W * t), t[1] - t[0]))


def settle_T(Ts, nb, thr):
    """Smallest T after which nb stays below thr for all longer T in the list (None = not in list)."""
    above = np.where(nb >= thr)[0]
    if above.size == 0:
        return float(Ts[0])
    last = above.max()
    if last == len(Ts) - 1:
        return None
    return float(Ts[last + 1])


# ---------------------------------------------------------------- Part 2: DAC staircase + filter
def staircase_nbar(N, T, f_filt):
    """N held steps of D/N over time T, each smoothed as d (1 - exp(-(t - t_k)/tau)), tau = 1/(2 pi f_filt).

    [inference] jump k happens at t_k = k T/N for k = 0..N-1 (first jump at t = 0).
    [inference] the well centre follows the filtered voltage linearly (given in the task).
    [inference] grid step = (T/N)/K with K = ceil((T/N) / (1/(400 f_ax))): each step interval holds an
    integer number of grid points, so the jump times fall exactly on the grid (no rounding).
    """
    d = D / N
    dt_step = T / N
    tau = 1.0 / (2 * np.pi * f_filt)
    K = int(np.ceil(dt_step / DT_FINE))
    dt_g = dt_step / K
    t_end = (N - 1) * dt_step + 10 * tau
    pad = 4                                                   # zero samples before t = 0, so the
    n = pad + int(np.ceil(t_end / dt_g)) + 1                  # first jump is not on the grid edge
    t = (np.arange(n) - pad) * dt_g
    jumps = np.zeros(n)
    np.add.at(jumps, pad + np.arange(N) * K, 1.0)
    count = np.cumsum(jumps)                                  # number of steps taken so far
    a = np.exp(-dt_g / tau)
    decay = lfilter([1.0], [1.0, -a], jumps)                  # sum over steps of exp(-(t - t_k)/tau)
    s = d * (count - decay)                                   # well centre, 0 -> ~D
    s2 = np.gradient(np.gradient(s, dt_g), dt_g)
    return nbar_from_integral(trapz_uniform(s2 * np.exp(1j * W * t), dt_g))


def staircase_nbar_analytic(N, T, f_filt):
    """[inference] closed form of the same model with exact jump times t_k = k T/N:
    int s'' e^{iwt} dt = -i w d S / (1 - i w tau), S = sum_k exp(i w t_k), so
    nbar = (m/2) w^2 d^2 |S|^2 / (hbar w (1 + w^2 tau^2)). Used only as a cross-check."""
    d = D / N
    tau = 1.0 / (2 * np.pi * f_filt)
    S = np.sum(np.exp(1j * W * np.arange(N) * T / N))
    return float(0.5 * M * W ** 2 * d ** 2 * np.abs(S) ** 2 / (EQ * (1 + (W * tau) ** 2)))


# ---------------------------------------------------------------- Part 3: DAC waveform file
def load_waveforms():
    data = np.genfromtxt(WAVES, delimiter=",", names=True)
    names = data.dtype.names
    y = data[names[0]]
    V = np.column_stack([data[nm] for nm in names[1:]])
    return names[1:], y, V


if __name__ == "__main__":
    print(f"m = {M:.4e} kg, w = {W:.4e} rad/s, hbar w = {EQ:.4e} J")
    print(f"zero-point size x0 = {X0*1e9:.3f} nm")

    # ---- Part 1
    print("\nPART 1: smooth ramps")
    nb_lin = nbar_linear(T_LIST)
    env = envelope_linear(T_LIST)
    nb_s2 = np.array([nbar_sin2(T) for T in T_LIST])
    nb_mj = np.array([nbar_minjerk(T) for T in T_LIST])

    settle = {}
    for name, nb in (("linear", nb_lin), ("sin2", nb_s2), ("minjerk", nb_mj)):
        settle[name] = {}
        for thr in THRESH:
            settle[name][str(thr)] = settle_T(T_LIST, nb, thr)
        s1, s01 = settle[name]["1.0"], settle[name]["0.1"]
        print(f"  {name:8s}: nbar stays < 1 for all longer T from T = "
              f"{'none in list' if s1 is None else f'{s1:.3e} s'}; "
              f"stays < 0.1 from T = {'none in list' if s01 is None else f'{s01:.3e} s'}")

    print("\n  sampled rows (every 20th of 200 T values):")
    print(f"  {'T (us)':>10s} {'linear':>12s} {'envelope':>12s} {'sin2':>12s} {'minjerk':>12s}")
    for i in range(0, len(T_LIST), 20):
        print(f"  {T_LIST[i]*1e6:10.3f} {nb_lin[i]:12.4e} {env[i]:12.4e} {nb_s2[i]:12.4e} {nb_mj[i]:12.4e}")

    tab = np.column_stack([T_LIST, nb_lin, env, nb_s2, nb_mj])
    np.savetxt(os.path.join(OUT, "part1_table.csv"), tab, delimiter=",", comments="",
               header="T_s,nbar_linear,nbar_linear_envelope,nbar_sin2,nbar_minjerk", fmt="%.6e")

    # linear-ramp envelope check at T = 100 us against the closed-form maximum nearby
    # window +-1%: the closed form peaks every 0.625 us (half an axial period), and the envelope
    # scales as 1/T^2, so a wide window would mix in a T-dependence of the envelope itself
    T100 = 100e-6
    Tfine = np.linspace(0.99 * T100, 1.01 * T100, 400001)
    vals = nbar_linear(Tfine)
    i_pk = int(np.argmax(vals))
    env100 = float(envelope_linear(T100))
    max100 = float(vals[i_pk])
    print(f"\n  linear envelope at T = 100 us: 2 m (D/T)^2 / (hbar w) = {env100:.4e}")
    print(f"  max of closed form within +-1% of 100 us = {max100:.4e} at T = {Tfine[i_pk]*1e6:.4f} us "
          f"(envelope there {float(envelope_linear(Tfine[i_pk])):.4e})")

    mj_1ms = float(nbar_minjerk(1e-3))
    print(f"  minimum-jerk nbar at T = 1 ms = {mj_1ms:.3e}")

    # dense curve for the plot (the linear closed form oscillates faster than the 200-point grid)
    Td = np.logspace(np.log10(10e-6), np.log10(1e-3), 20000)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.loglog(Td, np.maximum(nbar_linear(Td), 1e-30), lw=0.8, label="linear ramp (closed form)")
    ax.loglog(Td, envelope_linear(Td), "--", color="0.4", lw=1, label="linear ramp envelope")
    ax.loglog(T_LIST, np.maximum(nb_s2, 1e-30), "o-", ms=2.5, lw=0.8, label="sin$^2$ ramp")
    ax.loglog(T_LIST, np.maximum(nb_mj, 1e-30), "s-", ms=2.5, lw=0.8, label="minimum-jerk ramp")
    ax.axhline(1.0, color="k", lw=0.8)
    ax.set(xlabel="transport time T (s)", ylabel="nbar left in the motion",
           title="Classical axial excitation, 480 um move, f_ax = 0.8 MHz")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "nbar_vs_T.png"), dpi=150)
    plt.close(fig)

    # ---- single sudden jump
    print("\nSINGLE UNFILTERED JUMP: nbar = (d / 2 x0)^2")
    jump = {}
    for d in (10e-6, 1e-6, 0.1e-6):
        jump[f"{d*1e6:g}um"] = float((d / (2 * X0)) ** 2)
        print(f"  d = {d*1e6:5.1f} um: nbar = {jump[f'{d*1e6:g}um']:.4e}")

    # ---- Part 2
    print("\nPART 2: staircase through a first-order filter (numerical; analytic cross-check in brackets)")
    stair = {}
    stair_an = {}
    for N in (48, 480, 4800):
        d_step = D / N
        print(f"\n  {N} steps of {d_step*1e6:g} um:")
        print("  f_filt (kHz) | " + " ".join(f"T={T*1e6:8.0f}us" for T in T_PART2))
        stair[str(N)] = {}
        stair_an[str(N)] = {}
        for f in F_FILTS:
            row = [staircase_nbar(N, T, f) for T in T_PART2]
            an = [staircase_nbar_analytic(N, T, f) for T in T_PART2]
            stair[str(N)][f"{f/1e3:g}kHz"] = [float(x) for x in row]
            stair_an[str(N)][f"{f/1e3:g}kHz"] = an
            print(f"  {f/1e3:12.0f} | " + " ".join(f"{x:14.4e}" for x in row))
            print(f"  {'[analytic]':>12s} | " + " ".join(f"{x:14.4e}" for x in an))

    # [inference] extra check: all four T in T_PART2 are whole numbers of axial periods, which makes the
    # staircase sum exactly 0 or N. Shifting each T by 0.3 axial periods gives a generic T (analytic form).
    print("\nPART 2 extra: same T shifted by 0.3 axial periods (analytic, [inference])")
    for N in (48, 480, 4800):
        off = [T + 0.3 / F_AX for T in T_PART2]
        print(f"  {N:5d} steps: " + " | ".join(
            f"{f/1e3:g} kHz: " + " ".join(f"{staircase_nbar_analytic(N, T, f):.3e}" for T in off)
            for f in F_FILTS))

    # ---- Part 3
    print("\nPART 3: DAC requirements")
    names, y, V = load_waveforms()
    assert V.shape == (49, 34), V.shape
    assert np.allclose(np.diff(y), 10.0)
    dV = np.abs(np.diff(V, axis=0))
    max_step = float(dV.max())
    i_row, i_col = np.unravel_index(dV.argmax(), dV.shape)
    vmax = float(np.abs(V).max())
    print(f"  electrodes: {names[0]}..{names[-1]} ({len(names)}), rows {y[0]:.0f}..{y[-1]:.0f} um")
    print(f"  largest step between consecutive rows: {max_step:.4f} V "
          f"(electrode {names[i_col]}, row y = {y[i_row]:.0f} -> {y[i_row+1]:.0f} um)")
    print(f"  largest absolute voltage: {vmax:.4f} V")
    print(f"  {'T (us)':>10s} {'update rate (Hz)':>18s} {'max slew (V/us)':>18s}")
    dac = {}
    for T in T_PART2:
        rate = N_STEPS / T
        slew = max_step / (T / N_STEPS) / 1e6
        dac[f"{T*1e6:g}us"] = {"update_rate_Hz": float(rate), "max_slew_V_per_us": float(slew)}
        print(f"  {T*1e6:10.0f} {rate:18.4e} {slew:18.4e}")

    # ---- acceptance
    checks = {
        "x0_between_6.5_and_7.1_nm": bool(6.5e-9 <= X0 <= 7.1e-9),
        "largest_step_1.708_V_within_0.002": bool(abs(max_step - 1.708) <= 0.002),
        "linear_envelope_matches_closed_form_max_within_5pct": bool(abs(max100 / env100 - 1) <= 0.05),
        "staircase_numeric_vs_analytic_within_1pct_or_1e-3": bool(all(
            abs(stair[k][f][i] - stair_an[k][f][i]) <= max(0.01 * stair_an[k][f][i], 1e-3)
            for k in stair for f in stair[k] for i in range(len(T_PART2)))),
        "minjerk_nbar_1ms_far_below_1 (threshold 0.1 [inference])": bool(mj_1ms < 0.1),
        "single_jump_roughly_5e5": bool(4e5 <= jump["10um"] <= 6e5),
    }
    print("\nACCEPTANCE")
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")

    summary = {
        "x0_nm": float(X0 * 1e9),
        "hbar_w_J": float(EQ),
        "part1_settle_T_s": settle,
        "linear_envelope_100us": env100,
        "linear_closed_form_max_near_100us": max100,
        "minjerk_nbar_1ms": mj_1ms,
        "single_jump_nbar": jump,
        "part2_nbar_by_steps": stair,
        "part2_nbar_by_steps_analytic": stair_an,
        "part2_T_s": list(T_PART2),
        "part3_max_step_V": max_step,
        "part3_max_abs_V": vmax,
        "part3_dac": dac,
        "acceptance": checks,
    }
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(f"\nwrote {OUT}")
