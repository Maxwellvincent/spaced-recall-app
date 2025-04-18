import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects

if "user" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)

st.title("🆕 Create a New Subject")

with st.form("subject_form", clear_on_submit=True):
    name = st.text_input("Subject Name")
    study_style = st.selectbox("Choose a Study Style", [
        "concept_mastery", "exam_mode", "book_study", "reading", "research"
    ])
    submitted = st.form_submit_button("Add Subject")

    if submitted:
        if name in subjects:
            st.warning("This subject already exists.")
        else:
            subjects[name] = {"study_style": study_style}
            save_user_subjects(user, subjects)
            st.success(f"✅ Subject '{name}' added!")
