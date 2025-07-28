
import streamlit as st

import qrcode

from io import BytesIO

from PIL import Image

import time

import os

 

# --- Page Setup ---c

st.set_page_config(page_title="Fun Retro", page_icon="🎉", layout="centered")

 # Theme configurations
bg_themes = {
    "Cricket": {
        "bg_texture": "https://dm0qx8t0i9gc9.cloudfront.net/watermarks/image/rDtN98Qoishumwih/vector-illustration-of-cricket-background_G14nsZ5u_SB_PM.jpg",
        "bg_color": "#28a745",
        "text_color": "#ffffff"
    },
    "Cinema": {
        "bg_texture": "https://www.transparenttextures.com/patterns/brilliant.png",
        "bg_color": "#dc3545",
        "text_color": "#ffffff"
    },
    "Space": {
        "bg_texture": "https://www.transparenttextures.com/patterns/dark-geometric.png",
        "bg_color": "#6610f2",
        "text_color": "#ffffff"
    }
}

# Initialize session state
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "Cricket"


st.markdown("""

    <style>

    /* Target the main app container instead of html/body */

    [data-testid="stAppViewContainer"] {

        background-image: url("https://www.transparenttextures.com/patterns/food.png");

        background-color: #00a2bf;

        background-attachment: fixed;

        background-size: auto;

    }

 

    /* Center block content with translucent styling */

    .block-container {

        background-color: rgba(255, 255, 255, 0.85);

        padding: 2rem 2rem 3rem;

        border-radius: 15px;

        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);

        max-width: 700px;
        margin: auto;

    }

    </style>

""", unsafe_allow_html=True)

 



# --- Logo Display ---

logo_path = "https://s14.gifyu.com/images/bHD96.gif"
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_path}" width="300">
    </div>
    """,
    unsafe_allow_html=True
)

#st.markdown("<h1 style='text-align: center; font-family: Comic Sans MS; color: #4B0082;'>🎉 Fun Retro</h1>", unsafe_allow_html=True)

 

# --- Initialize State ---

if "step" not in st.session_state:

    st.session_state.step = 0

if "theme_button" not in st.session_state:

    st.session_state["theme_button"] = None

if "feedback" not in st.session_state:

    st.session_state.feedback = {"good": "", "bad": "", "improve": ""}

if "ticket" not in st.session_state:

    st.session_state.ticket = None

 

# --- Themes ---

themes = {

    "🏏 Cricket Fever": {

        "good": "🏆 What were our Match Winning Moments this sprint?",

        "bad": "💥 Where did we lose wickets?",

        "improve": "🚀 How do we improve our Game Plan next sprint?"

    },

    "🐉 Game of Thrones": {

        "good": "🛡️ Which team moments were worthy of the Iron Throne?",

        "bad": "🧟 Where did the ‘White Walkers’ invade",

        "improve": "⚔️ What alliances or strategies do we need next sprint?"

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

 

def center_text(text, size="22px", color="#4B0082", weight="bold"):

    return f"<div style='text-align:center;font-size:{size};color:{color};font-weight:{weight};'>{text}</div>"

 

# --- Step 0: QR Code ---

def show_qr():

    st.markdown(center_text("Scan to Start", "24px"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2,2,1.2])

    with col2:

        qr = qrcode.make("https://funretro.company/retro/session/abc")

        buf = BytesIO()

        qr.save(buf)

        st.image(Image.open(buf), caption="📱 Scan this QR code to open on mobile", width=275)

        st.markdown("<div style='text-align:right; margin-top: 2rem;'>", unsafe_allow_html=True)

        st.button("✅ I’ve scanned it", use_container_width=True, type="primary", on_click=advance_step)

 

def advance_step():

    st.session_state.step = 1

def set_theme(theme):
    """Store selected theme and proceed to feedback"""
    st.session_state.selected_theme = theme["label"]
    st.session_state.theme = theme["label"]
    st.session_state.theme_config = {
        "bg_texture": theme["bg_texture"]
                }
    goto_feedback(theme["label"])  # Call your feedback navigation

def goto_feedback(theme_label):
    """Navigate to feedback page"""
    st.session_state.step = 2  # Assuming 2 is your feedback page index
    # No need for rerun - Streamlit handles this automatically

# --- Step 1: Theme Selection ---
def show_theme():
    st.markdown(center_text("🎭 Choose a Theme", "26px"), unsafe_allow_html=True)

    themes = [
        {"label": "🏏 Cricket Fever", "color": "#1BD7BE",             "bg_texture": "https://www.transparenttextures.com/patterns/crissxcross.png",
},
        {"label": "🐉 Game of Thrones", "color": "#dc3545",             "bg_texture": "https://www.transparenttextures.com/patterns/brilliant.png",
},
        {"label": "🪐 Space Odyssey", "color": "#1BD7BE",             "bg_texture": "https://www.transparenttextures.com/patterns/dark-geometric.png",
},
        {"label": "⏳ Time Travel", "color": "#fd7e14",             "bg_texture": "https://www.transparenttextures.com/patterns/45-degree-fabric-light.png",
},
        {"label": "🐭 Magical Disney", "color": "#e83e8c",             "bg_texture": "https://www.transparenttextures.com/patterns/always-grey.png",
},
    ]

    if 'theme_config' in st.session_state:
        st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background-image: {st.session_state.theme_config['bg_texture']};
            }}
        </style>
        """, unsafe_allow_html=True)

    # Generate dynamic CSS for each button
    button_styles = """
    <style>
    """
    
    for i, theme in enumerate(themes):
        button_styles += f"""
        div[data-testid="stButton"] > button[kind="secondary"]:nth-child({i+1}) {{
            background-color: {theme['color']} !important;
            border: none !important;
            padding: 14px 20px !important;
            width: 100% !important;
            border-radius: 12px !important;
            margin-bottom: 14px !important;
            color: white !important;
            font-size: 28px !important;
            font-weight: bold !important;
            text-align: center !important;
            cursor: pointer !important;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.15) !important;
            transition: all 0.3s ease !important;
        }}
        
        div[data-testid="stButton"] > button[kind="secondary"]:nth-child({i+1}):hover {{
            opacity: 0.85 !important;
            color: white !important;
            transform: scale(1.02) !important;
        }}
        """
    
    button_styles += """
    </style>
    """
    
    st.markdown(button_styles, unsafe_allow_html=True)

    for theme in themes:
        col1, col2, col3 = st.columns([0.5, 4, 0.5])
        with col2:
            st.button(
                theme['label'],
                key=f"theme_{theme['label']}",  # More unique key
                on_click=set_theme,
                args=(theme,),
            )


 

