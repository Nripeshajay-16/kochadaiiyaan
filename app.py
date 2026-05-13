"""
கோச்சடையான் — Kochadaiiyaan
சைபர்பங்க் தமிழ் வானியல் தளம்
Tamil-Native Cyberpunk Astronomy Portal · v3.0
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import math
import re
from datetime import date, datetime
import textwrap
from gtts import gTTS
import tempfile

# ══════════════════════════════════════════════════════════════════
# பக்க அமைப்பு · PAGE CONFIG  (must be the very first ST call)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="கோச்சடையான் | தமிழ் வானியல் தளம்",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data(ttl=3600)
def get_nasa_apod_cached():
    return get_nasa_apod()

@st.cache_data(ttl=3600)
def translate_cached(text):
    return translate_to_tamil(text)

def tamil_voice(text):
    try:
        tts = gTTS(text=text, lang='ta')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except:
        return None

def translate_to_tamil(text):
    try:
        text = text[:1200]  # limit size to prevent API rejection
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ta",
            "dt": "t",
            "q": text,
        }
        r = requests.get(url, params=params, timeout=10)
        
        # FIXED: Loop through all the translated sentences and combine them
        translated_text = ""
        for sentence in r.json()[0]:
            if sentence[0]:
                translated_text += sentence[0]
                
        return translated_text
    except:
        return text

# ── GLOBAL LANGUAGE TOGGLE ──
# Moved here so it controls the Intro screen before the sidebar loads
lang = st.radio("🌐 Language", ["Tamil", "English"])
is_ta = (lang == "Tamil")

# 🚀 INTRO SCREEN
if "page" not in st.session_state:
    st.session_state.page = "intro"

if st.session_state.page == "intro":
    
    # Text Variables based on toggle
    intro_sub = "சைபர்பங்க் தமிழ் வானியல் தளம்" if is_ta else "CYBERPUNK TAMIL ASTRONOMY PORTAL"
    f1 = "நாசா வான்படங்கள்" if is_ta else "NASA Imagery"
    f2 = "நேரடி ISS கண்காணிப்பு" if is_ta else "ISS Live Tracking"
    f3 = "ராசி கணிப்பான்" if is_ta else "Zodiac Engine"
    f4 = "தமிழர் அறிவியல்" if is_ta else "Ancient Science"

    btn_manual = "📖 பயனர் கையேடு" if is_ta else "📖 User Manual"
    btn_enter = "✨ பயன்பாட்டைத் திற" if is_ta else "✨ Enter App"

    st.markdown(f"""
    <div style='text-align:center;padding:3rem 1rem 2rem'>
        <h1 style='font-size:4.5rem;color:#00ffe7;text-shadow:0 0 40px rgba(0,255,231,0.6), 0 0 15px rgba(0,255,231,0.8);letter-spacing:0.08em;margin-bottom:0;'>
            🚀 கோச்சடையான்
        </h1>
        <div style='font-size:1.1rem;color:#ff2d78;letter-spacing:0.3em;margin-top:15px;font-weight:700;text-transform:uppercase;'>
            {intro_sub}
        </div>
    </div>

    <div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 900px; margin: 0 auto 3.5rem auto; padding: 0 1rem;'>
        <div class='gc' style='text-align:center; padding: 2rem 1rem; border-color: rgba(0,255,231,0.4);'>
            <div style='font-size:3rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(255,255,255,0.5);'>🌌</div>
            <div style='color:#00ffe7; font-weight:600; font-size:1.1rem; letter-spacing: 0.05em;'>{f1}</div>
        </div>
        <div class='gc' style='text-align:center; padding: 2rem 1rem; border-color: rgba(255,45,120,0.4); box-shadow: 0 0 30px rgba(255,45,120,0.05);'>
            <div style='font-size:3rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(255,255,255,0.5);'>🛸</div>
            <div style='color:#ff2d78; font-weight:600; font-size:1.1rem; letter-spacing: 0.05em;'>{f2}</div>
        </div>
        <div class='gc' style='text-align:center; padding: 2rem 1rem; border-color: rgba(255,215,0,0.4); box-shadow: 0 0 30px rgba(255,215,0,0.05);'>
            <div style='font-size:3rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(255,255,255,0.5);'>♈</div>
            <div style='color:#ffd700; font-weight:600; font-size:1.1rem; letter-spacing: 0.05em;'>{f3}</div>
        </div>
        <div class='gc' style='text-align:center; padding: 2rem 1rem; border-color: rgba(199,125,255,0.4); box-shadow: 0 0 30px rgba(199,125,255,0.05);'>
            <div style='font-size:3rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(255,255,255,0.5);'>🏛️</div>
            <div style='color:#c77dff; font-weight:600; font-size:1.1rem; letter-spacing: 0.05em;'>{f4}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c_left, c_right = st.columns(2)
        with c_left:
            if st.button(btn_manual, use_container_width=True):
                st.session_state.page = "manual"
                st.rerun()
        with c_right:
            if st.button(btn_enter, use_container_width=True):
                st.session_state.page = "main"
                st.rerun()

    st.stop()

# 📖 USER MANUAL SCREEN
if st.session_state.page == "manual":
    
    manual_title = "📖 பயனர் கையேடு" if is_ta else "📖 User Manual"
    btn_back = "⬅ பின்செல்" if is_ta else "⬅ Back"
    btn_start = "🚀 பயன்பாட்டைத் தொடங்கு" if is_ta else "🚀 Start Exploring"

    st.markdown(f"""
<h1 style='color:#00ffe7;text-align:center'>
    {manual_title}
</h1>
""", unsafe_allow_html=True)

    if is_ta:
        manual_html = """
<div class='gc'>
<div class='ta'>
🚀 கோச்சடையானுக்கு வருக!<br><br>
இந்த செயலி மூலம் நீங்கள் ஆராயலாம்:<br>
🌌 நாசா இன்றைய வான்படம்<br>
📡 சர்வதேச விண்வெளி நிலைய நேரடி கண்காணிப்பு<br>
♈ ராசி மற்றும் நட்சத்திர கணிப்பான்<br>
🧠 அடிப்படை வானியல் அறிவு<br>
🏛️ பண்டைய தமிழர் வானியல்<br><br>
─────────────────────<br>
🧭 எப்படி பயன்படுத்துவது:<br>
1. Tabs பயன்படுத்தி பகுதிகளை மாற்றுங்கள்<br>
2. Date select செய்து ராசி கண்டுபிடிக்கலாம்<br>
3. ISS tab-ல் live location பார்க்கலாம்<br>
4. தமிழர் வரலாறு tab-ல் பழமையான அறிவு தெரிந்து கொள்ளலாம்<br><br>
─────────────────────<br>
💡 குறிப்புகள்:<br>
• Dark mode UI → கண்களுக்கு பாதுகாப்பானது<br>
• தமிழ் + ஆங்கிலம் கலவை → எளிதான புரிதல்<br>
• Interactive charts → சிறந்த கற்றல்
</div>
</div>
"""
    else:
        manual_html = """
<div class='gc'>
<div class='ta'>
🚀 Welcome to Kochadaiiyaan!<br><br>
This app helps you explore:<br>
🌌 NASA Astronomy Picture of the Day<br>
📡 Live ISS Tracking<br>
♈ Zodiac & Rasi Calculator<br>
🧠 Basic Astronomy Knowledge<br>
🏛️ Ancient Tamil Astronomy<br><br>
─────────────────────<br>
🧭 How to use:<br>
1. Use Tabs to navigate sections<br>
2. Select Date to calculate Zodiac<br>
3. View live location in ISS tab<br>
4. Learn ancient knowledge in Tamil History tab<br><br>
─────────────────────<br>
💡 Tips:<br>
• Dark mode UI → eye-friendly<br>
• Tamil + English mix → easy understanding<br>
• Interactive charts → better learning
</div>
</div>
"""
    
    st.markdown(manual_html, unsafe_allow_html=True)

    if st.button(btn_back):
        st.session_state.page = "intro"
        st.rerun()

    if st.button(btn_start):
        st.session_state.page = "main"
        st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════════
# CSS — கண்ணாடி தோற்றம் (Glassmorphism) + நோட்டோ சான்ஸ் தமிழ்
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

/* ── CSS Variables ── */
:root {
    --neon-cyan:    #00ffe7;
    --neon-pink:    #ff2d78;
    --neon-gold:    #ffd700;
    --neon-violet:  #c77dff;
    --glass-bg:     rgba(6, 6, 24, 0.78);
    --glass-border: rgba(0, 255, 231, 0.22);
    --glass-blur:   blur(20px);
    --body-bg:      #030316;
    --tamil-text:   #ffe8b0;
    --dim-text:     #5a6a84;
}

/* ── Base Reset ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--body-bg) !important;
    color: #dce8ff !important;
    font-family: 'Noto Sans Tamil', 'Share Tech Mono', sans-serif !important;
}

/* Ambient starfield */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 15% 45%, rgba(0,80,255,0.07) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, rgba(200,0,255,0.06) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(0,255,200,0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(3, 3, 22, 0.94) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: var(--glass-blur);
}
[data-testid="stSidebar"] * {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    color: #c0d0f0 !important;
}

/* ── Headings — Orbitron for sci-fi headers ── */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 28px var(--neon-cyan);
    letter-spacing: 0.06em;
}
h2 {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    color: var(--neon-pink) !important;
    text-shadow: 0 0 18px rgba(255,45,120,0.7);
    font-weight: 700;
}
h3 {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    color: var(--neon-gold) !important;
    font-weight: 600;
}

/* ── Tamil text utility ── */
.ta {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 1.0rem;
    line-height: 2.0;
    color: var(--tamil-text) !important;
    white-space: pre-wrap; /* Added this to preserve newlines! */
}
.ta-sm {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.82rem;
    line-height: 1.85;
    color: #8898b8 !important;
    white-space: pre-wrap; /* Added this to preserve newlines! */
}
.ta-lg {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 1.25rem;
    line-height: 2.0;
    color: var(--neon-gold) !important;
}

/* ── Glass Card ── */
.gc {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem 1.8rem;
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    box-shadow: 0 0 48px rgba(0,255,231,0.05), inset 0 0 32px rgba(0,0,0,0.45);
    margin-bottom: 1.3rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeIn 0.6s ease;
}
.gc:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 30px rgba(0,255,231,0.3);
}
.gc::after {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0.5;
}
.gc-pink {
    border-color: rgba(255,45,120,0.3);
    box-shadow: 0 0 48px rgba(255,45,120,0.05);
}
.gc-gold {
    border-color: rgba(255,215,0,0.3);
    box-shadow: 0 0 48px rgba(255,215,0,0.05);
}

