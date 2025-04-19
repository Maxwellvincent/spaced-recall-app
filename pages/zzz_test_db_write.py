import streamlit as st
from firebase_db import db
import datetime

st.set_page_config(page_title="DB Write Test")

st.title("🧪 Firestore Write Test")

if st.button("Write Test Data"):
    db.collection("debug_tests").document("test_doc").set({
        "message": "It works!",
        "timestamp": datetime.datetime.now().isoformat()
    })
    st.success("✅ Test data written to Firestore!")
