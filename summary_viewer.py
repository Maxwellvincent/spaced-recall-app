import json
from datetime import datetime
from rich import print, box
from rich.table import Table

REVIEW_LOG_FILE = "review_log.json"

def load_logs():
    try:
        with open(REVIEW_LOG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[bold red]No log file found.[/bold red]")
        return {}

def get_days_until(date_str):
    try:
        next_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        days = (next_date - datetime.now().date()).days
        return f"{days} days" if days >= 0 else "Overdue"
    except:
        return "Unknown"

def show_summary(logs):
    for subject, topics in logs.items():
        print(f"\n[bold underline green]{subject}[/bold underline green]")

        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL)
        table.add_column("Topic", style="cyan", width=20)
        table.add_column("Stage", width=22)
        table.add_column("Level")
        table.add_column("XP")
        table.add_column("Power")
        table.add_column("Next Review", justify="center")

        for topic, data in topics.items():
            if isinstance(data, list):  # Skip old entries
                continue
            stage = data.get("stage", "Unknown")
            level = str(data.get("level", "N/A"))
            xp = str(data.get("xp", 0))
            power = str(data.get("power", 0))
            reviews = data.get("reviews", [])
            next_review = reviews[-1]["next_review"] if reviews else "N/A"
            next_in = get_days_until(next_review)

            table.add_row(topic, stage, level, xp, power, next_in)

        print(table)

if __name__ == "__main__":
    logs = load_logs()
    if logs:
        show_summary(logs)
