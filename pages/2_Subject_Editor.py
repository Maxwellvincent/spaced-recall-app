import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects, add_user_xp
from datetime import datetime

if "user" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)

st.set_page_config(page_title="Subject Editor", layout="centered")
st.title("🛠️ Subject Editor")

if not subjects:
    st.warning("No subjects found. Create one first.")
    st.stop()

selected_subject = st.selectbox("Select a subject:", list(subjects.keys()))
subject_data = subjects[selected_subject]
style = subject_data.get("study_style", "unknown")

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
