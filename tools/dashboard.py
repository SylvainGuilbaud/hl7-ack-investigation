#!/usr/bin/env python3
"""Dashboard for the lab simulator's delivery log (by default the lab container's current log, results/dashboard/lab<date>.jsonl).

    python3 tools/dashboard.py                 # current log -> results/dashboard/dashboard<date>.html (self-contained)
    python3 tools/dashboard.py --no-fetch -i results/lab.jsonl -o /tmp/reference.html   # view the committed reference without touching it
    python3 tools/dashboard.py --open          # ... and opens it in the browser
    python3 tools/dashboard.py --serve [PORT]  # live: re-reads the log on every refresh (default 8765)
    python3 tools/dashboard.py -i other.jsonl -o out.html

stdlib only; the page itself is vanilla JS/SVG with no external requests.
Control ids are expected as  <case>-<MODE>-<run>  (e.g. app.failrej-AR-154436).
"""
import argparse, http.server, json, os, subprocess, sys, webbrowser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True      # no __pycache__ in the repo
sys.path.insert(0, os.path.join(ROOT, "tools"))
from labpath import current_log, sibling
# Per-log siblings: lab<date>.jsonl -> dashboard<date>.html + sessions<date>.json (control id -> IRIS session id).
# A new IRIS container has new session ids, so each log keeps its own cache; the reference lab.jsonl keeps sessions.json.
SESSIONS_CACHE = os.path.join(ROOT, "results", "sessions.json")   # set from --input in main()
# Portal link target: {portal}/csp/healthshare/{ns}/EnsPortal.VisualTrace.zen?SESSIONID=<id>
OPTS = {"container": "hl7ack-iris", "portal": "http://localhost:9772", "ns": "repro", "fetch": True}

# Maps the control id (MSH-10) of every inbound HL7 request to its Interoperability session id.
MAP_CODE = """\
Set rs=##class(%SQL.Statement).%ExecDirect(,"SELECT SessionId, MessageBodyId FROM Ens.MessageHeader WHERE MessageBodyClassName='EnsLib.HL7.Message' AND SourceConfigName LIKE 'in.%' AND Type=1 ORDER BY ID")
While rs.%Next() { Set m=##class(EnsLib.HL7.Message).%OpenId(rs.MessageBodyId) If $IsObject(m) Write "MAP|",m.GetValueAt("MSH:10"),"|",rs.SessionId,! }
"""


