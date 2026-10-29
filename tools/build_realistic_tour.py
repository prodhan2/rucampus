import json

with open(r'C:\Users\ACER\Downloads\rajshahi-campus-tour\tools\campus_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

buildings = data['buildings']
landmarks = data['landmarks']

extra_landmarks = [
  {
    "id": "sabash",
    "name": "সাবাশ বাংলাদেশ",
    "en": "Sabash Bangladesh Sculpture",
    "icon": "✊",
    "x": 660,
    "y": 1080,
    "r": 110,
    "fact": "১৯৭১ সালের মহান মুক্তিযুদ্ধের স্মারক হিসেবে ভাস্কর নিতুন কুণ্ডুর অমর সৃষ্টি 'সাবাশ বাংলাদেশ'। সিনেট ভবনের দক্ষিণ পাশে উন্মুক্ত চত্বরে রাইফেল উঁচিয়ে দাঁড়িয়ে থাকা দুই মুক্তিযোদ্ধার ভাস্কর্য আর লাল সূর্যের প্রাচীর — রাজশাহী বিশ্ববিদ্যালয়ের চিরন্তন অহংকার।"
  },
  {
    "id": "tukitaki",
    "name": "টুকিটাকি চত্বর",
    "en": "Tukitaki Chattar",
    "icon": "☕",
    "x": 760,
    "y": 990,
    "r": 100,
    "fact": "কেন্দ্রীয় লাইব্রেরির পাশে রাজশাহী বিশ্ববিদ্যালয়ের সবচেয়ে প্রাণবন্ত চত্বর — 'টুকিটাকি চত্বর'। আড্ডা, বিতর্ক, রাজনীতি, কবিতা, চা আর পরোটার গন্ধে মুখর শিক্ষার্থীদের প্রিয় মিলনমেলা।"
  },
  {
    "id": "zoha",
    "name": "শহীদ ড. জোহা চত্বর",
    "en": "Dr. Zoha Memorial",
    "icon": "🕯️",
    "x": 860,
    "y": 1240,
    "r": 105,
    "fact": "১৯৬৯ সালের গণঅভ্যুত্থানের মহান শহীদ ও রাবির তৎকালীন প্রক্টর ড. শামসুজ্জোহার স্মরণে নির্মিত চত্বর। শিক্ষার্থীদের বাঁচাতে গিয়ে পাকিস্তানি বাহিনীর বুলেটে তিনি শহীদ হন। তাঁর অমর উক্তি: 'আমার কোনো ছাত্রের গায়ে গুলি লাগার আগে সে গুলি আমার বুকে লাগবে'।"
  }
]

all_landmarks = landmarks + extra_landmarks
buildings_json = json.dumps(buildings, ensure_ascii=False)
landmarks_json = json.dumps(all_landmarks, ensure_ascii=False)

html_content = r'''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>Rajshahi University 3D — Real Campus & Helicopter Tour (রাবি ৩ডি রিয়েল ট্যুর)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Hind+Siliguri:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --vc-pink: #ff2a8d;
    --vc-cyan: #00e5ff;
    --vc-yellow: #ffea00;
    --vc-orange: #ff7700;
    --ru-navy: #0b2545;
    --ru-gold: #ffd700;
    --bn-font: 'Hind Siliguri', 'Segoe UI', system-ui, sans-serif;
  }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body {
    margin: 0; padding: 0; width: 100%; height: 100%;
    overflow: hidden; background: #000; font-family: var(--bn-font);
    user-select: none; -webkit-user-select: none;
  }
  #c {
    display: block; width: 100vw; height: 100vh; position: absolute; inset: 0; z-index: 1;
  }

  /* ═══════════ VICE CITY HUD ═══════════ */
  #hud {
    position: fixed; inset: 0; pointer-events: none; z-index: 10;
  }

  /* Top Right Stats */
  #top-right {
    position: absolute; top: 16px; right: 20px;
    display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
  }
  .vc-clock {
    font-family: 'Orbitron', monospace; font-size: 26px; font-weight: 900;
    color: var(--vc-yellow); text-shadow: 0 0 12px rgba(255, 234, 0, 0.8), 2px 2px 0 #000;
    letter-spacing: 2px;
  }
  .vc-bars {
    display: flex; flex-direction: column; gap: 5px; width: 190px;
  }
  .bar-row {
    display: flex; align-items: center; gap: 8px;
    background: rgba(0, 0, 0, 0.65); padding: 3px 8px; border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.15);
  }
  .bar-icon { font-size: 15px; width: 20px; text-align: center; }
  .bar-track {
    flex: 1; height: 12px; background: rgba(255, 255, 255, 0.15);
    border-radius: 4px; overflow: hidden; position: relative;
  }
  .bar-fill {
    height: 100%; width: 100%; border-radius: 3px;
    transition: width 0.2s ease;
  }
  .health-fill {
    background: linear-gradient(90deg, #ff0055, var(--vc-pink));
    box-shadow: 0 0 10px var(--vc-pink);
  }
  .armor-fill {
    background: linear-gradient(90deg, #0088cc, var(--vc-cyan));
    box-shadow: 0 0 10px var(--vc-cyan);
  }
  .bar-val {
    font-family: 'Orbitron', monospace; font-size: 12px; font-weight: 700;
    color: #fff; width: 32px; text-align: right;
  }
  .vc-cash {
    font-family: 'Orbitron', monospace; font-size: 24px; font-weight: 900;
    color: #55ff55; text-shadow: 0 0 10px #00aa00, 2px 2px 0 #000;
    letter-spacing: 2px;
  }
  .vc-stars {
    font-size: 20px; color: #444; letter-spacing: 2px;
  }
  .vc-stars .lit {
    color: var(--vc-yellow); text-shadow: 0 0 10px var(--vc-yellow);
  }

  .vc-weapon {
    width: 68px; height: 68px; border-radius: 12px;
    background: radial-gradient(circle, rgba(255,42,141,0.25), rgba(0,0,0,0.85));
    border: 2px solid var(--vc-pink); box-shadow: 0 0 15px rgba(255,42,141,0.5);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative;
  }
  .vc-weapon .w-icon { font-size: 32px; line-height: 1; }
  .vc-weapon .w-ammo {
    position: absolute; bottom: 3px; right: 5px;
    font-family: 'Orbitron', monospace; font-size: 10px; font-weight: 900;
    color: var(--vc-cyan);
  }

  /* Bottom Left Radar Minimap */
  #radar-box {
    position: absolute; bottom: 20px; left: 20px;
    width: 175px; height: 175px; border-radius: 50%;
    border: 3.5px solid var(--vc-cyan);
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.6), inset 0 0 20px rgba(0,0,0,0.8);
    background: rgba(10, 20, 25, 0.88);
    overflow: hidden; pointer-events: auto;
  }
  #radar {
    width: 100%; height: 100%; display: block;
  }
  .radar-n {
    position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
    font-family: 'Orbitron', monospace; font-size: 12px; font-weight: 900;
    color: var(--vc-pink); text-shadow: 0 0 6px var(--vc-pink);
    pointer-events: none;
  }

  /* Action Prompt */
  #action-prompt {
    position: absolute; bottom: 85px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 5, 20, 0.92); border: 2px solid var(--vc-yellow);
    border-radius: 30px; padding: 10px 24px; color: #fff;
    font-size: 16px; font-weight: 700; display: none; align-items: center; gap: 10px;
    box-shadow: 0 0 25px rgba(255, 234, 0, 0.6); backdrop-filter: blur(8px);
    animation: promptBounce 0.6s infinite alternate ease-in-out;
  }
  @keyframes promptBounce { from { transform: translateX(-50%) translateY(0); } to { transform: translateX(-50%) translateY(-6px); } }
  #action-prompt kbd {
    background: var(--vc-yellow); color: #000; padding: 3px 10px;
    border-radius: 6px; font-family: 'Orbitron', monospace; font-size: 14px; font-weight: 900;
  }

  /* Speedometer & Altitude Meter */
  #speedo {
    position: absolute; bottom: 24px; right: 24px;
    background: rgba(10, 5, 24, 0.9); border: 2px solid var(--vc-pink);
    border-radius: 16px; padding: 12px 20px; display: none;
    flex-direction: column; align-items: flex-end;
    box-shadow: 0 0 22px rgba(255, 42, 141, 0.6); backdrop-filter: blur(8px);
  }
  #speedo .veh-name {
    font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
    color: var(--vc-cyan); font-weight: 700;
  }
  #speedo .speed-num {
    font-family: 'Orbitron', monospace; font-size: 34px; font-weight: 900;
    color: #fff; text-shadow: 0 0 12px var(--vc-pink); line-height: 1; margin: 4px 0 2px;
  }
  #speedo .speed-unit {
    font-size: 11px; color: #aaa; letter-spacing: 1px; font-weight: 600;
  }
  #speedo .alt-row {
    margin-top: 6px; padding-top: 4px; border-top: 1px solid rgba(255,255,255,0.15);
    font-family: 'Orbitron', monospace; font-size: 13px; font-weight: 700;
    color: var(--vc-yellow); display: none;
  }

  /* Mission Banner */
  #mission-banner {
    position: absolute; top: 110px; left: 50%; transform: translateX(-50%) scale(0.8);
    display: none; flex-direction: column; align-items: center; text-align: center;
    background: linear-gradient(180deg, rgba(255,42,141,0.95), rgba(120,10,70,0.95));
    border: 3px solid var(--vc-yellow); border-radius: 18px; padding: 16px 36px;
    box-shadow: 0 0 40px rgba(255, 42, 141, 0.9), 0 10px 30px rgba(0,0,0,0.8);
    color: #fff; animation: bannerPop 0.4s cubic-bezier(0.18, 1.25, 0.4, 1.1) forwards;
  }
  @keyframes bannerPop {
    to { transform: translateX(-50%) scale(1); opacity: 1; }
  }
  #mission-banner .m-title {
    font-family: 'Orbitron', sans-serif; font-size: 18px; font-weight: 900;
    color: var(--vc-yellow); letter-spacing: 4px; text-shadow: 2px 2px 0 #000;
  }
  #mission-banner .m-name {
    font-size: 26px; font-weight: 700; margin: 4px 0; color: #fff;
    text-shadow: 0 2px 10px rgba(0,0,0,0.8);
  }
  #mission-banner .m-sub {
    font-size: 13px; color: #ffe6f3; font-style: italic; letter-spacing: 1px;
  }
  #mission-banner .m-respect {
    margin-top: 8px; font-family: 'Orbitron', monospace; font-size: 15px; font-weight: 900;
    color: #55ff55; text-shadow: 0 0 10px #00ff00, 1px 1px 0 #000;
  }

  /* Aerial Tour Indicator */
  #tour-indicator {
    position: absolute; top: 80px; left: 50%; transform: translateX(-50%);
    background: rgba(11, 37, 69, 0.94); border: 2px solid var(--vc-cyan);
    border-radius: 30px; padding: 8px 24px; display: none; align-items: center; gap: 10px;
    color: #fff; font-size: 15px; font-weight: 700; box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
  }
  #tour-indicator .rec-dot {
    width: 12px; height: 12px; border-radius: 50%; background: #ff0055;
    animation: blink 0.8s infinite alternate;
  }
  @keyframes blink { from { opacity: 0.3; } to { opacity: 1; } }

  /* Toolbar */
  #toolbar {
    position: absolute; top: 16px; left: 20px;
    display: flex; align-items: center; gap: 8px; pointer-events: auto; flex-wrap: wrap;
    max-width: 65vw;
  }
  .tb-btn {
    background: rgba(14, 8, 28, 0.88); border: 1.5px solid var(--vc-cyan);
    color: #fff; border-radius: 12px; padding: 8px 14px; font-size: 13px; font-weight: 700;
    cursor: pointer; display: flex; align-items: center; gap: 6px;
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3); backdrop-filter: blur(6px);
    transition: all 0.15s ease;
  }
  .tb-btn:hover {
    background: var(--vc-pink); border-color: var(--vc-yellow);
    box-shadow: 0 0 18px var(--vc-pink); transform: translateY(-2px);
  }
  .tb-btn.heli {
    background: linear-gradient(135deg, #ff7700, var(--vc-yellow));
    color: #000; border-color: #fff; font-weight: 900;
    box-shadow: 0 0 18px rgba(255, 234, 0, 0.7);
  }
  .tb-btn.heli:hover {
    background: #ff5500; color: #fff; box-shadow: 0 0 25px #ff5500;
  }

  /* Modals */
  .modal-overlay {
    position: fixed; inset: 0; z-index: 50;
    display: flex; justify-content: center; align-items: flex-start;
    padding: 24px 16px; background: rgba(5, 2, 12, 0.82);
    backdrop-filter: blur(12px); overflow-y: auto; overflow-x: hidden;
    touch-action: pan-y; -webkit-overflow-scrolling: touch;
  }
  .modal-overlay.hidden { display: none !important; }
  .vc-sheet {
    width: min(650px, 100%); max-height: min(88vh, calc(100dvh - 36px));
    background: rgba(14, 8, 28, 0.92); border-radius: 22px; padding: 26px 26px 24px;
    margin: auto 0; border: 2px solid var(--vc-pink);
    box-shadow: 0 0 35px rgba(255, 42, 141, 0.4), 0 20px 50px rgba(0,0,0,0.8);
    color: #f1f4f9; position: relative; overflow-y: auto; overflow-x: hidden;
    touch-action: pan-y; user-select: text; -webkit-overflow-scrolling: touch;
    animation: sheetRise 0.3s cubic-bezier(0.18, 1.25, 0.4, 1.1);
  }
  @keyframes sheetRise {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  .vc-sheet::-webkit-scrollbar { width: 7px; }
  .vc-sheet::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 4px; }
  .vc-sheet::-webkit-scrollbar-thumb { background: var(--vc-pink); border-radius: 4px; }

  .vc-title {
    font-family: 'Orbitron', var(--bn-font); font-size: 26px; font-weight: 900;
    color: var(--vc-yellow); text-shadow: 0 0 15px rgba(255,234,0,0.6);
    line-height: 1.2; margin: 0 0 6px;
  }
  .vc-subtitle {
    font-size: 13px; color: var(--vc-cyan); letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 16px; font-weight: 700;
  }
  .vc-btn {
    background: linear-gradient(135deg, var(--vc-pink), #ff0055);
    color: #fff; border: 2px solid var(--vc-yellow); border-radius: 14px;
    padding: 12px 24px; font-size: 15px; font-weight: 800; cursor: pointer;
    box-shadow: 0 0 20px rgba(255, 42, 141, 0.6); display: inline-flex;
    align-items: center; gap: 8px; transition: transform 0.1s ease, box-shadow 0.1s ease;
  }
  .vc-btn:hover {
    transform: scale(1.03); box-shadow: 0 0 28px rgba(255, 42, 141, 0.9);
  }
  .vc-btn:active { transform: scale(0.98); }

  .key-badge {
    background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 8px; padding: 4px 9px; font-size: 12.5px; display: inline-flex;
    align-items: center; gap: 6px; margin: 3px 2px;
  }
  .key-badge b {
    background: var(--vc-pink); color: #fff; padding: 2px 6px; border-radius: 4px;
    font-family: 'Orbitron', monospace; font-size: 11px;
  }

  .fact-box {
    background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 14px; padding: 16px; font-size: 15px; line-height: 1.7;
    color: #e5edf5; margin: 16px 0;
  }
</style>
<script src="three.min.js"></script>
<script>
  if (typeof THREE === 'undefined') {
    document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\/script>');
  }
</script>
</head>
<body>

<canvas id="c"></canvas>

<!-- HUD -->
<div id="hud">
  <div id="toolbar">
    <button class="tb-btn heli" id="btnFlyHeli">🚁 হেলিকপ্টার ওড়াও (Fly Heli)</button>
    <button class="tb-btn heli" id="btnAutoTour" style="background:linear-gradient(135deg,#00b4d8,#0077b6);color:#fff">🗺️ রিয়েল এরিয়াল ট্যুর</button>
    <button class="tb-btn" id="btnHelp">❓ কন্ট্রোল (H)</button>
    <button class="tb-btn" id="btnTime">🌅 সানসেট (T)</button>
    <button class="tb-btn" id="btnRadio">📻 রেডিও (M)</button>
    <button class="tb-btn" id="btnCam">🎥 ভিউ (V)</button>
  </div>

  <div id="top-right">
    <div class="vc-clock" id="hudClock">08:45 PM</div>
    <div class="vc-bars">
      <div class="bar-row">
        <span class="bar-icon">❤️</span>
        <div class="bar-track"><div class="bar-fill health-fill" id="hpBar" style="width:100%"></div></div>
        <span class="bar-val" id="hpVal">100</span>
      </div>
      <div class="bar-row">
        <span class="bar-icon">🛡️</span>
        <div class="bar-track"><div class="bar-fill armor-fill" id="armBar" style="width:100%"></div></div>
        <span class="bar-val" id="armVal">100</span>
      </div>
    </div>
    <div class="vc-cash" id="hudCash">$00125000</div>
    <div class="vc-stars" id="hudStars">★★★★★</div>
    <div class="vc-weapon">
      <span class="w-icon" id="weaponIcon">🚁</span>
      <span class="w-ammo">RU</span>
    </div>
  </div>

  <div id="radar-box">
    <canvas id="radar" width="175" height="175"></canvas>
    <div class="radar-n">N</div>
  </div>

  <div id="action-prompt">
    <kbd id="actKey">F / E</kbd>
    <span id="actText">হেলিকপ্টারে ওঠো (Board Helicopter)</span>
  </div>

  <div id="speedo">
    <div class="veh-name" id="vehName">RU MAVERICK HELI</div>
    <div class="speed-num" id="speedVal">0</div>
    <div class="speed-unit">KM / H</div>
    <div class="alt-row" id="altRow">ALTITUDE: <span id="altVal">0</span> M</div>
  </div>

  <div id="mission-banner">
    <div class="m-title">★ LANDMARK VISITED ★</div>
    <div class="m-name" id="mName">সাবাশ বাংলাদেশ</div>
    <div class="m-sub" id="mEn">Sabash Bangladesh Sculpture</div>
    <div class="m-respect" id="mReward">RESPECT +100 · PASSPORT STAMPED</div>
  </div>

  <div id="tour-indicator">
    <div class="rec-dot"></div>
    <span>🚁 রাজশাহী বিশ্ববিদ্যালয় রিয়েল এরিয়াল ট্যুর চলছে (RU Aerial Tour Active)</span>
  </div>
</div>

<!-- Welcome Modal -->
<div class="modal-overlay" id="start-modal">
  <div class="vc-sheet">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
      <div style="font-size:38px">🏛️</div>
      <div>
        <h1 class="vc-title">রাজশাহী বিশ্ববিদ্যালয় ৩ডি রিয়েল ট্যুর 🌴</h1>
        <div class="vc-subtitle">UNIVERSITY OF RAJSHAHI — REALISTIC 3D CAMPUS & HELICOPTER SIMULATION</div>
      </div>
    </div>
    
    <p style="font-size:15px;line-height:1.7;color:#e8edf5;margin-bottom:14px">
      ঐতিহাসিক <b>রাজশাহী বিশ্ববিদ্যালয় (স্থাপিত ১৯৫৩)</b>-এর পুরো <b>৭৫৩ একর ক্যাম্পাস</b> এখন বাস্তবসম্মত টেক্সচার, প্রাকৃতিক গতিবিধি ও এরোডাইনামিক্সে তৈরি! 
      রোবটিক অনুভূতির বদলে এখানে রয়েছে মসৃণ মুভমেন্ট, সত্যিকারের লাল ইটের ক্লাসিক্যাল আর্কিটেকচার এবং <b>হেলিকপ্টার চালিয়ে আকাশ থেকে পুরো ক্যাম্পাস ঘুরে দেখার রোমাঞ্চকর সুযোগ</b>।
    </p>

    <div style="background:rgba(255,42,141,0.12);border:1.5px solid var(--vc-pink);border-radius:14px;padding:12px 16px;margin-bottom:16px">
      <div style="color:var(--vc-yellow);font-weight:700;font-size:14px;margin-bottom:6px">🚁 হেলিকপ্টার কন্ট্রোলস (রিয়েল অ্যারোডাইনামিক্স):</div>
      <div class="key-badge"><b>SPACE</b> উঁচুতে ওড়ো (Climb Up)</div>
      <div class="key-badge"><b>SHIFT / C</b> নিচে নামো ও ল্যান্ড করো (Descend)</div>
      <div class="key-badge"><b>W / S</b> সামনে ও পেছনে কাত হয়ে ওড়ো (Forward/Back)</div>
      <div class="key-badge"><b>A / D</b> ডানে ও বাঁমে টার্ন ও ব্যাংকিং (Bank & Turn)</div>
      <div class="key-badge"><b>F বা E</b> হেলিকপ্টারে ওঠো / নামো</div>
      <div class="key-badge"><b>🗺️ এরিয়াল ট্যুর বাটন</b> স্বয়ংক্রিয়ভাবে পুরো ক্যাম্পাসের আকাশ ভ্রমণ</div>
    </div>

    <div style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:14px;padding:10px 14px;margin-bottom:18px;font-size:13px;color:#cde">
      🌿 <b>ক্যাম্পাসের প্রাণকেন্দ্রসমূহ:</b> ভাস্কর নিতুন কুণ্ডুর সাবাশ বাংলাদেশ, শহীদ ড. শামসুজ্জোহা চত্বর, প্রাণবন্ত টুকিটাকি চত্বর, প্যারিস রোডের কৃষ্ণচূড়া গাছ, ঐতিহাসিক শহীদ মিনার ও রেলওয়ে স্টেশন।
    </div>

    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
      <button class="vc-btn" id="startBtn">ক্যাম্পাসে প্রবেশ করো (ENTER CAMPUS) →</button>
      <button class="vc-btn" id="startHeliBtn" style="background:linear-gradient(135deg,#ff7700,var(--vc-yellow));color:#000">🚁 সরাসরি হেলিকপ্টার ট্যুর শুরু</button>
    </div>
  </div>
</div>

<!-- Landmark Modal -->
<div class="modal-overlay hidden" id="landmark-modal">
  <div class="vc-sheet">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
      <div style="font-size:38px" id="lmIcon">🏛️</div>
      <div>
        <h2 class="vc-title" style="font-size:24px;margin:0" id="lmName">প্রধান ফটক</h2>
        <div class="vc-subtitle" style="margin:2px 0 0" id="lmEn">Main Gate</div>
      </div>
    </div>
    <div class="fact-box" id="lmFact">—</div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;flex-wrap:wrap;gap:10px">
      <button class="vc-btn" id="btnSpeak" style="padding:10px 18px;font-size:14px">🔊 বাংলায় শোনো</button>
      <button class="vc-btn" id="btnCloseLm" style="background:#334;border-color:#667">বন্ধ করো (Close)</button>
    </div>
  </div>
</div>

<script>
/* ══════════════════════════════════════════════════════════════════
   CAMPUS DATA (Rajshahi University 1953)
══════════════════════════════════════════════════════════════════ */
const BUILDINGS = ''' + buildings_json + r''';
const LANDMARKS = ''' + landmarks_json + r''';

const ROADS = [
  {x:150,y:1200,w:2338,h:76,t:'main'},
  {x:150,y:506,w:2338,h:72,t:'main'},
  {x:150,y:506,w:76,h:770,t:'main'},
  {x:2412,y:506,w:76,h:770,t:'main'},
  {x:816,y:1276,w:88,h:164,t:'main'},
  {x:1470,y:96,w:80,h:412,t:'lane'},
  {x:196,y:1276,w:72,h:110,t:'lane'},
  {x:1714,y:1276,w:72,h:110,t:'lane'},
  {x:0,y:1470,w:2600,h:86,t:'natore'},
  {x:816,y:1420,w:88,h:460,t:'lane'},
];

const SCALE = 0.4;
function to3D(x, y) {
  return {
    x: (x - 1300) * SCALE,
    z: (y - 1000) * SCALE
  };
}

/* ══════════════════════════════════════════════════════════════════
   PROCEDURAL REALISTIC TEXTURES ENGINE
══════════════════════════════════════════════════════════════════ */
function generateGrassTexture() {
  const cvs = document.createElement('canvas'); cvs.width = 512; cvs.height = 512;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = '#3a6c32'; ctx.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 40000; i++) {
    const x = Math.random() * 512, y = Math.random() * 512;
    ctx.fillStyle = Math.random() > 0.5 ? '#48823f' : '#2d5727';
    ctx.fillRect(x, y, 1.5, 2.5);
  }
  const tex = new THREE.CanvasTexture(cvs);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(45, 45);
  return tex;
}

function generateAsphaltTexture() {
  const cvs = document.createElement('canvas'); cvs.width = 512; cvs.height = 512;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = '#2b2e30'; ctx.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 25000; i++) {
    const x = Math.random() * 512, y = Math.random() * 512;
    const v = Math.random() > 0.5 ? '#3a3d40' : '#1e2022';
    ctx.fillStyle = v; ctx.fillRect(x, y, 1.8, 1.8);
  }
  const tex = new THREE.CanvasTexture(cvs);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(10, 10);
  return tex;
}

function generateBrickTexture(mainColor = '#a84732', mortarColor = '#d9d2c5') {
  const cvs = document.createElement('canvas'); cvs.width = 256; cvs.height = 256;
  const ctx = cvs.getContext('2d');
  ctx.fillStyle = mortarColor; ctx.fillRect(0, 0, 256, 256);
  ctx.fillStyle = mainColor;
  const bh = 14, bw = 30;
  for (let r = 0; r < 256; r += bh + 2) {
    const shift = (Math.floor(r / (bh + 2)) % 2) * (bw / 2);
    for (let c = -bw; c < 256; c += bw + 2) {
      ctx.fillRect(c + shift, r, bw, bh);
    }
  }
  const tex = new THREE.CanvasTexture(cvs);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(4, 4);
  return tex;
}

/* ══════════════════════════════════════════════════════════════════
   AUDIO ENGINE (Helicopter Turbines, Rotor Chops, Campus Sounds)
══════════════════════════════════════════════════════════════════ */
class RealisticAudioEngine {
  constructor() {
    this.ctx = null;
    this.radioPlaying = false;
    this.radioTimer = null;
    this.step = 0;
    this.heliActive = false;
    this.heliTimer = null;
    this.whineOsc = null;
    this.whineGain = null;
  }

  init() {
    if (this.ctx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContext();
  }

  startHeliSound() {
    if (this.heliActive || !this.ctx) return;
    this.heliActive = true;

    // High turbine turbine whine
    this.whineOsc = this.ctx.createOscillator();
    this.whineGain = this.ctx.createGain();
    this.whineOsc.type = 'sawtooth';
    this.whineOsc.frequency.setValueAtTime(360, this.ctx.currentTime);
    this.whineGain.gain.setValueAtTime(0.04, this.ctx.currentTime);

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(800, this.ctx.currentTime);

    this.whineOsc.connect(filter);
    filter.connect(this.whineGain);
    this.whineGain.connect(this.ctx.destination);
    this.whineOsc.start();

    // Rhythmic organic rotor chop
    this.heliTimer = setInterval(() => {
      if (!this.heliActive || !this.ctx) return;
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(58, now);
      osc.frequency.exponentialRampToValueAtTime(24, now + 0.08);
      gain.gain.setValueAtTime(0.22, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    }, 115);
  }

  updateHeliAudio(speed, climb) {
    if (!this.ctx || !this.whineGain) return;
    const targetFreq = 360 + Math.min(speed * 4, 180) + (climb > 0 ? 60 : 0);
    this.whineOsc.frequency.setTargetAtTime(targetFreq, this.ctx.currentTime, 0.1);
  }

  stopHeliSound() {
    this.heliActive = false;
    if (this.heliTimer) clearInterval(this.heliTimer);
    if (this.whineOsc) {
      try { this.whineOsc.stop(); } catch(e){}
      this.whineOsc = null;
    }
  }

  playMissionFanfare() {
    if (!this.ctx) return;
    const notes = [261.6, 329.6, 392.0, 523.3, 659.3];
    const now = this.ctx.currentTime;
    notes.forEach((freq, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq, now + i * 0.09);
      gain.gain.setValueAtTime(0.14, now + i * 0.09);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.09 + 0.4);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + i * 0.09);
      osc.stop(now + i * 0.09 + 0.45);
    });
  }

  toggleRadio() {
    this.init();
    this.radioPlaying = !this.radioPlaying;
    if (this.radioPlaying) {
      this.playSynthwaveBeat();
    } else {
      if (this.radioTimer) clearInterval(this.radioTimer);
    }
    return this.radioPlaying;
  }

  playSynthwaveBeat() {
    if (!this.ctx) return;
    const bassline = [110, 110, 146.8, 146.8, 130.8, 130.8, 98, 98];
    this.radioTimer = setInterval(() => {
      if (!this.radioPlaying || !this.ctx) return;
      const now = this.ctx.currentTime;
      const idx = this.step % bassline.length;

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(bassline[idx] * 0.5, now);
      gain.gain.setValueAtTime(0.07, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.2);

      this.step++;
    }, 180);
  }
}

const audio = new RealisticAudioEngine();

/* ══════════════════════════════════════════════════════════════════
   THREE.JS REALISTIC SETUP
══════════════════════════════════════════════════════════════════ */
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.5, 3500);

let timeMode = 0;
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.3);
dirLight.position.set(220, 480, 160);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.near = 10;
dirLight.shadow.camera.far = 1300;
const d = 520;
dirLight.shadow.camera.left = -d; dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d; dirLight.shadow.camera.bottom = -d;
scene.add(dirLight);

const hemiLight = new THREE.HemisphereLight(0xffbbaa, 0x244222, 0.75);
scene.add(hemiLight);

function setTimeOfDay(mode) {
  timeMode = mode;
  const btn = document.getElementById('btnTime');
  if (mode === 0) {
    btn.innerHTML = '🌅 সানসেট (T)';
    scene.background = new THREE.Color(0x381542);
    scene.fog = new THREE.FogExp2(0x4a1b4f, 0.0017);
    dirLight.color.setHex(0xffaa55);
    dirLight.intensity = 1.35;
    hemiLight.color.setHex(0xff88aa);
  } else if (mode === 1) {
    btn.innerHTML = '☀️ দিন (T)';
    scene.background = new THREE.Color(0x82c8f8);
    scene.fog = new THREE.FogExp2(0x9fd6fa, 0.0012);
    dirLight.color.setHex(0xffffff);
    dirLight.intensity = 1.45;
    hemiLight.color.setHex(0xffffff);
  } else {
    btn.innerHTML = '🌙 রাত (T)';
    scene.background = new THREE.Color(0x06050e);
    scene.fog = new THREE.FogExp2(0x080614, 0.0024);
    dirLight.color.setHex(0x4466aa);
    dirLight.intensity = 0.4;
    hemiLight.color.setHex(0x334466);
  }
}
setTimeOfDay(0);

// Ground Plane with Organic Grass Texture
const grassTex = generateGrassTexture();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(2000, 1600), new THREE.MeshStandardMaterial({ map: grassTex, roughness: 0.9, metalness: 0.05 }));
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Roads with Bituminous Asphalt Texture
const asphaltTex = generateAsphaltTexture();
const roadMat = new THREE.MeshStandardMaterial({ map: asphaltTex, roughness: 0.85, metalness: 0.1 });
const stripeMat = new THREE.MeshBasicMaterial({ color: 0xffea00 });

ROADS.forEach(r => {
  const p0 = to3D(r.x, r.y);
  const p1 = to3D(r.x + r.w, r.y + r.h);
  const rw = Math.abs(p1.x - p0.x);
  const rd = Math.abs(p1.z - p0.z);
  const cx = (p0.x + p1.x) / 2;
  const cz = (p0.z + p1.z) / 2;

  const roadMesh = new THREE.Mesh(new THREE.PlaneGeometry(rw, rd), roadMat);
  roadMesh.rotation.x = -Math.PI / 2;
  roadMesh.position.set(cx, 0.06, cz);
  roadMesh.receiveShadow = true;
  scene.add(roadMesh);

  if (rw > 20 || rd > 20) {
    const sw = rw > rd ? rw * 0.96 : 1.2;
    const sd = rw > rd ? 1.2 : rd * 0.96;
    const stripe = new THREE.Mesh(new THREE.PlaneGeometry(sw, sd), stripeMat);
    stripe.rotation.x = -Math.PI / 2;
    stripe.position.set(cx, 0.09, cz);
    scene.add(stripe);
  }
});

/* ══════════════════════════════════════════════════════════════════
   AUTHENTIC RU SCULPTURES & MONUMENTS
══════════════════════════════════════════════════════════════════ */
// 1. Sabash Bangladesh (সাবাশ বাংলাদেশ - ভাস্কর নিতুন কুণ্ডু)
(function() {
  const p = to3D(660, 1080);
  const group = new THREE.Group();

  // Stone Platform
  const base = new THREE.Mesh(new THREE.BoxGeometry(22, 2.6, 18), new THREE.MeshStandardMaterial({ color: 0xd8c8af, roughness: 0.8 }));
  base.position.y = 1.3;
  base.receiveShadow = true;
  group.add(base);

  // Iconic Red Sun Background Wall
  const wall = new THREE.Mesh(new THREE.BoxGeometry(19, 13, 2), new THREE.MeshStandardMaterial({ color: 0xa4927f, roughness: 0.9 }));
  wall.position.set(0, 9, -6);
  wall.castShadow = true;
  group.add(wall);

  const redSun = new THREE.Mesh(new THREE.CircleGeometry(4.5, 32), new THREE.MeshBasicMaterial({ color: 0xff0025, side: THREE.DoubleSide }));
  redSun.position.set(0, 10, -4.9);
  group.add(redSun);

  // Bronze Sculpted Hero Figures (Nitun Kundu style)
  const heroMat = new THREE.MeshStandardMaterial({ color: 0x4a3a2e, roughness: 0.6, metalness: 0.3 });
  const hero1 = new THREE.Mesh(new THREE.BoxGeometry(2.6, 9.5, 2.4), heroMat);
  hero1.position.set(-3.4, 7, 0);
  hero1.castShadow = true;
  group.add(hero1);

  // Raised Rifle
  const rifle = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.25, 9, 8), new THREE.MeshStandardMaterial({ color: 0x1a1a1a, metalness: 0.7 }));
  rifle.position.set(-3.4, 12.5, 0.6);
  rifle.rotation.z = -0.32;
  group.add(rifle);

  const hero2 = new THREE.Mesh(new THREE.BoxGeometry(2.8, 8.5, 2.5), heroMat);
  hero2.position.set(3.4, 6.5, 0.6);
  hero2.castShadow = true;
  group.add(hero2);

  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 2. Central Shaheed Minar (4 Soaring Marble Columns & Steps)
(function() {
  const p = to3D(1130, 960);
  const group = new THREE.Group();
  const podium = new THREE.Mesh(new THREE.CylinderGeometry(26, 28, 3.2, 6), new THREE.MeshStandardMaterial({ color: 0xeaeaea, roughness: 0.6 }));
  podium.position.y = 1.6;
  podium.receiveShadow = true;
  group.add(podium);

  const sunMesh = new THREE.Mesh(new THREE.CircleGeometry(11, 32), new THREE.MeshBasicMaterial({ color: 0xff002b, side: THREE.DoubleSide }));
  sunMesh.position.set(0, 17, -1.2);
  group.add(sunMesh);

  const pillarMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4, metalness: 0.1 });
  const heights = [30, 24, 24, 18];
  const xOffsets = [-7.5, -2.6, 2.6, 7.5];
  heights.forEach((h, i) => {
    const pil = new THREE.Mesh(new THREE.BoxGeometry(2.6, h, 2.6), pillarMat);
    pil.position.set(xOffsets[i], 3.2 + h / 2, 0);
    pil.rotation.z = (i < 2 ? -0.065 : 0.065);
    pil.castShadow = true;
    group.add(pil);
  });
  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 3. Central Jamia Mosque
(function() {
  const p = to3D(1072, 1111);
  const group = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(40, 15, 30), new THREE.MeshStandardMaterial({ color: 0xf5f5f5, roughness: 0.7 }));
  base.position.y = 7.5;
  group.add(base);

  const dome = new THREE.Mesh(new THREE.SphereGeometry(9.5, 24, 24, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x266e5c, roughness: 0.5 }));
  dome.position.y = 15;
  group.add(dome);

  const minMat = new THREE.MeshStandardMaterial({ color: 0xf0f0f0, roughness: 0.5 });
  [[-18, -13], [18, -13], [-18, 13], [18, 13]].forEach(([mx, mz]) => {
    const min = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.5, 28, 12), minMat);
    min.position.set(mx, 14, mz);
    min.castShadow = true;
    group.add(min);
  });
  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 4. Tukitaki Chattar (টুকিটাকি চত্বর)
(function() {
  const p = to3D(760, 990);
  const group = new THREE.Group();
  const pave = new THREE.Mesh(new THREE.CylinderGeometry(19, 19, 0.4, 24), new THREE.MeshStandardMaterial({ color: 0xd2c2a8, roughness: 0.85 }));
  pave.position.y = 0.2;
  group.add(pave);

  const stall = new THREE.Mesh(new THREE.BoxGeometry(7, 4.5, 4.5), new THREE.MeshStandardMaterial({ color: 0x82442d, roughness: 0.8 }));
  stall.position.set(0, 2.25, -11);
  group.add(stall);

  [[-6, -3], [6, -3], [-5, 5], [5, 5]].forEach(([tx, tz]) => {
    const table = new THREE.Mesh(new THREE.CylinderGeometry(1.8, 1.8, 1.6, 16), new THREE.MeshStandardMaterial({ color: 0xdfdfdf, roughness: 0.5 }));
    table.position.set(tx, 0.8, tz);
    group.add(table);
  });
  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 5. Paris Road Trees (Krishnachura & Rain Trees with White/Red Painted Bases)
const parisStart = to3D(500, 1050);
const parisEnd = to3D(500, 1250);
const trunkMat = new THREE.MeshStandardMaterial({ color: 0x4f3627, roughness: 0.9 });
const baseWhiteMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
const leafLushMat = new THREE.MeshStandardMaterial({ color: 0x245d2d, roughness: 0.8 });
const redFlowerMat = new THREE.MeshStandardMaterial({ color: 0xe62214, roughness: 0.8 }); // Blooming Krishnachura

for (let i = 0; i <= 24; i++) {
  const z = parisStart.z + (parisEnd.z - parisStart.z) * (i / 24);
  [-14, 14].forEach(offX => {
    const tg = new THREE.Group();
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.95, 11, 8), trunkMat);
    trunk.position.y = 5.5;
    trunk.castShadow = true;
    tg.add(trunk);

    // White/Red Band
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.97, 1.0, 3.2, 8), baseWhiteMat);
    band.position.y = 1.6;
    tg.add(band);

    // Multi-level natural canopy
    const leaves1 = new THREE.Mesh(new THREE.DodecahedronGeometry(5.8, 1), leafLushMat);
    leaves1.position.y = 12.5;
    leaves1.castShadow = true;
    tg.add(leaves1);

    // Occasional Krishnachura Red Blossoms
    if (i % 3 === 0) {
      const blooms = new THREE.Mesh(new THREE.DodecahedronGeometry(3.5, 1), redFlowerMat);
      blooms.position.set(0.8, 14, 0.5);
      tg.add(blooms);
    }

    tg.position.set(parisStart.x + offX, 0, z);
    scene.add(tg);
  });
}

// 6. Buildings with Muzharul Islam Terracotta Brick Textures
const brickTex = generateBrickTexture('#a84732', '#dfd7ca');
const buildingMat = new THREE.MeshStandardMaterial({ map: brickTex, roughness: 0.85, metalness: 0.05 });
const roofMat = new THREE.MeshStandardMaterial({ color: 0x2d3238, roughness: 0.9 });

BUILDINGS.forEach(b => {
  const p = to3D(b.x, b.y);
  const bw = Math.max(b.w * SCALE, 14);
  const bd = Math.max(b.h * SCALE, 12);
  const bh = 14 + (Math.abs(b.x * 13 + b.y * 7) % 18);

  const bMesh = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, bd), buildingMat);
  bMesh.position.set(p.x, bh / 2, p.z);
  bMesh.castShadow = true;
  bMesh.receiveShadow = true;
  scene.add(bMesh);

  const roof = new THREE.Mesh(new THREE.BoxGeometry(bw + 1.2, 1.2, bd + 1.2), roofMat);
  roof.position.set(p.x, bh + 0.6, p.z);
  scene.add(roof);

  // 3D Bangla Label
  const cLabel = document.createElement('canvas');
  cLabel.width = 512; cLabel.height = 128;
  const cx = cLabel.getContext('2d');
  cx.fillStyle = 'rgba(12, 6, 24, 0.88)';
  cx.roundRect(10, 10, 492, 108, 16);
  cx.fill();
  cx.strokeStyle = '#00e5ff'; cx.lineWidth = 4; cx.stroke();
  cx.fillStyle = '#ffffff'; cx.font = 'bold 36px "Hind Siliguri", sans-serif';
  cx.textAlign = 'center'; cx.textBaseline = 'middle';
  cx.fillText(b.l, 256, 64);

  const tex = new THREE.CanvasTexture(cLabel);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true }));
  sprite.position.set(p.x, bh + 9, p.z);
  sprite.scale.set(22, 5.5, 1);
  scene.add(sprite);
});

/* ══════════════════════════════════════════════════════════════════
   REALISTIC HELICOPTER & HELIPADS
══════════════════════════════════════════════════════════════════ */
function createHelipad(x, z, label = 'RU HELIPAD') {
  const group = new THREE.Group();
  const pad = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 0.4, 28), new THREE.MeshStandardMaterial({ color: 0x272b2f, roughness: 0.8 }));
  pad.position.y = 0.2;
  pad.receiveShadow = true;
  group.add(pad);

  const ring = new THREE.Mesh(new THREE.RingGeometry(11.5, 12.8, 32), new THREE.MeshBasicMaterial({ color: 0xffea00, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2;
  ring.position.y = 0.42;
  group.add(ring);

  const canvasH = document.createElement('canvas'); canvasH.width = 256; canvasH.height = 256;
  const ctxH = canvasH.getContext('2d');
  ctxH.fillStyle = '#ffea00'; ctxH.font = '900 160px "Orbitron", sans-serif';
  ctxH.textAlign = 'center'; ctxH.textBaseline = 'middle';
  ctxH.fillText('H', 128, 128);

  const markH = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(canvasH), transparent: true }));
  markH.rotation.x = -Math.PI / 2;
  markH.position.y = 0.44;
  group.add(markH);

  group.position.set(x, 0, z);
  scene.add(group);
}

const helipadSenate = to3D(780, 1150);
createHelipad(helipadSenate.x, helipadSenate.z, 'SENATE HELIPAD');
const helipadStadium = to3D(1288, 733);
createHelipad(helipadStadium.x, helipadStadium.z, 'STADIUM HELIPAD');

// Realistic 3D Helicopter
const heliGroup = new THREE.Group();

// Aerodynamic Fuselage
const heliMat = new THREE.MeshStandardMaterial({ color: 0x0b2545, roughness: 0.35, metalness: 0.6 });
const heliBody = new THREE.Mesh(new THREE.BoxGeometry(4.5, 3.8, 11), heliMat);
heliBody.position.y = 3.2;
heliBody.castShadow = true;
heliGroup.add(heliBody);

// Curved Glass Canopy
const glassMat = new THREE.MeshStandardMaterial({ color: 0x00e5ff, transparent: true, opacity: 0.72, roughness: 0.1, metalness: 0.9 });
const heliGlass = new THREE.Mesh(new THREE.BoxGeometry(4.2, 2.7, 4.4), glassMat);
heliGlass.position.set(0, 3.65, 3.5);
heliGroup.add(heliGlass);

// Tail Boom & Stabilizer
const tailBoom = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.4, 9.8), heliMat);
tailBoom.position.set(0, 3.8, -8.6);
heliGroup.add(tailBoom);

const vertFin = new THREE.Mesh(new THREE.BoxGeometry(0.35, 3.4, 2.4), new THREE.MeshStandardMaterial({ color: 0xffea00, roughness: 0.4 }));
vertFin.position.set(0, 4.9, -13.2);
heliGroup.add(vertFin);

// Skids
const skidMat = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.8, roughness: 0.3 });
[[-2.2, 0.4, 0], [2.2, 0.4, 0]].forEach(([sx, sy, sz]) => {
  const skid = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.3, 11.5), skidMat);
  skid.position.set(sx, sy, sz);
  heliGroup.add(skid);
  const strutF = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.8, 0.3), skidMat);
  strutF.position.set(sx, 1.4, 2.8);
  heliGroup.add(strutF);
  const strutB = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.8, 0.3), skidMat);
  strutB.position.set(sx, 1.4, -2.8);
  heliGroup.add(strutB);
});

// Rotors with Motion Blur Disc Effect
const mainRotorGroup = new THREE.Group();
mainRotorGroup.position.set(0, 5.5, 0.6);
const rotorMast = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1.3, 12), skidMat);
mainRotorGroup.add(rotorMast);

const bladeMat = new THREE.MeshStandardMaterial({ color: 0x151515, metalness: 0.5 });
const blade1 = new THREE.Mesh(new THREE.BoxGeometry(18, 0.16, 1.0), bladeMat);
blade1.position.y = 0.65;
mainRotorGroup.add(blade1);
const blade2 = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.16, 18), bladeMat);
blade2.position.y = 0.65;
mainRotorGroup.add(blade2);

// Motion blur rotor disc (visible when spinning fast for realism)
const blurDisc = new THREE.Mesh(
  new THREE.CircleGeometry(9.2, 32),
  new THREE.MeshBasicMaterial({ color: 0x222222, transparent: true, opacity: 0.0, side: THREE.DoubleSide })
);
blurDisc.rotation.x = Math.PI / 2;
blurDisc.position.y = 0.7;
mainRotorGroup.add(blurDisc);
heliGroup.add(mainRotorGroup);

// Tail Rotor
const tailRotorGroup = new THREE.Group();
tailRotorGroup.position.set(0.55, 4.9, -13.2);
const tailBlade = new THREE.Mesh(new THREE.BoxGeometry(0.15, 3.4, 0.45), bladeMat);
tailRotorGroup.add(tailBlade);
heliGroup.add(tailRotorGroup);

// Spotlight
const heliLight = new THREE.SpotLight(0xffffff, 4, 220, Math.PI / 4, 0.35);
heliLight.position.set(0, 1.8, 4.6);
heliLight.target.position.set(0, -60, 30);
heliGroup.add(heliLight);
heliGroup.add(heliLight.target);

heliGroup.position.set(helipadSenate.x, 0, helipadSenate.z);
scene.add(heliGroup);

const helicopter = {
  mesh: heliGroup,
  mainRotor: mainRotorGroup,
  tailRotor: tailRotorGroup,
  blurDisc,
  speed: 0,
  altitude: 0,
  yaw: 0,
  pitch: 0,
  roll: 0,
  active: false
};

/* ══════════════════════════════════════════════════════════════════
   PLAYER CHARACTER (Smooth Human Kinetics)
══════════════════════════════════════════════════════════════════ */
const playerGroup = new THREE.Group();
const torso = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.2, 0.9), new THREE.MeshStandardMaterial({ color: 0x00e5ff, roughness: 0.7 }));
torso.position.y = 3.1; torso.castShadow = true; playerGroup.add(torso);
const head = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.1, 1.0), new THREE.MeshStandardMaterial({ color: 0xdeb887, roughness: 0.8 }));
head.position.y = 4.75; playerGroup.add(head);

const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.0, 0.6), new THREE.MeshStandardMaterial({ color: 0x2a4477, roughness: 0.8 }));
leftLeg.position.set(-0.45, 1.0, 0); playerGroup.add(leftLeg);
const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.0, 0.6), new THREE.MeshStandardMaterial({ color: 0x2a4477, roughness: 0.8 }));
rightLeg.position.set(0.45, 1.0, 0); playerGroup.add(rightLeg);

const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 1.8, 0.45), new THREE.MeshStandardMaterial({ color: 0xdeb887, roughness: 0.8 }));
leftArm.position.set(-1.05, 3.0, 0); playerGroup.add(leftArm);
const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 1.8, 0.45), new THREE.MeshStandardMaterial({ color: 0xdeb887, roughness: 0.8 }));
rightArm.position.set(1.05, 3.0, 0); playerGroup.add(rightArm);

const spawnPos = to3D(860, 1400);
playerGroup.position.set(spawnPos.x, 0, spawnPos.z);
scene.add(playerGroup);

/* ══════════════════════════════════════════════════════════════════
   CONTROLS & CAMERA
══════════════════════════════════════════════════════════════════ */
let camMode = 1;
let camYaw = 0, camPitch = 0.25, camDistance = 15;
const keys = {};

window.addEventListener('keydown', e => {
  keys[e.code] = true;
  if (e.code === 'KeyV') cycleCamera();
  if (e.code === 'KeyM') {
    const on = audio.toggleRadio();
    document.getElementById('btnRadio').innerHTML = on ? '📻 রেডিও (ON)' : '📻 রেডিও (OFF)';
  }
  if (e.code === 'KeyT') setTimeOfDay((timeMode + 1) % 3);
  if (e.code === 'KeyF' || e.code === 'KeyE') handleVehicleEnterExit();
});
window.addEventListener('keyup', e => { keys[e.code] = false; });

let isMouseDown = false;
canvas.addEventListener('mousedown', () => { isMouseDown = true; audio.init(); });
window.addEventListener('mouseup', () => { isMouseDown = false; });
window.addEventListener('mousemove', e => {
  if (document.pointerLockElement === canvas || isMouseDown) {
    camYaw -= e.movementX * 0.0035;
    camPitch = Math.max(-0.25, Math.min(1.15, camPitch + e.movementY * 0.0035));
  }
});
canvas.addEventListener('click', () => {
  if (!document.pointerLockElement) canvas.requestPointerLock();
});
window.addEventListener('wheel', e => {
  if (e.target.closest && e.target.closest('.modal-overlay')) return;
  camDistance = Math.max(6, Math.min(85, camDistance + e.deltaY * 0.02));
});

function cycleCamera() {
  camMode = (camMode + 1) % 4;
  const modes = ['🎥 ক্লোজ (V)', '🎥 চেজ (V)', '🎥 ফার (V)', '🎥 টপ ভিউ (V)'];
  document.getElementById('btnCam').innerHTML = modes[camMode];
}

/* ══════════════════════════════════════════════════════════════════
   HELICOPTER FLIGHT & REALISTIC AERIAL TOUR
══════════════════════════════════════════════════════════════════ */
let inHelicopter = false;
let autoTourActive = false;
let autoTourIndex = 0;

const TOUR_WAYPOINTS = [
  { name: 'প্রধান ফটক (Main Gate)', x: to3D(860, 1400).x, z: to3D(860, 1400).z, alt: 48, fact: 'ঐতিহাসিক প্রধান ফটক — নাটোর রোড থেকে রাজশাহী বিশ্ববিদ্যালয়ে প্রবেশের রাজপথ।' },
  { name: 'প্যারিস রোড (Paris Road)', x: to3D(500, 1140).x, z: to3D(500, 1140).z, alt: 42, fact: 'বিখ্যাত প্যারিস রোড — সারি সারি কৃষ্ণচূড়া ও রেইনট্রি বৃক্ষের চিরসবুজ রাজপথ।' },
  { name: 'টুকিটাকি চত্বর (Tukitaki)', x: to3D(760, 990).x, z: to3D(760, 990).z, alt: 45, fact: 'শিক্ষার্থীদের প্রাণবন্ত টুকিটাকি চত্বর ও কেন্দ্রীয় লাইব্রেরি।' },
  { name: 'সাবাশ বাংলাদেশ (Sabash Bangladesh)', x: to3D(660, 1080).x, z: to3D(660, 1080).z, alt: 45, fact: 'ভাস্কর নিতুন কুণ্ডুর অমর মুক্তিযুদ্ধ ভাস্কর্য সাবাশ বাংলাদেশ ও সিনেট ভবন।' },
  { name: 'কেন্দ্রীয় শহীদ মিনার (Shaheed Minar)', x: to3D(1130, 960).x, z: to3D(1130, 960).z, alt: 52, fact: 'চারটি সুউচ্চ স্তম্ভ ও রক্তিম সূর্যের ঐতিহাসিক কেন্দ্রীয় শহীদ মিনার।' },
  { name: 'বিশ্ববিদ্যালয় স্টেডিয়াম (Stadium)', x: to3D(1288, 733).x, z: to3D(1288, 733).z, alt: 58, fact: 'রাবি স্টেডিয়াম, জিমনেসিয়াম ও সুইমিং পুল কমপ্লেক্স।' },
  { name: 'কেন্দ্রীয় জামে মসজিদ (Central Mosque)', x: to3D(1072, 1111).x, z: to3D(1072, 1111).z, alt: 50, fact: 'সুউচ্চ মিনার ও গম্বুজ শোভিত কেন্দ্রীয় জামে মসজিদ।' },
  { name: 'রাবি রেলওয়ে স্টেশন (Railway Station)', x: to3D(1560, 265).x, z: to3D(1560, 265).z, alt: 46, fact: 'ক্যাম্পাসের উত্তর সীমানার ঐতিহ্যবাহী রাজশাহী বিশ্ববিদ্যালয় রেল স্টেশন।' },
  { name: 'বধ্যভূমি স্মৃতিস্তম্ভ (Boddhovumi 71)', x: to3D(2000, 470).x, z: to3D(2000, 470).z, alt: 50, fact: '১৯৭১ সালের মহান মুক্তিযুদ্ধের শহীদদের স্মরণে নির্মিত বধ্যভূমি স্মৃতিস্তম্ভ।' },
  { name: 'সিনেট হেলিপ্যাড (Return to Helipad)', x: helipadSenate.x, z: helipadSenate.z, alt: 8, fact: 'ট্যুর সমাপ্ত — সিনেট হেলিপ্যাডে নিরাপদ অবতরণ।' }
];

function boardHelicopter() {
  inHelicopter = true;
  helicopter.active = true;
  playerGroup.visible = false;
  audio.init();
  audio.startHeliSound();

  document.getElementById('speedo').style.display = 'flex';
  document.getElementById('vehName').innerText = 'RU MAVERICK HELI';
  document.getElementById('altRow').style.display = 'block';
  document.getElementById('action-prompt').style.display = 'none';
  document.getElementById('weaponIcon').innerText = '🚁';
}

function exitHelicopter() {
  if (helicopter.altitude > 2.5) return;
  inHelicopter = false;
  autoTourActive = false;
  helicopter.active = false;
  audio.stopHeliSound();

  playerGroup.position.copy(helicopter.mesh.position);
  playerGroup.position.x += 6;
  playerGroup.position.y = 0;
  playerGroup.visible = true;

  document.getElementById('speedo').style.display = 'none';
  document.getElementById('tour-indicator').style.display = 'none';
  document.getElementById('weaponIcon').innerText = '👊';
}

function handleVehicleEnterExit() {
  if (inHelicopter) {
    exitHelicopter();
  } else {
    const d = playerGroup.position.distanceTo(helicopter.mesh.position);
    if (d < 18) boardHelicopter();
  }
}

function startAutoHeliTour() {
  boardHelicopter();
  autoTourActive = true;
  autoTourIndex = 0;
  document.getElementById('tour-indicator').style.display = 'flex';
}

// UI Buttons
document.getElementById('btnFlyHeli').addEventListener('click', () => {
  boardHelicopter();
  helicopter.mesh.position.y = 16;
  helicopter.altitude = 16;
});

document.getElementById('btnAutoTour').addEventListener('click', () => {
  startAutoHeliTour();
});

document.getElementById('startBtn').addEventListener('click', () => {
  document.getElementById('start-modal').classList.add('hidden');
  audio.init();
});

document.getElementById('startHeliBtn').addEventListener('click', () => {
  document.getElementById('start-modal').classList.add('hidden');
  startAutoHeliTour();
});

document.getElementById('btnHelp').addEventListener('click', () => document.getElementById('start-modal').classList.remove('hidden'));
document.getElementById('btnTime').addEventListener('click', () => setTimeOfDay((timeMode + 1) % 3));
document.getElementById('btnRadio').addEventListener('click', () => {
  const on = audio.toggleRadio();
  document.getElementById('btnRadio').innerHTML = on ? '📻 রেডিও (ON)' : '📻 রেডিও (OFF)';
});
document.getElementById('btnCam').addEventListener('click', cycleCamera);
document.getElementById('btnCloseLm').addEventListener('click', () => document.getElementById('landmark-modal').classList.add('hidden'));

// Radar Drawing
const radarCanvas = document.getElementById('radar');
const rx = radarCanvas.getContext('2d');

function updateRadar() {
  rx.clearRect(0, 0, 175, 175);
  const cx = 87.5, cy = 87.5;
  const pPos = inHelicopter ? helicopter.mesh.position : playerGroup.position;

  rx.save();
  rx.translate(cx, cy);
  rx.rotate(camYaw);

  rx.strokeStyle = '#39464d'; rx.lineWidth = 4;
  ROADS.forEach(r => {
    const p0 = to3D(r.x, r.y);
    const p1 = to3D(r.x + r.w, r.y + r.h);
    rx.beginPath();
    rx.rect((p0.x - pPos.x) * 0.45, (p0.z - pPos.z) * 0.45, (p1.x - p0.x) * 0.45, (p1.z - p0.z) * 0.45);
    rx.stroke();
  });

  // Landmark Stars
  rx.fillStyle = '#ffea00';
  LANDMARKS.forEach(lm => {
    const lp = to3D(lm.x, lm.y);
    const dx = (lp.x - pPos.x) * 0.45, dz = (lp.z - pPos.z) * 0.45;
    if (Math.hypot(dx, dz) < 80) {
      rx.beginPath(); rx.arc(dx, dz, 3.5, 0, Math.PI * 2); rx.fill();
    }
  });

  // Helipads
  rx.fillStyle = '#00e5ff';
  [helipadSenate, helipadStadium].forEach(hp => {
    const dx = (hp.x - pPos.x) * 0.45, dz = (hp.z - pPos.z) * 0.45;
    if (Math.hypot(dx, dz) < 80) rx.fillRect(dx - 3, dz - 3, 6, 6);
  });
  rx.restore();

  // Player Arrow
  rx.save();
  rx.translate(cx, cy);
  rx.fillStyle = inHelicopter ? '#00e5ff' : '#ff2a8d';
  rx.strokeStyle = '#ffffff'; rx.lineWidth = 1.5;
  rx.beginPath();
  rx.moveTo(0, -9); rx.lineTo(6, 7); rx.lineTo(0, 4); rx.lineTo(-6, 7);
  rx.closePath(); rx.fill(); rx.stroke();
  rx.restore();
}

let visitedSet = new Set();
function checkLandmarks(pos) {
  LANDMARKS.forEach(lm => {
    const lp = to3D(lm.x, lm.y);
    const d = Math.hypot(pos.x - lp.x, pos.z - lp.z);
    if (d < 36 && !visitedSet.has(lm.id)) {
      visitedSet.add(lm.id);
      triggerMissionBanner(lm);
    }
  });
}

function triggerMissionBanner(lm) {
  audio.playMissionFanfare();
  const banner = document.getElementById('mission-banner');
  document.getElementById('mName').innerText = lm.name;
  document.getElementById('mEn').innerText = lm.en;
  banner.style.display = 'flex';

  if ('speechSynthesis' in window) {
    const ut = new SpeechSynthesisUtterance(lm.name + '। ' + lm.fact);
    ut.lang = 'bn-BD';
    window.speechSynthesis.speak(ut);
  }
  setTimeout(() => { banner.style.display = 'none'; }, 4500);
}

/* ══════════════════════════════════════════════════════════════════
   ANIMATION & PHYSICS LOOP (Real Aerodynamics & Kinetics)
══════════════════════════════════════════════════════════════════ */
let lastTime = performance.now();
let walkCycle = 0;
let playerVel = new THREE.Vector3();

function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min((now - lastTime) / 1000, 0.1);
  lastTime = now;

  // Spin Rotors with Blur Disc Alpha
  const rotorSpeed = (inHelicopter ? 36 : 4);
  helicopter.mainRotor.rotation.y += rotorSpeed * dt;
  helicopter.tailRotor.rotation.x += rotorSpeed * dt * 1.6;
  helicopter.blurDisc.material.opacity = (inHelicopter ? 0.45 : 0.0);

  if (inHelicopter) {
    const heli = helicopter;

    if (autoTourActive) {
      // Smooth Spline Autopilot Tour
      const wp = TOUR_WAYPOINTS[autoTourIndex];
      const dx = wp.x - heli.mesh.position.x;
      const dz = wp.z - heli.mesh.position.z;
      const dist = Math.hypot(dx, dz);

      const targetYaw = Math.atan2(dx, dz);
      let diff = targetYaw - heli.yaw;
      while (diff < -Math.PI) diff += Math.PI * 2;
      while (diff > Math.PI) diff -= Math.PI * 2;
      heli.yaw += diff * 0.04;
      heli.mesh.rotation.y = heli.yaw;

      heli.altitude = THREE.MathUtils.lerp(heli.altitude, wp.alt, 0.025);
      // Gentle atmospheric hover oscillation for realism
      heli.mesh.position.y = heli.altitude + Math.sin(now * 0.003) * 0.18;

      const flySpeed = Math.min(dist * 0.8, 40);
      heli.mesh.position.x += Math.sin(heli.yaw) * flySpeed * dt;
      heli.mesh.position.z += Math.cos(heli.yaw) * flySpeed * dt;
      heli.speed = flySpeed;

      // Realistic forward nose pitch & banking
      heli.mesh.rotation.x = THREE.MathUtils.lerp(heli.mesh.rotation.x, 0.16, 0.05);
      heli.mesh.rotation.z = THREE.MathUtils.lerp(heli.mesh.rotation.z, -diff * 0.25, 0.05);

      if (dist < 20) {
        if ('speechSynthesis' in window && !window.speechSynthesis.speaking) {
          const ut = new SpeechSynthesisUtterance(wp.name + '। ' + wp.fact);
          ut.lang = 'bn-BD';
          window.speechSynthesis.speak(ut);
        }
        autoTourIndex = (autoTourIndex + 1) % TOUR_WAYPOINTS.length;
      }
    } else {
      // Player Flight Controls with Aerodynamic Inertia
      let climb = 0;
      if (keys['Space']) climb = 22;
      if (keys['ShiftLeft'] || keys['ShiftRight'] || keys['KeyC']) climb = -18;

      heli.altitude = Math.max(0, Math.min(140, heli.altitude + climb * dt));
      heli.mesh.position.y = heli.altitude + (heli.altitude > 1 ? Math.sin(now * 0.004) * 0.12 : 0);

      let targetSpeed = 0;
      if (keys['KeyW'] || keys['ArrowUp']) targetSpeed = 46;
      if (keys['KeyS'] || keys['ArrowDown']) targetSpeed = -24;

      heli.speed = THREE.MathUtils.lerp(heli.speed, targetSpeed, 0.05);

      let turn = 0;
      if (keys['KeyA'] || keys['ArrowLeft']) turn = 1.9;
      if (keys['KeyD'] || keys['ArrowRight']) turn = -1.9;
      heli.yaw += turn * dt;

      heli.mesh.rotation.y = heli.yaw;
      // Pitch tilt forward when moving forward
      const targetPitch = (heli.speed > 0 ? 0.2 : (heli.speed < 0 ? -0.15 : 0));
      heli.mesh.rotation.x = THREE.MathUtils.lerp(heli.mesh.rotation.x, targetPitch, 0.08);
      // Realistic banking roll into turns
      heli.mesh.rotation.z = THREE.MathUtils.lerp(heli.mesh.rotation.z, -turn * 0.16, 0.08);

      heli.mesh.position.x += Math.sin(heli.yaw) * heli.speed * dt;
      heli.mesh.position.z += Math.cos(heli.yaw) * heli.speed * dt;

      audio.updateHeliAudio(heli.speed, climb);
    }

    document.getElementById('speedVal').innerText = Math.round(Math.abs(heli.speed) * 2.2);
    document.getElementById('altVal').innerText = Math.round(heli.altitude);

    // Cinematic Camera Following
    const hPos = heli.mesh.position;
    const camDist = (camMode === 3 ? 120 : (camDistance + 14));
    const camHeight = (camMode === 3 ? 160 : (camDistance * 0.5 + 8));

    if (camMode === 3) {
      camera.position.set(hPos.x, hPos.y + camHeight, hPos.z + 0.1);
      camera.lookAt(hPos);
    } else {
      const cx = hPos.x - Math.sin(camYaw) * camDist;
      const cz = hPos.z - Math.cos(camYaw) * camDist;
      const cy = hPos.y + camHeight + Math.sin(camPitch) * camDist;
      camera.position.lerp(new THREE.Vector3(cx, cy, cz), 0.12);
      camera.lookAt(hPos.x, hPos.y + 2, hPos.z);
    }

    checkLandmarks(hPos);
  } else {
    // ── Organic Human Walking with Inertia & Spine Bob ──
    let inputX = 0, inputZ = 0;
    if (keys['KeyW'] || keys['ArrowUp']) { inputX += Math.sin(camYaw); inputZ += Math.cos(camYaw); }
    if (keys['KeyS'] || keys['ArrowDown']) { inputX -= Math.sin(camYaw); inputZ -= Math.cos(camYaw); }
    if (keys['KeyA'] || keys['ArrowLeft']) { inputX += Math.sin(camYaw + Math.PI / 2); inputZ += Math.cos(camYaw + Math.PI / 2); }
    if (keys['KeyD'] || keys['ArrowRight']) { inputX -= Math.sin(camYaw + Math.PI / 2); inputZ -= Math.cos(camYaw + Math.PI / 2); }

    const isMoving = (inputX !== 0 || inputZ !== 0);
    const targetSpeed = isMoving ? (keys['ShiftLeft'] ? 22 : 11) : 0;

    if (isMoving) {
      const len = Math.hypot(inputX, inputZ);
      inputX /= len; inputZ /= len;
      playerVel.x = THREE.MathUtils.lerp(playerVel.x, inputX * targetSpeed, 0.12);
      playerVel.z = THREE.MathUtils.lerp(playerVel.z, inputZ * targetSpeed, 0.12);
    } else {
      playerVel.x *= 0.85;
      playerVel.z *= 0.85;
    }

    playerGroup.position.x += playerVel.x * dt;
    playerGroup.position.z += playerVel.z * dt;

    const currentSpeed = playerVel.length();
    if (currentSpeed > 0.8) {
      const targetAngle = Math.atan2(playerVel.x, playerVel.z);
      playerGroup.rotation.y = THREE.MathUtils.lerp(playerGroup.rotation.y, targetAngle, 0.15);

      walkCycle += dt * (keys['ShiftLeft'] ? 14 : 9);
      // Smooth articulated limb kinetics
      leftLeg.rotation.x = Math.sin(walkCycle) * 0.65;
      rightLeg.rotation.x = -Math.sin(walkCycle) * 0.65;
      leftArm.rotation.x = -Math.sin(walkCycle) * 0.55;
      rightArm.rotation.x = Math.sin(walkCycle) * 0.55;

      // Natural vertical spine bobbing
      torso.position.y = 3.1 + Math.abs(Math.sin(walkCycle)) * 0.12;
      head.position.y = 4.75 + Math.abs(Math.sin(walkCycle)) * 0.12;
    } else {
      leftLeg.rotation.x = 0; rightLeg.rotation.x = 0;
      leftArm.rotation.x = 0; rightArm.rotation.x = 0;
      torso.position.y = 3.1; head.position.y = 4.75;
    }

    const pPos = playerGroup.position;
    const camDist = (camMode === 3 ? 80 : camDistance);
    const camHeight = (camMode === 3 ? 110 : (camDistance * 0.45 + 3));

    if (camMode === 3) {
      camera.position.set(pPos.x, pPos.y + camHeight, pPos.z + 0.1);
      camera.lookAt(pPos);
    } else {
      const cx = pPos.x - Math.sin(camYaw) * camDist;
      const cz = pPos.z - Math.cos(camYaw) * camDist;
      const cy = pPos.y + camHeight + Math.sin(camPitch) * camDist;
      camera.position.set(cx, Math.max(1.5, cy), cz);
      camera.lookAt(pPos.x, pPos.y + 2.5, pPos.z);
    }

    const dHeli = playerGroup.position.distanceTo(helicopter.mesh.position);
    const prompt = document.getElementById('action-prompt');
    if (dHeli < 18) {
      prompt.style.display = 'flex';
      document.getElementById('actText').innerText = 'হেলিকপ্টারে ওঠো (Fly Helicopter)';
    } else {
      prompt.style.display = 'none';
    }

    checkLandmarks(pPos);
  }

  updateRadar();
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();
</script>
</body>
</html>
'''

with open(r'C:\Users\ACER\Downloads\rajshahi-campus-tour\ru-campus-tour.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Realistic overhaul complete! Output written to ru-campus-tour.html (Size: {len(html_content)} bytes)")
