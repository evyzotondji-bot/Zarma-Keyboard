import os
import math
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

class ZarmaCanvas:
    def __init__(self):
        self.contours = []
        self.svg_elements = []

    def rect(self, x1, y1, x2, y2):
        xa, xb = min(x1, x2), max(x1, x2)
        ya, yb = min(y1, y2), max(y1, y2)
        pts = [(xa, ya), (xb, ya), (xb, yb), (xa, yb)]
        self.contours.append(pts)
        self.svg_elements.append(f'<rect x="{xa}" y="{1000-yb}" width="{xb-xa}" height="{yb-ya}" fill="currentColor"/>')

    def thick_line(self, x1, y1, x2, y2, w=76):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return
        nx, ny = -dy / length * (w / 2), dx / length * (w / 2)
        pts = [
            (round(x1 + nx), round(y1 + ny)),
            (round(x2 + nx), round(y2 + ny)),
            (round(x2 - nx), round(y2 - ny)),
            (round(x1 - nx), round(y1 - ny)),
        ]
        self.contours.append(pts)
        svg_pts = " ".join(f"{x},{1000-y}" for x, y in pts)
        self.svg_elements.append(f'<polygon points="{svg_pts}" fill="currentColor"/>')

    def ring(self, cx, cy, r_outer, r_inner=None, segs=36):
        if r_inner is None:
            r_inner = max(10, r_outer - 76)
        outer, inner = [], []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            outer.append((round(cx + r_outer * math.cos(a)), round(cy + r_outer * math.sin(a))))
            a_rev = 2 * math.pi * (segs - 1 - i) / segs
            inner.append((round(cx + r_inner * math.cos(a_rev)), round(cy + r_inner * math.sin(a_rev))))
        self.contours.append(outer)
        self.contours.append(inner)
        self.svg_elements.append(f'<circle cx="{cx}" cy="{1000-cy}" r="{(r_outer+r_inner)/2}" fill="none" stroke="currentColor" stroke-width="{r_outer-r_inner}"/>')

    def dot(self, cx, cy, r=55):
        pts = [(round(cx + r * math.cos(2 * math.pi * i / 24)), round(cy + r * math.sin(2 * math.pi * i / 24))) for i in range(24)]
        self.contours.append(pts)
        self.svg_elements.append(f'<circle cx="{cx}" cy="{1000-cy}" r="{r}" fill="currentColor"/>')

    def u_cup(self, x_left, x_right, y_bot, y_top, w=76):
        self.rect(x_left, y_bot, x_right, y_bot + w)
        self.rect(x_left, y_top - w, x_right, y_top)
        self.rect(x_left, y_bot, x_left + w, y_top)

    def to_svg(self):
        body = "\n  ".join(self.svg_elements)
        return f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n  {body}\n</svg>\n'

    def draw_to_pen(self, pen):
        for pts in self.contours:
            pen.moveTo(pts[0])
            for pt in pts[1:]:
                pen.lineTo(pt)
            pen.closePath()

