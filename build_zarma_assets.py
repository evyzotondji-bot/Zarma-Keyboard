import os, math
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

class ZarmaCanvas:
    def __init__(self):
        self.contours, self.svg_elements = [], []

    def rect(self, x1, y1, x2, y2):
        xa, xb, ya, yb = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        self.contours.append([(xa, ya), (xb, ya), (xb, yb), (xa, yb)])
        self.svg_elements.append(f'<rect x="{xa}" y="{1000-yb}" width="{xb-xa}" height="{yb-ya}" fill="currentColor"/>')

    def thick_line(self, x1, y1, x2, y2, w=76):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length == 0: return
        nx, ny = -dy / length * (w / 2), dx / length * (w / 2)
        pts = [(round(x1+nx), round(y1+ny)), (round(x2+nx), round(y2+ny)), (round(x2-nx), round(y2-ny)), (round(x1-nx), round(y1-ny))]
        self.contours.append(pts)
        self.svg_elements.append(f'<polygon points="{" ".join(f"{x},{1000-y}" for x,y in pts)}" fill="currentColor"/>')

    def ring(self, cx, cy, r_outer, r_inner=None, segs=36):
        if r_inner is None: r_inner = max(10, r_outer - 76)
        outer = [(round(cx + r_outer * math.cos(2*math.pi*i/segs)), round(cy + r_outer * math.sin(2*math.pi*i/segs))) for i in range(segs)]
        inner = [(round(cx + r_inner * math.cos(2*math.pi*(segs-1-i)/segs)), round(cy + r_inner * math.sin(2*math.pi*(segs-1-i)/segs))) for i in range(segs)]
        self.contours.extend([outer, inner])
        self.svg_elements.append(f'<circle cx="{cx}" cy="{1000-cy}" r="{(r_outer+r_inner)/2}" fill="none" stroke="currentColor" stroke-width="{r_outer-r_inner}"/>')

    def dot(self, cx, cy, r=55):
        self.contours.append([(round(cx + r * math.cos(2*math.pi*i/24)), round(cy + r * math.sin(2*math.pi*i/24))) for i in range(24)])
        self.svg_elements.append(f'<circle cx="{cx}" cy="{1000-cy}" r="{r}" fill="currentColor"/>')

    def u_cup(self, xl, xr, yb, yt, w=76):
        self.rect(xl, yb, xr, yb+w); self.rect(xl, yt-w, xr, yt); self.rect(xl, yb, xl+w, yt)

    def to_svg(self):
        return '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n  ' + "\n  ".join(self.svg_elements) + '\n</svg>\n'

    def draw_to_pen(self, pen):
        for pts in self.contours:
            pen.moveTo(pts[0])
            for pt in pts[1:]: pen.lineTo(pt)
            pen.closePath()

