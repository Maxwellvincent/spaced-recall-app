import streamlit as st
from firebase_db import db
import streamlit_authenticator as stauth

st.set_page_config(page_title="Register", layout="centered")

st.title("🆕 Create a New Account")

st.markdown("""
Register now to start tracking your study progress, reviewing smarter with spaced repetition,
and leveling up your learning power with XP-based achievements.
""")

# === Registration Form ===
name = st.text_input("Full Name")
email = st.text_input("Email")
username = st.text_input("Username (unique)")
password = st.text_input("Password", type="password")

if st.button("Create Account"):
    if not name or not email or not username or not password:
        st.warning("🚫 All fields are required.")
    else:
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
            st.success("✅ Account created successfully!")
            st.info("You can now return to the Home page and log in.")