def build_all_glyphs():
    G = {}
    def new(cp, name, cat):
        c = ZarmaCanvas()
        G[name] = (cp, cat, c)
        return c

    # 10 Voyelles minuscules manuscrites
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

    # 10 Voyelles initiales / majuscules
    for idx, (nm, bars) in enumerate([("V_A", 1), ("V_I", 2), ("V_O", 3)]):
        c = new(0xE00A + idx, nm, "vowels_cap")
        c.rect(460, 160, 536, 840); c.rect(460, 764, 660, 840); c.rect(584, 650, 660, 840)
        for b in range(bars):
            y = 220 + b * 110; c.rect(340, y, 660, y + 66)
    for idx, (nm, bars) in enumerate([("V_E", 1), ("V_OU", 2)]):
        c = new(0xE00D + idx, nm, "vowels_cap")
        c.rect(530, 160, 606, 840); c.ring(445, 290, 120)
        for b in range(bars):
            y = 560 + b * 115; c.rect(380, y, 680, y + 66)
    for idx, (nm, bars) in enumerate([("V_AI", 1), ("V_OI", 2)]):
        c = new(0xE00F + idx, nm, "vowels_cap")
        c.rect(530, 160, 606, 840); c.rect(380, 160, 606, 236); c.rect(380, 160, 456, 360)
        for b in range(bars):
            y = 560 + b * 115; c.rect(380, y, 680, y + 66)
    for idx, (nm, bars) in enumerate([("V_AN", 1), ("V_IN", 2), ("V_ON", 3)]):
        c = new(0xE011 + idx, nm, "vowels_cap")
        c.rect(530, 160, 606, 840); c.ring(435, 690, 140)
        for b in range(bars):
            y = 200 + b * 105; c.rect(380, y, 680, y + 64)

    # 22 Consonnes + V
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
    c = new(0xE025, "c_gn", "letters"); [c.rect(x, 180, x + 76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 640, 640, 705)
    c = new(0xE026, "c_ch", "letters"); [c.rect(x, 180, x + 76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 700, 640, 760); c.rect(360, 580, 640, 640)
    c = new(0xE027, "c_tch", "letters"); [c.rect(x, 180, x + 76, 500) for x in (260, 462, 664)]; c.rect(260, 440, 740, 516); c.rect(462, 480, 538, 840); c.rect(360, 740, 640, 795); c.rect(360, 640, 640, 695); c.rect(360, 540, 640, 595)
    c = new(0xE028, "c_dj", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360)
    c = new(0xE029, "c_nw", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360); c.dot(420, 550, 52)
    c = new(0xE02A, "c_v", "letters"); c.thick_line(380, 680, 240, 540); c.thick_line(240, 540, 460, 320); c.thick_line(460, 320, 640, 500); c.thick_line(640, 500, 780, 360); c.thick_line(280, 780, 380, 680); c.dot(420, 550, 52)

    # 8 Signes de ponctuation & modificateurs
    c = new(0xE02B, "p_allongement", "punctuation"); c.dot(500, 500, 68)
    c = new(0xE02C, "p_fin_mot", "punctuation"); c.rect(260, 462, 660, 538); c.rect(620, 240, 696, 760)
    c = new(0xE02D, "p_point", "punctuation"); c.rect(200, 462, 440, 538); c.rect(300, 380, 366, 620); c.u_cup(440, 720, 360, 640, 70); c.rect(700, 240, 776, 760)
    c = new(0xE02E, "p_infinitif", "punctuation"); c.rect(200, 462, 440, 538); c.rect(300, 380, 366, 620); c.u_cup(440, 740, 360, 640, 70)
    c = new(0xE02F, "p_intrus", "punctuation"); c.rect(220, 540, 480, 616); c.rect(440, 440, 720, 516); c.rect(680, 300, 756, 700)
    c = new(0xE030, "p_interrogation", "punctuation"); c.thick_line(680, 740, 460, 500); c.thick_line(460, 500, 680, 260); c.dot(350, 640, 56); c.dot(350, 360, 56)
    c = new(0xE031, "p_guillemet", "punctuation"); c.rect(220, 462, 440, 538); c.ring(565, 500, 130); c.rect(695, 240, 771, 760)
    c = new(0xE032, "p_doute", "punctuation"); c.rect(220, 462, 460, 538); c.rect(320, 380, 386, 620); c.ring(600, 500, 140)

    # 10 Chiffres + 4 Multiplicateurs + 5 Abréviations
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
    c = new(0xE041, "abbr_da", "abbreviations"); c.ring(500, 660, 130); c.thick_line(430, 560, 300, 200); c.thick_line(570, 560, 700, 200)
    c = new(0xE042, "abbr_boro", "abbreviations"); c.ring(500, 680, 140); c.rect(462, 180, 538, 550)
    c = new(0xE043, "abbr_si", "abbreviations"); c.ring(500, 360, 160); c.rect(462, 180, 538, 820); c.rect(462, 744, 720, 820)
    c = new(0xE044, "abbr_ga", "abbreviations"); c.rect(280, 724, 720, 800); c.thick_line(400, 724, 280, 200); c.thick_line(600, 724, 720, 200)
    c = new(0xE045, "abbr_go", "abbreviations"); c.ring(480, 640, 150); c.rect(340, 440, 660, 516); c.thick_line(440, 440, 640, 200)
    return G

def export_svgs_and_ttf(glyphs):
    for name, (cp, cat, canvas) in glyphs.items():
        os.makedirs(f"svg/{cat}", exist_ok=True)
        with open(f"svg/{cat}/{name}_U{cp:04X}.svg", "w", encoding="utf-8") as f:
            f.write(canvas.to_svg())
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder([".notdef", "space"] + list(glyphs.keys()))
    cmap = {0x0020: "space"}
    for name, (cp, _, _) in glyphs.items():
        cmap[cp] = name
    fb.setupCharacterMap(cmap)
    pen_dict = {}
    nd = TTGlyphPen(None); nd.moveTo((100, 0)); nd.lineTo((100, 800)); nd.lineTo((500, 800)); nd.lineTo((500, 0)); nd.closePath()
    pen_dict[".notdef"] = nd.glyph()
    pen_dict["space"] = TTGlyphPen(None).glyph()
    for name, (_, _, canvas) in glyphs.items():
        pen = TTGlyphPen(None); canvas.draw_to_pen(pen); pen_dict[name] = pen.glyph()
    fb.setupGlyf(pen_dict)
    metrics = {".notdef": (600, 100), "space": (350, 0)}
    for name in glyphs:
        metrics[name] = (920, 80)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({"familyName": "Zarma Eldas", "styleName": "Regular", "uniqueFontIdentifier": "ZarmaEldas-1.0", "fullName": "Zarma Eldas Regular", "version": "Version 1.0", "psName": "ZarmaEldas-Regular"})
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120)
    fb.setupPost()
    for out_path in ["font/ZarmaEldas.ttf", "android/app/src/main/assets/fonts/ZarmaEldas.ttf", "windows/ZarmaEldas.ttf"]:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fb.save(out_path)
    print(f"[OK] {len(glyphs)} SVG + ZarmaEldas.ttf générés.")

def write_file(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))

