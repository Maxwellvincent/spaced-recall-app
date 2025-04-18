import streamlit as st
st.set_page_config(page_title="Dashboard", layout="centered")  # MUST be first!

import pandas as pd
import calendar
from datetime import datetime, timedelta
from gcal_sync import sync_reviews_to_calendar
from firebase_db import load_user_subjects

# ✅ Check login session
if "user" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

# ✅ Get logged-in user
user = st.session_state["user"]

# ✅ Safe call to load data
try:
    subjects = load_user_subjects(user)
except Exception as e:
    st.error(f"⚠️ Failed to load data for `{user}`. Error: {e}")
    st.stop()

st.title("🆕 Create a New Subject")

with st.form("subject_form", clear_on_submit=True):
    name = st.text_input("Subject Name")
    study_style = st.selectbox("Choose a Study Style", [
        "concept_mastery", "exam_mode", "book_study", "reading", "research"
    ])
    submitted = st.form_submit_button("Add Subject")

    if submitted:
        if name in subjects:
            st.warning("This subject already exists.")
        else:
            subjects[name] = {"study_style": study_style}
            save_user_subjects(user, subjects)
            st.success(f"✅ Subject '{name}' added!")