def load_sessions():
    """control id -> session id, asked from the running IRIS container; falls back to the cached file."""
    cache = {}
    if os.path.exists(SESSIONS_CACHE):
        try:
            cache = json.load(open(SESSIONS_CACHE))
        except ValueError:
            pass
    if not OPTS["fetch"]:
        return cache
    try:
        out = subprocess.run(["docker", "exec", "-i", OPTS["container"], "iris", "session", "IRIS", "-U", "REPRO"],
                             input=MAP_CODE, capture_output=True, text=True, timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return cache
    fresh = {}
    for line in out.splitlines():
        if line.startswith("MAP|"):
            _, cid, sid = (line.strip().split("|") + ["", ""])[:3]
            if cid and sid:
                fresh[cid] = sid          # later rows win: the newest session for a repeated control id
    if fresh:
        cache.update(fresh)
        try:
            json.dump(cache, open(SESSIONS_CACHE, "w"), indent=0)
        except OSError:
            pass
    return cache

# What each lab mode does (mirrors simulator/lab.py) - shown in tooltips.
MODES = {
    "AA": "plain ACK, MSA|AA", "AE": "application error, MSA|AE", "AR": "application reject, MSA|AR",
    "AR3": "MSA|AR with MSH-9 ACK^A28^ACK", "OTHERID": "AA for another message (MSA-2 mismatch)",
    "NOMSA": "reply without MSA segment", "LATE": "AA after a delay (LATE_DELAY)",
    "NOFRAME": "AA without MLLP end block", "CLOSE": "socket closed, no ACK",
}


def load(path):
    events, bad = [], 0
    if os.path.exists(path):
        with open(path, errors="replace") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    d["_n"] = n
                    events.append(d)
                except ValueError:
                    bad += 1
    return {"events": events, "bad": bad, "source": os.path.abspath(path), "modes": MODES,
            "sessions": load_sessions(),
            "trace": f"{OPTS['portal'].rstrip('/')}/csp/healthshare/{OPTS['ns']}/EnsPortal.VisualTrace.zen?SESSIONID="}


def render(path):
    data = json.dumps(load(path)).replace("</", "<\\/")
    return PAGE.replace("/*__DATA__*/null", data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default=None, help="default: the lab's current log (results/.lab-current)")
    ap.add_argument("-o", "--output", default=None, help="default: dashboard<date>.html next to the input")
    ap.add_argument("--serve", nargs="?", const=8765, type=int, metavar="PORT")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--portal", default=OPTS["portal"], help="Management Portal base URL (default %(default)s)")
    ap.add_argument("--ns", default=OPTS["ns"], help="namespace web-app name (default %(default)s)")
    ap.add_argument("--container", default=OPTS["container"], help="IRIS container queried for session ids")
    ap.add_argument("--no-fetch", action="store_true", help="don't query IRIS; use the cached sessions<date>.json only")
    a = ap.parse_args()
    OPTS.update(portal=a.portal, ns=a.ns, container=a.container, fetch=not a.no_fetch)
    global SESSIONS_CACHE
    from pathlib import Path
    log = Path(a.input).resolve() if a.input else current_log()
    a.input = str(log)
    if not log.exists():
        sys.exit(f"no lab log at {log}\nStart (or recreate) the lab container of THIS checkout: docker compose up -d --build")
    a.output = a.output or str(sibling(log, "dashboard", ".html"))
    SESSIONS_CACHE = str(sibling(log, "sessions", ".json"))

    if a.serve:
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = render(a.input).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass
        url = f"http://127.0.0.1:{a.serve}/"
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.serve), H)
        print(f"serving {a.input} at {url}  (reload the page to re-read the log)")
        if a.open:
            webbrowser.open(url)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        return

    with open(a.output, "w") as f:
        f.write(render(a.input))
    print(f"wrote {a.output}")
    if a.open:
        webbrowser.open("file://" + os.path.abspath(a.output))


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HL7 ACK lab — dashboard</title>
<style>
:root{color-scheme:light;--bg:#f6f6f6;--surface:#fff;--ink:#191919;--ink2:#666;--grid:#e6e6e6;--line:#d0d0d0;
 --recv:#257de0;--ack:#00b894;--close:#f47230;--bar:#257de0;--hl:#fff3c4;--warn:#b3261e;--ok:#0a7d1f}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#111;--surface:#191919;--ink:#efefef;--ink2:#9c9c9c;--grid:#2c2c2c;--line:#3a3a3a;
 --recv:#338ced;--ack:#00a888;--close:#e76624;--bar:#338ced;--hl:#3a3410;--warn:#ff8a80;--ok:#4cd964}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{padding:14px 20px 0}
h1{font-size:18px;margin:0}.sub{color:var(--ink2);font-size:12px;margin-top:2px}
.filters{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:10px 20px;position:sticky;top:0;background:var(--bg);z-index:5;border-bottom:1px solid var(--grid)}
.filters label{color:var(--ink2);font-size:12px;display:flex;gap:6px;align-items:center}
select,input,button{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:4px 8px}
button{cursor:pointer}button:hover{border-color:var(--ink2)}
main{padding:14px 20px 40px;display:grid;gap:14px}
.card{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:14px 16px;min-width:0}
.card h2{font-size:13px;margin:0 0 2px}.card .note{color:var(--ink2);font-size:12px;margin:0 0 10px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.kpi{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:10px 14px}
.kpi b{display:block;font-size:26px;font-weight:600;line-height:1.15}.kpi span{color:var(--ink2);font-size:12px}
.row2{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:14px}
@media(max-width:1000px){.row2{grid-template-columns:1fr}}
table{border-collapse:collapse;width:100%}
th,td{padding:4px 8px;text-align:left;border-bottom:1px solid var(--grid);white-space:nowrap}
th{color:var(--ink2);font-weight:500;cursor:pointer;position:sticky;top:0;background:var(--surface);user-select:none}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
tr.sel td{background:var(--hl)}tbody tr{cursor:pointer}tbody tr:hover td{background:var(--grid)}
.scroll{overflow:auto;max-height:420px}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--ink2);font-size:12px;margin-bottom:6px}
.legend i{display:inline-block;vertical-align:-2px;margin-right:4px}
#tip{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);padding:6px 9px;border-radius:6px;font-size:12px;max-width:340px;z-index:20;display:none;white-space:pre-line}
.pill{display:inline-block;padding:0 7px;border-radius:9px;border:1px solid var(--line);font-size:11px}
.obs li{margin:3px 0}.obs{padding-left:18px;margin:0}
.warn{color:var(--warn)}.ok{color:var(--ok)}
a{color:var(--recv)}
svg text{fill:var(--ink2);font-size:11px}svg .lbl{fill:var(--ink)}
.cell{cursor:pointer}.cell:hover rect{stroke:var(--ink);stroke-width:1.5}
code{font-family:ui-monospace,Menlo,monospace;font-size:12px}
.tabs button.on{background:var(--ink);color:var(--bg)}
</style></head><body>
<header><h1>HL7 ACK lab — delivery log</h1><div class="sub" id="src"></div></header>
<div class="filters">
 <label>Case <select id="fCase"></select></label>
 <label>Mode <select id="fMode"></select></label>
 <label>Run <select id="fRun"></select></label>
 <label>Show <select id="fOnly"><option value="">all messages</option><option value="retried">retried (&gt;1 delivery)</option><option value="noack">never ACKed</option><option value="once">delivered once</option></select></label>
 <button id="reset">Reset</button><span class="sub" id="count"></span>
