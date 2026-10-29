import json, math, sys
sys.path.insert(0,'/home/user/tools')
from geo import gx, gy
W,H=2600,1620
ROADS=[(150,1200,2338,76),(150,388,2338,76),(150,388,76,888),(2412,388,76,888),
       (1420,1276,88,164),(1470,96,80,300),(0,1470,2600,86)]
IN_L,IN_R,IN_T,IN_B = 232,2406,470,1194
SET=[('stadium',1288,733),('pool',1594,795),('minar',1130,960),('iblish',360,1000),
     ('boddho',1990,520),('station',1565,223)]
OBST=[(1092,609,392,248),(1490,717,208,148),(1018,848,224,224),(256,896,208,208),
      (1330,196,470,54),(1349,1376,230,82),(1960,470,120,120)]
# name, lat, lon, w, h, kind, zone
B=[
 ("মাদার বখশ হল",24.37485,88.64160,200,84,'hall','north'),
 ("শহীদ সোহরাওয়ার্দী হল",24.37480,88.64410,200,84,'hall','north'),
 ("শহীদ হবিবুর রহমান হল",24.374136,88.638536,190,84,'hall','north'),
 ("শহীদ জিয়াউর রহমান হল",24.374114,88.640487,190,84,'hall','north'),
 ("মতিহার হল",24.368837,88.642422,185,82,'hall','in'),
 ("সৈয়দ আমীর আলী হল",24.370655,88.646979,185,82,'hall','in'),
 ("শাহ মখদুম হল",24.370045,88.645254,235,92,'hall','in'),
 ("বরেন্দ্র হল",24.37210,88.64610,150,84,'hall','in'),
 ("রহিম হল",24.37195,88.64450,150,84,'hall','in'),
 ("নওয়াব আব্দুল লতিফ হল",24.371484,88.645372,235,88,'hall','in'),
 ("শহীদ শামসুজ্জোহা হল",24.373473,88.645385,176,84,'hall','in'),
 ("শেরে-বাংলা হল",24.36640,88.64530,165,100,'hall','in'),
 ("বেগম রোকেয়া হল",24.37070,88.63300,150,72,'ghall','in'),
 ("মন্নুজান হল",24.37000,88.63410,150,72,'ghall','in'),
 ("নূরজাহান হল",24.36935,88.63360,150,72,'ghall','in'),
 ("চন্দ্রিমা হল",24.36990,88.63530,150,72,'ghall','in'),
 ("বঙ্গমাতা শেখ ফজিলাতুন্নেছা হল",24.371577,88.633286,150,72,'ghall','in'),
 ("রহমতুন্নেসা হল",24.36920,88.63580,150,72,'ghall','in'),
 ("কেন্দ্রীয় গ্রন্থাগার",24.368943,88.636851,230,100,'library','in'),
 ("প্রশাসন ভবন-১",24.36990,88.63640,310,112,'admin','in'),
 ("সিনেট ভবন",24.367422,88.637015,200,96,'block','in'),
 ("উপাচার্য ভবন",24.36800,88.63560,210,92,'block','in'),
 ("প্রশাসন ভবন-২",24.36920,88.63770,150,86,'block','in'),
 ("অমৃতলাল ব্যানার্জী",24.36830,88.63860,130,86,'block','in'),
 ("প্রথম বিজ্ঞান ভবন",24.36940,88.63520,170,86,'block','in'),
 ("তৃতীয় বিজ্ঞান ভবন",24.36890,88.63430,180,86,'block','in'),
 ("দ্বিতীয় বিজ্ঞান ভবন",24.36990,88.63480,165,86,'block','in'),
 ("চতুর্থ বিজ্ঞান ভবন",24.36840,88.63390,165,86,'block','in'),
 ("একাডেমিক ভবন",24.37030,88.63600,160,60,'block','in'),
 ("সৈয়দ নজরুল ইসলাম ভবন",24.37060,88.63720,160,86,'block','in'),
 ("শিল্পকলা ভবন",24.36960,88.63850,160,86,'block','in'),
 ("সিরাজী কলাভবন",24.370032,88.634433,160,86,'block','in'),
 ("শহীদুল্লাহ কলাভবন",24.368627,88.635793,175,86,'block','in'),
 ("মমতাজ উদ্দিন কলাভবন",24.368618,88.634628,145,86,'block','in'),
 ("শহীদ স্মৃতি সংগ্রহশালা",24.36870,88.64060,92,62,'museum','in'),
 ("মেডিকেল সেন্টার",24.369245,88.644234,185,104,'medical','in'),
 ("জিমনেশিয়াম",24.37150,88.64250,112,84,'gym','in'),
 ("কেন্দ্রীয় জামে মসজিদ",24.367089,88.639328,215,100,'mosque','in'),
]
items=[]
for i,(n,la,lo,w,h,k,z) in enumerate(B):
    items.append(dict(n=n,x=gx(lo)+((i*37)%23-11),y=gy(la)+((i*53)%19-9),tx=gx(lo),ty=gy(la),w=w,h=h,k=k,zone=z))

def rect(i): return (i['x']-i['w']/2,i['y']-i['h']/2,i['w'],i['h'])
def pen(a,b,pad):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    ox=min(ax+aw,bx+bw)-max(ax,bx)+pad
    oy=min(ay+ah,by+bh)-max(ay,by)+pad
    return (ox,oy) if ox>0 and oy>0 else (0,0)

for it in range(2600):
    for o in items:
        o['x']+=(o['tx']-o['x'])*0.02; o['y']+=(o['ty']-o['y'])*0.02
    for i in range(len(items)):
        for j in range(i+1,len(items)):
            a,b=items[i],items[j]; ox,oy=pen(rect(a),rect(b),22)
            if ox and oy:
                if ox<oy:
                    s=(ox/2)*0.55; a['x']-= s if a['x']<b['x'] else -s; b['x']+= s if a['x']<b['x'] else -s
                else:
                    s=(oy/2)*0.55; a['y']-= s if a['y']<b['y'] else -s; b['y']+= s if a['y']<b['y'] else -s
    for a in items:
        for (rx,ry,rw,rh) in OBST:
            ox,oy=pen(rect(a),(rx,ry,rw,rh),16)
            if ox and oy:
                if ox<oy: a['x']+= ox if a['x']>rx+rw/2 else -ox
                else:     a['y']+= oy if a['y']>ry+rh/2 else -oy
        for r in ROADS:
            ox,oy=pen(rect(a),r,16)
            if ox and oy:
                if ox<oy: a['x']+= ox if a['x']>r[0]+r[2]/2 else -ox
                else:     a['y']+= oy if a['y']>r[1]+r[3]/2 else -oy
        if a['zone']=='north':
            a['x']=min(max(a['x'],a['w']/2+70),W-a['w']/2-70); a['y']=min(max(a['y'],252+a['h']/2),444)
        else:
            a['x']=min(max(a['x'],IN_L+a['w']/2),IN_R-a['w']/2)
            a['y']=min(max(a['y'],IN_T+a['h']/2),IN_B-a['h']/2)
for a in items: a['x']=round(a['x']); a['y']=round(a['y'])
json.dump(items,open('/tmp/layout.json','w'),ensure_ascii=False)
bad=0
for i in range(len(items)):
    for j in range(i+1,len(items)):
        ox,oy=pen(rect(items[i]),rect(items[j]),0)
        if ox and oy: bad+=1; print('OVERLAP',items[i]['n'],items[j]['n'],round(ox),round(oy))
print('overlaps:',bad)
print('max drift:',max(math.hypot(a['x']-a['tx'],a['y']-a['ty']) for a in items))
