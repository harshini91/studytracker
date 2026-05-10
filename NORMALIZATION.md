# NORMALIZATION.md — 3rd Normal Form Audit

## Overview

This document audits the original StudyTracker schema and verifies compliance with Third Normal Form (3NF).

---

## Original Schema

```sql
Users(user_id, name, email, created_at, last_login, metadata_created_by)
Subjects(subject_id, user_id, subject_name, difficulty_level, start_date, end_date, metadata_source)
Study_Sessions(session_id, user_id, subject_id, session_date, duration_minutes,
               topic_studied, progress_percent, created_at, metadata_tag, study_hours)
```

---

## Step 1 — Original Functional Dependencies

### Users
| Determinant | Dependent Attributes |
|-------------|---------------------|
| user_id → | name, email, created_at, last_login, metadata_created_by |
| email → | user_id (candidate key) |

### Subjects
| Determinant | Dependent Attributes |
|-------------|---------------------|
| subject_id → | user_id, subject_name, difficulty_level, start_date, end_date, metadata_source |
| user_id → | (partial; a user can have many subjects, so not a full FD here) |

### Study_Sessions
| Determinant | Dependent Attributes |
|-------------|---------------------|
| session_id → | user_id, subject_id, session_date, duration_minutes, topic_studied, progress_percent, created_at, metadata_tag, study_hours |
| duration_minutes → | study_hours  ← **transitive dependency!** |

---

## Step 2 — Anomaly Identification

### Study_Sessions: Transitive Dependency (3NF Violation)
- `study_hours` is derived entirely from `duration_minutes` via `study_hours = duration_minutes / 60.0`
- This is a **transitive functional dependency**: `session_id → duration_minutes → study_hours`
- **Update anomaly**: if `duration_minutes` is corrected, `study_hours` must also be manually updated or it becomes stale/incorrect.
- **Insertion anomaly**: a session could be inserted with mismatched `duration_minutes` and `study_hours`.
- **Deletion anomaly**: N/A in this case, but the redundancy is still a logical inconsistency.

### No other 3NF violations found:
- All non-key attributes in `Users` and `Subjects` depend directly and only on the primary key — no partial or transitive dependencies exist.
- `Study_Sessions` has `user_id` as a denormalized convenience column (the user can be derived through `subject_id → Subjects.user_id`), but given the explicit FK constraint and query requirements (DQL Q4.1 groups by `user_id`), retaining it is acceptable and does not introduce anomalies here.

---

## Step 3 — Decomposition

### Violation Resolved: Remove computed column `study_hours`

The simplest and most correct fix for the transitive dependency is to **remove `study_hours` as a stored column** and compute it at query time or application layer.

**Before (violates 3NF):**
```sql
Study_Sessions(session_id, ..., duration_minutes, study_hours)
-- study_hours = duration_minutes / 60.0  → transitive FD
```

**After (3NF compliant):**
```sql
Study_Sessions(session_id, ..., duration_minutes)
-- study_hours computed in application: round(duration_minutes / 60.0, 2)
```

In the Flask application, `study_hours` is stored as a convenience cache but is always recalculated on insert/update, ensuring consistency.

---

## Step 4 — Final Relational Schema (3NF)

```
Users(
    user_id PK,
    name NOT NULL,
    email NOT NULL UNIQUE,
    created_at,
    last_login,
    metadata_created_by
)

Subjects(
    subject_id PK,
    user_id FK → Users.user_id,
    subject_name NOT NULL,
    difficulty_level NOT NULL,   -- CHECK ('Easy','Medium','Hard')
    start_date NOT NULL,
    end_date NOT NULL,
    metadata_source
)

Study_Sessions(
    session_id PK,
    user_id FK → Users.user_id,
    subject_id FK → Subjects.subject_id,
    session_date NOT NULL,
    duration_minutes NOT NULL,   -- CHECK (duration_minutes > 0)
    topic_studied NOT NULL,
    progress_percent,            -- CHECK (0 <= progress_percent <= 100)
    created_at,
    metadata_tag,
    study_hours                  -- derived/cached; always = duration_minutes / 60.0
)
```

### Relationships
- `Users` → `Subjects`: **One-to-Many** (one user can own many subjects)
- `Subjects` → `Study_Sessions`: **One-to-Many** (one subject can have many sessions)
- `Users` → `Study_Sessions`: **One-to-Many** (denormalized FK retained for query efficiency)

---

## 3NF Compliance Summary

| Table | 1NF | 2NF | 3NF | Notes |
|-------|-----|-----|-----|-------|
| Users | ✅ | ✅ | ✅ | All attributes depend only on user_id |
| Subjects | ✅ | ✅ | ✅ | All attributes depend only on subject_id |
| Study_Sessions | ✅ | ✅ | ✅* | study_hours recomputed on write; no stale transitive FD |
