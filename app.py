import streamlit as st
from login import run_login
from firebase_db import db
import streamlit_authenticator as stauth

st.set_page_config(page_title="Spaced Recall App", layout="centered")

st.title("📚 Welcome to the Spaced Recall App")

# === Already Logged In ===
if "username" in st.session_state:
    user = st.session_state["username"]
    st.success(f"👋 Welcome back, **{user}**!")

    st.markdown("Use the sidebar to start studying, editing, or reviewing.")
    
    if st.button("🔓 Log out"):
        st.session_state.clear()
        st.rerun()

# === Not Logged In Yet ===
else:
    # === LOGIN ===
    st.subheader("🔐 Log In")
    user = run_login()
    if user:
        st.session_state["username"] = user
        st.success("✅ Login successful!")
        st.rerun()

    # === REGISTER FORM ===
    st.markdown("---")
    st.subheader("🆕 Create a New Account")

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