</div>
<main>
 <section class="kpis" id="kpis"></section>
 <section class="card"><h2>Observations</h2><p class="note">Computed from the filtered messages.</p><ul class="obs" id="obs"></ul></section>
 <section class="row2">
  <div class="card"><h2>Deliveries per message — case × lab mode</h2>
   <p class="note">Cell = deliveries of the same control id seen by the lab (1 = no retry). Darker = more retries. “ACK n” = ACKs the lab managed to send. Click a cell to filter.</p>
   <div id="heat"></div></div>
  <div class="card"><h2>Deliveries per message</h2><p class="note">Messages sorted by delivery count (filtered). Click a bar to inspect.</p>
   <div class="scroll" id="bars" style="max-height:430px"></div></div>
 </section>
 <section class="card"><h2>Timeline</h2>
  <p class="note">One row per message. Relative = seconds since that message’s first delivery, so retry cadence lines up; absolute = wall clock.</p>
  <div class="legend">
   <span><svg width="12" height="12"><circle cx="6" cy="6" r="4.5" fill="var(--recv)"/></svg> delivery received</span>
   <span><svg width="12" height="12"><path d="M6 1L11 6L6 11L1 6Z" fill="var(--ack)"/></svg> ACK sent</span>
   <span><svg width="12" height="12"><path d="M2 2L10 10M10 2L2 10" stroke="var(--close)" stroke-width="2"/></svg> closed without ACK</span>
   <span class="tabs"><button id="tRel" class="on">relative</button> <button id="tAbs">absolute</button></span>
  </div>
  <div class="scroll" style="max-height:560px"><div id="tl"></div></div></section>
 <section class="row2">
  <div class="card"><h2>Messages</h2><p class="note">Click a header to sort, a row to see its events.</p>
   <div class="scroll"><table id="msgs"></table></div></div>
  <div class="card"><h2 id="detH">Message detail</h2><p class="note" id="detN">Select a message.</p>
   <div class="scroll"><table id="det"></table></div></div>
 </section>
 <section class="card"><h2>Raw events</h2><p class="note"><input id="q" placeholder="search any field…" size="32"> <span id="rawc" class="sub"></span></p>
  <div class="scroll"><table id="raw"></table></div></section>
</main>
<div id="tip"></div>
<script>
const DATA=/*__DATA__*/null;
const $=s=>document.querySelector(s), esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const NS="http://www.w3.org/2000/svg";
const tip=$("#tip");
const traceUrl=id=>DATA.sessions[id]?DATA.trace+encodeURIComponent(DATA.sessions[id]):null;
const traceLink=(id,txt)=>{const u=traceUrl(id);return u?`<a href="${esc(u)}" target="_blank" rel="noopener" title="Open Visual Trace (session ${esc(DATA.sessions[id])})" onclick="event.stopPropagation()">${txt||"trace ↗"}</a>`:"–"};
function showTip(e,t){tip.textContent=t;tip.style.display="block";const w=tip.offsetWidth,h=tip.offsetHeight;
 tip.style.left=Math.min(e.clientX+12,innerWidth-w-8)+"px";tip.style.top=Math.min(e.clientY+12,innerHeight-h-8)+"px"}
