> **Claude-authored.** Specification note for the lab's DC DAC, the Sinara Zotino, 2026-11-10. The team named the hardware ("we have a Zotino"); the numbers below are from the pages listed, read through a web fetch. The AD5372 datasheet did not load, so nothing below comes from it.

# T4: Sinara Zotino, the DC DAC

**Sources read:**
- [Zotino wiki, Home](https://github.com/sinara-hw/Zotino/wiki) (page shows "edited Jul 6, 2021"; it may lag the current hardware revision);
- [M-Labs Sinara core page](https://m-labs.hk/experiment-control/sinara-core/);
- [ARTIQ core drivers reference](https://m-labs.hk/artiq/manual/core_drivers_reference.html), `artiq.coredevice.zotino` and `artiq.coredevice.ad53xx`.

**Not read:**
- the AD5372 datasheet (timed out);
- the Zotino 5432 datasheet (M-Labs `/docs/sinara-datasheets/5432.pdf`);
- the [HV amplifier wiki](https://github.com/sinara-hw/HVAMP_32/wiki).

## Specification

| Item | Value | Where |
|---|---|---|
| Channels | 32 | Wiki Overview, "Channel count: 32"; M-Labs; ARTIQ `Zotino` docstring |
| Output range | ±10 V | Wiki Overview, "Output voltage: ±10V". ARTIQ `ad53xx.voltage_to_mu` gives the valid range as [−2·vref, +2·vref − 1 LSB] + offset, with the Zotino default vref = 5 V |
| Resolution | 16 bit; one step ≈ 0.31 mV over 20 V [team calc] | Wiki Overview; M-Labs; ARTIQ |
| DAC chip | AD5372BCPZ | Wiki Overview |
| Update rate | 1 MSPS **in total**, "divided arbitrarily between the channels" | Wiki Overview; M-Labs ("divided between channels") |
| Per-channel or full-update time | Not stated. The SPI clock runs at up to 50 MHz (ARTIQ `div_write` default). `load()` notes a busy period of at most 1.5 µs after writing | ARTIQ `zotino` / `ad53xx` docstrings |
| Output filter | 3rd-order Butterworth, 75 kHz cut-off | Wiki Overview, "Analogue bandwidth" |
| Output impedance | 470 Ω in parallel with 2.2 nF | Wiki Overview |
| Slew rate | Not given (the wiki shows "?V/s") | Wiki Overview |
| Output noise | Not published (the wiki's measurement section says work in progress) | Wiki, Measurements |
| Drift | Op-amp self-heating up to about 25 °C, about 4 ppm at 0.2 ppm/°C; M-Labs suggests the Sinara 8451 Thermostat | Wiki; M-Labs |
| Higher voltage | Sinara 5633 HV Amplifier: 32 channels, 5× gain, up to ±50 V, a mezzanine for Zotino and Fastino; 12 MHz/gain bandwidth, 21 V/µs slew rate [verify: M-Labs page only] | M-Labs Sinara core page |

## What it means for this design [team calc / inference]

- **Channel count.** The v4 trap dies have 35 DC electrodes: 2 (centre DC), 3–32 (segments) and 33–36 (end caps), per `gds/trap_die_v4_*_pads.csv`. One Zotino has 32 channels. Either use a second Zotino, or ground or tie electrodes at the carrier. Sim 26 tests which reductions work (DESIGN_LOG step 46).
- **±10 V is a real limit.** It is the limit sims 12, 13, 21 and 25 already use. A 45° radial tilt at 0.8 MHz axial needs 11–15 V at most zones (sim 25, DESIGN_LOG step 45); the HV amplifier would allow it, at 5× the DAC noise and step size.
- **Update rate per channel.** The 1 MSPS is shared. If all 35 channels change on every update, a full update takes at least 35 µs (at most about 28.6 kHz, before any SPI or RTIO overhead [verify]). Sim 21 assumed 1 MHz updates on every channel and a first-order filter, so its transport numbers do not describe this hardware until it is rerun with the Zotino rate and the 75 kHz 3rd-order filter. Note that 0.8 MHz / 28.57 kHz = 28 exactly: the naive full-update rate is a sub-multiple of the axial frequency, the case DESIGN_LOG step 40 says to avoid. The real rate depends on the SPI timing, which is not stated.
- **On-board filter.** The 75 kHz Butterworth sits before any filter the team adds at the feedthrough or carrier. Its attenuation at the 0.8 MHz axial frequency is about (75/800)³ ≈ 8 × 10⁻⁴ in amplitude for an ideal 3rd-order response [team calc].
