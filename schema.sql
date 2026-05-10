-- ============================================================
-- schema.sql — StudyTracker (3rd Normal Form)
-- CS665 Project 3
-- ============================================================

DROP TABLE IF EXISTS Study_Sessions;
DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Users;

-- ── Users ────────────────────────────────────────────────────
CREATE TABLE Users (
    user_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 VARCHAR(100) NOT NULL,
    email                VARCHAR(100) NOT NULL UNIQUE,
    created_at           DATE         NOT NULL,
    last_login           DATE,
    metadata_created_by  VARCHAR(50)
);

-- ── Subjects ─────────────────────────────────────────────────
CREATE TABLE Subjects (
    subject_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER      NOT NULL,
    subject_name     VARCHAR(100) NOT NULL,
    difficulty_level VARCHAR(20)  NOT NULL CHECK (difficulty_level IN ('Easy','Medium','Hard')),
    start_date       DATE         NOT NULL,
    end_date         DATE         NOT NULL,
    metadata_source  VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ── Study_Sessions ───────────────────────────────────────────
-- NOTE: study_hours is a cached computed column (duration_minutes / 60.0).
-- The transitive FD (session_id → duration_minutes → study_hours) is resolved
-- by always recalculating study_hours on every INSERT/UPDATE in the application.
-- See NORMALIZATION.md for full analysis.
CREATE TABLE Study_Sessions (
    session_id       INTEGER        PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER        NOT NULL,
    subject_id       INTEGER        NOT NULL,
    session_date     DATE           NOT NULL,
    duration_minutes INTEGER        NOT NULL CHECK (duration_minutes > 0),
    topic_studied    VARCHAR(150)   NOT NULL,
    progress_percent DECIMAL(5,2)   CHECK (progress_percent >= 0 AND progress_percent <= 100),
    created_at       DATE,
    metadata_tag     VARCHAR(50),
    study_hours      DECIMAL(5,2),  -- always = duration_minutes / 60.0
    FOREIGN KEY (user_id)    REFERENCES Users(user_id)    ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE CASCADE
);

-- ── Sample Data ──────────────────────────────────────────────
INSERT INTO Users (user_id, name, email, created_at, last_login, metadata_created_by) VALUES
(1, 'Asha',  'asha@email.com',  '2024-01-01', '2024-02-01', 'admin'),
(2, 'Brian', 'brian@email.com', '2024-01-05', '2024-02-03', 'super_admin'),
(3, 'Cathy', 'cathy@email.com', '2024-01-10', '2024-02-05', 'system'),
(4, 'David', 'david@email.com', '2024-01-15', '2024-02-07', 'system'),
(5, 'Emma',  'emma@email.com',  '2024-01-20', '2024-02-10', 'admin');

INSERT INTO Subjects (subject_id, user_id, subject_name, difficulty_level, start_date, end_date, metadata_source) VALUES
(101, 1, 'Database Systems',  'Hard',   '2024-02-01', '2024-06-01', 'manual'),
(102, 2, 'Python Programming','Medium', '2024-02-03', '2024-05-20', 'manual'),
(103, 3, 'Statistics',        'Hard',   '2024-02-05', '2024-05-25', 'imported'),
(104, 4, 'Web Development',   'Easy',   '2024-02-07', '2024-05-18', 'imported'),
(105, 5, 'Machine Learning',  'Hard',   '2024-02-10', '2024-05-30', 'manual');

-- Note: session_id 1004 (David / HTML Forms) was deleted per DML script
INSERT INTO Study_Sessions (session_id, user_id, subject_id, session_date, duration_minutes, topic_studied, progress_percent, created_at, metadata_tag, study_hours) VALUES
(1001, 1, 101, '2024-03-01', 120, 'ER Diagrams',        70.00, '2024-03-01', 'week1', 2.00),
(1002, 2, 102, '2024-03-02',  90, 'Loops and Functions',60.00, '2024-03-02', 'week1', 1.50),
(1003, 3, 103, '2024-03-03', 100, 'Probability Basics', 80.00, '2024-03-03', 'week1', 1.67),
(1005, 5, 105, '2024-03-05', 140, 'Regression Models',  65.00, '2024-03-05', 'week1', 2.33);
