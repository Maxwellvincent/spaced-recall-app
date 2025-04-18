import json
import os

SUBJECTS_FILE = "subjects.json"

def load_subjects():
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_subjects(subjects):
    with open(SUBJECTS_FILE, "w") as f:
        json.dump(subjects, f, indent=4)

def list_subjects(subjects):
    return list(subjects.keys())

def add_subject(name, style):
    subjects = load_subjects()
    if name in subjects:
        print(f"Subject '{name}' already exists.")
        return
    subjects[name] = {
        "study_style": style
    }
    save_subjects(subjects)
    print(f"Added subject: {name} ({style})")

def print_subject_summary(subjects):
    for name, data in subjects.items():
        print(f"📘 {name} — Style: {data.get('study_style', 'N/A')}")
