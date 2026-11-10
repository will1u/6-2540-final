> **Claude-authored.** Written by design/sim/22_rf_capacitance.py (regenerate, do not edit), 2026-11-10.

## Section table

Per unit: pF/mm per rail (slot, plain) or for the full strip (ubar, feed, pad). Section pF = both halves x length. [team calc]

| Config | Section | Length (um) | Per unit (pF/mm) | Section (pF) | p_Si | p_SiO2 | Section with grounded Si (pF) |
|---|---|---|---|---|---|---|---|
| A30_E2 | slot | 2240 | 0.25069 (per rail) | 1.1231 | 0.6073 | 0.2139 | 9.6364 |
| A30_E2 | plain | 1760 | 0.24566 (per rail) | 0.8647 | 0.5986 | 0.2185 | 7.6082 |
| A30_E2 | ubar | 75 | 0.33687 (full strip) | 0.0253 | 0.6831 | 0.1618 | 0.4109 |
| A30_E2 | feed | 2525 | 0.20973 (full strip) | 0.5296 | 0.6627 | 0.1911 | 3.9656 |
| A30_E2 | pad | 200 | 0.23667 (full strip) | 0.0473 | 0.8058 | 0.0892 | 1.0064 |
| A30_E1 | slot | 2240 | 0.23006 (per rail) | 1.0307 | 0.6609 | 0.2333 | 9.5367 |
| A30_E1 | plain | 1760 | 0.22492 (per rail) | 0.7917 | 0.6528 | 0.2388 | 7.5297 |
| A30_E1 | ubar | 75 | 0.31611 (full strip) | 0.0237 | 0.7272 | 0.1725 | 0.4093 |
| A30_E1 | feed | 2525 | 0.19887 (full strip) | 0.5021 | 0.6970 | 0.2026 | 3.9298 |
| A30_E1 | pad | 200 | 0.23217 (full strip) | 0.0464 | 0.8188 | 0.0925 | 1.0042 |
| NODET_E2_full | plain | 4000 | 0.24566 (per rail) | 1.9653 | 0.5986 | 0.2185 | 17.2914 |
| NODET_E2_full | ubar | 75 | 0.33687 (full strip) | 0.0253 | 0.6831 | 0.1618 | 0.4109 |
| NODET_E2_full | feed | 2525 | 0.20973 (full strip) | 0.5296 | 0.6627 | 0.1911 | 3.9656 |
| NODET_E2_full | pad | 200 | 0.23667 (full strip) | 0.0473 | 0.8058 | 0.0892 | 1.0064 |
| NODET_E2_thermal | plain | 4000 | 0.25659 (per rail) | 2.0527 | 0.6422 | 0.1821 | 23.9280 |
| NODET_E2_thermal | ubar | 75 | 0.34798 (full strip) | 0.0261 | 0.7138 | 0.1357 | 0.5720 |
| NODET_E2_thermal | feed | 2525 | 0.21819 (full strip) | 0.5509 | 0.7043 | 0.1549 | 5.4783 |
| NODET_E2_thermal | pad | 200 | 0.24122 (full strip) | 0.0482 | 0.8271 | 0.0701 | 1.4015 |
| NODET_E1_full | plain | 4000 | 0.22492 (per rail) | 1.7994 | 0.6528 | 0.2388 | 17.1129 |
| NODET_E1_full | ubar | 75 | 0.31611 (full strip) | 0.0237 | 0.7272 | 0.1725 | 0.4093 |
| NODET_E1_full | feed | 2525 | 0.19887 (full strip) | 0.5021 | 0.6970 | 0.2026 | 3.9298 |
| NODET_E1_full | pad | 200 | 0.23217 (full strip) | 0.0464 | 0.8188 | 0.0925 | 1.0042 |
| NODET_E1_thermal | plain | 4000 | 0.23579 (per rail) | 1.8863 | 0.6977 | 0.1986 | 23.7447 |
| NODET_E1_thermal | ubar | 75 | 0.32715 (full strip) | 0.0245 | 0.7582 | 0.1446 | 0.5702 |
| NODET_E1_thermal | feed | 2525 | 0.20730 (full strip) | 0.5234 | 0.7393 | 0.1643 | 5.4409 |
| NODET_E1_thermal | pad | 200 | 0.23674 (full strip) | 0.0473 | 0.8403 | 0.0729 | 1.3992 |

## Chip totals [team calc]

Chip = sum of sections; end effects neglected [inference]. p values are length-weighted means (as the brief asks); the C-weighted values are in summary.json.

| Config | C_chip (pF), Si lossless | C_chip (pF), Si as grounded conductor | p_Si (length-wt) | p_SiO2 (length-wt) |
|---|---|---|---|---|
| A30_E2 | 2.590 | 22.628 | 0.6323 | 0.2024 |
| A30_E1 | 2.395 | 22.410 | 0.6776 | 0.2185 |
| NODET_E2_full | 2.567 | 22.674 | 0.6294 | 0.2039 |
| NODET_E2_thermal | 2.678 | 31.380 | 0.6715 | 0.1682 |
| NODET_E1_full | 2.372 | 22.456 | 0.6749 | 0.2203 |
| NODET_E1_thermal | 2.482 | 31.155 | 0.7180 | 0.1816 |

## Loss and Q [inference: first-order, small-loss]

tan_d Si at 28 MHz with rho = 200 Ohm m: 0.2743 (not small: order-of-magnitude only). At 5 K the Si is treated as lossless (carriers frozen out, as 10b). tan_d Si at 1 MHz, room temperature: 7.68 (the Si conducts more than it stores).