const hideTip=()=>tip.style.display="none";
const fmtS=ms=>ms==null?"–":(ms<1000?Math.round(ms)+" ms":(ms/1000).toFixed(ms<10000?2:1)+" s");
const median=a=>{if(!a.length)return null;a=[...a].sort((x,y)=>x-y);const m=a.length>>1;return a.length%2?a[m]:(a[m-1]+a[m])/2};
const T=s=>Date.parse(s);

// ---------- model ----------
const ev=DATA.events, bad=DATA.bad;
const msgs=new Map();
function parseId(id){const p=id.split("-");if(p.length>=3)return{run:p.pop(),mode:p.pop(),cs:p.join("-")};return{run:"?",mode:"?",cs:id}}
const recvByConn=new Map(); // conn -> pending received ts queue for latency
for(const e of ev){
 e.t=T(e.ts);
 if(!e.control_id)continue;
 let m=msgs.get(e.control_id);
 if(!m){const p=parseId(e.control_id);m={id:e.control_id,case:p.cs,run:p.run,idMode:p.mode,mode:e.mode||p.mode,ev:[],recv:[],acks:[],closes:[],lat:[],conns:new Set()};msgs.set(e.control_id,m)}
 m.ev.push(e);m.conns.add(e.conn);
 if(e.mode)m.mode=e.mode;
 if(e.event==="received"){m.recv.push(e.t);recvByConn.set(e.control_id+"|"+e.conn,e.t)}
 else if(e.event==="ack_sent"){m.acks.push(e);const r=recvByConn.get(e.control_id+"|"+e.conn);if(r!=null){m.lat.push(e.t-r);}}
 else if(e.event==="closing_without_ack")m.closes.push(e.t);
}
const M=[...msgs.values()];
for(const m of M){
 m.t0=m.ev[0].t;m.t1=m.ev[m.ev.length-1].t;m.span=m.t1-m.t0;
 m.gaps=m.recv.slice(1).map((t,i)=>t-m.recv[i]);
 m.deliveries=m.recv.length;m.nacks=m.acks.length;
 m.msa=[...new Set(m.acks.map(a=>a.msa1||"∅"))].join(",")||"–";
 m.lat_med=median(m.lat);
}
const MODE_ORDER=Object.keys(DATA.modes);
const modes=[...new Set(M.map(m=>m.mode))].sort((a,b)=>(MODE_ORDER.indexOf(a)+99)%99-(MODE_ORDER.indexOf(b)+99)%99);
const cases=[...new Set(M.map(m=>m.case))];
const runs=[...new Set(M.map(m=>m.run))].sort();

// ---------- filters ----------
const F={case:"",mode:"",run:"",only:"",sel:null};
function fill(sel,vals,all){sel.innerHTML=`<option value="">${all}</option>`+vals.map(v=>`<option>${esc(v)}</option>`).join("")}
fill($("#fCase"),cases,"all cases");fill($("#fMode"),modes,"all modes");fill($("#fRun"),runs,"all runs");
for(const [id,k] of [["fCase","case"],["fMode","mode"],["fRun","run"],["fOnly","only"]])$("#"+id).onchange=e=>{F[k]=e.target.value;draw()};
$("#reset").onclick=()=>{Object.assign(F,{case:"",mode:"",run:"",only:"",sel:null});for(const id of["fCase","fMode","fRun","fOnly"])$("#"+id).value="";draw()};
function setF(k,v){F[k]=v;$({case:"#fCase",mode:"#fMode",run:"#fRun",only:"#fOnly"}[k]).value=v}
const passes=(m,ignore)=>(ignore==="case"||!F.case||m.case===F.case)&&(ignore==="mode"||!F.mode||m.mode===F.mode)&&(!F.run||m.run===F.run)&&
 (!F.only||(F.only==="retried"&&m.deliveries>1)||(F.only==="noack"&&m.nacks===0)||(F.only==="once"&&m.deliveries===1));