def generate_android_project():
    write_file("android/gradle.properties", "android.useAndroidX=true\norg.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n")
    write_file("android/settings.gradle.kts", 'pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }\ndependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }\nrootProject.name = "ZarmaKeyboard"\ninclude(":app")\n')
    write_file("android/build.gradle.kts", 'plugins { id("com.android.application") version "8.5.2" apply false; id("org.jetbrains.kotlin.android") version "1.9.24" apply false }\n')
    write_file("android/app/build.gradle.kts", """
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.zedempires.zarmakeyboard"
    compileSdk = 34
    defaultConfig { applicationId = "com.zedempires.zarmakeyboard"; minSdk = 24; targetSdk = 34; versionCode = 1; versionName = "1.0.0" }
    buildTypes { release { isMinifyEnabled = false; proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro") } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
}
""")
    write_file("android/app/src/main/AndroidManifest.xml", """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:allowBackup="true" android:label="Clavier Zarma" android:supportsRtl="true" android:theme="@style/Theme.Material3.DayNight.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter>
        </activity>
        <service android:name=".ZarmaIMEService" android:exported="true" android:label="Clavier Zarma (ELDAS)" android:permission="android.permission.BIND_INPUT_METHOD">
            <intent-filter><action android:name="android.view.InputMethod" /></intent-filter>
            <meta-data android:name="android.view.im" android:resource="@xml/method" />
        </service>
    </application>
</manifest>
""")
    write_file("android/app/src/main/res/xml/method.xml", '<?xml version="1.0" encoding="utf-8"?>\n<input-method xmlns:android="http://schemas.android.com/apk/res/android" android:settingsActivity="com.zedempires.zarmakeyboard.MainActivity"><subtype android:label="Zarma (Niger)" android:imeSubtypeLocale="dje_NE" android:imeSubtypeMode="keyboard" /></input-method>\n')
    write_file("android/app/src/main/java/com/zedempires/zarmakeyboard/ThemeManager.kt", """
package com.zedempires.zarmakeyboard
import android.content.Context
import android.graphics.Color

data class KeyboardTheme(val id: String, val name: String, val bgColor: Int, val keyColor: Int, val actionKeyColor: Int, val textColor: Int, val hintColor: Int)

object ThemeManager {
    val THEMES = listOf(
        KeyboardTheme("green", "Vert Zarma", Color.parseColor("#388E3C"), Color.parseColor("#57A05A"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#C8E6C9")),
        KeyboardTheme("eldas_blue", "Bleu ELDAS", Color.parseColor("#154360"), Color.parseColor("#1F618D"), Color.parseColor("#0E2F44"), Color.WHITE, Color.parseColor("#AED6F1")),
        KeyboardTheme("turquoise", "Turquoise", Color.parseColor("#00796B"), Color.parseColor("#26A69A"), Color.parseColor("#004D40"), Color.WHITE, Color.parseColor("#B2DFDB")),
        KeyboardTheme("amoled", "Noir AMOLED", Color.parseColor("#000000"), Color.parseColor("#1E1E1E"), Color.parseColor("#2E7D32"), Color.WHITE, Color.parseColor("#A5D6A7")),
        KeyboardTheme("gold", "Or & Ardoise", Color.parseColor("#212121"), Color.parseColor("#37474F"), Color.parseColor("#F9A825"), Color.WHITE, Color.parseColor("#FFF59D"))
    )
    fun getCurrentTheme(context: Context): KeyboardTheme {
        val id = context.getSharedPreferences("zarma_kbd_prefs", Context.MODE_PRIVATE).getString("theme_id", "green")
        return THEMES.find { it.id == id } ?: THEMES.first()
    }
    fun nextTheme(context: Context): KeyboardTheme {
        val current = getCurrentTheme(context)
        val next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.size]
        context.getSharedPreferences("zarma_kbd_prefs", Context.MODE_PRIVATE).edit().putString("theme_id", next.id).apply()
        return next
    }
}
""")
    write_file("android/app/src/main/java/com/zedempires/zarmakeyboard/ZarmaIMEService.kt", """
package com.zedempires.zarmakeyboard
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.inputmethodservice.InputMethodService
import android.util.TypedValue
import android.view.*
import android.widget.*

class ZarmaIMEService : InputMethodService() {
    private lateinit var zarmaFont: Typeface
    private lateinit var rootLayout: LinearLayout
    private var isShift = false
    private var isSymbols = false

    private val row1Lower = listOf(Pair("\\uE000","\\uE034"), Pair("\\uE024","\\uE035"), Pair("\\uE003","\\uE036"), Pair("\\uE01F","\\uE037"), Pair("\\uE021","\\uE038"), Pair("\\uE023","\\uE039"), Pair("\\uE004","\\uE03A"), Pair("\\uE001","\\uE03B"), Pair("\\uE002","\\uE03C"), Pair("\\uE01E","\\uE033"))
    private val row2Lower = listOf("\\uE005","\\uE020","\\uE015","\\uE016","\\uE017","\\uE018","\\uE019","\\uE01A","\\uE01B","\\uE01C")
    private val row3Lower = listOf("\\uE022","\\uE006","\\uE007","\\uE008","\\uE009","\\uE014","\\uE01D")
    private val row1Upper = listOf(Pair("\\uE00A","\\uE034"), Pair("\\uE02A","\\uE035"), Pair("\\uE00D","\\uE036"), Pair("\\uE025","\\uE037"), Pair("\\uE027","\\uE038"), Pair("\\uE026","\\uE039"), Pair("\\uE00E","\\uE03A"), Pair("\\uE00B","\\uE03B"), Pair("\\uE00C","\\uE03C"), Pair("\\uE028","\\uE033"))
    private val row2Upper = listOf("\\uE00F","\\uE029","\\uE015","\\uE016","\\uE017","\\uE018","\\uE019","\\uE01A","\\uE01B","\\uE01C")
    private val row3Upper = listOf("\\uE022","\\uE010","\\uE011","\\uE012","\\uE013","\\uE014","\\uE01D")
    private val symRow1 = listOf("\\uE034","\\uE035","\\uE036","\\uE037","\\uE038","\\uE039","\\uE03A","\\uE03B","\\uE03C","\\uE033")
    private val symRow2 = listOf("\\uE03D","\\uE03E","\\uE03F","\\uE040","\\uE041","\\uE042","\\uE043","\\uE044","\\uE045")
    private val symRow3 = listOf("\\uE02B","\\uE02C","\\uE02D","\\uE02E","\\uE02F","\\uE030","\\uE031","\\uE032")

    override fun onCreate() { super.onCreate(); zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf") }
    override fun onCreateInputView(): View {
        rootLayout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(8, 8, 8, 16) }
        renderKeyboard()
        return rootLayout
    }
    private fun dp(v: Int): Int = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()
    private fun makeKeyBg(color: Int, radiusDp: Int = 10) = GradientDrawable().apply { setColor(color); cornerRadius = dp(radiusDp).toFloat() }

    private fun renderKeyboard() {
        val theme = ThemeManager.getCurrentTheme(this)
        rootLayout.removeAllViews(); rootLayout.setBackgroundColor(theme.bgColor)
        val topBar = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(12, 4, 12, 10) }
        val titleView = TextView(this).apply { text = "ZARMA • ${theme.name}"; setTextColor(theme.hintColor); textSize = 13f; layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f) }
        val paletteBtn = TextView(this).apply {
            text = "🎨 Couleur"; setTextColor(theme.textColor); textSize = 13f; setPadding(dp(12), dp(6), dp(12), dp(6)); background = makeKeyBg(theme.actionKeyColor, 16)
            setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); ThemeManager.nextTheme(this@ZarmaIMEService); renderKeyboard() }
        }
        topBar.addView(titleView); topBar.addView(paletteBtn); rootLayout.addView(topBar)
        if (isSymbols) {
            rootLayout.addView(buildSimpleRow(symRow1, theme)); rootLayout.addView(buildSimpleRow(symRow2, theme)); rootLayout.addView(buildRow3(symRow3, theme, false))
        } else {
            rootLayout.addView(buildRow1(if (isShift) row1Upper else row1Lower, theme))
            rootLayout.addView(buildSimpleRow(if (isShift) row2Upper else row2Lower, theme))
            rootLayout.addView(buildRow3(if (isShift) row3Upper else row3Lower, theme, true))
        }
        rootLayout.addView(buildBottomRow(theme))
    }

    private fun buildRow1(keys: List<Pair<String, String>>, theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for ((mainChar, numHint) in keys) {
            val cell = FrameLayout(this).apply {
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }; background = makeKeyBg(theme.keyColor)
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(mainChar, 1) }
                setOnLongClickListener { it.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS); currentInputConnection?.commitText(numHint, 1); true }
            }
            cell.addView(TextView(this).apply { text = mainChar; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER })
            cell.addView(TextView(this).apply { text = numHint; typeface = zarmaFont; setTextColor(theme.hintColor); textSize = 11f; gravity = Gravity.TOP or Gravity.END; setPadding(0, dp(2), dp(5), 0) })
            row.addView(cell)
        }
        return row
    }

    private fun buildSimpleRow(keys: List<String>, theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        for (ch in keys) {
            row.addView(TextView(this).apply {
                text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER; background = makeKeyBg(theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(ch, 1) }
            })
        }
        return row
    }

    private fun buildRow3(keys: List<String>, theme: KeyboardTheme, showShift: Boolean): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        if (showShift) {
            row.addView(TextView(this).apply {
                text = if (isShift) "⬆" else "⇧"; setTextColor(theme.textColor); textSize = 20f; gravity = Gravity.CENTER
                background = makeKeyBg(if (isShift) theme.actionKeyColor else theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1.3f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { isShift = !isShift; renderKeyboard() }
            })
        }
        for (ch in keys) {
            row.addView(TextView(this).apply {
                text = ch; typeface = zarmaFont; setTextColor(theme.textColor); textSize = 24f; gravity = Gravity.CENTER; background = makeKeyBg(theme.keyColor)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), 1f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.commitText(ch, 1) }
            })
        }
        row.addView(TextView(this).apply {
            text = "⌫"; setTextColor(theme.textColor); textSize = 20f; gravity = Gravity.CENTER; background = makeKeyBg(theme.actionKeyColor)
            layoutParams = LinearLayout.LayoutParams(0, dp(50), 1.4f).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
            setOnClickListener { it.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP); currentInputConnection?.deleteSurroundingText(1, 0) }
        })
        return row
    }

    private fun buildBottomRow(theme: KeyboardTheme): LinearLayout {
        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        val addKey = { txt: String, zFont: Boolean, w: Float, bg: Int, rad: Int, onClick: () -> Unit ->
            row.addView(TextView(this).apply {
                text = txt; if (zFont) typeface = zarmaFont; setTextColor(theme.textColor); textSize = if (zFont) 20f else 17f; gravity = Gravity.CENTER; background = makeKeyBg(bg, rad)
                layoutParams = LinearLayout.LayoutParams(0, dp(50), w).apply { setMargins(dp(3), dp(4), dp(3), dp(4)) }
                setOnClickListener { onClick() }
            })
        }
        addKey(if (isSymbols) "\\uE000\\uE014" else "\\uE034\\uE035\\uE036", true, 1.5f, theme.actionKeyColor, 18) { isSymbols = !isSymbols; renderKeyboard() }
        addKey("\\uE02C", true, 1f, theme.keyColor, 10) { currentInputConnection?.commitText("\\uE02C", 1) }
        addKey("Zarma", false, 3.8f, theme.keyColor, 14) { currentInputConnection?.commitText(" ", 1) }
        addKey("\\uE02D", true, 1f, theme.keyColor, 10) { currentInputConnection?.commitText("\\uE02D", 1) }
        addKey("↵", false, 1.5f, theme.actionKeyColor, 24) { currentInputConnection?.commitText("\\n", 1) }
        return row
    }
}
""")
    write_file("android/app/src/main/java/com/zedempires/zarmakeyboard/MainActivity.kt", """
package com.zedempires.zarmakeyboard
import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.provider.Settings
import android.view.inputmethod.InputMethodManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val zarmaFont = Typeface.createFromAsset(assets, "fonts/ZarmaEldas.ttf")
        val layout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(48, 64, 48, 48) }
        layout.addView(TextView(this).apply { text = "Clavier Zarma Officiel (ELDAS)"; textSize = 22f })
        layout.addView(Button(this).apply { text = "1. Activer le Clavier Zarma"; setOnClickListener { startActivity(Intent(Settings.ACTION_INPUT_METHOD_SETTINGS)) } })
        layout.addView(Button(this).apply { text = "2. Choisir Clavier Zarma"; setOnClickListener { (getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager).showInputMethodPicker() } })
        layout.addView(Button(this).apply {
            text = "3. Couleur : ${ThemeManager.getCurrentTheme(this@MainActivity).name}"
            setOnClickListener { text = "3. Couleur : ${ThemeManager.nextTheme(this@MainActivity).name}" }
        })
        layout.addView(EditText(this).apply { hint = "Testez l'écriture Zarma ici..."; typeface = zarmaFont; textSize = 26f; minLines = 3 })
        setContentView(layout)
    }
}
""")

