import firebase_admin
import json
import streamlit as st
from firebase_admin import credentials, firestore

# === Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

# === Connect to Firestore
db = firestore.client()

# === SUBJECTS ===

def load_user_subjects(username):
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("subjects", {})
    return {}

def save_user_subjects(username, subjects_dict):
    doc_ref = db.collection("users").document(username)
    doc_ref.set({"subjects": subjects_dict}, merge=True)

# === XP SUPPORT ===

def add_user_xp(username, amount):
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()

    current = doc.to_dict() if doc.exists else {}
    current_xp = current.get("xp", 0)
    total_xp = current_xp + amount

    doc_ref.set({"xp": total_xp}, merge=True)
    return total_xp

def get_user_xp(username):
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("xp", 0)
    return 0
