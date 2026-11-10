> **Claude-authored.** Reading pointers for Chiaverini et al. 2005: a five-wire surface trap, unequal RF widths, rotated radial axes. These are pointers only. The Sec. 4 items were checked against the arXiv PDF on 2026-11-10 (journal pp. 425–427). Items still marked [verify] were not checked.

# Chiaverini et al. 2005, surface-electrode architecture

**Citation.** J. Chiaverini, R. B. Blakestad, J. Britton, J. D. Jost, C. Langer, D. Leibfried, R. Ozeri, D. J. Wineland, "Surface-electrode architecture for ion-trap quantum information processing", Quant. Inf. Comput. 5, 419 (2005); arXiv:quant-ph/0501147. The journal page numbers come from the PDF page headers.

**Link.** https://arxiv.org/abs/quant-ph/0501147

**Status.** PDF pp. 7–12 (journal pp. 425–430) were read. This settles the earlier conflict: the sibling note `../Radial tilt 2026-11/chiaverini_2005_quant-ph0501147.md` read only pp. 419–421, which comes before Sec. 4.

## Where to read

- **Sec. 4, journal p. 426, the paragraph after Fig. 5 (checked):**
  - In a linear trap the RF pseudopotential is nearly cylindrically symmetric near the centre. The **static** potential therefore sets the two radial principal axes.
  - The symmetric five-wire layout gives axes parallel and perpendicular to the substrate (Fig. 5a).
  - Widen one RF electrode by half its width and narrow the other by the same amount, and the axes rotate by **30°** (Fig. 5b).
  - The four-wire layout gives axes near ±45° over a wide range of electrode potentials (Fig. 5c).
- **Fig. 6, journal p. 427 (checked):** three layouts that split the centre control electrode into several electrodes, including one split lengthwise. They are proposed there for ion separation, not for tilt.
- **Fig. 4, journal p. 425 (checked):** pseudopotential contours of four geometries, with relative frequencies and depths in the caption.
- **Sec. 5, journal p. 428 (checked):** the static potential is usually trapping along one radial axis and anti-trapping along the other. Changing the axis angles and the control voltages can deepen the trap by about a factor of 2.

## Per-source numbers

| Item | Value | Status |
|---|---|---|
| Tilt reached | 30° (five-wire, RF widths ×1.5 and ×0.5); about ±45° (four-wire) | Checked, p. 426 |
| What does it | The static (DC) potential, once the RF layout is asymmetric. The paper says the angles hold for a large range of control voltages (relative to the RF amplitude) | Checked, p. 426 |
| Voltages | Not given for the tilt | Checked |
| Ion height, frequencies | About 50 µm; secular frequencies around 10 MHz for 100 V RF at 100 MHz, for the Fig. 7 chip (Sec. 6, p. 429) | Read on p. 429 |

## Relevance to this design [inference]

- The RF-width ratio in Fig. 5b corresponds to δ = 0.5 in variant G3 of sim 27 (a_top = 1.5a, a_bot = 0.5a).
- The paper gives the angle only, with no voltage, frequency split or depth cost; sims 27 and 28 compute those for our trap.
