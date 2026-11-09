#!/usr/bin/env python3
"""Картинки для groove-mix-session: гитары, клавиши, синты, ковбелл,
сайдчейн, MIX BUS. Тот же тёплый стиль, что в bfd3-groove."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

FS = 48000.0
F = np.logspace(np.log10(20), np.log10(20000), 2000)

BG = "#201c18"
GRID = "#35302a"
TXT = "#f2ede4"
SUB = "#a89d8c"
CURVE = "#e0a050"
FILL_P = "#e0a05033"
FILL_N = "#50a0b433"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TXT, "axes.edgecolor": GRID,
    "axes.labelcolor": SUB, "xtick.color": SUB, "ytick.color": SUB,
})


def biquad(b, a):
    w = 2 * np.pi * F / FS
    z = np.exp(-1j * w)
    h = (b[0] + b[1] * z + b[2] * z**2) / (a[0] + a[1] * z + a[2] * z**2)
    return 20 * np.log10(np.maximum(np.abs(h), 1e-9))


def peak(f0, g, q):
    A = 10 ** (g / 40)
    w0 = 2 * np.pi * f0 / FS
    al = np.sin(w0) / (2 * q)
    return biquad([1 + al * A, -2 * np.cos(w0), 1 - al * A],
                  [1 + al / A, -2 * np.cos(w0), 1 - al / A])


def shelf(f0, g, high=True, s=0.9):
    A = 10 ** (g / 40)
    w0 = 2 * np.pi * f0 / FS
    al = np.sin(w0) / 2 * np.sqrt((A + 1 / A) * (1 / s - 1) + 2)
    cos = np.cos(w0)
    sq = 2 * np.sqrt(A) * al
    if high:
        b = [A * ((A + 1) + (A - 1) * cos + sq), -2 * A * ((A - 1) + (A + 1) * cos),
             A * ((A + 1) + (A - 1) * cos - sq)]
        a = [(A + 1) - (A - 1) * cos + sq, 2 * ((A - 1) - (A + 1) * cos),
             (A + 1) - (A - 1) * cos - sq]
    else:
        b = [A * ((A + 1) - (A - 1) * cos + sq), 2 * A * ((A - 1) - (A + 1) * cos),
             A * ((A + 1) - (A - 1) * cos - sq)]
        a = [(A + 1) + (A - 1) * cos + sq, -2 * ((A - 1) + (A + 1) * cos),
             (A + 1) + (A - 1) * cos - sq]
    return biquad(b, a)


def bhp(f0, order=4):
    t = np.zeros_like(F)
    for k in range(order // 2):
        q = 1 / (2 * np.sin(np.pi * (2 * k + 1) / (2 * order)))
        w0 = 2 * np.pi * f0 / FS
        al = np.sin(w0) / (2 * q)
        c = np.cos(w0)
        t += biquad([(1 + c) / 2, -(1 + c), (1 + c) / 2], [1 + al, -2 * c, 1 - al])
    return t


def blp(f0, order=2):
    t = np.zeros_like(F)
    for k in range(order // 2):
        q = 1 / (2 * np.sin(np.pi * (2 * k + 1) / (2 * order)))
        w0 = 2 * np.pi * f0 / FS
        al = np.sin(w0) / (2 * q)
        c = np.cos(w0)
        t += biquad([(1 - c) / 2, 1 - c, (1 - c) / 2], [1 + al, -2 * c, 1 - al])
    return t


def eq_plot(fname, title, subtitle, bands, dots, ymin=-18, ymax=12):
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    total = np.sum(bands, axis=0)
    ax.fill_between(F, 0, total, where=total >= 0, color=FILL_P, zorder=2)
    ax.fill_between(F, 0, total, where=total < 0, color=FILL_N, zorder=2)
    ax.plot(F, total, color=CURVE, lw=2.6, zorder=4)
    ax.axhline(0, color="#5a5248", lw=1)
    for fr, g, lab, dyn in dots:
        ec = "#e05555" if dyn else "white"
        ax.scatter([fr], [g], s=90, zorder=6, color=BG, edgecolors=ec, linewidths=2.2)
        va = "bottom" if g >= 0 else "top"
        off = 1.1 if g >= 0 else -1.1
        ax.annotate(lab, (fr, g + off), ha="center", va=va, fontsize=8.6,
                    color=("#e08585" if dyn else TXT), zorder=7)
    ax.set_xscale("log")
    ax.set_xlim(20, 20000)
    ax.set_ylim(ymin, ymax)
    ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"],
                       fontsize=8.5)
    ax.grid(True, which="both", color=GRID, lw=0.6, alpha=0.8)
    ax.tick_params(labelsize=8.5)
    ax.set_ylabel("dB", fontsize=9)
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left", color=TXT, pad=14)
    ax.text(0.0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color=SUB)
    for s in ax.spines.values():
        s.set_color(GRID)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{fname}", facecolor=BG)
    plt.close(fig)
    print(fname)


def knob_card(fname, title, subtitle, knobs, buttons=None, meter=None, accent="#e0a050"):
    n = len(knobs)
    wfig = max(7.2, 1.75 * n + 0.8)
    fig = plt.figure(figsize=(wfig, 3.1), dpi=150)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, wfig)
    ax.set_ylim(0, 3.1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.12, 0.12), wfig - 0.24, 2.86,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="#2a251f", ec=accent, lw=2))
    ax.text(0.4, 2.62, title, fontsize=13, fontweight="bold", color=TXT)
    ax.text(0.4, 2.32, subtitle, fontsize=9, color=SUB)
    x0 = 1.1
    step = (wfig - 1.6) / max(n - 1, 1) if n > 1 else 0
    for i, (lab, val, frac) in enumerate(knobs):
        cx = x0 + i * step
        cy = 1.35
        r = 0.42
        ax.add_patch(Circle((cx, cy), r, fc="#352f27", ec="#5a5248", lw=2))
        ang = np.deg2rad(225 - 270 * frac)
        ax.plot([cx, cx + r * 0.72 * np.cos(ang)], [cy, cy + r * 0.72 * np.sin(ang)],
                color=accent, lw=3, solid_capstyle="round")
        ax.add_patch(Circle((cx, cy), 0.055, fc=accent, ec="none"))
        ax.text(cx, cy - r - 0.16, lab, ha="center", fontsize=8.6, color=SUB)
        ax.text(cx, cy - r - 0.42, val, ha="center", fontsize=9.4, color=TXT,
                fontweight="bold")
    if buttons:
        bx = wfig - 0.5 - 0.62 * len(buttons)
        for j, (blab, on) in enumerate(buttons):
            fc = accent if on else "#352f27"
            tc = "#111" if on else SUB
            ax.add_patch(FancyBboxPatch((bx + j * 0.62, 2.28), 0.52, 0.34,
                                        boxstyle="round,pad=0.01,rounding_size=0.06",
                                        fc=fc, ec="#5a5248", lw=1))
            ax.text(bx + j * 0.62 + 0.26, 2.45, blab, ha="center", va="center",
                    fontsize=7.6, color=tc, fontweight="bold")
    if meter:
        ax.text(wfig - 0.45, 0.35, meter, ha="right", fontsize=9.2, color="#e0a050",
                fontweight="bold")
    fig.savefig(f"{OUT}/{fname}", facecolor=BG)
    plt.close(fig)
    print(fname)


# ===================== EQ =====================

# Ковбелл
eq_plot("eq-cowbell.png",
        "COWBELL — Pro-Q 4 / Frequency",
        "HPF 300 Hz 24/oct · −3 dB @ 650 Hz Q 2 (звон, если лезет) · LPF 8 kHz",
        [bhp(300, 4), peak(650, -3, 2.0), blp(8000, 2)],
        [(300, -3, "HPF 300", False), (650, -3, "−3 dB · звон", False),
         (8000, -3, "LPF 8k", False)])

# Гитары
eq_plot("eq-guitar.png",
        "GUITAR (каждая из Guit 1/2/3) — Pro-Q 4",
        "HPF 95 Hz · −2.5 dB @ 300 Hz Q 1.2 (мутность) · +1.5 dB @ 2.5 kHz Q 1.1 · LPF 11k (винтаж)",
        [bhp(95, 4), peak(300, -2.5, 1.2), peak(2500, 1.5, 1.1), blp(11000, 2)],
        [(95, -3, "HPF 95", False), (300, -2.5, "−2.5 dB", False),
         (2500, 1.5, "+1.5 dB", False), (11000, -3, "LPF 11k", False)])

# Клавиши
eq_plot("eq-keys.png",
        "KEYS — Pro-Q 4",
        "HPF 100 Hz · −2 dB @ 250 Hz Q 1.2 (место рабочему!) · −1.5 dB @ 3 kHz если спорит с гитарами",
        [bhp(100, 4), peak(250, -2, 1.2), peak(3000, -1.5, 1.4)],
        [(100, -3, "HPF 100", False), (250, -2, "−2 dB", False),
         (3000, -1.5, "−1.5 dB", False)])

# Синты
eq_plot("eq-synth.png",
        "SYNTH (Serum / Spire) — Pro-Q 4",
        "HPF 130 Hz 24/oct (низ — бочке и басу!) · −2 dB @ 400 Hz · shelf −2 dB @ 10 kHz (не спорить с OH)",
        [bhp(130, 4), peak(400, -2, 1.2), shelf(10000, -2, True)],
        [(130, -3, "HPF 130", False), (400, -2, "−2 dB", False),
         (10000, -2, "shelf −2", False)])

# MIX BUS
eq_plot("eq-mixbus.png",
        "MIX BUS — Pro-Q 4 (финальный тон всего микса)",
        "shelf +1 dB @ 80 Hz · shelf −1 dB @ 13 kHz — совсем чуть-чуть, винтажный наклон",
        [shelf(80, 1.0, False), shelf(13000, -1.0, True)],
        [(80, 1.0, "shelf +1", False), (13000, -1.0, "shelf −1", False)],
        ymin=-6, ymax=6)

# ===================== Ручки =====================

# Гитарный комп
knob_card("comp-guitar.png",
          "GTR GROUP — LA-2A или Pro-C 2 (стиль Vocal)",
          "Едва касаемся: гитары в печати уже сжаты при записи",
          [("RATIO", "2:1", 0.25), ("ATTACK", "30 ms", 0.6),
           ("RELEASE", "Auto", 1.0), ("THRESH", "GR 2–3 dB", 0.35),
           ("MAKEUP", "по уровню", 0.4)],
          meter="GR: −2…−3 dB")

# Сайдчейн синтов
knob_card("comp-sidechain.png",
          "SYNTH GROUP — Pro-C 2 / Compressor (SIDECHAIN от Kick!)",
          "Вход сайдчейна: канал Kick front · синты 'приседают' под бочку — это грув",
          [("RATIO", "2:1", 0.25), ("ATTACK", "5 ms", 0.12),
           ("RELEASE", "120 ms", 0.4), ("THRESH", "GR 1–2 dB", 0.3),
           ("MIX", "100%", 1.0)],
          buttons=[("SC IN", True), ("AUDITION", False)],
          meter="GR: −1…−2 dB в ритме бочки", accent="#50a0b4")

# Keys LA-2A
knob_card("comp-keys-la2a.png",
          "KEYS — LA-2A",
          "Чуть выровнять клавиши, не задушить динамику",
          [("PEAK REDUCTION", "GR 1–2 dB", 0.3), ("GAIN", "по уровню", 0.5)],
          buttons=[("COMP", True), ("LIMIT", False)],
          meter="GR: −1…−2 dB")

# MIX BUS цепочка
knob_card("knob-mixbus-tape.png",
          "MIX BUS — плёнка (Studer/Satin) + Glue, легче чем на барабанах",
          "Input +1…+2 (мягче, чем на DRUM BUS!) · Glue 2:1, GR ~1 dB",
          [("TAPE INPUT", "+1…+2 dB", 0.45), ("SPEED", "15 IPS", 0.5),
           ("GLUE RATIO", "2:1", 0.25), ("GLUE ATT", "30 ms", 0.6),
           ("GLUE GR", "~1 dB", 0.2)],
          meter="Весь микс: тёплый, не раздавленный", accent="#e0a050")

print("ALL DONE")
