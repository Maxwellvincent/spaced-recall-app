import streamlit as st
import streamlit_authenticator as stauth

# === Define users
names = ["Louis Maxwel", "Admin User"]
usernames = ["louis", "admin"]
emails = ["louis@example.com", "admin@example.com"]

# Hashed passwords: use plain text first, then hash and replace (see note below)
passwords = ["test123", "admin123"]
hashed_passwords = [stauth.Hasher().hash(pw) for pw in passwords]


# === Authentication configuration
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
    key="random_signature_key_12345",
    cookie_expiry_days=30
)

# === Run login process
def run_login():
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status is False:
        st.error("❌ Incorrect username or password.")
    elif auth_status is None:
        st.warning("⚠️ Please enter your credentials.")

    if auth_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.success(f"✅ Logged in as: {name}")
        return username
    else:
        st.stop()
