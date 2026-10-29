"""Emit a standalone SVG campus map from the exact geometry in the game file.

Reads the BLD array + the landmark list out of ru-campus-tour.html so the
poster can never drift from what the game draws.
"""
import re, json

src = open('/home/user/ru-campus-tour.html').read()

bld = []
for m in re.finditer(r"\{x:(-?\d+),y:(-?\d+),w:(\d+),h:(\d+),l:'([^']+)',k:'([a-z]+)'\}", src):
    bld.append(dict(x=int(m.group(1)), y=int(m.group(2)), w=int(m.group(3)),
                    h=int(m.group(4)), l=m.group(5), k=m.group(6)))

lm = []
lmblk = src[src.index('const LANDMARKS=['):src.index('const RING_ROUTE=[')]
for m in re.finditer(r"id:'([a-z]+)',name:'([^']+)',en:'[^']*',icon:'[^']*',x:(\d+),y:(\d+)", lmblk):
    lm.append(dict(id=m.group(1), name=m.group(2), x=int(m.group(3)), y=int(m.group(4))))

W, H = 2600, 1900
out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" '
  'font-family="Hind Siliguri, Noto Sans Bengali, system-ui, sans-serif">')
A('<defs>'
  '<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#dcebc7"/><stop offset="1" stop-color="#d2e4b9"/></linearGradient>'
  '<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
  '<feDropShadow dx="3" dy="5" stdDeviation="5" flood-color="#41502f" flood-opacity="0.18"/></filter>'
  '</defs>')
A(f'<rect width="{W}" height="{H}" fill="#eceae3"/>')

# town blocks
for x in range(-40, W + 200, 192):
    for y in range(-40, H + 170, 158):
        A(f'<rect x="{x+10}" y="{y+10}" width="160" height="126" rx="8" fill="#f6f4ee"/>')

# campus green
A('<rect x="44" y="304" width="2492" height="1150" rx="30" fill="#d9e8c4"/>')
A('<rect x="150" y="392" width="2280" height="1000" rx="24" fill="url(#grass)"/>')

# railway
A('<rect x="0" y="132" width="2600" height="36" fill="#cfccc2"/>')
A('<line x1="0" y1="150" x2="2600" y2="150" stroke="#fff" stroke-width="3" stroke-dasharray="18 15"/>')

roads = [(150, 1200, 2338, 76), (150, 506, 2338, 72), (150, 506, 76, 770),
         (2412, 506, 76, 770), (816, 1276, 88, 164), (1470, 96, 80, 412),
         (196, 1276, 72, 110), (1714, 1276, 72, 110)]
for x, y, w, h in roads:
    A(f'<rect x="{x-5}" y="{y-5}" width="{w+10}" height="{h+10}" rx="8" fill="#e2ded2"/>')
for x, y, w, h in roads:
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#ffffff"/>')
A('<rect x="0" y="1470" width="2600" height="86" fill="#fcf2cf"/>')
# bus stand
A('<rect x="866" y="1552" width="1648" height="338" rx="18" fill="#d8d2c0"/>')
A('<rect x="880" y="1562" width="1620" height="318" rx="14" fill="#a9a598"/>')
A('<rect x="890" y="1586" width="1600" height="52" rx="10" fill="#7c7a73"/>')
for i in range(20):
    bx0 = 944 + i*70
    A(f'<rect x="{bx0-26}" y="1735" width="52" height="84" rx="6" fill="#e8e6df"/>')
