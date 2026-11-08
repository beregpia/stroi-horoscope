#!/usr/bin/env python3
"""Карточки чистки барабанных каналов: гейты, свипы, de-room."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
F = np.logspace(np.log10(20), np.log10(20000), 2000)

BG = "#201c18"; GRID = "#35302a"; TXT = "#f2ede4"; SUB = "#a89d8c"
CURVE = "#e0a050"; FILL_N = "#50a0b433"

plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TXT,
    "axes.edgecolor": GRID, "axes.labelcolor": SUB,
    "xtick.color": SUB, "ytick.color": SUB})


def knob_card(fname, title, subtitle, knobs, buttons=None, meter=None, accent="#e0a050"):
    n = len(knobs); wfig = max(7.2, 1.75 * n + 0.8)
    fig = plt.figure(figsize=(wfig, 3.1), dpi=150)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, wfig); ax.set_ylim(0, 3.1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.12, 0.12), wfig - 0.24, 2.86,
                 boxstyle="round,pad=0.02,rounding_size=0.12", fc="#2a251f", ec=accent, lw=2))
    ax.text(0.4, 2.62, title, fontsize=13, fontweight="bold", color=TXT)
    ax.text(0.4, 2.32, subtitle, fontsize=9, color=SUB)
    x0 = 1.1; step = (wfig - 1.6) / max(n - 1, 1) if n > 1 else 0
    for i, (lab, val, frac) in enumerate(knobs):
        cx = x0 + i * step; cy = 1.35; r = 0.42
        ax.add_patch(Circle((cx, cy), r, fc="#352f27", ec="#5a5248", lw=2))
        ang = np.deg2rad(225 - 270 * frac)
        ax.plot([cx, cx + r * 0.72 * np.cos(ang)], [cy, cy + r * 0.72 * np.sin(ang)],
                color=accent, lw=3, solid_capstyle="round")
        ax.add_patch(Circle((cx, cy), 0.055, fc=accent, ec="none"))
        ax.text(cx, cy - r - 0.16, lab, ha="center", fontsize=8.6, color=SUB)
        ax.text(cx, cy - r - 0.42, val, ha="center", fontsize=9.4, color=TXT, fontweight="bold")
    if buttons:
        bx = wfig - 0.5 - 0.62 * len(buttons)
        for j, (blab, on) in enumerate(buttons):
            fc = accent if on else "#352f27"; tc = "#111" if on else SUB
            ax.add_patch(FancyBboxPatch((bx + j * 0.62, 2.28), 0.52, 0.34,
                         boxstyle="round,pad=0.01,rounding_size=0.06", fc=fc, ec="#5a5248", lw=1))
            ax.text(bx + j * 0.62 + 0.26, 2.45, blab, ha="center", va="center",
                    fontsize=7.6, color=tc, fontweight="bold")
    if meter:
        ax.text(wfig - 0.45, 0.35, meter, ha="right", fontsize=9.2, color="#e0a050", fontweight="bold")
    fig.savefig(f"{OUT}/{fname}", facecolor=BG); plt.close(fig)
    print(fname)


def bell(f0, g, q):
    return g / (1 + ((np.log2(F / f0)) * q * 1.4) ** 2)


def sweep_plot(fname, title, subtitle, sweep_f, sweep_label, cuts, xlim=(30, 10000),
               hpf_note=None):
    fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=150)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    sw = bell(sweep_f, 10, 5)
    ax.plot(F, sw, color="#e05555", lw=2.2, ls="--", zorder=4)
    ax.annotate(sweep_label, (sweep_f, 10.5), ha="center", fontsize=9, color="#e08585")
    total = np.zeros_like(F)
    for f0, g, q in cuts:
        total += bell(f0, g, q)
    ax.plot(F, total, color=CURVE, lw=2.6, zorder=5)
    ax.fill_between(F, 0, total, where=total < 0, color=FILL_N, zorder=2)
    for f0, g, q in cuts:
        ax.scatter([f0], [g], s=80, zorder=6, color=BG, edgecolors="white", linewidths=2)
    ax.axhline(0, color="#5a5248", lw=1)
    ax.set_xscale("log"); ax.set_xlim(*xlim); ax.set_ylim(-10, 13)
    tick_all = [30, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    tl = {30: "30", 50: "50", 100: "100", 200: "200", 500: "500",
          1000: "1k", 2000: "2k", 5000: "5k", 10000: "10k"}
    ticks = [t for t in tick_all if xlim[0] <= t <= xlim[1]]
    ax.set_xticks(ticks); ax.set_xticklabels([tl[t] for t in ticks], fontsize=8.5)
    ax.grid(True, which="both", color=GRID, lw=0.6, alpha=0.8)
    ax.set_ylabel("dB", fontsize=9)
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left", color=TXT, pad=14)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color=SUB)
    if hpf_note:
        ax.annotate(hpf_note[1], (hpf_note[0], -8), ha="center", fontsize=8.6, color=TXT)
    for s in ax.spines.values():
        s.set_color(GRID)
    fig.tight_layout(); fig.savefig(f"{OUT}/{fname}", facecolor=BG); plt.close(fig)
    print(fname)


# 1. Гейт бочки
knob_card("dclean-kick-gate.png",
          "KICK BEATER — Pro-G / Gate (bleed рабочего и хэта)",
          "SC-фильтр на 50–100 Hz: гейт слышит только 'бум' бочки, не рабочего!",
          [("THRESHOLD", "~−32 dB", 0.4), ("ATTACK", "0.02 ms", 0.03),
           ("HOLD", "100 ms", 0.35), ("RELEASE", "200 ms", 0.4),
           ("RANGE", "−15 dB (НЕ −inf!)", 0.5)],
          buttons=[("PUNCH", True), ("SC", True)],
          meter="Прибрать bleed, а не стереть", accent="#50a0b4")

# 2. Свип бочки
sweep_plot("dclean-kick-sweep.png",
           "KICK — свип-чистка: гул ноты и картон",
           "HPF 30 Hz уже стоит · ищем ГУЛ (60–120) и КАРТОН (250–500) — у каждой бочки свои адреса",
           90, "свип 60–120 Hz:\nнота гула бочки",
           [(90, -3.5, 3.5), (380, -4.5, 2.5)],
           xlim=(30, 5000))

# 3. Звон рабочего
sweep_plot("dclean-snare-ring.png",
           "SNARE — свип-чистка: кольцо (ring)",
           "Свип 400–900 Hz → нота кольца → вырез −4…−6 dB Q 4–6 · звенит только на громких? → динамический!",
           650, "свип 400–900 Hz:\nнота кольца",
           [(650, -5, 5)],
           xlim=(100, 10000))

# 4. Гейт пружины (bottom)
knob_card("dclean-snare-btm-gate.png",
          "SNARE BOTTOM — Gate (дребезг пружины)",
          "Пружина отвечает 'дзззз' на бас и гитары — закрываем между ударами",
          [("THRESHOLD", "под удар", 0.45), ("ATTACK", "0.05 ms", 0.05),
           ("HOLD", "60 ms", 0.25), ("RELEASE", "150 ms", 0.3),
           ("RANGE", "−10 dB", 0.6)],
          meter="Мягко: −10 dB, не глухой мьют", accent="#50a0b4")

# 5. Томы: гейт + кроссфейды
knob_card("dclean-toms-gate.png",
          "TOMS — Gate / Strip Silence (гул между филлами)",
          "Вариант А: гейт мягкий · Вариант Б: Strip Silence руками + КРОССФЕЙДЫ 10–20 ms",
          [("THRESHOLD", "под удар", 0.45), ("HOLD", "180 ms", 0.4),
           ("RELEASE", "300 ms", 0.45), ("RANGE", "−12 dB", 0.55)],
          buttons=[("A: GATE", True), ("Б: STRIP", False)],
          meter="+ вырез симпат. гула: свип 80–200 Hz", accent="#50a0b4")

# 6. De-room / шумодав
knob_card("dclean-deroom.png",
          "DE-ROOM — Zynaptiq UNVEIL / Accentize DeRoom Pro",
          "Нейро-удаление комнаты из ЗАКРЫТЫХ каналов (kick/snare/toms) · НЕ трогать OH/Room!",
          [("REDUCTION", "3–6 dB", 0.3), ("FOCUS", "по центру", 0.5),
           ("OUTPUT", "по уровню", 0.5)],
          buttons=[("DIFF", True)],
          meter="Больше 6 dB = пластик! A/B постоянно", accent="#c05840")

print("ALL DONE")
