import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
from gcal_sync import sync_reviews_to_calendar
from firebase_db import load_user_subjects

if "user" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)

st.title("📊 Dashboard")
st.markdown(f"Welcome back, **{user}**!")

if st.button("🔄 Sync Reviews to Google Calendar"):
    with st.spinner("Syncing to Google Calendar..."):
        result = sync_reviews_to_calendar()
    st.success(result)

today = datetime.now().date()
today_str = today.isoformat()
yesterday_str = (today - timedelta(days=1)).isoformat()
upcoming_range = [(today + timedelta(days=i)).isoformat() for i in range(1, 6)]

due_today, missed_yesterday, upcoming_reviews = [], [], []

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
            if sec_data.get("study_style") == "concept_mastery":
                for topic_name, topic in sec_data.get("topics", {}).items():
                    full_path = f"{subj_name} > {section}"
                    check_review_entry(full_path, topic, topic_name)

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
