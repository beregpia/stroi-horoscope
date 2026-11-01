#!/usr/bin/env python3
"""ПОЛНЫЙ PDF: карта мультитрека + 10 шагов с картинками (вкл. бас и вокал)."""
from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
GIMG = os.path.join(BASE, "..", "bfd3-groove", "img")
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
        self.cell(0, 6, "Groove Mix Session · полный гид со схемами",
                  new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(1)

    def footer(self):
        self.set_y(-13)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"— {self.page_no()} —", align="C")

    def h2(self, t, color=ACCENT):
        if self.get_y() > 248:
            self.add_page()
        self.ln(2.5)
        self.set_font("DejaVu", "B", 12.5)
        self.set_text_color(*TXT)
        self.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*color)
        self.set_line_width(0.6)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(2.5)

    def h3(self, t, color=BLUE):
        if self.get_y() > 260:
            self.add_page()
        self.ln(1)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")

    def row(self, c1, c2, c3, head=False, w=(44, 70, 68)):
        if self.get_y() > 266:
            self.add_page()
        self.set_font("DejaVu", "B" if head else "", 8.4)
        self.set_text_color(*(TXT if not head else GREY))
        self.set_draw_color(225, 218, 205)
        self.set_line_width(0.2)
        x = self.get_x()
        y = self.get_y()
        h = 5.4
        lines = 1
        for txt, wd in zip((c1, c2, c3), w):
            n = len(self.multi_cell(wd, h, txt, dry_run=True, output="LINES"))
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

    def img(self, path, w=120):
        if not os.path.exists(path):
            return
        # высота ~ w * 0.48 (4.6/9.6)
        hh = w * 0.48
        if self.get_y() + hh > 276:
            self.add_page()
        x = (210 - w) / 2
        self.image(path, x=x, w=w)
        self.ln(1.5)

    def note(self, text):
        self.set_x(18)
        self.set_font("DejaVu", "", 8.6)
        self.set_text_color(*GREY)
        self.multi_cell(174, 4.7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


pdf = PDF()
pdf.add_page()

# ================= Титул =================
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 60, style="F")
pdf.set_fill_color(*ACCENT)
pdf.rect(0, 60, 210, 1.8, style="F")
pdf.set_xy(14, 13)
pdf.set_font("DejaVu", "B", 22)
pdf.set_text_color(245, 240, 230)
pdf.cell(0, 11, "Groove Mix Session — полный гид", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(210, 200, 185)
pdf.cell(0, 7, "Мультитрек: барабаны · бас · гитары · клавиши · синты · вокал + 2 бэка",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_x(14)
pdf.set_font("DejaVu", "", 9)
pdf.set_text_color(170, 160, 145)
pdf.cell(0, 6, "Звук: Lenny Kravitz / Morcheeba / Jamiroquai · кривые EQ посчитаны по формулам RBJ",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_y(68)

# ================= Импорт =================
pdf.h2("0 · Импорт в Cubase")
pdf.check("Частота проекта = частоте WAV · импорт всех файлов в начало проекта · копия в папку проекта")
pdf.check("Стемы в сетке? Темп — по Demo minus (Tempo Detection)")
pdf.check("Pre Gain: пики к −18…−12 dBFS")

# ================= Карта =================
pdf.h2("1 · Карта треков")

pdf.h3("Барабаны")
pdf.row("WAV", "Что это", "Куда", head=True)
pdf.row("Kick beater / Kick front", "колотушка / фронт бочки", "группа KICK (In/Out)")
pdf.row("Snare top / bottom", "рабочий · на bottom ПОЛЯРНОСТЬ ø!", "группа SNARE")
pdf.row("Tom 1 / 2 / 3", "томы", "группа TOMS")
pdf.row("HiHat extra dry", "хэт — ОСНОВНОЙ", "в DRUM BUS")
pdf.row("HiHat / HH wet", "варианты хэта", "MUTE (wet можно −12 дБ для вайба)")
pdf.row("Overhead", "основные OH", "в DRUM BUS")
pdf.row("Overhead HH_Cow", "OH на хэт+ковбелл", "подмешать −6…−8 дБ · проверить ø!")
pdf.row("Room", "комната", "группа ROOMS")
pdf.row("Cowbell", "ковбелл", "отд. канал в DRUM BUS")

pdf.h3("Инструменты")
pdf.row("WAV", "Что это", "Куда", head=True)
pdf.row("Guit / Guit 2 / Guit 3", "гитары в печати", "группа GTR · панорамы C/L/R")
pdf.row("Guit drt / * dry", "сухие дубли (DI)", "MUTE — запас под реамп")
pdf.row("Keys", "клавиши", "группа SYNTH")
pdf.row("Serum 2/3, Spire-1.5*", "синты · ОДИН ИЗ НИХ — БАС!", "бас → канал BASS (отдельно!) · остальные → SYNTH · лишние слои MUTE")
pdf.row("Вокал лид", "главный голос", "группа VOX")
pdf.row("Бэк 1 / Бэк 2", "бэк-вокалы", "группа BACKS · панорамы L50/R50")

pdf.h3("В микс НЕ идут", RED)
pdf.row("WAV", "Что это", "Что делать", head=True)
pdf.row("Master", "микс автора", "MUTE · референс для A/B")
pdf.row("Demo minus (+ -01)", "минус", "MUTE · референс")
pdf.row("Out 1-2 / A Output / KT Out", "распечатки выходов", "MUTE / удалить")
pdf.row("Drums FX / Snare FX / Toms FX", "печёные FX из демо", "сначала MUTE; фишку можно подмешать потом")

pdf.note("Как найти бас среди синтов: соло по очереди. Бас играет по одной ноте внизу (ниже ~250 Гц) "
         "в ритме с бочкой. Он идёт на отдельный канал BASS, не в группу SYNTH!")

# ================= Группы =================
pdf.h2("2 · Группы (все стерео)")
pdf.set_font("DejaVu", "", 9.5)
pdf.set_text_color(*TXT)
pdf.multi_cell(0, 5.6,
    "KICK, SNARE, TOMS, ROOMS → DRUM BUS (+ HiHat, OH, Cowbell напрямую)\n"
    "GTR (гитары) · SYNTH (Keys+синты) · BASS (отдельно!) · VOX (лид) · BACKS (бэки)\n"
    "DRUM BUS + GTR + SYNTH + BASS + VOX + BACKS → MIX BUS → Stereo Out\n"
    "FX: Verb барабанный (тёмная Room) · FAT (LA-2A параллель) · VOX Verb (Plate + дилей)",
    new_x="LMARGIN", new_y="NEXT")

# ================= Шаги =================
pdf.h2("Шаг 1 · Фазы — до любых плагинов!")
pdf.check("Snare bottom → ø (MixConsole → Pre)")
pdf.check("Kick beater vs front: вместе низа должно быть БОЛЬШЕ. Нет → ø на front")
pdf.check("OH + бочка + рабочий: низ не 'худеет'? → иначе ø на OH")
pdf.check("Overhead HH_Cow vs Overhead — тот же тест, главный кандидат на гребёнку!")

pdf.h2("Шаг 2 · Бочка (beater + front → KICK)")
pdf.img(os.path.join(GIMG, "eq-kick-in.png"))
pdf.img(os.path.join(GIMG, "eq-kick-out.png"))
pdf.img(os.path.join(GIMG, "comp-kick-la2a.png"))
pdf.check("beater = Kick In (круглая атака 1.8 кГц, не клик) · front = Kick Out (тело 70 Гц)")
pdf.check("Группа: LA-2A GR 3–4 дБ → Decapitator T, Mix 30%")

pdf.h2("Шаг 3 · Рабочий (top + bottom → SNARE)")
pdf.img(os.path.join(GIMG, "eq-snare-top.png"))
pdf.img(os.path.join(GIMG, "comp-snare-1176.png"))
pdf.check("Top: ЖИР +4 дБ @ 180 Гц · LPF 12k · Bottom: ø! HPF 400, фейдер −10…−12 дБ")
pdf.check("Группа: CLA-76 ленивый (Attack 2, Release 5, GR 2–4) — ghost-ноты дышат!")

pdf.h2("Шаг 4 · Томы и хэт")
pdf.img(os.path.join(GIMG, "eq-toms.png"))
pdf.check("Томы: EQ по кривой · гейт мягкий (Range −12) или без")
pdf.check("HiHat extra dry: HPF 250 · Morcheeba-вайб: shelf −2 дБ @ 8k · остальные хэты MUTE")

pdf.h2("Шаг 5 · Оверхеды и комната")
pdf.img(os.path.join(GIMG, "eq-oh-vintage.png"))
pdf.img(os.path.join(GIMG, "comp-rooms-fatso.png"))
pdf.check("Overhead: полная картина, HPF 90, ТЁМНЫЙ верх (shelf −2.5 @ 9k)")
pdf.check("HH_Cow: подмешать −6…−8 дБ · Room → ROOMS: EQ → Fatso GR 4–6 дБ")

pdf.h2("Шаг 6 · Ковбелл")
pdf.img(os.path.join(IMG, "eq-cowbell.png"))
pdf.check("HPF 300 · LPF 8k · панорама как в OH · фейдер −10…−14 дБ ПОД хэтом · чуть Decapitator N")

pdf.h2("Шаг 7 · Гитары (→ GTR)")
pdf.img(os.path.join(IMG, "eq-guitar.png"))
pdf.img(os.path.join(IMG, "comp-guitar.png"))
pdf.check("Каждая: HPF 95 · −2.5 дБ @ 300 · LPF 11k · панорамы: Guit 2 ←L, Guit 3 →R, Guit — центр")
pdf.check("Группа: LA-2A / Pro-C 2 (2:1, GR 2–3 дБ) · dry-версии MUTE")

pdf.h2("Шаг 8 · Клавиши и синты (→ SYNTH)")
pdf.img(os.path.join(IMG, "eq-keys.png"))
pdf.img(os.path.join(IMG, "eq-synth.png"))
pdf.img(os.path.join(IMG, "comp-sidechain.png"))
pdf.check("Keys: HPF 100 · −2 дБ @ 250 · LA-2A GR 1–2")
pdf.check("Синты: слои по одному, лишние MUTE · HPF 130 · shelf −2 @ 10k")
pdf.check("Группа SYNTH: сайдчейн от Kick front (2:1, 5 ms, 120 ms, GR 1–2 дБ) — приседают под бочку")

pdf.h2("Шаг 8.3 · БАС (найден в синтах!) → канал BASS")
pdf.note("Бас + бочка = фундамент. Канал BASS в центре, НЕ в группе SYNTH, моно ниже 150 Гц.")
pdf.img(os.path.join(IMG, "eq-bass.png"))
pdf.img(os.path.join(IMG, "comp-bass.png"))
pdf.img(os.path.join(IMG, "comp-bass-sc.png"))
pdf.img(os.path.join(IMG, "knob-bass-sat.png"))
pdf.check("EQ: HPF 30 · +2 @ 80 · −2 @ 250 · +2.5 @ 800 (читаемость на телефоне!) · LPF 7k")
pdf.check("Комп: 4:1, Attack 15 ms, GR 3–5 дБ стабильно — ровный как рельс")
pdf.check("Сайдчейн от Kick front: 3:1, Attack 1 ms, Release 100 ms, GR 2–3 дБ — КЛЮЧ К ГРУВУ")
pdf.check("Сатурация: Drive 2–3, Mix 30–40% — гармоники для маленьких колонок")
pdf.check("Соло KICK + BASS: должны звучать как один инструмент (бочка — удар, бас — нота)")

pdf.h2("Шаг 8.5 · Вокал: лид + 2 бэка (→ VOX и BACKS)")
pdf.h3("Чистка от бяк (до всего!) — порядок: ремонт → шум → щелчки/дыхания → де-эссер → резонансы", RED)
pdf.check("1а. RX Spectral De-noise (офлайн!): Learn на тишине → Reduction 6–12 дБ. Бюджет: Clarity Vx / Bertom Denoiser")
pdf.img(os.path.join(IMG, "clean-rx-denoise.png"))
pdf.check("1б. RX Mouth De-click: Sensitivity 3–5 — щелчки губ. Плюс De-hum (гул) и Spectral Repair (точечные бяки кистью)")
pdf.img(os.path.join(IMG, "clean-rx-declick.png"))
pdf.check("2. Дыхания: RX Breath Control / Waves DeBreath на −10…−15 дБ")
pdf.img(os.path.join(IMG, "clean-debreath.png"))
pdf.check("3. Де-эссер (Pro-DS Single Vocal): 5–9 кГц, GR 2–4 дБ только на 'с/ц'")
pdf.img(os.path.join(IMG, "clean-prods.png"))
pdf.check("4. soothe2: гнусавость/жёсткость/звон — динамически")
pdf.img(os.path.join(IMG, "clean-soothe2.png"))
pdf.check("5. EQ-хирургия: свип узким Q по 150–500 Гц → вырезы −3…−5 дБ, Q 2–3")
pdf.img(os.path.join(IMG, "clean-eq-sweep.png"))
pdf.check("6. Интонация: VariAudio (в Cubase Pro!) / Melodyne — коррекция ≤ 50%")

# Золотые правила — рамка
if pdf.get_y() > 215:
    pdf.add_page()
_y = pdf.get_y() + 2
pdf.set_fill_color(252, 243, 228)
pdf.set_draw_color(*ACCENT)
pdf.set_line_width(0.5)
pdf.rect(16, _y, 178, 42, style="DF")
pdf.set_xy(22, _y + 4)
pdf.set_font("DejaVu", "B", 11)
pdf.set_text_color(*RED)
pdf.cell(0, 6, "★ Золотые правила чистки вокала", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("DejaVu", "", 9.2)
pdf.set_text_color(*TXT)
for r in ["RX — всегда ОФЛАЙН-рендером, не реалтайм-плагином · оригинал файла сохранить!",
          "Не перечищать: дыхания −10 дБ (не в ноль) · шумодав 6–12 дБ (не 30)",
          "После каждого шага — A/B с оригиналом: стало лучше или просто тише/мертвее?",
          "Лёгкая комната и вдохи — часть вайба Kravitz/Morcheeba. Стерильный вокал = бяка наоборот",
          "Порядок важен: сначала хирургия (RX), потом косметика (EQ/комп)"]:
    pdf.set_x(22)
    pdf.multi_cell(166, 5.4, "• " + r, new_x="LMARGIN", new_y="NEXT")
pdf.set_y(_y + 44)
pdf.ln(2)

pdf.h3("Основная цепочка лида")
pdf.img(os.path.join(IMG, "eq-vocal-lead.png"))
pdf.img(os.path.join(IMG, "comp-vocal-1176.png"))
pdf.img(os.path.join(IMG, "comp-vocal-la2a.png"))
pdf.check("Лид EQ: HPF 90 · −2.5 @ 300 · динам. −3 @ 2.5–4k · shelf +2 @ 10k мягко")
pdf.check("Компрессия в 2 ступени: CLA-76 пики (GR 2–4) → LA-2A фразы (GR 3–5)")
pdf.check("После: Saturn/Decapitator T, Mix 10–15% — тёплая лампа")
pdf.img(os.path.join(IMG, "eq-vocal-back.png"))
pdf.img(os.path.join(IMG, "comp-vocal-backs.png"))
pdf.check("Бэки: панорамы L50/R50 · HPF 150 · −3 @ 2.5k (уступаем лиду!) · комп GR 5–7 — 'подушка'")
pdf.check("Фейдер BACKS: −8…−12 дБ под лидом (выкл — лид 'осиротел', вкл — 'оделся')")
pdf.img(os.path.join(IMG, "knob-vocal-fx.png"))
pdf.check("FX: Plate 1.2 с, pre-delay 40 мс + дилей 1/8 dotted · бэкам верба больше")
pdf.check("Сайдчейн-дак: GTR и SYNTH приседают под VOX на −1 дБ (2:1, 10 ms, 150 ms)")

pdf.h2("Шаг 9 · Шины")
pdf.img(os.path.join(GIMG, "knob-tape.png"))
pdf.img(os.path.join(GIMG, "eq-drumbus.png"))
pdf.check("DRUM BUS: плёнка 15 IPS (+2…+4) → Glue 2:1 GR 1–2 → EQ винтажный тон")
pdf.check("FX FAT и Verb — по groove-карточкам")
pdf.img(os.path.join(IMG, "knob-mixbus-tape.png"))
pdf.img(os.path.join(IMG, "eq-mixbus.png"))
pdf.check("MIX BUS: плёнка мягче (+1…+2) → Glue GR ~1 дБ → shelf +1 @ 80 / −1 @ 13k · БЕЗ лимитера")

pdf.h2("Шаг 10 · Баланс и сверка")
pdf.check("Вокал сидит В миксе · рабочий ≥ бочки · хэт заметный · бас+бочка = один инструмент · синты — подложка")
pdf.check("A/B с Master.wav на одинаковой громкости")
pdf.check("Моно-проверка (бэки L/R — кандидаты на пропажу!) · маленькие колонки")
pdf.check("Автоматизация вокального фейдера по фразам (±1–1.5 дБ) — последние 10% магии")

pdf.h2("Грабли мультитрека", RED)
pdf.set_font("DejaVu", "", 9.3)
pdf.set_text_color(*TXT)
for e in ["Стемы встали не с 1-го такта — всё разъехалось",
          "Забытый mute на Master/minus — 'микс двоится'",
          "Два хэта одновременно — гребёнка!",
          "Бас в группе SYNTH под общим сайдчейном — двойное приседание",
          "Бас стерео внизу — каша в моно",
          "Печёные FX поверх своих — каша; сначала свои",
          "Бэки громче лида — 'хор' вместо песни"]:
    pdf.set_x(16)
    pdf.cell(0, 5.6, "✗  " + e, new_x="LMARGIN", new_y="NEXT")

pdf.output(os.path.join(BASE, "Groove-Mix-Session.pdf"))
print("PDF saved")
