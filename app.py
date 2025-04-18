import streamlit as st
from firebase_db import db
import streamlit_authenticator as stauth

st.set_page_config(page_title="Register Test", layout="centered")

st.title("🆕 Register Test Page")

st.markdown("Trying to register a new user below...")

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
        st.success("✅ Account created! 🎉")
