#!/usr/bin/env python3
"""Vintage Groove Edition (Kravitz / Morcheeba / Jamiroquai):
EQ-кривые (биквады RBJ) + карточки ручек. Тёплая палитра."""
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

BG = "#201c18"        # тёплый тёмный
GRID = "#35302a"
TXT = "#f2ede4"
SUB = "#a89d8c"
CURVE = "#e0a050"     # янтарный
FILL_P = "#e0a05033"
FILL_N = "#50a0b433"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TXT, "axes.edgecolor": GRID,
    "axes.labelcolor": SUB, "xtick.color": SUB, "ytick.color": SUB,
})


def biquad_response(b, a):
    w = 2 * np.pi * F / FS
    z = np.exp(-1j * w)
    h = (b[0] + b[1] * z + b[2] * z**2) / (a[0] + a[1] * z + a[2] * z**2)
    return 20 * np.log10(np.maximum(np.abs(h), 1e-9))


def peak(f0, gain_db, q):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / FS
    al = np.sin(w0) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w0), 1 - al * A]
    a = [1 + al / A, -2 * np.cos(w0), 1 - al / A]
    return biquad_response(b, a)


def shelf(f0, gain_db, high=True, s=0.9):
    A = 10 ** (gain_db / 40)
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
    return biquad_response(b, a)


