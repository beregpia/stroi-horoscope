#!/usr/bin/env python3
"""Plugin-Loadout.pdf: моднючий топ-лоадаут — кто встаёт в каждый слот паспорта."""
from fpdf import FPDF
from PIL import Image
import os

BASE = os.path.dirname(os.path.abspath(__file__))
RIMG = os.path.join(BASE, "img-real")
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

DARK = (32, 28, 24)
ACCENT = (224, 160, 80)
BLUE = (80, 160, 180)
RED = (192, 88, 64)
GREEN = (110, 150, 90)
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
        self.cell(0, 6, "Моднючий лоадаут · топ-плагины на каждый слот",
                  new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(1)

    def footer(self):
        self.set_y(-13)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"— {self.page_no()} —", align="C")

    def part(self, t):
        if self.get_y() > 225:
            self.add_page()
        self.ln(3)
        self.set_fill_color(*DARK)
        y = self.get_y()
        self.rect(14, y, 182, 10, style="F")
        self.set_xy(18, y + 1.6)
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(*ACCENT)
        self.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + 12.5)

    def plug(self, name, slot):
        if self.get_y() > 235:
            self.add_page()
        self.ln(2)
        self.set_font("DejaVu", "B", 11.5)
        self.set_text_color(*TXT)
        self.cell(0, 6.5, name, new_x="LMARGIN", new_y="NEXT")
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(*BLUE)
        self.multi_cell(182, 5, f"СЛОТ: {slot}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.4)
        self.line(14, self.get_y() + 0.8, 196, self.get_y() + 0.8)
        self.ln(2.2)

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

    def why(self, text):
        self.set_x(20)
        self.set_font("DejaVu", "", 8.6)
        self.set_text_color(*GREY)
        self.multi_cell(172, 4.6, "почему моднюче: " + text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.8)

    def img(self, name, w=110):
        path = os.path.join(RIMG, name)
        if not os.path.exists(path):
            return
        iw, ih = Image.open(path).size
        hh = w * ih / iw
        if hh > 105:
            w = 105 * iw / ih
            hh = 105
        if self.get_y() + hh > 274:
            self.add_page()
        x = (210 - w) / 2
        self.image(path, x=x, w=w)
        self.ln(1.5)

    def row(self, c1, c2, c3, head=False, w=(52, 70, 60)):
        if self.get_y() > 266:
            self.add_page()
        self.set_font("DejaVu", "B" if head else "", 8.4)
        self.set_text_color(*(GREY if head else TXT))
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

    def goldbox(self, title, rows, hbox):
        if self.get_y() + hbox > 272:
            self.add_page()
        y = self.get_y() + 2
        self.set_fill_color(252, 243, 228)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.5)
        self.rect(16, y, 178, hbox, style="DF")
        self.set_xy(22, y + 4)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(*RED)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_font("DejaVu", "", 9.2)
        self.set_text_color(*TXT)
        for r in rows:
            self.set_x(22)
            self.multi_cell(166, 5.4, "• " + r, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + hbox + 2)


pdf = PDF()
pdf.add_page()

