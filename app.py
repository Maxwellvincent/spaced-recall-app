import streamlit as st
st.set_page_config(page_title="Spaced Recall App", layout="centered")

from login import run_login

if "username" not in st.session_state:
    user = run_login()
    st.session_state["username"] = user
else:
    user = st.session_state["username"]

# ✅ Debug
st.sidebar.write("🔐 Logged in as:", user)

# Home UI
st.title("📚 Welcome to Spaced Recall App")
st.markdown(f"👋 Hello, `{user}`!")


st.markdown("""
This is your personalized learning system, with spaced repetition, XP leveling, and anime-powered global progress.

Choose a page from the sidebar to get started:
- 📘 Create subjects and study plans
- ✏️ Edit existing subjects, topics, or sections
- 📈 Track progress (coming soon)
""")
