import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
from gcal_sync import sync_reviews_to_calendar
from firebase_db import load_user_subjects

st.set_page_config(page_title="Dashboard", layout="wide")

# ✅ Check login
if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]
subjects = load_user_subjects(user)

st.title("📊 Study Dashboard")
st.markdown(f"Welcome back, **{st.session_state.get('name', user)}**! Track your progress below.")

# === XP Table View ===
if subjects:
    subject_rows = []
    section_rows = []

    for subj_name, subj_data in subjects.items():
        style = subj_data.get("study_style", "unknown")

        if style == "exam_mode":
            for section_name, sec in subj_data.get("sections", {}).items():
                xp = sec.get("xp", 0)
                topics = sec.get("topics", {})
                conf_avg = (
                    round(sum(t.get("confidence", 0) for t in topics.values()) / len(topics), 2)
                    if topics else 0
                )
                section_rows.append({
                    "Subject": subj_name,
                    "Section": section_name,
                    "XP": xp,
                    "Avg Confidence": conf_avg,
                    "Topics": len(topics)
                })
        else:
            topics = subj_data.get("topics", {})
            xp_total = sum(t.get("xp", 0) for t in topics.values())
            conf_avg = (
                round(sum(t.get("confidence", 0) for t in topics.values()) / len(topics), 2)
                if topics else 0
            )
            subject_rows.append({
                "Subject": subj_name,
                "Style": style,
                "XP": xp_total,
                "Avg Confidence": conf_avg,
                "Topics": len(topics)
            })

    # Display Subject Overview
    if subject_rows:
        st.subheader("📘 Subject Overview")
        df = pd.DataFrame(subject_rows)
        st.dataframe(df, use_container_width=True)

        for _, row in df.iterrows():
            st.markdown(f"**{row['Subject']}** — XP: {row['XP']} | Confidence: {row['Avg Confidence']}")
            st.progress(min(row['Avg Confidence'] / 10, 1.0))

    # Display Section Overview if available
    if section_rows:
        st.subheader("🧩 Section-Level Progress")
        section_df = pd.DataFrame(section_rows)
        st.dataframe(section_df, use_container_width=True)

        for _, row in section_df.iterrows():
            st.markdown(f"📖 **{row['Section']}** in *{row['Subject']}* — XP: {row['XP']} | Confidence: {row['Avg Confidence']}")
            st.progress(min(row['Avg Confidence'] / 10, 1.0))

else:
    st.warning("You have no subjects yet. Create one to begin tracking progress!")
