#!/usr/bin/env python3
"""PDF: карта мультитрека + план groove-сведения."""
from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

DARK = (32, 28, 24)
ACCENT = (224, 160, 80)
BLUE = (80, 160, 180)
RED = (192, 88, 64)
GREY = (120, 112, 100)
TXT = (40, 36, 32)


class PDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("DejaVu", "", DEJAVU + "DejaVuSans.ttf")
        self.add_font("DejaVu", "B", DEJAVU + "DejaVuSans-Bold.ttf")
        self.set_auto_page_break(True, margin=16)
        self.set_margins(14, 14, 14)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, "Groove Mix Session · карта мультитрека и план сведения",
                  new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(1)

    def footer(self):
        self.set_y(-13)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"— {self.page_no()} —", align="C")

    def h2(self, t, color=ACCENT):
        if self.get_y() > 252:
            self.add_page()
        self.ln(2.5)
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(*TXT)
        self.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*color)
        self.set_line_width(0.5)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(2.5)

    def h3(self, t, color=BLUE):
        if self.get_y() > 262:
            self.add_page()
        self.ln(1)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")

    def row(self, c1, c2, c3, head=False, w=(44, 70, 68)):
        if self.get_y() > 268:
            self.add_page()
        self.set_font("DejaVu", "B" if head else "", 8.4)
        self.set_text_color(*(TXT if not head else GREY))
        self.set_draw_color(225, 218, 205)
        self.set_line_width(0.2)
        x = self.get_x()
        y = self.get_y()
        h = 5.4
        # вычислить высоту по самой длинной ячейке
        lines = 1
        for txt, wd in zip((c1, c2, c3), w):
            n = len(self.multi_cell(wd, h, txt, split_only=True))
            lines = max(lines, n)
        hh = h * lines
        for txt, wd in zip((c1, c2, c3), w):
            self.rect(x, y, wd, hh)
            self.set_xy(x, y)
            self.multi_cell(wd, h, txt)
            x += wd
        self.set_xy(14, y + hh)

    def check(self, text, indent=0):
        x0 = 16 + indent
        self.set_x(x0)
        y = self.get_y() + 1
        self.set_draw_color(*GREY)
        self.set_line_width(0.3)
        self.rect(x0, y, 3.4, 3.4)
        self.set_x(x0 + 5.5)
        self.set_font("DejaVu", "", 9.3)
        self.set_text_color(*TXT)
        self.multi_cell(190 - x0, 5.2, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)


pdf = PDF()
pdf.add_page()

