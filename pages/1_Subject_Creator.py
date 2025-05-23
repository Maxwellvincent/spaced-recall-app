import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects

st.set_page_config(page_title="Create New Subject", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]

st.title("📘 Create a New Subject")

# === Load existing subjects ===
subjects = load_user_subjects(user)

# === Subject Creation Form ===
with st.form("create_subject_form"):
    subject_name = st.text_input("Subject Name (e.g. Organic Chemistry)")
    study_style = st.selectbox("Study Style", ["subject_mastery", "exam_mode", "reading", "book_study", "research"])

    subtopics_input = st.text_area("Optional: Add initial subtopics or sections (comma-separated)", placeholder="e.g. Anki, CARS, Biology")

    submit = st.form_submit_button("Create Subject")

    if submit:
        if not subject_name:
            st.warning("⚠️ Please enter a subject name.")
        elif subject_name in subjects:
            st.warning("⚠️ That subject already exists.")
        else:
            subitems = [s.strip() for s in subtopics_input.split(",") if s.strip()]

            if study_style == "subject_mastery":
                topic_dict = {name: {"stage": "book_review", "xp": 0, "confidence": 0} for name in subitems}
                subjects[subject_name] = {
                    "study_style": study_style,
                    "topics": topic_dict
                }

            elif study_style == "exam_mode":
                section_dict = {}
                for name in subitems:
                    section_dict[name] = {
                        "study_style": "subject_mastery",  # default nested style
                        "topics": {},
                        "xp": 0,
                        "activity_type": "anki" if name.lower() == "anki" else "standard"
                    }
                subjects[subject_name] = {
                    "study_style": study_style,
                    "sections": section_dict
                }

            elif study_style == "reading":
                subjects[subject_name] = {
                    "study_style": study_style,
                    "articles": []
                }
            elif study_style == "book_study":
                subjects[subject_name] = {
                    "study_style": study_style,
                    "books": []
                }
            elif study_style == "research":
                subjects[subject_name] = {
                    "study_style": study_style,
                    "logs": []
                }

            save_user_subjects(user, subjects)
            st.success(f"✅ Created subject: {subject_name}")
