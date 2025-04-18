import streamlit as st
from login import run_login

st.set_page_config(page_title="Spaced Recall App", layout="centered")

st.title("📚 Welcome to the Spaced Recall App")

st.markdown("""
👋 **Welcome, future master of memory!**

Spaced Recall is your personal learning command center. Here's what it helps you do:

- 🧠 Learn deeply using intelligent spaced repetition
- ✍️ Organize your studies across subjects and topics
- 📆 Track your review schedule and never forget a concept
- ⚡ Customize your learning style: exam prep, mind maps, reading logs, and more
- 🎮 Gain XP and level up with power meters based on your progress
- 🧙 Personalize with themes like Naruto chakra mode, DBZ power levels, or minimalist stats

Use the sidebar to begin:
- 🔐 Log in if you're already a user
- 🆕 Go to the Register page to create your account
- 🧭 Explore your dashboard, subjects, and study logs once logged in
""")

# === LOGGED IN VIEW ===
if "username" in st.session_state:
    user = st.session_state["username"]
    st.success(f"👋 Welcome back, **{user}**!")

    st.markdown("Use the sidebar to explore your dashboard, edit subjects, or begin reviewing.")

    if st.button("🔓 Log out"):
        st.session_state.clear()
        st.rerun()

# === NOT LOGGED IN ===
else:
    st.subheader("🔐 Log In")
    user = run_login()
    if user:
        st.session_state["username"] = user
        st.success("✅ Login successful!")
        st.rerun()
