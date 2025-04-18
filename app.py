import streamlit as st
st.set_page_config(page_title="Spaced Recall App", layout="centered")

from login import run_login

if "username" not in st.session_state:
    user = run_login()
    st.session_state["username"] = user
else:
    user = st.session_state["username"]

# ✅ Debug
st.sidebar.write("🔐 Logged in as:", user)

# Home UI
st.title("📚 Welcome to Spaced Recall App")
st.markdown(f"👋 Hello, `{user}`!")

st.markdown("Use the sidebar to start studying, editing subjects, or reviewing.")

# === Optional: Toggle Register Form ===
st.markdown("---")
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

if st.button("🆕 Register New Account"):
    st.session_state["show_register"] = not st.session_state["show_register"]

if st.session_state["show_register"]:
    st.subheader("Create a New Account")

    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        username = st.text_input("Username (unique)")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            users_ref = db.collection("users_metadata")
            user_doc = users_ref.document(username).get()

            if user_doc.exists:
                st.warning("🚫 Username already exists. Choose another.")
            else:
                hashed_pw = stauth.Hasher().hash([password])[0]
                users_ref.document(username).set({
                    "name": name,
                    "email": email,
                    "password": hashed_pw,
                    "roles": ["user"]
                })
                st.success("✅ Account created! You can now log in from the top.")
                st.session_state["show_register"] = False

st.markdown("""
This is your personalized learning system, with spaced repetition, XP leveling, and anime-powered global progress.

Choose a page from the sidebar to get started:
- 📘 Create subjects and study plans
- ✏️ Edit existing subjects, topics, or sections
- 📈 Track progress (coming soon)
""")
