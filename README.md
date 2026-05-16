# StudyTracker applications — CS665 Project 3

A full-stack study tracking application built with Python/Flask, SQLAlchemy, and SQLite.

---

## Project Description

StudyTracker is a web application that allows students and educators to track academic progress across multiple subjects. Users can log study sessions, monitor time spent, and view aggregate progress metrics through a summary dashboard.

**Who is it for?** Students managing multiple courses who want visibility into their study habits and progress.

---

## Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Language   | Python 3.10+                            |
| Framework  | Flask                                   |
| Database   | SQLite (default) / MySQL / PostgreSQL   |
| ORM        | SQLAlchemy (via Flask-SQLAlchemy)       |
| Frontend   | HTML5, CSS3, Bootstrap 5, Jinja2        |
| Version Control | Git                                |

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd studytracker
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///studytracker.db
```
If omitted, the app defaults to SQLite.

---

## Database Setup

### Option A — Automatic (SQLite, recommended for development)
The database is created automatically on first run. Sample seed data is inserted if the database is empty.

### Option B — Manual SQL schema
```bash
sqlite3 studytracker.db < schema.sql
```

### Option C — PostgreSQL or MySQL
Update `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/studytracker
DATABASE_URL=mysql+pymysql://user:password@localhost/studytracker
```

---

## Usage

### Start the development server
```bash
flask run
# or
python app.py
```

The app will be available at **http://127.0.0.1:5000**

### Navigating the app

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Aggregate stats and charts |
| Users | `/users` | View, add, edit, delete users |
| Subjects | `/subjects` | Manage course subjects |
| Study Sessions | `/sessions` | Log and review study sessions |

---

## Features

- **Multi-Table CRUD** across Users, Subjects, and Study_Sessions
- **One-to-Many relationships**: each User owns many Subjects; each Subject has many Sessions
- **SQL Transaction**: adding a session uses `db.session.flush()` + `db.session.commit()` ensuring atomicity
- **Server-side validation**: empty fields, invalid emails, negative durations, and out-of-range progress are all rejected
- **Summary Dashboard**: uses `COUNT`, `SUM`, and `AVG` aggregate functions

---

## Git Requirements

- Minimum 5 incremental commits
- `.gitignore` excludes `venv/`, `__pycache__/`, `.env`, and `*.db`

---

## Project Structure

```
studytracker/
├── app.py              # Flask routes and app factory
├── database.py         # SQLAlchemy models
├── seed.py             # Sample data seeder
├── schema.sql          # Raw SQL schema (3NF)
├── requirements.txt    # Python dependencies
├── .gitignore
├── README.md
├── NORMALIZATION.md    # 3NF normalization report
├── AI_LOG.md           # AI usage disclosure
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── users.html
    ├── user_form.html
    ├── subjects.html
    ├── subject_form.html
    ├── sessions.html
    └── session_form.html
```