def generate_windows_package():
    write_file("windows/INSTALLER_CLAVIER_ZARMA.bat", '@echo off\npowershell -ExecutionPolicy Bypass -File "%~dp0Install_Zarma_Windows.ps1"\npause\n')
    write_file("windows/Install_Zarma_Windows.ps1", """
$fontSrc = Join-Path $PSScriptRoot "ZarmaEldas.ttf"
$fontDst = Join-Path $env:LOCALAPPDATA "Microsoft\\Windows\\Fonts\\ZarmaEldas.ttf"
New-Item -ItemType Directory -Force -Path (Split-Path $fontDst) | Out-Null
Copy-Item -Path $fontSrc -Destination $fontDst -Force
New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" -Name "Zarma Eldas (TrueType)" -Value $fontDst -PropertyType String -Force | Out-Null
Copy-Item -Path (Join-Path $PSScriptRoot "LANCER_CLAVIER_ZARMA.bat") -Destination (Join-Path ([Environment]::GetFolderPath("Desktop")) "Clavier Zarma.bat") -Force
Write-Host "[OK] Police ZarmaEldas.ttf et Clavier Zarma installes !" -ForegroundColor Green
""")
    write_file("windows/LANCER_CLAVIER_ZARMA.bat", '@echo off\nstart "" powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0ZarmaVisualKeyboard.ps1"\n')
    write_file("windows/ZarmaVisualKeyboard.ps1", """
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms
$themes = @(@{Bg="#388E3C"}, @{Bg="#154360"}, @{Bg="#00796B"}, @{Bg="#000000"})
$script:idx = 0
[xml]$xaml = '<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" Title="Clavier Zarma (ELDAS)" Width="820" Height="340" Topmost="True" WindowStartupLocation="CenterScreen" Background="#388E3C"><Grid Margin="10"><Grid.RowDefinitions><RowDefinition Height="38"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/><RowDefinition Height="*"/></Grid.RowDefinitions><Button Name="BtnTheme" Grid.Row="0" Content="Changer Couleur" HorizontalAlignment="Right" Padding="12,4" Background="#2E7D32" Foreground="White"/><UniformGrid Name="Row1" Grid.Row="1" Columns="10"/><UniformGrid Name="Row2" Grid.Row="2" Columns="10"/><UniformGrid Name="Row3" Grid.Row="3" Columns="10"/><UniformGrid Name="Row4" Grid.Row="4" Columns="6"/></Grid></Window>'
$win = [Windows.Markup.XamlReader]::Load((New-Object System.Xml.XmlNodeReader $xaml))
$zFont = New-Object System.Windows.Media.FontFamily((New-Object System.Uri($PSScriptRoot + "\\")), "./#Zarma Eldas")
function Add-Keys($p, $codes) {
    foreach ($cp in $codes) {
        $b = New-Object System.Windows.Controls.Button; $b.Content = [string][char]$cp; $b.FontFamily = $zFont; $b.FontSize = 22; $b.Foreground = "White"; $b.Background = "#57A05A"; $b.Margin = "3"
        $b.Add_Click({ param($s,$e); [System.Windows.Clipboard]::SetText($s.Content); [System.Windows.Forms.SendKeys]::SendWait("^v") })
        $p.Children.Add($b) | Out-Null
    }
}
Add-Keys $win.FindName("Row1") @(0xE000,0xE024,0xE003,0xE01F,0xE021,0xE023,0xE004,0xE001,0xE002,0xE01E)
Add-Keys $win.FindName("Row2") @(0xE005,0xE020,0xE015,0xE016,0xE017,0xE018,0xE019,0xE01A,0xE01B,0xE01C)
Add-Keys $win.FindName("Row3") @(0xE022,0xE006,0xE007,0xE008,0xE009,0xE014,0xE01D,0xE025,0xE026,0xE027)
Add-Keys $win.FindName("Row4") @(0xE028,0xE029,0xE02B,0xE02C,0xE02D,0xE030)
$win.FindName("BtnTheme").Add_Click({ $script:idx = ($script:idx + 1) % $themes.Count; $win.Background = $themes[$script:idx].Bg })
$win.ShowDialog() | Out-Null
""")

