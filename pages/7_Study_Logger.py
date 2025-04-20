import streamlit as st
from urllib.parse import parse_qs
from firebase_db import load_user_subjects, save_user_subjects, add_user_xp, db
from datetime import datetime, timedelta
from gcal_sync import add_event_to_calendar

st.set_page_config(page_title="📚 Study Session Logger", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]
subjects = load_user_subjects(user)

# === Parse URL Params ===
query_params = st.query_params.to_dict()
selected_subject = query_params.get("subject")
selected_section = query_params.get("section")

if not selected_subject or selected_subject not in subjects:
    st.warning("No subject selected or invalid.")
    st.stop()

subject_data = subjects[selected_subject]
section_data = None

if subject_data.get("study_style") == "exam_mode":
    if not selected_section or selected_section not in subject_data.get("sections", {}):
        st.warning("No section selected or invalid.")
        st.stop()
    section_data = subject_data["sections"][selected_section]
else:
    selected_section = None
    section_data = subject_data

st.title("📘 Log Study Session")
st.markdown(f"**Subject:** {selected_subject}")
if selected_section:
    st.markdown(f"**Section:** {selected_section}")

# === Load Mastery Path for effort type ===
effort_options = ["Reading + Notes", "Mind Map", "Quiz/Review", "Teaching", "Practice Exam"]
linked_path = section_data.get("linked_path") or section_data.get("mastery_path")

if linked_path:
    all_paths = list(db.collection("mastery_paths").stream())
    for doc in all_paths:
        path_data = doc.to_dict()
        if path_data.get("name") == linked_path:
            effort_options = path_data.get("steps", effort_options)
            break

# === Study Session Form ===
with st.form("log_study_session"):
    minutes = st.number_input("Minutes Studied", min_value=5, max_value=360, step=5)
    effort_type = st.selectbox("Effort Type", effort_options)
    journal = st.text_area("Notes / Reflections")
    confirm = st.checkbox("✅ I confirm this session is complete")
    submit = st.form_submit_button("Submit Session")

    if submit and confirm:
        now = datetime.now()
        session = {
            "timestamp": now.isoformat(),
            "minutes": minutes,
            "effort_type": effort_type,
            "notes": journal
        }

        logs = section_data.get("logs", [])
        logs.append(session)
        section_data["logs"] = logs

        # XP Calculation
        effort_multiplier = effort_options.index(effort_type) + 1
        time_weight = minutes / 30
        xp_gain = int(10 * effort_multiplier * time_weight)

        section_data["xp"] = section_data.get("xp", 0) + xp_gain
        add_user_xp(user, xp_gain)
        save_user_subjects(user, subjects)

        st.success(f"✅ Session logged. +{xp_gain} XP awarded!")

        # Schedule next review 2-3 days later (example FSRS placeholder)
        next_review = now + timedelta(days=2)
        title = f"Review: {selected_section or selected_subject}"
        description = f"Spaced review for: {selected_subject} / {selected_section or 'Topic'}"
        add_event_to_calendar(title, description, next_review)

        st.success("📆 Google Calendar event added for next review!")
        st.balloons()
        st.rerun()
    elif submit:
        st.warning("You must confirm completion before submitting.")
