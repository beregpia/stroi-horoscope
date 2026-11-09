#!/usr/bin/env python3
"""Cubase-Routing-Guide.pdf: пошаговый роутинг в Cubase + реальные виды плагинов."""
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
        self.cell(0, 6, "Cubase Routing Guide · пошагово + реальные плагины",
                  new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(1)

    def footer(self):
        self.set_y(-13)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"— {self.page_no()} —", align="C")

    def h2(self, t, color=ACCENT):
        if self.get_y() > 240:
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
        if self.get_y() > 255:
            self.add_page()
        self.ln(1)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")

    def step(self, n, text):
        if self.get_y() > 262:
            self.add_page()
        y = self.get_y() + 0.6
        self.set_fill_color(*ACCENT)
        self.ellipse(16, y, 6, 6, style="F")
        self.set_xy(16, y + 0.6)
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(255, 255, 255)
        self.cell(6, 4.8, str(n), align="C")
        self.set_xy(25, y)
        self.set_font("DejaVu", "", 9.4)
        self.set_text_color(*TXT)
        self.multi_cell(168, 5.3, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1.2)

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

    def img(self, name, w=120, caption=None):
        path = os.path.join(RIMG, name)
        if not os.path.exists(path):
            return
        iw, ih = Image.open(path).size
        hh = w * ih / iw
        if hh > 110:
            w = 110 * iw / ih
            hh = 110
        extra = 5 if caption else 0
        if self.get_y() + hh + extra > 274:
            self.add_page()
        x = (210 - w) / 2
        self.image(path, x=x, w=w)
        if caption:
            self.set_font("DejaVu", "", 8)
            self.set_text_color(*GREY)
            self.cell(0, 4.5, caption, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(1.5)

    def note(self, text):
        self.set_x(18)
        self.set_font("DejaVu", "", 8.6)
        self.set_text_color(*GREY)
        self.multi_cell(174, 4.7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

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
pdf.set_y(95)
pdf.set_font("DejaVu", "B", 27)
pdf.set_text_color(*ACCENT)
pdf.cell(0, 13, "CUBASE: РОУТИНГ ПОШАГОВО", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("DejaVu", "B", 16)
pdf.set_text_color(242, 237, 228)
pdf.cell(0, 10, "+ настоящие виды плагинов с нашими настройками",
         new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(168, 157, 140)
pdf.cell(0, 7, "Компаньон к Groove-Mix-Session.pdf", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.cell(0, 7, "группы · посылы · сайдчейн · офлайн-обработка", new_x="LMARGIN", new_y="NEXT", align="C")

pdf.add_page()

# ============ ЧАСТЬ 1. РОУТИНГ ============
pdf.h2("Часть 1 · Группы: создать и направить")

pdf.h3("1.1 Создаём группы")
pdf.img("real-cubase-addtrack.png", w=85, caption="Окно Add Track → Group (официальный вид Cubase)")
pdf.step(1, "Правый клик в пустом месте списка треков → Add Track → Group (или меню Project → Add Track → Group).")
pdf.step(2, "Configuration: Stereo · Name: KICK · Add Track.")
pdf.step(3, "Повторить для всех: KICK, SNARE, DRUMS, ROOMS, GTR, SYNTH, BASS, VOX, BACKS, MIX BUS. "
            "Удобно: Count = 10 и переименовать потом (двойной клик по имени).")
pdf.note("Группы появятся в папке 'Group Tracks'. Это и есть наши шины из карты сессии.")

pdf.h3("1.2 Направляем треки в группы")
pdf.step(1, "Выделить трек → вверху Инспектора слот Output Routing (где написано Stereo Out) → выбрать группу. "
            "Kick beater и Kick front → KICK, Snare top/bottom → SNARE и т.д.")
pdf.step(2, "МАССОВО: выделить несколько треков → зажать Shift+Alt и выбрать routing у одного — применится ко всем выделенным!")
pdf.step(3, "Иерархия шин: у групп KICK, SNARE, томов/хэта/OH выставить Output → DRUMS. "
            "Room → ROOMS → DRUMS (или сразу DRUMS). Затем DRUMS, GTR, SYNTH, BASS, VOX, BACKS → MIX BUS. "
            "MIX BUS → Stereo Out. Это делается в том же слоте Output Routing у самой группы.")
pdf.step(4, "Проверка: подвиньте фейдер MIX BUS — должна тихнуть ВСЯ песня. Фейдер DRUMS — все барабаны.")

pdf.h3("1.3 FX-каналы и посылы")
pdf.img("real-cubase-channel.png", w=130, caption="Channel Settings (клик по 'e' на треке): Inserts · Strip · EQ · Sends")
pdf.step(1, "Add Track → Effect: создать VERB PLATE (плейт-ревер), DLY 8TH (delay 1/8 dotted), FAT (параллельный краш).")
pdf.step(2, "На треке: Инспектор → Sends → пустой слот → выбрать FX-канал → ВКЛЮЧИТЬ кнопкой питания → крутить уровень посыла.")
pdf.step(3, "Для параллельного краша (FAT, Devil Crush): посыл переключить в PRE-fader (правый клик по слоту → "
            "Move to Pre-Fader) и выставить уровень 0 dB — тогда баланс рулится только фейдером FX-канала.")
pdf.step(4, "Кнопка 'e' у трека открывает Channel Settings — там всё в одном окне: инсерты, EQ, посылы (картинка выше).")

pdf.h2("Часть 2 · Сайдчейн пошагово (бас приседает от бочки)")
pdf.img("real-cubase-sc.png", w=120, caption="Кнопка Side-Chain в шапке плагина (подсвечена красным)")
pdf.step(1, "На канале BASS вставить компрессор (Cubase Compressor или любой с поддержкой SC).")
pdf.step(2, "В ШАПКЕ окна плагина нажать кнопку Side-Chain (на картинке — подсвечена). Она активирует SC-вход.")
pdf.step(3, "Перейти на трек Kick front → Sends → в списке теперь есть раздел Side-Chains → выбрать 'Compressor — BASS'.")
pdf.step(4, "Включить этот посыл, уровень 0 dB. Теперь компрессор баса 'слышит' бочку.")
pdf.step(5, "Настроить по карточке: Ratio 3:1 · Attack 1 ms · Release 100 ms · Threshold до GR 2–3 дБ. "
            "Соло KICK+BASS: на каждый удар бочки бас чуть приседает — качач!")
pdf.step(6, "То же для SYNTH (GR 1–2 дБ) и Room Duck (комп на ROOMS, SC от Kick front, GR 3–4 дБ).")

pdf.h2("Часть 3 · Полезные места Cubase (для нашей сессии)")
pdf.check("F3 — MixConsole · в racks включить 'Pre' — там кнопка Ø (полярность) для Шага 1 (фазы) и фильтры HPF")
pdf.check("Direct Offline Processing (F7, меню Audio) — сюда вставлять RX-модули ОФЛАЙН: выделил клип → F7 → плагин → Apply")
pdf.check("Audio → Advanced → Detect Silence — это Strip Silence для томов (потом кроссфейды: выделить стыки → X)")
pdf.check("Инспектор → Track Delay (мс) — трюк 'отодвинуть стены' для рума (+15…30 мс)")
pdf.check("VariAudio: двойной клик по вокальному клипу → редактор → вкладка VariAudio (встроен в Cubase Pro)")
pdf.check("Констрейн задержки (кнопка с часами внизу слева / в транспорте) — выключает тяжёлые плагины при записи; "
          "для сведения должна быть ВЫКЛЮЧЕНА (т.е. компенсация работает)")

# ============ ЧАСТЬ 4. РЕАЛЬНЫЕ ПЛАГИНЫ ============
pdf.add_page()
pdf.h2("Часть 4 · Настоящие плагины + наши настройки")
pdf.note("Виды могут немного отличаться от ваших версий — важны ПАРАМЕТРЫ, а не морда. "
         "К каждому — бесплатная замена, если плагина нет.")

pdf.h3("FabFilter Pro-Q 3/4 — все наши EQ-карточки делаются тут")
pdf.img("real-proq.png", w=150, caption="Pro-Q 4: инстансы kick out / snare / snare top — как у нас!")
pdf.check("Свип бяк: создать bell, Gain +10, Q 5–6, таскать по частоте; нашли — Gain в минус (−3…−5)")
pdf.check("Динамическая полоса: потянуть за точку ВНИЗ появится dynamic range (для кольца рабочего, хэта в snare top)")
pdf.check("Бесплатно вместо: TDR Nova (тоже с динамикой!) или встроенный Frequency в Cubase Pro")

pdf.h3("iZotope RX Spectral De-noise — чистка (ОФЛАЙН!)")
pdf.img("real-rx-denoise.png", w=130, caption="1 — выделить паузу с шумом · Learn · 2 — Threshold · 3 — Reduction 6–12 дБ")
pdf.check("В RX-редакторе: выделить кусок ТОЛЬКО с шумом → Learn → Reduction 6–12 дБ → Render")
pdf.check("В Cubase: через Direct Offline Processing (F7) или ARA-расширение")
pdf.check("Бесплатно вместо: Bertom Denoiser Pro")

pdf.h3("Waves CLA-76 (это 1176) — лид-вокал ступень 1, drum smash")
pdf.img("real-cla76.png", w=120, caption="Revision Bluey/Blacky · кнопки Ratio · шкала Attack ПЕРЕВЁРНУТА: 7 = быстрее всего")
pdf.check("Лид-вокал: Ratio 4 · Attack 3 · Release 7 · Input до GR 2–4 только на пиках")
pdf.check("DRUM SMASH (параллель): нажать ВСЕ кнопки Ratio сразу (All-Buttons) · Input до GR 8–12 · фейдер −10…−6")
pdf.check("Бесплатно вместо: Analog Obsession FETish или Cubase VintageCompressor")

pdf.h3("Waves CLA-2A (это LA-2A) — лид ступень 2, бас")
pdf.img("real-cla2a.png", w=110, caption="Всего две ручки: Gain (громкость) и Peak Reduction (сколько жать)")
pdf.check("Лид после CLA-76: Peak Reduction до GR 3–5 дБ — выравнивает фразы в 'шёлк'")
pdf.check("Бас: Peak Reduction до GR 3–5 — ровная линия без убийства атаки")
pdf.check("Бесплатно вместо: Analog Obsession LALA")

pdf.h3("oeksound soothe2 — резонансы сами находятся")
pdf.img("real-soothe2.png", w=110, caption="Depth · Sharpness · Selectivity · зона работы на графике")
pdf.check("Вокал: зона 1–8k · Depth 4–6 · Sharpness 7 · кнопка DELTA — слушаем, что убирает")
pdf.check("OH/тарелки: зона 3–10k · гул бочки: зона 50–200 (да, он умеет и низ!)")
pdf.check("Бюджетно вместо: TDR Nova (динамические полосы руками)")

pdf.h3("UAD/Empirical Labs Fatso — ROOMS и жир")
pdf.img("real-fatso.png", w=130, caption="Fatso Jr/Sr: Input жмёт, Warmth греет верх, Tranny — трансформаторный жир")
pdf.check("ROOMS: режим Spank · Input до GR 4–6 дБ · Warmth 3–5 — главный качач комнаты")
pdf.check("Бюджетно вместо: Cubase Magneto II (плёнка) + компрессор, или Klanghelm MJUC")

pdf.h3("Soundtoys Devil-Loc Deluxe — Devil Crush рума")
pdf.img("real-devilloc.png", w=130, caption="Пресет 'Big Box Drums' — буквально наш случай :)")
pdf.check("Crush 5–7 · Crunch 2–3 · Darkness 3–4 · Release Slow · на ПАРАЛЛЕЛЬ, −10…−6 под основным румом")

pdf.h3("Soundtoys Decapitator — сатурация (trash mic, ковбелл, бас)")
pdf.img("real-decap.png", w=120, caption="Style A/E/N/T/P — разное железо · Punish — турбо-кнопка")
pdf.check("Trash mic: Style P · Drive 5–7 · + фильтры Low Cut/High Cut прямо в нём (200 Hz / 2.5k) · в MONO")
pdf.check("Ковбелл: Style N, Drive 2–3 · Бас: Style A, Drive 2–3, Mix 30–40%")
pdf.check("Бесплатно вместо: Softube Saturation Knob")

pdf.h3("Xfer OTT — бесплатный! Синты и бэки")
pdf.img("real-ott.png", w=85, caption="Depth — главная ручка. У нас 10–25%, НЕ 100!")
pdf.check("Depth 10–25% · Time ~150 ms · In Gain до GR 2–4 — плотность без EDM-пластика")

pdf.goldbox("★ Золотые правила этого гида", [
    "Шапка плагина в Cubase — это НЕ плагин: там Bypass, A/B, пресеты и кнопка Side-Chain",
    "Все RX-чистки — офлайн (F7), все EQ/компрессоры — инсертами, параллели — PRE-fader посылами",
    "Нет плагина — бесплатная замена рядом в каждой карточке. Звук решают ПАРАМЕТРЫ",
    "Один новый плагин за раз + A/B. Моднятина — приправа!",
], 34)

pdf.output(os.path.join(BASE, "Cubase-Routing-Guide.pdf"))
print("PDF saved")
