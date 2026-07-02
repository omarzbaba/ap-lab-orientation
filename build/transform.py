#!/usr/bin/env python3
"""Fork the TQM 3D deck into Dr. Favaza's 'Intro to the AP Lab' orientation deck.
v3 presenter: stepped beats with (1) one-point-per-click list reveal,
(2) photo paired with a one-line explanation per frame, (3) photos that slide in
from their diorama and fan out as they accumulate.

Usage: python transform.py <base.html> <out.html> [content.json]
"""
import sys, json, html, os

base_path, out_path = sys.argv[1], sys.argv[2]
content_path = sys.argv[3] if len(sys.argv) > 3 else None

with open(base_path, 'r', encoding='utf-8') as f:
    src = f.read()

def replace_once(s, old, new, label):
    n = s.count(old)
    if n == 0:
        print(f"  [WARN] not found: {label}"); return s
    if n > 1:
        print(f"  [WARN] {n}x (replacing all): {label}")
    return s.replace(old, new)

# ---------- 1. Branding ----------
brand = [
    ("<title>Total Quality Management in Digital Pathology — Grand Rounds</title>",
     "<title>The Anatomic Pathology Lab — An Introduction</title>", "title"),
    ('<div id="pres-header">TQM in Digital Pathology &nbsp;&nbsp;·&nbsp;&nbsp; PALM Grand Rounds &nbsp;&nbsp;·&nbsp;&nbsp; April 2026 &nbsp;&nbsp;·&nbsp;&nbsp; OZB / JMT</div>',
     '<div id="pres-header">The Anatomic Pathology Lab &nbsp;&nbsp;·&nbsp;&nbsp; An Introduction &nbsp;&nbsp;·&nbsp;&nbsp; Medical Student &amp; Resident Orientation</div>', "pres-header"),
    ('<h1 class="intro-line visible" id="intro-h1">TOTAL QUALITY MANAGEMENT<br>IN DIGITAL PATHOLOGY</h1>',
     '<h1 class="intro-line visible" id="intro-h1">THE ANATOMIC<br>PATHOLOGY LAB</h1>', "intro-h1"),
    ('<h2 class="intro-line visible" id="intro-h2">From Tissues to Pixels</h2>',
     '<h2 class="intro-line visible" id="intro-h2">An Introduction</h2>', "intro-h2"),
    ('<div class="intro-authors intro-line visible" id="intro-authors">Omar Z. Baba, MD<br>J. Mark Tuthill, MD</div>',
     '<div class="intro-authors intro-line visible" id="intro-authors">Laura Favaza, MD</div>', "intro-authors"),
    ('<div class="intro-event intro-line visible" id="intro-event">Grand Rounds &bull; April 14, 2026<br>Department of Pathology &amp; Laboratory Medicine<br>Henry Ford Health</div>',
     '<div class="intro-event intro-line visible" id="intro-event">A Guided Tour for Medical Students<br>&amp; Transitional Residents<br>Department of Pathology</div>', "intro-event"),
    ('<h1>TQM in Digital Pathology</h1>',
     '<h1>The Anatomic Pathology Lab</h1>', "topbar-h1"),
    ('<span class="subtitle">From Tissues to Pixels &bull; Grand Rounds &bull; Henry Ford Health</span>',
     '<span class="subtitle">An Introduction &bull; A Guided Tour of the AP Lab</span>', "topbar-subtitle"),
    ('<h1>TOTAL QUALITY MANAGEMENT<br>IN DIGITAL PATHOLOGY</h1>',
     '<h1>THE ANATOMIC<br>PATHOLOGY LAB</h1>', "center-title-h1"),
    ('<h2>From Tissues to Pixels</h2>',
     '<h2>An Introduction</h2>', "center-title-h2"),
    ('<div class="tagline" style="font-size:18px;line-height:2.2;">Omar Z. Baba, MD<br>J. Mark Tuthill, MD<br>Henry Ford Health<br>April 2026</div>',
     '<div class="tagline" style="font-size:18px;line-height:2.2;">Laura Favaza, MD<br>An Orientation for Medical Students<br>&amp; Transitional Residents</div>', "center-title-tagline"),
    ('GRAND ROUNDS &nbsp;·&nbsp; HENRY FORD HEALTH', 'ANATOMIC PATHOLOGY &nbsp;·&nbsp; AN INTRODUCTION', "closing-c1"),
    ('Total Quality Management<br>in Digital Pathology', 'The Anatomic Pathology Lab', "closing-h1"),
    ('>Omar Z. Baba, MD</div>', '>Laura Favaza, MD</div>', "closing-author1"),
    ('>J. Mark Tuthill, MD</div>', '>Medical Student &amp; Resident Orientation</div>', "closing-author2"),
    ('>Henry Ford Health &nbsp;·&nbsp; Detroit, Michigan</div>', '>A Guided Tour of the AP Lab</div>', "closing-org"),
]
print("Branding:")
for old, new, label in brand:
    src = replace_once(src, old, new, label)