def build_all_glyphs():
    G = {}
    def new(cp, name, cat):
        c = ZarmaCanvas(); G[name] = (cp, cat, c); return c

    # 10 Voyelles minuscules (U+E000 - U+E009)
    c = new(0xE000, "v_a", "vowels"); c.u_cup(320, 680, 380, 740); c.rect(320, 200, 680, 276)
    c = new(0xE001, "v_i", "vowels"); c.u_cup(320, 680, 480, 820); c.rect(320, 330, 680, 400); c.rect(320, 190, 680, 260)
    c = new(0xE002, "v_o", "vowels"); c.u_cup(320, 680, 560, 860); c.rect(320, 430, 680, 495); c.rect(320, 300, 680, 365); c.rect(320, 170, 680, 235)
    c = new(0xE003, "v_e", "vowels"); c.rect(320, 720, 680, 796); c.u_cup(320, 680, 240, 600)
    c = new(0xE004, "v_ou", "vowels"); c.rect(320, 770, 680, 835); c.rect(320, 640, 680, 705); c.u_cup(320, 680, 200, 540)
    c = new(0xE005, "v_ai", "vowels"); c.rect(320, 720, 680, 796); c.ring(500, 410, 185)
    c = new(0xE006, "v_oi", "vowels"); c.rect(320, 770, 680, 835); c.rect(320, 640, 680, 705); c.ring(500, 380, 175)
    c = new(0xE007, "v_an", "vowels"); c.ring(500, 570, 185); c.rect(320, 200, 680, 276)
    c = new(0xE008, "v_in", "vowels"); c.ring(500, 630, 175); c.rect(320, 330, 680, 400); c.rect(320, 190, 680, 260)
    c = new(0xE009, "v_on", "vowels"); c.ring(500, 680, 160); c.rect(320, 430, 680, 495); c.rect(320, 300, 680, 365); c.rect(320, 170, 680, 235)

    # 10 Voyelles initiales (U+E00A - U+E013)
    for idx, (nm, bars) in enumerate([("V_A", 1), ("V_I", 2), ("V_O", 3)]):
        c = new(0xE00A+idx, nm, "vowels_cap"); c.rect(460, 160, 536, 840); c.rect(460, 764, 660, 840); c.rect(584, 650, 660, 840)
        for b in range(bars): c.rect(340, 220+b*110, 660, 286+b*110)
    for idx, (nm, bars) in enumerate([("V_E", 1), ("V_OU", 2)]):
        c = new(0xE00D+idx, nm, "vowels_cap"); c.rect(530, 160, 606, 840); c.ring(445, 290, 120)
        for b in range(bars): c.rect(380, 560+b*115, 680, 626+b*115)
    for idx, (nm, bars) in enumerate([("V_AI", 1), ("V_OI", 2)]):
        c = new(0xE00F+idx, nm, "vowels_cap"); c.rect(530, 160, 606, 840); c.rect(380, 160, 606, 236); c.rect(380, 160, 456, 360)
        for b in range(bars): c.rect(380, 560+b*115, 680, 626+b*115)
    for idx, (nm, bars) in enumerate([("V_AN", 1), ("V_IN", 2), ("V_ON", 3)]):
        c = new(0xE011+idx, nm, "vowels_cap"); c.rect(530, 160, 606, 840); c.ring(435, 690, 140)
        for b in range(bars): c.rect(380, 200+b*105, 680, 264+b*105)

    # 22 Consonnes + V (U+E014 - U+E02A)
    c = new(0xE014, "c_b", "letters"); c.rect(462, 380, 538, 840); c.rect(280, 360, 720, 436); c.rect(280, 180, 720, 256)
    c = new(0xE015, "c_d", "letters"); c.rect(260, 180, 740, 256); c.rect(260, 180, 336, 440); c.rect(664, 180, 740, 440); c.rect(462, 180, 538, 840); c.rect(380, 520, 620, 590)
    c = new(0xE016, "c_f", "letters"); c.rect(300, 180, 376, 560); c.rect(624, 180, 700, 560); c.rect(280, 500, 720, 576); c.thick_line(320, 820, 500, 560); c.thick_line(680, 820, 500, 560)
    c = new(0xE017, "c_g", "letters"); c.rect(462, 540, 538, 840); c.rect(340, 500, 660, 576); c.thick_line(660, 538, 340, 220); c.rect(340, 180, 680, 256)
    c = new(0xE018, "c_h", "letters"); c.rect(524, 180, 600, 840); c.rect(340, 764, 600, 840); c.rect(340, 610, 600, 686); c.thick_line(562, 200, 360, 380)
    c = new(0xE019, "c_j", "letters"); c.rect(584, 180, 660, 840); c.thick_line(620, 820, 340, 580); c.thick_line(340, 580, 620, 440)
    c = new(0xE01A, "c_k", "letters"); c.rect(420, 180, 496, 840); c.thick_line(458, 820, 300, 640); c.rect(420, 420, 720, 496); c.rect(420, 180, 720, 256)
    c = new(0xE01B, "c_l", "letters"); c.thick_line(280, 640, 540, 340); c.rect(400, 724, 720, 800); c.thick_line(700, 760, 440, 180)
    c = new(0xE01C, "c_m", "letters"); c.rect(280, 180, 356, 500); c.rect(644, 180, 720, 500); c.rect(280, 440, 720, 516); c.dot(500, 310, 55); c.rect(462, 480, 538, 840); c.rect(360, 700, 640, 760); c.rect(360, 580, 640, 640)
    c = new(0xE01D, "c_n", "letters"); c.rect(280, 180, 356, 500); c.rect(644, 180, 720, 500); c.rect(280, 440, 720, 516); c.dot(500, 310, 55); c.rect(462, 480, 538, 840); c.rect(360, 640, 640, 705)
    c = new(0xE01E, "c_p", "letters"); c.rect(584, 180, 660, 840); c.thick_line(620, 820, 320, 510); c.thick_line(320, 510, 620, 200)
    c = new(0xE01F, "c_r", "letters"); c.rect(320, 724, 680, 800); c.thick_line(660, 760, 360, 380); c.thick_line(360, 380, 480, 180)
    c = new(0xE020, "c_s", "letters"); c.rect(462, 520, 538, 840); c.rect(280, 480, 720, 550); c.rect(280, 330, 720, 400); c.rect(280, 180, 720, 250)
    c = new(0xE021, "c_t", "letters"); c.rect(340, 440, 416, 840); c.rect(584, 180, 660, 580); c.rect(340, 470, 660, 546)
    c = new(0xE022, "c_w", "letters"); c.rect(260, 180, 740, 256); c.rect(462, 180, 538, 700); c.rect(300, 664, 700, 740); c.ring(370, 610, 95, 35); c.ring(630, 610, 95, 35)
    c = new(0xE023, "c_y", "letters"); c.rect(584, 180, 660, 840); c.thick_line(620, 820, 340, 460); c.rect(340, 440, 660, 516)
    c = new(0xE024, "c_z", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360); c.thick_line(280, 780, 380, 680)
    c = new(0xE025, "c_gn", "letters"); [c.rect(x, 180, x+76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 640, 640, 705)
    c = new(0xE026, "c_ch", "letters"); [c.rect(x, 180, x+76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 700, 640, 760); c.rect(360, 580, 640, 640)
    c = new(0xE027, "c_tch", "letters"); [c.rect(x, 180, x+76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 740, 640, 795); c.rect(360, 640, 640, 695); c.rect(360, 540, 640, 595)
    c = new(0xE028, "c_dj", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360)
    c = new(0xE029, "c_nw", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360); c.dot(420, 550, 52)
    c = new(0xE02A, "c_v", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360); c.thick_line(280, 780, 380, 680); c.dot(420, 550, 52)

    # 8 Ponctuations (U+E02B - U+E032)
    c = new(0xE02B, "p_allongement", "punctuation"); c.dot(500, 500, 68)
    c = new(0xE02C, "p_fin_mot", "punctuation"); c.rect(260, 462, 660, 538); c.rect(620, 240, 696, 760)
    c = new(0xE02D, "p_point", "punctuation"); c.rect(200, 462, 440, 538); c.rect(300, 380, 366, 620); c.u_cup(440, 720, 360, 640, 70); c.rect(700, 240, 776, 760)
    c = new(0xE02E, "p_infinitif", "punctuation"); c.rect(200, 462, 440, 538); c.rect(300, 380, 366, 620); c.u_cup(440, 740, 360, 640, 70)
    c = new(0xE02F, "p_intrus", "punctuation"); c.rect(220, 540, 480, 616); c.rect(440, 440, 720, 516); c.rect(680, 300, 756, 700)
    c = new(0xE030, "p_interrogation", "punctuation"); c.thick_line(680, 740, 460, 500); c.thick_line(460, 500, 680, 260); c.dot(350, 640, 56); c.dot(350, 360, 56)
    c = new(0xE031, "p_guillemet", "punctuation"); c.rect(220, 462, 440, 538); c.ring(565, 500, 130); c.rect(695, 240, 771, 760)
    c = new(0xE032, "p_doute", "punctuation"); c.rect(220, 462, 460, 538); c.rect(320, 380, 386, 620); c.ring(600, 500, 140)

    # 14 Chiffres/Multiplicateurs (U+E033 - U+E040)
    c = new(0xE033, "n_0", "numbers"); c.rect(260, 565, 740, 640); c.rect(260, 360, 740, 435); c.thick_line(320, 260, 680, 740)
    c = new(0xE034, "n_1", "numbers"); c.rect(320, 740, 680, 815); c.rect(462, 180, 538, 640); c.rect(320, 380, 680, 455)
    c = new(0xE035, "n_2", "numbers"); c.thick_line(320, 780, 680, 360); c.thick_line(680, 780, 320, 360); c.rect(260, 180, 740, 256)
    c = new(0xE036, "n_3", "numbers"); c.rect(320, 180, 396, 820); c.rect(320, 744, 700, 820); c.rect(320, 462, 700, 538); c.rect(320, 180, 700, 256)
    c = new(0xE037, "n_4", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.dot(550, 520, 65)
    c = new(0xE038, "n_5", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.rect(440, 480, 700, 556)
    c = new(0xE039, "n_6", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.rect(535, 420, 605, 680); c.rect(440, 420, 700, 490)
    c = new(0xE03A, "n_7", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.thick_line(450, 700, 690, 420, 64); c.thick_line(690, 700, 450, 420, 64)
    c = new(0xE03B, "n_8", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.rect(450, 420, 515, 720); c.rect(450, 660, 690, 720); c.rect(450, 540, 690, 600); c.rect(450, 420, 690, 480)
    c = new(0xE03C, "n_9", "numbers"); c.rect(300, 180, 376, 820); c.rect(300, 180, 720, 256); c.rect(450, 420, 515, 720); c.rect(450, 420, 690, 480); c.dot(600, 600, 50)
    c = new(0xE03D, "m_da", "numbers"); c.ring(500, 700, 130); c.rect(462, 180, 538, 820); c.rect(340, 420, 660, 490); c.rect(320, 180, 680, 250)
    c = new(0xE03E, "m_zangou", "numbers"); c.rect(340, 180, 416, 820); c.rect(584, 180, 660, 820); c.rect(340, 180, 660, 256); c.rect(240, 380, 760, 456)
    c = new(0xE03F, "m_zambar", "numbers"); c.rect(340, 180, 416, 820); c.rect(584, 180, 660, 820); c.rect(340, 180, 660, 256); c.rect(240, 520, 760, 590); c.rect(240, 340, 760, 410)
    c = new(0xE040, "m_hawari", "numbers"); c.rect(340, 180, 416, 820); c.rect(584, 180, 660, 820); c.rect(340, 180, 660, 256); c.rect(240, 620, 760, 685); c.rect(240, 460, 760, 525); c.rect(240, 300, 760, 365)

    # 15 Mots abrégés ELDAS (U+E041 - U+E04F)
    c = new(0xE041, "abbr_da", "abbreviations"); c.ring(500, 660, 130); c.thick_line(430, 560, 300, 200); c.thick_line(570, 560, 700, 200)
    c = new(0xE042, "abbr_boro", "abbreviations"); c.ring(500, 680, 140); c.rect(462, 180, 538, 550)
    c = new(0xE043, "abbr_si", "abbreviations"); c.ring(500, 360, 160); c.rect(462, 180, 538, 820); c.rect(462, 744, 720, 820)
    c = new(0xE044, "abbr_ga", "abbreviations"); c.rect(280, 724, 720, 800); c.thick_line(400, 724, 280, 200); c.thick_line(600, 724, 720, 200)
    c = new(0xE045, "abbr_go", "abbreviations"); c.ring(480, 640, 150); c.rect(340, 440, 660, 516); c.thick_line(440, 440, 640, 200)
    c = new(0xE046, "abbr_ya", "abbreviations"); c.thick_line(300, 780, 500, 460); c.thick_line(700, 780, 500, 460); c.ring(500, 320, 140)
    c = new(0xE047, "abbr_dey", "abbreviations"); c.rect(320, 340, 396, 780); c.rect(604, 340, 680, 780); c.rect(320, 340, 680, 416); c.rect(240, 540, 760, 616); c.rect(462, 200, 538, 360)
    c = new(0xE048, "abbr_haya", "abbreviations"); c.ring(340, 500, 140); c.thick_line(480, 720, 760, 280); c.thick_line(760, 720, 480, 280)
    c = new(0xE049, "abbr_don", "abbreviations"); c.rect(260, 320, 336, 680); c.rect(664, 320, 740, 680); c.rect(260, 320, 740, 396); c.rect(380, 480, 620, 556); c.rect(462, 200, 538, 520)
    c = new(0xE04A, "abbr_yadine", "abbreviations"); c.rect(462, 180, 538, 820); c.ring(500, 500, 170); c.rect(462, 744, 700, 820); c.rect(300, 180, 538, 256)
    c = new(0xE04B, "abbr_haifo", "abbreviations"); c.ring(500, 500, 130); c.thick_line(240, 720, 420, 540); c.thick_line(240, 280, 420, 460); c.thick_line(760, 720, 580, 540); c.thick_line(760, 280, 580, 460)
    c = new(0xE04C, "abbr_haikoul", "abbreviations"); c.ring(500, 500, 130); c.thick_line(300, 800, 460, 600); c.thick_line(700, 800, 540, 600); c.thick_line(300, 200, 460, 400); c.thick_line(700, 200, 540, 400)
    c = new(0xE04D, "abbr_zanga", "abbreviations"); c.rect(260, 260, 740, 336); c.rect(260, 260, 336, 520); c.rect(664, 260, 740, 520); c.dot(500, 480, 65)
    c = new(0xE04E, "abbr_kan", "abbreviations"); c.rect(280, 640, 520, 716); c.rect(462, 300, 538, 716); c.rect(462, 300, 720, 376); c.rect(644, 300, 720, 540)
    c = new(0xE04F, "abbr_ik", "abbreviations"); c.rect(340, 180, 416, 820); c.thick_line(416, 500, 680, 780); c.thick_line(416, 500, 680, 220)
    return G

if __name__ == "__main__":
    glyphs = build_all_glyphs()
    for name, (cp, cat, canvas) in glyphs.items():
        os.makedirs(f"svg/{cat}", exist_ok=True)
        with open(f"svg/{cat}/{name}_U{cp:04X}.svg", "w", encoding="utf-8") as f: f.write(canvas.to_svg())
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder([".notdef", "space"] + list(glyphs.keys()))
    cmap = {0x0020: "space"}
    for name, (cp, _, _) in glyphs.items(): cmap[cp] = name
    fb.setupCharacterMap(cmap)
    pen_dict = {"space": TTGlyphPen(None).glyph()}
    nd = TTGlyphPen(None); nd.moveTo((100,0)); nd.lineTo((100,800)); nd.lineTo((500,800)); nd.lineTo((500,0)); nd.closePath()
    pen_dict[".notdef"] = nd.glyph()
    for name, (_, _, canvas) in glyphs.items():
        pen = TTGlyphPen(None); canvas.draw_to_pen(pen); pen_dict[name] = pen.glyph()
    fb.setupGlyf(pen_dict)
    metrics = {".notdef": (600, 100), "space": (350, 0)}
    for name in glyphs: metrics[name] = (920, 80)
    fb.setupHorizontalMetrics(metrics); fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({"familyName": "Zarma Eldas", "styleName": "Regular", "uniqueFontIdentifier": "ZarmaEldas-2.0", "fullName": "Zarma Eldas Regular", "version": "Version 2.0", "psName": "ZarmaEldas-Regular"})
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120); fb.setupPost()
    for out in ["font/ZarmaEldas.ttf", "android/app/src/main/assets/fonts/ZarmaEldas.ttf", "windows/ZarmaEldas.ttf"]:
        os.makedirs(os.path.dirname(out), exist_ok=True); fb.save(out)
    print(f"[OK] {len(glyphs)} SVG + ZarmaEldas.ttf v2.0 générés.")
