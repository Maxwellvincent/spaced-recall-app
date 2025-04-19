import streamlit as st
from firebase_db import db
import streamlit_authenticator as stauth
import bcrypt


st.set_page_config(page_title="Register", layout="centered")
st.title("🆕 Create a New Account")

st.markdown("""
Register now to start tracking your study progress, reviewing smarter with spaced repetition,
and leveling up your learning power with XP-based achievements.
""")

# === Registration Form ===
with st.form("register_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username (unique)")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Create Account")

    if submit:
        if not name or not email or not username or not password:
            st.warning("🚫 All fields are required.")
        else:
            try:
                users_ref = db.collection("users_metadata")
                user_doc = users_ref.document(username).get()

                if user_doc.exists:
                    st.warning("🚫 Username already exists.")
                else:
                    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                    users_ref.document(username).set({
                        "name": name,
                        "email": email,
                        "password": hashed_pw,
                        "roles": ["user"]
                    })
                    st.success("✅ Account created! Please log in on the Home page.")
            except Exception as e:
                st.error(f"❌ Error writing to Firestore: {e}")