# ================= Титул =================
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 297, style="F")
pdf.set_y(92)
pdf.set_font("DejaVu", "B", 28)
pdf.set_text_color(*ACCENT)
pdf.cell(0, 13, "МОДНЮЧИЙ ЛОАДАУТ", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("DejaVu", "B", 15)
pdf.set_text_color(242, 237, 228)
pdf.cell(0, 9, "топ-плагины 2026 на каждый слот нашего паспорта",
         new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)
pdf.set_font("DejaVu", "", 10.5)
pdf.set_text_color(168, 157, 140)
for s in ["умный гейт · нейро-чистка · Bricasti-ревер · авто-дакинг",
          "каждый — с настройками под нашу сессию",
          "",
          "цепочки и «что зачем» — Channel-Passport.pdf"]:
    pdf.cell(0, 6.5, s, new_x="LMARGIN", new_y="NEXT", align="C")

pdf.add_page()

# ============ БАРАБАНЫ ============
pdf.part("БАРАБАНЫ")

pdf.plug("Sonnox Oxford Drum Gate 2", "вместо обычных гейтов на kick beater / snare bottom / томах")
pdf.img("top-drumgate.png", w=125)
pdf.check("Drum: выбрать Kick/Snare/Tom · Detect сам отличает УДАР от bleed (видно треугольники под пиками)")
pdf.check("Threshold по экрану · вкладка Decay — форма хвоста вместо тупого Hold/Release")
pdf.check("Наш рецепт остаётся: прибирать, не убивать (у него это ручка Reduction, не −inf)")
pdf.why("обычный гейт слышит громкость, этот — распознаёт сам барабан: ghost-ноты выживают автоматически. Для нашего грува это золото")

pdf.plug("Kirchhoff-EQ (Three-Body Tech)", "вместо/рядом с Pro-Q на всех барабанных каналах")
pdf.img("top-kirchhoff.png", w=125)
pdf.check("Все наши EQ-карточки работают 1-в-1 · динамические полосы: Below/Above с Range и Ratio")
pdf.check("Фишка: типы фильтров легендарных консолей в каждой полосе (выбор кривой в band-меню)")
pdf.check("Для кольца рабочего: полоса 650 Гц, динамика Above, Attack 15/Release 200 — давит только звон")
pdf.why("главный претендент на трон Pro-Q: та же скорость, но динамика гибче и 'аналоговые' кривые. Моднее некуда")

pdf.plug("Shadow Hills Mastering Compressor (Brainworx/UAD)", "на DRUM BUS вместо простого glue")
pdf.img("top-shadowhills.png", w=125)
pdf.check("Двухступенчатый: OPTICAL (мягко собирает, GR 1–2) → DISCRETE (панч, Ratio 2:1, GR 1–2)")
pdf.check("Трансформатор: NICKEL = наш грув (мягкий винтаж) · IRON — нейтрально · STEEL — агрессия")
pdf.check("Итого GR суммарно 2–3 дБ — больше не надо, комната должна дышать")
pdf.why("компрессор с характером консоли за миллион: две ступени делают то, что у нас делали плёнка+glue по отдельности")

pdf.plug("Soundtheory Gullfoss", "на DRUMS или MIX BUS — ПОСЛЕДНИМ в цепи")
pdf.img("top-gullfoss.png", w=110)
pdf.check("Recover 20–30% (достаёт замазанные детали) · Tame 10–20% (давит кашу) — и это всё, две ручки")
pdf.check("Слушать A/B: барабаны становятся 'разборчивее', как будто протёрли стекло")
pdf.why("авто-EQ на психоакустической модели — пол-индустрии тихонько держит его на мастере. Две ручки, ноль мозга, вау-эффект")

# ============ БАС И СИНТЫ ============
pdf.part("БАС И СИНТЫ")

pdf.plug("Pulsar Mu", "BASS слот 2 (основной комп) · или MIX BUS glue")
pdf.img("top-pulsarmu.png", w=95)
pdf.check("Бас: Attack средний · Release Fast · GR 3–5 — вари-мю лампы ровняют и ГРЕЮТ одновременно")
pdf.check("Сайдчейн-EQ прямо внутри (ручки внизу): HPF 200 в детектор — низ не качает компрессор")
pdf.check("На MIX BUS: Attack Slow · Release Auto · GR ~1 — легендарный 'клей Fairchild-типа'")
pdf.why("самый хайповый вари-мю в плагинах: тепло лампы + современный сайдчейн-инструментарий")

pdf.plug("Xfer OTT + SubLab XL", "синты (OTT уже в лоадауте) · суб-фундамент баса")
pdf.check("OTT остаётся — он бесплатный и топ одновременно, Depth 10–25%")
pdf.check("SubLab XL вместо bx_subsynth из бонуса: синтезирует суб 40–60 Гц под найденный бас-слой, слой X-Sub по тону")
pdf.why("SubLab — стандарт хип-хоп продюсеров для суба; у нас — страховка, если бас-слой окажется худым внизу")

# ============ ВОКАЛ ============
pdf.part("ВОКАЛ")

pdf.plug("Waves Clarity Vx Pro", "чистка лида — ДО или вместо RX De-noise (слот 0)")
pdf.img("top-clarityvx.png", w=115)
pdf.check("Нейросеть Broad ECO · главная ручка Ambience↔Voice на 30–50% · Process Amount по вкусу")
pdf.check("Реалтайм! Не надо офлайн-рендерить — но RX оставить для хирургии (клики, пластика)")
pdf.check("Reflections — отдельно убирает отражения комнаты (лёгкий де-рум для вокала)")
pdf.why("нейро-чистка в реальном времени: слышишь результат сразу в миксе. RX — скальпель, Clarity — волшебная губка")

pdf.plug("LiquidSonics Seventh Heaven", "FX-канал VERB PLATE — вместо обычного плейта")
pdf.img("top-7heaven.png", w=115)
pdf.check("Это эмуляция Bricasti M7 — ревер за $4000 из всех топ-студий")
pdf.check("Пресет: Vocal Plate или Sunset Chamber · Decay 1.2–1.5 s · pre-delay 40 ms как у нас")
pdf.check("После него тот же Pro-Q: HPF 200 / LPF 8k — правило фильтрованного ревера не отменяется")
pdf.why("хвост М7 'дорогой' сам по себе: плотный, тёмный, не мылит. Разница с обычным плейтом слышна за секунду")

pdf.plug("Soundtoys EchoBoy", "FX-канал DLY 8TH — вместо обычного delay")
pdf.img("top-echoboy.png", w=120)
pdf.check("Style: Studio Tape (тёплые повторы) · Note 1/8 dotted · Feedback ~30% · LowCut/HighCut внутри")
pdf.check("ФИШКА ДЛЯ НАС: ручки Groove (Shuffle/Swing) и Feel (Rushin/Draggin) — повторы свингуют с грувом!")
pdf.why("король дилеев 15 лет подряд: 30 стилей железа внутри. Groove-ручка = буквально название нашего жанра")

# ============ КЛЕЙ И ДАКИНГ ============
pdf.part("КЛЕЙ, ДАКИНГ, МАСТЕР-ШИНА")

pdf.plug("Wavesfactory Trackspacer", "вместо duck-компрессоров на GTR и SYNTH (SC от VOX)")
pdf.img("top-trackspacer.png", w=80)
pdf.check("Инсерт на GTR, сайдчейн с вокала (в Cubase: кнопка SC + посыл с VOX как обычно)")
pdf.check("Amount 30–40% · Low-Cut 200 (низ гитар не трогаем) · High-Cut 8k")
pdf.check("То же на SYNTH · GR-эквивалент крошечный, но вокал вдруг 'сел' идеально")
pdf.why("не просто приглушает — вырезает РОВНО те 32 полосы, где сейчас звучит вокал. Авто-карман в реальном времени")

pdf.plug("Black Box HG-2MS (Brainworx)", "MIX BUS — сатурация вместо/рядом с плёнкой")
pdf.img("top-hg2.png", w=100)
pdf.check("Pentode чуть-чуть (плотность) · Triode по вкусу (тепло) · Density 2–4")
pdf.check("MS-версия: сатурировать можно только Mid (центр жирнее) или только Side (края шире)")
pdf.check("Air Density на Side +1–2 — ширина без фазовых трюков")
pdf.why("лампа с мастеринг-студий: 'дорогая' плотность на шине, которой не добиться эквалайзером")

# ============ ТАБЛИЦА ============
pdf.part("СВОДНАЯ: слот → было → моднюче → бесплатно")
pdf.ln(1)
pdf.row("Слот", "Моднючий топ", "Бесплатно/бюджет", head=True)
pdf.row("Гейты барабанов", "Oxford Drum Gate 2", "Cubase Gate + SC-фильтр")
pdf.row("EQ каналов", "Kirchhoff-EQ / Pro-Q 4", "TDR Nova / Frequency")
pdf.row("Drum bus комп", "Shadow Hills (Nickel)", "Cubase Bus Comp + Magneto II")
pdf.row("Авто-чистка каши", "Gullfoss", "soothe2 (у нас есть) / TDR Nova")
pdf.row("Бас-комп", "Pulsar Mu", "Cubase Tube Compressor")
pdf.row("Суб-страховка", "SubLab XL", "RBass-подобные / синт заново")
pdf.row("Нейро-чистка вокала", "Clarity Vx Pro", "Bertom Denoiser / RX Elements")
pdf.row("Резонансы", "soothe2 (вне конкуренции)", "TDR Nova")
pdf.row("Ревер", "Seventh Heaven (M7)", "Valhalla VintageVerb ($50 — честный топ)")
pdf.row("Delay", "EchoBoy", "Cubase ModMachine / Valhalla Delay")
pdf.row("Дакинг под вокал", "Trackspacer", "SC-комп GR ~1 дБ (как в паспорте)")
pdf.row("Мастер-сатурация", "HG-2MS", "Cubase Magneto II")

pdf.ln(3)
pdf.goldbox("★ Золотые правила моднючего шопинга", [
    "У ВСЕХ есть демо 14–30 дней: сначала пробуем на ЭТОЙ песне, потом покупаем",
    "Параметры важнее бренда: наш микс доедет и на стоке Cubase — топы дают последние 10–15%",
    "Покупать по одному и только то, что услышали в A/B. Распродажа — не аргумент :)",
    "Порядок цепочек из паспорта не меняется: меняется только табличка на двери слота",
], 42)

pdf.output(os.path.join(BASE, "Plugin-Loadout.pdf"))
print("PDF saved")
