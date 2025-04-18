import streamlit as st
from login import run_login

st.set_page_config(page_title="Spaced Recall App", layout="centered")

# 🔐 Handle login once
user = run_login()

# ✅ Store user globally so all pages can access
st.session_state["user"] = user

# 🎉 Landing Page
st.title("📚 Welcome to the Spaced Recall App")
st.markdown(f"👋 Hello, `{user}`!")

st.markdown("""
This is your personalized learning system, with spaced repetition, XP leveling, and anime-powered global progress.

Choose a page from the sidebar to get started:
- 📘 Create subjects and study plans
- ✏️ Edit existing subjects, topics, or sections
- 📈 Track progress (coming soon)
""")
