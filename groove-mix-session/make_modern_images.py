#!/usr/bin/env python3
"""Моднятина: карточки современных трюков — румы и весь микс."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
BG = "#201c18"; GRID = "#35302a"; TXT = "#f2ede4"; SUB = "#a89d8c"

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


# ---------- ШАГ 5.5: МОДНЫЕ РУМЫ ----------

# 1. Devil Crush
knob_card("modern-devilloc.png",
          "ROOM CRUSH — Devil-Loc Deluxe (параллель)",
          "Или 1176 All-Buttons-In · подмешать −10…−6 дБ под основной рум · автоматом в припевах!",
          [("CRUSH", "5–7", 0.6), ("CRUNCH", "2–3", 0.28),
           ("DARKNESS", "3–4 (винтаж!)", 0.38), ("MIX", "у фейдера", 0.5)],
          buttons=[("ALL-IN", True)],
          meter="Выключили — должно стать ЖАЛКО", accent="#c05840")

# 2. Trash Mic
knob_card("modern-trashmic.png",
          "TRASH MIC — а-ля Tchad Blake (параллель, MONO!)",
          "Цепочка: HPF 200 → LPF 2.5k → Decapitator → в МОНО · узкий грязный центр под широкими OH",
          [("HPF", "200 Hz", 0.3), ("LPF", "2.5 kHz", 0.45),
           ("DRIVE", "5–7 (Style P)", 0.6), ("OUTPUT", "по уровню", 0.5)],
          buttons=[("MONO", True), ("P", True)],
          meter="Подмешать чуть-чуть: радио-мусорный жир", accent="#8a6fb0")

# 3. Room duck
knob_card("modern-roomduck.png",
          "ROOM DUCK — компрессор с сайдчейном от бочки",
          "Рум приседает на удар бочки (низ не мылится) и расцветает между ударами — 'дыхание' микса",
          [("RATIO", "4:1", 0.5), ("ATTACK", "1 ms", 0.08),
           ("RELEASE", "150 ms", 0.3), ("GR", "3–4 dB", 0.4)],
          buttons=[("SC: KICK", True)],
          meter="Release в темп: качает — правильно", accent="#50a0b4")

# 4. Transient designer
knob_card("modern-transient.png",
          "ROOM SUSTAIN — SPL Transient Designer / Smack Attack",
          "Атаки убрать (они в закрытых микрофонах), хвосты комнаты вытянуть → чистый 'воздух и размер'",
          [("ATTACK", "−3…−5", 0.3), ("SUSTAIN", "+4…+6", 0.72),
           ("OUTPUT", "по уровню", 0.5)],
          meter="Каши меньше, комнаты больше", accent="#e0a050")

# ---------- БОНУС: МОДНЯТИНА ПО ВСЕМУ МИКСУ ----------

# 5. Параллельный драм-краш
knob_card("modern-drumsmash.png",
          "DRUM SMASH — параллельный краш всей установки",
          "Посыл ВСЕХ барабанов (кроме румов) → 1176 All-In / OTT · фейдер −10…−6 дБ под главным звуком",
          [("INPUT", "жарко, GR 8–12", 0.75), ("ATTACK", "3 (медл. шкала!)", 0.4),
           ("RELEASE", "7 (быстро)", 0.85), ("FADER", "−10…−6 dB", 0.35)],
          buttons=[("ALL-IN", True)],
          meter="Жир в куплете, взрыв в припеве", accent="#c05840")

# 6. Суб-генератор бочки
knob_card("modern-subkick.png",
          "KICK SUB — bx_subsynth / SubLab / R-Bass (параллель)",
          "Догенерировать суб 40–60 Hz, если бочке не хватает фундамента · ПОСЛЕ сайдчейнов!",
          [("RANGE", "40–60 Hz", 0.25), ("MIX", "15–25%", 0.25),
           ("OUTPUT", "по уровню", 0.5)],
          buttons=[("MONO", True)],
          meter="Проверка на НАУШНИКАХ + маленьких колонках",
          accent="#50a0b4")

# 7. Вокальная ширина
knob_card("modern-voxwidth.png",
          "VOX WIDTH — micro-pitch (трюк Эдди Ван Халена для вокала)",
          "Копия лида → питч −9 cents в L, +9 cents в R, delay 15/23 ms · подмешать −12 дБ под лидом",
          [("PITCH L", "−9 cents", 0.42), ("PITCH R", "+9 cents", 0.58),
           ("DELAY L/R", "15 / 23 ms", 0.2), ("MIX", "−12 dB под лидом", 0.3)],
          buttons=[("100% WET", True)],
          meter="Лид широкий, но В МОНО не плывёт — проверить!", accent="#8a6fb0")

# 8. OTT на синты/бэки
knob_card("modern-ott.png",
          "OTT (Xfer, бесплатный) — синты и бэки по-современному",
          "Мультибэнд-жмак: детали и плотность · НО: Depth 10–25%, не 100% как в дабстепе!",
          [("DEPTH", "10–25% !!!", 0.18), ("TIME", "150 ms", 0.4),
           ("IN GAIN", "по GR 2–4", 0.4), ("OUT", "по уровню", 0.5)],
          meter="100% Depth = EDM-пластик, нам нельзя", accent="#e0a050")

# 9. Telephone throw
knob_card("modern-voxthrow.png",
          "VOX THROW — 'телефон' на последнее слово фразы",
          "FX-канал: HPF 800 + LPF 3k + delay 1/4 (feedback 35%) · посыл АВТОМАТИЗАЦИЕЙ только на слово",
          [("HPF", "800 Hz", 0.55), ("LPF", "3 kHz", 0.5),
           ("DELAY", "1/4", 0.5), ("FEEDBACK", "35%", 0.35)],
          buttons=[("AUTO", True)],
          meter="Morcheeba-магия: слово улетает в даль", accent="#8a6fb0")

# 10. Клиппер на драм-бас
knob_card("modern-clipper.png",
          "SOFT CLIPPER — DRUM BUS (KClip / StandardCLIP / FreeClip)",
          "Срезать 1–2 дБ самых острых пиков ДО Glue-компрессора — громче и плотнее без накачки",
          [("THRESHOLD", "пики 1–2 dB", 0.6), ("KNEE", "soft", 0.4),
           ("OUTPUT", "по уровню", 0.5)],
          meter="Слышно искажение = перебор, откатить", accent="#c05840")

print("ALL DONE")