# ---------- 2. Hide the HFH floating logo ----------
src = replace_once(src, '<div id="hfh-float">', '<div id="hfh-float" style="display:none">', "hfh-logo-hide")

# ---------- 2b. Vendor Three.js locally (offline portability) ----------
src = replace_once(src, "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
                   "assets/vendor/three.min.js", "three-vendor")

# ---------- 3. Presenter CSS ----------
CSS = r"""
  /* ── AP Lab Orientation: stepped station presenter ── */
  #content-overlay, #ihc-right-panel { display:none !important; }
  #ap-stage{ position:fixed; inset:0; z-index:60; pointer-events:none; font-family:'Inter','Segoe UI',sans-serif; }
  #ap-stage::before{ content:''; position:absolute; inset:0; pointer-events:none; opacity:0; transition:opacity .6s ease;
    background:linear-gradient(100deg, rgba(244,247,250,0.985) 0%, rgba(244,247,250,0.95) 27%, rgba(244,247,250,0.72) 40%, rgba(244,247,250,0.0) 60%); }
  #ap-stage.on::before{ opacity:1; }
  .ap-chip{ position:absolute; top:78px; left:56px; max-width:48vw; opacity:0; transform:translateY(-8px); transition:opacity .55s, transform .55s; }
  #ap-stage.on .ap-chip{ opacity:1; transform:none; }
  .ap-chip .ap-step{ display:block; font-size:13px; font-weight:800; letter-spacing:3px; color:#0077b6; text-transform:uppercase; margin-bottom:7px; }
  .ap-chip .ap-title{ display:block; font-size:34px; font-weight:800; color:#0d1b2a; line-height:1.08; letter-spacing:.3px; }
  .ap-chip .ap-rule{ width:64px; height:4px; border-radius:3px; margin-top:14px; background:linear-gradient(90deg,#0077b6,#00b4d8); }

  .ap-rail{ position:absolute; left:56px; top:184px; bottom:176px; width:min(40vw,500px); display:flex; flex-direction:column; justify-content:center; pointer-events:none; }
  .ap-hook{ font-size:25px; line-height:1.42; font-weight:600; color:#0d1b2a; opacity:0; transform:translateY(16px); animation:apRise .6s cubic-bezier(.16,1,.3,1) forwards; }
  .ap-eyebrow{ font-size:12px; font-weight:800; letter-spacing:2.5px; text-transform:uppercase; color:#0077b6; margin-bottom:12px; opacity:0; animation:apRise .5s .02s forwards; }
  .ap-lead{ font-size:22px; line-height:1.45; font-weight:600; color:#0d1b2a; opacity:0; transform:translateY(14px); animation:apRise .6s .05s forwards; }
  .ap-h{ font-size:13px; font-weight:800; letter-spacing:2.5px; text-transform:uppercase; color:#0077b6; margin-bottom:14px; opacity:0; animation:apRise .5s forwards; }
  .ap-list{ list-style:none; padding:0; margin:0; }
  .ap-list li{ font-size:17.5px; line-height:1.44; color:#26384a; margin-bottom:12px; padding-left:27px; position:relative; }
  .ap-list li::before{ content:''; position:absolute; left:0; top:9px; width:11px; height:11px; border-radius:50%; background:linear-gradient(135deg,#0077b6,#00b4d8); box-shadow:0 2px 6px rgba(0,119,182,.4); }
  .ap-list li.in{ animation:apItem .55s cubic-bezier(.16,1,.3,1); }
  .ap-fact{ font-size:20px; line-height:1.5; color:#0d1b2a; background:linear-gradient(90deg,rgba(0,180,216,.14),rgba(0,119,182,.04)); border-left:4px solid #00b4d8; border-radius:0 14px 14px 0; padding:18px 22px; box-shadow:0 12px 34px rgba(8,24,40,.10); opacity:0; transform:translateY(14px); animation:apRise .6s forwards; }
  .ap-fact .ap-fl{ font-weight:800; color:#0077b6; margin-right:5px; }

  .ap-photos{ position:absolute; right:7vw; top:50%; width:min(40vw,560px); height:72vh; transform:translateY(-50%); pointer-events:none; }
  .ap-photo-card{ position:absolute; top:50%; left:50%; width:min(33vw,440px); margin:0; background:#fff; border-radius:18px; overflow:hidden; box-shadow:0 30px 72px rgba(8,24,40,.34); will-change:transform,opacity; }
  .ap-photo-card img{ display:block; width:100%; max-height:62vh; object-fit:cover; background:#e6edf3; }
  .ap-photo-card .ap-real{ position:absolute; top:13px; left:13px; z-index:3; font-size:10px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; color:#fff; background:rgba(0,119,182,.92); padding:4px 11px; border-radius:30px; box-shadow:0 4px 12px rgba(0,0,0,.2); }
  /* "whole-slide scanner" capture reveal — a cyan line sweeps the photo as it pops in */
  .ap-photo-card .ap-scan{ position:absolute; left:0; right:0; top:0; height:4px; z-index:4; pointer-events:none; opacity:0;
    background:linear-gradient(90deg, rgba(0,180,216,0), rgba(0,180,216,.95) 45%, rgba(180,240,255,1) 50%, rgba(0,180,216,.95) 55%, rgba(0,180,216,0));
    box-shadow:0 0 22px 6px rgba(0,180,216,.5); }
  .ap-photo-card .ap-scan.run{ animation:apScan .95s cubic-bezier(.4,0,.2,1) forwards; }
  .ap-photo-card .ap-glare{ position:absolute; inset:0; z-index:2; pointer-events:none; border-radius:18px; opacity:0;
    background:linear-gradient(120deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.35) 50%, rgba(255,255,255,0) 60%); }
  .ap-photo-card .ap-glare.run{ animation:apGlare 1.1s ease-out .1s forwards; }
  @keyframes apScan{ 0%{ top:-2%; opacity:0; } 12%{ opacity:1; } 86%{ opacity:1; } 100%{ top:101%; opacity:0; } }
  @keyframes apGlare{ 0%{ transform:translateX(-60%); opacity:0; } 30%{ opacity:1; } 100%{ transform:translateX(60%); opacity:0; } }

  .ap-foot{ position:absolute; left:56px; bottom:60px; display:flex; align-items:center; gap:16px; pointer-events:auto; opacity:0; transition:opacity .5s; }
  #ap-stage.on .ap-foot{ opacity:1; }
  .ap-dots{ display:flex; gap:8px; align-items:center; }
  .ap-dot{ width:8px; height:8px; border-radius:50%; background:rgba(0,119,182,.22); transition:all .3s; }
  .ap-dot.on{ background:#0077b6; transform:scale(1.4); }
  .ap-dot.done{ background:rgba(0,119,182,.5); }
  .ap-btn{ appearance:none; border:1px solid rgba(0,119,182,.35); background:rgba(255,255,255,.72); -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px); color:#0077b6; font-weight:700; font-size:12.5px; letter-spacing:1px; text-transform:uppercase; padding:9px 17px; border-radius:30px; cursor:pointer; transition:all .2s; min-width:118px; }
  .ap-btn:hover{ background:#0077b6; color:#fff; border-color:#0077b6; }
  .ap-btn.ghost{ background:transparent; border-color:rgba(0,119,182,.22); padding:9px 13px; min-width:0; }
  @keyframes apItem{ from{ opacity:0; transform:translateX(-12px); } to{ opacity:1; transform:none; } }
  @keyframes apRise{ to{ opacity:1; transform:none; } }
</style>
</head>"""
src = replace_once(src, "</style>\n</head>", CSS, "presenter-css")

