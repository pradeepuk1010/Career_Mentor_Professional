import os
import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.environ.get("CAREER_MENTOR_DB", "career_mentor.db")

DEFAULT_PROFILE = {
    "name": "",
    "target_role": "Data Scientist",
    "stage": "Undergraduate",
    "weekly_hours": 6,
    "interests": "AI, Python, projects",
    "career_goal": "Build a strong portfolio and prepare for placements.",
    "skills": ["Python", "SQL"],
}

def connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                payload TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                due_date TEXT,
                notes TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wins TEXT, blockers TEXT, next_step TEXT,
                created_at TEXT NOT NULL
            )
        """)
        existing = conn.execute("SELECT payload FROM profile WHERE id=1").fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO profile(id,payload) VALUES(1,?)",
                (json.dumps(DEFAULT_PROFILE),)
            )

def get_profile():
    with connect() as conn:
        row = conn.execute("SELECT payload FROM profile WHERE id=1").fetchone()
        if not row:
            return DEFAULT_PROFILE.copy()
        data = json.loads(row["payload"])
        for key, value in DEFAULT_PROFILE.items():
            data.setdefault(key, value)
        return data

def save_profile(profile):
    payload = {**DEFAULT_PROFILE, **profile}
    with connect() as conn:
        conn.execute(
            "INSERT INTO profile(id,payload) VALUES(1,?) "
            "ON CONFLICT(id) DO UPDATE SET payload=excluded.payload",
            (json.dumps(payload),)
        )

def get_goals():
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM goals ORDER BY completed ASC, due_date ASC, id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

def add_goal(title, category, due_date, notes=""):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO goals(title,category,due_date,notes,completed,created_at) VALUES(?,?,?,?,0,?)",
            (title, category, due_date, notes, now)
        )
        return cur.lastrowid

def toggle_goal(goal_id, completed):
    with connect() as conn:
        conn.execute("UPDATE goals SET completed=? WHERE id=?", (int(completed), int(goal_id)))

def delete_goal(goal_id):
    with connect() as conn:
        conn.execute("DELETE FROM goals WHERE id=?", (int(goal_id),))

def add_reflection(wins, blockers, next_step):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with connect() as conn:
        conn.execute(
            "INSERT INTO reflections(wins,blockers,next_step,created_at) VALUES(?,?,?,?)",
            (wins, blockers, next_step, now)
        )

def get_reflections():
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM reflections ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]
