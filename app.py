import streamlit as st
st.set_page_config(page_title="Spaced Recall App", layout="centered")

from login import run_login
from firebase_db import db
import streamlit_authenticator as stauth



# === LOGGED IN VIEW ===
if "username" in st.session_state:
    user = st.session_state["username"]
    st.title("📚 Welcome to the Spaced Recall App")
    st.markdown(f"👋 Hello, **{user}**!")

    st.markdown("Use the sidebar to start studying, editing subjects, or reviewing.")

    if st.button("🔓 Log out"):
        st.session_state.clear()
        st.rerun()


# === GUEST VIEW ===
else:
    st.title("📚 Welcome to the Spaced Recall App")
    st.markdown("""
    👋 **Welcome, future master of memory!**

    This app helps you:
    - 🧠 Learn deeply through spaced repetition
    - 📈 Track progress by topic, section, and subject
    - 🏆 Level up with XP, confidence, and AI feedback
    - 🎮 Customize your learning journey with anime-style power levels
    """)

    # === LOGIN ===
    st.subheader("🔐 Log In")
    user = run_login()
    if user:
        st.session_state["username"] = user
        st.success("✅ Login successful.")
        st.stop()

    # === REGISTER ===
    st.markdown("---")
    st.subheader("🆕 Register a New Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username (unique)")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        users_ref = db.collection("users_metadata")
        user_doc = users_ref.document(username).get()

        if user_doc.exists:
            st.warning("🚫 Username already exists.")
        else:
            hashed_pw = stauth.Hasher().hash([password])[0]
            users_ref.document(username).set({
                "name": name,
                "email": email,
                "password": hashed_pw,
                "roles": ["user"]
            })
            st.success("✅ Account created! You can now log in above.")