A('<rect x="1150" y="1556" width="470" height="30" rx="8" fill="#e9dfc6"/>')
A('<rect x="1180" y="1520" width="410" height="34" rx="8" fill="#1f5f8f"/>')
A('<text x="1385" y="1543" font-size="19" font-weight="800" fill="#eaf6ff" text-anchor="middle">রাবি বাস স্ট্যান্ড · ২০টি বাস</text>')
# food street
names = ['চায়ের দোকান','বিরিয়ানি','ফুচকা','রুটি-ডাল','বার্গার','মিষ্টি','চটপটি','কাবাব','সিঙ্গারা','লুচি','জুস','আইসক্রিম','নুডলস','কফি']
cols = ['#c4553a','#2f7d4a','#c98a2e','#8a5a3a','#b8543a','#a9553c','#2f8a6a','#8e4a7a','#c08a2e','#3f6ea8','#2f6fb0','#6a4fa0','#c4553a','#6b4a36']
xs = [1000]+[1096,1204,1312,1420,1528]+[1888,1996,2104,2212,2320,2428,2440]
for i,x in enumerate(xs):
    A(f'<rect x="{x}" y="1332" width="96" height="74" rx="5" fill="#f3efe5" stroke="#d6d0c0" stroke-width="1.6"/>')
    A(f'<rect x="{x}" y="1332" width="96" height="10" rx="4" fill="{cols[i%len(cols)]}"/>')
A('<rect x="1060" y="1288" width="1470" height="58" rx="10" fill="#e6d9bd"/>')
for i,x in enumerate(xs):
    A(f'<text x="{x+48}" y="1424" font-size="12" font-weight="600" fill="#4a4433" text-anchor="middle">{names[i%len(names)]}</text>')
A('<text x="1084" y="1252" font-size="18" font-weight="800" fill="#8a4a2a" text-anchor="middle">খাবারের গলি</text>')

# set pieces
A('<ellipse cx="1288" cy="733" rx="202" ry="130" fill="#e9e2d2" stroke="#d2c9b4" stroke-width="3"/>')
A('<ellipse cx="1288" cy="733" rx="152" ry="88" fill="#c6dda7" stroke="#aacb8b" stroke-width="2"/>')
A('<rect x="1276" y="672" width="24" height="124" rx="4" fill="#e8dbb6"/>')
A('<rect x="1506" y="735" width="176" height="120" rx="12" fill="#84bedd"/>')
A('<rect x="1514" y="743" width="160" height="104" rx="9" fill="#a8d7ef"/>')
A('<rect x="230" y="1090" width="180" height="100" rx="5" fill="#c3dca3" stroke="#fff" stroke-width="3"/>')
A('<text x="320" y="1218" font-size="13" font-weight="600" fill="#3d4a37" text-anchor="middle">ফুটবল মাঠ</text>')
A('<ellipse cx="400" cy="1035" rx="92" ry="64" fill="#e3e0d1"/>')
A('<ellipse cx="400" cy="1035" rx="78" ry="51" fill="#84bedd"/>')
A('<ellipse cx="400" cy="1035" rx="72" ry="46" fill="#a8d7ef"/>')
A('<circle cx="1130" cy="960" r="94" fill="#e7e1d1"/>')
A('<circle cx="1130" cy="960" r="24" fill="#f6f3ea"/>')
A('<circle cx="2000" cy="470" r="30" fill="#e2ded0" stroke="#cdd8bd" stroke-width="3"/>')
A('<circle cx="860" cy="1238" r="46" fill="#d3e3ba" stroke="#e5e1d4" stroke-width="7"/>')

# buildings
for b in bld:
    r = 12 if b['k'] == 'mosque' else 6
    A(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="{r}" '
      f'fill="#f3efe5" stroke="#d6d0c0" stroke-width="1.8"/>')
A('<rect x="548" y="686" width="300" height="136" rx="12" fill="#f3efe5" stroke="#d6d0c0" stroke-width="1.8"/>')
A('<rect x="1330" y="196" width="470" height="54" rx="8" fill="#f3efe5" stroke="#d6d0c0" stroke-width="1.8"/>')

# wall + gates
A('<rect x="40" y="300" width="2500" height="1158" rx="26" fill="none" stroke="#c7c1af" stroke-width="7"/>')
for gx in (860, 232, 1750):
    A(f'<rect x="{gx-27}" y="1436" width="54" height="26" rx="6" fill="#a4b391"/>')

