"""Neon colour theme for the Streamlit dashboard."""
import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@500;700&display=swap');
.stApp{background:radial-gradient(900px 500px at 85% 0,#2a0a4a,#0a0614) fixed;color:#f4eaff;font-family:'Rajdhani','Segoe UI',sans-serif;font-size:1.05rem}
header[data-testid="stHeader"]{background:transparent}
h1,h2,h3{font-family:'Bebas Neue',Impact,sans-serif!important;letter-spacing:.06em;font-weight:400!important;color:#fff;text-shadow:0 0 10px #ff2e97}
h1{font-size:3.2rem!important}
.stTabs [data-baseweb="tab-list"]{border-bottom:1px solid #8a2bff;gap:1.4rem}
.stTabs [data-baseweb="tab"]{background:transparent;color:#b9a9d9;letter-spacing:.22em;font-weight:700;text-transform:uppercase}
.stTabs [aria-selected="true"]{color:#00f0ff;text-shadow:0 0 10px #00f0ff}
.stTabs [data-baseweb="tab-highlight"]{background:#00f0ff;box-shadow:0 0 10px #00f0ff}
.stTextArea textarea,.stTextInput input{background:#120a22;color:#f4eaff;border:1px solid rgba(0,240,255,.5);border-radius:0;font-family:'Rajdhani',sans-serif;font-size:1.1rem}
.stTextArea textarea:focus,.stTextInput input:focus{border-color:#00f0ff;box-shadow:0 0 14px rgba(0,240,255,.45)}
div[data-baseweb="select"]>div{background:#120a22;border:1px solid rgba(0,240,255,.5);border-radius:0;color:#f4eaff}
.stButton>button,.stDownloadButton>button{background:#ff2e97;color:#0a0614;border:0;border-radius:0;font-weight:700;letter-spacing:.3em;text-transform:uppercase;box-shadow:0 0 18px #ff2e97;transition:box-shadow .2s,transform .2s}
.stButton>button p{color:#0a0614;font-weight:700}
.stButton>button:hover{background:#ff5cb0;color:#0a0614;box-shadow:0 0 34px #ff2e97,0 0 60px rgba(255,46,151,.5);transform:translateY(-1px)}
[data-testid="stMetricValue"]{font-family:'Bebas Neue',Impact,sans-serif;font-size:3.2rem;color:#ff2e97;text-shadow:0 0 14px #ff2e97}
[data-testid="stMetricLabel"]{letter-spacing:.25em;color:#00f0ff;text-transform:uppercase;font-weight:700}
[data-testid="stDataFrame"]{border:1px solid rgba(0,240,255,.4);box-shadow:0 0 14px rgba(0,240,255,.2)}
div[data-testid="stAlert"]{border-radius:0;border:1px solid #8a2bff;background:#120a22}
hr{border-color:#8a2bff}
"""


def apply_theme() -> None:
    st.markdown("<style>" + "".join(l.strip() for l in _CSS.strip().splitlines()) + "</style>", unsafe_allow_html=True)