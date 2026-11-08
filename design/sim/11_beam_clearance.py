"""11 - Laser beam clearance over the chip surface at h = 50 um.

A Gaussian beam focused on the ion (height h) travels parallel to the surface. Over a path of
length s_max on each side of the focus, the beam radius grows as w(s) = w0 sqrt(1 + (s/zR)^2).
The fraction of power striking the surface at the worst point is ~ 0.5 erfc(sqrt(2) h / w_max)
(1-D Gaussian tail below z = 0). Scattered light near the readout zone ends up on the SNSPD, so
the budget there is strict.

For each wavelength (138Ba+: 493 cooling/detection, 650 repump, 553 + 405 nm photoionization
would only be used at the loading zone) and each path half-length, w0 is chosen to minimise
w_max (w0 = sqrt(lambda s_max / pi)), and the clipped fraction is reported.

Path half-length for a beam at angle theta to the trap axis over a chip half-width D:
s_max = D / sin(theta). On a full 10 mm chip with the trap axis on the centre line, D = 5 mm.
A bowtie (notched) chip near the zone reduces D to the isthmus half-width.

Outputs: sim/out/11_beam_clearance/clearance.png, summary.json
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "11_beam_clearance")
os.makedirs(OUT, exist_ok=True)
H = 50e-6
LAMBDAS = {"493 nm (cool/detect)": 493e-9, "650 nm (repump)": 650e-9, "405 nm (PI step 2)": 405e-9}
THETA = np.deg2rad(45.0)


def clip(lam, s_max, h=H):
    w0 = np.sqrt(lam * s_max / np.pi)            # minimises w(s_max)
    w_max = w0 * np.sqrt(2.0)
    return 0.5 * erfc(np.sqrt(2) * h / w_max), w0, w_max


D = np.linspace(0.2e-3, 5e-3, 400)                 # chip half-width across the beam path
fig, ax = plt.subplots(figsize=(6.5, 4))
summary = {}
for name, lam in LAMBDAS.items():
    fr = np.array([clip(lam, d / np.sin(THETA))[0] for d in D])
    ax.semilogy(D * 2e3, np.maximum(fr, 1e-30), label=name)
    # widest isthmus that keeps clipping below 1e-6 (readout) and 1e-4 (elsewhere)
    ok6 = D[fr < 1e-6]
    ok4 = D[fr < 1e-4]
    summary[name] = dict(full_chip_10mm=float(clip(lam, 5e-3 / np.sin(THETA))[0]),
                         max_isthmus_mm_clip_1em6=float(2e3 * ok6.max()) if ok6.size else None,
                         max_isthmus_mm_clip_1em4=float(2e3 * ok4.max()) if ok4.size else None)
for lvl in (1e-6, 1e-4):
    ax.axhline(lvl, color="0.5", lw=0.7, ls="--")
ax.set(xlabel="chip width crossed by the beam, 2D (mm)", ylabel="fraction of beam power hitting the surface",
       title=f"beam at {np.rad2deg(THETA):.0f} deg to the axis, ion height {H*1e6:.0f} um", ylim=(1e-20, 1))
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "clearance.png"), dpi=150)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
for k, v in summary.items():
    print(f"{k}: full 10 mm chip clips {v['full_chip_10mm']:.2e}; widest isthmus for 1e-6: "
          f"{v['max_isthmus_mm_clip_1em6']} mm, for 1e-4: {v['max_isthmus_mm_clip_1em4']} mm")

# ---------------------------------------------------------------- square chip, zones near a corner
# (DESIGN_LOG step 8: the team chose a plain diced 10 x 10 mm chip, no bowtie). A beam at 45 deg to
# the trap axis through a zone at distance dx from the right edge and dy from the top edge crosses
# the chip corner: path on chip = sqrt(2) dy before the focus and sqrt(2) dx after it. The worst-
# case radius is minimised by a waist placed at the zone with w0 = sqrt(lambda s_max / pi).
print("\nsquare 10 mm chip, beams at 45 deg cutting the top-right corner:")
corner = {}
for zone, dx, dy in (("readout", 800e-6, 800e-6), ("loading", 1400e-6, 800e-6), ("chip centre", 5e-3, 5e-3)):
    s_max = np.sqrt(2) * max(dx, dy)
    corner[zone] = {name: float(clip(lam, s_max)[0]) for name, lam in LAMBDAS.items()}
    print(f"  {zone:11s} (dx {dx*1e6:.0f}, dy {dy*1e6:.0f} um): " +
          ", ".join(f"{k.split()[0]} nm {v:.1e}" for k, v in corner[zone].items()))
with open(os.path.join(OUT, "corner_summary.json"), "w") as fh:
    json.dump(corner, fh, indent=1)

# ---------------------------------------------------------------- narrow 10 x 2.5 mm die (log step 12)
# Trap axis on the die centre line, 1.25 mm from both long edges; beams at 45 deg cross the die
# width only: path on chip = sqrt(2) * 1.25 mm on each side of the focus.
print("\nnarrow 10 x 2.5 mm die, trap on the centre line, beams at 45 deg:")
narrow = {}
for width in (2.0e-3, 2.5e-3, 3.0e-3):
    s_max = np.sqrt(2) * width / 2
    narrow[f"{width*1e3:.1f} mm"] = {name: float(clip(lam, s_max)[0]) for name, lam in LAMBDAS.items()}
    print(f"  die width {width*1e3:.1f} mm: " + ", ".join(f"{k.split()[0]} nm {v:.1e}" for k, v in narrow[f'{width*1e3:.1f} mm'].items()))
with open(os.path.join(OUT, "narrow_summary.json"), "w") as fh:
    json.dump(narrow, fh, indent=1)