| Config | tan_d SiO2 [verify] | Q (room temperature, Si lossy) | Q (cold, Si lossless) |
|---|---|---|---|
| A30_E2 | 0.0001 | 5.8 | 49415.0 |
| A30_E2 | 0.001 | 5.8 | 4941.5 |
| A30_E2 | 0.01 | 5.7 | 494.1 |
| A30_E1 | 0.0001 | 5.4 | 45760.4 |
| A30_E1 | 0.001 | 5.4 | 4576.0 |
| A30_E1 | 0.01 | 5.3 | 457.6 |
| NODET_E2_full | 0.0001 | 5.8 | 49053.6 |
| NODET_E2_full | 0.001 | 5.8 | 4905.4 |
| NODET_E2_full | 0.01 | 5.7 | 490.5 |
| NODET_E2_thermal | 0.0001 | 5.4 | 59449.8 |
| NODET_E2_thermal | 0.001 | 5.4 | 5945.0 |
| NODET_E2_thermal | 0.01 | 5.4 | 594.5 |
| NODET_E1_full | 0.0001 | 5.4 | 45388.5 |
| NODET_E1_full | 0.001 | 5.4 | 4538.9 |
| NODET_E1_full | 0.01 | 5.3 | 453.9 |
| NODET_E1_thermal | 0.0001 | 5.1 | 55077.9 |
| NODET_E1_thermal | 0.001 | 5.1 | 5507.8 |
| NODET_E1_thermal | 0.01 | 5.0 | 550.8 |

## RF heating bound (sim 18 formula) [team calc]

Sim 18 bound: 0.5 I^2 R_feed + I^2 R_rail / 12, I = omega C V. Linear-fall line: rail term / 3 (brief's sensitivity line; sim 18's 1/12 already assumes a linear fall along the rail). Upper bound: the full current through the whole resistance, as sim 18.

| Config | C_chip (pF) | I (mA) | P, bulk, RRR 2 (mW) | P linear, bulk, RRR 2 (mW) | P, film, RRR 2 (mW) | P linear, film, RRR 2 (mW) |
|---|---|---|---|---|---|---|
| A30_E2 | 2.590 | 24.150 | 0.0308 | 0.0277 | 0.0505 | 0.0453 |
| A30_E1 | 2.395 | 22.328 | 0.4513 | 0.4053 | 0.7398 | 0.6644 |
| NODET_E2_full | 2.567 | 23.939 | 0.0303 | 0.0272 | 0.0496 | 0.0446 |
| NODET_E2_thermal | 2.678 | 24.970 | 0.0329 | 0.0296 | 0.0540 | 0.0485 |
| NODET_E1_full | 2.372 | 22.114 | 0.4427 | 0.3976 | 0.7257 | 0.6517 |
| NODET_E1_thermal | 2.482 | 23.139 | 0.4847 | 0.4353 | 0.7945 | 0.7136 |

## Resonator table [team calc; C_other sources cited per row]

P = omega C_tot V^2 / (2 Q) at V = 53 V; L = 1/(omega^2 C_tot); df/f = -dC/(2 C_tot) per pF of error.

| Chip | C_chip (pF) | C_other (pF) | C_tot (pF) | L (uH) | P at Q 50 / 100 / 200 / 500 (mW) | df/f per pF (%) | Source of C_other |
|---|---|---|---|---|---|---|---|
| A30_E2 | 2.590 | 3 | 5.590 | 5.780 | 27.6 / 13.8 / 6.9 / 2.8 | -8.945 | design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 97 (Zhao et al.: RF-to-ground 3 pF after wire-bond pads removed; a trap-die value, used as a size reference [inference]) |
| A30_E2 | 2.590 | 7 | 9.590 | 3.369 | 47.4 / 23.7 / 11.8 / 4.7 | -5.214 | design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 95 (Stick et al.: 7 pF RF-to-ground, trap and CPGA package) |
| A30_E2 | 2.590 | 17 | 19.590 | 1.649 | 96.8 / 48.4 / 24.2 / 9.7 | -2.552 | design/research/research_notes/Bond pad sizing for ion traps/pad_electrical_effects.md line 20 (Siverns et al.: 17 +/- 2 pF, ion trap plus vacuum system) |
| A30_E1 | 2.395 | 3 | 5.395 | 5.989 | 26.7 / 13.3 / 6.7 / 2.7 | -9.268 | design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 97 (Zhao et al.: RF-to-ground 3 pF after wire-bond pads removed; a trap-die value, used as a size reference [inference]) |
| A30_E1 | 2.395 | 7 | 9.395 | 3.439 | 46.4 / 23.2 / 11.6 / 4.6 | -5.322 | design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 95 (Stick et al.: 7 pF RF-to-ground, trap and CPGA package) |
| A30_E1 | 2.395 | 17 | 19.395 | 1.666 | 95.8 / 47.9 / 24.0 / 9.6 | -2.578 | design/research/research_notes/Bond pad sizing for ion traps/pad_electrical_effects.md line 20 (Siverns et al.: 17 +/- 2 pF, ion trap plus vacuum system) |

## Acceptance

- PASS: reproduces_10c_slot_E2
- PASS: reproduces_10b_rail
- PASS: grid_converged
- PASS: reproduces_sim18_1pF_row
- PASS: feed_sanity

Limits: 2-D; ideal conductors; B60 = A30 [inference]; end effects neglected [inference]; a10 limits are for the chip alone, not the packaged device [inference].
