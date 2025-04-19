import streamlit as st
from login import run_login

st.set_page_config(page_title="Spaced Recall App", layout="centered")

# 🔐 Login
if "username" not in st.session_state:
    user = run_login()
    if not user:
        st.stop()
else:
    user = st.session_state["username"]

# ✅ Welcome UI
st.title("🧠 Spaced Recall Hub")
name = st.session_state.get("name", user)
st.success(f"✅ Welcome, {name}!")

st.subheader("📚 Choose where to go next:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        st.markdown("[Redirecting...](./Dashboard)")

with col2:
    if st.button("🛠️ Subject Editor"):
        st.markdown("[Redirecting...](./Subject_Editor)")

with col3:
    if st.button("🎮 Profile"):
        st.markdown("[Redirecting...](./Profile)")

# === Optional Logout ===
st.markdown("---")
if st.button("🔒 Log out"):
    st.session_state.clear()
    st.rerun()
