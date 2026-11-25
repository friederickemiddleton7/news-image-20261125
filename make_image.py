#!/usr/bin/env python3
"""Build the news-image-20261125 entry: a 1024x1024 flat "front page" poster
summing up Wednesday 25 November 2026 world news.

Layout (design pixels; rendered at 2x supersample then downscaled to 1024):
  - masthead 0..150: kicker, the day "WEDNESDAY 25 NOVEMBER 2026" in the
    largest type on the page, amber rule, region key.
  - lead card 150..256: full-width emphasized story (chip, one-line headline,
    two factual lines).
  - briefs band 256..1024: the remaining 37 stories flow through 4 columns of
    measured ALL-CAPS lines: teal region code + grey place + white bold
    headline, 19 px type on a 19 px line step (glyph-box verified).

Every text run is measured with real font metrics, asserted >= 19 px and
inside the canvas; a final pass asserts no two runs overlap. Deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

SS = 2
CANVAS = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (11, 18, 32)
CARD = (21, 31, 51)
BAND = (13, 20, 35)
HAIR = (42, 58, 87)
BODY = (215, 222, 234)
WHITE = (255, 255, 255)
AMBER = (242, 179, 61)
TEAL = (79, 209, 197)
MUTED = (147, 160, 180)

BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"
MIN_FONT = 19

_fonts = {}
_meas_img = Image.new("RGB", (8, 8))
_meas = ImageDraw.Draw(_meas_img)

runs = []


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_DIR + name, size * SS)
    return _fonts[key]


def text_w(s, fnt):
    return _meas.textlength(s, font=fnt) / SS


def ink_h(s, name, size):
    bb = font(name, size).getbbox(s)
    return bb[3] - bb[1]


def tracked_w(s, fnt, tracking):
    return text_w(s, fnt) + tracking * max(0, len(s) - 1)


def ink_box(s, name, size):
    bb = font(name, size).getbbox(s)
    return bb[1] / SS, bb[3] / SS


def draw(d, x, y, s, name, size, fill, tracking=0, clip=None, label=""):
    """Draw text with top-left anchor, record its ink box, assert bounds."""
    fnt = font(name, size)
    if tracking:
        cx = x
        for ch in s:
            d.text((cx * SS, y * SS), ch, font=fnt, fill=fill)
            cx += text_w(ch, fnt) + tracking
    else:
        d.text((x * SS, y * SS), s, font=fnt, fill=fill)
    w = tracked_w(s, fnt, tracking)
    it, ib = ink_box(s, name, size)
    top = y + it
    box = (x, top, x + w, y + ib)
    runs.append(box + (size, label or s[:28]))
    if size < MIN_FONT:
        raise AssertionError("font %d < %d: %r" % (size, MIN_FONT, s))
    if box[2] > CANVAS or box[3] > CANVAS:
        raise AssertionError("run leaves canvas: %r %s" % (s[:30], box))
    if clip is not None:
        if box[0] < clip[0] or box[1] < clip[1] or box[2] > clip[2] or box[3] > clip[3]:
            raise AssertionError("run escapes clip %s: %r %s" % (clip, s[:30], box))
    return box[3]


def P(*vals):
    return [int(round(v * SS)) for v in vals]


def pw(v):
    return max(1, int(round(v * SS)))


STORIES = [
    ("EUR", "SAMARA, RUSSIA", "UKRAINIAN DRONES HIT THREE OIL REFINERIES"),
    ("EUR", "KYIV, UKRAINE", "EUROPE JOINS UKRAINE-US TALKS ON RUSSIA"),
    ("EUR", "MOSCOW, RUSSIA", "RUSSIA'S WAR LOSSES HIT 432,519, KYIV SAYS"),
    ("EUR", "BRUSSELS, EU", "EU IMPOSES QUOTAS ON HYBRID CAR IMPORTS"),
    ("EUR", "BERLIN, GERMANY", "GERMAN BUSINESS MORALE SAGS, FACTORIES WEAK"),
    ("EUR", "MADRID, SPAIN", "SPAIN'S RIGHT KEEPS POLL LEAD BEFORE VOTE"),
    ("EUR", "LONDON, UK", "UK FACES BACKLASH OVER E-VISA PLANS"),
    ("EUR", "SANDRINGHAM, ENGLAND", "TWO HELD OVER ROYAL ESTATE BREAK-IN"),
    ("EUR", "ESK\u0130\u015eEH\u0130R, TURKEY", "MILITARY HELICOPTER CRASH KILLS FIVE CREW"),
    ("AMR", "CARTAGENA, COLOMBIA", "GUNMEN HOLD 25 HOSTAGES AFTER HEIST"),
    ("AMR", "S\u00c3O PAULO, BRAZIL", "BRASKEM CLINCHES $4.9 BILLION CREDITOR DEAL"),
    ("AMR", "WASHINGTON, US", "US READIES TARIFFS ON CHINA, EU"),
    ("AMR", "CHICAGO, US", "O'HARE GROUND STOP HITS THANKSGIVING TRAVEL"),
    ("AMR", "SAN FRANCISCO, US", "KING TIDES FLOOD SAN FRANCISCO STREETS"),
    ("AMR", "JUNEAU, US", "ALASKA ENDS VOTER-DATA DEAL WITH DOJ"),
    ("AMR", "HAVANA, CUBA", "WHO CHIEF URGES END TO CUBA BLOCKADE"),
    ("AMR", "OTTAWA, CANADA", "CANADA TELLS PENTAGON IT 'ANSWERS TO NO ONE'"),
    ("APC", "JIUQUAN, CHINA", "CHINA LAUNCHES FIRST FOREIGN ASTRONAUT TO TIANGONG"),
    ("APC", "BEIJING, CHINA", "CHINA PROBES SHANGHAI PARTY CHIEF CHEN JINING"),
    ("APC", "NEW DELHI, INDIA", "FIRST AYODHYA-JANAKPUR TRAIN LAUNCHED WITH NEPAL"),
    ("APC", "DHAKA, BANGLADESH", "SHEIKH HASINA SEEKS PLANE HOME FOR DEC 16"),
    ("APC", "PYONGYANG, NORTH KOREA", "KIM HOSTS PHILIPPINE ENVOY IN PYONGYANG"),
    ("APC", "BANGKOK, THAILAND", "THAILAND DEFERS 20-BILLION-BAHT CIVIL SERVICE BUYOUT"),
    ("APC", "CANBERRA, AUSTRALIA", "AUSTRALIA INFLATION JUMPS TO 4.9 PERCENT"),
    ("APC", "HONIARA, SOLOMON ISLANDS", "SOLOMONS, AUSTRALIA SIGN TREATY TO BAR FOREIGN BASES"),
    ("APC", "PONTIANAK, INDONESIA", "72 ORANGUTANS RESCUED FROM BORNEO WILDFIRES"),
    ("APC", "MELBOURNE, AUSTRALIA", "RISING GOLF STAR ARCHIE ALSTON DIES AT 17"),
    ("MES", "SANA'A, YEMEN", "HOUTHIS THREATEN SAUDI PORTS OVER HODEIDAH"),
    ("MES", "JERUSALEM, ISRAEL", "EISENKOT SIGNS FIRST COALITION PARTNER IN ISRAEL"),
    ("AFR", "ASMARA, ERITREA", "HORN OF AFRICA SUMMIT CALLS FOR PEACE"),
    ("AFR", "BUNIA, DR CONGO", "WHO STAFF RESCUED FROM CONGO HOSPITAL"),
    ("GLB", "WASHINGTON, US", "AI-POWERED HACK BREACHED CIA SYSTEM, NYT SAYS"),
    ("GLB", "WORLD MARKETS", "GOLD AND SILVER TUMBLE, OIL NEAR LOWS"),
    ("GLB", "TOKYO AND SEOUL", "ASIAN STOCKS PLUNGE: NIKKEI -1,800, KOSPI -5%"),
    ("GLB", "SAN JUAN, PUERTO RICO", "AUSTRALIA CROWNED MISS UNIVERSE 2026"),
    ("GLB", "COLOGNY, SWITZERLAND", "WORLD CHESS TITLE MATCH BEGINS IN COLOGNY"),
    ("GLB", "DOHA, QATAR", "TEEN SMASHES 28-BALL ONE-DAY CENTURY"),
    ("GLB", "WORLDWIDE", "16 DAYS OF ACTIVISM ON GENDER VIOLENCE BEGIN"),
]
assert len(STORIES) == 38


def wrap_pairs(parts, maxw, size):
    """Greedy wrap of (text, fontname) parts; lines of (text, fontname, dx)."""
    fc = {}

    def F(n):
        if n not in fc:
            fc[n] = font(n, size)
        return fc[n]

    sp = text_w(" ", F(REG))
    lines, cur, curw = [], [], 0.0
    for (t, fn) in parts:
        w = text_w(t, F(fn))
        if cur and curw + sp + w > maxw:
            lines.append(cur)
            cur = []
            curw = 0.0
        x = curw if not cur else curw + sp
        cur.append((t, fn, x))
        curw = x + w
    if cur:
        lines.append(cur)
    return lines


def mix_headline(code, place, head):
    parts = [(code + " \u00b7", REG)]
    parts += [(w, REG) for w in place.split()]
    parts.append(("\u2014", REG))
    parts += [(w, BOLD) for w in head.split()]
    return parts


def masthead(d):
    draw(d, 24, 10, "WORLD NEWS", BOLD, 22, AMBER, tracking=8,
         clip=(0, 0, CANVAS, 52), label="kicker")
    draw(d, 24, 44, "WEDNESDAY 25 NOVEMBER 2026", BOLD, 44, WHITE,
         clip=(0, 0, CANVAS, 114), label="date")
    d.rectangle(P(24, 108, 1000, 111), fill=AMBER)
    key = ("REGION KEY \u2014 EUR EUROPE \u00b7 AMR AMERICAS \u00b7 APC ASIA-PAC \u00b7 "
           "MES MIDEAST \u00b7 AFR AFRICA \u00b7 GLB GLOBAL")
    draw(d, 20, 114, key, REG, 19, MUTED, clip=(0, 102, CANVAS, 148), label="key")


def lead(d):
    y0, y1 = 150, 278
    d.rectangle(P(0, y0, CANVAS, y1), fill=CARD)
    d.rectangle(P(0, y0, CANVAS - 1, y1 - 1), outline=HAIR, width=pw(1))
    clip = (0, y0, CANVAS, y1)

    draw(d, 24, y0 + 4, "LEAD \u00b7 EUROPE \u00b7 SAMARA, RUSSIA", BOLD, 19, TEAL,
         tracking=1, clip=clip, label="lead-chip")

    head = STORIES[0][2]
    # one line at the largest size that fits the full width
    size = 19
    for sz in range(36, 18, -1):
        if text_w(head, font(BOLD, sz)) <= 976:
            size = sz
            break
    y = y0 + 28
    draw(d, 24, y, head, BOLD, size, WHITE, clip=clip, label="lead-head")

    bodies = [
        "Overnight strikes set fires at Syzran, Novokuybyshevsk and Kuibyshev plants; Kyiv claims the strikes.",
        "Also today: Europe joins Ukraine-US talks on Russia's war in Kyiv.",
    ]
    by = y + 32
    for i, s in enumerate(bodies):
        draw(d, 24, by, s, REG, 19, BODY, clip=clip, label="lead-body%d" % i)
        by += 19
    if by > y1 - 2:
        raise AssertionError("lead body overflows card: %d > %d" % (by, y1 - 2))


def briefs(d):
    y0 = 278
    d.rectangle(P(0, y0, CANVAS, CANVAS), fill=BAND)
    d.rectangle(P(0, y0, CANVAS - 1, y0), fill=HAIR)

    cols = 4
    col_w = 250
    col_x = [4 + i * (col_w + 4) for i in range(cols)]
    start_y = 278
    step = 19
    limit = 1000

    brief_ls = [wrap_pairs(mix_headline(*s), col_w, 19) for s in STORIES[1:]]
    overflow = 0.0
    for bl in brief_ls:
        for ln in bl:
            w = ln[-1][2] + text_w(ln[-1][0], font(ln[-1][1], 19))
            overflow = max(overflow, w - col_w)
    if overflow > 2.0:
        raise AssertionError("brief line exceeds column by %.1f px" % overflow)

    ys = [start_y] * cols
    ci = 0
    placed = 0
    first = True
    for bl in brief_ls:
        for ln in bl:
            if ys[ci] + step > limit:
                ci += 1
                if ci >= cols:
                    raise AssertionError("briefs overflow at line %d" % placed)
                ys[ci] = start_y
            x = col_x[ci]
            for (t, fn, dx) in ln:
                if fn == BOLD:
                    color = WHITE
                elif t.endswith("\u00b7"):
                    color = TEAL
                else:
                    color = BODY
                draw(d, x + dx, ys[ci], t, fn, 19, color,
                     clip=(x - 4, y0, CANVAS, CANVAS), label="brief")
            ys[ci] += step
            placed += 1
    return placed


def build(path):
    img = Image.new("RGB", (CANVAS * SS, CANVAS * SS), NAVY)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead(d)
    n_lines = briefs(d)

    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            a, b = runs[i], runs[j]
            if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
                raise AssertionError("text runs overlap: %r vs %r" % (a[5], b[5]))

    out = img.resize((CANVAS, CANVAS), Image.LANCZOS)
    out.save(path, "PNG", optimize=True)
    print("stories: %d (1 lead + %d briefs), brief lines: %d, text runs: %d"
          % (len(STORIES), len(STORIES) - 1, n_lines, len(runs)))
    assert n_lines >= 37, "too few brief lines: %d" % n_lines
    print("ALL LAYOUT CHECKS PASSED")


if __name__ == "__main__":
    build("entry.png")
