"""09 - NbN SNSPD optical stack: absorption at 493 nm by transfer matrix (Claude-authored).

Physics
  The ion's 493 nm fluorescence falls on a thin NbN meander that sits in a small optical cavity:
  an Al ground plane below acts as a mirror, SiO2 layers set the standing-wave phase, and a thin
  high-index ITO film on top (the grounded RF shield) acts as a matching layer. The quantity we
  want is the fraction of incident photons absorbed in the NbN (an upper bound on detection
  efficiency; the internal efficiency and fill-factor geometry are not modelled beyond this).

  Transfer-matrix method (TMM): in each planar layer the field is a sum of an up- and a down-
  going plane wave. The tangential E and H are continuous at every interface, so a 2x2
  "characteristic matrix" per layer carries (E, H) from the bottom of a layer to its top. Starting
  from a single outgoing wave in the substrate and stepping up gives the incident and reflected
  amplitudes. The power flux Re(E H*) entering the top of each layer, minus the flux leaving its
  bottom, is the power absorbed in that layer. Oblique incidence: the transverse wavevector
  q = k0 n_in sin(theta) is the same in every layer (Snell); s and p polarisations are separate.

  Nanowire layer = effective medium. A grating of wires (width w, pitch p, fill f = w/p) with
  p (200 nm) below the wavelength in the oxide (493/1.46 = 337 nm) behaves like a uniaxial film.
  With the wires along y:
    E along the wires (y) or along z: the field is continuous across the wire sidewalls, so the
      permittivities add like parallel capacitors:      eps_par  = f eps_NbN + (1-f) eps_SiO2
    E across the wires (x): D is continuous across the sidewalls, so they add like capacitors in
      series:                                          1/eps_perp = f/eps_NbN + (1-f)/eps_SiO2
  These are the two Wiener bounds; for a lamellar grating they are the exact zeroth-order
  (long-wavelength) limits. At p = 200 nm vs 337 nm the meander is only marginally sub-
  wavelength, so final numbers should come from RCWA/FDTD (as Hampel 2023 and Todaro 2021 did).

  Oblique incidence in the uniaxial layer is done exactly in the two principal planes (plane of
  incidence across the wires, x-z, or along them, y-z), where s and p do not mix:
     s-wave:  kz^2 = eps_s k0^2 - q^2,                  admittance eta = kz/k0
     p-wave:  kz^2 = eps_t (k0^2 - q^2/eps_z),          admittance eta = k0 eps_t/kz
  (eps_s = permittivity along E for s, eps_t = along the in-plane part of E for p). Other azimuths
  are interpolated as cos^2(phi) A_xz + sin^2(phi) A_yz, which is exact at normal incidence.

  Light reaching the detector: the ion sits ~50 um above a ~30 um square detector, so rays arrive
  at up to ~23 deg (corners). The cone average weights each point of the detector by the flux per
  unit area of an isotropic, unpolarised emitter (cos^3 theta). The real ion emits a dipole
  pattern with structured polarisation; this is an approximation.

Window variants (light comes from vacuum above):
  etched : the 10 um D2 SiO2 is etched away over the detector down to the ITO (etch stop).
           vacuum / ITO / SiO2 cap / NbN / SiO2 spacer / Al / thermal SiO2 / Si
  itoD2  : D2 not etched; ITO patch on top of D2 at the bottom of the 6 um Au pocket.
           vacuum / ITO / 10 um SiO2 (D2, cap merges into it) / NbN / spacer / Al / ...
           The 10 um layer is coherent for narrow-band ion light. Its exact thickness is unknown
           to many fringes (one fringe = lambda/2n = 168 nm), so we report (i) the average over one
           fringe of D2 thickness (= incoherent result) and (ii) the min/max over that fringe.

Optical constants (n + ik, room temperature; no cryogenic data found; see research notes
  design/research/research_notes/Trap integrated SNSPD design/stack_shielding_ito.md, Q3):
  NbN   Banerjee et al., Opt. Mater. Express 8, 2072 (2018), Glasgow dataset
        DOI 10.5525/gla.researchdata.637 ("5 nm thick, sputtered"), interpolated
  NbN   (alt) Medeiros et al., arXiv:1812.05559 Table 1, interpolated (650 nm extrapolated from
        598/638 nm)
  NbTiN Banerjee 2018 dataset (Hampel validation at 395 nm)
  Al    McPeak et al., ACS Photonics 2, 326 (2015) (refractiveindex.info)
  SiO2  Malitson, JOSA 55, 1205 (1965) Sellmeier
  Si    Green, Sol. Energ. Mater. Sol. Cells 92, 1305 (2008)
  ITO   Moerland & Hoogenboom, Optica 3, 112 (2016) (k = 0.003 at 493 nm); Minenkov et al. 2024
        "on Si, bottom" (1.844 + 0.011i) and a hypothetical k = 0.03 as sensitivity cases

Validation: Hampel et al., APL 122, 174001 (2023), arXiv:2302.01462: NbTiN 10 nm, 90 nm wires on
  180 nm pitch, 130 nm SiO2 cap, 212 nm SiO2 over 50 nm Al (trap devices; 186 nm in the stand-alone
  fibre-coupled devices "optimized ... for theoretically maximum SDE"), SDE 68 % with mirror and
  40 % without at 395 nm.

Outputs: sim/out/09_optical_stack_tmm/stack_tmm.png, summary.json
Run:     ./run.sh 09_optical_stack_tmm.py
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import minimum_filter, uniform_filter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "09_optical_stack_tmm")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ optical constants (n + ik)
NK = {
    493: dict(SiO2=1.463, Si=4.333 + 0.048j, Al=0.605 + 5.245j, ITO=1.965 + 0.003j,
              NbN=2.109 + 1.997j, NbN_Medeiros=2.503 + 2.511j),
    614: dict(SiO2=1.458, Si=3.910 + 0.018j, Al=1.057 + 6.507j, ITO=1.886 + 0.002j,
              NbN=2.456 + 2.338j, NbN_Medeiros=2.715 + 3.107j),
    650: dict(SiO2=1.457, Si=3.844 + 0.014j, Al=1.246 + 6.852j, ITO=1.864 + 0.003j,
              NbN=2.528 + 2.436j, NbN_Medeiros=2.876 + 3.242j),
    395: dict(SiO2=1.471, Si=5.826 + 0.370j, Al=0.365 + 4.170j, NbTiN=2.039 + 1.413j),
}
ITO_ALT = {"Moerland k=0.003": 1.965 + 0.003j, "Minenkov k=0.011": 1.844 + 0.011j,
           "hypothetical k=0.03": 1.95 + 0.03j}

# ------------------------------------------------------------------ fixed stack parameters (nm)
T_NBN = 7.0          # NbN thickness (5-8 nm planned)
FILL = 0.5           # 100 nm wires on 200 nm pitch
T_AL = 150.0         # Al ground plane / mirror (opaque above ~50 nm)
T_THERM = 1000.0     # thermal SiO2 under the Al
T_D2 = 10000.0       # PECVD SiO2 D2 layer (only in the itoD2 variant)
TOL = 10.0           # +/- fabrication tolerance on every thickness (nm)
CAP_MIN, SP_MIN = 30.0, 40.0    # practical lower limits on cap and spacer (nm)
ITO_MIN, ITO_MAX = 20.0, 130.0  # ITO range considered for the shield (nm)
DET_SIDE = 30.0      # um, detector side
DET_DIST = [50.0, 66.0]  # um, ion-to-detector distance: 50 as specified; 66 = 50 + 6 Au + 10 D2


# ------------------------------------------------------------------ layer helpers
def iso(n, d):
    """Isotropic layer: (eps_x, eps_y, eps_z, thickness)."""
    e = n ** 2
    return (e, e, e, d)


def wires(n_wire, n_host, f, d):
    """Nanowire grating (wires along y) as a uniaxial effective medium (Wiener bounds)."""
    ew, eh = n_wire ** 2, n_host ** 2
    e_par = f * ew + (1 - f) * eh               # E along wires (y) and along z
    e_perp = 1.0 / (f / ew + (1 - f) / eh)      # E across wires (x)
    return (e_perp, e_par, e_par, d)


def tmm(layers, n_in, n_sub, lam, theta=0.0, pol="s", plane="xz"):
    """Transfer matrix for a planar stack. layers: list of (eps_x, eps_y, eps_z, d_nm) from the
    light side down; d may be a numpy array (all arrays broadcast together). Light comes from a
    lossless medium n_in at angle theta; the substrate n_sub is semi-infinite.
    Returns (R, [absorbed fraction in each layer])."""
    u = n_in * np.sin(theta)                    # q / k0, conserved through the stack
    k0 = 2 * np.pi / lam

    def kz_eta(ex, ey, ez):
        e_s, e_t = (ey, ex) if plane == "xz" else (ex, ey)
        if pol == "s":
            kz = np.sqrt(e_s - u ** 2 + 0j)
        else:
            kz = np.sqrt(e_t * (1 - u ** 2 / ez) + 0j)
        kz = np.where(kz.imag < 0, -kz, kz)     # decaying branch downwards
        eta = kz if pol == "s" else e_t / kz
        return kz, eta

    # substrate: a single downgoing wave with E = 1, H = eta_sub
    _, eta_sub = kz_eta(*iso(n_sub, 0)[:3])
    E, H = 1.0 + 0j, eta_sub + 0j
    flux = [np.real(E * np.conj(H))]            # flux into the substrate
    for ex, ey, ez, d in reversed(layers):       # step from the bottom of each layer to its top
        kz, eta = kz_eta(ex, ey, ez)
        delta = k0 * kz * d
        c, s = np.cos(delta), np.sin(delta)
        E, H = c * E - 1j * s / eta * H, -1j * eta * s * E + c * H
        flux.append(np.real(E * np.conj(H)))
    flux = flux[::-1]                           # flux[j] = flux into the top of layer j
    _, eta0 = kz_eta(*iso(n_in, 0)[:3])
    a_in = (E + H / eta0) / 2                   # incident amplitude
    b_ref = (E - H / eta0) / 2                  # reflected amplitude
    s_in = np.real(eta0) * np.abs(a_in) ** 2
    R = np.abs(b_ref / a_in) ** 2
    A = [(flux[j] - flux[j + 1]) / s_in for j in range(len(layers))]
    return R, A


# ------------------------------------------------------------------ the stacks we compare
def stack_etched(nk, t_sp, t_cap, t_ito, nbn="NbN", ito=None, t_nbn=T_NBN, f=FILL, mirror=True):
    """vacuum / ITO / cap / NbN / spacer / Al / thermal SiO2 / Si. Returns layers, n_in, n_sub.
    Layer 0 = ITO, layer 2 = NbN in every variant (zero-thickness layers are harmless)."""
    ito = nk["ITO"] if ito is None else ito
    layers = [iso(ito, t_ito), iso(nk["SiO2"], t_cap), wires(nk[nbn], nk["SiO2"], f, t_nbn),
              iso(nk["SiO2"], t_sp), iso(nk["Al"] if mirror else nk["SiO2"], T_AL if mirror else 0.0),
              iso(nk["SiO2"], T_THERM)]
    return layers, 1.0, nk["Si"]


def stack_itoD2(nk, t_sp, t_ito, d2=T_D2, nbn="NbN", ito=None, t_nbn=T_NBN, f=FILL, mirror=True):
    """vacuum / ITO / D2 (+cap, both SiO2) / NbN / spacer / Al / thermal SiO2 / Si.
    Layer 0 = ITO, layer 2 = NbN."""
    ito = nk["ITO"] if ito is None else ito
    layers = [iso(ito, t_ito), iso(nk["SiO2"], d2), wires(nk[nbn], nk["SiO2"], f, t_nbn),
              iso(nk["SiO2"], t_sp), iso(nk["Al"] if mirror else nk["SiO2"], T_AL if mirror else 0.0),
              iso(nk["SiO2"], T_THERM)]
    return layers, 1.0, nk["Si"]


def absorb(stack, lam, theta=0.0, plane="xz", layer=2):
    """Unpolarised absorption (mean of s and p) in one layer for a plane of incidence."""
    layers, n_in, n_sub = stack
    a = [tmm(layers, n_in, n_sub, lam, theta, pol, plane)[1][layer] for pol in ("s", "p")]
    return 0.5 * (a[0] + a[1])


def absorb_normal(stack, lam, layer=2):
    """Normal incidence: returns (A for E along wires, A for E across wires, mean)."""
    layers, n_in, n_sub = stack
    a_par = tmm(layers, n_in, n_sub, lam, 0.0, "s", "xz")[1][layer]    # s in x-z plane: E along y
    a_perp = tmm(layers, n_in, n_sub, lam, 0.0, "s", "yz")[1][layer]   # s in y-z plane: E along x
    return a_par, a_perp, 0.5 * (a_par + a_perp)


def fringe_avg(make_stack, lam, n_d2, n=12, layer=2):
    """Average (and min/max) of normal-incidence absorption over one fringe of D2 thickness."""
    vals = np.array([absorb_normal(make_stack(T_D2 + k * lam / (2 * n_d2) / n), lam, layer)[2]
                     for k in range(n)])
    return vals.mean(axis=0), vals.min(axis=0), vals.max(axis=0)


def cone_avg(make_stack, lam, dist, side=DET_SIDE, layer=2):
    """Absorption averaged over a square detector of the given side at distance dist below an
    isotropic unpolarised point source: weight cos^3(theta) per unit area, azimuth interpolated
    between the two principal planes (wires along y)."""
    th = np.deg2rad(np.linspace(0, 30, 31))
    a_xz = np.array([absorb(make_stack(), lam, t, "xz", layer) for t in th])
    a_yz = np.array([absorb(make_stack(), lam, t, "yz", layer) for t in th])
    g = np.linspace(-side / 2, side / 2, 41)
    X, Y = np.meshgrid(g, g)
    r = np.hypot(X, Y)
    theta = np.arctan2(r, dist)
    phi = np.arctan2(Y, X)
    a = np.cos(phi) ** 2 * np.interp(theta, th, a_xz) + np.sin(phi) ** 2 * np.interp(theta, th, a_yz)
    w = np.cos(theta) ** 3
    return float((a * w).sum() / w.sum()), float(np.rad2deg(theta.max())), th, a_xz, a_yz


# ------------------------------------------------------------------ 0. sanity checks of the TMM
nk = NK[493]
R_al = tmm([], 1.0, nk["Al"], 493.0)[0]
R_al_exact = abs((nk["Al"] - 1) / (nk["Al"] + 1)) ** 2
assert abs(R_al - R_al_exact) < 1e-12, "bulk Al reflectance"
brewster = np.arctan(nk["SiO2"])
assert tmm([], 1.0, nk["SiO2"], 493.0, brewster, "p")[0] < 1e-12, "Brewster angle"
_, A_lossless = tmm([iso(nk["SiO2"], 300.0), iso(1.8, 77.0)], 1.0, 1.5, 493.0, 0.4, "p")
assert abs(sum(A_lossless)) < 1e-12, "lossless films must not absorb"
print(f"checks: bulk Al R = {R_al:.4f} (exact {R_al_exact:.4f}); Brewster and lossless checks ok")

# ------------------------------------------------------------------ 1. etched window: 3-D sweep
lam = 493.0
t_sp = np.arange(0, 302, 2.0)[:, None]          # spacer (Al -> NbN), axis 1 of the cube
t_cap = np.arange(0, 302, 2.0)[None, :]         # cap (NbN -> ITO),   axis 2
t_ito = np.arange(0, 155, 5.0)                  # ITO,                axis 0
cube = np.array([absorb_normal(stack_etched(nk, t_sp, t_cap, ti), lam)[2] for ti in t_ito])
cube_ito = np.array([absorb_normal(stack_etched(nk, t_sp, t_cap, ti), lam, layer=0)[2] for ti in t_ito])
# worst case over a +/-TOL box in all three thicknesses
# Robustness: every thickness may be off by up to +/-TOL. 'worst' = the minimum over that box
# (all three errors at their worst at once, pessimistic); 'boxmean' = the mean over the box (the
# expected absorption for independent, uniformly distributed errors). We design on boxmean.
box = (2 * int(TOL / 5) + 1, 2 * int(TOL / 2) + 1, 2 * int(TOL / 2) + 1)
robust = minimum_filter(cube, size=box, mode="nearest")
boxmean = uniform_filter(cube, size=box, mode="nearest")


sp1d, cap1d = t_sp[:, 0], t_cap[0, :]
S3 = sp1d[None, :, None] + 0 * cube          # spacer value at every point of the cube
C3 = cap1d[None, None, :] + 0 * cube         # cap value
I3 = t_ito[:, None, None] + 0 * cube         # ITO value
# Practical limits: NbN must be capped (>= 30 nm; Hampel used 130 nm), spacer >= 40 nm over the
# Al (hillocks, pinholes), ITO 20-120 nm (sheet resistance ~40-400 Ohm/sq at 50 nm, notes Q2).
ok = (C3 >= CAP_MIN) & (S3 >= SP_MIN)
ok_ito = ok & (I3 >= ITO_MIN) & (I3 <= ITO_MAX)


def pick(arr, mask):
    """Index of the largest value of arr where mask is True."""
    return np.unravel_index(np.argmax(np.where(mask, arr, -1)), arr.shape)


def describe(i, j, k):
    return dict(t_ito=float(t_ito[i]), t_spacer=float(sp1d[j]), t_cap=float(cap1d[k]),
                A_nominal=float(cube[i, j, k]), A_boxmean_pm10nm=float(boxmean[i, j, k]),
                A_worst_pm10nm=float(robust[i, j, k]), A_ITO=float(cube_ito[i, j, k]))


results = {}
for name, arr, mask in (("nominal_best", cube, ok_ito), ("robust_best", boxmean, ok_ito),
                        ("robust_best_1st_order_spacer", boxmean, ok_ito & (S3 < 140)),
                        ("robust_best_2nd_order_spacer", boxmean, ok_ito & (S3 >= 140)),
                        ("no_ITO_nominal", cube, ok & (I3 == 0)), ("no_ITO_robust", boxmean, ok & (I3 == 0))):
    results[name] = describe(*pick(arr, mask))
# table: best and most robust spacer/cap for each ITO thickness
per_ito = {}
for i, ti in enumerate(t_ito):
    if ti > ITO_MAX:
        break
    m = np.zeros_like(ok)
    m[i] = ok[i]
    per_ito[f"{ti:.0f}"] = dict(nominal=describe(*pick(cube, m)), robust=describe(*pick(boxmean, m)))
results["per_ITO_thickness"] = per_ito
# no mirror: the Al is replaced by SiO2 (spacer + 1 um thermal oxide on Si), re-optimised
nm_cube = np.array([absorb_normal(stack_etched(nk, t_sp, t_cap, ti, mirror=False), lam)[2] for ti in (0.0, 50.0)])
for ii, ti in enumerate((0.0, 50.0)):
    j, k = pick(nm_cube[ii], ok[0])
    results[f"no_mirror_ITO{ti:.0f}_best"] = dict(t_spacer_plus_1um_thermal=float(sp1d[j]), t_cap=float(cap1d[k]),
                                                 A_nominal=float(nm_cube[ii, j, k]))

# Recommended etched-window design: robust optimum (rounded to the 2/5 nm grid already)
D = results["robust_best"]
d_sp, d_cap, d_ito = D["t_spacer"], D["t_cap"], D["t_ito"]
D2nd = results["robust_best_2nd_order_spacer"]


def design(nbn="NbN", ito=None, t_nbn=T_NBN, f=FILL, which=D, lam_=493, mirror=True):
    return stack_etched(NK[lam_], which["t_spacer"], which["t_cap"], which["t_ito"], nbn, ito, t_nbn, f, mirror)


par, perp, mean = absorb_normal(design(), lam)
results["design_polarisation"] = dict(E_along_wires=float(par), E_across_wires=float(perp), mean=float(mean))
results["design_mirror_removed_same_thicknesses"] = float(absorb_normal(design(mirror=False), lam)[2])
# tolerance table around the design (one thickness at a time)
tol_table = {}
for label, dd in (("spacer", (TOL, 0, 0)), ("cap", (0, TOL, 0)), ("ITO", (0, 0, TOL))):
    vals = []
    for sgn in (-1, 1):
        s_ = stack_etched(nk, d_sp + sgn * dd[0], d_cap + sgn * dd[1], max(d_ito + sgn * dd[2], 0))
        vals.append(float(absorb_normal(s_, lam)[2]))
    tol_table[label] = dict(minus10=vals[0], plus10=vals[1])
results["design_one_at_a_time_pm10nm"] = tol_table

# sensitivity: NbN dataset, NbN thickness, fill factor, ITO k
sens = {}
sens["NbN_Medeiros_at_design"] = float(absorb_normal(design(nbn="NbN_Medeiros"), lam)[2])
cubeM = absorb_normal(stack_etched(nk, t_sp, t_cap, d_ito, nbn="NbN_Medeiros"), lam)[2]
j, k = np.unravel_index(np.argmax(cubeM), cubeM.shape)
sens["NbN_Medeiros_reoptimised"] = dict(A=float(cubeM[j, k]), t_spacer=float(sp1d[j]), t_cap=float(cap1d[k]))
for tn in (5.0, 8.0, 10.0):
    sens[f"NbN_{tn:.0f}nm_at_design"] = float(absorb_normal(design(t_nbn=tn), lam)[2])
for ff in (0.4, 0.6):
    sens[f"fill_{ff}_at_design"] = float(absorb_normal(design(f=ff), lam)[2])
for nm_, n_ito in ITO_ALT.items():
    sens[f"ITO {nm_}"] = dict(A_NbN=float(absorb_normal(design(ito=n_ito), lam)[2]),
                              A_ITO=float(absorb_normal(design(ito=n_ito), lam, layer=0)[2]))
results["sensitivity"] = sens

# other wavelengths at the 493 nm design (leakage of 614/650 nm stray light)
other = {}
for lw in (493, 614, 650):
    other[f"{lw}nm"] = dict(design=float(absorb_normal(design(lam_=lw), lw)[2]),
                            design_Medeiros=float(absorb_normal(design(lam_=lw, nbn="NbN_Medeiros"), lw)[2]),
                            no_ITO=float(absorb_normal(design(lam_=lw, which=dict(results["no_ITO_robust"])), lw)[2]))
results["other_wavelengths"] = other

# cone average over the detector
cone = {}
for dist in DET_DIST:
    a_c, th_max, th, a_xz, a_yz = cone_avg(lambda: design(), lam, dist)
    cone[f"{dist:.0f}um"] = dict(A_cone=a_c, theta_max_deg=th_max)
cone_curves_etched = (th, a_xz, a_yz)
results["cone_average"] = cone

# ------------------------------------------------------------------ 2. ITO on top of D2 (no etch)
n_d2 = nk["SiO2"]
sp_line = np.arange(0, 302, 2.0)[:, None]
ito_line = np.arange(0, 155, 5.0)[None, :]
d2_mean, d2_min, d2_max = fringe_avg(lambda d2: stack_itoD2(nk, sp_line, ito_line, d2), lam, n_d2)
d2_mean_ito, _, _ = fringe_avg(lambda d2: stack_itoD2(nk, sp_line, ito_line, d2), lam, n_d2, layer=0)
d2_rob = minimum_filter(d2_mean, size=(2 * int(TOL / 2) + 1, 2 * int(TOL / 5) + 1), mode="nearest")
d2_box = uniform_filter(d2_mean, size=(2 * int(TOL / 2) + 1, 2 * int(TOL / 5) + 1), mode="nearest")
d2_ok = (sp_line >= SP_MIN) & (ito_line >= ITO_MIN) & (ito_line <= ITO_MAX)
j, k = np.unravel_index(np.argmax(np.where(d2_ok, d2_box, -1)), d2_box.shape)
itoD2 = dict(robust_best=dict(t_spacer=float(sp_line[j, 0]), t_ito=float(ito_line[0, k]),
                              A_fringe_avg=float(d2_mean[j, k]), A_boxmean_pm10nm=float(d2_box[j, k]),
                              A_worst_pm10nm=float(d2_rob[j, k]),
                              A_coherent_min=float(d2_min[j, k]), A_coherent_max=float(d2_max[j, k])))
jb = j
for ti in (0.0, 50.0, 100.0, 125.0):
    kk = int(np.argmin(np.abs(ito_line[0] - ti)))
    jj = int(np.argmax(np.where(sp_line[:, 0] >= SP_MIN, d2_mean[:, kk], -1)))
    itoD2[f"ITO{ti:.0f}"] = dict(t_spacer_best=float(sp_line[jj, 0]), A_fringe_avg=float(d2_mean[jj, kk]),
                                 A_coherent_min=float(d2_min[jj, kk]), A_coherent_max=float(d2_max[jj, kk]),
                                 A_ITO=float(d2_mean_ito[jj, kk]))
# cone average with a fixed (coherent) 10.000 um D2 - angular spread washes fringes out
best_sp, best_ito = itoD2["robust_best"]["t_spacer"], itoD2["robust_best"]["t_ito"]
for ti in sorted({best_ito, 50.0}):
    for dist in DET_DIST:
        vals = [cone_avg(lambda: stack_itoD2(nk, best_sp, ti, T_D2 + dd), lam, dist)[0]
                for dd in np.linspace(0, lam / (2 * n_d2), 4, endpoint=False)]
        itoD2[f"cone_coherent_ITO{ti:.0f}_{dist:.0f}um"] = dict(min=float(min(vals)), max=float(max(vals)))
for lw in (614, 650):
    m, _, _ = fringe_avg(lambda d2: stack_itoD2(NK[lw], best_sp, best_ito, d2), lw, NK[lw]["SiO2"])
    itoD2[f"{lw}nm_fringe_avg"] = float(m)
results["ito_on_D2"] = itoD2

# ------------------------------------------------------------------ 3. Hampel 2023 check at 395 nm
nh = NK[395]


def hampel(t_bot, mirror=True, n_in=1.0):
    layers = [iso(nh["SiO2"], 130.0), wires(nh["NbTiN"], nh["SiO2"], 0.5, 10.0)]
    if mirror:
        layers += [iso(nh["SiO2"], t_bot), iso(nh["Al"], 50.0), iso(nh["SiO2"], 150.0)]
    else:
        layers += [iso(nh["SiO2"], t_bot)]
    return absorb_normal((layers, n_in, nh["Si"]), 395.0, layer=1)[2]


tb = np.arange(100, 301, 1.0)
h_curve = hampel(tb)
hamp = dict(A_trap_212nm=float(hampel(212.0)), A_standalone_186nm=float(hampel(186.0)),
            A_186nm_fibre_index_incidence=float(hampel(186.0, n_in=nh["SiO2"])),
            model_optimum_bottom_oxide=float(tb[np.argmax(h_curve)]), A_model_optimum=float(h_curve.max()),
            A_no_mirror_336nm_on_Si=float(hampel(336.0, mirror=False)),
            A_no_mirror_best_100_400nm=float(hampel(np.arange(100, 401, 1.0), mirror=False).max()),
            measured_SDE=dict(mirror=0.68, no_mirror=0.40))
results["hampel_check_395nm"] = hamp

# ------------------------------------------------------------------ figures
fig, axs = plt.subplots(2, 3, figsize=(15, 8.5))
i_d = int(np.argmin(np.abs(t_ito - d_ito)))
k_d = int(np.argmin(np.abs(cap1d - d_cap)))
j_d = int(np.argmin(np.abs(sp1d - d_sp)))
ax = axs[0, 0]
ax.plot(sp1d, cube[i_d, :, k_d], label=f"etched, ITO {d_ito:.0f} nm, cap {d_cap:.0f} nm")
k0n = int(np.argmin(np.abs(cap1d - results["no_ITO_robust"]["t_cap"])))
ax.plot(sp1d, cube[0, :, k0n], label=f"etched, no ITO, cap {cap1d[k0n]:.0f} nm")
kb = int(np.argmin(np.abs(ito_line[0] - best_ito)))
ax.plot(sp1d, d2_mean[:, kb], label=f"ITO {best_ito:.0f} nm on D2 (fringe avg)")
ax.fill_between(sp1d, d2_min[:, kb], d2_max[:, kb], color="C2", alpha=0.15, label="ITO on D2, coherent range")
ax.plot(sp1d, nm_cube[1][:, k_d], "k:", label="no mirror (Si), ITO 50 nm")
ax.set(xlabel="spacer Al -> NbN (nm)", ylabel="A_NbN at 493 nm (normal, unpolarised)", title="spacer sweep")
ax.legend(fontsize=7)
ax = axs[0, 1]
im = ax.pcolormesh(cap1d, sp1d, cube[i_d], shading="auto", vmin=0, vmax=cube.max())
ax.contour(cap1d, sp1d, boxmean[i_d], levels=[0.5, 0.55], colors="w", linewidths=0.8)
ax.plot(d_cap, d_sp, "r+", ms=12)
ax.plot(D2nd["t_cap"], D2nd["t_spacer"], "rx", ms=8)
fig.colorbar(im, ax=ax, label="A_NbN")
ax.set(xlabel="cap NbN -> ITO (nm)", ylabel="spacer (nm)",
       title=f"etched, ITO {d_ito:.0f} nm (white: +/-10 nm box mean 0.5, 0.55)")
ax = axs[0, 2]
best_per_ito = cube.reshape(len(t_ito), -1).max(axis=1)
rob_per_ito = np.where(ok, boxmean, -1).reshape(len(t_ito), -1).max(axis=1)
ax.plot(t_ito, best_per_ito, label="etched: best spacer/cap")
ax.plot(t_ito, rob_per_ito, "--", label="etched: best mean over +/-10 nm box")
ax.plot(ito_line[0], d2_mean.max(axis=0), label="ITO on D2: best spacer (fringe avg)")
ax.set(xlabel="ITO thickness (nm)", ylabel="A_NbN", title="ITO thickness")
ax.legend(fontsize=7)
ax = axs[1, 0]
ax.plot(np.rad2deg(cone_curves_etched[0]), cone_curves_etched[1], label="etched design, plane across wires")
ax.plot(np.rad2deg(cone_curves_etched[0]), cone_curves_etched[2], label="etched design, plane along wires")
ax.axvline(np.rad2deg(np.arctan(DET_SIDE / np.sqrt(2) / DET_DIST[0])), color="0.5", ls="--", lw=0.8)
ax.set(xlabel="angle of incidence in vacuum (deg)", ylabel="A_NbN (s/p mean)", title="angle dependence")
ax.legend(fontsize=7)
ax = axs[1, 1]
names = ["493", "614", "650"]
ax.bar(np.arange(3) - 0.2, [other[f"{n}nm"]["design"] for n in names], 0.4, label="Banerjee NbN")
ax.bar(np.arange(3) + 0.2, [other[f"{n}nm"]["design_Medeiros"] for n in names], 0.4, label="Medeiros NbN")
ax.set_xticks(range(3), [f"{n} nm" for n in names])
ax.set(ylabel="A_NbN at the 493 nm design", title="stray-light wavelengths")
ax.legend(fontsize=7)
ax = axs[1, 2]
ax.plot(tb, h_curve, label="model, Al mirror")
ax.axvline(186, color="C1", ls="--", lw=0.8, label="Hampel stand-alone (186 nm)")
ax.axvline(212, color="C2", ls="--", lw=0.8, label="Hampel trap (212 nm)")
ax.axhline(0.68, color="k", lw=0.8, label="measured SDE 68 %")
ax.axhline(hamp["A_no_mirror_336nm_on_Si"], color="0.5", ls=":", label="model, no mirror")
ax.axhline(0.40, color="0.5", lw=0.8, label="measured SDE 40 % (no mirror)")
ax.set(xlabel="bottom SiO2 (nm)", ylabel="A_NbTiN at 395 nm", title="check vs Hampel 2023")
ax.legend(fontsize=7)
for a_ in axs.flat:
    a_.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "stack_tmm.png"), dpi=150)

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(dict(inputs=dict(lambda_nm=493, t_NbN=T_NBN, fill=FILL, t_Al=T_AL, t_D2=T_D2, tol_nm=TOL,
                               nk_493={k: [v.real, v.imag] if isinstance(v, complex) else v for k, v in nk.items()}),
                   etched_window=results), fh, indent=1)

# ------------------------------------------------------------------ print
print(f"\nNbN {T_NBN} nm, fill {FILL}, 493 nm, Banerjee NbN, McPeak Al, Moerland ITO")
print("ETCHED WINDOW (vacuum / ITO / cap / NbN / spacer / Al):")
for kname in ("nominal_best", "robust_best", "robust_best_1st_order_spacer", "robust_best_2nd_order_spacer",
              "no_ITO_robust"):
    r = results[kname]
    print(f"  {kname:30s} ITO {r['t_ito']:5.0f}  spacer {r['t_spacer']:5.0f}  cap {r['t_cap']:5.0f}  "
          f"A = {r['A_nominal']:.3f}  box mean {r['A_boxmean_pm10nm']:.3f}  worst {r['A_worst_pm10nm']:.3f}")
print("  per ITO thickness: nominal best (spacer/cap: A) | best box mean (spacer/cap: A, box mean, worst)")
for ti, v in per_ito.items():
    n_, r_ = v["nominal"], v["robust"]
    print(f"    ITO {ti:>3s}: {n_['t_spacer']:4.0f}/{n_['t_cap']:4.0f}: {n_['A_nominal']:.3f} | "
          f"{r_['t_spacer']:4.0f}/{r_['t_cap']:4.0f}: {r_['A_nominal']:.3f}, {r_['A_boxmean_pm10nm']:.3f}, {r_['A_worst_pm10nm']:.3f}  A_ITO {r_['A_ITO']:.3f}")
print("  no mirror (Si below), re-optimised:",
      {k: round(v["A_nominal"], 3) for k, v in results.items() if k.startswith("no_mirror")})
print("  design with the mirror removed (same thicknesses):", round(results["design_mirror_removed_same_thicknesses"], 3))
print("  polarisation at design:", {k: round(v, 3) for k, v in results["design_polarisation"].items()})
print("  one-at-a-time +/-10 nm:", tol_table)
print("  sensitivity:", json.dumps(sens, indent=None))
print("  other wavelengths:", other)
print("  cone average:", cone)
print("ITO ON TOP OF D2 (vacuum / ITO / 10 um SiO2 / NbN / spacer / Al):")
for kname, v in itoD2.items():
    print(f"  {kname}: {v}")
print("HAMPEL 2023 CHECK (395 nm, NbTiN 10 nm):", hamp)
