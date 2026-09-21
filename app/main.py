import os
import csv
import io
import sqlite3

import psycopg
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .database import init_db, get_connection


# ---------------------------------------------------------
# BASIC CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL uses %s
# SQLite uses ?
PLACEHOLDER = "%s" if DATABASE_URL else "?"


# ---------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------

app = FastAPI(
    title="Student Placement Data Collection System",
    version="2.0.0"
)


# ---------------------------------------------------------
# STARTUP
# ---------------------------------------------------------

@app.on_event("startup")
def startup():
    init_db()


# ---------------------------------------------------------
# HOME / DASHBOARD
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    conn = get_connection()

    total_row = conn.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()

    placed_row = conn.execute(
        "SELECT COUNT(*) AS count FROM students WHERE placement_status = 'Placed'"
    ).fetchone()

    if isinstance(total_row, dict):
        total = total_row["count"]
        placed = placed_row["count"]
    else:
        total = total_row[0]
        placed = placed_row[0]

    not_placed = total - placed

    conn.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "total": total,
            "placed": placed,
            "not_placed": not_placed
        }
    )


# ---------------------------------------------------------
# CREATE STUDENT RECORD
# ---------------------------------------------------------

@app.post("/students")
def create_student(

    student_id: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    branch: str = Form(...),
    year: str = Form(...),

    cgpa: float = Form(...),
    tenth_percentage: float = Form(...),
    twelfth_percentage: float = Form(...),
    backlogs: int = Form(...),
    attendance: float = Form(...),

    internships: int = Form(...),
    projects: int = Form(...),
    certifications: int = Form(...),

    coding_skill: float = Form(...),
    aptitude_score: float = Form(...),
    communication_skill: float = Form(...),
    technical_skill: float = Form(...),

    hackathons: int = Form(...),
    extracurricular_activities: int = Form(...),

    placement_training: str = Form(...),
    mock_interview_score: float = Form(...),
    resume_score: float = Form(...),

    teamwork_skill: float = Form(...),
    leadership_skill: float = Form(...),
    problem_solving_skill: float = Form(...),
    logical_reasoning_score: float = Form(...),
    analytical_skill: float = Form(...),

    technical_training: str = Form(...),
    work_experience: int = Form(...),
    career_guidance: int = Form(...),

    placement_status: str = Form(...),
    salary_package: str = Form("")
):

    # -----------------------------------------------------
    # SALARY
    # -----------------------------------------------------

    salary = (
        float(salary_package)
        if salary_package.strip()
        else None
    )


    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    data = (
        student_id.strip().upper(),
        age,
        gender,
        branch,
        year,

        cgpa,
        tenth_percentage,
        twelfth_percentage,
        backlogs,
        attendance,

        internships,
        projects,
        certifications,

        coding_skill,
        aptitude_score,
        communication_skill,
        technical_skill,

        hackathons,
        extracurricular_activities,

        placement_training,
        mock_interview_score,
        resume_score,

        teamwork_skill,
        leadership_skill,
        problem_solving_skill,
        logical_reasoning_score,
        analytical_skill,

        technical_training,
        work_experience,
        career_guidance,

        placement_status,
        salary
    )


    # -----------------------------------------------------
    # COLUMN LIST
    # -----------------------------------------------------

    columns = """
        student_id,
        age,
        gender,
        branch,
        year,
        cgpa,
        tenth_percentage,
        twelfth_percentage,
        backlogs,
        attendance,
        internships,
        projects,
        certifications,
        coding_skill,
        aptitude_score,
        communication_skill,
        technical_skill,
        hackathons,
        extracurricular_activities,
        placement_training,
        mock_interview_score,
        resume_score,
        teamwork_skill,
        leadership_skill,
        problem_solving_skill,
        logical_reasoning_score,
        analytical_skill,
        technical_training,
        work_experience,
        career_guidance,
        placement_status,
        salary_package
    """


    # -----------------------------------------------------
    # PLACEHOLDERS
    # -----------------------------------------------------

    placeholders = ",".join(
        [PLACEHOLDER] * 32
    )


    # -----------------------------------------------------
    # INSERT QUERY
    # -----------------------------------------------------

    query = f"""
        INSERT INTO students ({columns})
        VALUES ({placeholders})
    """


    conn = get_connection()


    try:

        conn.execute(
            query,
            data
        )

        conn.commit()


    except sqlite3.IntegrityError:

        conn.close()

        return RedirectResponse(
            "/?error=duplicate",
            status_code=303
        )


    except psycopg.errors.UniqueViolation:

        conn.rollback()
        conn.close()

        return RedirectResponse(
            "/?error=duplicate",
            status_code=303
        )


    finally:

        try:
            conn.close()
        except Exception:
            pass


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return RedirectResponse(
        "/?success=1",
        status_code=303
    )


# ---------------------------------------------------------
# STUDENTS DATASET
# ---------------------------------------------------------

@app.get(
    "/students",
    response_class=HTMLResponse
)
def students(request: Request):

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        "students.html",
        {
            "request": request,
            "students": rows
        }
    )


# ---------------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------------

@app.get("/export")
def export_csv():

    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            student_id,
            age,
            gender,
            branch,
            year,
            cgpa,
            tenth_percentage,
            twelfth_percentage,
            backlogs,
            attendance,
            internships,
            projects,
            certifications,
            coding_skill,
            aptitude_score,
            communication_skill,
            technical_skill,
            hackathons,
            extracurricular_activities,
            placement_training,
            mock_interview_score,
            resume_score,
            teamwork_skill,
            leadership_skill,
            problem_solving_skill,
            logical_reasoning_score,
            analytical_skill,
            technical_training,
            work_experience,
            career_guidance,
            placement_status,
            salary_package
        FROM students
        ORDER BY id
    """)

    rows = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    conn.close()


    # -----------------------------------------------------
    # CREATE CSV
    # -----------------------------------------------------

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(columns)

    for row in rows:

        writer.writerow(
            [
                row[column]
                for column in columns
            ]
        )


    output.seek(0)


    # -----------------------------------------------------
    # DOWNLOAD CSV
    # -----------------------------------------------------

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=student_placement_dataset.csv"
        }
    )


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "running",
        "module": "Data Collection",
        "attributes": 32,
        "database": (
            "PostgreSQL"
            if DATABASE_URL
            else "SQLite"
        )
    }