// ---------- helpers ----------
function el(tag,attrs={},parent){const n=document.createElementNS(NS,tag);for(const k in attrs)n.setAttribute(k,attrs[k]);parent&&parent.appendChild(n);return n}
function mix(a){ // blue ramp light->dark by alpha over surface
 return `color-mix(in srgb, var(--bar) ${Math.round(a*100)}%, var(--surface))`}

// ---------- KPIs + observations ----------
function kpis(S){
 const tot=S.reduce((a,m)=>a+m.deliveries,0),acks=S.reduce((a,m)=>a+m.nacks,0),retried=S.filter(m=>m.deliveries>1),
  extra=S.reduce((a,m)=>a+Math.max(0,m.deliveries-1),0),noack=S.filter(m=>m.nacks===0),
  lat=S.flatMap(m=>m.lat),conns=new Set(S.flatMap(m=>[...m.conns]));
 const k=[[S.length,"distinct messages"],[tot,"deliveries received"],[extra,"redeliveries (retries)"],
  [S.length?Math.round(retried.length/S.length*100)+"%":"–",`messages retried (${retried.length})`],
  [acks,"ACKs sent by lab"],[noack.length,"messages never ACKed"],[fmtS(median(lat)),"median ACK latency"],[conns.size,"connections"]];
 $("#kpis").innerHTML=k.map(([v,l])=>`<div class="kpi"><b>${v}</b><span>${l}</span></div>`).join("");
}
function observations(S){
 const o=[];
 if(!S.length){$("#obs").innerHTML="<li>No messages match the filters.</li>";return}
 const g=(f)=>{const r=new Map();for(const m of S){const k=f(m);r.set(k,(r.get(k)||[]).concat(m))}return r};
 const byMode=g(m=>m.mode);
 for(const [md,L] of byMode){
  const mx=Math.max(...L.map(m=>m.deliveries)),mn=Math.min(...L.map(m=>m.deliveries));
  if(mx>1){const worst=L.filter(m=>m.deliveries===mx),cs=[...new Set(worst.map(m=>m.case))];
   const gaps=worst.flatMap(m=>m.gaps);
   o.push(`<b>${md}</b>: up to <b class="warn">${mx} deliveries</b> per message in ${cs.length} case(s) (${esc(cs.slice(0,4).join(", "))}${cs.length>4?"…":""})${gaps.length?`, median gap ${fmtS(median(gaps))}`:""}${mn<mx?`; ${L.filter(m=>m.deliveries===1).length} of ${L.length} delivered once`:""}.`)}
 }
 const noack=S.filter(m=>m.nacks===0&&m.mode!=="CLOSE");
 if(noack.length)o.push(`<b class="warn">${noack.length}</b> message(s) never ACKed although the mode isn’t CLOSE: ${esc(noack.slice(0,3).map(m=>m.id).join(", "))}${noack.length>3?"…":""}`);
 const mism=S.filter(m=>m.acks.some(a=>a.msa1&&/^A[AER]3?$/.test(m.mode)&&a.msa1!==m.mode.slice(0,2)));
 if(mism.length)o.push(`${mism.length} ACK(s) whose MSA-1 differs from the requested mode.`);
 const late=S.filter(m=>m.lat_med>5000);
 if(late.length)o.push(`${late.length} message(s) with ACK latency over 5 s (median ${fmtS(median(late.map(m=>m.lat_med)))}) — compare with ResponseTimeout.`);
 const noM=cases.filter(c=>!S.some(m=>m.case===c)).length;
 const one=S.filter(m=>m.deliveries===1&&m.nacks>0&&!["AA","OTHERID"].includes(m.mode));
 if(one.length)o.push(`${one.length} message(s) with a non-AA reply were <b class="ok">not retried</b> (e.g. ${esc([...new Set(one.map(m=>m.case+"/"+m.mode))].slice(0,5).join(", "))}).`);
 if(bad)o.push(`<span class="warn">${bad} unparseable line(s)</span> skipped in the log.`);
 $("#obs").innerHTML=o.map(x=>`<li>${x}</li>`).join("");
}

