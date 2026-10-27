"""Animated neon title intro for the Streamlit dashboard (CSS only, no JavaScript)."""
import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@500;700&display=swap');
.pdi{--t:1s;--u:1vw;--pink:#ff2e97;--cyan:#00f0ff;--violet:#8a2bff;--ink:#0a0614;position:fixed;inset:0;z-index:1000000;overflow:hidden;background:var(--ink);color:#f4eaff;font-family:'Bebas Neue',Impact,'Arial Narrow',sans-serif;pointer-events:none;animation:pdi-out calc(var(--t)*.7) cubic-bezier(.7,0,.2,1) calc(var(--t)*5.3) forwards}
.pdi *{box-sizing:border-box}
.pdi::after{content:'';position:absolute;inset:0;z-index:9;background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 1px,transparent 1px 3px)}
.pdi .bg{position:absolute;inset:0;background:radial-gradient(55% 55% at 50% 50%,rgba(138,43,255,.5),rgba(255,46,151,.12) 60%,transparent 80%);animation:pdi-fade calc(var(--t)*.8) ease calc(var(--t)*2.4) both}
.pdi .pan{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);gap:calc(var(--u)*.35);padding:calc(var(--u)*.35);animation:pdi-pan calc(var(--t)*.25) ease-in calc(var(--t)*2.3) forwards}
.pdi .p{--d:.3;--c:var(--pink);--g:rgba(255,46,151,.5);position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:calc(var(--u)*.8);border:1px solid var(--c);background:radial-gradient(120% 80% at 50% 100%,var(--g),var(--ink) 70%);animation:pdi-wipe calc(var(--t)*.6) cubic-bezier(.7,0,.2,1) calc(var(--t)*var(--d)) both}
.pdi .p:nth-child(2){--d:.55;--c:var(--cyan);--g:rgba(0,240,255,.4)}
.pdi .p:nth-child(3){--d:.8;--c:#ffe14d;--g:rgba(255,225,77,.35)}
.pdi .w{font-size:calc(var(--u)*7.2);line-height:.9;letter-spacing:.02em;white-space:nowrap;color:#fff;text-shadow:0 0 calc(var(--u)*.7) var(--c),0 0 calc(var(--u)*2.8) var(--c);animation:pdi-push calc(var(--t)*2.1) linear calc(var(--t)*var(--d)) both}
.pdi .k{font-family:'Rajdhani','Segoe UI',sans-serif;font-weight:700;font-size:max(calc(var(--u)*1.1),9px);letter-spacing:.32em;white-space:nowrap;color:var(--c)}
.pdi .ttl{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:calc(var(--u)*.7)}
.pdi .t1,.pdi .t2{font-size:min(calc(var(--u)*15),190px);line-height:.9;letter-spacing:.04em;white-space:nowrap}
.pdi .t1{color:#fff;text-shadow:0 0 calc(var(--u)*.9) var(--pink),0 0 calc(var(--u)*3.4) var(--pink);animation:pdi-slam calc(var(--t)*.5) cubic-bezier(.2,1.3,.3,1) calc(var(--t)*2.5) both,pdi-glitch calc(var(--t)*.5) steps(1,end) calc(var(--t)*4.4)}
.pdi .t2{color:transparent;-webkit-text-stroke:max(calc(var(--u)*.22),1px) var(--cyan);text-shadow:0 0 calc(var(--u)*2.4) rgba(0,240,255,.7);animation:pdi-slam calc(var(--t)*.5) cubic-bezier(.2,1.3,.3,1) calc(var(--t)*2.9) both,pdi-fill calc(var(--t)*.6) ease calc(var(--t)*3.5) forwards}
.pdi .bar{width:calc(var(--u)*46);height:max(calc(var(--u)*.3),2px);background:linear-gradient(90deg,var(--violet),var(--pink));box-shadow:0 0 calc(var(--u)*1.2) var(--pink);animation:pdi-bar calc(var(--t)*.6) cubic-bezier(.7,0,.2,1) calc(var(--t)*3.5) both}
.pdi .s{font-family:'Rajdhani','Segoe UI',sans-serif;font-weight:700;font-size:max(calc(var(--u)*1.7),10px);letter-spacing:.4em;white-space:nowrap;color:#f4eaff;animation:pdi-rise calc(var(--t)*.6) ease-out calc(var(--t)*3.9) both}
.pdi .hud{position:absolute;font-family:'Rajdhani','Segoe UI',sans-serif;font-weight:700;font-size:max(calc(var(--u)*1.05),9px);letter-spacing:.3em;white-space:nowrap;animation:pdi-rise calc(var(--t)*.5) ease-out calc(var(--t)*2.8) both}
.pdi .tl{top:calc(var(--u)*2);left:calc(var(--u)*2.4);color:var(--cyan)}
.pdi .tr{top:calc(var(--u)*2);right:calc(var(--u)*2.4);color:var(--pink);animation:pdi-rise calc(var(--t)*.5) ease-out calc(var(--t)*2.8) both,pdi-blink calc(var(--t)*1.4) ease-in-out calc(var(--t)*3.4) infinite}
.pdi .tk{bottom:calc(var(--u)*2.4);left:0;right:0;text-align:center;color:#f4eaff}
.pdi .fl{position:absolute;inset:0;z-index:8;background:linear-gradient(180deg,#fff,#ffc4e3);opacity:0;animation:pdi-fl calc(var(--t)*.4) ease-out calc(var(--t)*2.3)}
.pdi .ld{position:absolute;left:0;bottom:0;z-index:8;width:100%;height:max(calc(var(--u)*.25),3px);background:linear-gradient(90deg,var(--violet),var(--pink),var(--cyan));animation:pdi-ld calc(var(--t)*5.3) linear both}
@keyframes pdi-out{from{clip-path:inset(0 0 0 0)}to{clip-path:inset(0 0 100% 0);visibility:hidden}}
@keyframes pdi-fade{from{opacity:0}}
@keyframes pdi-pan{to{opacity:0;transform:scale(1.06)}}
@keyframes pdi-wipe{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes pdi-push{from{transform:scale(.9)}to{transform:scale(1.08)}}
@keyframes pdi-slam{from{opacity:0;transform:scale(1.8);filter:blur(14px)}}
@keyframes pdi-rise{from{opacity:0;transform:translateY(calc(var(--u)*1.2));filter:blur(4px)}}
@keyframes pdi-bar{from{width:0}}
@keyframes pdi-fill{to{color:rgba(0,240,255,.18)}}
@keyframes pdi-glitch{0%{transform:translate(calc(var(--u)*-.5),0);text-shadow:calc(var(--u)*.6) 0 0 var(--cyan),calc(var(--u)*-.6) 0 0 var(--pink)}34%{transform:translate(calc(var(--u)*.5),0) skewX(-4deg);text-shadow:calc(var(--u)*-.6) 0 0 var(--cyan),calc(var(--u)*.6) 0 0 var(--violet)}67%{transform:translate(0,calc(var(--u)*.2));text-shadow:calc(var(--u)*.3) 0 0 var(--pink),calc(var(--u)*-.3) 0 0 var(--cyan)}100%{transform:none}}
@keyframes pdi-fl{0%{opacity:0}25%{opacity:.9}100%{opacity:0}}
@keyframes pdi-ld{from{width:0}}
@keyframes pdi-blink{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.pdi{animation:pdi-out .3s ease 1.2s forwards}.pdi *{animation:none!important}.pdi .pan,.pdi .fl{display:none}}
"""

_HTML = """
<div class="pdi">
<div class="bg"></div>
<div class="pan">
<div class="p"><div class="w">URGENT</div><div class="k">ACTION REQUIRED</div></div>
<div class="p"><div class="w">VERIFY</div><div class="k">YOUR ACCOUNT</div></div>
<div class="p"><div class="w">SUSPENDED</div><div class="k">WITHIN 24 HOURS</div></div>
</div>
<div class="ttl"><div class="t1">PHISHING</div><div class="t2">DETECTOR</div><div class="bar"></div><div class="s">SCAN THE MESSAGE. CATCH THE SCAM.</div></div>
<div class="hud tl">PROJECT 01 // PHISH WATCH</div>
<div class="hud tr">SCAN ACTIVE</div>
<div class="hud tk">6 SOURCES // 87.8% ON UNSEEN SOURCES</div>
<div class="fl"></div><div class="ld"></div>
</div>
"""


def _one_line(text: str) -> str:
    # Markdown treats indented lines and blank lines as code/paragraph breaks, so send one line.
    return "".join(line.strip() for line in text.strip().splitlines())


def show_intro(once: bool = False) -> None:
    """Play the intro. once=True shows it only the first time in a browser session."""
    if once:
        if st.session_state.get("_intro_shown"):
            return
        st.session_state["_intro_shown"] = True
    st.markdown("<style>" + _one_line(_CSS) + "</style>" + _one_line(_HTML), unsafe_allow_html=True)
    