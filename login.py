import streamlit as st
import streamlit_authenticator as stauth

names = ["Louis Maxwel", "Admin User"]
usernames = ["louis", "admin"]
emails = ["louis@example.com", "admin@example.com"]
passwords = ["test123", "admin123"]

hashed_passwords = [stauth.Hasher().hash(pw) for pw in passwords]

credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "email": emails[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name="spaced_recall_login",
    key="random_signature_key_123",
    cookie_expiry_days=30
)

def run_login():
    if "logout" not in st.session_state:
        st.session_state["logout"] = False

    result = authenticator.login("main", "Login")
    if result is None:
        st.warning("⚠️ Please enter your credentials.")
        st.stop()

    name, auth_status, username = result

    if auth_status is False:
        st.error("❌ Incorrect username or password.")
        st.stop()
    elif auth_status is None:
        st.warning("⚠️ Please enter your credentials.")
        st.stop()

    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"✅ Logged in as: {name}")
    return username  # <== this must return a string like "louis"

