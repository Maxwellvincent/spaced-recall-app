import streamlit as st
import json
from firebase_db import db

st.set_page_config(page_title="Create Mastery Path", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

user = st.session_state["username"]

st.title("🎯 Mastery Progression Builder")
st.markdown("Define a custom path for mastering a topic. Or reuse one from the global library.")

# === Search existing global mastery paths ===
all_paths = db.collection("mastery_paths").stream()
global_paths = []

for doc in all_paths:
    data = doc.to_dict()
    global_paths.append({"name": data.get("name"), "steps": data.get("steps", []), "source": data.get("created_by", "Unknown")})

with st.expander("🔍 Browse Global Progressions"):
    for path in global_paths:
        st.markdown(f"**{path['name']}** — by `{path['source']}`")
        for i, step in enumerate(path['steps'], 1):
            st.markdown(f"{i}. {step}")
        if st.button(f"Use '{path['name']}'", key=f"use_{path['name']}"):
            st.session_state["preloaded_steps"] = path['steps']
            st.success(f"✔️ Loaded '{path['name']}' into editor below.")

# === Build your own ===
st.markdown("---")
st.subheader("🛠️ Build Your Progression")

progression_name = st.text_input("Progression Name", value="")
custom_steps = st.session_state.get("preloaded_steps", [])

# Editable steps list
edited_steps = []
num_steps = len(custom_steps)
for i in range(num_steps):
    step = st.text_input(f"Step {i+1}", value=custom_steps[i], key=f"step_{i}")
    edited_steps.append(step)

if st.button("➕ Add New Step"):
    st.session_state.setdefault("preloaded_steps", []).append("New step")
    st.experimental_rerun()

if st.button("🚫 Clear All"):
    st.session_state["preloaded_steps"] = []
    st.experimental_rerun()

if st.button("✅ Save Progression"):
    if not progression_name or not edited_steps:
        st.warning("Please give a name and at least one step.")
    else:
        data = {
            "name": progression_name,
            "steps": edited_steps,
            "created_by": user
        }
        db.collection("mastery_paths").add(data)
        st.success(f"🎉 Saved '{progression_name}' to global library!")
        st.session_state["preloaded_steps"] = []
        st.rerun()
