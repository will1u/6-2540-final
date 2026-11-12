> **Claude-authored.** Written by sim/24b_rcwa_stack_scan.py (regenerate, do not edit).

## Acceptance (spacer 238, NbN 7 nm, n 1.463, no ITO)

| cap (nm) | along | across | unpol | sim 24 unpol | abs diff | nG along | nG across |
|---|---|---|---|---|---|---|---|
| 160 | 0.82166 | 0.83383 | 0.82775 | 0.8274 | 0.00035 | 55 | 55 |
| 80 | 0.57816 | 0.58781 | 0.58298 | 0.5826 | 0.00038 | 55 | 55 |

Solve time (one grcwa solve, request 9): 0.015 s. Every solve uses a fixed harmonic request of 57 (nG 55); the script's docstring gives the reason and the 0.0005 it costs.

## Top 5 nominals by worst corner (spacer 220..250, cap 140..180, +-10 nm box)

| spacer (nm) | cap (nm) | box mean | worst corner |
|---|---|---|---|
| 240 | 160 | 0.8027 | 0.7638 |
| 235 | 170 | 0.8034 | 0.7598 |
| 230 | 175 | 0.7987 | 0.7537 |
| 245 | 150 | 0.7921 | 0.7532 |
| 235 | 165 | 0.8036 | 0.7525 |

## Tolerance box at 238 / 160

| spacer (nm) | cap 150 | cap 160 | cap 170 |
|---|---|---|---|
| 228 | 0.7529 | 0.7933 | 0.8172 |
| 238 | 0.8071 | 0.8277 | 0.8253 |
| 248 | 0.8137 | 0.8075 | 0.7792 |

Box mean 0.8027, worst corner 0.7529.

**Decision:** 238/160 worst corner 0.7529; best worst corner 0.7638 at 240/160; difference 0.0109; Z <= 0.02: yes.

## Sensitivities at spacer 238, cap 160 (unpolarised A_nbn)

| change | value | A_nbn |
|---|---|---|
| NbN thickness 6 nm | | 0.7785 |
| NbN thickness 7 nm | | 0.8277 |
| NbN thickness 8 nm | | 0.8654 |
| SiO2 index | 1.45 | 0.8230 |
| SiO2 index | 1.463 | 0.8277 |
| SiO2 index | 1.48 | 0.8269 |

## ITO on top (spacer 238, cap 60..200 step 10)

| cap (nm) | no ITO A_nbn | ITO 20 nm A_nbn | ITO 20 nm A_ito | ITO 50 nm A_nbn | ITO 50 nm A_ito |
|---|---|---|---|---|---|
| 60 | 0.6063 | 0.5446 | 0.0006 | 0.6611 | 0.0019 |
| 70 | 0.5887 | 0.5835 | 0.0005 | 0.7695 | 0.0027 |
| 80 | 0.5830 | 0.6374 | 0.0007 | 0.8653 | 0.0040 |
| 90 | 0.5894 | 0.7036 | 0.0011 | 0.9089 | 0.0055 |
| 100 | 0.6077 | 0.7743 | 0.0018 | 0.8768 | 0.0068 |
| 110 | 0.6373 | 0.8353 | 0.0027 | 0.7865 | 0.0074 |
| 120 | 0.6768 | 0.8688 | 0.0036 | 0.6778 | 0.0072 |
| 130 | 0.7227 | 0.8625 | 0.0043 | 0.5799 | 0.0067 |
| 140 | 0.7690 | 0.8189 | 0.0046 | 0.5039 | 0.0059 |
| 150 | 0.8071 | 0.7530 | 0.0044 | 0.4505 | 0.0052 |
| 160 | 0.8277 | 0.6824 | 0.0040 | 0.4172 | 0.0044 |
| 170 | 0.8253 | 0.6194 | 0.0034 | 0.4012 | 0.0037 |
| 180 | 0.8003 | 0.5700 | 0.0027 | 0.4012 | 0.0030 |
| 190 | 0.7598 | 0.5358 | 0.0021 | 0.4171 | 0.0024 |
| 200 | 0.7129 | 0.5169 | 0.0016 | 0.4504 | 0.0020 |

| case | A_nbn at 160 | A_ito at 160 | best cap | best A_nbn | A_ito at best |
|---|---|---|---|---|---|
| no ITO | 0.8277 | - | 160 | 0.8277 | - |
| ITO 20 nm | 0.6824 | 0.0040 | 120 | 0.8688 | 0.0036 |
| ITO 50 nm | 0.4172 | 0.0044 | 90 | 0.9089 | 0.0055 |

Energy: max |sum - 1| = 4.44e-15 over 620 polarised solves.
