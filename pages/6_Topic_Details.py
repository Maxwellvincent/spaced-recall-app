import streamlit as st
from firebase_db import load_user_subjects, save_user_subjects, db

st.set_page_config(page_title="Topic Details", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]
subjects = load_user_subjects(user)

st.title("🔎 Topic Details & Mastery Path")

selected_subject = st.selectbox("Choose Subject", list(subjects.keys()))
subject_data = subjects[selected_subject]

if subject_data.get("study_style") != "subject_mastery":
    st.warning("⚠️ Only subject_mastery topics are supported here.")
    st.stop()

all_topics = list(subject_data.get("topics", {}).keys())
if not all_topics:
    st.info("This subject has no topics yet.")
    st.stop()

selected_topic = st.selectbox("Choose Topic", all_topics)
topic_data = subject_data["topics"][selected_topic]

st.subheader(f"🧠 {selected_topic}")
st.write(f"**XP:** {topic_data.get('xp', 0)}")
st.write(f"**Confidence:** {topic_data.get('confidence', 0)}")
st.write(f"**Stage:** {topic_data.get('stage', 'unknown')}")

# === Fetch Global Mastery Paths ===
st.markdown("---")
st.subheader("🔗 Link to Mastery Path")
paths_docs = list(db.collection("mastery_paths").stream())
path_names = [doc.to_dict().get("name") for doc in paths_docs if doc.exists()]
choices = ["None"] + sorted(set(path_names))

linked_path = topic_data.get("linked_path", "None")
selected_path = st.selectbox("Mastery Path", choices, index=choices.index(linked_path) if linked_path in choices else 0)

if st.button("💾 Save Changes"):
    if selected_path == "None":
        topic_data.pop("linked_path", None)
    else:
        topic_data["linked_path"] = selected_path

    save_user_subjects(user, subjects)
    st.success(f"✅ Mastery path updated for {selected_topic}")

# === Display Mastery Steps if linked ===
if selected_path != "None":
    st.markdown("---")
    st.subheader(f"📋 Steps in '{selected_path}'")
    for doc in paths_docs:
        data = doc.to_dict()
        if data.get("name") == selected_path:
            steps = data.get("steps", [])
            for i, step in enumerate(steps, 1):
                st.markdown(f"{i}. {step}")
            break
