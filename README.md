# Spaced Recall App

A CLI-based spaced repetition logger with FSRS scheduling, study stage tracking, and confidence-based progression.

## 🔑 Features

- ✅ FSRS-based interval scheduling
- ✅ Structured study stage progression
- ✅ Logs quality of recall and confidence
- ✅ Transitions from Book Study → Teaching via confidence & completion
- 🔜 Future: XP, leveling system, Google Calendar, and question generator

## 📦 Structure

spaced_recall_app/ ├── fsrs_model/ # Local FSRS logic from GitHub ├── main.py # CLI interface ├── review_log.json # Dynamic log storage ├── .gitignore └── README.md


## 🚀 Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install rich
