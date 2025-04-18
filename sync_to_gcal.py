import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def authenticate_google():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def sync_reviews_to_calendar(service, subjects_path="subjects.json"):
    if not os.path.exists(subjects_path):
        print("❌ subjects.json not found.")
        return

    with open(subjects_path, "r") as f:
        subjects = json.load(f)

    count = 0
    for subj_name, subj in subjects.items():
        if subj.get("study_style") == "concept_mastery":
            for topic_name, topic in subj.get("topics", {}).items():
                add_topic_event(service, subj_name, topic_name, topic)

        elif subj.get("study_style") == "exam_mode":
            for section, sec_data in subj.get("sections", {}).items():
                if sec_data.get("study_style") == "concept_mastery":
                    for topic_name, topic in sec_data.get("topics", {}).items():
                        full_path = f"{subj_name} > {section}"
                        add_topic_event(service, full_path, topic_name, topic)
                        count += 1
    print(f"✅ Synced {count} review topics to Google Calendar.")

def add_topic_event(service, subject_path, topic_name, topic_data):
    review_date = topic_data.get("next_review")
    if not review_date:
        return

    start_time = datetime.datetime.fromisoformat(review_date).replace(hour=17, minute=0)
    end_time = start_time + datetime.timedelta(minutes=30)

    summary = f"📚 Review: {topic_name}"
    date_min = start_time.isoformat() + 'Z'
    date_max = end_time.isoformat() + 'Z'

    # Search for existing events
    events_result = service.events().list(
        calendarId='primary',
        timeMin=date_min,
        timeMax=date_max,
        q=summary,
        singleEvents=True
    ).execute()

    events = events_result.get('items', [])
    if events:
        print(f"⏭️ Skipped (already exists): {topic_name}")
        return

    # If no duplicate, insert the event
    event = {
        'summary': summary,
        'description': f"{subject_path} — Confidence: {topic_data.get('confidence', 0)}",
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/New_York'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/New_York'},
        'reminders': {
            'useDefault': False,
            'overrides': [{'method': 'popup', 'minutes': 10}]
        }
    }

    service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Synced: {topic_name}")



if __name__ == '__main__':
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    print("📤 Syncing review events from subjects.json...")
    sync_reviews_to_calendar(service)