def butter_hp(f0, order=4):
    total = np.zeros_like(F)
    for k in range(order // 2):
        q = 1 / (2 * np.sin(np.pi * (2 * k + 1) / (2 * order)))
        w0 = 2 * np.pi * f0 / FS
        al = np.sin(w0) / (2 * q)
        cos = np.cos(w0)
        b = [(1 + cos) / 2, -(1 + cos), (1 + cos) / 2]
        a = [1 + al, -2 * cos, 1 - al]
        total += biquad_response(b, a)
    return total


def butter_lp(f0, order=2):
    total = np.zeros_like(F)
    for k in range(order // 2):
        q = 1 / (2 * np.sin(np.pi * (2 * k + 1) / (2 * order)))
        w0 = 2 * np.pi * f0 / FS
        al = np.sin(w0) / (2 * q)
        cos = np.cos(w0)
        b = [(1 - cos) / 2, 1 - cos, (1 - cos) / 2]
        a = [1 + al, -2 * cos, 1 - al]
        total += biquad_response(b, a)
    return total


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
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"], fontsize=8.5)
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
        ax.text(cx, cy - r - 0.42, val, ha="center", fontsize=9.4, color=TXT, fontweight="bold")
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


# ===================== EQ-КРИВЫЕ (грув-версии!) =====================

# Kick In — МЕНЬШЕ щелчка, круглая атака (1-2 кГц вместо 4)
eq_plot("eq-kick-in.png",
        "KICK IN — Pro-Q 4   (круглая, а не кликовая!)",
        "HPF 30 Hz · −4 dB @ 400 Hz Q 1.2 · +2.5 dB @ 1.8 kHz Q 1.1 (мягкая атака) · LPF 10k",
        [butter_hp(30, 4), peak(400, -4, 1.2), peak(1800, 2.5, 1.1), butter_lp(10000, 2)],
        [(30, -3, "HPF 30", False), (400, -4, "−4 dB", False),
         (1800, 2.5, "+2.5 dB · мягко", False), (10000, -3, "LPF 10k", False)])

# Kick Out — жирное тело 60-90, вместо суб-50
eq_plot("eq-kick-out.png",
        "KICK OUT — Pro-Q 4   (тело выше, 'бум' 70-х)",
        "+4 dB @ 70 Hz Q 0.9 · −2.5 dB @ 300 Hz · LPF 6 kHz",
        [peak(70, 4, 0.9), peak(300, -2.5, 1.2), butter_lp(6000, 2)],
        [(70, 4, "+4 dB · тело!", False), (300, -2.5, "−2.5 dB", False),
         (6000, -3, "LPF 6k", False)])

# Snare — жир 150-250, минимум 5k-хайпа
eq_plot("eq-snare-top.png",
        "SNARE TOP — Pro-Q 4   (жирный, ленивый, THICK)",
        "HPF 70 Hz · +4 dB @ 180 Hz Q 1.0 (ЖИР) · −3 dB @ 550 Hz · +2 dB @ 3.5 kHz Q 1.2 · LPF 12k",
        [butter_hp(70, 4), peak(180, 4, 1.0), peak(550, -3, 1.6),
         peak(3500, 2, 1.2), butter_lp(12000, 2)],
        [(70, -3, "HPF 70", False), (180, 4, "+4 dB · ЖИР", False),
         (550, -3, "−3 dB", False), (3500, 2, "+2 dB · мягко", False),
         (12000, -3, "LPF 12k", False)])

eq_plot("eq-snare-bottom.png",
        "SNARE BOTTOM — Pro-Q 4   (ø вкл! пружины меньше, чем в роке)",
        "HPF 400 Hz · фейдер −10…−12 dB ниже Top (пружина — только намёк)",
        [butter_hp(400, 4)],
        [(400, -3, "HPF 400", False)])

# Toms — тёплые, бумкие
eq_plot("eq-toms.png",
        "TOMS — Pro-Q 4   (тёплые, без металла)",
        "HPF 60 Hz · +3 dB @ 100 Hz Q 0.9 · −4 dB @ 450 Hz · +2 dB @ 3 kHz · LPF 9k",
        [butter_hp(60, 4), peak(100, 3, 0.9), peak(450, -4, 1.4),
         peak(3000, 2, 1.1), butter_lp(9000, 2)],
        [(60, -3, "HPF 60", False), (100, 3, "+3 dB", False),
         (450, -4, "−4 dB", False), (9000, -3, "LPF 9k", False)])

# OH — ПОЛНАЯ картина, тёмный верх!
eq_plot("eq-oh-vintage.png",
        "OVERHEADS — Pro-Q 4   (полная картина, ТЁМНЫЙ верх — ключ к винтажу!)",
        "HPF 90 Hz · −2 dB @ 3.5 kHz Q 1.5 (DYN) · shelf −2.5 dB @ 9 kHz (приглушить!)",
        [butter_hp(90, 4), peak(3500, -2, 1.5), shelf(9000, -2.5, True)],
        [(90, -3, "HPF 90", False), (3500, -2, "−2 dB · DYN", True),
         (9000, -2.5, "shelf −2.5 · тьма", False)])

# Rooms — тёплая комната, не стадион
eq_plot("eq-rooms.png",
        "ROOMS — Pro-Q 4   (маленькая тёплая комната, не арена)",
        "HPF 80 Hz · −2 dB @ 600 Hz · shelf −3 dB @ 8 kHz (тёмный хвост)",
        [butter_hp(80, 4), peak(600, -2, 1.0), shelf(8000, -3, True)],
        [(80, -3, "HPF 80", False), (600, -2, "−2 dB", False),
         (8000, -3, "shelf −3", False)])

# Fat bus (вместо Smash) — мягкая параллель
eq_plot("eq-fat.png",
        "FX FAT — Pro-Q 4   (после LA-2A, тёплая параллель вместо NY-взрыва)",
        "+3 dB @ 120 Hz Q 0.8 · shelf +1.5 dB @ 5 kHz (чуть-чуть)",
        [peak(120, 3, 0.8), shelf(5000, 1.5, True)],
        [(120, 3, "+3 dB", False), (5000, 1.5, "shelf +1.5", False)], ymin=-12, ymax=12)

# Drum bus — винтажный тон
eq_plot("eq-drumbus.png",
        "DRUM BUS — Pro-Q 4   (винтажный тон: низ есть, верх скромный)",
        "shelf +1.5 dB @ 90 Hz · −1 dB @ 500 Hz · shelf −1.5 dB @ 12 kHz (анти-hi-fi!)",
        [shelf(90, 1.5, False), peak(500, -1, 1.0), shelf(12000, -1.5, True)],
        [(90, 1.5, "shelf +1.5", False), (500, -1, "−1 dB", False),
         (12000, -1.5, "shelf −1.5", False)], ymin=-9, ymax=9)

# ===================== КАРТОЧКИ РУЧЕК =====================

# Kick — LA-2A вместо 1176!
knob_card("comp-kick-la2a.png",
          "KICK GROUP — UAD/Arturia LA-2A",
          "Оптический — медленный и круглый по природе. Идеален для грув-бочки",
          [("PEAK REDUCTION", "GR 3–4 dB", 0.4), ("GAIN", "по уровню", 0.5)],
          buttons=[("COMP", True), ("LIMIT", False)],
          meter="GR: −3…−4 dB · медленно и кругло")

# Snare — 1176 но ленивый
knob_card("comp-snare-1176.png",
          "SNARE GROUP — CLA-76 / UAD 1176",
          "Медленнее, чем в роке: Attack 2, Release 5 — жир, а не щелчок",
          [("INPUT", "GR 2–4 dB", 0.42), ("OUTPUT", "по уровню", 0.5),
           ("ATTACK", "2 (медл.!)", 0.25), ("RELEASE", "5", 0.6)],
          buttons=[("4:1", True), ("8:1", False), ("12:1", False), ("20:1", False)],
          meter="GR: −2…−4 dB")

# Rooms — Fatso вместо Distressor NUKE
knob_card("comp-rooms-fatso.png",
          "ROOMS — UAD Fatso Jr/Sr (или Kotelnikov)",
          "Режим Spank умеренно + Warmth: тёплая комната, НЕ стадион",
          [("INPUT", "GR 4–6 dB", 0.55), ("WARMTH", "3–5", 0.45),
           ("OUTPUT", "по уровню", 0.5)],
          buttons=[("SPANK", True), ("TRACK", True)],
          meter="GR: −4…−6 dB — дышит, не рычит", accent="#c05840")

# Fat parallel — LA-2A
knob_card("comp-fat-la2a.png",
          "FX FAT — LA-2A (параллельная шина)",
          "Вместо взрывного NY — тёплое оптическое уплотнение",
          [("PEAK REDUCTION", "GR 6–8 dB", 0.62), ("GAIN", "+6…+8", 0.6)],
          buttons=[("COMP", True), ("LIMIT", False)],
          meter="GR: −6…−8 dB · кругло", accent="#c05840")

# Tape — главный клей жанра
knob_card("knob-tape.png",
          "DRUM BUS — UAD Studer A800 / Satin / Kramer Tape",
          "ПЛЁНКА — главный секрет Kravitz/Jamiroquai. 15 IPS, GP9",
          [("INPUT", "+2…+4 dB", 0.6), ("SPEED", "15 IPS", 0.5),
           ("LOW EMPH", "0", 0.5), ("HI EMPH", "−1", 0.45),
           ("OUTPUT", "по уровню", 0.5)],
          buttons=[("GP9", True), ("456", False), ("250", False)],
          meter="15 IPS = жирный низ + мягкий верх", accent="#e0a050")

# Glue — мягче чем в роке
knob_card("comp-bus-glue.png",
          "DRUM BUS — The Glue / SSL Bus Comp",
          "Мягче рока: 2:1, Attack 30, GR 1–2 dB — только обнять",
          [("RATIO", "2:1", 0.25), ("ATTACK", "30 ms", 0.6),
           ("RELEASE", "AUTO", 1.0), ("THRESH", "GR 1–2 dB", 0.3),
           ("MAKEUP", "по уровню", 0.4), ("MIX", "100%", 1.0)],
          meter="GR: −1…−2 dB", accent="#50a0b4")

# Decapitator — тёплый, не злой
knob_card("knob-decapitator.png",
          "SATURATION — Decapitator (бочка/рабочий)",
          "Style T (Triode — ламповое тепло) или N (Neve) · никакой злости",
          [("DRIVE", "1.5–2.5", 0.22), ("LOW CUT", "OFF", 0.0),
           ("TONE", "чуть темнее (11 ч)", 0.42), ("HIGH CUT", "12k", 0.75),
           ("MIX", "30%", 0.3), ("OUTPUT", "auto-comp", 0.5)],
          buttons=[("A", False), ("E", False), ("N", False), ("T", True), ("P", False)],
          meter="Punish: НИКОГДА", accent="#8c6a4a")

# Verb — короткая тёмная комната/spring
knob_card("knob-verb.png",
          "FX VERB — Valhalla VintageVerb",
          "Room (не Plate!) · Color 1970s · короткий тёмный хвост",
          [("MIX", "100%", 1.0), ("PREDELAY", "15 ms", 0.15),
           ("DECAY", "0.9 s", 0.12), ("SIZE", "небольшой", 0.35),
           ("HIGH CUT", "6 kHz", 0.4), ("LOW CUT", "250 Hz", 0.3)],
          buttons=[("ROOM", True), ("PLATE", False), ("SPRING", False)],
          meter="Mode: Room · 1970s · тёмный", accent="#8c6a4a")

print("ALL DONE")