# ---------- 4. Journey nav ----------
def replace_block(s, start_marker, new_block, label):
    i = s.find(start_marker)
    if i < 0:
        print(f"  [WARN] block start not found: {label}"); return s
    j = s.find("\n];", i)
    if j < 0:
        print(f"  [WARN] block end not found: {label}"); return s
    end = j + len("\n];")
    print(f"  replaced block: {label} ({s[i:end].count(chr(10))+1} lines)")
    return s[:i] + new_block + s[end:]

BNAV = """const BNAV_SLIDES=[
  {id:'overview',label:'The Journey',short:'\\u2302',action:()=>navigateTo(-1)},
  {id:'sep1'},
  {id:'s0',label:'1 · Origin',short:'1',action:()=>navigateTo(0)},
  {id:'s1',label:'2 · Transport',short:'2',action:()=>navigateTo(1)},
  {id:'s2',label:'3 · Receipt',short:'3',action:()=>navigateTo(2)},
  {id:'s3',label:'4 · Grossing',short:'4',action:()=>navigateTo(3)},
  {id:'s4',label:'5 · Fixation',short:'5',action:()=>navigateTo(4)},
  {id:'sep2'},
  {id:'s5',label:'6 · Processing',short:'6',action:()=>navigateTo(5)},
  {id:'s6',label:'7 · Embedding',short:'7',action:()=>navigateTo(6)},
  {id:'s7',label:'8 · Microtomy',short:'8',action:()=>navigateTo(7)},
  {id:'s8',label:'9 · H&E Staining',short:'9',action:()=>navigateTo(8)},
  {id:'s9',label:'10 · Special / IHC',short:'10',action:()=>navigateTo(9)},
  {id:'s10',label:'11 · Coverslip',short:'11',action:()=>navigateTo(10)},
  {id:'s11',label:'12 · Collation',short:'12',action:()=>navigateTo(11)},
  {id:'sep3'},
  {id:'s12',label:'13 · Scanning',short:'13',action:()=>navigateTo(12)},
  {id:'s13',label:'14 · AI Assist',short:'14',action:()=>navigateTo(13)},
  {id:'s14',label:'15 · Sign-Out',short:'15',action:()=>navigateTo(14)},
  {id:'sep4'},
  {id:'closing',label:'Wrap-Up',short:'\\u2605',action:()=>{if(!closingActive)showClosing();}},
];"""
print("Nav:")
src = replace_block(src, "const BNAV_SLIDES=[", BNAV, "BNAV_SLIDES")

