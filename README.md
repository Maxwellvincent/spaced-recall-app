# Spaced Recall App 🧠⚡

A command-line spaced repetition tracker powered by [FSRS](https://github.com/open-spaced-repetition/fsrs4anki), personalized study stages, and **anime-themed global experience tracking** — for learners who want to level up like they're in Dragon Ball Z or Naruto.

---

## 🔑 Features

### 🗂️ Subject + Topic Based Reviews
- Organize by subject (e.g., Physics) and topic (e.g., Density)
- Tracks each topic’s review history and confidence level

### ⏳ FSRS-Based Review Scheduling
- Implements machine-learning-powered [Free Spaced Repetition Scheduler (FSRS)](https://github.com/open-spaced-repetition/fsrs4anki)
- Dynamically calculates your next review date based on memory decay models

### 🧠 Structured Study Stage Progression
- From Book Study → Notes → Mind Maps → Teaching
- Progression is **confidence-based**, not rigid — you control your pace

### 🎮 Gamification System
- Earn XP for each review (+ bonuses for confidence and stage progression)
- Each topic tracks:
  - XP, Level, Power Score
- Global tracker summarizes your growth across all subjects

### 🌍 Anime-Themed Global XP Tracker
Choose your theme:
- **Dragon Ball Z**: XP → Power Level
- **Naruto**: XP → Chakra + Sage Level
- **Neutral Mode**: Plain XP and Score

---

## 💾 Data Structure

- `review_log.json`: Stores per-topic logs and study metadata
- `global_profile.json`: Stores global XP, level, and anime theme progress

---

## 📦 Project Structure

spaced_recall_app/ ├── fsrs_model/ # FSRS logic ├── global_tracker.py # Global XP + theme progress ├── main.py # CLI logic for reviews ├── review_log.json # (local) topic progress ├── global_profile.json # (local) global progress ├── .gitignore └── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone and Install
```bash
git clone https://github.com/YOUR_USERNAME/spaced-recall-app.git
cd spaced-recall-app
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt  # (if requirements file used)
2. Run the App
bash
Copy
Edit
python main.py
You’ll be prompted to:

Enter a subject and topic

Rate your recall (Again → Easy)

Rate your confidence (0–10)

Watch your XP and Power grow 🎮

🛠️ Coming Soon
🌐 Streamlit dashboard interface

📊 Progress graphs + charts

🧠 Smart question engine (MCQs, FRQs, reasoning)

🏆 Badges, streaks, and unlockables

🧑‍🎓 Teaching Mode (write-your-own-summary quiz)

✨ Credits
FSRS scheduling from fsrs4anki

Built for learners who want to grow intelligently — one review at a time.

💬 Want to Contribute?
PRs and ideas welcome! Let's build the most fun and effective learning tracker on the planet.

yaml
Copy
Edit

---

### ✅ Next Steps:
- Save that into `README.md`
- Commit & push:
```bash
git add README.md
git commit -m "Update README with anime tracker and app features"
git push
