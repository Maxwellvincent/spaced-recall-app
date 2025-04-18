import streamlit as st
import json
import os
from login import run_login
from user_data import load_user_subjects, save_user_subjects

if "user" not in st.session_state:
    st.warning("⚠️ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)



SUBJECTS_FILE = "subjects.json"

def load_subjects():
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_subjects(subjects):
    with open(SUBJECTS_FILE, "w") as f:
        json.dump(subjects, f, indent=4)

def add_subject(name, style, sections=None):
    subjects = load_subjects()
    if name in subjects:
        return False

    subject_entry = {
        "study_style": style
    }

    if style == "exam_mode":
        subject_entry["sections"] = sections if sections else {}
        subject_entry["practice_scores"] = []

    save_subjects({**subjects, name: subject_entry})
    return True

# ==== Streamlit UI ====

st.title("📘 Add a New Study Subject")

subject_name = st.text_input("Enter subject name (e.g., Biology, MCAT, Literature)")

study_styles = {
    "Concept Mastery": "concept_mastery",
    "Exam Mode": "exam_mode",
    "Book Study": "book_study",
    "Reading Tracker": "reading",
    "Research Log": "research"
}

selected_style = st.selectbox("Choose study style", list(study_styles.keys()))
style_code = study_styles[selected_style]

sections_dict = {}

if style_code == "exam_mode":
    define_now = st.radio("Would you like to define sections now?", ["Yes", "No"])
    
    if define_now == "Yes":
        section_input = st.text_input("Enter section names (comma-separated):", placeholder="e.g. Biology, CARS, Psychology")

        if section_input:
            section_names = [sec.strip() for sec in section_input.split(",") if sec.strip()]
            for section in section_names:
                sec_style = st.selectbox(
                    f"Study style for '{section}':",
                    list(study_styles.keys()),
                    key=f"section_style_{section}"
                )
                sections_dict[section] = {
                    "study_style": study_styles[sec_style],
                    # Optionally initialize structure here
                    "topics" if study_styles[sec_style] == "concept_mastery" else "articles" if study_styles[sec_style] == "reading" else "books" if study_styles[sec_style] == "book_study" else "logs": []
                }

if st.button("Add Subject"):
    added = add_subject(subject_name, style_code, sections_dict if style_code == "exam_mode" and define_now == "Yes" else None)
    if added:
        st.success(f"✅ Added subject: {subject_name} ({selected_style})")
    else:
        st.warning(f"⚠️ Subject '{subject_name}' already exists.")

# Show current subject summary
st.markdown("---")
st.subheader("📚 Existing Subjects")

subjects = load_subjects()
if subjects:
    for subj, data in subjects.items():
        st.write(f"**{subj}** — Style: `{data.get('study_style', 'unknown')}`")
        if data.get("study_style") == "exam_mode":
            if "sections" in data and data["sections"]:
                st.write("Sections:")
                for sec in data["sections"]:
                    st.markdown(f"- `{sec}` → {data['sections'][sec]['study_style']}")
            else:
                st.markdown("*(No sections defined yet)*")
else:
    st.info("No subjects added yet.")
