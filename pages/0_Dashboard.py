import streamlit as st
import json
import os
import pandas as pd
import calendar
from datetime import datetime, timedelta
# from gcal_sync import sync_reviews_to_calendar
from firebase_db import load_user_subjects

st.set_page_config(page_title="Study Dashboard", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]
subjects = load_user_subjects(user)

st.title("📊 Study Dashboard")
st.markdown(f"Welcome back, **{user}**!")

if not subjects:
    st.info("No subjects found yet. Create one to get started!")
    st.stop()

# === Filter bar ===
with st.expander("🔍 Filter Subjects"):
    filter_style = st.selectbox("Filter by Study Style", ["All"] + sorted({s.get("study_style") for s in subjects.values()}))
    filter_query = st.text_input("Search Subject Name")

# === Filter logic ===
def subject_matches(name, data):
    if filter_style != "All" and data.get("study_style") != filter_style:
        return False
    if filter_query and filter_query.lower() not in name.lower():
        return False
    return True

filtered_subjects = {name: data for name, data in subjects.items() if subject_matches(name, data)}

if not filtered_subjects:
    st.warning("No subjects match your filters.")
    st.stop()

# === Display all subjects with progress ===
for subject_name, subject_data in filtered_subjects.items():
    st.markdown(f"## 📘 {subject_name} — *{subject_data.get('study_style')}*")

    if subject_data.get("study_style") == "subject_mastery":
        topics = subject_data.get("topics", {})
        total_xp = sum(t.get("xp", 0) for t in topics.values())
        max_xp = len(topics) * 100 if topics else 1
        progress = int((total_xp / max_xp) * 100)
        st.progress(progress, text=f"Progress: {progress}%")

        with st.expander("Topics"):
            for topic_name, tdata in topics.items():
                st.markdown(f"- **{topic_name}** | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")

    elif subject_data.get("study_style") == "exam_mode":
        st.markdown("**Sections:**")
        for section_name, section_data in subject_data.get("sections", {}).items():
            sec_xp = section_data.get("xp", 0)
            topics = section_data.get("topics", {})
            max_xp = len(topics) * 100 if topics else 1
            progress = int((sec_xp / max_xp) * 100)
            with st.expander(f"📂 {section_name} — {section_data.get('study_style')}"):
                st.progress(progress, text=f"Progress: {progress}%")
                for topic_name, tdata in topics.items():
                    st.markdown(f"- **{topic_name}** | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")

    elif subject_data.get("study_style") == "reading":
        articles = subject_data.get("articles", [])
        st.markdown(f"Total Articles: {len(articles)}")

    elif subject_data.get("study_style") == "book_study":
        books = subject_data.get("books", [])
        st.markdown(f"Books Tracked: {len(books)}")

    elif subject_data.get("study_style") == "research":
        logs = subject_data.get("logs", [])
        st.markdown(f"Research Logs: {len(logs)}")
