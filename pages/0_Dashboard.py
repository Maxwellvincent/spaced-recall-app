import streamlit as st
import json
import os
import pandas as pd
import calendar
from datetime import datetime, timedelta
from gcal_sync import sync_reviews_to_calendar
from login import run_login
from user_data import load_user_subjects, save_user_subjects

user = run_login()
subjects = load_user_subjects(user)



# === Load Subjects ===
SUBJECTS_FILE = "subjects.json"

def load_subjects():
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            return json.load(f)
    return {}

subjects = load_subjects()

st.set_page_config(page_title="Study Dashboard", layout="centered")
st.title("📊 Study Dashboard")

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
            if sec_data.get("study_style") == "concept_mastery":
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
    if "selected_section" not in st.session_state:
        for section, sec_data in subject_data.get("sections", {}).items():
            sec_style = sec_data.get("study_style", "unknown")
            if st.button(f"🔍 View '{section}' — {sec_style}", key=f"btn_{section}"):
                st.session_state["selected_section"] = section
                st.session_state["section_data"] = sec_data
                st.session_state["section_style"] = sec_style
                st.rerun()
    else:
        section = st.session_state["selected_section"]
        sec_data = st.session_state["section_data"]
        sec_style = st.session_state["section_style"]
        st.markdown("---")
        st.subheader(f"📂 Section: {section}")

        if sec_style == "concept_mastery":
            for topic, tdata in sec_data.get("topics", {}).items():
                st.markdown(f"- **{topic}** | Stage: {tdata.get('stage')} | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")
        elif sec_style == "reading":
            for a in sec_data.get("articles", []):
                st.markdown(f"- **{a['title']}** from *{a['source']}*")
        elif sec_style == "book_study":
            for b in sec_data.get("books", []):
                st.markdown(f"- **{b['title']}** by {b['author']}")
        elif sec_style == "research":
            for log in sec_data.get("logs", []):
                st.markdown(f"- {log}")

        st.button("🔙 Back to all sections", on_click=lambda: st.session_state.pop("selected_section"))

# === SINGLE STUDY STYLE DISPLAY ===
elif style == "concept_mastery":
    st.subheader("🧠 Topics")
    for topic, tdata in subject_data.get("topics", {}).items():
        st.markdown(f"- **{topic}** | Stage: {tdata.get('stage')} | XP: {tdata.get('xp')} | Confidence: {tdata.get('confidence')}")

elif style == "book_study":
    st.subheader("📚 Books")
    for book in subject_data.get("books", []):
        st.markdown(f"- **{book['title']}** by {book['author']}")

elif style == "reading":
    st.subheader("📰 Articles")
    for article in subject_data.get("articles", []):
        st.markdown(f"- **{article['title']}** from *{article['source']}*")

# === OPTIONAL CALENDAR VIEW ===
def collect_due_dates(subjects):
    review_dates = {}
    def add(date_str, label):
        if date_str:
            review_dates.setdefault(date_str, []).append(label)
    for subj_name, subj in subjects.items():
        if subj.get("study_style") == "concept_mastery":
            for topic_name, topic in subj.get("topics", {}).items():
                add(topic.get("next_review"), f"{subj_name}: {topic_name}")
        elif subj.get("study_style") == "exam_mode":
            for section, sec_data in subj.get("sections", {}).items():
                if sec_data.get("study_style") == "concept_mastery":
                    for topic_name, topic in sec_data.get("topics", {}).items():
                        full = f"{subj_name} > {section}: {topic_name}"
                        add(topic.get("next_review"), full)
    return review_dates

def build_calendar_matrix(dates_dict):
    year, month = today.year, today.month
    cal = calendar.Calendar(firstweekday=6)
    days = cal.itermonthdays(year, month)
    data, week = [], []
    for day in days:
        if day == 0:
            week.append("")
        else:
            date_str = datetime(year, month, day).date().isoformat()
            items = "\n".join(dates_dict.get(date_str, []))
            week.append(f"{day}\n{items}" if items else str(day))
        if len(week) == 7:
            data.append(week)
            week = []
    return pd.DataFrame(data, columns=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

st.markdown("---")
st.markdown("### 📆 Monthly Review Calendar")
calendar_df = build_calendar_matrix(collect_due_dates(subjects))
st.dataframe(calendar_df, use_container_width=True)
