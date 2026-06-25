import sqlite3
import os
import sys

# Ensure config can be imported if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SQLITE_DB_PATH

def get_connection():
    # Use an absolute path for the DB based on the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, SQLITE_DB_PATH)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Institutions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            state TEXT,
            institution_type TEXT,
            student_strength INTEGER,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            program_interest TEXT,
            lead_source TEXT,
            lead_status TEXT,
            assigned_to TEXT,
            priority_score FLOAT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')

    # Follow-up Tasks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS follow_up_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution_id INTEGER,
            task_type TEXT,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT,
            FOREIGN KEY(institution_id) REFERENCES institutions(id)
        )
    ''')

    # Meetings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution_id INTEGER,
            scheduled_at TEXT,
            mode TEXT,
            agenda TEXT,
            outcome TEXT,
            created_at TEXT,
            FOREIGN KEY(institution_id) REFERENCES institutions(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_all_institutions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM institutions")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_institution(institution_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM institutions WHERE id = ?", (institution_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_institution_score(institution_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE institutions SET priority_score = ? WHERE id = ?", (score, institution_id))
    conn.commit()
    conn.close()