// ---------- heatmap ----------
function heat(){
 const cs=cases.filter(c=>M.some(m=>m.case===c)),W=64,H=40,L=130,Tp=26;
 const maxD=Math.max(1,...M.map(m=>m.deliveries));
 const svg=el("svg",{width:L+modes.length*W+4,height:Tp+cs.length*H+4,role:"img","aria-label":"Deliveries per case and mode"});
 modes.forEach((md,i)=>{const t=el("text",{x:L+i*W+W/2,y:16,"text-anchor":"middle"},svg);t.textContent=md;
  t.style.cursor="help";t.onmousemove=e=>showTip(e,md+": "+(DATA.modes[md]||""));t.onmouseleave=hideTip});
 cs.forEach((c,r)=>{const t=el("text",{x:L-8,y:Tp+r*H+H/2+4,"text-anchor":"end",class:"lbl"},svg);t.textContent=c;
  modes.forEach((md,i)=>{
  const L2=M.filter(m=>m.case===c&&m.mode===md&&(!F.run||m.run===F.run));
  const g=el("g",{class:"cell"},svg);
  const x=L+i*W,y=Tp+r*H;
  if(!L2.length){el("rect",{x:x+1,y:y+1,width:W-2,height:H-2,rx:4,fill:"none",stroke:"var(--grid)"},g);return}
  const d=Math.max(...L2.map(m=>m.deliveries)),a=Math.max(...L2.map(m=>m.nacks));
  const al=d<=1?0.12:0.25+0.75*(d-1)/Math.max(1,maxD-1);
  const sel=F.case===c&&F.mode===md;
  el("rect",{x:x+1,y:y+1,width:W-2,height:H-2,rx:4,fill:mix(al),stroke:sel?"var(--ink)":"none","stroke-width":2},g);
  const dark=al>0.55;
  const t1=el("text",{x:x+W/2,y:y+H/2-1,"text-anchor":"middle",style:`font-size:14px;font-weight:600;fill:${dark?"#fff":"var(--ink)"}`},g);t1.textContent=d;
  const t2=el("text",{x:x+W/2,y:y+H/2+12,"text-anchor":"middle",style:`font-size:10px;fill:${dark?"#fff":"var(--ink2)"}`},g);t2.textContent="ACK "+a;
  g.onmousemove=e=>showTip(e,`${c} / ${md}\n${DATA.modes[md]||""}\ndeliveries: ${d}\nACKs sent: ${a}${L2[0].gaps.length?"\nmedian retry gap: "+fmtS(median(L2.flatMap(m=>m.gaps))):""}${L2[0].lat_med!=null?"\nACK latency: "+fmtS(L2[0].lat_med):""}`);
  g.onmouseleave=hideTip;
  g.onclick=()=>{const same=F.case===c&&F.mode===md;setF("case",same?"":c);setF("mode",same?"":md);draw()};
  })});
 $("#heat").replaceChildren(svg);
}

// ---------- bars ----------
function bars(S){
 const L=[...S].sort((a,b)=>b.deliveries-a.deliveries||a.id.localeCompare(b.id)),mx=Math.max(1,...L.map(m=>m.deliveries));
 const RH=20,LW=190,W=560,svg=el("svg",{width:W,height:L.length*RH+4,role:"img","aria-label":"Deliveries per message"});
 L.forEach((m,i)=>{const y=i*RH,g=el("g",{style:"cursor:pointer"},svg);
  el("rect",{x:0,y:y,width:W,height:RH,fill:F.sel===m.id?"var(--hl)":"transparent"},g);
  const t=el("text",{x:LW-6,y:y+14,"text-anchor":"end",class:"lbl"},g);t.textContent=m.case+" · "+m.mode;
  const w=(W-LW-40)*m.deliveries/mx;
  const b=el("path",{d:`M${LW} ${y+4}h${Math.max(2,w-4)}a4 4 0 0 1 4 4v0a4 4 0 0 1 -4 4h-${Math.max(2,w-4)}z`,fill:"var(--bar)"},g);
  const v=el("text",{x:LW+w+6,y:y+14},g);v.textContent=m.deliveries;
  g.onmousemove=e=>showTip(e,`${m.id}\n${m.deliveries} deliveries, ${m.nacks} ACK(s) [${m.msa}]`);g.onmouseleave=hideTip;g.onclick=()=>{F.sel=m.id;draw();$("#detH").scrollIntoView({block:"nearest"})}});
 $("#bars").replaceChildren(svg);
}