# hall / building names
label = {'hall': 13.5, 'ghall': 12.5, 'library': 14, 'medical': 13.5, 'mosque': 14, 'gym': 12.5}
lmboxes = []
for b in bld:
    fs = label.get(b['k'])
    if not fs:
        continue
    cx, cy = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
    A(f'<text x="{cx}" y="{cy+fs*0.35}" font-size="{fs}" font-weight="600" fill="#3d4a37" '
      f'text-anchor="middle">{b["l"]}</text>')
    half = len(b['l']) * fs * 0.55 / 2
    lmboxes.append((cx - half, cy - 10, cx + half, cy + 6))

# landmark pins
for l in lm:
    x, y = l['x'], l['y']
    A(f'<g><path d="M{x},{y} C{x-15},{y-15} {x-17},{y-35} {x},{y-35} '
      f'C{x+17},{y-35} {x+15},{y-15} {x},{y} Z" fill="#e0563c" stroke="#fff" stroke-width="3"/>'
      f'<circle cx="{x}" cy="{y-25}" r="5.6" fill="#fff"/></g>')

# landmark names with a soft halo, nudged so they never collide
halo = ('<text x="%d" y="%d" font-size="17" font-weight="700" fill="#2d3c2a" text-anchor="middle" '
        'stroke="#ffffff" stroke-width="5" paint-order="stroke">%s</text>')
placed = list(lmboxes)
for l in lm:
    x, y = l['x'], l['y']
    half = len(l['name']) * 17 * 0.55 / 2
    for dx, dy in ((0, 30), (0, -48), (half + 40, -6), (-half - 40, -6),
                   (0, 48), (0, -66), (half + 46, 22), (-half - 46, 22)):
        px, py = x + dx, y + dy
        box = (px - half, py - 15, px + half, py + 8)
        if any(not (box[2] < o[0] or box[0] > o[2] or box[3] < o[1] or box[1] > o[3]) for o in placed):
            continue
        placed.append(box)
        A(halo % (px, py, l['name']))
        break

# title block
A('<g filter="url(#sh)"><rect x="60" y="40" width="700" height="150" rx="18" fill="#fdf8ec"/></g>')
A('<text x="98" y="128" font-size="40" font-weight="800" fill="#2d3c2a">রাজশাহী বিশ্ববিদ্যালয়</text>')
A('<text x="98" y="164" font-size="19" font-weight="600" fill="#6b7358">ক্যাম্পাস ম্যাপ · ৭৫৩ একর · স্থানাঙ্ক অনুযায়ী বসানো</text>')
A('<text x="98" y="192" font-size="16" fill="#8a8f7a">OpenStreetMap · 88.622–88.660 E, 24.360–24.378 N</text>')

# north arrow + scale
A('<g transform="translate(2430,1010)">'
  '<circle r="46" fill="#fdf8ec" opacity="0.95"/>'
  '<path d="M0,-32 L12,10 L0,2 L-12,10 Z" fill="#e0563c"/>'
  '<text y="30" font-size="17" font-weight="700" text-anchor="middle" fill="#3d4a37">উত্তর</text></g>')
A('<g transform="translate(126,1580)">'
  '<rect x="-14" y="-40" width="300" height="62" rx="10" fill="#fdf8ec" opacity="0.96"/>'
  '<rect width="200" height="8" fill="#3d4a37"/><rect x="100" width="100" height="8" fill="#fff" stroke="#3d4a37"/>'
  '<text y="-10" font-size="15" font-weight="600" fill="#3d4a37">০</text>'
  '<text x="200" y="-10" font-size="15" font-weight="600" fill="#3d4a37" text-anchor="end">প্রায় ৫০০ মিটার</text></g>')

A('</svg>')
open('/home/user/campus-map.svg', 'w').write('\n'.join(out))
print('wrote campus-map.svg —', len(bld), 'buildings,', len(lm), 'landmarks')
