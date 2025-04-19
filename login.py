import streamlit as st
from firebase_db import db
import bcrypt

def run_login():
    with st.form("login_form"):
        login_id = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Look for exact match by username
            user_ref = db.collection("users_metadata").document(login_id)
            user_doc = user_ref.get()

            if not user_doc.exists:
                # Try finding by email
                results = db.collection("users_metadata").where("email", "==", login_id).stream()
                matched_doc = None
                for doc in results:
                    matched_doc = doc
                    break

                if matched_doc:
                    user_doc = matched_doc
                    login_id = matched_doc.id  # Set login_id to the found username
                else:
                    st.error("❌ No user found with that username or email.")
                    return None

            data = user_doc.to_dict()
            hashed_pw = data.get("password", "")

            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                st.session_state["username"] = login_id
                st.session_state["name"] = data.get("name", login_id)
                st.session_state["roles"] = data.get("roles", ["user"])
                return login_id
            else:
                st.error("❌ Incorrect password.")
                return None
