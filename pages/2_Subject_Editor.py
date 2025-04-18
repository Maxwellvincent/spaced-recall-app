import streamlit as st
import json
import os
from datetime import datetime
from login import run_login
from firebase_db import load_user_subjects, save_user_subjects, add_user_xp

if "user" not in st.session_state:
    st.warning("⚠️ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)

st.set_page_config(page_title="Subject Editor", layout="centered")
st.title("🛠️ Subject + Section Editor")

if not subjects:
    st.warning("No subjects found. Add one in the subject creator first.")
    st.stop()

selected_subject = st.selectbox("Select a subject to edit:", list(subjects.keys()))
subject_data = subjects[selected_subject]
style = subject_data.get("study_style", "unknown")

st.markdown(f"**Study Style:** `{style}`")

if style == "reading":
    st.subheader("📰 Add Article or CARS Passage")

    if "articles" not in subject_data:
        subject_data["articles"] = []

    with st.form("add_article_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            passage_number = st.text_input("Passage Number (e.g., 'Passage 7')")
            topic = st.text_input("Topic (e.g., Philosophy, Ethics)")
        with col2:
            title = st.text_input("Title (optional)")
            source = st.text_input("Source (e.g., AAMC FL 1, NY Review)")

        score_percentage = st.slider("Score Percentage", 0, 100, 80)
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add Entry")
        if submitted:
            new_article = {
                "title": title.strip(),
                "passage_number": passage_number.strip(),
                "topic": topic.strip(),
                "source": source.strip(),
                "score_percentage": score_percentage,
                "notes": notes.strip(),
                "date_read": datetime.today().date().isoformat()
            }
            subject_data["articles"].append(new_article)
            save_user_subjects(user, subjects)

            # XP system based on score
            xp_gain = 0
            if score_percentage >= 90:
                xp_gain = 10
            elif score_percentage >= 80:
                xp_gain = 8
            elif score_percentage >= 70:
                xp_gain = 6
            elif score_percentage >= 60:
                xp_gain = 4
            elif score_percentage >= 50:
                xp_gain = 2
            else:
                xp_gain = 1

            new_total_xp = add_user_xp(user, xp_gain)
            st.success(f"✅ Entry added! You gained {xp_gain} XP. Total XP: {new_total_xp}")

    if subject_data["articles"]:
        st.markdown("### 🧾 Your Reading Entries")
        for i, art in enumerate(subject_data["articles"], 1):
            st.markdown(f"**{i}. {art.get('passage_number', 'Article')}** — {art.get('topic', '')} from *{art.get('source', '')}*")
            st.markdown(f"• Title: {art.get('title', '-')}\n• Score: **{art.get('score_percentage', '-')}/100**\n• Notes: {art.get('notes', '-')}")
            st.markdown("---")
