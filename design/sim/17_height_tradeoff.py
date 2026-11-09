"""17 - Ion height trade-off: is 50 um right, or should the trap be lower? (Claude-authored)

Uses the analytic gapless five-wire model (trapcalc.fivewire_rf_phi) at each ion height h.
For each h the RF rail width a is set so the RF null sits at h, then the RF voltage for a
3 MHz radial frequency at 28 MHz drive, the pseudopotential depth, and the detector collection
(493 nm, isotropic emitter, through t_au of Au) are computed. Heating is taken as ~ h^-4 and as
the shallower ~ h^-2.6 bracket.

Scaling to keep the 50 um depth: V -> v * scale^2, f_RF -> 28 * scale MHz, f_radial -> 3 * scale MHz,
with scale = sqrt(D0 / depth), D0 = depth at h = 50 um (same centre DC width c = 40 um).

Three tables:
  A. fixed centre DC c = 40 um, window 30 um (A30) or 60 x 30 um (B60), h in HS.
  B. self-similar trap c = 0.8 h, square window (c - 10) um, h in HS without 45.
  C. h = 50 um, c in (40, 50, 60, 70), window (c - 10) um radial x 30 or 60 um axial.

Outputs: sim/out/17_height_tradeoff/height_tradeoff.png and summary.json
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc

import trapcalc as tc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "17_height_tradeoff")
os.makedirs(OUT, exist_ok=True)

GAP = 5.0                  # um, RF / DC electrode gap
H0 = 50.0                  # um, reference ion height
HS = [30, 35, 40, 45, 50, 60, 70]
HS_B = [h for h in HS if h != 45]
C_A = 40.0                 # um, fixed centre DC width for table A
F_RF0 = 28.0               # MHz, reference drive
F_RAD0 = 3.0               # MHz, reference radial frequency
D_BEAM = 5e-3              # m, half chip width crossed by the beam (10 mm die)
THETA = np.deg2rad(45.0)
LAMS = {"493": 493e-9, "650": 650e-9}
T_AU = {"E1": 0.35, "E2": 6.0}   # um, Au thickness (electrode options)


def design(h, c, frad=3e6, frf=28e6):
    """RF rail width, RF volts, q, and depth (meV) for a null at height h and centre DC width c."""
    g = GAP
    x1 = c / 2 + g / 2
    x2 = h * h / x1
    a = x2 - x1 - g
    if a < 5:
        return None
    zz = np.linspace(1, 900, 18000)
    d = 1e-3
    phi = lambda x, z: tc.fivewire_rf_phi(x, z, c, a, g)
    Ez = (phi(0, zz + d) - phi(0, zz - d)) / (2 * d)
    hxx = (phi(d, h) - 2 * phi(0, h) + phi(-d, h)) / d ** 2
    hzz = (phi(0, h + d) - 2 * phi(0, h) + phi(0, h - d)) / d ** 2
    H = np.diag([hxx, 0, hzz])
    f1, q1, _ = tc.rf_hessian_to_freqs(H, 1.0, frf)
    v = frad / f1.max()
    f, q, _ = tc.rf_hessian_to_freqs(H, v, frf)
    psi = tc.pseudo_eV(np.column_stack([0 * zz, 0 * zz, Ez]), v, frf)
    k = np.argmax(np.where(zz > h, psi, -1))
    return a, v, q.max(), 1e3 * psi[k]


def design_checked(h, c):
    r = design(h, c)
    if r is None:
        raise SystemExit(f"design(h={h}, c={c}) gave a < 5 um; stop")
    return r


def clip(lam, h):
    """Fraction of the beam clipped by the die surface (same formula as sim 11)."""
    s = D_BEAM / np.sin(THETA)
    w0 = np.sqrt(lam * s / np.pi)
    return 0.5 * erfc(np.sqrt(2) * (h * 1e-6) / (w0 * np.sqrt(2)))


def coll(h, wx, wy, t_au):
    """Percent of 493 nm photons from an isotropic emitter at h landing on a wx x wy window."""
    return 100 * tc.collection_fraction(h + t_au, wx, wy, "iso")


# ------------------------------------------------------------------ reference depth at h = 50, c = 40
a0, v0, q0, D0 = design_checked(H0, C_A)
print(f"reference h = {H0:g} um, c = {C_A:g} um: a = {a0:.1f} um, V = {v0:.1f} V, q = {q0:.3f}, depth = {D0:.1f} meV")

# ------------------------------------------------------------------ table A
print("\nTable A: fixed centre DC c = 40 um")
print(f"{'h':>4} {'a':>6} {'V':>6} {'q':>6} {'depth':>7} | {'V_k':>6} {'fRF_k':>6} {'fRad_k':>6} | "
      f"{'A30E1':>6} {'A30E2':>6} {'B60E1':>6} {'B60E2':>6} | {'h^-4':>7} {'h^-2.6':>7} | {'clip493':>8} {'clip650':>8}")
table_a = []
for h in HS:
    a, v, q, depth = design_checked(h, C_A)
    scale = np.sqrt(D0 / depth)
    row = dict(h=h, a=a, V=v, q=q, depth_meV=depth,
               V_keep_D0=v * scale ** 2, fRF_MHz_keep_D0=F_RF0 * scale, fRAD_MHz_keep_D0=F_RAD0 * scale,
               A30_E1=coll(h, 30, 30, T_AU["E1"]), A30_E2=coll(h, 30, 30, T_AU["E2"]),
               B60_E1=coll(h, 60, 30, T_AU["E1"]), B60_E2=coll(h, 60, 30, T_AU["E2"]),
               heat_h4=(h / H0) ** -4, heat_h26=(h / H0) ** -2.6,
               clip493=clip(LAMS["493"], h), clip650=clip(LAMS["650"], h))
    table_a.append(row)
    print(f"{h:4.0f} {a:6.1f} {v:6.1f} {q:6.2f} {depth:7.1f} | {row['V_keep_D0']:6.1f} "
          f"{row['fRF_MHz_keep_D0']:6.2f} {row['fRAD_MHz_keep_D0']:6.2f} | "
          f"{row['A30_E1']:6.2f} {row['A30_E2']:6.2f} {row['B60_E1']:6.2f} {row['B60_E2']:6.2f} | "
          f"{row['heat_h4']:7.2f} {row['heat_h26']:7.2f} | {row['clip493']:8.1e} {row['clip650']:8.1e}")

# ------------------------------------------------------------------ table B
print("\nTable B: self-similar trap c = 0.8 h, square window (c - 10) um")
print(f"{'h':>4} {'c':>6} {'a':>6} {'window':>7} {'V':>6} {'depth':>7} {'E1 %':>7} {'E2 %':>7}")
table_b = []
for h in HS_B:
    c = 0.8 * h
    a, v, q, depth = design_checked(h, c)
    win = c - 10
    row = dict(h=h, c=c, a=a, window=win, V=v, depth_meV=depth,
               E1=coll(h, win, win, T_AU["E1"]), E2=coll(h, win, win, T_AU["E2"]))
    table_b.append(row)
    print(f"{h:4.0f} {c:6.1f} {a:6.1f} {win:7.1f} {v:6.1f} {depth:7.1f} {row['E1']:7.2f} {row['E2']:7.2f}")

# ------------------------------------------------------------------ table C
print("\nTable C: h = 50 um, window (c - 10) um radial x 30 or 60 um axial")
print(f"{'c':>4} {'a':>6} {'V':>6} {'depth':>7} | {'30ax E1':>8} {'30ax E2':>8} | {'60ax E1':>8} {'60ax E2':>8}")
table_c = []
for c in (40.0, 50.0, 60.0, 70.0):
    a, v, q, depth = design_checked(H0, c)
    win = c - 10
    row = dict(c=c, a=a, V=v, depth_meV=depth,
               ax30_E1=coll(H0, win, 30, T_AU["E1"]), ax30_E2=coll(H0, win, 30, T_AU["E2"]),
               ax60_E1=coll(H0, win, 60, T_AU["E1"]), ax60_E2=coll(H0, win, 60, T_AU["E2"]))
    table_c.append(row)
    print(f"{c:4.0f} {a:6.1f} {v:6.1f} {depth:7.1f} | {row['ax30_E1']:8.2f} {row['ax30_E2']:8.2f} | "
          f"{row['ax60_E1']:8.2f} {row['ax60_E2']:8.2f}")

# ------------------------------------------------------------------ figure
hs = np.array([r["h"] for r in table_a])
fig, ax1 = plt.subplots(figsize=(6.5, 4))
ax1.plot(hs, [r["A30_E2"] for r in table_a], "o-", label="A30 window (E2)")
ax1.plot(hs, [r["B60_E2"] for r in table_a], "s-", label="B60 window (E2)")
ax1.axvline(H0, color="0.4", ls="--", lw=0.8)
ax1.set_xlabel("ion height h (um), centre DC 40 um")
ax1.set_ylabel("photons on detector (%)  [isotropic, 493 nm]")
ax2 = ax1.twinx()
ax2.semilogy(hs, [r["heat_h4"] for r in table_a], "k:", label="heating ~ h^-4")
ax2.semilogy(hs, [r["heat_h26"] for r in table_a], "k--", lw=0.8, alpha=0.5, label="heating ~ h^-2.6")
ax2.set_ylabel("relative heating rate (re 50 um)")
ax2.grid(False)
l1, n1 = ax1.get_legend_handles_labels()
l2, n2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, n1 + n2, fontsize=7, loc="upper right")
ax1.set_title("collection vs heating, table A")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "height_tradeoff.png"), dpi=150)

# ------------------------------------------------------------------ summary
summary = dict(reference=dict(h_um=H0, c_um=C_A, a_um=a0, V=v0, q=q0, depth_meV=D0),
               table_A=table_a, table_B=table_b, table_C=table_c)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1, default=float)
print(f"\nwrote {os.path.join(OUT, 'height_tradeoff.png')} and summary.json")
