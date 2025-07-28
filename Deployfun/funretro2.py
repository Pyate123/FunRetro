import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Fun Retro Demo", layout="wide")

# Load Lottie Animations (if using)
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Header
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>🎉 Fun Retro Shark Tank Demo</h1>
    <p style='text-align: center;'>Make retros fun again with games, themes, emojis & more!</p>
""", unsafe_allow_html=True)

# Theme Selection
st.subheader("🎭 Choose a Retro Theme")
themes = ["🏏 Cricket Fever", "🎬 South Cinema Madness", "🕹 Arcade Throwback", "🏖 Beach Vibes", "🎃 Spooky Sprint"]
theme_choice = st.selectbox("Pick a theme for today's retro", themes)

# Retro Board
st.subheader(f"🎬 {theme_choice} Retro Board")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🟢 Mass Scenes\nWhat went well?")
    st.text_area("Share positives", key="good")
with col2:
    st.markdown("### 🟡 Flop Scenes\nWhat didn’t go well?")
    st.text_area("Share concerns", key="bad")
with col3:
    st.markdown("### 🔵 Director’s Cut\nWhat can we do better?")
    st.text_area("Share improvements", key="better")

st.markdown("---")

# Emoji Reaction Wall
st.subheader("🎉 Emoji Reaction Wall")
st.markdown("Click your reactions for today’s sprint!")
emoji_cols = st.columns(5)
emoji_list = ["🔥", "🙌", "😢", "💥", "🎯"]
for i, emoji in enumerate(emoji_list):
    if emoji_cols[i].button(emoji):
        st.success(f"You clicked {emoji}")

st.markdown("---")

# Appreciation Wall
st.subheader("💐 Lights, Camera, Appreciation!")
st.text_input("Give a shoutout to a teammate:", key="appreciation")

# Wrap Up
if st.button("🎬 Wrap Up and Reveal Next Theme"):
    st.balloons()
    st.markdown("""
        ### 🎬 That’s a Wrap!
        Thanks for joining the Fun Retro session.

        📣 **Next Theme Teaser**: 🧙‍♂️ Harry Potter Sprint!
    """)
