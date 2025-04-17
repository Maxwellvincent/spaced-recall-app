import json
import os

GLOBAL_PROFILE_FILE = "global_profile.json"

DEFAULT_PROFILE = {
    "xp": 0,
    "level": 1,
    "theme": "dbz",  # Options: "dbz", "naruto", "neutral"
    "progress": {
        "dbz": {
            "power_level": 0
        },
        "naruto": {
            "chakra": 0,
            "sage_level": 1
        },
        "neutral": {
            "score": 0
        }
    }
}

def load_profile():
    if not os.path.exists(GLOBAL_PROFILE_FILE):
        save_profile(DEFAULT_PROFILE)
    with open(GLOBAL_PROFILE_FILE, "r") as f:
        return json.load(f)

def save_profile(profile):
    with open(GLOBAL_PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)

def choose_theme():
    print("\n[bold cyan]Choose your theme:[/bold cyan]")
    print("[1] Dragon Ball Z (Power Level)")
    print("[2] Naruto (Chakra & Sage Mode)")
    print("[3] Neutral (Score-based only)")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return "dbz"
        elif choice == "2":
            return "naruto"
        elif choice == "3":
            return "neutral"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def calculate_theme_progress(profile):
    xp = profile["xp"]
    theme = profile["theme"]

    if theme == "dbz":
        profile["progress"]["dbz"]["power_level"] = xp * 42

    elif theme == "naruto":
        profile["progress"]["naruto"]["chakra"] = xp * 2
        profile["progress"]["naruto"]["sage_level"] = (xp // 150) + 1

    elif theme == "neutral":
        profile["progress"]["neutral"]["score"] = xp

    profile["level"] = (xp // 100) + 1
    return profile

def add_xp_to_global(xp_gained):
    profile = load_profile()

    # Set theme if not already chosen
    if not profile.get("theme"):
        profile["theme"] = choose_theme()

    profile["xp"] += xp_gained
    updated = calculate_theme_progress(profile)
    save_profile(updated)

    return updated
