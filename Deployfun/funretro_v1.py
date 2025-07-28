from PIL import Image
import streamlit as st
import qrcode
from io import BytesIO
import time

# --- Page Config ---
st.set_page_config(page_title="Fun Retro", page_icon="🎉", layout="centered")

# --- Logo ---
st.image("fun2.png", width=150)
st.markdown("<h1 style='text-align: center; font-family: Comic Sans MS; color: #4B0082;'>🎉 Fun Retro</h1>", unsafe_allow_html=True)

# --- Session State ---
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

# --- Step Functions ---
def show_qr_page():
    st.subheader("📲 Scan to Start Retro")
    qr = qrcode.make("https://funretro.company/retro/session/abc")
    buf = BytesIO()
    qr.save(buf)
    st.image(Image.open(buf), caption="📱 Scan this QR code to open on mobile", width=200)
    if st.button("✅ I’ve scanned it"):
        st.session_state.step = 1

def show_theme_page():
    st.subheader("🎭 Choose a Theme")
    for name in themes:
        if st.button(name):
            st.session_state.theme = name
            st.session_state.step = 2

def show_feedback_page():
    theme = st.session_state.theme
    st.subheader(f"📝 Retro Theme: {theme}")
    st.session_state.feedback["good"] = st.text_area(themes[theme]["good"], value=st.session_state.feedback["good"])
    st.session_state.feedback["bad"] = st.text_area(themes[theme]["bad"], value=st.session_state.feedback["bad"])
    st.session_state.feedback["improve"] = st.text_area(themes[theme]["improve"], value=st.session_state.feedback["improve"])
    if st.button("📤 Submit to Jira"):
        time.sleep(1.5)
        st.session_state.ticket = "RET-123"
        st.session_state.step = 3

def show_submission_page():
    st.success("🎉 Feedback submitted!")
    st.markdown(f"📌 Your Jira ticket: **{st.session_state.ticket}**")
    st.balloons()
    if st.button("🔁 Start New Retro"):
        for key in ["step", "theme", "feedback", "ticket"]:
            if key in st.session_state:
                del st.session_state[key]

# --- Render Flow ---
steps = {
    0: show_qr_page,
    1: show_theme_page,
    2: show_feedback_page,
    3: show_submission_page
}
steps[st.session_state.step]()
