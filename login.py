import streamlit as st
import streamlit_authenticator as stauth

# === Define users (name, username, email)
names = ["Louis Maxwel", "Admin User"]
usernames = ["louis", "admin"]
emails = ["louis@example.com", "admin@example.com"]
passwords = ["test123", "admin123"]  # Plaintext temporarily

# === Hash passwords
hashed_passwords = [stauth.Hasher().hash(pw) for pw in passwords]

# === Build credentials config
credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "email": emails[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

# === Create authenticator instance
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="spaced_recall_login",
    key="random_signature_key_12345",
    cookie_expiry_days=30
)

# === Handle login
def run_login():
    # Ensure 'logout' key is initialized
    if 'logout' not in st.session_state:
        st.session_state['logout'] = False
        
    name, auth_status, username = authenticator.login(location="main")

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
