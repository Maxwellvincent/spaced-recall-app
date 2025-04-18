import json
import os

DATA_DIR = "user_data"

def get_user_file(username):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{username}.json")

def load_user_subjects(username):
    filepath = get_user_file(username)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_user_subjects(username, subjects):
    filepath = get_user_file(username)
    with open(filepath, "w") as f:
        json.dump(subjects, f, indent=4)
