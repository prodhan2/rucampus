"""Place the campus buildings at their real OpenStreetMap positions.

Targets are OSM way/node centroids converted with geo.py's transform
(gx/gy).  A building keeps its true spot unless it would overlap an
already-placed building, a set-piece block or a road: then it is nudged
by the smallest offset that clears everything.
"""
import json, math

X0, LON0, SX = 1565.0, 88.643191, 127700.0
Y0, LAT0, SY = 223.0, 24.375464, 106030.0
gx = lambda lon: X0 + (lon - LON0) * SX
gy = lambda lat: Y0 + (LAT0 - lat) * SY

SZ = {'hall': (150, 64), 'ghall': (120, 56), 'block': (118, 56),
      'library': (144, 66), 'mosque': (162, 78), 'medical': (146, 76),
      'gym': (112, 64), 'museum': (150, 60), 'admin': (300, 136)}

# name, kind, lat, lon  (None,None → use the explicit world xy in the 3rd slot)
B = [
 ('শহীদ হবিবুর রহমান হল','hall',24.374136,88.638536),
 ('শহীদ জিয়াউর রহমান হল','hall',24.374114,88.640487),
 ('মাদার বখশ হল','hall',24.37327,88.642090),
 ('শহীদ সোহরাওয়ার্দী হল','hall',24.37360,88.644200),
 ('শহীদ শামসুজ্জোহা হল','hall',24.373473,88.645385),
 ('নওয়াব আব্দুল লতিফ হল','hall',24.371484,88.645372),
 ('শাহ মখদুম হল','hall',24.370045,88.645254),
 ('সৈয়দ আমীর আলী হল','hall',24.370655,88.646979),
 ('মতিহার হল','hall',24.368837,88.642422),
 ('বরেন্দ্র হল','hall',24.372800,88.647400),
 ('রহিম হল','hall',24.372400,88.644800),
 ('শেরে-বাংলা হল','hall',24.367200,88.646600),
 ('বঙ্গমাতা শেখ ফজিলাতুন্নেছা হল','ghall',24.371577,88.633286),
 ('বেগম রোকেয়া হল','ghall',24.371240,88.633930),
 ('নূরজাহান হল','ghall',24.370900,88.634100),
 ('মন্নুজান হল','ghall',24.370970,88.634900),
 ('চন্দ্রিমা হল','ghall',24.370500,88.635900),
 ('রহমতুন্নেসা হল','ghall',24.369900,88.636500),
 ('সিরাজী কলাভবন','block',24.370032,88.634433),
 ('মমতাজ উদ্দিন কলাভবন','block',24.368618,88.634628),
 ('শহীদুল্লাহ কলাভবন','block',24.368627,88.635793),
 ('চতুর্থ বিজ্ঞান ভবন','block',24.371371,88.636806),
 ('দ্বিতীয় বিজ্ঞান ভবন','block',24.371185,88.638156),
 ('তৃতীয় বিজ্ঞান ভবন','block',24.370962,88.638029),
 ('প্রথম বিজ্ঞান ভবন','block',24.370078,88.638214),
 ('সৈয়দ নজরুল ইসলাম ভবন','block',24.369900,88.639100),
 ('শিল্পকলা ভবন','block',24.370400,88.637300),
 ('একাডেমিক ভবন','block',24.370100,88.636100),
 ('অমৃতলাল ব্যানার্জী','block',24.368900,88.640100),
 ('প্রশাসন ভবন-২','block',24.368600,88.638400),
 ('উপাচার্য ভবন','block',24.367700,88.637000),
 ('সিনেট ভবন','block',24.367422,88.637015),
 ('কেন্দ্রীয় গ্রন্থাগার','library',24.368943,88.636851),
 ('কেন্দ্রীয় জামে মসজিদ','mosque',24.367089,88.639328),
 ('মেডিকেল সেন্টার','medical',24.369245,88.644234),
 ('জিমনেশিয়াম','gym',24.37160,88.64560),
 ('শহীদ স্মৃতি সংগ্রহশালা','museum',24.367981,88.640264),
]

