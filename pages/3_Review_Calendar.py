import streamlit as st
import pandas as pd
import calendar
import json
import os
from datetime import datetime
from login import run_login
from user_data import load_user_subjects, save_user_subjects

user = run_login()
subjects = load_user_subjects(user)



SUBJECTS_FILE = "subjects.json"

def load_subjects():
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            return json.load(f)
    return {}

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
    today = datetime.today()
    year, month = today.year, today.month
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.itermonthdays(year, month)

    data = []
    week = []
    for day in month_days:
        if day == 0:
            week.append("")  # padding
        else:
            date_str = datetime(year, month, day).date().isoformat()
            items = "\n".join(dates_dict.get(date_str, []))
            week.append(f"{day}\n{items}" if items else str(day))
        if len(week) == 7:
            data.append(week)
            week = []
    return pd.DataFrame(data, columns=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

# Main app
st.set_page_config(page_title="Review Calendar")
st.title("📆 Review Calendar")

subjects = load_subjects()
due_dates = collect_due_dates(subjects)
calendar_df = build_calendar_matrix(due_dates)

st.dataframe(calendar_df, use_container_width=True)
