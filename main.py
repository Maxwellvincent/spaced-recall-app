import json
import os
from datetime import datetime
from fsrs_model.fsrs import FSRS
from fsrs_model.card import Card
from fsrs_model.log import Rating
from rich import print

from global_tracker import add_xp_to_global

fsrs = FSRS()
now = datetime.now()
REVIEW_LOG_FILE = "review_log.json"

STUDY_STAGES = [
    "Book Study + Note Creation",
    "Note Review",
    "Mind Map",
    "Mind Map Review",
    "Teaching / Self-Test",
    "Mastery Quiz"
]

XP_RULES = {
    "base_review": 10,
    "confidence_bonus": 5,
    "stage_up_bonus": 10
}

STAGE_MULTIPLIERS = {
    "Book Study + Note Creation": 1.0,
    "Note Review": 1.1,
    "Mind Map": 1.2,
    "Mind Map Review": 1.3,
    "Teaching / Self-Test": 1.5,
    "Mastery Quiz": 2.0
}

def get_level(xp):
    return (xp // 100) + 1

def calculate_power(xp, stage_name):
    multiplier = STAGE_MULTIPLIERS.get(stage_name, 1.0)
    return round(xp * multiplier, 1)

def load_logs():
    if os.path.exists(REVIEW_LOG_FILE):
        with open(REVIEW_LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_logs(logs):
    with open(REVIEW_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def save_log(subject, topic, reviewed_on, quality, next_review, logs):
    if subject not in logs:
        logs[subject] = {}

    if topic not in logs[subject]:
        logs[subject][topic] = {
            "stage": STUDY_STAGES[0],
            "book_study_done": False,
            "notes_done": False,
            "xp": 0,
            "level": 1,
            "power": 0,
            "reviews": []
        }

    logs[subject][topic]["reviews"].append({
        "reviewed_on": reviewed_on.strftime("%Y-%m-%d"),
        "quality": quality,
        "next_review": next_review.strftime("%Y-%m-%d")
    })

    return logs

def get_quality_rating():
    print("\n[bold blue]Rate your recall:[/bold blue]")
    print("[0] Again — couldn't recall")
    print("[1] Hard — barely remembered")
    print("[2] Good — remembered with some effort")
    print("[3] Easy — instantly knew it")

    while True:
        try:
            quality = int(input("Enter your score (0-3): "))
            if quality in [0, 1, 2, 3]:
                return quality
            else:
                print("Choose 0, 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Enter a number.")

def get_confidence():
    print("\n[bold magenta]Rate your confidence in this topic (0-10):[/bold magenta]")
    while True:
        try:
            score = int(input("Your score: "))
            if 0 <= score <= 10:
                return score
            else:
                print("Enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input.")

def update_book_and_note_status(logs, subject, topic):
    current = logs[subject][topic]
    if not current["book_study_done"]:
        answer = input("Have you finished the book study? (y/n): ").lower().strip()
        if answer == 'y':
            current["book_study_done"] = True

    if not current["notes_done"]:
        answer = input("Have you finished taking notes? (y/n): ").lower().strip()
        if answer == 'y':
            current["notes_done"] = True

def maybe_advance_stage(logs, subject, topic, confidence_score):
    current_data = logs[subject][topic]
    current_stage = current_data["stage"]
    stage_index = STUDY_STAGES.index(current_stage)
    advanced = False

    if current_stage == "Book Study + Note Creation":
        if current_data["book_study_done"] and current_data["notes_done"] and confidence_score >= 7:
            next_stage = STUDY_STAGES[stage_index + 1]
            logs[subject][topic]["stage"] = next_stage
            print(f"\n[bold green]Advanced to next study stage:[/] {next_stage}")
            advanced = True
        else:
            print(f"\n[bold yellow]Still in:[/] {current_stage}. Complete both tasks with confidence ≥ 7.")
    else:
        if confidence_score >= 7 and stage_index < len(STUDY_STAGES) - 1:
            next_stage = STUDY_STAGES[stage_index + 1]
            logs[subject][topic]["stage"] = next_stage
            print(f"\n[bold green]Advanced to next study stage:[/] {next_stage}")
            advanced = True
        else:
            print(f"\n[bold yellow]Remaining at:[/] {current_stage}")

    return advanced

def apply_xp(logs, subject, topic, confidence_score, stage_advanced):
    data = logs[subject][topic]

    if "xp" not in data:
        data["xp"] = 0
    if "level" not in data:
        data["level"] = 1
    if "power" not in data:
        data["power"] = 0

    base = XP_RULES["base_review"]
    bonus = XP_RULES["confidence_bonus"] if confidence_score >= 7 else 0
    stage_bonus = XP_RULES["stage_up_bonus"] if stage_advanced else 0
    total_xp = base + bonus + stage_bonus

    data["xp"] += total_xp
    data["level"] = get_level(data["xp"])
    data["power"] = calculate_power(data["xp"], data["stage"])

    print(f"\n[bold cyan]XP Gained:[/] {total_xp}")
    print(f"[bold cyan]Total XP:[/] {data['xp']} | [bold green]Level:[/] {data['level']} | [bold magenta]Power:[/] {data['power']}")

    # 🌍 Update global XP and show anime-style progress
    updated_global = add_xp_to_global(total_xp)
    print(f"\n[bold cyan]🌍 Global XP:[/] {updated_global['xp']} | [green]Global Level:[/] {updated_global['level']}")

    theme = updated_global['theme']
    if theme == "dbz":
        print(f"[yellow]🟡 Power Level:[/] {updated_global['progress']['dbz']['power_level']}")
    elif theme == "naruto":
        print(f"[blue]🔵 Chakra:[/] {updated_global['progress']['naruto']['chakra']} | Sage Level: {updated_global['progress']['naruto']['sage_level']}")
    else:
        print(f"[grey]⚪ Score:[/] {updated_global['progress']['neutral']['score']}")

# === MAIN APP START ===
print("[bold green]Spaced Recall Tracker + Study Stages + XP + Anime Progress[/bold green]")

subject = input("Enter the subject (e.g., Physics, Biology): ").strip()
topic = input("Enter the topic (e.g., Density, Circuits): ").strip()

logs = load_logs()
card = Card()
state = fsrs.get_recommended_state(card, now)
quality = get_quality_rating()

log = fsrs.create_log(card, state, now, Rating(quality))
card.review_log.append(log)

result = fsrs.repeat(card, state, now)
next_due = result.due

# Save review data
logs = save_log(subject, topic, now, quality, next_due, logs)
current_stage = logs[subject][topic]["stage"]
print(f"\n[bold cyan]Current study stage:[/] {current_stage}")

# Check for book/note progress
update_book_and_note_status(logs, subject, topic)
confidence = get_confidence()

# Evaluate stage advancement
stage_advanced = maybe_advance_stage(logs, subject, topic, confidence)

# XP, Power, and Global Profile Updates
apply_xp(logs, subject, topic, confidence, stage_advanced)

# Save everything
save_logs(logs)

print(f"\n[bold green]Next review in:[/] {next_due - now.date()} days on {next_due}")