# ---------- 5. STATIONS with beats ----------
LABELS = {0:"Overview",1:"Origin",2:"Transport",3:"Receipt",4:"Grossing",5:"Fixation",
          6:"Processing",7:"Embedding",8:"Microtomy",9:"H&E",10:"Special/IHC",11:"Coverslip",
          12:"Collation",13:"Scanning",14:"AI Assist",15:"Sign-Out"}
COLORS = {0:0x0077b6,1:0x5a6b7a,2:0xe67e22,3:0x3498db,4:0xc0392b,5:0xf39c12,6:0x16a085,
          7:0x8e44ad,8:0x2980b9,9:0xd6336c,10:0x9b59b6,11:0x27ae60,12:0x34495e,13:0x00b4d8,
          14:0x6c5ce7,15:0x0a7d5a}

def esc_tl(s):
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "$\\{")

def build_beats(c):
    beats = []
    if c.get("hook"):
        beats.append({"kind": "title", "hook": c["hook"]})
    if c.get("whatHappens"):
        beats.append({"kind": "points", "heading": "What happens here", "items": c["whatHappens"]})
    for p in (c.get("photos") or []):
        beats.append({"kind": "photo",
                      "src": "assets/img/" + os.path.basename(p["file"]),
                      "caption": p["caption"]})
    if c.get("whyItMatters"):
        beats.append({"kind": "points", "heading": "Why it matters", "items": c["whyItMatters"]})
    if c.get("funFact"):
        beats.append({"kind": "fact", "text": c["funFact"]})
    return beats

