#!/usr/bin/env python3
"""PDF-чеклист: сведение барабанов BFD3 для рока в Cubase (fpdf2)."""
from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

DARK = (28, 30, 38)
ACCENT = (240, 130, 40)
BLUE = (52, 120, 246)
PURPLE = (140, 90, 220)
RED = (220, 60, 80)
GREY = (105, 110, 122)
TXT = (35, 38, 46)


class PDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("DejaVu", "", DEJAVU + "DejaVuSans.ttf")
        self.add_font("DejaVu", "B", DEJAVU + "DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", DEJAVU + "DejaVuSans.ttf")
        self.set_auto_page_break(True, margin=18)
        self.set_margins(16, 16, 16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, "BFD3 → Cubase · чеклист сведения барабанов для рока",
                  new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(2)

    def footer(self):
        self.set_y(-14)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"— {self.page_no()} —", align="C")

    def stage(self, num, title, color=ACCENT):
        if self.get_y() > 255:
            self.add_page()
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*color)
        self.rect(16, y, 11, 8, style="F")
        self.set_xy(16, y)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(255, 255, 255)
        self.cell(11, 8, str(num), align="C")
        self.set_xy(30, y)
        self.set_font("DejaVu", "B", 12.5)
        self.set_text_color(*TXT)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*color)
        self.set_line_width(0.5)
        self.line(16, self.get_y() + 0.5, 194, self.get_y() + 0.5)
        self.ln(3)

    def sub(self, title, color=BLUE):
        if self.get_y() > 262:
            self.add_page()
        self.ln(1.5)
        self.set_font("DejaVu", "B", 10.5)
        self.set_text_color(*color)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def check(self, text, indent=0):
        x0 = 18 + indent
        self.set_x(x0)
        y = self.get_y() + 1.1
        self.set_draw_color(*GREY)
        self.set_line_width(0.35)
        self.rect(x0, y, 3.6, 3.6)
        self.set_x(x0 + 6)
        self.set_font("DejaVu", "", 9.5)
        self.set_text_color(*TXT)
        self.multi_cell(188 - x0, 5.4, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.6)

    def note(self, text):
        self.set_x(20)
        self.set_font("DejaVu", "I", 8.8)
        self.set_text_color(*GREY)
        self.multi_cell(168, 4.8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


pdf = PDF()

# ================= Титул =================
pdf.add_page()
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 74, style="F")
pdf.set_fill_color(*ACCENT)
pdf.rect(0, 74, 210, 1.8, style="F")
pdf.set_xy(16, 16)
pdf.set_font("DejaVu", "B", 26)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, "Сведение барабанов BFD3", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(16)
pdf.cell(0, 12, "для рок-музыки в Cubase", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_x(16)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(200, 205, 215)
pdf.cell(0, 7, "Пошаговый чеклист: мультивыход → группы → Drum Bus", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(16)
pdf.set_font("DejaVu", "", 9)
pdf.set_text_color(150, 156, 170)
pdf.cell(0, 6, "Все значения — стартовые точки. Финальное слово — за ушами и референсом.",
         new_x="LMARGIN", new_y="NEXT")

pdf.set_y(84)

# ================= Этап 0 =================
pdf.stage(0, "Подготовка в BFD3", PURPLE)
pdf.check("Выбран рок-кит: бочка 22\", металлический или глубокий деревянный рабочий")
pdf.check("Damping: бочка — побольше (убрать гул), рабочий — умеренно (не пересушить)")
pdf.check("Tuning: рабочий чуть вверх для панча; томы не конфликтуют между собой")
pdf.check("Bleed: бочка и рабочий ≈ −7 дБ, томы −10…−12 дБ — но НЕ в ноль")
pdf.check("Vel Dyn: бочка/рабочий/томы ≈ +77%, хэт и тарелки — 100%")
pdf.check("Встроенные эффекты BFD3 (EQ, компрессоры) выключены — всё делаем в Cubase")
pdf.check("Ambient-каналы (OH, Room, Amb) оставлены включёнными")
pdf.check("Лишние микрофоны (Sub Kick, Snare Top 2, Cym'ы) — mute")

# ================= Этап 1 =================
pdf.stage(1, "Мультивыход BFD3 → Cubase", BLUE)
pdf.check("В микшере BFD3 каналы разведены по выходам: Kick In→1, Kick Out→2, "
          "Snare Top→3, Snare Bottom→4, Hi-Hat→5, Toms→6–8, OH→St 2, "
          "Room→St 3, Amb→St 4 · все фейдеры 0.00")
pdf.check("Cubase: F11 → правый клик по BFD3 → Activate Outputs → включены все выходы")
pdf.check("Моно-источники выведены в моно, амбиент — в стерео")
pdf.check("Панорама: бочка/рабочий в центр, хэт ~30–40% вбок, томы веером; "
          "направление томов совпадает с картиной в OH")

# ================= Этап 2 =================
pdf.stage(2, "Структура групп в Cubase", ACCENT)
pdf.check("Созданы группы (ВСЕ СТЕРЕО): KICK, SNARE, TOMS, ROOMS, DRUM BUS")
pdf.check("Все группы и прямые каналы (Hi-Hat, OH) направлены в DRUM BUS")
pdf.check("Созданы FX-каналы: Drum Verb (реверб) и Smash (параллельная компрессия)")
pdf.note("Полная схема роутинга — на последней странице.")

# ================= Этап 3 =================
pdf.stage(3, "Gain staging и фаза", RED)
pdf.check("Пики каналов около −18…−12 dBFS, фейдеры на 0")
pdf.check("Snare Bottom: полярность перевёрнута (MixConsole → Pre → ø) — "
          "проверено на слух вместе со Snare Top")
pdf.check("Kick In vs Kick Out: выбрана полярность, при которой больше низа")
pdf.check("Соло OH + бочка + рабочий: низ не «худеет» при добавлении OH")

# ================= Этап 4 =================
pdf.stage(4, "Поканальная обработка", ACCENT)
pdf.note("Принцип: EQ и гейты — на КАНАЛАХ (чиним каждый микрофон отдельно). "
         "Компрессия и сатурация — на ГРУППАХ (обрабатываем барабан как целое).")

pdf.sub("Бочка (группа KICK)")
pdf.check("[канал Kick In] EQ: HPF 35–40 Гц · вырез −4…−6 дБ @ 300–450 Гц · +3…+5 дБ @ 3–5 кГц", 4)
pdf.check("[канал Kick In] Gate — если мешает bleed", 4)
pdf.check("[канал Kick Out] EQ: +2…+4 дБ @ 50–60 Гц · LPF 8–10 кГц", 4)
pdf.check("[группа KICK] Comp 4:1, Attack 20–30 мс (пропустить щелчок!), Release 50–100 мс/Auto, GR 3–5 дБ", 4)
pdf.check("[группа KICK] По вкусу: Magneto III, Saturation 20–30%", 4)

pdf.sub("Рабочий (группа SNARE)")
pdf.check("[канал Top] EQ: HPF 70–90 Гц · +2…+4 дБ @ 150–250 Гц · −3…−5 дБ @ 400–600 Гц · +3 дБ @ 4–6 кГц", 4)
pdf.check("[канал Bottom] ø! · HPF 300–400 Гц (только пружина), фейдер на −6…−10 дБ ниже Top", 4)
pdf.check("[группа SNARE] Comp 4:1, Attack 10–20 мс, Release 80–150 мс, GR 4–6 дБ", 4)
pdf.check("[группа SNARE] Для агрессии: второй быстрый комп (1176-стиль), GR 2–3 дБ", 4)
pdf.check("[группа SNARE] EnvelopeShaper: Attack +2…+4 дБ, если не хватает щелчка", 4)
pdf.check("[группа SNARE] Send → Drum Verb", 4)

pdf.sub("Томы (группа TOMS)")
pdf.check("[каждый том] Gate: Attack мин., Hold 100–200 мс, Release 200–400 мс", 4)
pdf.check("[каждый том] EQ: HPF 50–60 Гц (флор) / 70–80 Гц (альты) · −4 дБ @ 300–500 Гц · +3 дБ @ 4–6 кГц", 4)
pdf.check("[группа TOMS] Comp 4:1, Attack 20 мс, GR 3–4 дБ · Send → Drum Verb", 4)

pdf.sub("Хэт")
pdf.check("HPF 200–300 Гц; при резкости — узкий вырез или динамический EQ @ 3–4 кГц", 4)

pdf.sub("Оверхеды (OH)")
pdf.check("Выбран подход: «только тарелки» (HPF 400–500 Гц, плотный современный рок) "
          "или «полная картина» (HPF 100–150 Гц, живой винтажный рок)", 4)
pdf.check("Шелф +1–2 дБ выше 10 кГц (воздух); при жёстких тарелках — динам. EQ 3–5 кГц", 4)
pdf.check("Компрессия лёгкая (2:1, GR 1–2 дБ) или отсутствует", 4)

pdf.sub("Room / Amb (группа ROOMS) — «размер» барабанов")
pdf.check("Компрессор: Ratio 8:1–20:1, Attack/Release быстрые, GR 10+ дБ — пусть качает", 4)
pdf.check("По вкусу: Magneto III / Distortion для грязи", 4)
pdf.check("Фейдер вкачен под микс: от «чуть воздуха» до «стадионного грохота»", 4)

# ================= Этап 5 =================
pdf.stage(5, "Параллельная компрессия (Smash)", PURPLE)
pdf.check("Send'ы с KICK, SNARE, TOMS → FX Smash (пост-фейдер, 0 дБ)")
pdf.check("Комп: Ratio 10:1+, Attack минимальный, Release быстрый, GR 10–15 дБ")
pdf.check("EQ на Smash: +3 дБ @ 100 Гц и @ 8 кГц")
pdf.check("Фейдер Smash поднят с −∞ до плотности (обычно −10…−6 дБ от основного)")

# ================= Этап 6 =================
pdf.stage(6, "Реверберация (Drum Verb)", PURPLE)
pdf.check("REVerence (Plate/Studio Room) или RoomWorks · plate 1.2–1.8 с (короче для быстрых темпов)")
pdf.check("На ревербе: HPF 300 Гц + LPF 8 кГц")
pdf.check("Pre-delay 20–40 мс — отделяет хвост от удара, панч сохраняется")
pdf.check("Бочка в реверб не идёт (или совсем чуть-чуть)")

# ================= Этап 7 =================
pdf.stage(7, "Драм-бас (DRUM BUS)", RED)
pdf.check("Glue-комп (SSL-стиль): 2:1–4:1, Attack 10–30 мс, Release Auto/0.1 с, GR всего 1–3 дБ")
pdf.check("Сатурация: Magneto III, Saturation 15–25%")
pdf.check("Финальный EQ: лёгкая «улыбка» +1–1.5 дБ @ 60–80 Гц и @ 10 кГц — по необходимости")
pdf.check("Лимитер на пару дБ — если выпрыгивают пики томов")

# ================= Этап 8 =================
pdf.stage(8, "Финальные штрихи", BLUE)
pdf.check("Автоматизация: ROOMS и Drum Verb +1.5–2 дБ в припевах — припев «раскрывается»")
pdf.check("Velocity/humanize в Groove-редакторе BFD3 (особенно на хэте)")
pdf.check("Баланс от бочки: бочка → рабочий (примерно поровну) → OH → остальное")
pdf.check("Сравнение с референсом на одинаковой громкости")
pdf.check("Проверка в моно (Control Room) — фазовые проблемы OH вылезут сразу")

# ================= Ошибки =================
pdf.ln(2)
if pdf.get_y() > 215:
    pdf.add_page()
y = pdf.get_y()
pdf.set_fill_color(253, 240, 240)
pdf.set_draw_color(*RED)
pdf.set_line_width(0.4)
pdf.rect(16, y, 178, 46, style="DF")
pdf.set_xy(22, y + 4)
pdf.set_font("DejaVu", "B", 11)
pdf.set_text_color(*RED)
pdf.cell(0, 6, "Типичные ошибки", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("DejaVu", "", 9.3)
pdf.set_text_color(*TXT)
for e in ["Сведение стереовыхода BFD3 вместо мультивыхода",
          "Забытая полярность Snare Bottom",
          "Слишком быстрая атака компрессора на бочке/рабочем — убивает панч",
          "Полностью вырезанный bleed — «мёртвый», пластиковый звук",
          "Реверб без HPF — каша в нижней середине"]:
    pdf.set_x(22)
    pdf.cell(0, 5.9, "✗  " + e, new_x="LMARGIN", new_y="NEXT")

# ================= Pro Plugins =================
pdf.add_page()
pdf.stage("★", "Pro Edition: цепочки на топовых плагинах", (180, 140, 30))
pdf.note("Альтернатива стоковым плагинам Cubase. В квадратных скобках — куда ставить: "
         "[канал ...] = отдельный канал BFD3, [группа ...] = групповой трек. "
         "Порядок в списке = порядок в цепочке.")

pdf.sub("Бочка (KICK)")
pdf.check("[канал Kick In] EQ: FabFilter Pro-Q 4 — HPF 35 Гц · динам. вырез 300–450 Гц · +4 дБ @ 4 кГц", 4)
pdf.check("[канал Kick In] Гейт: FabFilter Pro-G (режим Punch)", 4)
pdf.check("[канал Kick Out] EQ: Pro-Q 4 — +3.5 дБ @ 55 Гц · −3 дБ @ 250 Гц · LPF 9 кГц", 4)
pdf.check("[канал Kick Out] Суб: Waves Submarine / RBass @ 40–50 Гц — чуть-чуть (опционально)", 4)
pdf.check("[группа KICK] Консоль: bx_console SSL 4000 E / Waves SSL EV2 — лёгкий драйв входа", 4)
pdf.check("[группа KICK] Комп: UAD/Arturia 1176 или Distressor/Arousor — 4:1, Attack медленный (3 у 1176 — шкала обратная!), GR 3–5 дБ", 4)
pdf.check("[группа KICK] Грязь: Soundtoys Decapitator — стиль A (Ampex), Drive 2–3, Mix 30–50%", 4)

pdf.sub("Рабочий (SNARE)")
pdf.check("[канал Snare Top] bx_console SSL E — гейт + EQ в одном, классика рока", 4)
pdf.check("[канал Snare Top] Pro-Q 4: динамический вырез 400–600 Гц (кольцо давится только на ударах)", 4)
pdf.check("[канал Snare Top] oeksound soothe2 — если «звенит» неприятной серединой", 4)
pdf.check("[канал Snare Btm] полярность ø! · HPF 350 Гц · фейдер −8 дБ ниже Top", 4)
pdf.check("[группа SNARE] CLA-76 / UAD 1176: Attack 3–4, Release 7 (быстрый), GR 3–5 дБ", 4)
pdf.check("[группа SNARE] Decapitator: стиль N (Neve) — тепло, стиль A — злость", 4)
pdf.check("[группа SNARE] Smack Attack / SPL Transient Designer — если мало щелчка", 4)

pdf.sub("Томы (TOMS)")
pdf.check("[каждый том] Pro-G (Punch) → EQ → Transient Designer (Attack +4, Sustain −2)", 4)
pdf.check("[группа TOMS] Pro-C 2 / комп: 4:1, Attack 20 мс, GR 3–4 дБ", 4)

pdf.sub("Оверхеды (OH)")
pdf.check("soothe2 — мягко давит резкость тарелок 3–6 кГц (главный секрет современных миксов)", 4)
pdf.check("UAD LA-2A — GR 1–2 дБ, просто «склеивает»", 4)
pdf.check("Maag EQ4 / Kush Clariphonic — Air band +2 дБ @ 20 кГц — дорогой «воздух»", 4)

pdf.sub("Rooms (ROOMS)")
pdf.check("Distressor (NUKE) или UAD Fatso (Spank) — легендарное рум-разрушение", 4)
pdf.check("Soundtoys Devil-Loc Deluxe: Crush 3–5 — стадионный грохот одной ручкой", 4)
pdf.check("Decapitator: стиль P (Pultec), Drive 4+", 4)

pdf.sub("Параллельная шина (Smash)")
pdf.check("CLA-76 / UAD 1176 в режиме All-Buttons-In — тот самый взрывной NY-звук", 4)

pdf.sub("Реверб (Drum Verb)")
pdf.check("Valhalla VintageVerb (Plate 1.4 с) — лучшая цена/качество", 4)
pdf.check("UAD EMT 140 — классическая пластина · LiquidSonics Seventh Heaven (Bricasti M7) — топ", 4)

pdf.sub("Drum Bus")
pdf.check("Cytomic The Glue / SSL Native Bus Comp 2: 4:1, Attack 10–30 мс, Auto, GR 1–3 дБ", 4)
pdf.check("Shadow Hills Mastering Comp — «дорогой» железный клей (по желанию)", 4)
pdf.check("FabFilter Saturn 2: Warm Tape, Drive 2–4 дБ", 4)
pdf.check("FabFilter Pro-L 2: Transparent, ловит пики", 4)
pdf.note("Бюджетные заменители: TDR Nova (динамический EQ), TDR Kotelnikov (glue), "
         "Analog Obsession — бесплатные эмуляции 1176/SSL/Fatso.")

# ================= Схема =================
pdf.add_page()
pdf.set_font("DejaVu", "B", 14)
pdf.set_text_color(*TXT)
pdf.cell(0, 9, "Схема роутинга", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.image(os.path.join(BASE, "routing-diagram.png"), x=16, w=178)

pdf.output(os.path.join(BASE, "BFD3-Rock-Drums-Checklist.pdf"))
print("PDF saved")
