import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.sqlite_db import get_connection

def check_overdue_followups():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("SELECT id FROM follow_up_tasks WHERE due_date < ? AND status = 'Pending'", (now,))
    overdue = cursor.fetchall()
    
    # Mark as overdue
    for row in overdue:
        cursor.execute("UPDATE follow_up_tasks SET status = 'Overdue' WHERE id = ?", (row['id'],))
    conn.commit()
    
    # Fetch all overdue for counting
    cursor.execute("SELECT * FROM follow_up_tasks WHERE status = 'Overdue'")
    overdue_tasks = cursor.fetchall()
    conn.close()
    return [dict(t) for t in overdue_tasks]

def auto_create_followup_task(institution_id, action, days_from_now):
    conn = get_connection()
    cursor = conn.cursor()
    due = (datetime.datetime.now() + datetime.timedelta(days=days_from_now)).isoformat()
    now = datetime.datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO follow_up_tasks (institution_id, task_type, description, due_date, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (institution_id, 'Auto', action, due, 'Pending', now))
    conn.commit()
    conn.close()

def log_status_change(institution_id, old_status, new_status):
    # Log to MongoDB if available
    from database.mongo_db import log_activity
    desc = f"Status changed from {old_status} to {new_status}"
    log_activity(institution_id, "StatusUpdate", desc)