# Титул
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 54, style="F")
pdf.set_fill_color(*ACCENT)
pdf.rect(0, 54, 210, 1.6, style="F")
pdf.set_xy(14, 12)
pdf.set_font("DejaVu", "B", 20)
pdf.set_text_color(245, 240, 230)
pdf.cell(0, 10, "Groove Mix Session", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(210, 200, 185)
pdf.cell(0, 7, "Карта мультитрека + план сведения · звук Kravitz / Morcheeba / Jamiroquai",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("DejaVu", "", 8.5)
pdf.set_text_color(170, 160, 145)
pdf.cell(0, 6, "Обработка барабанов — по карточкам bfd3-groove/groove-preset-cards.md",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_y(62)

pdf.h2("0 · Импорт в Cubase")
pdf.check("Частота проекта = частоте WAV (44.1/48) · импорт всех файлов в начало проекта, копия в папку проекта")
pdf.check("Проверить, что стемы встали в сетку (транзиенты бочки по клику); темп найти по Demo minus (Tempo Detection)")
pdf.check("Pre Gain: пики каждого трека к −18…−12 dBFS")

pdf.h2("1 · Карта треков")

pdf.h3("Барабаны — ядро (сводим по groove-карточкам)")
pdf.row("WAV", "Что это", "Куда / карточка", head=True)
pdf.row("Kick beater", "микрофон колотушки (= Kick In)", "группа KICK · GRV Kick In")
pdf.row("Kick front", "фронт бочки (= Kick Out)", "группа KICK · GRV Kick Out")
pdf.row("Snare top", "верх рабочего", "группа SNARE · GRV Snare Top")
pdf.row("Snare bottom", "низ рабочего — ПОЛЯРНОСТЬ ø!", "группа SNARE · GRV Snare Bottom")
pdf.row("Tom 1 / 2 / 3", "томы", "группа TOMS · GRV Toms")
pdf.row("HiHat extra dry", "хэт сухой — ОСНОВНОЙ", "в DRUM BUS · карточка HH")
pdf.row("HiHat / HH wet", "варианты хэта с обработкой", "MUTE (wet можно −12 дБ для вайба)")
pdf.row("Overhead", "основные OH", "в DRUM BUS · GRV OH")
pdf.row("Overhead HH_Cow", "OH на хэт+ковбелл", "подмешать к OH −6…−8 дБ, сверить ø и панораму")
pdf.row("Room", "комната", "группа ROOMS · GRV Rooms")
pdf.row("Cowbell", "ковбелл", "отд. канал в DRUM BUS: HPF 300 · LPF 8k · −10…−14 дБ под хэтом")

pdf.h3("Гитары (пары: обработка + dry)")
pdf.row("WAV", "Что это", "Что делать", head=True)
pdf.row("Guit / Guit 2 / Guit 3", "партии в печати", "группа GTR · HPF 90–100 · комп 2:1 GR 2–3 дБ · панорамы L/C/R")
pdf.row("Guit drt / 2 dry / 3 dry", "те же партии сухие (DI)", "MUTE — запас под реамп")
pdf.row("Guit FX 1", "запечённый эффект", "по вкусу, скорее MUTE")

pdf.h3("Клавиши и синты")
pdf.row("WAV", "Что это", "Что делать", head=True)
pdf.row("Keys", "клавиши", "группа SYNTH · HPF 100 · −2 дБ @ 200–350 если мутнит · LA-2A GR 1–2")
pdf.row("Serum 2 / 3", "синты", "группа SYNTH · HPF 100–150 · лёгкий сайдчейн от бочки")
pdf.row("Spire-1.5 (+3/4/5/(6))", "синт-слои, похоже 6 шт.", "прослушать по одному, лишние MUTE")

pdf.h3("Технические / референсы — В МИКС НЕ ИДУТ", RED)
pdf.row("WAV", "Что это", "Что делать", head=True)
pdf.row("Master", "готовый микс автора", "MUTE · ваш референс для A/B на равной громкости")
pdf.row("Demo minus (+ -01)", "минус", "MUTE · референс аранжировки")
pdf.row("Out 1-2 / A Output / KT Out", "распечатки выходов", "MUTE / удалить (прослушать KT Out — вдруг дубль)")
pdf.row("Drums FX / Snare FX / Toms FX", "печёные FX барабанов из демо", "сначала MUTE — свои FX строим сами; уникальную фишку можно подмешать −10…−14 дБ потом")

pdf.h2("2 · Группы")
pdf.set_font("DejaVu", "", 9.5)
pdf.set_text_color(*TXT)
pdf.multi_cell(0, 5.6,
    "KICK, SNARE, TOMS, ROOMS → DRUM BUS (+ HiHat, OH, Cowbell напрямую)\n"
    "Guit 1-3 → GTR · Keys/Serum/Spire → SYNTH\n"
    "DRUM BUS + GTR + SYNTH → MIX BUS → Stereo Out · все группы СТЕРЕО\n"
    "FX: Verb (тёмная Room 0.9 c) и FAT (LA-2A параллель) — из groove-карточек",
    new_x="LMARGIN", new_y="NEXT")

pdf.h2("3 · Порядок сведения")
pdf.check("Фазы: Snare bottom ø · Kick beater vs front · OH vs ядро · Overhead HH_Cow vs Overhead")
pdf.check("Барабаны по groove-карточкам: LA-2A на бочке · жир 180 Гц на рабочем · тёмные OH · Fatso на руме · плёнка на DRUM BUS")
pdf.check("Ковбелл: скромно (−10…−14 дБ), панорама как в OH, чуть сатурации")
pdf.check("Гитары: низ отдать ритм-секции (HPF), панорамы развести, комп едва-едва")
pdf.check("Синты: HPF обязательно, лишние слои Spire выключить, сайдчейн от бочки −1…−2 дБ")
pdf.check("Баланс жанра: рабочий ≥ бочки · хэт заметный · синты — подложка")
pdf.check("A/B с Master.wav на одинаковой громкости — финальная сверка")
pdf.check("MIX BUS: плёнка/Glue ещё мягче, чем на DRUM BUS (GR ~1 дБ)")

pdf.h2("Грабли мультитрека", RED)
pdf.set_font("DejaVu", "", 9.3)
for e in ["Стемы встали не с 1-го такта — всё разъехалось",
          "Забытый mute на Master/minus — «микс двоится»",
          "Два хэта одновременно (HiHat + extra dry) — гребёнка!",
          "Печёные FX поверх своих — каша; сначала свои",
          "Синтовый суб + бочка без сайдчейна — гудит низ"]:
    pdf.set_x(16)
    pdf.cell(0, 5.6, "✗  " + e, new_x="LMARGIN", new_y="NEXT")

pdf.output(os.path.join(BASE, "Groove-Mix-Session.pdf"))
print("PDF saved")
