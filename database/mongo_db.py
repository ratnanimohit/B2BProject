import pymongo
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGO_URI, MONGO_DB_NAME

client = None

def get_client():
    global client
    if client is None:
        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            # Verify connection
            client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Warning: Could not connect to MongoDB. Ensure it's running if you need logs/activities.")
            client = None
    return client

def get_db():
    c = get_client()
    if c:
        return c[MONGO_DB_NAME]
    return None

def log_email(institution_id, subject, body, status="Sent"):
    db = get_db()
    if db is not None:
        import datetime
        db.email_logs.insert_one({
            "institution_id": institution_id,
            "subject": subject,
            "body": body,
            "sent_at": datetime.datetime.now(),
            "status": status
        })

def log_ai_output(institution_id, score, reasoning, next_action, outreach_msg):
    db = get_db()
    if db is not None:
        import datetime
        db.ai_outputs.insert_one({
            "institution_id": institution_id,
            "score": score,
            "reasoning": reasoning,
            "next_action": next_action,
            "outreach_msg": outreach_msg,
            "timestamp": datetime.datetime.now()
        })

def log_activity(institution_id, event_type, description):
    db = get_db()
    if db is not None:
        import datetime
        db.activity_feed.insert_one({
            "institution_id": institution_id,
            "event_type": event_type,
            "description": description,
            "timestamp": datetime.datetime.now()
        })
