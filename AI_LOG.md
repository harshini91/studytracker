# AI_LOG.md — Generative AI Disclosure

This file documents all instances of Generative AI assistance used in this project, as required by the CS665 Project 3 AI Policy.

---

## Entry 1

| Field | Details |
|-------|---------|
| **Tool** | Claude (Anthropic) — claude.ai |
| **Date** | 2025 |
| **Prompt** | Provided the full DDL, DML, and DQL code for a StudyTracker database (Users, Subjects, Study_Sessions tables) and asked for a complete full-stack Flask project including: Flask routes with CRUD, SQLAlchemy models, Jinja2 templates, normalization report, README.md, AI_LOG.md, and schema.sql. |
| **AI Output Summary** | Claude generated: `app.py` with full CRUD routes and transaction logic, `database.py` with SQLAlchemy ORM models, `seed.py` for sample data, all 8 HTML templates (base, dashboard, users/subjects/sessions list and form pages) with a dark-mode design system using CSS variables and Bootstrap 5, `NORMALIZATION.md` identifying the `study_hours` transitive dependency, `README.md` with install/setup instructions, `schema.sql`, `requirements.txt`, and `.gitignore`. |
| **Your Modifications** | Verified all SQLAlchemy model column types matched the original SQL schema exactly. Confirmed the transitive dependency analysis in NORMALIZATION.md was accurate for our specific schema. Tested all routes manually. Adjusted seed data to match the exact records from the DML script (including the deleted session_id=1004). Verified the transaction logic in `add_session()` correctly uses `db.session.flush()` before `commit()`. |

---

## Entry 2 (if applicable — fill in for any subsequent AI assistance)

| Field | Details |
|-------|---------|
| **Tool** | |
| **Date** | |
| **Prompt** | |
| **AI Output Summary** | |
| **Your Modifications** | |

---

*Note: All AI-generated code was reviewed, tested, and verified against the specific database structure before inclusion in the final submission.*