def generate_github_files():
    write_file("LICENSE", "MIT License\n\nCopyright (c) 2026 Yves ZOTONDJI (ZEDEMPIRES / OMAR STARLINK) & Académie ELDAS\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n")
    write_file("README.md", "# Clavier Zarma Officiel — Android & Windows (Écriture ELDAS)\n\nClavier virtuel libre et gratuit pour écrire nativement la langue **Zarma** avec ses caractères propres (sans forme latine), basé sur le système de l'académie **ELDAS**.\n\n## Téléchargement Gratuit\nRendez-vous dans l'onglet **[Releases](../../releases)** à droite pour télécharger :\n1. **`ZarmaKeyboard-Android.apk`** (Android avec changement de couleurs intégré)\n2. **`ZarmaKeyboard-Windows.zip`** (Windows 10/11 + police `ZarmaEldas.ttf`)\n3. **`ZarmaScript-SVG-Pack.zip`** (Les 69 glyphes vectoriels `.svg` + `.ttf`)\n")
    write_file(".github/workflows/build-release.yml", """
name: Build Zarma Keyboard
on:
  push:
    branches: [ main ]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install fonttools && python generate_zarma_repo.py
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: gradle/actions/setup-gradle@v4
        with:
          gradle-version: '8.7'
      - run: |
          cd android
          gradle assembleDebug
          cp app/build/outputs/apk/debug/app-debug.apk ../ZarmaKeyboard-Android.apk
      - run: |
          zip -r ZarmaKeyboard-Windows.zip windows/ font/ZarmaEldas.ttf LICENSE README.md
          zip -r ZarmaScript-SVG-Pack.zip svg/ font/ZarmaEldas.ttf LICENSE
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: v1.0.${{ github.run_number }}
          name: "Clavier Zarma v1.0.${{ github.run_number }} (Android & Windows)"
          files: |
            ZarmaKeyboard-Android.apk
            ZarmaKeyboard-Windows.zip
            ZarmaScript-SVG-Pack.zip
""")

if __name__ == "__main__":
    glyphs = build_all_glyphs()
    export_svgs_and_ttf(glyphs)
    generate_android_project()
    generate_windows_package()
    generate_github_files()
    print("[TERMINE] Tout le depot Zarma-Keyboard est pret !")
