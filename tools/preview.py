import json, html, sys
items=json.load(open('/tmp/layout.json'))
ROADS=[(150,1200,2338,76),(150,388,2338,76),(150,388,76,888),(2412,388,76,888),
       (1420,1276,88,164),(1470,96,80,300),(0,1470,2600,86)]
SET=[("স্টেডিয়াম",1288,733,392,248,"#c3b393"),("সুইমিং পুল",1594,795,208,148,"#33b2e0"),
     ("শহীদ মিনার",1130,960,224,224,"#d7cbaa"),("ইবলিশ পুকুর",360,1000,208,208,"#2d87a0"),
     ("বদ্ধভূমি",1990,520,84,84,"#cfc3a3"),("ষ্টেশন",1565,223,470,54,"#d9cfb4")]
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="810" viewBox="0 0 2600 1620">']
parts.append('<rect width="2600" height="1620" fill="#4f8a3f"/>')
for x,y,w,h in ROADS: parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6b6f66"/>')
parts.append(f'<rect x="0" y="138" width="2600" height="24" fill="#8b8377"/>')
for n,x,y,w,h,c in SET:
    parts.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="{c}" opacity=".85"/>')
    parts.append(f'<text x="{x}" y="{y+4}" font-size="16" fill="#222" text-anchor="middle">{n}</text>')
for it in items:
    x,y,w,h=it['x']-it['w']/2,it['y']-it['h']/2,it['w'],it['h']
    col={'hall':'#a9553c','ghall':'#8a5a86','library':'#9c5335','admin':'#c9a227','mosque':'#2f7d6a','medical':'#c9553f','museum':'#8d5b3a','gym':'#5f8398'}.get(it['k'],'#bb6a4a')
    parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="8" fill="{col}"/>')
    parts.append(f'<text x="{it["x"]}" y="{it["y"]+5}" font-size="15" fill="#fff" text-anchor="middle">{html.escape(it["n"][:18])}</text>')
parts.append('</svg>')
open('/tmp/preview.svg','w').write(''.join(parts))
open('/tmp/preview.html','w').write('<body style="margin:0;background:#222"><img src="preview.svg" width="1300"></body>')
print('ok')
