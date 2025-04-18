import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from firebase_db import load_user_subjects

if "user" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["user"]
subjects = load_user_subjects(user)
today = datetime.today().date()

st.title("📅 Review Calendar")

def collect_review_dates(subjects):
    review_dates = {}
    def add(date_str, label):
        if date_str:
            review_dates.setdefault(date_str, []).append(label)

    for subj_name, subj in subjects.items():
        if subj.get("study_style") == "concept_mastery":
            for topic, data in subj.get("topics", {}).items():
                add(data.get("next_review"), f"{subj_name}: {topic}")
        elif subj.get("study_style") == "exam_mode":
            for sec_name, sec in subj.get("sections", {}).items():
                if sec.get("study_style") == "concept_mastery":
                    for topic, data in sec.get("topics", {}).items():
                        full = f"{subj_name} > {sec_name}: {topic}"
                        add(data.get("next_review"), full)
    return review_dates

def build_calendar(review_dict):
    year, month = today.year, today.month
    cal = calendar.Calendar(firstweekday=6)
    days = cal.itermonthdays(year, month)
    matrix, week = [], []

    for day in days:
        if day == 0:
            week.append("")
        else:
            date_str = datetime(year, month, day).date().isoformat()
            entries = "\n".join(review_dict.get(date_str, []))
            week.append(f"{day}\n{entries}" if entries else str(day))
        if len(week) == 7:
            matrix.append(week)
            week = []

    return pd.DataFrame(matrix, columns=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

review_dict = collect_review_dates(subjects)
calendar_df = build_calendar(review_dict)
st.dataframe(calendar_df, use_container_width=True)
