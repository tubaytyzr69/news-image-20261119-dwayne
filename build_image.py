#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news broadsheet for the @dwayne entry.

Reads nothing, draws everything with Pillow vector shapes and DejaVu
fonts, and writes entry.png (1024x1024, under 1 MiB). Deterministic:
no timestamps, no randomness, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
F = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

INK = (17, 17, 17)
PAPER = (247, 243, 234)
RED = (176, 42, 32)
NAVY = (28, 47, 87)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, width, lines, fnt, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def rule(x, y, w, color=INK, thick=2):
    d.rectangle([x, y, x + w, y + thick - 1], fill=color)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 148], fill=(255, 255, 255))
d.text((512, 18), "THE WORLD TODAY", font=SERIF_B(84), fill=INK, anchor="ma")
rule(36, 118, W - 72, RED, 4)
dateline = "THURSDAY  19 NOVEMBER 2026"
d.text((36, 126), dateline, font=SANS_B(21), fill=RED)
d.text((W - 36, 126), "THE DAY'S NEWS IN ONE PAGE", font=SANS_B(15), fill=GREY, anchor="ra")

# ---------------------------------------------------------------- leads
LEAD_Y, LEAD_H = 160, 252
COL_W = 320
GAP = 16
X0 = 16

def pictogram_summit(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 214, 235))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 130, 145))
    # three flag poles: US, China, Russia
    flags = [((178, 34, 52), "us"), ((222, 41, 16), "cn"), ((255, 255, 255), "ru")]
    fw, fh = 74, 48
    for i, (col, _) in enumerate(flags):
        fx = x + 24 + i * (fw + 26)
        d.rectangle([fx, y + 22, fx + fw, y + 22 + fh], fill=col, outline=INK, width=2)
        d.line([fx + fw // 2, y + 22 + fh, fx + fw // 2, y + h - 26], fill=INK, width=3)
        if i == 0:  # US canton + stripes
            d.rectangle([fx, y + 22, fx + 30, y + 40], fill=NAVY)
            for s in range(3):
                d.rectangle([fx, y + 34 + s * 12, fx + fw, y + 38 + s * 12], fill=(255, 255, 255))
        if i == 1:  # China stars
            for sx, sy in [(14, 10), (28, 8), (34, 18), (28, 28), (14, 24)]:
                d.ellipse([fx + sx, y + 22 + sy, fx + sx + 7, y + 29 + sy], fill=(255, 222, 0))
        if i == 2:  # Russia tricolour
            d.rectangle([fx, y + 38, fx + fw, y + 54], fill=(0, 57, 166))
            d.rectangle([fx, y + 54, fx + fw, y + 70], fill=(213, 0, 50))
    d.text((x + w // 2, y + h - 22), "SHENZHEN", font=SANS_B(13), fill=(255, 255, 255), anchor="ma")

def pictogram_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 224))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(64, 110, 160))
    # bridge deck + arch
    d.rectangle([x, y + 62, x + w, y + 74], fill=(70, 70, 70))
    d.arc([x + 30, y - 6, x + w - 30, y + 120], 180, 360, fill=(70, 70, 70), width=6)
    d.line([x + w // 2, y + 8, x + w // 2, y + 62], fill=(70, 70, 70), width=5)
    # explosion starburst
    cx, cy = x + w // 2, y + 40
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 12, 30
        a = math.radians(ang)
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=(255, 140, 0), width=6)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 200, 40), outline=(200, 60, 0), width=3)

def pictogram_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 190))
    cx, cy = x + w // 2, y + 26
    # scales of justice
    d.line([cx, cy, cx, y + h - 22], fill=INK, width=5)
    d.line([cx - 62, cy + 8, cx + 62, cy + 8], fill=INK, width=4)
    for sx in (cx - 62, cx + 62):
        d.line([sx, cy + 8, sx, cy + 34], fill=INK, width=3)
        d.polygon([(sx - 26, cy + 34), (sx + 26, cy + 34), (sx, cy + 52)], fill=(176, 42, 32))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(212, 175, 55), outline=INK, width=2)
    d.rectangle([x + 24, y + h - 20, x + w - 24, y + h - 12], fill=INK)

LEADS = [
    ("SHENZHEN  •  APEC", "Trump, Xi and Putin hold first three-way summit",
     "The US, Chinese and Russian presidents meet in Shenzhen, with Ukraine, Iran, "
     "nuclear arms and trade on the agenda. Few concrete results are expected.",
     pictogram_summit),
    ("UKRAINE  •  CRIMEA", "Ukraine strikes Crimean Bridge for third time in a week",
     "Traffic is halted after the latest attack on the bridge linking Russia to "
     "occupied Crimea.", pictogram_bridge),
    ("THE HAGUE  •  JUSTICE", "UN court rules on Rohingya genocide case",
     "The ICJ rules in Gambia's case over the 2017 crackdown that drove 730,000 "
     "Rohingya to Bangladesh.",
     pictogram_court),
]

for i, (kick, head, summ, pic) in enumerate(LEADS):
    x = X0 + i * (COL_W + GAP)
    d.rectangle([x, LEAD_Y, x + COL_W, LEAD_Y + LEAD_H], fill=(255, 255, 255),
                outline=INK, width=2)
    pic(x + 2, LEAD_Y + 2, COL_W - 4, 96)
    ty = LEAD_Y + 106
    d.text((x + 12, ty), kick, font=SANS_B(13), fill=RED)
    ty += 20
    ty = text_block(x + 12, ty, COL_W - 24, wrap(head, SANS_B(21), COL_W - 24),
                    SANS_B(21), leading=24)
    ty += 4
    text_block(x + 12, ty, COL_W - 24, wrap(summ, SANS(14), COL_W - 24), SANS(14), leading=18)

