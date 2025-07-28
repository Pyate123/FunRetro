import streamlit as st
import time
import qrcode
from PIL import Image
import io

# ------------------ QR Code Generator ------------------
def generate_qr(data: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Image.open(buf)

# ------------------ Page 0: QR Code Scan ------------------
def show_qr_scan_page():
    st.markdown("### 🧑‍🚀 Fun Retro")
    st.image("https://cdn-icons-png.flaticon.com/512/8766/8766412.png", width=100)
    st.markdown("<h3 style='text-align: center; color: #5c3df3;'>Fun Retro</h3>", unsafe_allow_html=True)

    retro_url = "https://example.com/retro"
    qr_img = generate_qr(retro_url)
    st.image(qr_img, width=200)
    st.markdown("<p style='text-align: center;'>📱 Scan to open the retro on your phone</p>", unsafe_allow_html=True)

    if st.button("🚀 I've scanned it"):
        st.session_state.step = 1

# ------------------ Page 1: Theme Selection ------------------
themes = [
    {"name": "Cricket Fever", "emoji": "🏏", "bg": "#d4f1dc"},
    {"name": "South Cinema", "emoji": "🎬", "bg": "#f7d4d4"},
    {"name": "Space Odyssey", "emoji": "🚀", "bg": "#e2dcf9"},
    {"name": "Time Travel", "emoji": "⏳", "bg": "#f9eec9"},
    {"name": "Magical Disney", "emoji": "🐭", "bg": "#fcdcec"},
]

def show_theme_step():
    st.subheader("🌈 Pick a fun vibe for today")
    for theme in themes:
        card = f"""
        <div style="
            background-color:{theme['bg']};
            padding:15px 25px;
            margin:10px 0;
            border-radius:12px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            cursor:pointer;
            border: 1px solid #ccc;
        "
        onclick="document.querySelector('form button[name=\\'{theme['name']}\\']').click()"
        >
            <div style="font-size:16px;">{theme['emoji']} {theme['name']}</div>
            <div style="font-size:16px;">⭐</div>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)
        if st.button(theme["name"], key=theme["name"]):
            st.session_state.theme = theme
            st.session_state.step = 2
            st.session_state.start_time = time.time()

# ------------------ Page 2: Feedback Form ------------------
def show_feedback_form():
    theme = st.session_state.theme
    st.markdown(f"### {theme['emoji']} {theme['name']}", unsafe_allow_html=True)
    st.markdown("---")

    questions = [
        {"icon": "✅", "emoji": "🚀", "question": "Which thrusters fired flawlessly?", "key": "positive_feedback"},
        {"icon": "👎", "emoji": "🔥", "question": "Where did we burn extra fuel?", "key": "negative_feedback"},
        {"icon": "💡", "emoji": "🛠️", "question": "What upgrades ensure a smoother orbit?", "key": "suggestion_feedback"},
    ]

    for q in questions:
        st.markdown(f"**{q['icon']} {q['emoji']} {q['question']}**")
        st.text_area("Share your thoughts...", key=q["key"], height=100)
        st.markdown("")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to Themes"):
            st.session_state.step = 1
    with col2:
        if st.button("👀 Preview My Feedback"):
            st.session_state.step = 3

# ------------------ Page 3: Preview Feedback ------------------
def preview_feedback():
    theme = st.session_state.theme
    st.markdown("### 🔍 Review your feedback", unsafe_allow_html=True)
    st.markdown("---")

    questions = [
        {"question": "Which thrusters fired flawlessly?", "emoji": "🚀", "key": "positive_feedback", "ok_icon": "✅", "fail_icon": "☐"},
        {"question": "Where did we burn extra fuel?", "emoji": "🔥", "key": "negative_feedback", "ok_icon": "❌", "fail_icon": "☐"},
        {"question": "What upgrades ensure a smoother orbit?", "emoji": "🛠️", "key": "suggestion_feedback", "ok_icon": "💡", "fail_icon": "☐"},
    ]

    for q in questions:
        response = st.session_state.get(q["key"], "").strip()
        icon = q["ok_icon"] if response else q["fail_icon"]
        st.markdown(f"**{q['emoji']} {q['question']}**")
        st.markdown(f"{icon} {'Provided' if response else 'No response'}")
        st.markdown("")

    st.markdown("---")

    # Add text input for dynamic ticket ID
    ticket_input = st.text_input("Enter JIRA ticket ID", value=st.session_state.get("ticket_id", ""))

    if st.button("🚀 Submit to Jira"):
        if ticket_input.strip() == "":
            st.error("Please enter a JIRA ticket ID before submitting.")
        else:
            st.session_state.ticket_id = ticket_input.strip()
            st.session_state.step = 4
            st.rerun()

    if st.button("🔁 Edit Feedback"):
        st.session_state.step = 2
        st.rerun()

# ------------------ Page 4: Feedback Submitted ------------------
def show_success_page():
    ticket = st.session_state.get("ticket_id", "RET-123")
    st.markdown("### 🎉 Feedback submitted successfully!", unsafe_allow_html=True)

    st.markdown("<div style='font-size:60px; text-align:center;'>🥳</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <h3 style='text-align: center; color: #111;'>
        🎉 <strong>Feedback submitted successfully!</strong>
        </h3>
        <p style='text-align: center; font-size: 18px;' >
        📌 Created Jira ticket <a href="#" style='color:#5c3df3; text-decoration:none;'><strong>{ticket}</strong></a>
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧾 Start New Retro"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.step = 0
            st.rerun()
            
# ------------------ Init Session State ------------------
if "step" not in st.session_state:
    st.session_state.step = 0  # Start from QR page

# ------------------ Main App Controller ------------------
if st.session_state.step == 0:
    show_qr_scan_page()
elif st.session_state.step == 1:
    show_theme_step()
elif st.session_state.step == 2:
    show_feedback_form()
elif st.session_state.step == 3:
    preview_feedback()
elif st.session_state.step == 4:
    show_success_page()
