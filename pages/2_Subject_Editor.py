import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects, add_user_xp
import pandas as pd
import calendar
from datetime import datetime

st.set_page_config(page_title="Subject Editor", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]

try:
    subjects = load_user_subjects(user)
except Exception as e:
    st.error(f"⚠️ Failed to load data for `{user}`. Error: {e}")
    st.stop()

st.title("🛠️ Subject Editor")

if not subjects:
    st.warning("No subjects found. Create one first.")
    st.stop()

selected_subject = st.selectbox("Select a subject:", list(subjects.keys()))
subject_data = subjects[selected_subject]
style = subject_data.get("study_style", "unknown")

# === ADD SECTION IF EXAM MODE ===
if style == "exam_mode":
    st.subheader("➕ Add Section to This Subject")

    with st.form("add_section_form", clear_on_submit=True):
        section_name = st.text_input("Section Name")
        section_style = st.selectbox("Section Study Style", [
            "subject_mastery", "reading", "book_study", "research"])
        submit_section = st.form_submit_button("Add Section")

        if submit_section:
            if "sections" not in subject_data:
                subject_data["sections"] = {}

            subject_data["sections"][section_name] = {
                "study_style": section_style,
                "topics": {} if section_style == "subject_mastery" else [],
                "xp": 0
            }
            save_user_subjects(user, subjects)
            st.success(f"✅ Section '{section_name}' added!")

# === ADD TOPICS IF SUBJECT MASTERY ===
if style == "subject_mastery":
    st.subheader("➕ Add Topics to Subject")
    with st.form("add_topic_form", clear_on_submit=True):
        topic_input = st.text_input("Enter topic name (e.g. Aldol Condensation)")
        add_topic = st.form_submit_button("Add Topic")

        if add_topic:
            if not topic_input:
                st.warning("⚠️ Please enter a topic name.")
            elif topic_input in subject_data.get("topics", {}):
                st.warning("⚠️ Topic already exists.")
            else:
                if "topics" not in subject_data:
                    subject_data["topics"] = {}

                subject_data["topics"][topic_input] = {
                    "stage": "book_review",
                    "xp": 0,
                    "confidence": 0
                }
                save_user_subjects(user, subjects)
                st.success(f"✅ Topic '{topic_input}' added to {selected_subject}.")

# === SHOW BASED ON STUDY STYLE ===
if style == "reading":
    st.subheader("📘 Add Reading or CARS Passage")

    if "articles" not in subject_data:
        subject_data["articles"] = []

    with st.form("add_article", clear_on_submit=True):
        title = st.text_input("Title (optional)")
        passage = st.text_input("Passage Number")
        topic = st.text_input("Topic")
        source = st.text_input("Source")
        score = st.slider("Score %", 0, 100, 80)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save")

        if submitted:
            new_entry = {
                "title": title,
                "passage_number": passage,
                "topic": topic,
                "source": source,
                "score_percentage": score,
                "notes": notes,
                "date_read": datetime.today().date().isoformat()
            }
            subject_data["articles"].append(new_entry)
            save_user_subjects(user, subjects)

            xp_gain = 10 if score >= 90 else 8 if score >= 80 else 6 if score >= 70 else 4 if score >= 60 else 2 if score >= 50 else 1
            total_xp = add_user_xp(user, xp_gain)
            st.success(f"✅ Added! +{xp_gain} XP (Total: {total_xp})")

# === UPDATE SECTION XP ON TOPIC CHANGE ===
if style == "exam_mode":
    st.subheader("📑 Section XP Overview")
    for section_name, sec_data in subject_data.get("sections", {}).items():
        if sec_data.get("study_style") == "subject_mastery":
            topics = sec_data.get("topics", {})
            section_xp = sum(t.get("xp", 0) for t in topics.values())
            sec_data["xp"] = section_xp
    save_user_subjects(user, subjects)
