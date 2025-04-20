import streamlit as st
import json
import os
import pandas as pd
import calendar
from datetime import datetime, timedelta
#from gcal_sync import sync_reviews_to_calendar
from firebase_db import load_user_subjects, add_user_xp

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]
subjects = load_user_subjects(user)

st.set_page_config(page_title="Study Dashboard", layout="centered")
st.title("📊 Study Dashboard")
st.markdown(f"Welcome back, **{user}**!")
st.markdown("Here’s where you’ll see your XP progress, reviews due, and study activity.")

# === SYNC BUTTON ===
if st.button("🔄 Sync Reviews to Google Calendar"):
    with st.spinner("Syncing to Google Calendar..."):
        result = sync_reviews_to_calendar()
    st.success(result)

# === DATE LOGIC ===
today = datetime.now().date()
today_str = today.isoformat()
yesterday_str = (today - timedelta(days=1)).isoformat()
upcoming_range = [(today + timedelta(days=i)).isoformat() for i in range(1, 6)]

due_today = []
missed_yesterday = []
upcoming_reviews = []

def check_review_entry(parent, topic_data, topic_name):
    due = topic_data.get("next_review")
    if due == today_str:
        due_today.append((parent, topic_name))
    elif due == yesterday_str:
        missed_yesterday.append((parent, topic_name))
    elif due in upcoming_range:
        upcoming_reviews.append((parent, topic_name, due))

for subj_name, subj in subjects.items():
    if subj.get("study_style") == "concept_mastery":
        for topic_name, topic in subj.get("topics", {}).items():
            check_review_entry(subj_name, topic, topic_name)
    elif subj.get("study_style") == "exam_mode":
        for section, sec_data in subj.get("sections", {}).items():
            if sec_data.get("study_style") in ["concept_mastery", "subject_mastery"]:
                for topic_name, topic in sec_data.get("topics", {}).items():
                    full_path = f"{subj_name} > {section}"
                    check_review_entry(full_path, topic, topic_name)

# === DISPLAY REVIEWS ===
st.markdown("### 📅 Review Summary")

if due_today:
    st.markdown("#### 🔁 Due Today")
    for parent, topic in due_today:
        st.markdown(f"- **{topic}** from *{parent}*")
else:
    st.success("✅ No reviews due today!")

if missed_yesterday:
    st.markdown("#### ❌ Missed Yesterday")
    for parent, topic in missed_yesterday:
        st.markdown(f"- **{topic}** from *{parent}*")

if upcoming_reviews:
    st.markdown("#### 🔜 Upcoming Reviews")
    for parent, topic, due in upcoming_reviews:
        st.markdown(f"- **{topic}** from *{parent}* — Due: `{due}`")

# === SUBJECT SELECTOR ===
st.markdown("---")
selected_subject = st.selectbox("Choose a subject to view:", list(subjects.keys()))
subject_data = subjects[selected_subject]
style = subject_data.get("study_style", "unknown")
st.header(f"🧠 {selected_subject} — `{style}`")

# === EXAM MODE SECTION VIEW ===
if style == "exam_mode":
    st.subheader("📑 Sections")
    for section, sec_data in subject_data.get("sections", {}).items():
        sec_style = sec_data.get("study_style", "unknown")
        st.markdown(f"### 🔍 {section} — `{sec_style}`")

        if sec_style in ["concept_mastery", "subject_mastery"]:
            for topic, tdata in sec_data.get("topics", {}).items():
                st.markdown(f"- **{topic}** | Stage: {tdata.get('stage')} | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")
            st.markdown(f"[📝 Log Session](?subject={selected_subject})")


        elif sec_style == "reading":
            for a in sec_data.get("articles", []):
                st.markdown(f"- **{a['title']}** from *{a['source']}*")
            st.markdown(f"[📝 Log Session](?subject={selected_subject})")


        elif sec_style == "book_study":
            for b in sec_data.get("books", []):
                st.markdown(f"- **{b['title']}** by {b['author']}*")
            st.markdown(f"[📝 Log Session](?subject={selected_subject})")


        elif sec_style == "research":
            for log in sec_data.get("logs", []):
                st.markdown(f"- {log}")
            st.markdown(f"[📝 Log Session](?subject={selected_subject})")


# === SINGLE STUDY STYLE DISPLAY ===
elif style in ["concept_mastery", "subject_mastery"]:
    st.subheader("🧠 Topics")
    for topic, tdata in subject_data.get("topics", {}).items():
        st.markdown(f"- **{topic}** | Stage: {tdata.get('stage')} | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")
    st.markdown(f"[📝 Log Session](?subject={selected_subject})")


elif style == "book_study":
    st.subheader("📚 Books")
    for book in subject_data.get("books", []):
        st.markdown(f"- **{book['title']}** by {book['author']}")
    st.markdown(f"[📝 Log Session](?subject={selected_subject})")


elif style == "reading":
    st.subheader("📰 Articles")
    for article in subject_data.get("articles", []):
        st.markdown(f"- **{article['title']}** from *{article['source']}*")
    st.markdown(f"[📝 Log Session](?subject={selected_subject})")

