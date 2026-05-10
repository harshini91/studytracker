from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"
    user_id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name                = db.Column(db.String(100), nullable=False)
    email               = db.Column(db.String(100), nullable=False, unique=True)
    created_at          = db.Column(db.Date, nullable=False)
    last_login          = db.Column(db.Date)
    metadata_created_by = db.Column(db.String(50))

    subjects  = db.relationship("Subject",      back_populates="user", cascade="all, delete-orphan")
    sessions  = db.relationship("StudySession", back_populates="user", cascade="all, delete-orphan")


class Subject(db.Model):
    __tablename__ = "Subjects"
    subject_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    subject_name    = db.Column(db.String(100), nullable=False)
    difficulty_level= db.Column(db.String(20), nullable=False)
    start_date      = db.Column(db.Date, nullable=False)
    end_date        = db.Column(db.Date, nullable=False)
    metadata_source = db.Column(db.String(50))

    user     = db.relationship("User",         back_populates="subjects")
    sessions = db.relationship("StudySession", back_populates="subject", cascade="all, delete-orphan")


class StudySession(db.Model):
    __tablename__ = "Study_Sessions"
    session_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("Users.user_id"),    nullable=False)
    subject_id       = db.Column(db.Integer, db.ForeignKey("Subjects.subject_id"), nullable=False)
    session_date     = db.Column(db.Date,    nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    topic_studied    = db.Column(db.String(150), nullable=False)
    progress_percent = db.Column(db.Numeric(5, 2))
    created_at       = db.Column(db.Date)
    metadata_tag     = db.Column(db.String(50))
    study_hours      = db.Column(db.Numeric(5, 2))

    user    = db.relationship("User",    back_populates="sessions")
    subject = db.relationship("Subject", back_populates="sessions")