# ---------------------------------------------------------------- region grid
GRID_Y = 428
BOX_W = 320
BOX_H = 242
ROW_GAP = 14

REGIONS = [
    ("AMERICAS", (28, 47, 87), [
        ("Anthropic's record $81bn IPO",
         "Biggest listing on record; $1.5tn valuation."),
        ("Democrats take 56-seat Senate majority",
         "An Alaska win hands Democrats the Senate."),
        ("US loses measles elimination status",
         "Country no longer meets the criteria."),
        ("Atmospheric river drenches California",
         "Record rain hits San Francisco."),
        ("US and Venezuela restore military ties",
         "The two nations sign a military pact."),
    ]),
    ("EUROPE", (90, 40, 90), [
        ("EU proposes \u20ac45bn loan for Ukraine",
         "Allies meet in Berlin; new funding unveiled."),
        ("France protests enter fourth weekend",
         "Cost-of-living marches go on nationwide."),
        ("Spain hit by general strike",
         "Police clash with protesters in walkout."),
        ("Imamoglu sentenced in Turkey",
         "Ex-mayor and eight others sentenced."),
        ("EU approves Indonesia trade deal",
         "Governments back the deal in Brussels."),
    ]),
    ("MIDDLE EAST", (140, 60, 20), [
        ("Iran hits Gulf states after US strike",
         "Tehran hits Gulf targets after US strikes."),
        ("Israel's Gaza op beyond 'yellow line'",
         "Rare ground operation in central Gaza."),
        ("Houthi missile aimed at Riyadh",
         "Riyadh plans a long Yemen campaign."),
        ("COP31 deadlock in Antalya",
         "Ministers push for a final climate text."),
        ("Eisenkot asked to form government",
         "Herzog bypasses Netanyahu for ex-army chief."),
    ]),
    ("ASIA", (150, 30, 30), [
        ("Bangladesh in turmoil",
         "Violence hits 28 districts; home torched."),
        ("North Korea expands enrichment",
         "IAEA reports more work at Yongbyon."),
        ("Cyclone Aqwan nears India's coast",
         "Storm heads for the Bay of Bengal."),
        ("South Korea's exam under AI curbs",
         "College test held amid AI-cheating curbs."),
        ("India seeks 20% defence rise",
         "Bid would fund 114 Rafale jets."),
    ]),
    ("AFRICA", (30, 110, 60), [
        ("Ethiopia and Eritrea mass troops",
         "Forces build up along the shared border."),
        ("Sudan drones drive civilian toll",
         "Aid reaches displaced at El Dabba."),
        ("Ebola vaccines trialled in DR Congo",
         "Trials begin in the east of DR Congo."),
        ("Five EU states eye Rwanda asylum plan",
         "Nations plan to send seekers to Kigali."),
        ("Nigeria: justice for 37 miners",
         "Senate demands action after custody deaths."),
    ]),
    ("OCEANIA & BEYOND", (0, 90, 110), [
        ("Fiji, Tonga declare drought emergencies",
         "El Ni\u00f1o drought grips Pacific islands."),
        ("Voyager 1 nears one light-day",
         "First human object to reach the mark."),
        ("Webb confirms rare star merger",
         "Supergiant merges with a sun-like star."),
        ("Blue whales up tenfold",
         "Antarctic numbers rebound since whaling."),
        ("1 in 4 children live in war zones",
         "A record 589 million children amid conflict."),
    ]),
]

for ri, (name, color, stories) in enumerate(REGIONS):
    col, row = ri % 3, ri // 3
    x = X0 + col * (BOX_W + GAP)
    y = GRID_Y + row * (BOX_H + ROW_GAP)
    d.rectangle([x, y, x + BOX_W, y + BOX_H], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x, y, x + BOX_W, y + 30], fill=color)
    d.text((x + 10, y + 6), name, font=SANS_B(16), fill=(255, 255, 255))
    iy = y + 40
    for head, summ in stories:
        iy = text_block(x + 10, iy, BOX_W - 20, wrap(head, SANS_B(13), BOX_W - 20),
                        SANS_B(13), leading=16)
        iy = text_block(x + 10, iy, BOX_W - 20, wrap(summ, SANS(12), BOX_W - 20),
                        SANS(12), fill=(60, 58, 52), leading=14)
        iy += 5

# ---------------------------------------------------------------- bottom strip
BY = GRID_Y + 2 * BOX_H + ROW_GAP + 8
d.rectangle([16, BY, W - 16, BY + 66], fill=NAVY)
d.text((28, BY + 6), "IN BRIEF", font=SANS_B(14), fill=(255, 210, 63))
briefs = ("Van Gogh sells for $190.4m, a record  \u2022  GTA VI on sale after 13 years  \u2022  "
          "IMF unlocks $2.3bn for Egypt  \u2022  Word of the year: \u2018human\u2019")
byy = BY + 26
for ln in wrap(briefs, SANS(13), W - 56):
    d.text((28, byy), ln, font=SANS(13), fill=(255, 255, 255))
    byy += 16
d.text((28, BY + 44), "MARKETS  S&P 500 7,324  \u22120.23%   \u2022   Hang Seng \u22122.78%   \u2022   Brent $89.3   \u2022   Gold $3,739.60",
       font=SANS_B(13), fill=(255, 255, 255))
FY = 1000
d.text((16, FY), "All stories reported on 19 November 2026. Compiled from wire and press reports.",
       font=SANS(11), fill=GREY)

img.save("entry.png", optimize=True)
import os
print("saved entry.png", os.path.getsize("entry.png"), "bytes,", img.size)