if content_path:
    data = json.load(open(content_path))
    by_id = {d["stationId"]: d for d in data}
    entries = []
    for sid in range(16):
        d = by_id.get(sid)
        if not d or not d.get("content"):
            print(f"  [WARN] missing content for station {sid}"); continue
        c = d["content"]
        phase = d.get("phase", "")
        step = "THE SPECIMEN JOURNEY" if sid == 0 else f"STATION {sid:02d} · {phase}"
        title = d.get("title", "")
        label = LABELS.get(sid, title.title())
        short = d.get("short", str(sid))
        color = COLORS.get(sid, 0x0077b6)
        beats = json.dumps(build_beats(c), ensure_ascii=False)
        narr = (c.get("narration") or "").replace("--", "—")
        entries.append(
            f'  {{ id: {sid}, label: "{label}", short: "{short}", title: "{esc_tl(title)}", '
            f'stepLabel: "{esc_tl(step)}", color: 0x{color:06x},\n'
            f'    beats: {beats},\n'
            f'    content: `<!-- {esc_tl(narr)} -->` }}')
    STATIONS = "const STATIONS = [\n" + ",\n".join(entries) + "\n];"
    print("Stations:")
    src = replace_block(src, "const STATIONS = [", STATIONS, "STATIONS")

# ---------- 6. Inject the station presenter before </body> ----------
PRESENTER = r"""
<script>
/* ── AP Lab Orientation — stepped Station Presenter ───────────────────────────
   Each station plays as beats. Lists reveal one point per click; photos pair with
   a one-line explanation and slide in from their diorama, fanning out as they
   accumulate. Wraps navigateTo/goNext/goPrev. */
(function(){
  if (window.__apPresenter) return; window.__apPresenter = true;

  var stage = document.createElement('div');
  stage.id = 'ap-stage';
  stage.innerHTML =
    '<div class="ap-chip"><span class="ap-step"></span><span class="ap-title"></span><div class="ap-rule"></div></div>' +
    '<div class="ap-rail"></div>' +
    '<div class="ap-photos"></div>' +
    '<div class="ap-foot">' +
      '<button class="ap-btn ghost" data-act="prev">&#9664;</button>' +
      '<div class="ap-dots"></div>' +
      '<button class="ap-btn" data-act="next">Continue &#9656;</button>' +
    '</div>';
  document.body.appendChild(stage);

  var elStep = stage.querySelector('.ap-step');
  var elTitle = stage.querySelector('.ap-title');
  var rail = stage.querySelector('.ap-rail');
  var photos = stage.querySelector('.ap-photos');
  var dots = stage.querySelector('.ap-dots');
  var nextBtn = stage.querySelector('[data-act="next"]');

  var beats = [], idx = 0, sub = 0, on = false;
  var railIdx = -1, railSub = -1;

  function stationData(){ return (typeof currentStation!=='undefined' && currentStation>=0 && typeof STATIONS!=='undefined') ? STATIONS[currentStation+1] : null; }
  function active(){ return on && typeof currentStation!=='undefined' && currentStation>=0 && !(typeof closingActive!=='undefined' && closingActive); }
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function buildDots(){ dots.innerHTML=''; for(var i=0;i<beats.length;i++){ dots.appendChild(document.createElement('span')); } syncDots(); }
  function syncDots(){ var c=dots.children; for(var i=0;i<c.length;i++){ c[i].className='ap-dot'+(i===idx?' on':(i<idx?' done':'')); } }

  function photoBeatsUpTo(i){ var a=[]; for(var j=0;j<=i;j++){ if(beats[j] && beats[j].kind==='photo') a.push(beats[j]); } return a; }
  function totalPhotos(){ var n=0; for(var j=0;j<beats.length;j++){ if(beats[j].kind==='photo') n++; } return n; }

  function fanTransform(depth){
    var rot = -2 - depth*7, x = -depth*40, y = -depth*8, s = (1 - depth*0.06).toFixed(3);
    return 'translate(calc(-50% + '+x+'px), calc(-50% + '+y+'px)) rotate('+rot+'deg) scale('+s+')';
  }

  function renderPhotos(forward){
    var pics = photoBeatsUpTo(idx), n = pics.length;
    photos.innerHTML='';
    for(var k=0;k<n;k++){
      var depth = (n-1)-k;
      var card = document.createElement('figure');
      card.className = 'ap-photo-card';
      card.style.zIndex = String(10+k);
      card.innerHTML = '<span class="ap-real">Real lab photo</span><img src="'+pics[k].src+'" alt="">';
      photos.appendChild(card);
      var finalT = fanTransform(depth);
      if (k===n-1 && forward){
        // active photo slides in from its diorama (lower-right) and pops to the fan
        card.style.transition='none';
        card.style.transform='translate(calc(-50% + 96px), calc(-50% + 52px)) rotate(7deg) scale(.8)';
        card.style.opacity='0';
        void card.offsetWidth;
        card.style.transition='transform .72s cubic-bezier(.18,1.25,.4,1), opacity .5s ease';
        card.style.transform=finalT; card.style.opacity='1';
        var scan=document.createElement('div'); scan.className='ap-scan';
        var glare=document.createElement('div'); glare.className='ap-glare';
        card.appendChild(scan); card.appendChild(glare);
        setTimeout(function(){ scan.classList.add('run'); glare.classList.add('run'); }, 150);
      } else {
        card.style.transition='none';
        card.style.transform=finalT;
        card.style.opacity = depth===0 ? '1' : String(Math.max(0.5, 1-depth*0.16));
      }
    }
  }

  function renderRail(forward){
    var b = beats[idx];
    if (b.kind==='points'){
      var ul = (railIdx===idx) ? rail.querySelector('.ap-list') : null;
      if (ul){
        if (sub > railSub){
          for (var i=railSub+1;i<=sub && i<b.items.length;i++){
            var li=document.createElement('li'); li.className='in'; li.textContent=b.items[i]; ul.appendChild(li);
          }
        } else if (sub < railSub){
          for (var r=railSub;r>sub;r--){ if(ul.lastChild) ul.removeChild(ul.lastChild); }
        }
        railSub=sub; return;
      }
      var items=''; for (var i2=0;i2<=sub && i2<b.items.length;i2++){ items+='<li'+(i2===sub?' class="in"':'')+'>'+esc(b.items[i2])+'</li>'; }
      rail.innerHTML='<div class="ap-beat"><div class="ap-h">'+esc(b.heading)+'</div><ul class="ap-list">'+items+'</ul></div>';
      railIdx=idx; railSub=sub; return;
    }
    railIdx=idx; railSub=-1;
    var html='';
    if (b.kind==='title'){ html='<div class="ap-hook">'+esc(b.hook)+'</div>'; }
    else if (b.kind==='photo'){
      var pics=photoBeatsUpTo(idx);
      html='<div class="ap-eyebrow">Real lab photo &middot; '+pics.length+' / '+totalPhotos()+'</div><div class="ap-lead">'+esc(b.caption)+'</div>';
    } else if (b.kind==='fact'){
      html='<div class="ap-fact"><span class="ap-fl">Did you know?</span>'+esc(b.text)+'</div>';
    }
    rail.innerHTML='<div class="ap-beat">'+html+'</div>';
  }

  function updateFootLabel(){
    var b=beats[idx];
    var more = (b && b.kind==='points' && sub < b.items.length-1);
    nextBtn.innerHTML = more ? 'More &#9662;' : 'Continue &#9656;';
  }

  function renderBeat(forward){
    syncDots();
    renderRail(forward);
    if (beats[idx] && beats[idx].kind==='photo') renderPhotos(forward); else photos.innerHTML='';
    updateFootLabel();
  }

  function enter(){
    var s = stationData(); if(!s){ exit(); return; }
    beats=(s.beats||[]); idx=0; sub=0; on=true; railIdx=-1; railSub=-1;
    elStep.textContent=s.stepLabel||''; elTitle.textContent=s.title||'';
    stage.classList.add('on'); buildDots();
    rail.innerHTML=''; photos.innerHTML='';
    setTimeout(function(){ if(active()) renderBeat(true); }, 420);
  }
  function exit(){ on=false; stage.classList.remove('on'); rail.innerHTML=''; photos.innerHTML=''; railIdx=-1; }

  function nextStep(){
    var b=beats[idx];
    if (b && b.kind==='points' && sub < b.items.length-1){ sub++; renderBeat(true); return true; }
    if (idx < beats.length-1){ idx++; sub=0; renderBeat(true); return true; }
    return false;
  }
  function prevStep(){
    var b=beats[idx];
    if (b && b.kind==='points' && sub > 0){ sub--; renderBeat(false); return true; }
    if (idx > 0){ idx--; var pb=beats[idx]; sub=(pb && pb.kind==='points')?(pb.items.length-1):0; renderBeat(false); return true; }
    return false;
  }

  var _nav=window.navigateTo;
  window.navigateTo=function(i){
    var prev=(typeof currentStation!=='undefined')?currentStation:-99;
    _nav(i);
    if (typeof currentStation==='undefined') return;
    if (currentStation>=0 && currentStation!==prev) enter();
    else if (currentStation<0) exit();
  };
  var _next=window.goNext, _prev=window.goPrev;
  // Clean linear walk over stations only — bypasses the base engine's TQM section flow
  // (clinical scenario, variability, Zarbo/Chitale pre-analytics, IHC, QP2, frameworks).
  window.goNext=function(){
    if (active() && nextStep()) return;
    exit();
    if (typeof closingActive!=='undefined' && closingActive) return;
    var cs=(typeof currentStation!=='undefined')?currentStation:-1, last=STATIONS.length-2;
    if (cs<0){ navigateTo(0); return; }
    if (cs<last){ navigateTo(cs+1); return; }
    if (typeof showClosing==='function') showClosing();
  };
  window.goPrev=function(){
    if (active() && prevStep()) return;
    exit();
    if (typeof closingActive!=='undefined' && closingActive){ if(typeof hideClosing==='function') hideClosing(); navigateTo(STATIONS.length-2); return; }
    var cs=(typeof currentStation!=='undefined')?currentStation:-1;
    if (cs<=0){ navigateTo(-1); return; }
    navigateTo(cs-1);
  };

  var nb=document.getElementById('next-btn'), pb=document.getElementById('prev-btn');
  if (nb) nb.onclick=function(e){ if(e&&e.stopPropagation)e.stopPropagation(); window.goNext(); };
  if (pb) pb.onclick=function(e){ if(e&&e.stopPropagation)e.stopPropagation(); window.goPrev(); };
  stage.querySelector('.ap-foot').addEventListener('click', function(e){
    var btn=e.target.closest('[data-act]'); if(!btn) return; e.stopPropagation();
    if (btn.dataset.act==='next') window.goNext(); else window.goPrev();
  });
})();
</script>
</body>"""
i = src.rfind("</body>")
if i < 0:
    print("  [WARN] </body> not found; appending presenter at end")
    src = src + PRESENTER
