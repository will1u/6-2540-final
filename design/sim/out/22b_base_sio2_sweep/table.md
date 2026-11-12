> **Claude-authored.** Written by sim/22b_base_sio2_sweep.py (regenerate, do not edit).

## Acceptance (sim 22 A30 chip totals reproduced) [team calc]

- E2: C_chip 2.5900 pF (sim 22 2.590); grounded-Si 22.6276 pF (sim 22 22.628): PASS
- E1: C_chip 2.3947 pF (sim 22 2.395); grounded-Si 22.4097 pF (sim 22 22.410): PASS

## Sweep: A30 chip, raised 100 nm Al mirror [team calc]

Base SiO2 = the SiO2 under the Al mirror and under the spacer. Cap = SiO2 over the NbN. Current I = omega C V_RF, V_RF = 53 V, 28 MHz. Energy fractions are length-weighted, as sim 22's config().

| Die option | Row | Base SiO2 (um) | Cap SiO2 (um) | C_chip, Si lossless (pF) | C_chip, Si grounded (pF) | p_Si | p_SiO2 | I (mA) |
|---|---|---|---|---|---|---|---|---|
| E2 | sweep | 0.15 | 0.110 | 2.878 | 57.542 | 0.7411 | 0.1092 | 26.84 |
| E2 | sweep | 0.30 | 0.110 | 2.813 | 45.125 | 0.7173 | 0.1298 | 26.23 |
| E2 | sweep | 0.50 | 0.110 | 2.738 | 35.134 | 0.6896 | 0.1536 | 25.53 |
| E2 | sweep | 1.00 | 0.110 | 2.589 | 22.773 | 0.6334 | 0.2013 | 24.14 |
| E2 | sweep | 2.00 | 0.110 | 2.383 | 13.572 | 0.5511 | 0.2701 | 22.22 |
| E1 | sweep | 0.15 | 0.110 | 2.682 | 57.307 | 0.7888 | 0.1177 | 25.01 |
| E1 | sweep | 0.30 | 0.110 | 2.617 | 44.893 | 0.7644 | 0.1400 | 24.40 |
| E1 | sweep | 0.50 | 0.110 | 2.542 | 34.907 | 0.7362 | 0.1656 | 23.70 |
| E1 | sweep | 1.00 | 0.110 | 2.394 | 22.555 | 0.6787 | 0.2174 | 22.32 |
| E1 | sweep | 2.00 | 0.110 | 2.188 | 13.363 | 0.5940 | 0.2929 | 20.40 |
| E2 | comparison (cap only) | 1.00 | 0.160 | 2.578 | 22.010 | 0.6289 | 0.2052 | 24.04 |
| E1 | comparison (cap only) | 1.00 | 0.160 | 2.383 | 21.792 | 0.6740 | 0.2217 | 22.22 |

## Grid check [team calc]

Plain section, base SiO2 0.15 um, cap 0.110 um, E2 (6.0 um Au). Half-domain capacitance: 0.275356 pF/mm at the sim 22 grid, 0.274971 pF/mm at half the spacing. Relative change 0.14% (below 1 %).

## Limits

2-D; ideal conductors; end effects neglected [inference]; the raised mirror step is not modelled in the electrode shape (flat zero-volt box, as sim 22) [inference]; a10 limits are for the chip alone [inference].
