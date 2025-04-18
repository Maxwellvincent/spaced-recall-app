# gcal_sync.py
import datetime
import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

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

def sync_reviews_to_calendar():
    from datetime import datetime, timedelta

    if not os.path.exists("subjects.json"):
        return "❌ subjects.json not found."

    with open("subjects.json", "r") as f:
        subjects = json.load(f)

    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    count = 0
    for subj_name, subj in subjects.items():
        if subj.get("study_style") == "concept_mastery":
            for topic_name, topic in subj.get("topics", {}).items():
                if add_event(service, subj_name, topic_name, topic):
                    count += 1
        elif subj.get("study_style") == "exam_mode":
            for section, sec_data in subj.get("sections", {}).items():
                if sec_data.get("study_style") == "concept_mastery":
                    for topic_name, topic in sec_data.get("topics", {}).items():
                        full_path = f"{subj_name} > {section}"
                        if add_event(service, full_path, topic_name, topic):
                            count += 1
    return f"✅ {count} new events synced."

def add_event(service, subject_path, topic_name, topic_data):
    review_date = topic_data.get("next_review")
    if not review_date:
        return False

    start_time = datetime.fromisoformat(review_date).replace(hour=17, minute=0)
    end_time = start_time + timedelta(minutes=30)
    summary = f"📚 Review: {topic_name}"

    time_min = start_time.isoformat() + 'Z'
    time_max = end_time.isoformat() + 'Z'

    existing = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        q=summary,
        singleEvents=True
    ).execute().get('items', [])

    if existing:
        return False  # Already exists

    event = {
        'summary': summary,
        'description': f"{subject_path} — Confidence: {topic_data.get('confidence', 0)}",
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/New_York'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/New_York'},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]}
    }

    service.events().insert(calendarId='primary', body=event).execute()
    return True