// ---------- timeline ----------
let rel=true;
$("#tRel").onclick=()=>{rel=true;$("#tRel").classList.add("on");$("#tAbs").classList.remove("on");draw()};
$("#tAbs").onclick=()=>{rel=false;$("#tAbs").classList.add("on");$("#tRel").classList.remove("on");draw()};
function timeline(S){
 const L=[...S].sort((a,b)=>a.t0-b.t0),RH=18,LW=210,W=Math.max(700,$("#tl").parentElement.clientWidth-20),PW=W-LW-20;
 if(!L.length){$("#tl").innerHTML="";return}
 const T0=Math.min(...L.map(m=>m.t0)),span=rel?Math.max(...L.map(m=>m.span),1):Math.max(...L.map(m=>m.t1))-T0||1;
 const xs=(m,t)=>LW+PW*((rel?t-m.t0:t-T0)/span);
 const svg=el("svg",{width:W,height:L.length*RH+30,role:"img","aria-label":"Event timeline"});
 const step=[0.5,1,2,5,10,15,30,60,120,300,600].find(s=>span/1000/s<=12)||600;
 for(let s=0;s*1000<=span;s+=step){const x=LW+PW*s*1000/span;el("line",{x1:x,x2:x,y1:14,y2:L.length*RH+16,stroke:"var(--grid)"},svg);
  const t=el("text",{x,y:10,"text-anchor":"middle"},svg);t.textContent=(rel?"+":"")+s+"s"}
 L.forEach((m,i)=>{const y=16+i*RH+RH/2,g=el("g",{},svg);
  if(F.sel===m.id)el("rect",{x:0,y:y-RH/2,width:W,height:RH,fill:"var(--hl)"},g);
  const t=el("text",{x:LW-8,y:y+4,"text-anchor":"end",class:"lbl",style:"cursor:pointer"},g);t.textContent=m.case+" · "+m.mode;
  t.onclick=()=>{F.sel=m.id;draw()};
  el("line",{x1:xs(m,m.t0),x2:xs(m,m.t1),y1:y,y2:y,stroke:"var(--line)","stroke-width":2},g);
  for(const e of m.ev){
   const x=xs(m,e.t);let n,tp;
   if(e.event==="received")n=el("circle",{cx:x,cy:y,r:4.5,fill:"var(--recv)",stroke:"var(--surface)","stroke-width":2},g);
   else if(e.event==="ack_sent")n=el("path",{d:`M${x} ${y-5}L${x+5} ${y}L${x} ${y+5}L${x-5} ${y}Z`,fill:"var(--ack)",stroke:"var(--surface)","stroke-width":1.5},g);
   else if(e.event==="closing_without_ack")n=el("path",{d:`M${x-4} ${y-4}L${x+4} ${y+4}M${x+4} ${y-4}L${x-4} ${y+4}`,stroke:"var(--close)","stroke-width":2.5,fill:"none"},g);
   else continue;
   n.onmousemove=ee=>showTip(ee,`${m.id}\n${e.event}${e.msa1?" MSA|"+e.msa1:""}${e.msh9?" ("+e.msh9+")":""}\n${e.ts}  conn ${e.conn}\n+${fmtS(e.t-m.t0)} since first delivery`);n.onmouseleave=hideTip}
 });
 $("#tl").replaceChildren(svg);
}

