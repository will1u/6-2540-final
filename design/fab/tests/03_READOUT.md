> **Claude-authored.** Rewritten for v4 2026-11-09.

# Detector readout electronics

[Test plan](../test_plan.md) · [Fab overview](../README.md) · [Open decisions](../OPEN_DECISIONS.md)

The structure follows Todaro Supp. Fig. S2 (Fig. S3 [verify which figure shows the full chain]).

```
SNSPD_S ─ on-chip lead ─ bond ─ cryo coax ─┬─ bias tee ─ RF port ─ amplifiers (~46 dB total [verify gain in Todaro Supp. Fig. S2/S3])
                                           │                     ─ notch at f_rf = 28 MHz (≥ 40 dB)
                                           │                     ─ low-pass
                                           │                     ─ comparator ─ LVTTL ─ ARTIQ TTL input (edge counter / timestamps)
                                           └─ DC port ─ series R (Hampel: 10 kΩ) ─ isolated low-noise voltage source,
                                                         gated by ARTIQ (DAC or switch, ~10 µs ramps)
SNSPD_G ─ bond ─ ground, or the termination chosen in the RF row below (open)
```

| Element | Choice | Reason / source |
|---|---|---|
| Notch | ≥ 40 dB at 28 MHz | Todaro: 7th-order Bessel notch, 40 dB at f_rf, 14 MHz 3 dB bandwidth, because RF pickup was "several times larger" than the ~250 µV pulses (Supp. Fig. S2) |
| Low-pass | Todaro used a 25 MHz Gaussian LPF, which gave 18 dB more at **67 MHz**. **At our 28 MHz a 25 MHz LPF adds almost nothing.** Use a lower corner (~10–15 MHz) and/or a steeper notch [inference] | Our pulses are slow (τ ≈ 60–190 ns), so a ~10 MHz bandwidth keeps the rising edge (~30 ns) [inference] |
| Gain | ~46 dB [verify]: 1 mV pulses become ~200 mV at the comparator | – |
| Comparator threshold | ~50 % of the mean pulse height; tune on the b4 pulse-height histogram | Pulse heights vary up to 3× with RF-modulated bias (Todaro Supp.) |
| RF grounding / termination | **Open** ([OPEN_DECISIONS](../OPEN_DECISIONS.md), RF grounding / filters). Options listed there: centre-DC filtering, carrier grounds, symmetric detector termination or cancellation, and for v4 an RF bypass at both SNS and SNG pads | Each v4 slot lead collects ≈ 44.5 µA (E2) / 28.3 µA (E1) of common-mode 28 MHz current over its 2.24 mm length (sim 18 / step 28). With a plain 50 Ω line on the signal lead and the return grounded, the lumped model (sim 19, upper bound) gives ≈ 4.1 µA (E2) / 2.6 µA (E1) through the A30 nanowire. Todaro Supp. Fig. S4 and Slichter App. A describe symmetric termination. Sim 19 also runs filter cases (`summary.json`); they are model cases, not a choice |
| Bias gate | Bias on only during readout. Bias off during loading, photoionisation and Raman / sideband work | Todaro thesis Sec. 6.3.1; PRL p. 4 (stray-light clicks blocked sideband cooling over the detector) |

**ARTIQ:** the comparator output goes to a TTL input. Count in the readout gate and also time-tag the edges: the same timestamps give RF-photon correlation for micromotion ([first trapping, step 9](04_TRAPPING.md)).

The filter corner and the termination are not chosen. Resolve them with the [cold RF-on/off measurements](02_CRYOGENIC.md) (b6), then record the selected settings and the carrier used.
