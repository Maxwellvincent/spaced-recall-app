import streamlit as st
from firebase_db import db
import streamlit_authenticator as stauth
from login import run_login

st.set_page_config(page_title="Spaced Recall App", layout="centered")

st.title("📚 Welcome to the Spaced Recall App")

# === Logged-in View ===
if "username" in st.session_state:
    user = st.session_state["username"]
    st.success(f"👋 Welcome back, **{user}**!")

    st.markdown("Use the sidebar to start studying, editing subjects, or reviewing.")

    if st.button("🔓 Log out"):
        st.session_state.clear()
        st.rerun()

# === Not Logged-in View ===
else:
    # === Login Section ===
    st.subheader("🔐 Log In")
    user = run_login()
    if user:
        st.session_state["username"] = user
        st.success("✅ Login successful!")
        st.rerun()

    # === Always Show Register Form ===
    st.markdown("---")
    st.subheader("🆕 Register a New Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    new_username = st.text_input("Username (unique)")
    new_password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        users_ref = db.collection("users_metadata")
        user_doc = users_ref.document(new_username).get()

        if user_doc.exists:
            st.warning("🚫 Username already exists.")
        else:
            hashed_pw = stauth.Hasher().hash([new_password])[0]
            users_ref.document(new_username).set({
                "name": name,
                "email": email,
                "password": hashed_pw,
                "roles": ["user"]
            })
            st.success("✅ Account created! You can now log in above.")