# --- Step 2: Feedback Collection ---

def show_feedback():

    theme = st.session_state.theme

    st.markdown(center_text(f"📝 {theme}", "22px"), unsafe_allow_html=True)


    with st.form("feedback_form"):

        st.session_state.feedback["good"] = st.text_area(themes[theme]["good"], value=st.session_state.feedback["good"])

        st.session_state.feedback["bad"] = st.text_area(themes[theme]["bad"], value=st.session_state.feedback["bad"])

        st.session_state.feedback["improve"] = st.text_area(themes[theme]["improve"], value=st.session_state.feedback["improve"])

        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

        submitted = st.form_submit_button("👀 Preview My Feedback", type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

       

   

    if submitted:

        st.session_state.step = 3

        st.rerun()

 

# --- Step 3: Preview Feedback (Single-click submit) ---

def show_preview():

    theme = st.session_state.theme

    fb = st.session_state.feedback

    st.markdown(center_text("🔍 Preview Your Feedback", "22px"), unsafe_allow_html=True)

    st.markdown(f"{themes[theme]['good']}\n\n✅ {fb['good']}")

    st.markdown(f"{themes[theme]['bad']}\n\n❌ {fb['bad']}")

    st.markdown(f"{themes[theme]['improve']}\n\n💡 {fb['improve']}")

 

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✏️ Edit"):

            st.session_state.step = 2

            st.rerun()

         

    with col2:

        if st.button("📤 Submit to Jira"):

            time.sleep(1.5)

            st.session_state.ticket = "RET-123"

            st.session_state.step = 4

            st.rerun()

 

# --- Step 4: Done ---

def show_done():

    st.markdown(center_text("🎉 Feedback Submitted Successfully!", "22px", "#228B22"), unsafe_allow_html=True)

    st.success(f"📌 Created Jira ticket: {st.session_state.ticket}")

    st.balloons()

    if st.button("🔁 Start New Retro", use_container_width=True):

        for k in ["step", "theme", "feedback", "ticket"]:

            if k in st.session_state:

                del st.session_state[k]

    st.session_state.step = 0

# --- App Step Flow ---

[show_qr, show_theme, show_feedback, show_preview, show_done][st.session_state.step]()
