> **Claude-authored.** Written by sim/23_dc_rf_coupling.py: RF coupling onto the DC electrodes and the filter-capacitor divider, 2026-11-10.

## Per-electrode capacitance [team calc]

| Electrode | Au | C_c, rails to electrode (pF) | C_g, to ground (pF) | of which Al mirror (pF) |
|---|---|---|---|---|
| centre DC, A30 (2240 um slot + 1760 um plain) | E2 | 0.4143 | 3.2056 | 3.0927 |
| centre DC, NODET (4000 um plain) | E2 | 0.7396 | 0.1219 | - |
| outer DC segment, 120 um (C_g from pad estimates, 5 / 8 mm lead) | E2 | 0.01495 | 0.401 / 0.581 | - |
| centre DC, A30 (2240 um slot + 1760 um plain) | E1 | 0.3290 | 3.1422 | 3.0750 |
| centre DC, NODET (4000 um plain) | E1 | 0.6567 | 0.1217 | - |
| outer DC segment, 120 um (C_g from pad estimates, 5 / 8 mm lead) | E1 | 0.01371 | 0.401 / 0.581 | - |

Mirror to centre DC: E2 3.093 pF over 2240 um, 3.769 pF over 2730 um (LOCAL_MIRROR.md quotes about 12 pF at 318 nm gap, 2.73 mm); E1 3.075 pF over 2240 um, 3.748 pF over 2730 um (LOCAL_MIRROR.md quotes about 12 pF at 318 nm gap, 2.73 mm).

## Divider and RF on the electrode, and filter current [team calc]

| Electrode | Au | C_f (pF) | V_el (V) | I = omega C_f V_el (uA) |
|---|---|---|---|---|
| centre DC (A30) (C_c 0.4143 pF, C_g 3.206 pF) | E2 | 0 | 6.067 | 0 |
| centre DC (A30) (C_c 0.4143 pF, C_g 3.206 pF) | E2 | 100 | 0.2119 | 3728 |
| centre DC (A30) (C_c 0.4143 pF, C_g 3.206 pF) | E2 | 1000 | 0.02188 | 3850 |
| centre DC (A30) (C_c 0.4143 pF, C_g 3.206 pF) | E2 | 10000 | 0.002195 | 3862 |
| centre DC (NODET) (C_c 0.7396 pF, C_g 0.122 pF) | E2 | 0 | 45.5 | 0 |
| centre DC (NODET) (C_c 0.7396 pF, C_g 0.122 pF) | E2 | 100 | 0.3886 | 6837 |
| centre DC (NODET) (C_c 0.7396 pF, C_g 0.122 pF) | E2 | 1000 | 0.03916 | 6890 |
| centre DC (NODET) (C_c 0.7396 pF, C_g 0.122 pF) | E2 | 10000 | 0.003919 | 6895 |
| outer segment, 5 mm lead (C_c 0.0149 pF, C_g 0.401 pF) | E2 | 0 | 1.905 | 0 |
| outer segment, 5 mm lead (C_c 0.0149 pF, C_g 0.401 pF) | E2 | 100 | 0.00789 | 138.8 |
| outer segment, 5 mm lead (C_c 0.0149 pF, C_g 0.401 pF) | E2 | 1000 | 0.0007919 | 139.3 |
| outer segment, 5 mm lead (C_c 0.0149 pF, C_g 0.401 pF) | E2 | 10000 | 7.922e-05 | 139.4 |
| outer segment, 8 mm lead (C_c 0.0149 pF, C_g 0.581 pF) | E2 | 0 | 1.329 | 0 |
| outer segment, 8 mm lead (C_c 0.0149 pF, C_g 0.581 pF) | E2 | 100 | 0.007876 | 138.6 |
| outer segment, 8 mm lead (C_c 0.0149 pF, C_g 0.581 pF) | E2 | 1000 | 0.0007918 | 139.3 |
| outer segment, 8 mm lead (C_c 0.0149 pF, C_g 0.581 pF) | E2 | 10000 | 7.922e-05 | 139.4 |
| centre DC (A30) (C_c 0.3290 pF, C_g 3.142 pF) | E1 | 0 | 5.023 | 0 |
| centre DC (A30) (C_c 0.3290 pF, C_g 3.142 pF) | E1 | 100 | 0.1685 | 2964 |
| centre DC (A30) (C_c 0.3290 pF, C_g 3.142 pF) | E1 | 1000 | 0.01737 | 3057 |
| centre DC (A30) (C_c 0.3290 pF, C_g 3.142 pF) | E1 | 10000 | 0.001743 | 3066 |
| centre DC (NODET) (C_c 0.6567 pF, C_g 0.122 pF) | E1 | 0 | 44.71 | 0 |
| centre DC (NODET) (C_c 0.6567 pF, C_g 0.122 pF) | E1 | 100 | 0.3453 | 6076 |
| centre DC (NODET) (C_c 0.6567 pF, C_g 0.122 pF) | E1 | 1000 | 0.03478 | 6118 |
| centre DC (NODET) (C_c 0.6567 pF, C_g 0.122 pF) | E1 | 10000 | 0.00348 | 6122 |
| outer segment, 5 mm lead (C_c 0.0137 pF, C_g 0.401 pF) | E1 | 0 | 1.752 | 0 |
| outer segment, 5 mm lead (C_c 0.0137 pF, C_g 0.401 pF) | E1 | 100 | 0.007237 | 127.3 |
| outer segment, 5 mm lead (C_c 0.0137 pF, C_g 0.401 pF) | E1 | 1000 | 0.0007264 | 127.8 |
| outer segment, 5 mm lead (C_c 0.0137 pF, C_g 0.401 pF) | E1 | 10000 | 7.266e-05 | 127.8 |
| outer segment, 8 mm lead (C_c 0.0137 pF, C_g 0.581 pF) | E1 | 0 | 1.222 | 0 |
| outer segment, 8 mm lead (C_c 0.0137 pF, C_g 0.581 pF) | E1 | 100 | 0.007224 | 127.1 |
| outer segment, 8 mm lead (C_c 0.0137 pF, C_g 0.581 pF) | E1 | 1000 | 0.0007262 | 127.8 |
| outer segment, 8 mm lead (C_c 0.0137 pF, C_g 0.581 pF) | E1 | 10000 | 7.266e-05 | 127.8 |