# set-piece keep-outs (x,y,w,h)
BLOCK = [
 (1104, 596, 392, 248),   # stadium
 (1506, 738, 176, 120),   # swimming pool
 (1044, 874, 172, 172),   # Shaheed Minar plaza
 (250, 946, 170, 124),    # ইবলিশ পুকুর
 (1944, 414, 112, 112),   # বধ্যভূমি
 (1330, 196, 470, 54),    # station platform
 (700, 1330, 330, 150),   # main gate forecourt
 (548, 722, 300, 136),    # প্রশাসন ভবন-১ (drawn by drawAdminBuilding)
]
# roads
ROADS = [
 (150, 506, 2338, 72), (150, 1200, 2338, 76),
 (150, 506, 76, 770), (2412, 506, 76, 770),
 (816, 1276, 88, 164), (1470, 96, 80, 412),
 (0, 1470, 2600, 86), (1450, 1120, 1150, 48),
]

def ov(a, b, m=0):
    return (min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0]) > -m and
            min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1]) > -m)

placed, out = [], []
PRIO = ('library','mosque','medical','museum','gym','hall','ghall','block')
order = sorted(B, key=lambda t: PRIO.index(t[1]))
for name, kind, lat, lon in order:
    w, h = SZ[kind]
    tx, ty = gx(lon), gy(lat)
    best = None
    for r in range(0, 21):
        step = r * 14
        cand = [(tx, ty)] if r == 0 else [
            (tx + dx, ty + dy) for dx in (-step, 0, step) for dy in (-step, 0, step)
            if dx or dy]
        for cx, cy in cand:
            rect = (cx - w/2, cy - h/2, w, h)
            if rect[0] < 240 or rect[1] < 260 or rect[0]+w > 2360 or rect[1]+h > 1430:
                continue
            if any(ov(rect, p, 10) for p in placed): continue
            if any(ov(rect, b, 4) for b in BLOCK): continue
            if any(ov(rect, r2, 2) for r2 in ROADS): continue
            best = (cx, cy, rect); break
        if best: break
    if not best:
        rect = (tx-w/2, ty-h/2, w, h)
        why = []
        for p in placed:
            if ov(rect, p, 10): why.append(('bld', p))
        for b in BLOCK:
            if ov(rect, b, 4): why.append(('blk', b))
        for r2 in ROADS:
            if ov(rect, r2, 2): why.append(('road', r2))
        print('FAILED', name, rect, why[:2]); best = (tx, ty, rect)
    placed.append(best[2])
    d = math.hypot(best[0]-tx, best[1]-ty)
    out.append(dict(n=name, k=kind, x=round(best[0]), y=round(best[1]), w=w, h=h,
                    d=round(d)))

worst = sorted(out, key=lambda o: -o['d'])[:6]
for o in out:
    flag = '  <<' if o['d'] > 140 else ''
    print(f"{o['n'][:26]:28s} {o['k']:8s} ({o['x']:5d},{o['y']:5d}) d={o['d']:3d}{flag}")
print('max drift:', worst[0]['n'], worst[0]['d'])
json.dump(out, open('/tmp/layout3.json', 'w'), ensure_ascii=False)

lines = []
for k in ['hall', 'ghall', 'gym', 'library', 'admin', 'medical', 'mosque', 'museum', 'block']:
    grp = [o for o in out if o['k'] == k]
    if not grp: continue
    lines.append(f"  /* ───── {k} ───── */")
    for o in grp:
        lines.append(f"  {{x:{o['x']-o['w']//2},y:{o['y']-o['h']//2},w:{o['w']},"
                     f"h:{o['h']},l:'{o['n']}',k:'{o['k']}'}},")
open('/tmp/bld3.js', 'w').write('\n'.join(lines) + '\n')
print('written /tmp/bld3.js')
