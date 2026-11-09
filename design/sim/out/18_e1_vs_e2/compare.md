# 18 - E1 vs E2 comparison

Claude-authored. Written by design/sim/18_e1_vs_e2.py; regenerate rather than edit. No option is recommended here.

| Part | Quantity | E1 | E2 | Unit | Source |
|---|---|---|---|---|---|
| 1 Au resistance | Rs, room temperature, bulk rho = 2.44e-08 ohm m | 0.0697 | 0.0041 | ohm/sq | [team calc] rho / t; rho [verify] |
| 1 Au resistance | Rs, 4 K, bulk rho, RRR = 2 | 0.0349 | 0.0020 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs, 4 K, bulk rho, RRR = 5 | 0.0139 | 0.0008 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs, 4 K, bulk rho, RRR = 10 | 0.0070 | 0.0004 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs, room temperature, film rho = 4.00e-08 ohm m | 0.1143 | 0.0067 | ohm/sq | [team calc] rho / t; rho [verify] |
| 1 Au resistance | Rs, 4 K, film rho, RRR = 2 | 0.0571 | 0.0033 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs, 4 K, film rho, RRR = 5 | 0.0229 | 0.0013 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs, 4 K, film rho, RRR = 10 | 0.0114 | 0.0007 | ohm/sq | [team calc] rho / (RRR t); RRR [verify] |
| 1 Au resistance | Rs(E1) / Rs(E2) (any rho) | 17.14 | - | ratio | [team calc] = t(E2) / t(E1) = 6 / 0.35 |
| 1 Au resistance | Skin depth at 28 MHz, bulk rho | 14.86 | 14.86 | um | [team calc] sqrt(rho / (pi f mu0)) |
| 1 Au resistance | t < skin depth (bulk rho): DC sheet resistance applies | yes | yes | - | [team calc] |
| 1 Au resistance | Skin depth at 28 MHz, film rho | 19.02 | 19.02 | um | [team calc] sqrt(rho / (pi f mu0)) |
| 1 Au resistance | t < skin depth (film rho): DC sheet resistance applies | yes | yes | - | [team calc] |
| 2 squares | RF rail, one rail (two rails) | 47.62 | 47.62 | sq | [team calc] (XRF1 - XRF0) / A |
| 2 squares | RF feed lead, 2060 to 4700 at 60 um | 44.00 | 44.00 | sq | [team calc] 2640 / 60 |
| 2 squares | SNSPD slot lead, brief tail (300 um) | 974.0 | 974.0 | sq | [team calc] brief geometry: about 300 um tail |
| 2 squares | SNSPD slot lead, drawn tail (402 um) | 994.5 | 994.5 | sq | [team calc] make_chip.py path X_LEAD_END -> X_BEND -> X_SNPAD |
| 2 squares | Centre DC lead, x-span -2040 to -4650 at 7.5 um | 348.0 | 348.0 | sq | [team calc] span only (brief) |
| 2 squares | Centre DC lead, drawn polyline at 7.5 um | 394.0 | 394.0 | sq | [team calc] make_chip.py path (-2040 -> -3600 -> -3700,450 -> -4650,450) |
| 2 squares | R at room temperature, bulk rho: RF rail (one) | 3.3197 | 0.1937 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, bulk rho: RF feed lead | 3.0674 | 0.1789 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, bulk rho: SNSPD slot lead (drawn) | 69.3289 | 4.0442 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, bulk rho: centre DC lead (drawn) | 27.4686 | 1.6023 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, film rho: RF rail (one) | 5.4422 | 0.3175 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, film rho: RF feed lead | 5.0286 | 0.2933 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, film rho: SNSPD slot lead (drawn) | 113.6540 | 6.6298 | ohm | [team calc] squares x Rs |
| 2 squares | R at room temperature, film rho: centre DC lead (drawn) | 45.0305 | 2.6268 | ohm | [team calc] squares x Rs |
| 3 RF heating | RF current amplitude, C_rf = 1 pF | 9.324 | 9.324 | mA | [team calc] 2 pi f C_rf V; C_rf [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, bulk rho, RRR = 2 | 78.70 | 4.59 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, bulk rho, RRR = 5 | 31.48 | 1.84 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, bulk rho, RRR = 10 | 15.74 | 0.92 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, film rho, RRR = 2 | 129.01 | 7.53 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, film rho, RRR = 5 | 51.61 | 3.01 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 1 pF, film rho, RRR = 10 | 25.80 | 1.51 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | RF current amplitude, C_rf = 2 pF | 18.648 | 18.648 | mA | [team calc] 2 pi f C_rf V; C_rf [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, bulk rho, RRR = 2 | 314.79 | 18.36 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, bulk rho, RRR = 5 | 125.92 | 7.35 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, bulk rho, RRR = 10 | 62.96 | 3.67 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, film rho, RRR = 2 | 516.05 | 30.10 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, film rho, RRR = 5 | 206.42 | 12.04 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 2 pF, film rho, RRR = 10 | 103.21 | 6.02 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | RF current amplitude, C_rf = 5 pF | 46.621 | 46.621 | mA | [team calc] 2 pi f C_rf V; C_rf [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, bulk rho, RRR = 2 | 1967.44 | 114.77 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, bulk rho, RRR = 5 | 786.98 | 45.91 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, bulk rho, RRR = 10 | 393.49 | 22.95 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, film rho, RRR = 2 | 3225.32 | 188.14 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, film rho, RRR = 5 | 1290.13 | 75.26 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 3 RF heating | P upper bound, C_rf = 5 pF, film rho, RRR = 10 | 645.06 | 37.63 | uW | [team calc] rho_4K = rho_RT / RRR; C_rf, RRR [verify] |
| 4 SNSPD slot lead | one lead R, room temperature, bulk rho | 69.33 | 4.04 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), room temperature, bulk rho | 138.66 | 8.09 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, room temperature, bulk rho | 0.2650 | 0.8608 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, room temperature, film rho | 113.65 | 6.63 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), room temperature, film rho | 227.31 | 13.26 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, room temperature, film rho | 0.1803 | 0.7904 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, bulk rho, RRR = 2 | 34.66 | 2.02 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, bulk rho, RRR = 2 | 69.33 | 4.04 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, bulk rho, RRR = 2 | 0.4190 | 0.9252 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, bulk rho, RRR = 5 | 13.87 | 0.81 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, bulk rho, RRR = 5 | 27.73 | 1.62 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, bulk rho, RRR = 5 | 0.6432 | 0.9687 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, bulk rho, RRR = 10 | 6.93 | 0.40 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, bulk rho, RRR = 10 | 13.87 | 0.81 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, bulk rho, RRR = 10 | 0.7829 | 0.9841 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, film rho, RRR = 2 | 56.83 | 3.31 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, film rho, RRR = 2 | 113.65 | 6.63 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, film rho, RRR = 2 | 0.3055 | 0.8829 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, film rho, RRR = 5 | 22.73 | 1.33 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, film rho, RRR = 5 | 45.46 | 2.65 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, film rho, RRR = 5 | 0.5238 | 0.9496 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 4 SNSPD slot lead | one lead R, 4 K, film rho, RRR = 10 | 11.37 | 0.66 | ohm | [team calc] drawn lead squares x Rs |
| 4 SNSPD slot lead | pair R (two in series), 4 K, film rho, RRR = 10 | 22.73 | 1.33 | ohm | [team calc] |
| 4 SNSPD slot lead | 50 ohm line: pulse amplitude factor = reset-time factor, 4 K, film rho, RRR = 10 | 0.6875 | 0.9742 | - | [team calc] 50/(50+R_pair); reset time = L_k/(50+R_pair) |
| 5 SiO2 screening | exp(-pi t/g), g = 5 um | 0.8026 | 0.02305 | - | [inference]: lowest-mode estimate, not a field solve |
| 5 SiO2 screening | E1/E2 ratio, g = 5 um | 34.8 | - | - | [inference]: lowest-mode estimate, not a field solve |
| 5 SiO2 screening | exp(-pi t/g), g = 10 um | 0.8959 | 0.15184 | - | [inference]: lowest-mode estimate, not a field solve |
| 5 SiO2 screening | E1/E2 ratio, g = 10 um | 5.9 | - | - | [inference]: lowest-mode estimate, not a field solve |
| 5 SiO2 screening | exp(-pi t/g), g = 30 um | 0.9640 | 0.53349 | - | [inference]: lowest-mode estimate, not a field solve |
| 5 SiO2 screening | E1/E2 ratio, g = 30 um | 1.8 | - | - | [inference]: lowest-mode estimate, not a field solve |
| 6 quoted simulated numbers | Window null drop, A30 | <= 0.37 | 1.19 | um | quoted: DESIGN_LOG.md step 25 (E1 is an upper bound from a 1 um pocket) |
| 6 quoted simulated numbers | Window null drop, B60 | <= 0.55 | 2.04 | um | quoted: DESIGN_LOG.md step 26 |
| 6 quoted simulated numbers | Micromotion after undoing the drop, 10 deg tilt, A30 | 54.88 | 173.36 | nm | quoted: DESIGN_LOG.md step 29 |
| 6 quoted simulated numbers | Micromotion after undoing the drop, 10 deg tilt, B60 | 81.46 | 290.83 | nm | quoted: DESIGN_LOG.md step 29 |
| 6 quoted simulated numbers | A30 geometric collection | 2.601-2.636 | 2.221 | % | quoted: DESIGN_LOG.md, v4 SNSPD overhang audit |
| 6 quoted simulated numbers | Nanowire RF pickup | 1.92 | 0.96 | uA | quoted: DESIGN_LOG.md step 26 (10b) |
| 6 quoted simulated numbers | RF pickup per slot lead | 28.3 | 44.5 | uA | quoted: DESIGN_LOG.md step 28 |
| 6 quoted simulated numbers | SiO2 gap depth-to-width ratio | 0.07 | 1.2 | - | quoted: fab/variants/LOCAL_MIRROR.md H.4 |
| 6 quoted simulated numbers | DC voltages for zones and transport | same to 0.01 V | reference | V | quoted: DESIGN_LOG.md step 25 |

## Acceptance

- PASS: Rs(E1)/Rs(E2) = 17.14 (value 17.143)
- PASS: exp(-pi t/g), g = 5, E1 = 0.803 (value 0.8026)
- PASS: exp(-pi t/g), g = 5, E2 = 0.0230 (value 0.02305)
- PASS: exp ratio about 35 (value 34.8)
- PASS: Rs(E1) bulk RT = 0.0697 ohm/sq (value 0.06971)
- PASS: one slot lead E1 bulk RT roughly 65-70 ohm (value 69.33)
- PASS: one slot lead E2 bulk RT about 4 ohm (value 4.044)
- PASS: skin depth at 28 MHz, bulk rho = 14.9 um (value 14.86)

## Inputs tagged [verify]

- rho_RT bulk 2.44e-8 ohm m (bulk Au at 20 C)
- rho_RT thin evaporated film 4.0e-8 ohm m
- RRR = 2, 5, 10 (4 K residual resistance ratio)
- C_rf = 1, 2, 5 pF (chip RF capacitance not computed)
- Slot-lead tail: brief said about 300 um; drawn path is 402 um (both shown)
- Centre DC lead: brief span to -4650 (348 sq) vs drawn polyline (394 sq) (both shown)
