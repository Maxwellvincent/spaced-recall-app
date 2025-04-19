import streamlit as st
from login import run_login

st.set_page_config(page_title="Spaced Recall App", layout="centered")

# 🔐 Login check
if "username" not in st.session_state:
    user = run_login()
    if not user:
        st.stop()
else:
    user = st.session_state["username"]

# ✅ Meta redirect if page triggered
if st.session_state.get("navigation_triggered"):
    st.session_state["navigation_triggered"] = False
    page = st.session_state.pop("target_page", None)
    if page:
        st.markdown(f"<meta http-equiv='refresh' content='0;URL=./{page}'>", unsafe_allow_html=True)
        st.stop()

# === Navigation helper ===
def go_to_page(page_name):
    st.session_state["target_page"] = page_name
    st.session_state["navigation_triggered"] = True
    st.experimental_rerun()

# === Main UI ===
st.title("🧠 Spaced Recall Hub")
name = st.session_state.get("name", user)
st.success(f"✅ Welcome, {name}!")
# Meta redirect if navigation was requested
if "target_page" in st.session_state:
    page = st.session_state.pop("target_page")
    st.markdown(f"<meta http-equiv='refresh' content='0;URL=./{page}'>", unsafe_allow_html=True)
    st.stop()


st.subheader("📚 Choose where to go next:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        st.session_state["target_page"] = "Dashboard"

with col2:
    if st.button("🛠️ Subject Editor"):
        st.session_state["target_page"] = "Subject_Editor"


with col3:
    if st.button("🎮 Profile"):
        st.session_state["target_page"] = "Profile"


st.markdown("---")
if st.button("🔒 Log out"):
    st.session_state.clear()
    st.rerun()
