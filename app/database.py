import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "placement_data.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id TEXT UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        branch TEXT NOT NULL,
        year TEXT NOT NULL,

        cgpa REAL NOT NULL,
        tenth_percentage REAL NOT NULL,
        twelfth_percentage REAL NOT NULL,
        backlogs INTEGER NOT NULL,
        attendance REAL NOT NULL,

        internships INTEGER NOT NULL,
        projects INTEGER NOT NULL,
        certifications INTEGER NOT NULL,

        coding_skill REAL NOT NULL,
        aptitude_score REAL NOT NULL,
        communication_skill REAL NOT NULL,
        technical_skill REAL NOT NULL,

        hackathons INTEGER NOT NULL,
        extracurricular_activities INTEGER NOT NULL,

        placement_training TEXT NOT NULL,
        mock_interview_score REAL NOT NULL,
        resume_score REAL NOT NULL,

        teamwork_skill REAL NOT NULL,
        leadership_skill REAL NOT NULL,
        problem_solving_skill REAL NOT NULL,
        logical_reasoning_score REAL NOT NULL,
        analytical_skill REAL NOT NULL,

        technical_training TEXT NOT NULL,
        work_experience INTEGER NOT NULL,
        career_guidance INTEGER NOT NULL,

        placement_status TEXT NOT NULL,
        salary_package REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()