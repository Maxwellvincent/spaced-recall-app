import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Example hardcoded user credentials
# In production, store this in a secure DB or config file
config = {
    'credentials': {
        'usernames': {
            'louis': {
                'email': 'louis@example.com',
                'name': 'Louis Maxwel',
                'password': stauth.Hasher(['test123']).generate()[0]  # hashed
            },
            'admin': {
                'email': 'admin@example.com',
                'name': 'Admin User',
                'password': stauth.Hasher(['admin123']).generate()[0]
            }
        }
    },
    'cookie': {
        'name': 'spaced_recall_login',
        'key': 'random_signature_key',
        'expiry_days': 30
    },
    'preauthorized': {
        'emails': ['louis@example.com']
    }
}

def run_login():
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    name, auth_status, username = authenticator.login('Login', 'main')

    if auth_status is False:
        st.error('❌ Username or password is incorrect.')
    if auth_status is None:
        st.warning('⚠️ Please enter your credentials.')

    if auth_status:
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.success(f"✅ Logged in as {name}")
        return username  # Return user for session use
    else:
        st.stop()
