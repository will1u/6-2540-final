> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

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
SNSPD_G ─ bond ─ ground (or a matched 50 Ω for symmetric termination, see below)
```

| Element | Choice | Reason / source |
|---|---|---|
| Notch | ≥ 40 dB at 28 MHz | Todaro: 7th-order Bessel notch, 40 dB at f_rf, 14 MHz 3 dB bandwidth, because RF pickup was "several times larger" than the ~250 µV pulses (Supp. Fig. S2) |
| Low-pass | Todaro used a 25 MHz Gaussian LPF, which gave 18 dB more at **67 MHz**. **At our 28 MHz a 25 MHz LPF adds almost nothing.** Use a lower corner (~10–15 MHz) and/or a steeper notch [inference] | Our pulses are slow (τ ≈ 60–190 ns), so a ~10 MHz bandwidth keeps the rising edge (~30 ns) [inference] |
| Gain | ~46 dB [verify]: 1 mV pulses become ~200 mV at the comparator | – |
| Comparator threshold | ~50 % of the mean pulse height; tune on the b4 pulse-height histogram | Pulse heights vary up to 3× with RF-modulated bias (Todaro Supp.) |
| Termination | Consider symmetric (both leads into 50 Ω) to cancel the uniform induced current I₀ | Todaro Supp. Fig. S4 remedies; Slichter App. A |
| Bias gate | Bias on only during readout. Bias off during loading, photoionisation and Raman / sideband work | Todaro thesis Sec. 6.3.1; PRL p. 4 (stray-light clicks blocked sideband cooling over the detector) |

**ARTIQ:** the comparator output goes to a TTL input. Count in the readout gate and also time-tag the edges: the same timestamps give RF-photon correlation for micromotion (section d).

Filter corner and termination remain choices. Resolve them using [cold RF-on/off measurements](02_CRYOGENIC.md), then record selected settings.