/* ── Neon badge ── */
.badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    border: 1px solid var(--neon-cyan);
    color: var(--neon-cyan) !important;
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.72rem;
    box-shadow: 0 0 10px rgba(0,255,231,0.25);
    margin-right: 8px;
    letter-spacing: 0.04em;
}
.badge-pink  { border-color: var(--neon-pink)  !important; color: var(--neon-pink)   !important; box-shadow: 0 0 10px rgba(255,45,120,0.25); }
.badge-gold  { border-color: var(--neon-gold)  !important; color: var(--neon-gold)   !important; box-shadow: 0 0 10px rgba(255,215,0,0.25); }
.badge-violet{ border-color: var(--neon-violet)!important; color: var(--neon-violet) !important; box-shadow: 0 0 10px rgba(199,125,255,0.25); }

/* ── Metric box ── */
.mbox {
    background: rgba(0,255,231,0.04);
    border: 1px solid rgba(0,255,231,0.18);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    text-align: center;
}
.mval {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.45rem;
    color: var(--neon-cyan);
    text-shadow: 0 0 14px var(--neon-cyan);
}
.mlbl {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.72rem;
    color: var(--dim-text);
    margin-top: 5px;
    letter-spacing: 0.02em;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.85rem !important;
    color: #5a6a84 !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.25s;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--neon-cyan) !important;
    border-bottom-color: var(--neon-cyan) !important;
    text-shadow: 0 0 8px var(--neon-cyan);
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--neon-pink) !important;
    color: var(--neon-pink) !important;
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.88rem !important;
    border-radius: 10px;
    transition: all 0.25s;
    letter-spacing: 0.03em;
}
.stButton > button:hover {
    background: rgba(255,45,120,0.1) !important;
    box-shadow: 0 0 22px rgba(255,45,120,0.35);
}

/* ── Verse block ── */
.verse {
    background: rgba(255,215,0,0.04);
    border-left: 3px solid var(--neon-gold);
    border-radius: 0 14px 14px 0;
    padding: 1rem 1.5rem;
    margin: 0.9rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #03031a; }
::-webkit-scrollbar-thumb { background: var(--neon-cyan); border-radius: 4px; opacity: 0.4; }

/* ── Divider ── */
hr { border-color: rgba(0,255,231,0.1) !important; }

/* ── Input elements ── */
.stDateInput input, .stSelectbox select,
.stTextInput input, .stNumberInput input {
    background: rgba(0,15,35,0.85) !important;
    border: 1px solid rgba(0,255,231,0.28) !important;
    color: #dce8ff !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans Tamil', sans-serif !important;
}

/* ── Toggle ── */
.stToggle label {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 0.95rem !important;
    color: #c0d0f0 !important;
}

/* ── Info/Warning boxes ── */
.stAlert { border-radius: 12px !important; }

/* ── ISS crew status ── */
.crew-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(0,255,231,0.07);
    font-family: 'Noto Sans Tamil', sans-serif;
}
.crew-num  { color: var(--neon-pink); font-size: 0.78rem; min-width: 28px; }
.crew-name { color: #c0d4f0; font-size: 0.85rem; }
.crew-tag  { color: var(--neon-gold); font-size: 0.72rem;
             border: 1px solid rgba(255,215,0,0.3);
             border-radius: 8px; padding: 1px 7px; }
.crew-earth { color: #ff8844; font-size: 0.72rem;
              border: 1px solid rgba(255,136,68,0.3);
              border-radius: 8px; padding: 1px 7px; }

/* ── APOD title translation box ── */
.apod-title-ta {
    font-family: 'Noto Sans Tamil', sans-serif !important;
    font-size: 1.1rem;
    color: var(--neon-cyan);
    text-shadow: 0 0 10px rgba(0,255,231,0.4);
    margin: 4px 0 12px;
    line-height: 1.8;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px);}
    to { opacity: 1; transform: translateY(0);}
}

