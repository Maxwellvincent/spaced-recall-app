import streamlit as st
import pandas as pd
from firebase_db import db

st.set_page_config(page_title="Your Profile", layout="centered")

if "username" not in st.session_state:
    st.error("❌ Please log in first.")
    st.stop()

username = st.session_state["username"]
name = st.session_state.get("name", username)

st.title("🎮 Your Profile")

# === Load metadata ===
user_doc = db.collection("users_metadata").document(username).get()
if not user_doc.exists:
    st.warning("⚠️ No profile data found.")
    st.stop()

meta = user_doc.to_dict()
total_xp = db.collection("users").document(username).get().to_dict().get("xp", 0)

# === Character Theme ===
selected_theme = meta.get("theme", "DBZ")
character = meta.get("character", "Vegeta")
theme_tokens = meta.get("tokens", {"DBZ": 0, "Naruto": 0, "Neutral": 0})

# === Power Level Logic ===
def get_character_stage(theme, xp):
    if theme == "DBZ":
        if xp >= 1500:
            return "Ultra Ego Vegeta"
        elif xp >= 800:
            return "SSJ Blue Vegeta"
        elif xp >= 500:
            return "Majin Vegeta"
        elif xp >= 250:
            return "SSJ Vegeta"
        elif xp >= 100:
            return "Vegeta"
        else:
            return "Kid Vegeta"
    return "Training Mode"

stage = get_character_stage(selected_theme, total_xp)

st.image(f"https://dummyimage.com/256x256/000/fff&text={stage.replace(' ', '+')}", width=180)
st.markdown(f"### 🧑‍🎓 **{name}**  ")
st.markdown(f"**Theme**: {selected_theme} | **Character**: {character}  ")
st.markdown(f"**Power Stage**: `{stage}`  ")

st.progress(min(total_xp / 1500, 1.0), text=f"XP: {total_xp}/1500")

# === Theme Tokens ===
st.markdown("---")
st.subheader("🎟️ Tokens by Theme")
token_df = pd.DataFrame([theme_tokens]).T.reset_index()
token_df.columns = ["Theme", "Tokens"]
st.dataframe(token_df, hide_index=True, use_container_width=True)

# === Option to Switch Theme ===
st.markdown("---")
st.subheader("🎨 Switch Theme")
new_theme = st.selectbox("Choose your new theme:", ["DBZ", "Naruto", "Neutral"])

if st.button("Switch Theme"):
    db.collection("users_metadata").document(username).update({
        "theme": new_theme
    })
    st.success(f"✅ Theme switched to {new_theme}!")
    st.rerun()
