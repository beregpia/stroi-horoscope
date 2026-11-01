#!/usr/bin/env python3
"""Карточки чистки вокала: RX, De-breath, Pro-DS, soothe2, EQ-свип."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
FS = 48000.0
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


# 1. RX De-noise
knob_card("clean-rx-denoise.png",
          "iZotope RX — Spectral De-noise (ОФЛАЙН-рендером!)",
          "1) Выделить участок тишины → LEARN  2) Reduction 6–12 dB  3) Render",
          [("REDUCTION", "6–12 dB", 0.35), ("SMOOTHING", "2–3", 0.3),
           ("QUALITY", "Best", 0.9)],
          buttons=[("LEARN", True), ("ADAPTIVE", False)],
          meter=">12 dB = 'водянистые' артефакты!", accent="#50a0b4")

# 2. RX Mouth De-click
knob_card("clean-rx-declick.png",
          "iZotope RX — Mouth De-click (щелчки губ)",
          "Волшебная кнопка от 'смачных ртов' · после — прослушать A/B целиком",
          [("SENSITIVITY", "3–5", 0.4), ("FREQ SKEW", "0", 0.5),
           ("CLICK WIDTH", "по умолч.", 0.5)],
          meter="Слишком высокая Sens = съест согласные", accent="#50a0b4")

# 3. De-breath
knob_card("clean-debreath.png",
          "RX Breath Control / Waves DeBreath",
          "Вдохи ПРИБРАТЬ, не удалить — вокал без дыханий мёртв!",
          [("TARGET", "−10…−15 dB", 0.35), ("SENSITIVITY", "средняя", 0.5)],
          buttons=[("GAIN", True), ("MUTE", False)],
          meter="НЕ в ноль! −10 dB = идеал", accent="#c05840")

# 4. Pro-DS
knob_card("clean-prods.png",
          "FabFilter Pro-DS — де-эссер",
          "Режим Single Vocal · ловит только 'с/ц/ч', не трогая тон",
          [("THRESHOLD", "GR 2–4 dB", 0.4), ("RANGE", "4–6 dB", 0.35),
           ("HP FREQ", "5 kHz", 0.45), ("LP FREQ", "9 kHz", 0.6)],
          buttons=[("SINGLE", True), ("ALLROUND", False), ("WIDE", True)],
          meter="GR только на свистящих", accent="#e0a050")

# 5. soothe2
knob_card("clean-soothe2.png",
          "oeksound soothe2 — резонансы динамически",
          "Гнусавость ~1k · жёсткость ~3k · звон комнаты — ест только когда вылезает",
          [("DEPTH", "4–6", 0.5), ("SHARPNESS", "7", 0.7),
           ("SELECTIVITY", "7–8", 0.75), ("SPEED", "Fast", 0.7),
           ("ZONE", "1–8 kHz", 0.5)],
          buttons=[("DELTA", True)],
          meter="Delta: слушаем ЧТО ест — только противное!", accent="#8c6a4a")

# 6. EQ-свип — картинка-схема
fig, ax = plt.subplots(figsize=(9.6, 4.2), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)


def bell(f0, g, q):
    return g / (1 + ((np.log2(F / f0)) * q * 1.4) ** 2)


# свип-колокол
sweep = bell(300, 10, 5)
ax.plot(F, sweep, color="#e05555", lw=2.2, ls="--", zorder=4)
ax.annotate("1. Свип: узкий Q 4–6, +10 dB —\nведём по 150–500 Hz, ищем 'загудело'",
            (300, 10.5), ha="center", fontsize=9, color="#e08585")
# вырезы
cuts = bell(200, -4, 3) + bell(450, -3.5, 3) + bell(1000, -3, 3) + bell(3000, -3, 3)
ax.plot(F, cuts, color=CURVE, lw=2.6, zorder=5)
ax.fill_between(F, 0, cuts, where=cuts < 0, color=FILL_N, zorder=2)
for fr, g, lab in [(200, -4, "200\nбубнит"), (450, -3.5, "400–500\nкоробка"),
                   (1000, -3, "1k\nгнусаво"), (3000, -3, "2.5–3.5k\nжёстко")]:
    ax.scatter([fr], [g], s=80, zorder=6, color=BG, edgecolors="white", linewidths=2)
    ax.annotate(lab, (fr, g - 1.2), ha="center", va="top", fontsize=8.4, color=TXT)
ax.axhline(0, color="#5a5248", lw=1)
ax.set_xscale("log"); ax.set_xlim(50, 10000); ax.set_ylim(-10, 13)
ticks = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
ax.set_xticks(ticks)
ax.set_xticklabels(["50", "100", "200", "500", "1k", "2k", "5k", "10k"], fontsize=8.5)
ax.grid(True, which="both", color=GRID, lw=0.6, alpha=0.8)
ax.set_ylabel("dB", fontsize=9)
ax.set_title("EQ-ХИРУРГИЯ — Pro-Q 4: свип-поиск бяк и адреса вырезов",
             fontsize=13, fontweight="bold", loc="left", color=TXT, pad=14)
ax.text(0, 1.02, "2. Нашли → вырез −3…−5 dB, Q 2–3 (не шире! широкие вырезы = тонкий голос)",
        transform=ax.transAxes, fontsize=9, color=SUB)
for s in ax.spines.values():
    s.set_color(GRID)
fig.tight_layout(); fig.savefig(f"{OUT}/clean-eq-sweep.png", facecolor=BG); plt.close(fig)
print("clean-eq-sweep.png")

print("ALL DONE")