@keyframes glowText {
    0% { text-shadow: 0 0 10px #00ffe7; }
    50% { text-shadow: 0 0 30px #00ffe7; }
    100% { text-shadow: 0 0 10px #00ffe7; }
}

h1 {
    animation: glowText 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# மாறிலிகள் & தரவு அட்டவணைகள் · CONSTANTS & LOOKUP TABLES
# ══════════════════════════════════════════════════════════════════

NASA_API_KEY = "mIpg268Y9u5czjVlqg9iIFcBalLBsmSeB8AZ7r3F"   # api.nasa.gov இல் இலவசமாக பெறலாம்

# ── விண்வெளி வீரர்கள் — பூமியில் திரும்பியவர்கள் ──────────────
RETURNED_ASTRONAUTS = {
    "Sunita Williams": "பூமிக்கு திரும்பினார் ✓",
    "Barry Wilmore":   "பூமிக்கு திரும்பினார் ✓",
    "Butch Wilmore":   "பூமிக்கு திரும்பினார் ✓",
}

# ── APOD தலைப்பு மொழிபெயர்ப்பு — பொதுவான வான்-பொருட்கள் ──────
APOD_TITLE_TRANSLATIONS = {
    "sun":          "சூரியன்",
    "solar":        "சூரிய",
    "moon":         "சந்திரன்",
    "lunar":        "சந்திர",
    "mercury":      "புதன்",
    "venus":        "சுக்கிரன்",
    "mars":         "செவ்வாய்",
    "jupiter":      "குரு",
    "saturn":       "சனி",
    "uranus":       "யுரேனஸ்",
    "neptune":      "நெப்டியூன்",
    "earth":        "பூமி",
    "milky way":    "பால்வழி",
    "galaxy":       "விண்மீன் திரள்",
    "nebula":       "நெபுலா",
    "supernova":    "மகா நட்சத்திர வெடிப்பு",
    "comet":        "வால் நட்சத்திரம்",
    "asteroid":     "சிறு கோள்",
    "star":         "நட்சத்திரம்",
    "aurora":       "வட விளக்கு",
    "eclipse":      "கிரகணம்",
    "black hole":   "கரும் துளை",
    "quasar":       "குவேசார்",
    "pulsar":       "துடிக்கும் நட்சத்திரம்",
    "exoplanet":    "வேற்று கோள்",
    "hubble":       "ஹப்பிள் தொலைநோக்கி",
    "james webb":   "ஜேம்ஸ் வெப் தொலைநோக்கி",
    "nasa":         "நாசா",
    "iss":          "சர்வதேச விண்வெளி நிலையம்",
    "orbit":        "சுற்றுப்பாதை",
    "cosmic":       "அண்டவெளி",
    "space":        "விண்வெளி",
    "universe":     "பிரபஞ்சம்",
    "cluster":      "கொத்து",
    "andromeda":    "ஆண்ட்ரோமெடா",
    "crater":       "குழி",
    "telescope":    "தொலைநோக்கி",
    "meteor":       "விண்கல்",
    "night sky":    "இரவு வானம்",
    "sunrise":      "சூரிய உதயம்",
    "sunset":       "சூரிய அஸ்தமனம்",
    "conjunction":  "கிரக சேர்க்கை",
    "transit":      "கோள் கடப்பு",
}

def translate_apod_title(english_title: str) -> str:
    lower = english_title.lower()
    found = []
    for eng, tam in sorted(APOD_TITLE_TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        if eng in lower:
            found.append(tam)
            lower = lower.replace(eng, "")
    if found:
        return "· ".join(found)
    return ""

# ── கிரக பெயர்கள் · Planet name table ────────────────────────────
PLANET_NAMES = {
    "Sun":     {"tamil": "சூரியன்",   "roman": "Sūriyan",   "deity": "சூரிய பகவான்"},
    "Moon":    {"tamil": "சந்திரன்",  "roman": "Chandiran",  "deity": "சந்திர பகவான்"},
    "Mercury": {"tamil": "புதன்",     "roman": "Budhan",     "deity": "புதன் பகவான்"},
    "Venus":   {"tamil": "சுக்கிரன்","roman": "Sukran",     "deity": "சுக்கிர பகவான்"},
    "Mars":    {"tamil": "செவ்வாய்",  "roman": "Sevvāi",    "deity": "செவ்வாய் பகவான்"},
    "Jupiter": {"tamil": "குரு",      "roman": "Guru",       "deity": "குரு பகவான்"},
    "Saturn":  {"tamil": "சனி",       "roman": "Sani",       "deity": "சனி பகவான்"},
    "Uranus":  {"tamil": "யுரேனஸ்",   "roman": "Yurēnas",   "deity": "—"},
    "Neptune": {"tamil": "நெப்டியூன்","roman": "Neptiyūn",  "deity": "—"},
}

RASI_DATA = [
    {"rasi": "மேஷம்",      "roman": "Mēsham",      "modern": "Aries",       "symbol": "♈", "start": 0,   "lord": "செவ்வாய்", "element": "நெருப்பு"},
    {"rasi": "ரிஷபம்",     "roman": "Rishabam",    "modern": "Taurus",      "symbol": "♉", "start": 30,  "lord": "சுக்கிரன்","element": "மண்"},
    {"rasi": "மிதுனம்",    "roman": "Mithunam",    "modern": "Gemini",      "symbol": "♊", "start": 60,  "lord": "புதன்",    "element": "காற்று"},
    {"rasi": "கடகம்",      "roman": "Kadagam",     "modern": "Cancer",      "symbol": "♋", "start": 90,  "lord": "சந்திரன்", "element": "நீர்"},
    {"rasi": "சிம்மம்",    "roman": "Simmam",      "modern": "Leo",         "symbol": "♌", "start": 120, "lord": "சூரியன்",  "element": "நெருப்பு"},
    {"rasi": "கன்னி",      "roman": "Kanni",       "modern": "Virgo",       "symbol": "♍", "start": 150, "lord": "புதன்",    "element": "மண்"},
    {"rasi": "துலாம்",     "roman": "Thulām",      "modern": "Libra",       "symbol": "♎", "start": 180, "lord": "சுக்கிரன்","element": "காற்று"},
    {"rasi": "விருச்சிகம்","roman": "Viruchigam",  "modern": "Scorpio",     "symbol": "♏", "start": 210, "lord": "செவ்வாய்", "element": "நீர்"},
    {"rasi": "தனுசு",      "roman": "Thanusu",     "modern": "Sagittarius", "symbol": "♐", "start": 240, "lord": "குரு",     "element": "நெருப்பு"},
    {"rasi": "மகரம்",      "roman": "Magaram",     "modern": "Capricorn",   "symbol": "♑", "start": 270, "lord": "சனி",      "element": "மண்"},
    {"rasi": "கும்பம்",    "roman": "Kumbam",      "modern": "Aquarius",    "symbol": "♒", "start": 300, "lord": "சனி",      "element": "காற்று"},
    {"rasi": "மீனம்",      "roman": "Mīnam",       "modern": "Pisces",      "symbol": "♓", "start": 330, "lord": "குரு",     "element": "நீர்"},
]

NAKSHATRAS = [
    ("அஸ்வினி",     "Ashwini"),    ("பரணி",       "Bharani"),
    ("கார்த்திகை",  "Krithika"),   ("ரோகிணி",     "Rohini"),
    ("மிருகசீரிடம்","Mrigasira"),  ("திருவாதிரை", "Ardra"),
    ("புனர்பூசம்",  "Punarvasu"),  ("பூசம்",       "Pushya"),
    ("ஆயில்யம்",   "Ashlesha"),   ("மகம்",        "Magha"),
    ("பூரம்",       "Pubba"),      ("உத்திரம்",    "Uttara"),
    ("அஸ்தம்",     "Hasta"),      ("சித்திரை",    "Chitra"),
    ("சுவாதி",      "Swati"),      ("விசாகம்",     "Vishakha"),
    ("அனுஷம்",     "Anuradha"),   ("கேட்டை",      "Jyeshtha"),
    ("மூலம்",       "Moola"),      ("பூராடம்",     "Purvashadha"),
    ("உத்திராடம்",  "Uttarashadha"),("திருவோணம்", "Shravana"),
    ("அவிட்டம்",   "Dhanishtha"), ("சதயம்",       "Shatabhisha"),
    ("பூரட்டாதி",   "Purvabhadra"),("உத்திரட்டாதி","Uttarabhadra"),
    ("ரேவதி",       "Revati"),
]

PURANANURU_VERSES = [
    {"verse": "யாதும் ஊரே யாவரும் கேளிர்", "meaning": "எல்லா ஊரும் என் ஊரே; எல்லாரும் என் உறவினரே.", "translation": "Every place is my homeland; every person is my kin.", "ref": "புறநானூறு 192 · கணியன் பூங்குன்றனார்"},
    {"verse": "வையம் தகளியா வார்கடலே நெய்யாக", "meaning": "இந்த உலகையே விளக்காய் கொண்டு…", "translation": "Taking this world as the lamp, the deep ocean as its oil…", "ref": "புறநானூறு 6 · நாலாயிர திவ்யப்பிரபந்தம்"},
    {"verse": "செல்வம் நிலையாமை கண்டும் துணிவாரே", "meaning": "செல்வம் நிலையற்றது என அறிந்தும் துணிவார்கள்.", "translation": "Knowing wealth is fleeting, the brave still act.", "ref": "புறநானூறு 18"},
    {"verse": "நீரின்றி அமையாது உலகு", "meaning": "நீர் இல்லாமல் இந்த உலகம் இயங்காது.", "translation": "The world cannot exist without water.", "ref": "திருக்குறள் 20 · திருவள்ளுவர்"},
    {"verse": "ஒருமைக்கண் தான் கற்ற கல்வி ஒருவற்கு", "meaning": "ஒரு பிறவியில் கற்ற கல்வி ஏழு பிறவியிலும் உதவும்.", "translation": "Knowledge gained in one birth serves across seven lives.", "ref": "திருக்குறள் 398 · திருவள்ளுவர்"},
    {"verse": "அன்னையும் பிதாவும் முன்னறி தெய்வம்", "meaning": "தாயும் தந்தையும் முதல் தெய்வங்கள்.", "translation": "Mother and father are the first gods one knows.", "ref": "புறநானூறு 312"},
    {"verse": "காலம் பொழுது கடந்தாலும் மாண்பு மாயாது", "meaning": "காலம் கடந்தாலும் நற்செயலின் மாண்பு அழியாது.", "translation": "Though ages pass, the glory of noble deeds never fades.", "ref": "புறநானூறு 215"},
    {"verse": "மண்ணில் நல்ல வண்ணம் வாழலாம்", "meaning": "இந்த பூமியில் நல்வாழ்வு வாழலாம்.", "translation": "On this good earth, we can live beautifully.", "ref": "புறநானூறு 188"},
    {"verse": "தீது இன்றி திகழ்வது அரிது", "meaning": "குறைபாடு இல்லாமல் பளபளப்பது அரிது.", "translation": "It is rare to shine without fault.", "ref": "புறநானூறு 99"},
    {"verse": "நிலம் நீர் தீ வளி விசும்பொடு ஐந்தும்", "meaning": "நிலம், நீர், நெருப்பு, காற்று, ஆகாயம் — ஐம்பூதங்கள்.", "translation": "Earth, water, fire, wind, and space — the five elements.", "ref": "புறநானூறு 166"},
    {"verse": "உலகம் யாவையும் தாம் உளவாக்கலும்", "meaning": "எல்லா உலகங்களும் தன்னிலிருந்தே தோன்றின.", "translation": "All worlds spring into being from the one Self.", "ref": "திருமந்திரம் · திருமூலர்"},
    {"verse": "அகல்விசும்பு ஊர்தரும் தெய்வத்தன்மை", "meaning": "விரிந்த வானவெளியில் செல்வது தெய்வீகத்தன்மை.", "translation": "The divine nature traverses the vast heavens.", "ref": "புறநானூறு 6"},
]

# ══════════════════════════════════════════════════════════════════
# தரவு பெறும் செயல்பாடுகள் · DATA FETCHING FUNCTIONS
# ══════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600, show_spinner=False)
def get_nasa_apod() -> dict:
    try:
        r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}", timeout=12)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=30)
def get_iss_position() -> dict:
    try:
        r = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        r.raise_for_status()
        d = r.json()
        return {
            "அட்சரேகை": float(d["iss_position"]["latitude"]),
            "தீர்க்கரேகை": float(d["iss_position"]["longitude"]),
            "நேரம்": d["timestamp"],
        }
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=120)
def get_iss_crew() -> list:
    try:
        r = requests.get("http://api.open-notify.org/astros.json", timeout=10)
        r.raise_for_status()
        return [p["name"] for p in r.json()["people"] if p["craft"] == "ISS"]
    except Exception:
        return []

# ══════════════════════════════════════════════════════════════════
# வானியல் கணிதம் · ASTRONOMY MATH
# ══════════════════════════════════════════════════════════════════

def sun_ecliptic_longitude(d: date) -> float:
    a = (14 - d.month) // 12
    y = d.year + 4800 - a
    m = d.month + 12 * a - 3
    jdn = (d.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045)
    n   = jdn - 2451545.0
    L   = (280.460 + 0.9856474 * n) % 360
    g   = math.radians((357.528 + 0.9856003 * n) % 360)
    lam = L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)
    return lam % 360

def get_rasi(lon: float) -> dict:
    return RASI_DATA[int(lon // 30) % 12]

def get_nakshatra(lon: float) -> tuple:
    idx = int((lon / 360) * 27) % 27
    return NAKSHATRAS[idx]

# ══════════════════════════════════════════════════════════════════
# PLOTLY விளக்கப்படங்கள் · CHART HELPERS
# ══════════════════════════════════════════════════════════════════

_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans Tamil, Share Tech Mono, sans-serif", color="#8898b8"),
    margin=dict(l=20, r=20, t=44, b=20),
)

def make_iss_globe(lat: float, lon: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=[lat], lon=[lon],
        mode="markers+text",
        marker=dict(size=18, color="#ff2d78", line=dict(color="#ff90b0", width=2)),
        text=["🛸 சர்வதேச விண்வெளி நிலையம்"],
        textposition="top center",
        textfont=dict(color="#ff2d78", size=11, family="Noto Sans Tamil, sans-serif"),
        name="சர்வதேச விண்வெளி நிலையம்",
    ))
    fig.update_layout(
        **_BASE,
        geo=dict(
            showland=True,   landcolor="rgba(18,28,58,0.95)",
            showocean=True,  oceancolor="rgba(0,8,28,0.95)",
            showcoastlines=True, coastlinecolor="rgba(0,255,231,0.3)",
            showframe=False, bgcolor="rgba(0,0,0,0)",
            projection_type="orthographic",
            projection_rotation=dict(lon=lon, lat=lat, roll=0),
            showlakes=True,  lakecolor="rgba(0,20,50,0.8)",
            showrivers=False,
            showcountries=True, countrycolor="rgba(0,255,231,0.08)",
        ),
        height=500,
        title=dict(text="சர்வதேச விண்வெளி நிலையம் · நேரடி கண்காணிப்பு", font=dict(family="Noto Sans Tamil", color="#00ffe7", size=13), x=0.5),
    )
    return fig

def make_rasi_wheel(sun_lon: float) -> go.Figure:
    fig = go.Figure()
    n = 12
    for i, rasi in enumerate(RASI_DATA):
        theta = math.radians(i * (360 / n) + 15)
        r = 0.88
        x, y = r * math.cos(theta), r * math.sin(theta)
        active  = (i == int(sun_lon // 30) % 12)
        t_color = "#ffd700" if active else "#5a7090"
        bg      = "rgba(255,215,0,0.14)" if active else "rgba(0,0,0,0)"
        bw      = 1 if active else 0

        fig.add_annotation(
            x=x, y=y,
            text=(f"<b>{rasi['symbol']}</b><br><span style='font-size:10px'>{rasi['rasi']}</span><br><span style='font-size:8px;color:#445060'>{rasi['roman']}</span>"),
            showarrow=False,
            font=dict(size=14, color=t_color, family="Noto Sans Tamil, sans-serif"),
            bgcolor=bg, bordercolor="#ffd700" if active else "rgba(0,0,0,0)", borderwidth=bw, borderpad=5, align="center",
        )

    for deg in range(0, 360, 30):
        t = math.radians(deg)
        x1, y1 = 1.06 * math.cos(t), 1.06 * math.sin(t)
        x2, y2 = 1.12 * math.cos(t), 1.12 * math.sin(t)
        fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2, line=dict(color="rgba(0,255,231,0.2)", width=1))

    angles_rad = [math.radians(a) for a in range(361)]
    fig.add_trace(go.Scatter(x=[1.13 * math.cos(a) for a in angles_rad], y=[1.13 * math.sin(a) for a in angles_rad], mode="lines", line=dict(color="rgba(0,255,231,0.18)", width=1), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[0.62 * math.cos(a) for a in angles_rad], y=[0.62 * math.sin(a) for a in angles_rad], mode="lines", line=dict(color="rgba(0,255,231,0.08)", width=1), hoverinfo="skip", showlegend=False))

    sx = 0.50 * math.cos(math.radians(sun_lon))
    sy = 0.50 * math.sin(math.radians(sun_lon))
    fig.add_trace(go.Scatter(x=[sx], y=[sy], mode="markers", marker=dict(size=26, color="#ffd700", symbol="circle", line=dict(color="#ff8800", width=2)), name="சூரியன்", hovertemplate=f"சூரியன்<br>{sun_lon:.2f}°<extra></extra>"))
    fig.add_annotation(x=sx, y=sy - 0.11, text="☀️ சூரியன்", showarrow=False, font=dict(size=10, color="#ffd700", family="Noto Sans Tamil, sans-serif"))

    fig.update_layout(**_BASE, xaxis=dict(range=[-1.4, 1.4], visible=False, scaleanchor="y"), yaxis=dict(range=[-1.4, 1.4], visible=False), height=480, showlegend=False, title=dict(text="ராசி சக்கரம் · சூரிய நிலை", font=dict(family="Noto Sans Tamil", color="#ffd700", size=14), x=0.5))
    return fig

def make_planet_orbit_chart(pandyan: bool) -> go.Figure:
    planets = list(PLANET_NAMES.keys())
    periods = [1, 0.08, 0.24, 0.62, 1.88, 11.86, 29.46, 84.01, 164.8]
    colours = ["#ffd700", "#c0c0c0", "#8888ff", "#00ccff", "#ff4444", "#ffaa44", "#aaaaff", "#44ffcc", "#4488ff"]
    labels = [PLANET_NAMES[p]["tamil"] if pandyan else p for p in planets]

    fig = go.Figure(go.Bar(
        x=labels, y=periods, marker=dict(color=colours, line=dict(color="rgba(255,255,255,0.08)", width=1)),
        text=[f"{p:.2f} ஆண்டு" if pandyan else f"{p:.2f} yr" for p in periods], textposition="outside", textfont=dict(size=9, color="#8090a8", family="Noto Sans Tamil"),
    ))
    fig.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(showgrid=False, zeroline=False, visible=True), yaxis=dict(title=dict(text="சுற்று காலம் (பூமி ஆண்டுகள்)" if pandyan else "Orbital Period (Earth Years)", font=dict(size=11)), gridcolor="rgba(0,255,231,0.06)"), height=500, dragmode='pan')
    return fig

# ══════════════════════════════════════════════════════════════════
# பக்கப்பட்டை · SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style='text-align:center;padding:1.2rem 0 0.6rem'>
    <div style='font-family:Orbitron,sans-serif;font-size:1.4rem; color:#00ffe7;text-shadow:0 0 22px #00ffe7;letter-spacing:0.1em'>
        கோச்சடையான்
    </div>
    <div style='font-family:Orbitron,sans-serif;font-size:0.55rem; color:#ff2d78;letter-spacing:0.28em;margin-top:5px'>
        KOCHADAIIYAAN
    </div>
    <div class='ta-sm' style='margin-top:7px;color:#304050 !important'>
        சைபர்பங்க் தமிழ் வானியல் தளம்
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

    st.markdown("<div class='ta' style='font-size:0.9rem;margin-bottom:6px'>⚙️ அமைப்புகள்</div>", unsafe_allow_html=True)

    pandyan_toggle = st.toggle("🔱 பாண்டியன் முறை", value=True, help="தமிழ் வானியல் பெயர்களை இயக்கு / நிறுத்து")

    mode_label = "தமிழ் பெயர்கள் இயக்கத்தில்" if pandyan_toggle else "ஆங்கில பெயர்கள் இயக்கத்தில்"
    badge_cls  = "badge" if pandyan_toggle else "badge badge-pink"
    
    st.markdown(f"""
<div class='gc' style='padding:0.7rem 1rem;margin-top:0.5rem'>
    <span class='{badge_cls}'>{'பாண்டியன்' if pandyan_toggle else 'MODERN'}</span>
    <div class='ta-sm' style='margin-top:6px'>{mode_label}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr><div class='ta' style='font-size:0.9rem;margin-bottom:8px'>🪐 கிரக பெயர்கள்</div>", unsafe_allow_html=True)

    for planet, data in PLANET_NAMES.items():
        disp = data["tamil"] if pandyan_toggle else planet
        sub  = planet if pandyan_toggle else data["roman"]
        st.markdown(f"""
<div style='display:flex;justify-content:space-between; padding:4px 0;border-bottom:1px solid rgba(0,255,231,0.06)'>
    <span class='ta' style='font-size:0.88rem !important'>{disp}</span>
    <span style='font-family:Share Tech Mono;color:#304050;font-size:0.72rem'>{sub}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<hr><div style='text-align:center;font-size:0.6rem;color:#202838; font-family:Share Tech Mono'>NASA DEMO_KEY · api.nasa.gov இல் மாற்றவும்</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# தலைப்பு · MAIN HEADER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;padding:1rem 0 0.2rem'>
    <h1 style='font-size:2.6rem;margin:0;letter-spacing:0.05em'>கோச்சடையான்</h1>
    <div class='ta' style='color:#ff2d78 !important;font-size:0.78rem; letter-spacing:0.12em;margin-top:4px'>
        சைபர்பங்க் தமிழ் வானியல் தளம் · CYBERPUNK TAMIL ASTRONOMY PORTAL
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# தாவல்கள் · TABS
# ══════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌌 இன்றைய வான்படம்",
    "📡 நேரடி கண்காணிப்பு",
    "♈ ராசி சக்கரம்",
    "🧠 அடிப்படை + தமிழர் அறிவு",
    "🏛️ தமிழர் வரலாறு"
])

def timeline_item(year, title, content):
    st.markdown(f"""
<div style='border-left:2px solid #00ffe7; padding:10px 20px;margin:20px 0; position:relative'>
    <div style='position:absolute;left:-7px;top:10px; width:12px;height:12px; background:#00ffe7;border-radius:50%; box-shadow:0 0 10px #00ffe7'></div>
    <div style='color:#00ffe7;font-size:0.8rem'>{year}</div>
    <div style='font-size:1.1rem;color:#ffd700'>{title}</div>
    <div style='color:#c0d0f0;font-size:0.9rem;margin-top:5px'>{content}</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# தாவல் 1 · இன்றைய வான்படம் (NASA APOD)
# ──────────────────────────────────────────────────────────────────
with tab1:
    data = get_nasa_apod_cached()

    if "error" in data:
        st.error("NASA API error: " + data["error"])
    else:
        title = data.get("title", "No Title")
        date_val = data.get("date", "")
        explanation = data.get("explanation", "")
        image_url = data.get("url", "")
        credit = data.get("copyright", "NASA")
        tamil_title = translate_apod_title(title)

        st.markdown(f"### 🌌 {title}")
        st.caption(f"📅 {date_val}")

        if tamil_title:
            st.markdown(f"🟢 **{tamil_title}**")
        st.caption(f"© {credit}")
        st.divider()

        media_type = data.get("media_type", "image")
        if media_type == "image":
            st.image(image_url, use_container_width=True)
        elif media_type == "video":
            st.video(image_url)

        st.divider()

        if explanation:
            tamil_explanation = translate_cached(explanation)

        st.markdown("### 📖 Explanation")
        st.write(explanation)

        st.markdown("### 📖 விளக்கம் (Tamil)")
        st.write(tamil_explanation)

        audio_file = tamil_voice(tamil_explanation)
        if audio_file:
            st.audio(audio_file)

# ──────────────────────────────────────────────────────────────────
# தாவல் 2 · சர்வதேச விண்வெளி நிலையம் (ISS Live Tracker)
# ──────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🛸 சர்வதேச விண்வெளி நிலையம்")
    st.markdown("<div class='ta-sm'>நேரடி விண்வெளி நிலைய கண்காணிப்பு · International Space Station Live Tracker</div>", unsafe_allow_html=True)
    st.write("")

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        if st.button("🔄 நிலையை புதுப்பி"):
            st.cache_data.clear()

    with st.spinner("விண்வெளி நிலைய தரவு பெறுகிறது…"):
        iss  = get_iss_position()
        crew = get_iss_crew()

    if "error" in iss:
        st.markdown(f"""
<div class='gc gc-pink'>
    <span class='badge badge-pink'>சமிக்ஞை இழந்தது</span>
    <p class='ta' style='color:#ff6090;margin-top:0.8rem'>Open-Notify API பிழை: {iss['error']}</p>
</div>
""", unsafe_allow_html=True)
    else:
        lat = iss["அட்சரேகை"]
        lon = iss["தீர்க்கரேகை"]
        ts  = datetime.utcfromtimestamp(iss["நேரம்"]).strftime("%Y-%m-%d %H:%M:%S UTC")

        m1, m2, m3, m4 = st.columns(4)
        iss_metrics = [("அட்சரேகை", f"{lat:.3f}°"), ("தீர்க்கரேகை", f"{lon:.3f}°"), ("உயரம்", "~408 கி.மீ"), ("வேகம்", "27,600 கி.மீ/மணி")]
        for col, (lbl, val) in zip([m1, m2, m3, m4], iss_metrics):
            with col:
                st.markdown(f"""
<div class='mbox'>
    <div class='mval'>{val}</div>
    <div class='mlbl'>{lbl}</div>
</div>
""", unsafe_allow_html=True)

        st.write("")
        col_globe, col_crew = st.columns([1.65, 1], gap="large")

        with col_globe:
            st.markdown("<div class='gc' style='padding:0.8rem'>", unsafe_allow_html=True)
            st.plotly_chart(make_iss_globe(lat, lon), use_container_width=True)
            st.markdown(f"<div class='ta-sm' style='text-align:center;margin-top:-10px'>கடைசி புதுப்பிப்பு: {ts}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_crew:
            st.markdown("""
<div class='gc'>
    <span class='badge'>விண்வெளி வீரர்கள்</span>
    <div class='ta-sm' style='margin-top:6px;margin-bottom:12px'>தற்போது நிலையத்தில் உள்ளவர்கள்</div>
""", unsafe_allow_html=True)

            if crew:
                for i, name in enumerate(crew):
                    if name in RETURNED_ASTRONAUTS:
                        tag_html = f"<span class='crew-earth'>{RETURNED_ASTRONAUTS[name]}</span>"
                    else:
                        tag_html = "<span class='crew-tag'>விண்வெளியில்</span>"

                    st.markdown(f"""
<div class='crew-row'>
    <span class='crew-num'>#{i+1:02d}</span>
    <span class='crew-name'>{name}</span>
    {tag_html}
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ta-sm'>தரவு கிடைக்கவில்லை.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
<div class='gc gc-gold'>
    <span class='badge badge-gold'>விண்வெளி நிலைய தகவல்கள்</span>
    <table style='width:100%;margin-top:0.9rem; border-collapse:collapse;font-size:0.78rem'>
        <tr><td class='ta-sm' style='padding:4px 0'>ஒரு நாளில் சுற்றுகள்</td><td style='color:#00ffe7;text-align:right'>15.5</td></tr>
        <tr><td class='ta-sm' style='padding:4px 0'>சுற்று காலம்</td><td style='color:#00ffe7;text-align:right'>~92 நிமிடம்</td></tr>
        <tr><td class='ta-sm' style='padding:4px 0'>தொடங்கப்பட்ட ஆண்டு</td><td style='color:#00ffe7;text-align:right'>1998</td></tr>
        <tr><td class='ta-sm' style='padding:4px 0'>எடை</td><td style='color:#00ffe7;text-align:right'>4,20,000 கி.கி</td></tr>
        <tr><td class='ta-sm' style='padding:4px 0'>நீளம்</td><td style='color:#00ffe7;text-align:right'>109 மீட்டர்</td></tr>
        <tr><td class='ta-sm' style='padding:4px 0'>சௌர பலகைகள்</td><td style='color:#00ffe7;text-align:right'>8 வரிசைகள்</td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# தாவல் 3 · ராசி சக்கர கணிப்பான் (Zodiac Degree Engine)
# ──────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("## ♈ ராசி சக்கர கணிப்பான்")
    st.markdown("<div class='ta-sm'>சூரியனின் ராசி நிலையை கண்டறி · வேத வானியல் கணிதம்</div>", unsafe_allow_html=True)
    st.write("")

    col_inp, col_res = st.columns([1, 1.7], gap="large")

    with col_inp:
        st.markdown("""
<div class='gc'>
    <span class='badge'>உள்ளீடு</span>
    <div class='ta' style='margin-top:0.6rem;font-size:0.92rem'>தேதி தேர்ந்தெடுக்கவும்</div>
""", unsafe_allow_html=True)

        selected_date = st.date_input("தேதி", value=date.today(), min_value=date(1900, 1, 1), max_value=date(2100, 12, 31), label_visibility="collapsed")
        st.write("")
        st.button("⚡ ராசி கணிக்க", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class='gc' style='font-size:0.78rem'>
    <span class='badge badge-violet'>கணிப்பு முறை</span>
    <p class='ta-sm' style='margin-top:0.8rem;line-height:1.75'>
        Jean Meeus கெப்லர் சூத்திரம்:<br>
        λ = L₀ + 1.915·sin(g) + 0.020·sin(2g)<br><br>
        L₀ = சராசரி தீர்க்கரேகை<br>
        g = சராசரி கோண இயக்கம்<br>
        துல்லியம் ≈ ±1°
    </p>
</div>
""", unsafe_allow_html=True)

    with col_res:
        sun_lon     = sun_ecliptic_longitude(selected_date)
        rasi        = get_rasi(sun_lon)
        nak_ta, nak_en = get_nakshatra(sun_lon)
        deg_in_rasi = sun_lon % 30
        verse       = PURANANURU_VERSES[int(sun_lon // 30) % 12]

        st.markdown(f"""
<div class='gc gc-gold'>
    <span class='badge badge-gold'>முடிவு</span>
    <div style='display:flex;gap:1rem;margin:1rem 0;flex-wrap:wrap;align-items:stretch'>
        <div class='mbox' style='flex:0.6;min-width:80px'>
            <div style='font-size:2.4rem'>{rasi['symbol']}</div>
            <div class='mlbl'>சின்னம்</div>
        </div>
        <div class='mbox' style='flex:1.4;min-width:140px'>
            <div class='ta-lg'>{rasi['rasi']}</div>
            <div class='mlbl'>{rasi['roman']} · {rasi['modern']}</div>
        </div>
        <div class='mbox' style='flex:1;min-width:110px'>
            <div class='mval'>{sun_lon:.2f}°</div>
            <div class='mlbl'>கிரகண நிலை</div>
        </div>
    </div>
    <div style='display:flex;gap:0.8rem;flex-wrap:wrap'>
        <div class='mbox'>
            <div class='mval' style='font-size:1.1rem'>{deg_in_rasi:.1f}°</div>
            <div class='mlbl'>ராசியில் படி</div>
        </div>
        <div class='mbox'>
            <div class='ta' style='color:#00ffe7'>{nak_ta}</div>
            <div class='mlbl'>நட்சத்திரம் · {nak_en}</div>
        </div>
        <div class='mbox'>
            <div class='ta' style='color:#ff2d78'>{rasi['lord']}</div>
            <div class='mlbl'>ராசி அதிபதி</div>
        </div>
        <div class='mbox'>
            <div class='ta' style='color:#c77dff'>{rasi['element']}</div>
            <div class='mlbl'>தத்துவம்</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class='gc'>
    <span class='badge badge-gold'>புறநானூறு · வெண்பா</span>
    <div class='verse' style='margin-top:0.8rem'>
        <div class='ta-lg'>"{verse['verse']}"</div>
        <div class='ta' style='color:#7888a8 !important; font-size:0.88rem;margin-top:6px'>{verse['meaning']}</div>
        <div style='color:#a0b0c0;font-size:0.8rem; margin-top:4px;font-style:italic'>"{verse['translation']}"</div>
        <div class='ta-sm' style='margin-top:6px'>{verse['ref']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    st.plotly_chart(make_rasi_wheel(sun_lon), use_container_width=True)

    st.markdown("### 🗂 ராசி முழு அட்டவணை")
    tbl = """
<div class='gc' style='overflow-x:auto'>
<table style='width:100%;border-collapse:collapse;font-size:0.82rem'>
    <thead>
        <tr style='border-bottom:1px solid rgba(0,255,231,0.2)'>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>எண்</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>ராசி</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>ஆங்கிலம்</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>சின்னம்</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>அதிபதி</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>தத்துவம்</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>ஆரம்பம்°</th>
            <th style='padding:9px 8px;color:#00ffe7;font-family:Noto Sans Tamil;text-align:left'>முடிவு°</th>
        </tr>
    </thead>
    <tbody>
"""
    for i, r in enumerate(RASI_DATA):
        hi = "background:rgba(255,215,0,0.07);" if int(sun_lon // 30) == i else ""
        tbl += (
            f"<tr style='border-bottom:1px solid rgba(255,255,255,0.04);{hi}'>"
            f"<td style='padding:7px 8px;color:#304050'>{i+1:02d}</td>"
            f"<td style='padding:7px 8px;font-family:Noto Sans Tamil;color:#ffe0a0'>{r['rasi']}</td>"
            f"<td style='padding:7px 8px;color:#8090a8'>{r['modern']}</td>"
            f"<td style='padding:7px 8px;font-size:1.15rem'>{r['symbol']}</td>"
            f"<td style='padding:7px 8px;font-family:Noto Sans Tamil;color:#ff2d78'>{r['lord']}</td>"
            f"<td style='padding:7px 8px;font-family:Noto Sans Tamil;color:#c77dff'>{r['element']}</td>"
            f"<td style='padding:7px 8px;color:#5a6a84'>{r['start']}°</td>"
            f"<td style='padding:7px 8px;color:#5a6a84'>{(r['start']+30)%360}°</td>"
            f"</tr>"
        )
    tbl += "</tbody></table></div>"
    st.markdown(tbl, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# தாவல் 4 · கிரக அட்லஸ் & அடிப்படை வானியல்
# ──────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────
# தாவல் 4 · கிரக அட்லஸ் & அடிப்படை வானியல் & வினாடி வினா
# ──────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("---")
    
    # ── BILINGUAL FACTS & NEWS ─────────────────────────────
    if is_ta:
        st.success("🚀 அறிவு + பாரம்பரியம் = சக்தி")   
        st.markdown("### 🔥 சுவாரஸ்யமான உண்மைகள்")
        facts = [
            "☀️ சூரிய குடும்பத்தின் நிறையில் 99.86% சூரியன் மட்டுமே!",
            "🪐 சனி கிரகம் தண்ணீரில் மிதக்கக்கூடிய அளவுக்கு அடர்த்தி குறைவானது",
            "🌍 பூமி மட்டுமே உயிர்களை ஆதரிக்கும் ஒரே கிரகம்",
            "🌙 சந்திரன் ஒவ்வொரு ஆண்டும் பூமியை விட்டு 3.8 செ.மீ விலகிச் செல்கிறது",
            "🔥 சுக்கிரன் (வெள்ளி) சூரிய குடும்பத்தின் மிக வெப்பமான கிரகம்"
        ]
        
        st.markdown("### 📰 விண்வெளி செய்திகள்")
        news = [
            "🚀 நாசாவின் புதிய செவ்வாய் கிரக பயணம் விரைவில் தொடக்கம்",
            "🌕 சந்திரனின் தென் துருவத்தில் புதிய கண்டுபிடிப்புகள்",
            "🛰️ சர்வதேச விண்வெளி நிலையத்தின் (ISS) மேம்பாடுகள் நிறைவு"
        ]
    else:
        st.success("🚀 Knowledge + Heritage = Power")   
        st.markdown("### 🔥 Interesting Facts")
        facts = [
            "☀️ Sun = 99.86% of solar system mass",
            "🪐 Saturn is so light it could float in water",
            "🌍 Earth is the only known planet to support life",
            "🌙 The Moon is moving away from Earth at 3.8 cm per year",
            "🔥 Venus is the hottest planet in our solar system"
        ]
        
        st.markdown("### 📰 Space News")
        news = [
            "🚀 NASA Mars mission launching soon",
            "🌕 New discoveries at the lunar south pole",
            "🛰️ ISS hardware upgrades successfully completed"
        ]

    # Render the styled cards
    for f in facts:
        st.markdown(f"<div class='gc'>{f}</div>", unsafe_allow_html=True)
    
    for n in news:
        st.markdown(f"<div class='gc gc-pink'>{n}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# தாவல் 5 · தமிழர் வானியல் வரலாறு (Ancient Tamil Astronomy)
# ──────────────────────────────────────────────────────────────────

    st.divider()
    st.header("🧪 வினாடி வினா (Quiz)")

    # ══════════════════════════════════════════════════════════════════
    # 10 TAMIL ASTRONOMY QUESTIONS (QUIZ LOGIC)
    # ══════════════════════════════════════════════════════════════════
    _QUIZ_CSS = """
    <style>
    .quiz-shell { max-width: 780px; margin: 0 auto; padding: 0 1rem; }
    .qpbar-track { height: 6px; background: rgba(0,255,231,0.1); border-radius: 6px; overflow: hidden; margin-bottom: 6px; }
    .qpbar-fill { height: 100%; border-radius: 6px; background: linear-gradient(90deg, #00ffe7, #c77dff); transition: width 0.4s cubic-bezier(.4,0,.2,1); box-shadow: 0 0 10px rgba(0,255,231,0.5); }
    .qpbar-meta { display: flex; justify-content: space-between; font-size: 0.72rem; color: #5a6a84; font-family: 'Noto Sans Tamil', sans-serif; margin-bottom: 1.2rem; }
    .qcard { background: rgba(6,6,24,0.82); border: 1px solid rgba(0,255,231,0.2); border-radius: 20px; padding: 2rem 2.2rem 1.4rem; position: relative; overflow: hidden; margin-bottom: 1.4rem; box-shadow: 0 0 60px rgba(0,255,231,0.04); }
    .qcard::before { content: ''; position: absolute; top: 0; left: 8%; right: 8%; height: 1px; background: linear-gradient(90deg,transparent,#00ffe7,transparent); opacity: 0.45; }
    .qnum { font-family: 'Orbitron', monospace; font-size: 0.7rem; color: #00ffe7; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 0.5rem; }
    .qbadges { display: flex; gap: 8px; margin-bottom: 1rem; }
    .qbadge { display: inline-block; padding: 2px 11px; border-radius: 20px; font-family: 'Noto Sans Tamil', sans-serif; font-size: 0.68rem; border: 1px solid rgba(0,255,231,0.3); color: rgba(0,255,231,0.8); }
    .qbadge.diff-easy   { border-color: rgba(0,255,80,0.4);  color: #00ff88; }
    .qbadge.diff-medium { border-color: rgba(255,215,0,0.4); color: #ffd700; }
    .qbadge.diff-hard   { border-color: rgba(255,45,120,0.4);color: #ff2d78; }
    .qtext { font-family: 'Noto Sans Tamil', sans-serif; font-size: 1.15rem; font-weight: 600; line-height: 2.0; color: #dce8ff; }
    .opt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 1.2rem 0 0.4rem; }
    .opt-btn { display: flex; align-items: center; gap: 10px; padding: 0.8rem 1rem; background: rgba(0,255,231,0.04); border: 1px solid rgba(0,255,231,0.18); border-radius: 12px; cursor: pointer; transition: all 0.2s; min-height: 52px; text-align: left; width: 100%; font-family: 'Noto Sans Tamil', sans-serif; }
    .opt-btn:hover:not(:disabled) { background: rgba(0,255,231,0.10); border-color: rgba(0,255,231,0.45); transform: translateY(-2px); }
    .opt-label { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; border: 1px solid rgba(0,255,231,0.35); font-family: 'Orbitron', monospace; font-size: 0.72rem; color: #00ffe7; flex-shrink: 0; }
    .opt-text { font-size: 0.92rem; line-height: 1.65; color: #b0c8e8; }
    .opt-btn.selected { border-color: rgba(0,180,255,0.7); background: rgba(0,180,255,0.12); }
    .opt-btn.correct { border-color: rgba(0,255,120,0.75) !important; background: rgba(0,255,120,0.10) !important; box-shadow: 0 0 15px rgba(0,255,120,0.2); }
    .opt-btn.wrong { border-color: rgba(255,45,120,0.75) !important; background: rgba(255,45,120,0.10) !important; }
    .opt-label.correct { background: #00ff88; color: #001820; border-color: #00ff88; }
    .opt-label.wrong   { background: #ff2d78; color: white;   border-color: #ff2d78; }
    .feedback-banner { padding: 0.85rem 1.1rem; border-radius: 12px; font-family: 'Noto Sans Tamil', sans-serif; font-size: 0.9rem; line-height: 1.75; margin-bottom: 0.8rem; border-left: 4px solid; }
    .feedback-banner.correct { background: rgba(0,255,120,0.07); border-color: #00ff88; color: #a0ffcc; }
    .feedback-banner.wrong { background: rgba(255,45,120,0.07); border-color: #ff2d78; color: #ffaac0; }
    .explanation { background: rgba(199,125,255,0.05); border: 1px solid rgba(199,125,255,0.22); border-radius: 12px; padding: 1rem 1.2rem; font-family: 'Noto Sans Tamil', sans-serif; font-size: 0.88rem; line-height: 1.85; color: #c0b0e8; margin-top: 0.6rem; }
    .explanation-title { font-size: 0.7rem; letter-spacing: 0.12em; color: #c77dff; margin-bottom: 0.4rem; font-family: 'Orbitron', monospace; }
    .result-shell { max-width: 680px; margin: 0 auto; text-align: center; padding: 1rem; }
    .result-score-ring { display: inline-flex; align-items: center; justify-content: center; width: 140px; height: 140px; border-radius: 50%; border: 3px solid #00ffe7; box-shadow: 0 0 40px rgba(0,255,231,0.3), inset 0 0 30px rgba(0,255,231,0.06); font-family: 'Orbitron', monospace; font-size: 2.6rem; color: #00ffe7; text-shadow: 0 0 18px #00ffe7; margin: 1rem auto; }
    .result-grade { font-family: 'Noto Sans Tamil', sans-serif; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; }
    .result-stars { font-size: 1.8rem; letter-spacing: 4px; margin: 0.4rem 0 1.2rem; }
    .result-breakdown { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin: 1rem 0; }
    .result-q-dot { height: 8px; border-radius: 4px; }
    .result-q-dot.correct { background: #00ff88; box-shadow: 0 0 6px rgba(0,255,136,0.6); }
    .result-q-dot.wrong   { background: #ff2d78; box-shadow: 0 0 6px rgba(255,45,120,0.5); }
    .result-q-dot.skip    { background: #3a4a5a; }
    .quiz-splash { text-align: center; padding: 2.5rem 1rem 1.5rem; }
    .quiz-splash-icon { font-size: 3.5rem; margin-bottom: 0.5rem; }
    .quiz-splash-title { font-family: 'Noto Sans Tamil', sans-serif; font-size: 1.6rem; font-weight: 700; color: #ffd700; text-shadow: 0 0 20px rgba(255,215,0,0.5); margin-bottom: 0.4rem; }
    .quiz-splash-sub { font-family: 'Noto Sans Tamil', sans-serif; font-size: 0.9rem; color: #5a6a84; line-height: 1.85; margin-bottom: 1.5rem; }
    .quiz-rules { background: rgba(6,6,24,0.8); border: 1px solid rgba(0,255,231,0.15); border-radius: 16px; padding: 1.2rem 1.5rem; text-align: left; font-family: 'Noto Sans Tamil', sans-serif; font-size: 0.88rem; color: #8898b8; line-height: 2.0; margin-bottom: 1.4rem; max-width: 500px; margin-left: auto; margin-right: auto; }
    </style>
    """

    QUIZ_QUESTIONS = [
        {
            "id": 1, "category": "சூரிய குடும்பம்", "difficulty": "எளிது",
            "question": "சூரிய குடும்பத்தில் மொத்தம் எத்தனை கிரகங்கள் உள்ளன?",
            "options": ["6 கிரகங்கள்", "7 கிரகங்கள்", "8 கிரகங்கள்", "9 கிரகங்கள்"],
            "correct_index": 2,
            "explanation": "2006 ஆம் ஆண்டு IAU முடிவின்படி, சூரிய குடும்பத்தில் 8 கிரகங்கள் உள்ளன. புளூட்டோ இப்போது 'குள்ள கோள்' என வகைப்படுத்தப்பட்டது. 8 கிரகங்கள்: புதன், சுக்கிரன், பூமி, செவ்வாய், குரு, சனி, யுரேனஸ், நெப்டியூன்.",
        },
        {
            "id": 2, "category": "நட்சத்திரம்", "difficulty": "எளிது",
            "question": "பூமியிலிருந்து மிக அருகில் உள்ள நட்சத்திரம் எது?",
            "options": ["சீரியஸ்", "பெட்டல்ஜூஸ்", "ப்ராக்ஸிமா சென்டாரி", "வேகா"],
            "correct_index": 2,
            "explanation": "ப்ராக்ஸிமா சென்டாரி பூமியிலிருந்து சுமார் 4.24 ஒளி ஆண்டுகள் தொலைவில் உள்ளது. இது ஆல்ஃபா சென்டாரி மண்டலத்தின் ஒரு பகுதி. நமது சூரியனுக்கு அடுத்த மிக நெருங்கிய நட்சத்திரம் இது தான்.",
        },
        {
            "id": 3, "category": "விண்வெளி நிலையம்", "difficulty": "நடுத்தரம்",
            "question": "சர்வதேச விண்வெளி நிலையம் (ISS) ஒரு நாளில் பூமியை எத்தனை முறை சுற்றுகிறது?",
            "options": ["சுமார் 8 முறை", "சுமார் 12 முறை", "சுமார் 15–16 முறை", "சுமார் 24 முறை"],
            "correct_index": 2,
            "explanation": "ISS மணிக்கு சுமார் 27,600 கி.மீ வேகத்தில் பயணிக்கிறது. ஒவ்வொரு சுற்றும் 92 நிமிடம் ஆகும். எனவே ஒரு நாளில் (24 மணி நேரம்) சுமார் 15–16 முறை பூமியை சுற்றுகிறது.",
        },
        {
            "id": 4, "category": "சூரியன்", "difficulty": "எளிது",
            "question": "சூரியனின் மேற்பரப்பு வெப்பநிலை தோராயமாக எவ்வளவு?",
            "options": ["1,000 கெல்வின்", "3,500 கெல்வின்", "5,500 கெல்வின்", "1,00,000 கெல்வின்"],
            "correct_index": 2,
            "explanation": "சூரியனின் ஒளிமண்டலம் (Photosphere) சுமார் 5,500°C / 5,778 கெல்வின் வெப்பநிலை கொண்டது. சுவாரஸ்யம்: சூரியனின் வெளி வளிமண்டலம் (Corona) இதை விட 200 மடங்கு அதிக வெப்பமாக இருக்கும்!",
        },
        {
            "id": 5, "category": "சந்திரன்", "difficulty": "நடுத்தரம்",
            "question": "சந்திரன் பூமியை ஒரு முறை சுற்ற எத்தனை நாட்கள் ஆகும்?",
            "options": ["14 நாட்கள்", "27.3 நாட்கள்", "30 நாட்கள்", "365 நாட்கள்"],
            "correct_index": 1,
            "explanation": "சந்திரன் பூமியை சுமார் 27.3 நாட்களில் சுற்றுகிறது (நட்சத்திர மாதம்). நாம் காணும் அமாவாசை-பௌர்ணமி சுழற்சி 29.5 நாட்கள் — ஏனென்றால் பூமியும் சூரியனை சுற்றுகிறது.",
        },
        {
            "id": 6, "category": "கிரகங்கள்", "difficulty": "நடுத்தரம்",
            "question": "சூரிய குடும்பத்தில் மிகப் பெரிய கிரகம் எது?",
            "options": ["சனி", "யுரேனஸ்", "குரு (வியாழன்)", "நெப்டியூன்"],
            "correct_index": 2,
            "explanation": "குரு (வியாழன் / Jupiter) சூரிய குடும்பத்தின் மிகப் பெரிய கிரகம். இது பூமியை விட சுமார் 1,321 மடங்கு பெரியது. இதன் புகழ்பெற்ற 'சிவப்பு புள்ளி' (Great Red Spot) ஒரு நூற்றாண்டுகளாக நீடிக்கும் மிகப்பெரிய புயல்!",
        },
        {
            "id": 7, "category": "தமிழர் வானியல்", "difficulty": "கடினம்",
            "question": "தமிழர் வானியல் மரபில் எத்தனை நட்சத்திர மண்டலங்கள் (Nakshatras) கண்டறியப்பட்டன?",
            "options": ["12", "18", "27", "36"],
            "correct_index": 2,
            "explanation": "தமிழர்கள் உட்பட இந்திய வானியல் மரபில் 27 நட்சத்திர மண்டலங்கள் கண்டறியப்பட்டன. சந்திரன் ஒவ்வொரு நாளும் ஒரு நட்சத்திர மண்டலத்தில் நிலைகொள்வதாக கணிக்கப்பட்டது. இது காலக் கணக்கீட்டிற்கு பயன்படுத்தப்பட்டது.",
        },
        {
            "id": 8, "category": "கரும் துளை", "difficulty": "கடினம்",
            "question": "கரும் துளையின் (Black Hole) 'நிகழ்வு எல்லை' (Event Horizon) என்றால் என்ன?",
            "options": [
                "கரும் துளை உருவாகும் தொடக்கப் புள்ளி",
                "ஒளி கூட திரும்ப முடியாத எல்லை",
                "கரும் துளையின் மையம்",
                "கரும் துளையின் வெளிப்புற வளிமண்டலம்",
            ],
            "correct_index": 1,
            "explanation": "நிகழ்வு எல்லை (Event Horizon) என்பது கரும் துளையின் சுற்றளவு எல்லை. இந்த எல்லையை கடந்தால் ஒளி கூட திரும்ப முடியாது — ஏனென்றால் அங்கே புவியீர்ப்பு விசை மிகவும் அதிகமாக இருக்கும். வெளிச்சம் இல்லாமல் நாம் பார்க்கவே முடியாது!",
        },
        {
            "id": 9, "category": "நாசா", "difficulty": "நடுத்தரம்",
            "question": "நாசா முதன்முதலில் மனிதனை சந்திரனில் இறக்கிய திட்டத்தின் பெயர் என்ன?",
            "options": ["கெமினி", "மெர்குரி", "அப்போலோ 11", "ஆர்டெமிஸ்"],
            "correct_index": 2,
            "explanation": "1969 ஆம் ஆண்டு ஜூலை 20 ஆம் தேதி அப்போலோ 11 திட்டத்தில் நீல் ஆம்ஸ்ட்ராங் மற்றும் பஸ் ஆல்ட்ரின் சந்திரனில் முதன்முதலில் கால் வைத்தனர். 'ஒரு மனிதனுக்கு சிறிய அடி, மனித குலத்திற்கு பிரம்மாண்டமான பாய்ச்சல்' என்று ஆம்ஸ்ட்ராங் கூறினார்.",
        },
        {
            "id": 10, "category": "பிரபஞ்சம்", "difficulty": "கடினம்",
            "question": "நம் பால்வழி (Milky Way) விண்மீன் திரளில் தோராயமாக எத்தனை நட்சத்திரங்கள் உள்ளன?",
            "options": [
                "சுமார் 10 கோடி நட்சத்திரங்கள்",
                "சுமார் 1,000 கோடி நட்சத்திரங்கள்",
                "சுமார் 1–4 லட்சம் கோடி நட்சத்திரங்கள்",
                "சுமார் 100 லட்சம் கோடி நட்சத்திரங்கள்",
            ],
            "correct_index": 2,
            "explanation": "நம் பால்வழி விண்மீன் திரளில் சுமார் 100–400 பில்லியன் (1–4 லட்சம் கோடி) நட்சத்திரங்கள் உள்ளதாக விஞ்ஞானிகள் மதிப்பிடுகின்றனர். இன்னும் ஆச்சரியம்: பிரபஞ்சத்தில் இதுபோல் 2 டிரில்லியன் விண்மீன் திரள்கள் உள்ளன!",
        },
    ]

    _GRADES = [
        (10, "🏆 வானியல் மேதை!",    "A+", "#ffd700", "நீங்கள் ஒரு உண்மையான விண்வெளி வல்லுநர்!"),
        (9,  "🥇 அசாதாரண திறமை",   "A+", "#ffd700", "மிகவும் சிறப்பான மதிப்பெண்!"),
        (8,  "🥈 சிறந்த செயல்திறன்","A",  "#00ffe7", "மிக நல்லது! கொஞ்சம் இன்னும் படிக்கலாம்."),
        (7,  "👍 நல்ல முயற்சி",      "B",  "#c77dff", "நல்ல ஆரம்பம். தொடர்ந்து படியுங்கள்!"),
        (6,  "📚 மேலும் படிக்கவும்", "B",  "#c77dff", "சரியான பாதையில் உள்ளீர்கள்."),
        (0,  "🔄 மீண்டும் முயற்சி",  "C",  "#ff2d78", "விடாமல் முயற்சியுங்கள்! நீங்கள் சிறப்பாக செய்வீர்கள்."),
    ]

    def _get_grade(score: int):
        for threshold, label, letter, colour, msg in _GRADES:
            if score >= threshold: return label, letter, colour, msg
        return _GRADES[-1][1], _GRADES[-1][2], _GRADES[-1][3], _GRADES[-1][4]

    def _diff_class(difficulty: str) -> str:
        return {"எளிது": "diff-easy", "நடுத்தரம்": "diff-medium", "கடினம்": "diff-hard"}.get(difficulty, "")

    _LABELS = ["அ", "ஆ", "இ", "ஈ"]

    def _init_state():
        defaults = {
            "quiz_started":   False,
            "quiz_index":     0,
            "quiz_answers":   [None] * len(QUIZ_QUESTIONS),
            "quiz_score":     0,
            "quiz_submitted": False,
            "quiz_complete":  False,
        }
        for k, v in defaults.items():
            if k not in st.session_state: st.session_state[k] = v

    def _reset():
        keys = ["quiz_started","quiz_index","quiz_answers","quiz_score","quiz_submitted","quiz_complete"]
        for k in keys:
            if k in st.session_state: del st.session_state[k]
        _init_state()

    def _render_splash():
        st.markdown("""
        <div class='quiz-splash'>
            <div class='quiz-splash-icon'>🧪</div>
            <div class='quiz-splash-title'>வானியல் வினாடி வினா</div>
            <div class='quiz-splash-sub'>
                தமிழில் வானியல் கேள்விகள் · 10 வினாக்கள்<br>
                உங்கள் விண்வெளி அறிவை சோதியுங்கள்!
            </div>
            <div class='quiz-rules'>
                📋 விதிகள்:<br>
                • மொத்தம் 10 கேள்விகள்<br>
                • ஒவ்வொரு கேள்விக்கும் 4 விருப்பங்கள்<br>
                • ஒரு முறை தேர்வு செய்தால் மாற்ற முடியாது<br>
                • சரியான விடை + விளக்கம் உடனே காட்டப்படும்<br>
                • இறுதியில் மதிப்பெண் + தரம் காட்டப்படும்
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_l, col_m, col_r = st.columns([1, 1.5, 1])
        with col_m:
            if st.button("🚀 வினாடி வினா தொடங்கு", use_container_width=True, key="quiz_start_btn"):
                st.session_state.quiz_started = True
                st.rerun()

    def _render_progress(idx: int, score: int):
        total = len(QUIZ_QUESTIONS)
        pct   = int((idx / total) * 100)
        st.markdown(f"""
        <div class='quiz-shell'>
            <div class='qpbar-track'>
                <div class='qpbar-fill' style='width:{pct}%'></div>
            </div>
            <div class='qpbar-meta'>
                <span>வினா {idx + 1} / {total}</span>
                <span>மதிப்பெண்: {score} / {min(idx, total)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_question(q: dict, idx: int):
        diff_cls = _diff_class(q["difficulty"])
        st.markdown(f"""
        <div class='quiz-shell'>
          <div class='qcard'>
            <div class='qnum'>வினா {q['id']} / {len(QUIZ_QUESTIONS)}</div>
            <div class='qbadges'>
              <span class='qbadge'>{q['category']}</span>
              <span class='qbadge {diff_cls}'>{q['difficulty']}</span>
            </div>
            <div class='qtext' lang='ta'>{q['question']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_options(q: dict, idx: int):
        submitted  = st.session_state.quiz_submitted
        user_ans   = st.session_state.quiz_answers[idx]
        correct_i  = q["correct_index"]
        options    = q["options"]

        col_a, col_b = st.columns(2)
        pairs = [(0, col_a), (1, col_b), (2, col_a), (3, col_b)]

        for opt_i, col in pairs:
            label    = _LABELS[opt_i]
            text     = options[opt_i]
            btn_key  = f"quiz_opt_{idx}_{opt_i}"

            if not submitted:
                extra_cls   = "selected" if user_ans == opt_i else ""
                label_cls   = ""; icon = ""
            else:
                if opt_i == correct_i:
                    extra_cls = "correct"; label_cls = "correct"; icon = " ✓"
                elif opt_i == user_ans and user_ans != correct_i:
                    extra_cls = "wrong";   label_cls = "wrong";   icon = " ✗"
                else:
                    extra_cls = ""; label_cls = ""; icon = ""

            with col:
                st.markdown(f"""
                <div class='opt-btn {extra_cls}' style='pointer-events:none'>
                    <span class='opt-label {label_cls}'>{label}</span>
                    <span class='opt-text' lang='ta'>{text}{icon}</span>
                </div>
                """, unsafe_allow_html=True)

                if not submitted:
                    if st.button(f"{label}. {text}", key=btn_key, use_container_width=True):
                        st.session_state.quiz_answers[idx] = opt_i
                        st.session_state.quiz_submitted = True
                        if opt_i == correct_i:
                            st.session_state.quiz_score += 1
                        st.rerun()

    def _render_feedback(q: dict, idx: int):
        if not st.session_state.quiz_submitted: return
        user_ans  = st.session_state.quiz_answers[idx]
        correct_i = q["correct_index"]
        if user_ans == correct_i:
            banner_cls = "correct"; banner_msg = "✅ சரியான விடை! மிகவும் சிறப்பு!"
        else:
            banner_cls = "wrong"; banner_msg  = f"❌ தவறான விடை. சரியான விடை: {q['options'][correct_i]}"

        st.markdown(f"""
        <div class='quiz-shell'>
            <div class='feedback-banner {banner_cls}' lang='ta'>
                {banner_msg}
            </div>
            <div class='explanation'>
                <div class='explanation-title'>💡 விளக்கம்</div>
                <span lang='ta'>{q['explanation']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_nav(idx: int):
        if not st.session_state.quiz_submitted: return
        st.write("")
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            if idx < len(QUIZ_QUESTIONS) - 1:
                if st.button("அடுத்த வினா →", use_container_width=True, key="quiz_next"):
                    st.session_state.quiz_index    += 1
                    st.session_state.quiz_submitted = False
                    st.rerun()
            else:
                if st.button("🏁 முடிவுகளை காண்க", use_container_width=True, key="quiz_finish"):
                    st.session_state.quiz_complete = True
                    st.rerun()
        with col_r:
            if st.button("↩ மீண்டும் தொடங்கு", use_container_width=True, key="quiz_reset_mid"):
                _reset()
                st.rerun()

    def _render_results():
        score   = st.session_state.quiz_score
        total   = len(QUIZ_QUESTIONS)
        answers = st.session_state.quiz_answers
        grade_label, grade_letter, grade_colour, grade_msg = _get_grade(score)
        pct     = int((score / total) * 100)

        st.markdown(f"""
        <div class='result-shell'>
            <div style='font-family:Noto Sans Tamil;font-size:1.1rem; color:#5a6a84;margin-bottom:0.5rem'>வினாடி வினா முடிந்தது!</div>
            <div class='result-score-ring' style='border-color:{grade_colour}; color:{grade_colour};text-shadow:0 0 18px {grade_colour}'>
                {score}/{total}
            </div>
            <div class='result-grade' style='color:{grade_colour}'>{grade_label}</div>
            <div style='font-family:Noto Sans Tamil;font-size:0.95rem; color:#8898b8;margin-bottom:1.2rem'>{grade_msg}</div>
            <div style='font-family:Orbitron,monospace;font-size:0.75rem; color:#5a6a84;letter-spacing:0.12em;margin-bottom:0.5rem'>
                தரம் {grade_letter} · {pct}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        dots = ""
        for i, ans in enumerate(answers):
            if ans is None: dots += "<div class='result-q-dot skip'></div>"
            elif ans == QUIZ_QUESTIONS[i]["correct_index"]: dots += "<div class='result-q-dot correct'></div>"
            else: dots += "<div class='result-q-dot wrong'></div>"

        st.markdown(f"""
        <div class='quiz-shell'>
            <div style='text-align:center;font-family:Noto Sans Tamil; font-size:0.78rem;color:#5a6a84;margin-bottom:6px'>பதில்கள் சுருக்கம்</div>
            <div class='result-breakdown'>{dots}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_l, col_c, col_r = st.columns([1, 1.5, 1])
        with col_c:
            if st.button("🔄 மீண்டும் விளையாடு", use_container_width=True, key="quiz_retry"):
                _reset()
                st.rerun()

    # --- EXECUTE THE QUIZ ---
    st.markdown(_QUIZ_CSS, unsafe_allow_html=True)
    _init_state()

    if st.session_state.quiz_complete:
        _render_results()
    elif not st.session_state.quiz_started:
        _render_splash()
    else:
        idx = st.session_state.quiz_index
        q   = QUIZ_QUESTIONS[idx]
        _render_progress(idx, st.session_state.quiz_score)
        _render_question(q, idx)
        _render_options(q, idx)
        _render_feedback(q, idx)
        _render_nav(idx)

# ──────────────────────────────────────────────────────────────────
# தாவல் 5 · தமிழர் வானியல் வரலாறு (Ancient Tamil Astronomy)
# ──────────────────────────────────────────────────────────────────
with tab5:
    st.header("🏛️ தமிழர் வானியல் வரலாறு")

    timeline_item("300 BCE", "சங்க காலம்", "தமிழர்கள் நட்சத்திரங்களை கொண்டு காலம் கணித்தனர்")
    timeline_item("500 BCE", "நட்சத்திர முறை", "27 நட்சத்திரங்கள் உருவாக்கப்பட்டது")
    timeline_item("Ancient Era", "கோயில் அறிவியல்", "சூரிய ஒளி alignment மூலம் கணிப்பு")
    timeline_item("Maritime Age", "கடல் பயணம்", "நட்சத்திரம் கொண்டு திசை கண்டறிதல்")

    st.markdown("### ⭐ நட்சத்திர அறிவு")
    st.markdown("""
<div class='gc'>
<div class='ta'>
தமிழர்கள் 27 நட்சத்திரங்களை (நட்சத்திர மண்டலம்) கண்டறிந்தனர்.<br><br>
இது இன்று:<br>
→ Nakshatra System (Indian Astronomy)<br><br>
பயன்பாடு:<br>
• திருமணம்<br>
• விவசாயம்<br>
• கால கணிப்பு<br><br>
முக்கியம்:<br>
சந்திரன் எந்த நட்சத்திரத்தில் இருக்கிறது என்பதை வைத்து நாள் கணிக்கப்பட்டது.
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### ⏳ கால கணக்கீடு (Time System)")
    st.markdown("""
<div class='gc gc-gold'>
<div class='ta'>
தமிழர்கள் மிகவும் துல்லியமான நேர கணக்கீடு செய்தனர்:<br><br>
🔸 நாள் → சூரியன் அடிப்படையில்<br>
🔸 மாதம் → சந்திரன் அடிப்படையில்<br>
🔸 ஆண்டு → பருவ மாற்றம் அடிப்படையில்<br><br>
அவர்கள் பயன்படுத்தியது:<br>
• சூரிய நிழல் (Shadow method)<br>
• சூரிய உதயம் / அஸ்தமனம்<br>
• நட்சத்திர நிலை
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 🛕 பயன்படுத்திய தொழில்நுட்பம் (Technology Used)")
    st.markdown("""
<div class='gc'>
<div class='ta'>
தமிழர்கள் advanced instruments இல்லாமல் இதை செய்தார்கள்:<br><br>
🔹 நிழல் கம்பம் (Gnomon) → நேரம் அளவிட<br>
🔹 கோயில் கட்டமைப்பு → சூரிய திசை alignment<br>
🔹 கல் குறியீடுகள் → seasonal tracking<br>
🔹 நீர் கடிகாரம் (Water clock)<br><br>
கோயில்கள்:<br>
• சூரிய ஒளி குறிப்பிட்ட நாளில் குறிப்பிட்ட இடத்தில் விழும்<br>
• இது ஒரு astronomical calculator போல வேலை செய்தது
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 👑 யார் இந்த அறிவை உருவாக்கினர்?")
    st.markdown("""
<div class='gc gc-pink'>
<div class='ta'>
இது ஒரே ஒரு மனிதரின் கண்டுபிடிப்பு அல்ல.<br><br>
பங்களித்தவர்கள்:<br>
🔸 சங்க கால அறிஞர்கள்<br>
🔸 சித்தர்கள்<br>
🔸 கோயில் கட்டிட நிபுணர்கள்<br>
🔸 விவசாயிகள்<br><br>
முக்கிய நூல்கள்:<br>
• சங்க இலக்கியம்<br>
• திருமந்திரம்<br>
• சிலப்பதிகாரம்<br>
• திருக்குறள்<br><br>
அவர்கள் observation + experience மூலம் அறிவை உருவாக்கினர்.
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 🌊 கடல் பயணம் (Navigation)")
    st.markdown("""
<div class='gc'>
<div class='ta'>
தமிழர்கள் பெரிய கடல் பயணிகள்:<br><br>
அவர்கள் பயன்படுத்தியது:<br>
• நட்சத்திர திசை<br>
• சந்திரன் நிலை<br>
• காற்றின் திசை<br><br>
இதன் மூலம்:<br>
→ இலங்கை<br>
→ தென்கிழக்கு ஆசியா<br>
→ ரோம பேரரசு<br>
வரை சென்றனர்.
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 🌾 விவசாயம் & வானியல்")
    st.markdown("""
<div class='gc'>
<div class='ta'>
வானியல் அறிவு = விவசாயத்தின் முதுகெலும்பு<br><br>
தமிழர்கள்:<br>
• மழை நேரம் கணித்தனர்<br>
• விதைப்பு நேரம் தீர்மானித்தனர்<br>
• அறுவடை காலம் கணித்தனர்<br><br>
இது அனைத்தும்:<br>
→ நட்சத்திரம் + சூரியன் + பருவம் அடிப்படையில்
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 🚀 முடிவு")
    st.success("தமிழர்கள் விஞ்ஞானிகள் — அவர்கள் வானத்தை பார்த்து உலகை புரிந்துகொண்டனர் 🌌")
    st.markdown("""
<div class='ta'>
அவர்கள் telescope இல்லாமல் செய்தது இன்று நாமும் வியக்கும் அளவுக்கு உள்ளது.<br><br>
இது:<br>
அறிவு + இயற்கை கவனிப்பு + அனுபவம்
</div>
""", unsafe_allow_html=True)     

    st.write("")
    st.markdown("### ⭐ இருபத்தேழு நட்சத்திரங்கள்")
    st.markdown("<div class='ta-sm' style='margin-bottom:12px'>27 நட்சத்திர மண்டலங்கள் · 27 Lunar Mansions (Nakshatras)</div>", unsafe_allow_html=True)

    nak_html = "<div class='gc'><div style='display:flex;flex-wrap:wrap;gap:8px'>"
    for idx, (ta_name, en_name) in enumerate(NAKSHATRAS):
        deg_s = idx * (360 / 27)
        nak_html += (
            f"<div style='background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.14);border-radius:10px; padding:6px 12px;min-width:0'>"
            f"<span style='color:#304050;font-family:Share Tech Mono;font-size:0.62rem'>{idx+1:02d} </span>"
            f"<span class='ta' style='font-size:0.88rem !important'>{ta_name}</span>"
            f"<span class='ta-sm' style='font-size:0.65rem !important;margin-left:5px; color:#304050 !important'>{deg_s:.1f}°</span>"
            f"</div>"
        )
    nak_html += "</div></div>"
    st.markdown(nak_html, unsafe_allow_html=True)

    

# ══════════════════════════════════════════════════════════════════
# அடிக்குறிப்பு · FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align:center;padding:1.5rem 0 1rem'>
    <div style='font-family:Orbitron,sans-serif;color:#00ffe7;font-size:0.82rem; letter-spacing:0.18em;margin-bottom:10px'>
        கோச்சடையான் · KOCHADAIIYAAN
    </div>
    <div class='ta' style='color:#5a6a84 !important;font-size:0.82rem; line-height:2'>
        யாதும் ஊரே யாவரும் கேளிர்
    </div>
    <div style='color:#3a4a5a;font-size:0.7rem;margin-top:4px; font-style:italic;font-family:Noto Sans Tamil,sans-serif'>
        "Every place is my homeland; every person is my kin."<br>
        — கணியன் பூங்குன்றனார், புறநானூறு 192
    </div>
    <div class='ta-sm' style='margin-top:10px;color:#202830 !important'>
        நாசா APOD API · Open-Notify ISS API · கெப்லர் வானியல் கணிதம் · புறநானூறு
    </div>
</div>
""", unsafe_allow_html=True)