import json
import os
from datetime import datetime
from fsrs_model.fsrs import FSRS
from fsrs_model.card import Card
from fsrs_model.log import Rating
from rich import print

fsrs = FSRS()
now = datetime.now()
REVIEW_LOG_FILE = "review_log.json"

STUDY_STAGES = [
    "Book Study + Note Creation",  # Stage 1 (parallel)
    "Note Review",
    "Mind Map",
    "Mind Map Review",
    "Teaching / Self-Test",
    "Mastery Quiz"
]

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

    if current_stage == "Book Study + Note Creation":
        if current_data["book_study_done"] and current_data["notes_done"] and confidence_score >= 7:
            next_stage = STUDY_STAGES[stage_index + 1]
            logs[subject][topic]["stage"] = next_stage
            print(f"\n[bold green]Advanced to next study stage:[/] {next_stage}")
        else:
            print(f"\n[bold yellow]Still in:[/] {current_stage}. Make sure both book study and notes are done with confidence ≥ 7.")
    else:
        if confidence_score >= 7 and stage_index < len(STUDY_STAGES) - 1:
            next_stage = STUDY_STAGES[stage_index + 1]
            logs[subject][topic]["stage"] = next_stage
            print(f"\n[bold green]Advanced to next study stage:[/] {next_stage}")
        else:
            print(f"\n[bold yellow]Remaining at:[/] {current_stage}")

# === MAIN APP START ===
print("[bold green]Spaced Recall Tracker + Study Stages[/bold green]")

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

# Save review
logs = save_log(subject, topic, now, quality, next_due, logs)

# Show stage and ask for status update
current_stage = logs[subject][topic]["stage"]
print(f"\n[bold cyan]Current study stage:[/] {current_stage}")

update_book_and_note_status(logs, subject, topic)
confidence = get_confidence()
maybe_advance_stage(logs, subject, topic, confidence)

# Save everything
save_logs(logs)

print(f"[bold green]Next review in:[/] {next_due - now.date()} days on {next_due}")
