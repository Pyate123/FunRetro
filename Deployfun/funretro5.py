import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import time
import os

# --- Page Setup ---
st.set_page_config(page_title="Fun Retro", page_icon="🎉", layout="centered")

# --- Logo Display ---
logo_path = "88051679-0dbe-4554-a05b-ec95622f4e9f.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
st.markdown("<h1 style='text-align: center; font-family: Comic Sans MS; color: #4B0082;'>🎉 Fun Retro</h1>", unsafe_allow_html=True)

# --- Initialize State ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "theme" not in st.session_state:
    st.session_state.theme = None
if "feedback" not in st.session_state:
    st.session_state.feedback = {"good": "", "bad": "", "improve": ""}
if "ticket" not in st.session_state:
    st.session_state.ticket = None

# --- Themes ---
themes = {
    "🏏 Cricket Fever": {
        "good": "🏆 Which shots hit the boundary?",
        "bad": "💥 Where did we lose wickets?",
        "improve": "🚀 How can we level up our next innings?"
    },
    "🎬 South Cinema": {
        "good": "🎉 Which scenes got whistles?",
        "bad": "😴 Which plot holes bored the crowd?",
        "improve": "🎬 What twist will make the sequel blockbuster?"
    },
    "🪐 Space Odyssey": {
        "good": "🚀 Which thrusters fired flawlessly?",
        "bad": "🔥 Where did we burn extra fuel?",
        "improve": "🔧 What upgrades ensure a smoother orbit?"
    },
    "⏳ Time Travel": {
        "good": "📅 What moment was worth repeating?",
        "bad": "🕳️ Where did we get stuck in a time loop?",
        "improve": "🔮 What would future-you suggest?"
    },
    "🐭 Magical Disney": {
        "good": "✨ Which spells worked wonders?",
        "bad": "🦹‍♂️ What villains challenged our path?",
        "improve": "🧙 What new magic can we bring next time?"
    }
}

# --- Centered Header Text ---
def center_text(text, size="22px", color="#4B0082", weight="bold"):
    return f"<div style='text-align:center;font-size:{size};color:{color};font-weight:{weight};'>{text}</div>"

# --- Step 0: QR Code ---
def show_qr():
    st.markdown(center_text("📲 Scan to Start Retro", "24px"), unsafe_allow_html=True)
    qr = qrcode.make("https://funretro.company/retro/session/abc")
    buf = BytesIO()
    qr.save(buf)
    st.image(Image.open(buf), caption="📱 Scan this QR code to open on mobile", width=200)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(center_text("👇 Click once scanned", "16px", "#444"), unsafe_allow_html=True)
    if st.button("✅ I’ve scanned it", use_container_width=True):
        st.session_state.step = 1

# --- Step 1: Theme Selection ---
def show_theme():
    st.markdown(center_text("🎭 Choose a Theme", "24px"), unsafe_allow_html=True)
    for name in themes:
        st.button(name, use_container_width=True, on_click=lambda n=name: select_theme(n))

def select_theme(name):
    st.session_state.theme = name
    st.session_state.step = 2

# --- Step 2: Feedback Collection ---
def show_feedback():
    theme = st.session_state.theme
    st.markdown(center_text(f"📝 Retro Theme: {theme}", "22px"), unsafe_allow_html=True)

    with st.form("feedback_form"):
        st.session_state.feedback["good"] = st.text_area(themes[theme]["good"], value=st.session_state.feedback["good"])
        st.session_state.feedback["bad"] = st.text_area(themes[theme]["bad"], value=st.session_state.feedback["bad"])
        st.session_state.feedback["improve"] = st.text_area(themes[theme]["improve"], value=st.session_state.feedback["improve"])
        submitted = st.form_submit_button("👀 Preview My Feedback")
        if submitted:
            st.session_state.step = 3

# --- Step 3: Preview Feedback (with Edit option) ---
def show_preview():
    theme = st.session_state.theme
    fb = st.session_state.feedback
    st.markdown(center_text("🔍 Preview Your Feedback", "22px"), unsafe_allow_html=True)
    st.markdown(f"**{themes[theme]['good']}**\n\n✅ {fb['good']}")
    st.markdown(f"**{themes[theme]['bad']}**\n\n❌ {fb['bad']}")
    st.markdown(f"**{themes[theme]['improve']}**\n\n💡 {fb['improve']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Edit"):
            st.session_state.step = 2
    with col2:
        if st.button("📤 Submit to Jira"):
            time.sleep(1.5)
            st.session_state.ticket = "RET-123"
            st.session_state.step = 4

# --- Step 4: Done ---
def show_done():
    st.markdown(center_text("🎉 Feedback Submitted Successfully!", "22px", "#228B22"), unsafe_allow_html=True)
    st.success(f"📌 Created Jira ticket: **{st.session_state.ticket}**")
    st.balloons()
    if st.button("🔁 Start New Retro"):
        for k in ["step", "theme", "feedback", "ticket"]:
            if k in st.session_state:
                del st.session_state[k]

# --- App Step Flow ---
[show_qr, show_theme, show_feedback, show_preview, show_done][st.session_state.step]()