## RF null shift (gds2itvg, A30 layout) [team calc]

Electrodes used: centre 2; outer segments nearest the ion (by unit potential) at readout: top 12, bottom 27; at loading: top 8, bottom 23.

| Zone | Au | C_f (pF) | centre DC shift (nm) | top segment, 5 mm lead (nm) | top + bottom, 5 mm (nm) | top + bottom, 8 mm (nm) |
|---|---|---|---|---|---|---|
| readout | E2 | 0 | 2758 | 180.4 | 249.1 | 173.8 |
| readout | E2 | 100 | 96.35 | 0.7474 | 1.032 | 1.03 |
| readout | E2 | 1000 | 9.948 | 0.07502 | 0.1036 | 0.1035 |
| readout | E2 | 10000 | 0.9981 | 0.007505 | 0.01036 | 0.01036 |
| readout | E1 | 0 | 2284 | 166 | 229.1 | 159.8 |
| readout | E1 | 100 | 76.61 | 0.6856 | 0.9464 | 0.9447 |
| readout | E1 | 1000 | 7.899 | 0.06881 | 0.09499 | 0.09497 |
| readout | E1 | 10000 | 0.7924 | 0.006884 | 0.009502 | 0.009502 |
| loading | E2 | 0 | 2091 | 180.4 | 249.1 | 173.8 |
| loading | E2 | 100 | 73.05 | 0.7473 | 1.032 | 1.03 |
| loading | E2 | 1000 | 7.542 | 0.07501 | 0.1035 | 0.1035 |
| loading | E2 | 10000 | 0.7566 | 0.007504 | 0.01036 | 0.01036 |
| loading | E1 | 0 | 1731 | 166 | 229.1 | 159.8 |
| loading | E1 | 100 | 58.07 | 0.6855 | 0.9462 | 0.9445 |
| loading | E1 | 1000 | 5.988 | 0.0688 | 0.09498 | 0.09496 |
| loading | E1 | 10000 | 0.6007 | 0.006883 | 0.009501 | 0.009501 |

Limits: 2-D capacitance, ideal conductors, no segment ends, no lead tracks near the rails; bond wire and lead inductance ignored; C_g for the outer segment is the pad note's estimate (10 um SiO2 over buried Al), not a value for this stack.
