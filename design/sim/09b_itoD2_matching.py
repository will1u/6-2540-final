"""09b - Can the 'ITO on D2' window get its absorption back with a buried matching layer?

09 found NbN absorption ~0.63 for an etched window (vacuum / ITO / cap / NbN / spacer / Al) but
only ~0.36-0.40 for ITO on top of the 10 um D2 oxide: with SiO2 above the cap, the cap/ITO can no
longer act as an impedance-matching layer. Here a high-index layer is put back directly on the
cap, UNDER the D2 (buried, grounded ITO as in Hampel 2023 Fig. 2(d), n ~ 1.95; or PECVD SiN,
n ~ 2.05 at 493 nm [verify on a witness]):

  vacuum / ITO_top (half wave, 125 nm) / D2 10 um / HI layer / cap / NbN / spacer / Al / SiO2 / Si

and the spacer, cap and HI thickness are scanned. The 10 um D2 is averaged over one fringe (the
ion's emission cone and +-1% thickness non-uniformity wash the fringe out; 09 showed this).
Uses the transfer-matrix and effective-medium functions of 09 (copied, not imported, because 09
runs its whole study at import).
"""

import json
import os

import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "09b_itoD2_matching")
os.makedirs(OUT, exist_ok=True)
LAM = 493.0
NK = dict(SiO2=1.463, Si=4.333 + 0.048j, Al=0.605 + 5.245j, ITO=1.965 + 0.003j, NbN=2.109 + 1.997j,
          SiN=2.05 + 0.0j)                       # same sources as 09; SiN: typical PECVD [verify]
T_NBN, FILL, T_AL, T_THERM, T_D2 = 7.0, 0.5, 150.0, 1000.0, 10000.0


def iso(n, d):
    e = n ** 2
    return (e, e, e, d)


def wires(nw, nh, f, d):
    ew, eh = nw ** 2, nh ** 2
    return (1.0 / (f / ew + (1 - f) / eh), f * ew + (1 - f) * eh, f * ew + (1 - f) * eh, d)


def tmm_A(layers, lam, n_sub, pol_plane):
    """Normal-incidence absorbed fraction per layer (copy of 09.tmm, theta = 0, s-polarisation)."""
    k0 = 2 * np.pi / lam
    pick = (lambda ex, ey: ey) if pol_plane == "xz" else (lambda ex, ey: ex)
    eta_sub = np.sqrt(n_sub ** 2 + 0j)
    E, H = 1.0 + 0j, eta_sub
    flux = [np.real(E * np.conj(H))]
    for ex, ey, ez, d in reversed(layers):
        kz = np.sqrt(pick(ex, ey) + 0j)
        kz = np.where(kz.imag < 0, -kz, kz)
        c, s = np.cos(k0 * kz * d), np.sin(k0 * kz * d)
        E, H = c * E - 1j * s / kz * H, -1j * kz * s * E + c * H
        flux.append(np.real(E * np.conj(H)))
    flux = flux[::-1]
    a_in = (E + H) / 2
    return [(flux[j] - flux[j + 1]) / np.abs(a_in) ** 2 for j in range(len(layers))]


def A_nbn(t_sp, t_cap, t_hi, hi="ITO", t_top=125.0):
    vals = []
    for k in range(12):                                  # average over one D2 fringe
        d2 = T_D2 + k * LAM / (2 * NK["SiO2"]) / 12
        layers = [iso(NK["ITO"], t_top), iso(NK["SiO2"], d2), iso(NK[hi], t_hi), iso(NK["SiO2"], t_cap),
                  wires(NK["NbN"], NK["SiO2"], FILL, T_NBN), iso(NK["SiO2"], t_sp), iso(NK["Al"], T_AL),
                  iso(NK["SiO2"], T_THERM)]
        a = [tmm_A(layers, LAM, NK["Si"], p)[4] for p in ("xz", "yz")]
        vals.append(0.5 * (a[0] + a[1]))
    return float(np.mean(vals))


res = {}
sp = np.arange(40, 260, 6.0)
for hi in ("none", "ITO", "SiN"):
    best = (-1, None)
    for t_sp in sp:
        for t_cap in np.arange(30, 200, 10.0):
            for t_hi in ([0.0] if hi == "none" else np.arange(20, 160, 10.0)):
                a = A_nbn(t_sp, t_cap, t_hi, hi if hi != "none" else "ITO")
                if a > best[0]:
                    best = (a, (float(t_sp), float(t_cap), float(t_hi)))
    a0, (t_sp, t_cap, t_hi) = best
    # +-10 nm robustness on spacer, cap, HI
    corners = [A_nbn(t_sp + d1, t_cap + d2, max(t_hi + d3, 0), hi if hi != "none" else "ITO")
               for d1 in (-10, 10) for d2 in (-10, 10) for d3 in ((-10, 10) if hi != "none" else (0,))]
    res[hi] = dict(A=a0, spacer=t_sp, cap=t_cap, hi=t_hi, worst_pm10=min(corners))
    print(f"buried layer {hi:4s}: A = {a0:.3f} at spacer {t_sp:.0f}, cap {t_cap:.0f}, layer {t_hi:.0f} nm; "
          f"worst corner +-10 nm: {min(corners):.3f}")
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1)

# ---------------------------------------------------------------- v3: no ITO at all (DESIGN_LOG step 17)
# vacuum / D2 10 um / cap / NbN / spacer / Al: top ITO and buried layer both removed (t_top = 0, t_hi = 0).
# Best cap for a 1st-order (40-130 nm) and a 2nd-order (180-300 nm) spacer, with the +-10 nm worst corner.
noito = {}
for order, sp_range in (("1st", np.arange(40, 131, 2.0)), ("2nd", np.arange(180, 301, 2.0))):
    best = (-1, None)
    for t_sp in sp_range:
        for t_cap in np.arange(30, 300, 5.0):
            a = A_nbn(t_sp, t_cap, 0.0, "ITO", t_top=0.0)
            if a > best[0]:
                best = (a, (float(t_sp), float(t_cap)))
    a0, (t_sp, t_cap) = best
    corners = [A_nbn(t_sp + d1, t_cap + d2, 0.0, "ITO", t_top=0.0) for d1 in (-10, 10) for d2 in (-10, 10)]
    noito[order] = dict(A=a0, spacer=t_sp, cap=t_cap, worst_pm10=min(corners))
    print(f"no ITO, {order}-order spacer: A = {a0:.3f} at spacer {t_sp:.0f}, cap {t_cap:.0f} nm; "
          f"worst corner +-10 nm: {min(corners):.3f}")
# the v2 thicknesses (spacer 238, cap 80) with the ITO simply removed, for comparison
noito["v2_thicknesses_no_ito"] = A_nbn(238.0, 80.0, 0.0, "ITO", t_top=0.0)
print(f"no ITO, v2 thicknesses (spacer 238, cap 80): A = {noito['v2_thicknesses_no_ito']:.3f}")
with open(os.path.join(OUT, "summary_noito.json"), "w") as fh:
    json.dump(noito, fh, indent=1)
