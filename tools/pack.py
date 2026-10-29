import json, math, sys
sys.path.insert(0,'/home/user/tools')
from geo import gx, gy
X0,X1,Y0,Y1 = 240, 2400, 478, 1186
CW,CH = 216, 118
cols = int((X1-X0)/CW); rows = int((Y1-Y0)/CH)
cells=[(X0+CW/2+c*CW, Y0+CH/2+r*CH, c, r) for r in range(rows) for c in range(cols)]
BLOCK=[  # set pieces (x,y,w,h)
 (1288,733,420,270,'stadium'),(1594,795,230,170,'pool'),(1130,960,240,240,'minar'),
 (360,1000,224,224,'iblish'),(1990,520,120,120,'boddho')]
B=[ # name, lat, lon, w, h, kind
 ("মতিহার হল",24.368837,88.642422,180,80,'hall'),
 ("সৈয়দ আমীর আলী হল",24.370655,88.646979,180,80,'hall'),
 ("শাহ মখদুম হল",24.370045,88.645254,200,90,'hall'),
 ("বরেন্দ্র হল",24.37210,88.64610,150,78,'hall'),
 ("রহিম হল",24.37195,88.64450,150,78,'hall'),
 ("নওয়াব আব্দুল লতিফ হল",24.371484,88.645372,200,84,'hall'),
 ("শহীদ শামসুজ্জোহা হল",24.373473,88.645385,176,80,'hall'),
 ("শেরে-বাংলা হল",24.36640,88.64530,165,92,'hall'),
 ("বেগম রোকেয়া হল",24.37070,88.63300,150,70,'ghall'),
 ("মন্নুজান হল",24.37000,88.63410,150,70,'ghall'),
 ("নূরজাহান হল",24.36935,88.63360,150,70,'ghall'),
 ("চন্দ্রিমা হল",24.36990,88.63530,150,70,'ghall'),
 ("বঙ্গমাতা শেখ ফজিলাতুন্নেছা হল",24.371577,88.633286,150,70,'ghall'),
 ("রহমতুন্নেসা হল",24.36920,88.63580,150,70,'ghall'),
 ("কেন্দ্রীয় গ্রন্থাগার",24.368943,88.636851,200,92,'library'),
 ("প্রশাসন ভবন-১",24.36990,88.63640,200,104,'admin'),
 ("সিনেট ভবন",24.367422,88.637015,190,90,'block'),
 ("উপাচার্য ভবন",24.36800,88.63560,190,86,'block'),
 ("প্রশাসন ভবন-২",24.36920,88.63770,150,82,'block'),
 ("অমৃতলাল ব্যানার্জী",24.36830,88.63860,130,82,'block'),
 ("প্রথম বিজ্ঞান ভবন",24.36940,88.63520,160,82,'block'),
 ("তৃতীয় বিজ্ঞান ভবন",24.36890,88.63430,170,82,'block'),
 ("দ্বিতীয় বিজ্ঞান ভবন",24.36990,88.63480,160,82,'block'),
 ("চতুর্থ বিজ্ঞান ভবন",24.36840,88.63390,160,82,'block'),
 ("একাডেমিক ভবন",24.37030,88.63600,160,60,'block'),
 ("সৈয়দ নজরুল ইসলাম ভবন",24.37060,88.63720,160,82,'block'),
 ("শিল্পকলা ভবন",24.36960,88.63850,160,82,'block'),
 ("সিরাজী কলাভবন",24.370032,88.634433,160,82,'block'),
 ("শহীদুল্লাহ কলাভবন",24.368627,88.635793,170,82,'block'),
 ("মমতাজ উদ্দিন কলাভবন",24.368618,88.634628,145,82,'block'),
 ("শহীদ স্মৃতি সংগ্রহশালা",24.36870,88.64060,92,62,'museum'),
 ("মেডিকেল সেন্টার",24.369245,88.644234,180,94,'medical'),
 ("জিমনেশিয়াম",24.47150,88.64250,110,80,'gym'),
 ("কেন্দ্রীয় জামে মসজিদ",24.367089,88.639328,200,94,'mosque'),
]
B=[x for x in B if x[0]!="জিমনেশিয়াম"]
B.append(("জিমনেশিয়াম",24.37150,88.64250,110,80,'gym'))
def hit(a,b,pad=14):
    return not (a[0]+a[2]/2+pad < b[0]-b[2]/2 or b[0]+b[2]/2+pad < a[0]-a[2]/2 or
                a[1]+a[3]/2+pad < b[1]-b[3]/2 or b[1]+b[3]/2+pad < a[1]-a[3]/2)
placed=[]
# reserve set pieces as pseudo-buildings
for x,y,w,h,t in BLOCK: placed.append((x,y,w,h,t))
north=[("মাদার বখশ হল",24.37485,88.64160,195,82,'hall',1362),
       ("শহীদ সোহরাওয়ার্দী হল",24.37480,88.64410,195,82,'hall',1681),
       ("শহীদ হবিবুর রহমান হল",24.374136,88.638536,185,82,'hall',971),
       ("শহীদ জিয়াউর রহমান হল",24.374114,88.640487,185,82,'hall',1220)]
out=[]
for n,la,lo,w,h,k,_gx in north:
    out.append(dict(n=n,x=round(gx(lo)),y=322,w=w,h=h,k=k))
order=sorted(B,key=lambda b:math.hypot(gx(b[2]),gy(b[1])))  # not meaningful; keep list order
for n,la,lo,w,h,k in B:
    tx,ty=gx(lo),gy(la)
    best=None;bd=1e9
    for (cx,cy,c,r) in cells:
        cand=(cx,cy,w,h)
        if any(hit(cand,p,10) for p in placed): continue
        # keep inside the ring
        if cx-w/2<232 or cx+w/2>2406 or cy-h/2<472 or cy+h/2>1192: continue
        d=math.hypot(cx-tx,cy-ty)
        if d<bd: bd=d;best=(cx,cy)
    if best is None:
        print('NO CELL',n); continue
    placed.append((best[0],best[1],w,h,n))
    out.append(dict(n=n,x=round(best[0]),y=round(best[1]),w=w,h=h,k=k,tx=round(tx),ty=round(ty)))
json.dump(out,open('/tmp/layout.json','w'),ensure_ascii=False)
for o in out:
    print(f"{o['n'][:26]:28s} {o['k']:8s} ({o['x']:4d},{o['y']:4d})  geo({o.get('tx','-'):>4},{o.get('ty','-'):>4})" if 'tx' in o else f"{o['n'][:26]:28s} {o['k']:8s} ({o['x']:4d},{o['y']:4d})")
# verify
bad=0
for i in range(len(out)):
    for j in range(i+1,len(out)):
        a,b=out[i],out[j]
        if hit((a['x'],a['y'],a['w'],a['h']),(b['x'],b['y'],b['w'],b['h']),2): bad+=1; print('OVL',a['n'],b['n'])
print('overlaps:',bad,'| cells',cols,'x',rows)
