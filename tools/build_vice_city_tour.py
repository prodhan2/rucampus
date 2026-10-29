import json

with open(r'C:\Users\ACER\Downloads\rajshahi-campus-tour\tools\campus_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

buildings_json = json.dumps(data['buildings'], ensure_ascii=False)
landmarks_json = json.dumps(data['landmarks'], ensure_ascii=False)

# Build the complete HTML
html_content = r'''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>RU Campus Tour 3D — GTA Vice City Edition (রাবি ৩ডি ট্যুর)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Pricedown&family=Hind+Siliguri:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --vc-pink: #ff2a8d;
    --vc-cyan: #00e5ff;
    --vc-yellow: #ffea00;
    --vc-orange: #ff7700;
    --vc-dark: #0a0518;
    --vc-card: rgba(14, 8, 28, 0.88);
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
    text-shadow: 1px 1px 0 #000;
  }
  .vc-stars .lit {
    color: var(--vc-yellow); text-shadow: 0 0 10px var(--vc-yellow);
    animation: pulse 1s infinite alternate;
  }
  @keyframes pulse { from { opacity: 0.8; } to { opacity: 1; transform: scale(1.05); } }

  /* Weapon / Item Slot */
  .vc-weapon {
    width: 68px; height: 68px; border-radius: 12px;
    background: radial-gradient(circle, rgba(255,42,141,0.2), rgba(0,0,0,0.8));
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
    width: 170px; height: 170px; border-radius: 50%;
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

  /* Bottom Center Action Prompt */
  #action-prompt {
    position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 5, 20, 0.9); border: 2px solid var(--vc-yellow);
    border-radius: 30px; padding: 10px 24px; color: #fff;
    font-size: 16px; font-weight: 700; display: none; align-items: center; gap: 10px;
    box-shadow: 0 0 20px rgba(255, 234, 0, 0.5); backdrop-filter: blur(8px);
    animation: promptBounce 0.6s infinite alternate ease-in-out;
  }
  @keyframes promptBounce { from { transform: translateX(-50%) translateY(0); } to { transform: translateX(-50%) translateY(-6px); } }
  #action-prompt kbd {
    background: var(--vc-yellow); color: #000; padding: 3px 10px;
    border-radius: 6px; font-family: 'Orbitron', monospace; font-size: 14px; font-weight: 900;
  }

  /* Bottom Right Speedometer (Vehicles) */
  #speedo {
    position: absolute; bottom: 24px; right: 24px;
    background: rgba(10, 5, 24, 0.85); border: 2px solid var(--vc-pink);
    border-radius: 16px; padding: 10px 18px; display: none;
    flex-direction: column; align-items: flex-end;
    box-shadow: 0 0 20px rgba(255, 42, 141, 0.5); backdrop-filter: blur(6px);
  }
  #speedo .veh-name {
    font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
    color: var(--vc-cyan); font-weight: 700;
  }
  #speedo .speed-num {
    font-family: 'Orbitron', monospace; font-size: 34px; font-weight: 900;
    color: #fff; text-shadow: 0 0 12px var(--vc-pink); line-height: 1;
  }
  #speedo .speed-unit {
    font-size: 11px; color: #aaa; letter-spacing: 1px; font-weight: 600;
  }

  /* Mission / Landmark Banner (Vice City Style) */
  #mission-banner {
    position: absolute; top: 110px; left: 50%; transform: translateX(-50%) scale(0.8);
    display: none; flex-direction: column; align-items: center; text-align: center;
    background: linear-gradient(180deg, rgba(255,42,141,0.92), rgba(120,10,70,0.95));
    border: 3px solid var(--vc-yellow); border-radius: 18px; padding: 16px 36px;
    box-shadow: 0 0 35px rgba(255, 42, 141, 0.8), 0 10px 30px rgba(0,0,0,0.7);
    color: #fff; animation: bannerPop 0.4s cubic-bezier(0.18, 1.25, 0.4, 1.1) forwards;
  }
  @keyframes bannerPop {
    to { transform: translateX(-50%) scale(1); opacity: 1; }
  }
  #mission-banner .m-title {
    font-family: 'Orbitron', sans-serif; font-size: 20px; font-weight: 900;
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
    margin-top: 8px; font-family: 'Orbitron', monospace; font-size: 16px; font-weight: 900;
    color: #55ff55; text-shadow: 0 0 10px #00ff00, 1px 1px 0 #000;
  }

  /* Top Left Quick Toolbar */
  #toolbar {
    position: absolute; top: 16px; left: 20px;
    display: flex; align-items: center; gap: 8px; pointer-events: auto;
  }
  .tb-btn {
    background: rgba(14, 8, 28, 0.85); border: 1.5px solid var(--vc-cyan);
    color: #fff; border-radius: 12px; padding: 8px 14px; font-size: 13px; font-weight: 700;
    cursor: pointer; display: flex; align-items: center; gap: 6px;
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.25); backdrop-filter: blur(6px);
    transition: all 0.15s ease;
  }
  .tb-btn:hover {
    background: var(--vc-pink); border-color: var(--vc-yellow);
    box-shadow: 0 0 15px var(--vc-pink); transform: translateY(-2px);
  }

  /* ═══════════ MODALS & OVERLAYS ═══════════ */
  .modal-overlay {
    position: fixed; inset: 0; z-index: 50;
    display: flex; justify-content: center; align-items: flex-start;
    padding: 24px 16px; background: rgba(5, 2, 12, 0.78);
    backdrop-filter: blur(10px); overflow-y: auto; overflow-x: hidden;
    touch-action: pan-y; -webkit-overflow-scrolling: touch;
  }
  .modal-overlay.hidden { display: none !important; }
  .vc-sheet {
    width: min(620px, 100%); max-height: min(88vh, calc(100dvh - 36px));
    background: var(--vc-card); border-radius: 22px; padding: 26px 26px 24px;
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
    font-family: 'Orbitron', var(--bn-font); font-size: 28px; font-weight: 900;
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
    padding: 13px 28px; font-size: 16px; font-weight: 800; cursor: pointer;
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

  /* Landmark Fact Card */
  .fact-box {
    background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 14px; padding: 16px; font-size: 15px; line-height: 1.7;
    color: #e5edf5; margin: 16px 0;
  }

  /* Crosshair */
  #crosshair {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 8px; height: 8px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.7); box-shadow: 0 0 6px #fff;
    pointer-events: none; opacity: 0.6;
  }

  /* Mobile Touch Controls */
  #mobile-controls {
    position: fixed; inset: 0; pointer-events: none; z-index: 15; display: none;
  }
  .touch-stick {
    position: absolute; bottom: 24px; left: 24px; width: 110px; height: 110px;
    border-radius: 50%; background: rgba(255, 255, 255, 0.15); border: 2px solid var(--vc-cyan);
    pointer-events: auto; backdrop-filter: blur(4px);
  }
  .touch-knob {
    position: absolute; top: 50%; left: 50%; width: 44px; height: 44px;
    margin: -22px 0 0 -22px; border-radius: 50%; background: var(--vc-cyan);
    box-shadow: 0 0 15px var(--vc-cyan);
  }
  .touch-act-btn {
    position: absolute; bottom: 30px; right: 30px; width: 68px; height: 68px;
    border-radius: 50%; background: var(--vc-pink); border: 2px solid var(--vc-yellow);
    color: #fff; font-size: 13px; font-weight: 800; display: grid; place-items: center;
    pointer-events: auto; box-shadow: 0 0 18px var(--vc-pink); cursor: pointer;
  }
</style>
<!-- Load Three.js locally with CDN fallback -->
<script src="three.min.js"></script>
<script>
  if (typeof THREE === 'undefined') {
    document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\/script>');
  }
</script>
</head>
<body>

<canvas id="c"></canvas>
<div id="crosshair"></div>

<!-- HUD -->
<div id="hud">
  <!-- Top Left Quick Actions -->
  <div id="toolbar">
    <button class="tb-btn" id="btnHelp">❓ কন্ট্রোল (H)</button>
    <button class="tb-btn" id="btnTime">🌅 সানসেট (T)</button>
    <button class="tb-btn" id="btnRadio">📻 রেডিও (M)</button>
    <button class="tb-btn" id="btnCam">🎥 ভিউ (V)</button>
  </div>

  <!-- Top Right Stats -->
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
      <span class="w-icon" id="weaponIcon">👊</span>
      <span class="w-ammo">∞</span>
    </div>
  </div>

  <!-- Radar Minimap -->
  <div id="radar-box">
    <canvas id="radar" width="170" height="170"></canvas>
    <div class="radar-n">N</div>
  </div>

  <!-- Action Prompt -->
  <div id="action-prompt">
    <kbd id="actKey">F / E</kbd>
    <span id="actText">বাসে ওঠো (Drive Bus)</span>
  </div>

  <!-- Vehicle Speedometer -->
  <div id="speedo">
    <div class="veh-name" id="vehName">RU DOUBLE DECKER</div>
    <div class="speed-num" id="speedVal">0</div>
    <div class="speed-unit">KM / H</div>
  </div>

  <!-- Mission Passed / Landmark Banner -->
  <div id="mission-banner">
    <div class="m-title">★ LANDMARK VISITED ★</div>
    <div class="m-name" id="mName">কেন্দ্রীয় শহীদ মিনার</div>
    <div class="m-sub" id="mEn">Central Shaheed Minar</div>
    <div class="m-respect" id="mReward">RESPECT +100 · PASSPORT STAMPED</div>
  </div>
</div>

<!-- Touch Controls for Mobile/Tablets -->
<div id="mobile-controls">
  <div class="touch-stick" id="touchStick"><div class="touch-knob" id="touchKnob"></div></div>
  <div class="touch-act-btn" id="touchActBtn">ENTER</div>
</div>

<!-- Welcome / Intro Modal -->
<div class="modal-overlay" id="start-modal">
  <div class="vc-sheet">
    <h1 class="vc-title">রাবি ৩ডি ট্যুর · ভাইস সিটি মোড 🌴</h1>
    <div class="vc-subtitle">RAJSHAHI UNIVERSITY 3D OPEN WORLD — VICE CITY EDITION</div>
    
    <p style="font-size:15px;line-height:1.7;color:#e8edf5;margin-bottom:14px">
      স্বাগতম! পুরো <b>৭৫৩ একর রাজশাহী বিশ্ববিদ্যালয় ক্যাম্পাস</b> এখন সম্পূর্ণ <b>3D ওপেন ওয়ার্ল্ড গেম</b> হিসেবে হাজির!
      টমি ভার্সেটি স্টাইলে হেঁটে, দৌড়ে, বা যেকোনো <b>রাবি ডাবল ডেকার বাস</b>, <b>রিকশা</b> কিংবা <b>স্পোর্টস কার</b> ড্রাইভ করে ক্যাম্পাস ঘুরে দেখো।
    </p>

    <div style="background:rgba(255,42,141,0.12);border:1.5px solid var(--vc-pink);border-radius:14px;padding:12px 16px;margin-bottom:16px">
      <div style="color:var(--vc-yellow);font-weight:700;font-size:14px;margin-bottom:6px">🎮 ভাইস সিটি কন্ট্রোলস:</div>
      <div class="key-badge"><b>W A S D</b> হাঁটা / গাড়ি চালানো</div>
      <div class="key-badge"><b>SHIFT</b> স্প্রিন্ট (Sprint)</div>
      <div class="key-badge"><b>SPACE</b> লাফ / হ্যান্ডব্রেক</div>
      <div class="key-badge"><b>F বা E</b> বাসে/রিকশায় ওঠো বা নামো (Drive)</div>
      <div class="key-badge"><b>MOUSE</b> ৩৬০° ক্যামেরা ঘোরানো</div>
      <div class="key-badge"><b>V</b> ক্যামেরা ভিউ বদলানো (1st/3rd/Top)</div>
      <div class="key-badge"><b>H</b> হর্ন / রিকশার বেল</div>
      <div class="key-badge"><b>M</b> ভাইস সিটি ৮০-এর দশকের সিন্থওয়েভ গান</div>
      <div class="key-badge"><b>T</b> সানসেট / দিন / রাত পরিবর্তন</div>
    </div>

    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:20px;flex-wrap:wrap;gap:12px">
      <button class="vc-btn" id="startBtn">গেম শুরু করো (START TOUR) →</button>
      <span style="font-size:12px;color:#a0aab8">১৮টি ল্যান্ডমার্ক · ৩৭টি ভবন · ২০টি বাস</span>
    </div>
  </div>
</div>

<!-- Landmark Detail Card Modal -->
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
   CAMPUS DATA (OpenStreetMap & RU Real Coordinates)
══════════════════════════════════════════════════════════════════ */
const BUILDINGS = ''' + buildings_json + r''';
const LANDMARKS = ''' + landmarks_json + r''';

/* ── Roads ── */
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

/* ── Coordinate Mapping: 2D Campus (2600 x 1900) -> 3D World (Units) ── */
const SCALE = 0.4;
function to3D(x, y) {
  return {
    x: (x - 1300) * SCALE,
    z: (y - 1000) * SCALE
  };
}

/* ══════════════════════════════════════════════════════════════════
   AUDIO ENGINE (Vice City 80s Synthwave Radio & SFX)
══════════════════════════════════════════════════════════════════ */
class AudioEngine {
  constructor() {
    this.ctx = null;
    this.radioPlaying = false;
    this.radioTimer = null;
    this.step = 0;
    this.engineOsc = null;
    this.engineGain = null;
  }

  init() {
    if (this.ctx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContext();
    this.startEngineAudio();
  }

  startEngineAudio() {
    if (!this.ctx) return;
    this.engineOsc = this.ctx.createOscillator();
    this.engineGain = this.ctx.createGain();
    this.engineOsc.type = 'sawtooth';
    this.engineOsc.frequency.setValueAtTime(35, this.ctx.currentTime);
    this.engineGain.gain.setValueAtTime(0, this.ctx.currentTime);

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(320, this.ctx.currentTime);

    this.engineOsc.connect(filter);
    filter.connect(this.engineGain);
    this.engineGain.connect(this.ctx.destination);
    this.engineOsc.start();
  }

  updateEngine(speed, inVehicle) {
    if (!this.ctx || !this.engineGain) return;
    if (inVehicle) {
      const targetVol = 0.12;
      const targetFreq = 40 + Math.min(speed * 3.5, 120);
      this.engineGain.gain.setTargetAtTime(targetVol, this.ctx.currentTime, 0.1);
      this.engineOsc.frequency.setTargetAtTime(targetFreq, this.ctx.currentTime, 0.08);
    } else {
      this.engineGain.gain.setTargetAtTime(0, this.ctx.currentTime, 0.1);
    }
  }

  playHorn() {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [320, 400].forEach(freq => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq, now);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.45);
    });
  }

  playBell() {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [1200, 1600, 2200].forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + idx * 0.08);
      gain.gain.setValueAtTime(0.15, now + idx * 0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + idx * 0.08);
      osc.stop(now + idx * 0.08 + 0.35);
    });
  }

  playTrainWhistle() {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [440, 554, 659].forEach(freq => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 1.25);
    });
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
      gain.gain.setValueAtTime(0.15, now + i * 0.09);
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
    const melody = [440, 554, 659, 880, 659, 554, 440, 329];

    this.radioTimer = setInterval(() => {
      if (!this.radioPlaying || !this.ctx) return;
      const now = this.ctx.currentTime;
      const idx = this.step % bassline.length;

      // Bass synth
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(bassline[idx] * 0.5, now);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.2);

      // Drum kick or snare
      if (idx % 2 === 0) {
        // Kick
        const kickOsc = this.ctx.createOscillator();
        const kickGain = this.ctx.createGain();
        kickOsc.frequency.setValueAtTime(140, now);
        kickOsc.frequency.exponentialRampToValueAtTime(30, now + 0.08);
        kickGain.gain.setValueAtTime(0.15, now);
        kickGain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
        kickOsc.connect(kickGain);
        kickGain.connect(this.ctx.destination);
        kickOsc.start(now);
        kickOsc.stop(now + 0.1);
      } else {
        // Snare
        const snareOsc = this.ctx.createOscillator();
        const snareGain = this.ctx.createGain();
        snareOsc.type = 'triangle';
        snareOsc.frequency.setValueAtTime(280, now);
        snareGain.gain.setValueAtTime(0.08, now);
        snareGain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        snareOsc.connect(snareGain);
        snareGain.connect(this.ctx.destination);
        snareOsc.start(now);
        snareOsc.stop(now + 0.1);
      }

      this.step++;
    }, 180);
  }
}

const audio = new AudioEngine();

/* ══════════════════════════════════════════════════════════════════
   THREE.JS 3D WORLD SETUP
══════════════════════════════════════════════════════════════════ */
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.5, 2000);

// Sky & Lighting
let timeMode = 0; // 0: Sunset, 1: Day, 2: Night
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.2);
dirLight.position.set(200, 350, 150);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.near = 10;
dirLight.shadow.camera.far = 1000;
const d = 400;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
scene.add(dirLight);

const hemiLight = new THREE.HemisphereLight(0xffaacc, 0x224422, 0.7);
scene.add(hemiLight);

function setTimeOfDay(mode) {
  timeMode = mode;
  const btn = document.getElementById('btnTime');
  if (mode === 0) {
    // Vice City Sunset
    btn.innerHTML = '🌅 সানসেট (T)';
    scene.background = new THREE.Color(0x35143e);
    scene.fog = new THREE.FogExp2(0x451a4a, 0.0022);
    dirLight.color.setHex(0xffaa55);
    dirLight.intensity = 1.3;
    dirLight.position.set(300, 180, 200);
    hemiLight.color.setHex(0xff77aa);
    hemiLight.groundColor.setHex(0x223322);
  } else if (mode === 1) {
    // Sunny Day
    btn.innerHTML = '☀️ দিন (T)';
    scene.background = new THREE.Color(0x7bc4f5);
    scene.fog = new THREE.FogExp2(0x9bd4f8, 0.0014);
    dirLight.color.setHex(0xffffff);
    dirLight.intensity = 1.4;
    dirLight.position.set(100, 400, 100);
    hemiLight.color.setHex(0xffffff);
    hemiLight.groundColor.setHex(0x336633);
  } else {
    // Neon Night
    btn.innerHTML = '🌙 রাত (T)';
    scene.background = new THREE.Color(0x05040d);
    scene.fog = new THREE.FogExp2(0x080614, 0.003);
    dirLight.color.setHex(0x4466aa);
    dirLight.intensity = 0.4;
    dirLight.position.set(-100, 200, -100);
    hemiLight.color.setHex(0x334466);
    hemiLight.groundColor.setHex(0x0a1015);
  }
}
setTimeOfDay(0);

/* ══════════════════════════════════════════════════════════════════
   ENVIRONMENT & PROCEDURAL MESHES
══════════════════════════════════════════════════════════════════ */
// Ground Plane (Grass)
const groundGeo = new THREE.PlaneGeometry(1600, 1400, 32, 32);
const groundMat = new THREE.MeshLambertMaterial({ color: 0x3d7037 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Roads
const roadMat = new THREE.MeshLambertMaterial({ color: 0x2e3336 });
const curbMat = new THREE.MeshLambertMaterial({ color: 0x999999 });
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
  roadMesh.position.set(cx, 0.05, cz);
  roadMesh.receiveShadow = true;
  scene.add(roadMesh);

  // Center stripe
  if (rw > 20 || rd > 20) {
    const sw = rw > rd ? rw * 0.95 : 1.2;
    const sd = rw > rd ? 1.2 : rd * 0.95;
    const stripe = new THREE.Mesh(new THREE.PlaneGeometry(sw, sd), stripeMat);
    stripe.rotation.x = -Math.PI / 2;
    stripe.position.set(cx, 0.08, cz);
    scene.add(stripe);
  }
});

// Railway Track & Train
const railZ = to3D(0, 180).z;
const railGeo = new THREE.PlaneGeometry(1200, 5);
const railMat = new THREE.MeshLambertMaterial({ color: 0x5a554f });
const railMesh = new THREE.Mesh(railGeo, railMat);
railMesh.rotation.x = -Math.PI / 2;
railMesh.position.set(0, 0.1, railZ);
scene.add(railMesh);

// 3D Moving Train
const trainGroup = new THREE.Group();
const trainEngine = new THREE.Mesh(new THREE.BoxGeometry(28, 8, 5.5), new THREE.MeshLambertMaterial({ color: 0x1f7fbf }));
trainEngine.position.y = 4;
trainEngine.castShadow = true;
trainGroup.add(trainEngine);

// Passenger coaches
for (let c = 1; c <= 3; c++) {
  const coach = new THREE.Mesh(new THREE.BoxGeometry(24, 7.5, 5.2), new THREE.MeshLambertMaterial({ color: 0x228b22 }));
  coach.position.set(-c * 27, 3.8, 0);
  coach.castShadow = true;
  trainGroup.add(coach);
}
trainGroup.position.set(-300, 0, railZ);
scene.add(trainGroup);

// Trees Generator
const treeTrunkMat = new THREE.MeshLambertMaterial({ color: 0x5c4033 });
const treeLeafMat = new THREE.MeshLambertMaterial({ color: 0x2f6b3a });
const trunkBaseMat = new THREE.MeshLambertMaterial({ color: 0xffffff }); // White painted base

function createTree(x, z, scale = 1, isParisRoad = false) {
  const group = new THREE.Group();
  const trunkH = 8 * scale;
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.5 * scale, 0.8 * scale, trunkH, 6), treeTrunkMat);
  trunk.position.y = trunkH / 2;
  trunk.castShadow = true;
  group.add(trunk);

  if (isParisRoad) {
    // Iconic white and red painted trunk bottom
    const baseBand = new THREE.Mesh(new THREE.CylinderGeometry(0.82 * scale, 0.85 * scale, 2.5 * scale, 6), trunkBaseMat);
    baseBand.position.y = 1.3 * scale;
    group.add(baseBand);
  }

  // Foliage
  const leaves = new THREE.Mesh(new THREE.DodecahedronGeometry(4.5 * scale, 1), treeLeafMat);
  leaves.position.y = trunkH + 2.5 * scale;
  leaves.castShadow = true;
  group.add(leaves);

  group.position.set(x, 0, z);
  scene.add(group);
}

// Paris Road Tree Avenue (Iconic double row of tall trees)
const parisStart = to3D(500, 1050);
const parisEnd = to3D(500, 1250);
for (let i = 0; i <= 24; i++) {
  const z = parisStart.z + (parisEnd.z - parisStart.z) * (i / 24);
  createTree(parisStart.x - 14, z, 1.3, true);
  createTree(parisStart.x + 14, z, 1.3, true);
}

// Random Campus Trees
for (let i = 0; i < 90; i++) {
  const tx = (Math.random() - 0.5) * 1100;
  const tz = (Math.random() - 0.5) * 850;
  createTree(tx, tz, 0.9 + Math.random() * 0.5);
}

/* ══════════════════════════════════════════════════════════════════
   3D BUILDINGS (Extruded Blocks with Windows & Bangla Name Labels)
══════════════════════════════════════════════════════════════════ */
const buildingColors = {
  hall: 0xa84f38,      // Brick red
  ghall: 0x8a5482,     // Female halls
  library: 0xc4553a,   // Library red brick
  medical: 0x3d7e9a,   // Medical cyan-blue
  mosque: 0x2f7d6a,    // Mosque green
  museum: 0xb57c48,    // Heritage wood/terracotta
  gym: 0x4f6b8a,       // Sports blue
  block: 0xd9c298      // Academic concrete yellow
};

BUILDINGS.forEach(b => {
  const p = to3D(b.x, b.y);
  const bw = Math.max(b.w * SCALE, 14);
  const bd = Math.max(b.h * SCALE, 12);
  const bh = 14 + (Math.abs(b.x * 13 + b.y * 7) % 18); // 14 to 32m height

  const col = buildingColors[b.k] || 0xb58a63;
  const bMat = new THREE.MeshLambertMaterial({ color: col });
  const bMesh = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, bd), bMat);
  bMesh.position.set(p.x, bh / 2, p.z);
  bMesh.castShadow = true;
  bMesh.receiveShadow = true;
  scene.add(bMesh);

  // Roof Ledge
  const roof = new THREE.Mesh(new THREE.BoxGeometry(bw + 1.2, 1.2, bd + 1.2), new THREE.MeshLambertMaterial({ color: 0x333333 }));
  roof.position.set(p.x, bh + 0.6, p.z);
  scene.add(roof);

  // Floating 3D Text Canvas Sprite for Building Name
  const canvasLabel = document.createElement('canvas');
  canvasLabel.width = 512;
  canvasLabel.height = 128;
  const ctxLabel = canvasLabel.getContext('2d');
  ctxLabel.fillStyle = 'rgba(12, 6, 24, 0.85)';
  ctxLabel.roundRect(10, 10, 492, 108, 16);
  ctxLabel.fill();
  ctxLabel.strokeStyle = '#00e5ff';
  ctxLabel.lineWidth = 4;
  ctxLabel.stroke();
  ctxLabel.fillStyle = '#ffffff';
  ctxLabel.font = 'bold 36px "Hind Siliguri", sans-serif';
  ctxLabel.textAlign = 'center';
  ctxLabel.textBaseline = 'middle';
  ctxLabel.fillText(b.l, 256, 64);

  const tex = new THREE.CanvasTexture(canvasLabel);
  const spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true });
  const sprite = new THREE.Sprite(spriteMat);
  sprite.position.set(p.x, bh + 9, p.z);
  sprite.scale.set(22, 5.5, 1);
  scene.add(sprite);
});

/* ══════════════════════════════════════════════════════════════════
   SPECIAL 3D LANDMARKS
══════════════════════════════════════════════════════════════════ */
// 1. Central Shaheed Minar (4 soaring pillars + red sun disc)
(function() {
  const p = to3D(1130, 960);
  const minarGroup = new THREE.Group();

  // Elevated Hexagonal Podium
  const podium = new THREE.Mesh(new THREE.CylinderGeometry(24, 26, 3, 6), new THREE.MeshLambertMaterial({ color: 0xdddddd }));
  podium.position.y = 1.5;
  podium.receiveShadow = true;
  minarGroup.add(podium);

  // Red Sun Disc
  const sunMesh = new THREE.Mesh(new THREE.CircleGeometry(10, 32), new THREE.MeshBasicMaterial({ color: 0xff002b, side: THREE.DoubleSide }));
  sunMesh.position.set(0, 16, -1);
  minarGroup.add(sunMesh);

  // Four Pillars
  const pillarMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
  const heights = [28, 22, 22, 16];
  const xOffsets = [-7, -2.5, 2.5, 7];
  heights.forEach((h, i) => {
    const pil = new THREE.Mesh(new THREE.BoxGeometry(2.4, h, 2.4), pillarMat);
    pil.position.set(xOffsets[i], 3 + h / 2, 0);
    pil.rotation.z = (i < 2 ? -0.06 : 0.06);
    pil.castShadow = true;
    minarGroup.add(pil);
  });

  minarGroup.position.set(p.x, 0, p.z);
  scene.add(minarGroup);
})();

// 2. Central Jamia Mosque (Domes and Minarets)
(function() {
  const p = to3D(1072, 1111);
  const group = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(38, 14, 28), new THREE.MeshLambertMaterial({ color: 0xffffff }));
  base.position.y = 7;
  group.add(base);

  // Main Dome
  const dome = new THREE.Mesh(new THREE.SphereGeometry(9, 16, 16, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshLambertMaterial({ color: 0x2f7d6a }));
  dome.position.y = 14;
  group.add(dome);

  // 4 Minarets
  const minMat = new THREE.MeshLambertMaterial({ color: 0xeeeeee });
  [[-17, -12], [17, -12], [-17, 12], [17, 12]].forEach(([mx, mz]) => {
    const min = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.4, 26, 8), minMat);
    min.position.set(mx, 13, mz);
    group.add(min);
  });

  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 3. Stadium (Bowl with grandstands and soccer pitch)
(function() {
  const p = to3D(1288, 733);
  const group = new THREE.Group();
  // Pitch
  const pitch = new THREE.Mesh(new THREE.PlaneGeometry(90, 55), new THREE.MeshLambertMaterial({ color: 0x228b22 }));
  pitch.rotation.x = -Math.PI / 2;
  pitch.position.y = 0.15;
  group.add(pitch);

  // Stands
  const standMat = new THREE.MeshLambertMaterial({ color: 0xa0a8b0 });
  const standN = new THREE.Mesh(new THREE.BoxGeometry(100, 9, 14), standMat);
  standN.position.set(0, 4.5, -34);
  group.add(standN);
  const standS = new THREE.Mesh(new THREE.BoxGeometry(100, 9, 14), standMat);
  standS.position.set(0, 4.5, 34);
  group.add(standS);

  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 4. Swimming Pool (Sunken pool with water shader/plane)
(function() {
  const p = to3D(1594, 795);
  const group = new THREE.Group();
  const deck = new THREE.Mesh(new THREE.BoxGeometry(50, 0.4, 30), new THREE.MeshLambertMaterial({ color: 0xddcbaa }));
  deck.position.y = 0.2;
  group.add(deck);

  const water = new THREE.Mesh(new THREE.PlaneGeometry(42, 22), new THREE.MeshBasicMaterial({ color: 0x00bfff, transparent: true, opacity: 0.85 }));
  water.rotation.x = -Math.PI / 2;
  water.position.y = 0.25;
  group.add(water);

  group.position.set(p.x, 0, p.z);
  scene.add(group);
})();

// 5. Food Alley (খাবারের গলি - 14 vibrant food stalls)
(function() {
  const alleyX = to3D(1290, 1300).x;
  const alleyZ = to3D(1290, 1300).z;
  const stallCols = [0xff2a8d, 0x00e5ff, 0xffea00, 0xff7700, 0x55ff55, 0xaa00ff];
  for (let i = 0; i < 14; i++) {
    const group = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(7, 4.5, 5), new THREE.MeshLambertMaterial({ color: 0xddc69d }));
    body.position.y = 2.25;
    group.add(body);

    // Awning
    const col = stallCols[i % stallCols.length];
    const awning = new THREE.Mesh(new THREE.ConeGeometry(5.5, 2, 4), new THREE.MeshLambertMaterial({ color: col }));
    awning.position.y = 5.2;
    awning.rotation.y = Math.PI / 4;
    group.add(awning);

    group.position.set(alleyX - 120 + i * 18, 0, alleyZ + (i % 2 === 0 ? -6 : 6));
    scene.add(group);
  }
})();

/* ══════════════════════════════════════════════════════════════════
   VEHICLES SYSTEM (RU Bus, Rickshaw, Vice City Sports Car)
══════════════════════════════════════════════════════════════════ */
const vehicles = [];

function createRUBus(x, z, angle = 0) {
  const group = new THREE.Group();
  // Double Decker Body (Blue & White)
  const lowerBody = new THREE.Mesh(new THREE.BoxGeometry(7, 4.5, 20), new THREE.MeshLambertMaterial({ color: 0x1f7fbf }));
  lowerBody.position.y = 2.8;
  lowerBody.castShadow = true;
  group.add(lowerBody);

  const upperBody = new THREE.Mesh(new THREE.BoxGeometry(6.8, 3.8, 19.5), new THREE.MeshLambertMaterial({ color: 0xfdf6e6 }));
  upperBody.position.y = 6.8;
  upperBody.castShadow = true;
  group.add(upperBody);

  // Glass strip
  const glass = new THREE.Mesh(new THREE.BoxGeometry(7.05, 1.4, 18), new THREE.MeshLambertMaterial({ color: 0x112233 }));
  glass.position.y = 6.8;
  group.add(glass);

  // Wheels
  const wheelMat = new THREE.MeshLambertMaterial({ color: 0x151515 });
  const wheels = [];
  [[-3.6, 1.1, -6], [3.6, 1.1, -6], [-3.6, 1.1, 6], [3.6, 1.1, 6]].forEach(([wx, wy, wz]) => {
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 1, 12), wheelMat);
    wheel.rotation.z = Math.PI / 2;
    wheel.position.set(wx, wy, wz);
    group.add(wheel);
    wheels.push(wheel);
  });

  // Headlights
  const light = new THREE.SpotLight(0xfffae0, 2, 90, Math.PI / 5, 0.4);
  light.position.set(0, 2.5, 10.5);
  light.target.position.set(0, 0, 30);
  group.add(light);
  group.add(light.target);

  group.position.set(x, 0, z);
  group.rotation.y = angle;
  scene.add(group);

  const vehData = {
    type: 'bus',
    name: 'RU DOUBLE DECKER',
    mesh: group,
    wheels,
    speed: 0,
    maxSpeed: 48,
    accel: 18,
    turnSpeed: 1.5,
    angle: angle
  };
  vehicles.push(vehData);
  return vehData;
}

function createRickshaw(x, z, angle = 0) {
  const group = new THREE.Group();
  // Frame
  const frame = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.2, 4), new THREE.MeshLambertMaterial({ color: 0x222222 }));
  frame.position.y = 1.6;
  group.add(frame);

  // Hood (Colorful traditional design)
  const hood = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 2.5, 8, 1, false, 0, Math.PI), new THREE.MeshLambertMaterial({ color: 0x2f7d4a }));
  hood.rotation.z = Math.PI / 2;
  hood.rotation.y = Math.PI / 2;
  hood.position.set(0, 3.2, -0.6);
  group.add(hood);

  // 3 Wheels
  const wheelMat = new THREE.MeshLambertMaterial({ color: 0x111111 });
  const w1 = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.3, 12), wheelMat);
  w1.rotation.z = Math.PI / 2; w1.position.set(0, 0.8, 2);
  group.add(w1);
  const w2 = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.3, 12), wheelMat);
  w2.rotation.z = Math.PI / 2; w2.position.set(-1.4, 0.8, -1.2);
  group.add(w2);
  const w3 = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.3, 12), wheelMat);
  w3.rotation.z = Math.PI / 2; w3.position.set(1.4, 0.8, -1.2);
  group.add(w3);

  group.position.set(x, 0, z);
  group.rotation.y = angle;
  scene.add(group);

  const vehData = {
    type: 'rickshaw',
    name: 'CAMPUS RICKSHAW',
    mesh: group,
    wheels: [w1, w2, w3],
    speed: 0,
    maxSpeed: 24,
    accel: 14,
    turnSpeed: 2.4,
    angle: angle
  };
  vehicles.push(vehData);
  return vehData;
}

function createSportsCar(x, z, angle = 0) {
  const group = new THREE.Group();
  // Low-slung Vice City Infernus style body
  const body = new THREE.Mesh(new THREE.BoxGeometry(4.8, 1.8, 10.5), new THREE.MeshLambertMaterial({ color: 0xff0044 }));
  body.position.y = 1.2;
  body.castShadow = true;
  group.add(body);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(4.2, 1.4, 4.8), new THREE.MeshLambertMaterial({ color: 0x111122 }));
  cabin.position.set(0, 2.5, -0.5);
  group.add(cabin);

  // Wheels
  const wheelMat = new THREE.MeshLambertMaterial({ color: 0x151515 });
  const wheels = [];
  [[-2.5, 0.8, -3.2], [2.5, 0.8, -3.2], [-2.5, 0.8, 3.2], [2.5, 0.8, 3.2]].forEach(([wx, wy, wz]) => {
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.6, 12), wheelMat);
    wheel.rotation.z = Math.PI / 2;
    wheel.position.set(wx, wy, wz);
    group.add(wheel);
    wheels.push(wheel);
  });

  group.position.set(x, 0, z);
  group.rotation.y = angle;
  scene.add(group);

  const vehData = {
    type: 'car',
    name: 'INFERNUS 86',
    mesh: group,
    wheels,
    speed: 0,
    maxSpeed: 82,
    accel: 36,
    turnSpeed: 2.8,
    angle: angle
  };
  vehicles.push(vehData);
  return vehData;
}

// Spawn Vehicles on Campus
const busStand = to3D(1500, 1749);
// 20 RU Buses at the terminal
for (let i = 0; i < 20; i++) {
  const bx = to3D(944 + i * 70, 1749);
  createRUBus(bx.x, bx.z, Math.PI);
}
// Cruising Buses on Ring Road
const ringA = to3D(860, 1238);
createRUBus(ringA.x, ringA.z, 0);

// Rickshaws near Main Gate & Halls
const rGate = to3D(840, 1340);
createRickshaw(rGate.x, rGate.z, 0);
const rZia = to3D(1150, 420);
createRickshaw(rZia.x, rZia.z, Math.PI / 2);

// Vice City Sports Car near Admin Building
const carAdmin = to3D(730, 860);
createSportsCar(carAdmin.x, carAdmin.z, -Math.PI / 2);

/* ══════════════════════════════════════════════════════════════════
   3D PLAYER CHARACTER (Tommy Vercetti / Student Style)
══════════════════════════════════════════════════════════════════ */
const playerGroup = new THREE.Group();

// Torso (Hawaiian Cyan Shirt)
const torsoMat = new THREE.MeshLambertMaterial({ color: 0x00e5ff });
const torso = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.2, 0.9), torsoMat);
torso.position.y = 3.1;
torso.castShadow = true;
playerGroup.add(torso);

// Head & Hair
const skinMat = new THREE.MeshLambertMaterial({ color: 0xdeb887 });
const head = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.1, 1.0), skinMat);
head.position.y = 4.75;
playerGroup.add(head);

const hairMat = new THREE.MeshLambertMaterial({ color: 0x221100 });
const hair = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.5, 1.05), hairMat);
hair.position.y = 5.25;
playerGroup.add(hair);

// Sunglasses
const shades = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.25, 0.2), new THREE.MeshBasicMaterial({ color: 0x050505 }));
shades.position.set(0, 4.8, 0.52);
playerGroup.add(shades);

// Arms
const armMat = new THREE.MeshLambertMaterial({ color: 0xdeb887 });
const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 1.8, 0.45), armMat);
leftArm.position.set(-1.05, 3.0, 0);
playerGroup.add(leftArm);

const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.45, 1.8, 0.45), armMat);
rightArm.position.set(1.05, 3.0, 0);
playerGroup.add(rightArm);

// Legs (Blue Jeans)
const pantsMat = new THREE.MeshLambertMaterial({ color: 0x2a4477 });
const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.0, 0.6), pantsMat);
leftLeg.position.set(-0.45, 1.0, 0);
leftLeg.castShadow = true;
playerGroup.add(leftLeg);

const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.0, 0.6), pantsMat);
rightLeg.position.set(0.45, 1.0, 0);
rightLeg.castShadow = true;
playerGroup.add(rightLeg);

// Initial spawn at Main Gate
const spawnPos = to3D(860, 1400);
playerGroup.position.set(spawnPos.x, 0, spawnPos.z);
scene.add(playerGroup);

/* ══════════════════════════════════════════════════════════════════
   CAMERA & CONTROLS
══════════════════════════════════════════════════════════════════ */
let camMode = 1; // 0: Close, 1: Normal, 2: Far, 3: Top-Down
let camYaw = 0;
let camPitch = 0.25;
let camDistance = 14;

const keys = {};
window.addEventListener('keydown', e => {
  keys[e.code] = true;
  if (e.code === 'KeyV') cycleCamera();
  if (e.code === 'KeyM') {
    const on = audio.toggleRadio();
    document.getElementById('btnRadio').innerHTML = on ? '📻 রেডিও (ON)' : '📻 রেডিও (OFF)';
  }
  if (e.code === 'KeyT') {
    setTimeOfDay((timeMode + 1) % 3);
  }
  if (e.code === 'KeyH') {
    if (currentVehicle) {
      if (currentVehicle.type === 'rickshaw') audio.playBell();
      else audio.playHorn();
    }
  }
  if (e.code === 'KeyF' || e.code === 'KeyE') {
    handleVehicleEnterExit();
  }
});
window.addEventListener('keyup', e => { keys[e.code] = false; });

// Mouse Orbit Controls (Pointer Lock or Drag)
let isMouseDown = false;
canvas.addEventListener('mousedown', () => { isMouseDown = true; audio.init(); });
window.addEventListener('mouseup', () => { isMouseDown = false; });
window.addEventListener('mousemove', e => {
  if (document.pointerLockElement === canvas || isMouseDown) {
    camYaw -= e.movementX * 0.004;
    camPitch = Math.max(-0.2, Math.min(1.1, camPitch + e.movementY * 0.004));
  }
});
canvas.addEventListener('click', () => {
  if (!document.pointerLockElement) {
    canvas.requestPointerLock();
  }
});
window.addEventListener('wheel', e => {
  if (e.target.closest && e.target.closest('.modal-overlay')) return;
  camDistance = Math.max(6, Math.min(60, camDistance + e.deltaY * 0.02));
});

function cycleCamera() {
  camMode = (camMode + 1) % 4;
  const modes = ['🎥 ক্লোজ (V)', '🎥 চেজ (V)', '🎥 ফার (V)', '🎥 টপ ভিউ (V)'];
  document.getElementById('btnCam').innerHTML = modes[camMode];
}

/* ══════════════════════════════════════════════════════════════════
   GAME STATE & LOOP
══════════════════════════════════════════════════════════════════ */
let currentVehicle = null;
let playerHealth = 100;
let playerArmor = 100;
let playerCash = 125000;
let visitedLandmarks = new Set();
let walkCycle = 0;

function handleVehicleEnterExit() {
  if (currentVehicle) {
    // Exit vehicle
    playerGroup.position.copy(currentVehicle.mesh.position);
    playerGroup.position.x += 4;
    playerGroup.visible = true;
    currentVehicle = null;
    document.getElementById('speedo').style.display = 'none';
    document.getElementById('action-prompt').style.display = 'none';
  } else {
    // Check nearest vehicle
    let nearest = null;
    let minDist = 12;
    vehicles.forEach(v => {
      const d = playerGroup.position.distanceTo(v.mesh.position);
      if (d < minDist) {
        minDist = d;
        nearest = v;
      }
    });

    if (nearest) {
      currentVehicle = nearest;
      playerGroup.visible = false;
      document.getElementById('speedo').style.display = 'flex';
      document.getElementById('vehName').innerText = nearest.name;
      document.getElementById('action-prompt').style.display = 'none';
    }
  }
}

// Radar Minimap Drawing
const radarCanvas = document.getElementById('radar');
const rx = radarCanvas.getContext('2d');

function updateRadar() {
  rx.clearRect(0, 0, 170, 170);
  const cx = 85, cy = 85;
  const pPos = currentVehicle ? currentVehicle.mesh.position : playerGroup.position;

  rx.save();
  rx.translate(cx, cy);
  rx.rotate(camYaw);

  // Draw Roads on Radar
  rx.strokeStyle = '#39464d';
  rx.lineWidth = 4;
  ROADS.forEach(r => {
    const p0 = to3D(r.x, r.y);
    const p1 = to3D(r.x + r.w, r.y + r.h);
    const dx0 = (p0.x - pPos.x) * 0.45;
    const dz0 = (p0.z - pPos.z) * 0.45;
    const dx1 = (p1.x - pPos.x) * 0.45;
    const dz1 = (p1.z - pPos.z) * 0.45;
    rx.beginPath();
    rx.rect(dx0, dz0, dx1 - dx0, dz1 - dz0);
    rx.stroke();
  });

  // Draw Landmarks Blips (Yellow Stars)
  rx.fillStyle = '#ffea00';
  LANDMARKS.forEach(lm => {
    const lp = to3D(lm.x, lm.y);
    const dx = (lp.x - pPos.x) * 0.45;
    const dz = (lp.z - pPos.z) * 0.45;
    if (Math.hypot(dx, dz) < 76) {
      rx.beginPath();
      rx.arc(dx, dz, 3.5, 0, Math.PI * 2);
      rx.fill();
    }
  });

  // Draw Vehicles Blips (Cyan)
  rx.fillStyle = '#00e5ff';
  vehicles.forEach(v => {
    if (v === currentVehicle) return;
    const dx = (v.mesh.position.x - pPos.x) * 0.45;
    const dz = (v.mesh.position.z - pPos.z) * 0.45;
    if (Math.hypot(dx, dz) < 76) {
      rx.fillRect(dx - 2, dz - 2, 4, 4);
    }
  });

  rx.restore();

  // Draw Center Player Arrow (Vice City Pink)
  rx.save();
  rx.translate(cx, cy);
  rx.fillStyle = '#ff2a8d';
  rx.strokeStyle = '#ffffff';
  rx.lineWidth = 1.5;
  rx.beginPath();
  rx.moveTo(0, -9);
  rx.lineTo(6, 7);
  rx.lineTo(0, 4);
  rx.lineTo(-6, 7);
  rx.closePath();
  rx.fill();
  rx.stroke();
  rx.restore();
}

// Proximity & Landmark Discovery Check
let activeNearbyLm = null;
function checkLandmarks() {
  const pPos = currentVehicle ? currentVehicle.mesh.position : playerGroup.position;
  let nearLm = null;

  LANDMARKS.forEach(lm => {
    const lp = to3D(lm.x, lm.y);
    const dist = Math.hypot(pPos.x - lp.x, pPos.z - lp.z);
    if (dist < 28) {
      nearLm = lm;
      if (!visitedLandmarks.has(lm.id)) {
        visitedLandmarks.add(lm.id);
        triggerMissionBanner(lm);
      }
    }
  });

  activeNearbyLm = nearLm;
}

function triggerMissionBanner(lm) {
  audio.playMissionFanfare();
  playerCash += 10000;
  document.getElementById('hudCash').innerText = '$' + playerCash.toString().padStart(8, '0');

  const banner = document.getElementById('mission-banner');
  document.getElementById('mName').innerText = lm.name;
  document.getElementById('mEn').innerText = lm.en;
  banner.style.display = 'flex';

  // Speak Bangla Voice
  if ('speechSynthesis' in window) {
    const ut = new SpeechSynthesisUtterance(lm.name + '। ' + lm.fact);
    ut.lang = 'bn-BD';
    window.speechSynthesis.speak(ut);
  }

  setTimeout(() => { banner.style.display = 'none'; }, 4500);
}

// UI Buttons & Modals
document.getElementById('startBtn').addEventListener('click', () => {
  document.getElementById('start-modal').classList.add('hidden');
  audio.init();
});

document.getElementById('btnHelp').addEventListener('click', () => {
  document.getElementById('start-modal').classList.remove('hidden');
});

document.getElementById('btnTime').addEventListener('click', () => {
  setTimeOfDay((timeMode + 1) % 3);
});

document.getElementById('btnRadio').addEventListener('click', () => {
  const on = audio.toggleRadio();
  document.getElementById('btnRadio').innerHTML = on ? '📻 রেডিও (ON)' : '📻 রেডিও (OFF)';
});

document.getElementById('btnCam').addEventListener('click', cycleCamera);

document.getElementById('btnCloseLm').addEventListener('click', () => {
  document.getElementById('landmark-modal').classList.add('hidden');
});

document.getElementById('btnSpeak').addEventListener('click', () => {
  if (activeNearbyLm && 'speechSynthesis' in window) {
    const ut = new SpeechSynthesisUtterance(activeNearbyLm.name + '। ' + activeNearbyLm.fact);
    ut.lang = 'bn-BD';
    window.speechSynthesis.speak(ut);
  }
});

/* ══════════════════════════════════════════════════════════════════
   MAIN ANIMATION LOOP (60 FPS)
══════════════════════════════════════════════════════════════════ */
let lastTime = performance.now();

function animate() {
  requestAnimationFrame(animate);

  const now = performance.now();
  const dt = Math.min((now - lastTime) / 1000, 0.1);
  lastTime = now;

  // 1. Move Moving Train across campus
  trainGroup.position.x += 24 * dt;
  if (trainGroup.position.x > 500) {
    trainGroup.position.x = -500;
    audio.playTrainWhistle();
  }

  // 2. Character & Vehicle Physics
  if (currentVehicle) {
    // ── Driving Vehicle Mode ──
    const v = currentVehicle;
    let accel = 0;
    if (keys['KeyW'] || keys['ArrowUp']) accel = v.accel;
    if (keys['KeyS'] || keys['ArrowDown']) accel = -v.accel * 0.6;

    if (accel !== 0) {
      v.speed += accel * dt;
    } else {
      v.speed *= 0.95; // Friction
    }
    v.speed = Math.max(-v.maxSpeed * 0.4, Math.min(v.maxSpeed, v.speed));

    if (Math.abs(v.speed) > 0.5) {
      let turn = 0;
      if (keys['KeyA'] || keys['ArrowLeft']) turn = v.turnSpeed;
      if (keys['KeyD'] || keys['ArrowRight']) turn = -v.turnSpeed;
      v.angle += turn * (v.speed / v.maxSpeed) * dt;
    }

    v.mesh.rotation.y = v.angle;
    v.mesh.position.x += Math.sin(v.angle) * v.speed * dt;
    v.mesh.position.z += Math.cos(v.angle) * v.speed * dt;

    // Rotate Wheels
    v.wheels.forEach(w => {
      w.rotation.x += (v.speed / 4) * dt;
    });

    audio.updateEngine(Math.abs(v.speed), true);
    document.getElementById('speedVal').innerText = Math.round(Math.abs(v.speed) * 1.8);

    // Camera follow vehicle
    const targetPos = v.mesh.position;
    const camDist = (camMode === 3 ? 90 : (camDistance + 6));
    const camHeight = (camMode === 3 ? 120 : (camDistance * 0.4 + 4));

    if (camMode === 3) {
      camera.position.set(targetPos.x, targetPos.y + camHeight, targetPos.z + 0.1);
      camera.lookAt(targetPos);
    } else {
      const cx = targetPos.x - Math.sin(camYaw) * camDist;
      const cz = targetPos.z - Math.cos(camYaw) * camDist;
      const cy = targetPos.y + camHeight + Math.sin(camPitch) * camDist;
      camera.position.lerp(new THREE.Vector3(cx, cy, cz), 0.1);
      camera.lookAt(targetPos.x, targetPos.y + 2, targetPos.z);
    }
  } else {
    // ── On Foot Character Mode ──
    audio.updateEngine(0, false);
    let moveX = 0, moveZ = 0;
    if (keys['KeyW'] || keys['ArrowUp']) { moveX += Math.sin(camYaw); moveZ += Math.cos(camYaw); }
    if (keys['KeyS'] || keys['ArrowDown']) { moveX -= Math.sin(camYaw); moveZ -= Math.cos(camYaw); }
    if (keys['KeyA'] || keys['ArrowLeft']) { moveX += Math.sin(camYaw + Math.PI / 2); moveZ += Math.cos(camYaw + Math.PI / 2); }
    if (keys['KeyD'] || keys['ArrowRight']) { moveX -= Math.sin(camYaw + Math.PI / 2); moveZ -= Math.cos(camYaw + Math.PI / 2); }

    const isMoving = (moveX !== 0 || moveZ !== 0);
    const isSprinting = keys['ShiftLeft'] || keys['ShiftRight'];
    const speed = (isSprinting ? 22 : 11);

    if (isMoving) {
      const len = Math.hypot(moveX, moveZ);
      moveX /= len; moveZ /= len;

      playerGroup.position.x += moveX * speed * dt;
      playerGroup.position.z += moveZ * speed * dt;

      // Rotate player to face movement direction
      const targetAngle = Math.atan2(moveX, moveZ);
      playerGroup.rotation.y = targetAngle;

      // Walk cycle animation
      walkCycle += dt * (isSprinting ? 16 : 9);
      leftLeg.rotation.x = Math.sin(walkCycle) * 0.7;
      rightLeg.rotation.x = -Math.sin(walkCycle) * 0.7;
      leftArm.rotation.x = -Math.sin(walkCycle) * 0.6;
      rightArm.rotation.x = Math.sin(walkCycle) * 0.6;
    } else {
      leftLeg.rotation.x = 0;
      rightLeg.rotation.x = 0;
      leftArm.rotation.x = 0;
      rightArm.rotation.x = 0;
    }

    // Camera follow player
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

    // Check if near any vehicle to show prompt
    let nearV = null;
    vehicles.forEach(v => {
      if (playerGroup.position.distanceTo(v.mesh.position) < 12) nearV = v;
    });

    const prompt = document.getElementById('action-prompt');
    if (nearV) {
      prompt.style.display = 'flex';
      document.getElementById('actText').innerText = nearV.name + ' চালাও (Drive)';
    } else if (activeNearbyLm) {
      prompt.style.display = 'flex';
      document.getElementById('actText').innerText = activeNearbyLm.name + ' দেখ (Inspect)';
    } else {
      prompt.style.display = 'none';
    }
  }

  // 3. Update Radar Minimap & Check Landmarks
  updateRadar();
  checkLandmarks();

  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start loop
animate();
</script>
</body>
</html>
'''

with open(r'C:\Users\ACER\Downloads\rajshahi-campus-tour\ru-campus-tour.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated 3D Vice City Tour! File size: {len(html_content)} bytes")
