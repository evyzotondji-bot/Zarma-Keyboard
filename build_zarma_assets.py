import os, math
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

class ZarmaCanvas:
    def __init__(self):
        self.contours, self.svg_elements = [], []

    def stroke_poly(self, raw_pts, w=66):
        pts = [raw_pts[0]]
        for p in raw_pts[1:]:
            if math.hypot(p[0]-pts[-1][0], p[1]-pts[-1][1]) >= 2.0:
                pts.append(p)
        if len(pts) < 2: return
        hw = w / 2.0
        left, right = [], []
        for i, (x, y) in enumerate(pts):
            dx, dy = (pts[1][0]-x, pts[1][1]-y) if i == 0 else ((x-pts[-2][0], y-pts[-2][1]) if i == len(pts)-1 else (pts[i+1][0]-pts[i-1][0], pts[i+1][1]-pts[i-1][1]))
            ln = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / ln * hw, dx / ln * hw
            left.append((round(x + nx), round(y + ny)))
            right.append((round(x - nx), round(y - ny)))
        ex, ey = pts[-1]
        ae = math.atan2(left[-1][1]-ey, left[-1][0]-ex)
        ecap = [(round(ex + hw*math.cos(ae - math.pi*k/8)), round(ey + hw*math.sin(ae - math.pi*k/8))) for k in range(1, 8)]
        sx, sy = pts[0]
        as_ = math.atan2(right[0][1]-sy, right[0][0]-sx)
        scap = [(round(sx + hw*math.cos(as_ - math.pi*k/8)), round(sy + hw*math.sin(as_ - math.pi*k/8))) for k in range(1, 8)]
        poly = left + ecap + list(reversed(right)) + scap
        clean = [poly[0]]
        for p in poly[1:]:
            if p != clean[-1]: clean.append(p)
        if len(clean) >= 3:
            self.contours.append(clean)
            self.svg_elements.append(f'<polygon points="{" ".join(f"{x},{1000-y}" for x,y in clean)}" fill="currentColor"/>')

    def line(self, x1, y1, x2, y2, w=66):
        self.stroke_poly([(x1, y1), (x2, y2)], w)

    def quad(self, x0, y0, cx, cy, x1, y1, w=66, steps=22):
        pts = [((1-t)**2*x0 + 2*(1-t)*t*cx + t**2*x1, (1-t)**2*y0 + 2*(1-t)*t*cy + t**2*y1) for t in (i/steps for i in range(steps+1))]
        self.stroke_poly(pts, w)

    def arc(self, cx, cy, rx, ry, deg0, deg1, w=66, steps=26):
        pts = [(cx + rx*math.cos(math.radians(deg0 + (deg1-deg0)*i/steps)), cy + ry*math.sin(math.radians(deg0 + (deg1-deg0)*i/steps))) for i in range(steps+1)]
        self.stroke_poly(pts, w)

    def oval(self, cx, cy, rx, ry, w=64, segs=36):
        hw = w / 2.0
        outer = [(round(cx + (rx+hw)*math.cos(2*math.pi*i/segs)), round(cy + (ry+hw)*math.sin(2*math.pi*i/segs))) for i in range(segs)]
        inner = [(round(cx + max(8, rx-hw)*math.cos(2*math.pi*(segs-1-i)/segs)), round(cy + max(8, ry-hw)*math.sin(2*math.pi*(segs-1-i)/segs))) for i in range(segs)]
        self.contours.extend([outer, inner])
        self.svg_elements.append(f'<ellipse cx="{cx}" cy="{1000-cy}" rx="{rx}" ry="{ry}" fill="none" stroke="currentColor" stroke-width="{w}"/>')

    def dot(self, cx, cy, r=52):
        self.contours.append([(round(cx + r*math.cos(2*math.pi*i/24)), round(cy + r*math.sin(2*math.pi*i/24))) for i in range(24)])
        self.svg_elements.append(f'<circle cx="{cx}" cy="{1000-cy}" r="{r}" fill="currentColor"/>')

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

    # 10 Voyelles minuscules curvilignes (U+E800 - U+E809)
    c = new(0xE800, "v_a", "vowels"); c.arc(540, 560, 175, 175, 85, 275); c.quad(340, 240, 500, 215, 660, 240, 62)
    c = new(0xE801, "v_i", "vowels"); c.arc(540, 630, 165, 160, 85, 275); c.quad(340, 355, 500, 335, 660, 355, 58); c.quad(340, 220, 500, 200, 660, 220, 58)
    c = new(0xE802, "v_o", "vowels"); c.arc(540, 690, 155, 145, 85, 275); c.quad(340, 445, 500, 430, 660, 445, 56); c.quad(340, 320, 500, 305, 660, 320, 56); c.quad(340, 195, 500, 180, 660, 195, 56)
    c = new(0xE803, "v_e", "vowels"); c.quad(340, 760, 500, 785, 660, 760, 62); c.arc(540, 430, 175, 175, 85, 275)
    c = new(0xE804, "v_ou", "vowels"); c.quad(340, 795, 500, 815, 660, 795, 58); c.quad(340, 665, 500, 685, 660, 665, 58); c.arc(540, 370, 165, 160, 85, 275)
    c = new(0xE805, "v_ai", "vowels"); c.quad(340, 760, 500, 785, 660, 760, 62); c.oval(500, 420, 165, 165, 62)
    c = new(0xE806, "v_oi", "vowels"); c.quad(340, 795, 500, 815, 660, 795, 58); c.quad(340, 665, 500, 685, 660, 665, 58); c.oval(500, 380, 155, 155, 58)
    c = new(0xE807, "v_an", "vowels"); c.oval(500, 580, 165, 165, 62); c.quad(340, 240, 500, 215, 660, 240, 62)
    c = new(0xE808, "v_in", "vowels"); c.oval(500, 640, 155, 155, 58); c.quad(340, 355, 500, 335, 660, 355, 58); c.quad(340, 220, 500, 200, 660, 220, 58)
    c = new(0xE809, "v_on", "vowels"); c.oval(500, 690, 145, 145, 56); c.quad(340, 445, 500, 430, 660, 445, 56); c.quad(340, 320, 500, 305, 660, 320, 56); c.quad(340, 195, 500, 180, 660, 195, 56)

    # 10 Voyelles initiales curvilignes (U+E80A - U+E813)
    for idx, (nm, bars) in enumerate([("V_A", 1), ("V_I", 2), ("V_O", 3)]):
        c = new(0xE80A+idx, nm, "vowels_cap"); c.line(480, 180, 480, 760); c.arc(570, 750, 90, 95, 0, 180)
        for b in range(bars): c.quad(350, 240+b*110, 500, 220+b*110, 650, 240+b*110, 58)
    for idx, (nm, bars) in enumerate([("V_E", 1), ("V_OU", 2)]):
        c = new(0xE80D+idx, nm, "vowels_cap"); c.line(560, 180, 560, 820); c.oval(460, 290, 100, 105, 60)
        for b in range(bars): c.quad(380, 575+b*115, 530, 595+b*115, 680, 575+b*115, 58)
    for idx, (nm, bars) in enumerate([("V_AI", 1), ("V_OI", 2)]):
        c = new(0xE80F+idx, nm, "vowels_cap"); c.line(560, 270, 560, 820); c.arc(470, 275, 90, 95, 180, 360)
        for b in range(bars): c.quad(380, 575+b*115, 530, 595+b*115, 680, 575+b*115, 58)
    for idx, (nm, bars) in enumerate([("V_AN", 1), ("V_IN", 2), ("V_ON", 3)]):
        c = new(0xE811+idx, nm, "vowels_cap"); c.line(560, 180, 560, 820); c.oval(455, 690, 110, 115, 60)
        for b in range(bars): c.quad(380, 220+b*105, 530, 200+b*105, 680, 220+b*105, 56)

    # 23 Consonnes curvilignes (U+E814 - U+E82A)
    c = new(0xE814, "c_b", "letters"); c.quad(510, 820, 490, 580, 500, 390); c.quad(300, 395, 500, 355, 700, 395); c.quad(300, 220, 500, 180, 700, 220)
    c = new(0xE815, "c_d", "letters"); c.arc(500, 410, 230, 215, 185, 355); c.line(500, 195, 500, 820); c.quad(390, 560, 500, 535, 610, 560, 58)
    c = new(0xE816, "c_f", "letters"); c.arc(500, 360, 195, 195, 0, 180); c.line(305, 190, 305, 360); c.line(695, 190, 695, 360); c.quad(330, 800, 500, 520, 670, 800)
    c = new(0xE817, "c_g", "letters"); c.line(500, 560, 500, 820); c.quad(340, 540, 500, 580, 640, 530); c.quad(640, 530, 480, 380, 350, 230); c.quad(350, 230, 510, 185, 680, 225)
    c = new(0xE818, "c_h", "letters"); c.line(560, 220, 560, 820); c.quad(560, 810, 440, 835, 350, 765); c.quad(560, 650, 440, 675, 350, 605); c.quad(560, 220, 460, 240, 370, 360)
    c = new(0xE819, "c_j", "letters"); c.line(610, 190, 610, 820); c.quad(610, 800, 290, 640, 610, 460)
    c = new(0xE81A, "c_k", "letters"); c.line(450, 190, 450, 820); c.quad(450, 810, 360, 740, 310, 640); c.quad(450, 470, 740, 460, 690, 320); c.quad(690, 320, 640, 200, 450, 210)
    c = new(0xE81B, "c_l", "letters"); c.quad(290, 610, 390, 340, 530, 390); c.quad(410, 750, 690, 810, 650, 580); c.quad(650, 580, 560, 360, 440, 195)
    c = new(0xE81C, "c_m", "letters"); c.arc(500, 340, 195, 175, 0, 180); c.line(305, 190, 305, 340); c.line(695, 190, 695, 340); c.dot(500, 300, 50); c.line(500, 515, 500, 820); c.quad(370, 730, 500, 705, 630, 730, 56); c.quad(370, 610, 500, 585, 630, 610, 56)
    c = new(0xE81D, "c_n", "letters"); c.arc(500, 340, 195, 175, 0, 180); c.line(305, 190, 305, 340); c.line(695, 190, 695, 340); c.dot(500, 300, 50); c.line(500, 515, 500, 820); c.quad(370, 670, 500, 645, 630, 670, 58)
    c = new(0xE81E, "c_p", "letters"); c.line(610, 190, 610, 820); c.quad(610, 800, 250, 510, 610, 220)
    c = new(0xE81F, "c_r", "letters"); c.quad(330, 740, 540, 825, 650, 720); c.quad(650, 720, 540, 540, 380, 410); c.quad(380, 410, 330, 300, 470, 195)
    c = new(0xE820, "c_s", "letters"); c.line(500, 535, 500, 820); c.quad(300, 520, 500, 485, 700, 520, 58); c.quad(300, 370, 500, 335, 700, 370, 58); c.quad(300, 220, 500, 185, 700, 220, 58)
    c = new(0xE821, "c_t", "letters"); c.quad(370, 820, 360, 540, 500, 510); c.quad(500, 510, 640, 480, 630, 190); c.quad(340, 520, 500, 495, 660, 520, 58)
    c = new(0xE822, "c_w", "letters"); c.arc(500, 400, 230, 200, 185, 355); c.line(500, 200, 500, 710); c.quad(310, 705, 500, 735, 690, 705, 58); c.oval(375, 615, 75, 75, 50); c.oval(625, 615, 75, 75, 50)
    c = new(0xE823, "c_y", "letters"); c.line(610, 190, 610, 820); c.quad(610, 800, 360, 650, 360, 480); c.quad(360, 480, 480, 455, 610, 480)
    c = new(0xE824, "c_z", "letters"); c.quad(290, 770, 380, 710, 370, 650); c.quad(370, 650, 220, 540, 350, 410); c.quad(350, 410, 470, 300, 560, 430); c.quad(560, 430, 660, 530, 770, 380)
    c = new(0xE825, "c_gn", "letters"); c.arc(385, 340, 115, 165, 0, 180); c.arc(615, 340, 115, 165, 0, 180); c.line(270, 190, 270, 340); c.line(500, 190, 500, 820); c.line(730, 190, 730, 340); c.quad(370, 670, 500, 645, 630, 670, 58)
    c = new(0xE826, "c_ch", "letters"); c.arc(385, 340, 115, 165, 0, 180); c.arc(615, 340, 115, 165, 0, 180); c.line(270, 190, 270, 340); c.line(500, 190, 500, 820); c.line(730, 190, 730, 340); c.quad(370, 730, 500, 705, 630, 730, 56); c.quad(370, 610, 500, 585, 630, 610, 56)
    c = new(0xE827, "c_tch", "letters"); c.arc(385, 340, 115, 165, 0, 180); c.arc(615, 340, 115, 165, 0, 180); c.line(270, 190, 270, 340); c.line(500, 190, 500, 820); c.line(730, 190, 730, 340); c.quad(370, 765, 500, 745, 630, 765, 52); c.quad(370, 665, 500, 645, 630, 665, 52); c.quad(370, 565, 500, 545, 630, 565, 52)
    c = new(0xE828, "c_dj", "letters"); c.quad(370, 650, 220, 540, 350, 410); c.quad(350, 410, 470, 300, 560, 430); c.quad(560, 430, 660, 530, 770, 380)
    c = new(0xE829, "c_nw", "letters"); c.quad(370, 650, 220, 540, 350, 410); c.quad(350, 410, 470, 300, 560, 430); c.quad(560, 430, 660, 530, 770, 380); c.dot(410, 545, 48)
    c = new(0xE82A, "c_v", "letters"); c.quad(290, 770, 380, 710, 370, 650); c.quad(370, 650, 220, 540, 350, 410); c.quad(350, 410, 470, 300, 560, 430); c.quad(560, 430, 660, 530, 770, 380); c.dot(410, 545, 48)

    # 8 Ponctuations curvilignes (U+E82B - U+E832)
    c = new(0xE82B, "p_allongement", "punctuation"); c.dot(500, 500, 62)
    c = new(0xE82C, "p_fin_mot", "punctuation"); c.quad(270, 500, 460, 480, 650, 500); c.line(650, 260, 650, 740)
    c = new(0xE82D, "p_point", "punctuation"); c.line(210, 500, 430, 500, 58); c.line(320, 390, 320, 610, 58); c.arc(580, 500, 120, 125, 85, 275, 58); c.line(730, 260, 730, 740)
    c = new(0xE82E, "p_infinitif", "punctuation"); c.line(220, 500, 440, 500, 58); c.line(330, 390, 330, 610, 58); c.arc(600, 500, 130, 130, 85, 275, 58)
    c = new(0xE82F, "p_intrus", "punctuation"); c.quad(230, 575, 360, 595, 480, 565, 58); c.quad(450, 475, 580, 455, 710, 480, 58); c.line(710, 310, 710, 690)
    c = new(0xE830, "p_interrogation", "punctuation"); c.quad(660, 730, 440, 500, 660, 270); c.dot(350, 635, 50); c.dot(350, 365, 50)
    c = new(0xE831, "p_guillemet", "punctuation"); c.line(220, 500, 420, 500, 58); c.oval(555, 500, 115, 115, 58); c.line(730, 260, 730, 740)
    c = new(0xE832, "p_doute", "punctuation"); c.line(220, 500, 440, 500, 58); c.line(330, 390, 330, 610, 58); c.oval(590, 500, 125, 125, 58)

    # 14 Chiffres/Multiplicateurs curvilignes (U+E833 - U+E840)
    c = new(0xE833, "n_0", "numbers"); c.quad(270, 595, 500, 620, 730, 595, 58); c.quad(270, 405, 500, 380, 730, 405, 58); c.quad(340, 260, 500, 500, 660, 740, 60)
    c = new(0xE834, "n_1", "numbers"); c.quad(330, 770, 500, 800, 670, 770); c.line(500, 200, 500, 630); c.quad(330, 415, 500, 390, 670, 415)
    c = new(0xE835, "n_2", "numbers"); c.quad(330, 770, 500, 560, 670, 360); c.quad(670, 770, 500, 560, 330, 360); c.quad(270, 215, 500, 185, 730, 215)
    c = new(0xE836, "n_3", "numbers"); c.line(350, 200, 350, 800); c.quad(350, 795, 540, 815, 680, 775); c.quad(350, 500, 540, 520, 680, 490); c.quad(350, 205, 540, 185, 680, 225)
    c = new(0xE837, "n_4", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.dot(550, 520, 58)
    c = new(0xE838, "n_5", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.quad(450, 515, 570, 495, 690, 515, 58)
    c = new(0xE839, "n_6", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.line(570, 440, 570, 680, 56); c.quad(450, 455, 570, 435, 690, 455, 56)
    c = new(0xE83A, "n_7", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.line(460, 690, 680, 430, 54); c.line(680, 690, 460, 430, 54)
    c = new(0xE83B, "n_8", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.line(470, 430, 470, 710, 52); c.quad(470, 705, 580, 720, 680, 695, 50); c.quad(470, 570, 580, 585, 680, 560, 50); c.quad(470, 435, 580, 420, 680, 445, 50)
    c = new(0xE83C, "n_9", "numbers"); c.line(330, 240, 330, 810); c.arc(410, 245, 80, 65, 180, 270); c.quad(410, 180, 570, 175, 700, 210); c.line(470, 430, 470, 710, 52); c.quad(470, 435, 580, 420, 680, 445, 50); c.dot(600, 600, 48)
    c = new(0xE83D, "m_da", "numbers"); c.oval(500, 690, 115, 115, 58); c.line(500, 200, 500, 810); c.quad(350, 455, 500, 435, 650, 455, 56); c.quad(330, 215, 500, 190, 670, 215, 58)
    c = new(0xE83E, "m_zangou", "numbers"); c.line(370, 330, 370, 810); c.line(630, 330, 630, 810); c.arc(500, 330, 130, 130, 180, 360); c.quad(250, 420, 500, 395, 750, 420, 58)
    c = new(0xE83F, "m_zambar", "numbers"); c.line(370, 330, 370, 810); c.line(630, 330, 630, 810); c.arc(500, 330, 130, 130, 180, 360); c.quad(250, 540, 500, 515, 750, 540, 54); c.quad(250, 390, 500, 365, 750, 390, 54)
    c = new(0xE840, "m_hawari", "numbers"); c.line(370, 330, 370, 810); c.line(630, 330, 630, 810); c.arc(500, 330, 130, 130, 180, 360); c.quad(250, 630, 500, 610, 750, 630, 50); c.quad(250, 490, 500, 470, 750, 490, 50); c.quad(250, 350, 500, 330, 750, 350, 50)

    # 15 Mots abrégés curvilignes (U+E841 - U+E84F)
    c = new(0xE841, "abbr_da", "abbreviations"); c.oval(500, 660, 115, 115, 58); c.quad(430, 560, 360, 380, 310, 210); c.quad(570, 560, 640, 380, 690, 210)
    c = new(0xE842, "abbr_boro", "abbreviations"); c.oval(500, 670, 130, 130, 60); c.line(500, 190, 500, 540)
    c = new(0xE843, "abbr_si", "abbreviations"); c.oval(500, 360, 145, 145, 60); c.line(500, 190, 500, 740); c.arc(600, 735, 100, 85, 0, 180)
    c = new(0xE844, "abbr_ga", "abbreviations"); c.quad(290, 750, 500, 785, 710, 750); c.quad(400, 750, 330, 480, 290, 210); c.quad(600, 750, 670, 480, 710, 210)
    c = new(0xE845, "abbr_go", "abbreviations"); c.oval(480, 640, 135, 135, 58); c.quad(340, 475, 500, 455, 660, 475, 56); c.quad(450, 465, 560, 330, 640, 210)
    c = new(0xE846, "abbr_ya", "abbreviations"); c.quad(310, 780, 410, 610, 500, 460); c.quad(690, 780, 590, 610, 500, 460); c.oval(500, 325, 130, 130, 58)
    c = new(0xE847, "abbr_dey", "abbreviations"); c.arc(500, 520, 155, 160, 180, 360); c.line(345, 520, 345, 770); c.line(655, 520, 655, 770); c.quad(250, 575, 500, 555, 750, 575, 56); c.line(500, 200, 500, 360)
    c = new(0xE848, "abbr_haya", "abbreviations"); c.oval(345, 500, 130, 130, 58); c.quad(490, 720, 620, 500, 750, 280); c.quad(750, 720, 620, 500, 490, 280)
    c = new(0xE849, "abbr_don", "abbreviations"); c.arc(500, 510, 210, 175, 180, 360); c.line(290, 510, 290, 680); c.line(710, 510, 710, 680); c.quad(380, 520, 500, 500, 620, 520, 56); c.line(500, 200, 500, 510)
    c = new(0xE84A, "abbr_yadine", "abbreviations"); c.line(500, 260, 500, 740); c.oval(500, 500, 155, 155, 58); c.arc(590, 735, 90, 80, 0, 180); c.arc(410, 265, 90, 80, 180, 360)
    c = new(0xE84B, "abbr_haifo", "abbreviations"); c.oval(500, 500, 115, 115, 56); c.quad(240, 720, 340, 620, 420, 540, 54); c.quad(240, 280, 340, 380, 420, 460, 54); c.quad(760, 720, 660, 620, 580, 540, 54); c.quad(760, 280, 660, 380, 580, 460, 54)
    c = new(0xE84C, "abbr_haikoul", "abbreviations"); c.oval(500, 500, 115, 115, 56); c.quad(300, 800, 390, 690, 460, 600, 54); c.quad(700, 800, 610, 690, 540, 600, 54); c.quad(300, 200, 390, 310, 460, 400, 54); c.quad(700, 200, 610, 310, 540, 400, 54)
    c = new(0xE84D, "abbr_zanga", "abbreviations"); c.arc(500, 470, 220, 190, 185, 355); c.dot(500, 490, 60)
    c = new(0xE84E, "abbr_kan", "abbreviations"); c.arc(410, 620, 90, 80, 0, 180); c.line(500, 410, 500, 620); c.arc(590, 410, 90, 80, 180, 360)
    c = new(0xE84F, "abbr_ik", "abbreviations"); c.line(370, 190, 370, 810); c.quad(370, 500, 520, 640, 670, 780); c.quad(370, 500, 520, 360, 670, 220)
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
    fb.setupNameTable({"familyName": "Zarma Eldas", "styleName": "Regular", "uniqueFontIdentifier": "ZarmaEldas-2.1", "fullName": "Zarma Eldas Regular", "version": "Version 2.1", "psName": "ZarmaEldas-Regular"})
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120); fb.setupPost()
    for out in ["font/ZarmaEldas.ttf", "android/app/src/main/assets/fonts/ZarmaEldas.ttf", "windows/ZarmaEldas.ttf"]:
        os.makedirs(os.path.dirname(out), exist_ok=True); fb.save(out)
    print(f"[OK] {len(glyphs)} SVG curvilignes + ZarmaEldas.ttf v2.1 générés.")