// ---------- tables ----------
let sortK="deliveries",sortD=-1;
const COLS=[["case","case"],["mode","mode"],["run","run"],["deliveries","deliv.",1],["nacks","ACKs",1],["msa","MSA-1"],["gap","median gap",1],["lat","ACK latency",1],["span","span",1],["conns","conns",1],["first","first seen"],["trace","trace"]];
function msgTable(S){
 const val=(m,k)=>({gap:median(m.gaps)??-1,lat:m.lat_med??-1,conns:m.conns.size,first:m.t0}[k]??m[k]);
 const L=[...S].sort((a,b)=>{const x=val(a,sortK),y=val(b,sortK);return (x>y?1:x<y?-1:0)*sortD});
 $("#msgs").innerHTML=`<thead><tr>${COLS.map(([k,l,n])=>`<th data-k="${k}" class="${n?"n":""}">${l}${sortK===k?(sortD>0?" ▲":" ▼"):""}</th>`).join("")}</tr></thead><tbody>`+
 L.map(m=>`<tr data-id="${esc(m.id)}" class="${F.sel===m.id?"sel":""}"><td>${esc(m.case)}</td><td>${esc(m.mode)}</td><td>${esc(m.run)}</td>
 <td class="n ${m.deliveries>1?"warn":""}">${m.deliveries}</td><td class="n">${m.nacks}</td><td>${esc(m.msa)}</td>
 <td class="n">${m.gaps.length?fmtS(median(m.gaps)):"–"}</td><td class="n">${fmtS(m.lat_med)}</td><td class="n">${fmtS(m.span)}</td><td class="n">${m.conns.size}</td><td>${esc(m.ev[0].ts.slice(11))}</td><td>${traceLink(m.id)}</td></tr>`).join("")+"</tbody>";
 for(const th of $("#msgs").querySelectorAll("th"))if(th.dataset.k!=="trace")th.onclick=()=>{const k=th.dataset.k;sortD=sortK===k?-sortD:-1;sortK=k;draw()};
 for(const tr of $("#msgs").querySelectorAll("tbody tr"))tr.onclick=()=>{F.sel=tr.dataset.id;draw()};
}
function detail(){
 const m=msgs.get(F.sel);
 if(!m){$("#detH").textContent="Message detail";$("#detN").textContent="Select a message.";$("#det").innerHTML="";return}
 $("#detH").textContent=m.id;
 $("#detN").innerHTML=`${m.deliveries} deliveries · ${m.nacks} ACK(s) · mode <b>${esc(m.mode)}</b> — ${esc(DATA.modes[m.mode]||"")} · ${traceLink(m.id,"Open Visual Trace ↗")}`;
 $("#det").innerHTML=`<thead><tr><th>#</th><th>time</th><th class="n">Δ first</th><th class="n">Δ prev</th><th>event</th><th>conn</th><th>detail</th></tr></thead><tbody>`+
 m.ev.map((e,i)=>`<tr><td>${i+1}</td><td>${esc(e.ts.slice(11))}</td><td class="n">${fmtS(e.t-m.t0)}</td><td class="n">${i?fmtS(e.t-m.ev[i-1].t):"–"}</td><td>${esc(e.event)}</td><td>${e.conn}</td><td>${esc(e.msa1?"MSA|"+e.msa1+" "+(e.msh9||""):"")}</td></tr>`).join("")+"</tbody>";
}
function raw(){
 const q=$("#q").value.toLowerCase(),ids=new Set(M.filter(m=>passes(m)).map(m=>m.id));
 const L=ev.filter(e=>(!e.control_id||ids.has(e.control_id))&&(!(F.case||F.mode||F.run||F.only)||e.control_id)&&(!q||JSON.stringify(e).toLowerCase().includes(q)));
 $("#rawc").textContent=`${L.length} of ${ev.length} events`;
 const cols=["_n","ts","event","conn","control_id","mode","msa1","msh9","peer","trace"];
 $("#raw").innerHTML=`<thead><tr>${cols.map(c=>`<th>${c==="_n"?"line":c}</th>`).join("")}</tr></thead><tbody>`+
 L.slice(0,1000).map(e=>`<tr data-id="${esc(e.control_id||"")}">${cols.map(c=>c==="trace"?`<td>${e.control_id?traceLink(e.control_id):""}</td>`:`<td>${esc(e[c])}</td>`).join("")}</tr>`).join("")+"</tbody>";
 for(const tr of $("#raw").querySelectorAll("tbody tr"))tr.onclick=()=>{if(tr.dataset.id){F.sel=tr.dataset.id;draw()}};
}
$("#q").oninput=raw;

function draw(){
 const S=M.filter(m=>passes(m));
 if(F.sel&&!msgs.has(F.sel))F.sel=null;
 $("#count").textContent=`${S.length} of ${M.length} messages`;
 kpis(S);observations(S);heat();bars(S);timeline(S);msgTable(S);detail();raw();
}
const nTr=M.filter(m=>DATA.sessions[m.id]).length;
$("#src").textContent=`Visual Trace links: ${nTr}/${M.length} messages · `+`${DATA.source} · ${ev.length} events · ${M.length} messages · ${new Set(ev.map(e=>e.conn)).size} connections · ${ev.length?ev[0].ts+" → "+ev[ev.length-1].ts:"empty"}`;
addEventListener("resize",()=>timeline(M.filter(m=>passes(m))));
draw();
</script></body></html>
"""

if __name__ == "__main__":
    main()
