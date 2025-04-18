import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects, add_user_xp


st.set_page_config(page_title="Spaced Recall App", layout="centered")

st.title("📚 Welcome to the Spaced Recall App")

st.markdown("""
This is your personalized learning system, with spaced repetition, XP leveling, and anime-powered global progress.

Choose a page from the sidebar to get started:
- 📘 Create subjects and study plans
- 🛠️ Edit existing subjects, topics, or sections
- 📈 Track progress (coming soon)
""")