else:
    src = src[:i] + PRESENTER + src[i+len("</body>"):]
print("Presenter injected.")

# ---------- Living-lab: continuous motion for a true 3D-animated feel ----------
LIVINGLAB = r"""
<script>
/* Living-lab: ambient motes, breathing camera, hero-orbit overview, idle instrument motion.
   Layered on top of the engine — only acts when parked (never fights the camera tween). */
(function(){
  if(window.__livingLab) return; window.__livingLab=true;
  if(typeof THREE==='undefined'||typeof scene==='undefined') return;
  // 1) Ambient drifting motes for depth / atmosphere
  var motes=null, spd=[], MN=300;
  try{
    var geo=new THREE.BufferGeometry(), pos=new Float32Array(MN*3);
    for(var i=0;i<MN;i++){ var r=16+Math.random()*46, a=Math.random()*Math.PI*2;
      pos[i*3]=Math.cos(a)*r; pos[i*3+1]=0.5+Math.random()*28; pos[i*3+2]=Math.sin(a)*r; spd.push(0.003+Math.random()*0.008); }
    geo.setAttribute('position', new THREE.BufferAttribute(pos,3));
    var mat=new THREE.PointsMaterial({color:0x3a86b8,size:0.13,transparent:true,opacity:0.42,depthWrite:false});
    motes=new THREE.Points(geo,mat); motes.renderOrder=-1; scene.add(motes);
  }catch(e){}
  // 2) Tag instrument meshes for idle motion
  try{
    if(typeof stationGroups!=='undefined'){
      for(var s=0;s<stationGroups.length;s++){
        var g=stationGroups[s]; g.userData.leds=[]; g.userData.liquids=[]; g.userData.instr=null;
        for(var c=0;c<g.children.length;c++){ if(g.children[c].type==='Group'){ g.userData.instr=g.children[c]; break; } }
        if(g.userData.instr) g.userData.instrBaseY=g.userData.instr.rotation.y;
        g.traverse(function(m){
          if(!m.isMesh||!m.geometry) return; var gt=m.geometry.type, p=m.geometry.parameters;
          if(gt==='SphereGeometry'&&m.material&&m.material.isMeshBasicMaterial&&p&&p.radius&&p.radius<0.17){
            m.material=m.material.clone(); m.material.transparent=true;
            g.userData.leds.push({m:m,base:(m.material.opacity||1),ph:Math.random()*6.28}); }
          if(typeof MATS!=='undefined'&&m.material===MATS.liquid){ g.userData.liquids.push({m:m,base:m.scale.y,ph:Math.random()*6.28}); }
        });
      }
    }
  }catch(e){}
  // 3) Continuous rAF loop
  function loop(){
    requestAnimationFrame(loop);
    try{
      var now=performance.now(), t=now*0.001;
      if(motes){ var a=motes.geometry.attributes.position, arr=a.array;
        for(var i=0;i<MN;i++){ arr[i*3+1]+=spd[i]; if(arr[i*3+1]>30) arr[i*3+1]=0.5; } a.needsUpdate=true; motes.rotation.y=t*0.006; }
      var ready=(typeof introComplete!=='undefined'&&introComplete);
      var anim=(typeof isAnimating!=='undefined'&&isAnimating);
      var closing=(typeof closingActive!=='undefined'&&closingActive);
      var fly=(typeof flyoverActive!=='undefined'&&flyoverActive);
      if(typeof stationGroups!=='undefined'){
        for(var s=0;s<stationGroups.length;s++){ var g=stationGroups[s];
          for(var L=0;L<g.userData.leds.length;L++){ var led=g.userData.leds[L];
            led.m.material.opacity=led.base*(0.5+0.5*Math.abs(Math.sin(t*2.2+led.ph))); }
          for(var Q=0;Q<g.userData.liquids.length;Q++){ var lq=g.userData.liquids[Q];
            lq.m.scale.y=lq.base*(1+0.06*Math.sin(t*1.7+lq.ph)); }
          if(g.userData.instr){ var focused=(typeof currentStation!=='undefined'&&s===currentStation&&ready&&!anim);
            g.userData.instr.rotation.y=g.userData.instrBaseY+(focused?Math.sin(t*0.6)*0.14:0); }
        }
      }
      if(ready&&!anim&&!closing&&!fly&&typeof camTo!=='undefined'&&camTo&&camTo.pos){
        if(typeof currentStation!=='undefined'&&currentStation>=0){
          var bx=camTo.pos.x,by=camTo.pos.y,bz=camTo.pos.z,tx=camTo.target.x,ty=camTo.target.y,tz=camTo.target.z;
          var ang=Math.sin(now*0.00016)*0.028, bob=Math.sin(now*0.0003)*0.28;
          var dx=bx-tx,dz=bz-tz,ca=Math.cos(ang),sa=Math.sin(ang);
          camera.position.set(tx+dx*ca-dz*sa, by+bob, tz+dx*sa+dz*ca);
          camTarget.set(tx,ty+bob*0.25,tz); camera.lookAt(camTarget);
        } else if(currentStation<0 && !((typeof narrativeActive!=='undefined'&&narrativeActive)||(typeof varActive!=='undefined'&&varActive)||(typeof preanalyticalActive!=='undefined'&&preanalyticalActive))){
          var oa=now*0.00006; camera.position.set(Math.sin(oa)*26,44,Math.cos(oa)*26); camTarget.set(0,2,0); camera.lookAt(camTarget);
        }
      }
    }catch(e){}
  }
  requestAnimationFrame(loop);
})();
</script>
"""
j = src.rfind("</body>")
if j >= 0:
    src = src[:j] + LIVINGLAB + src[j:]
    print("Living-lab injected.")

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(src)
print(f"\nWrote {out_path} ({len(src)} bytes)")
