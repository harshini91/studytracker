from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, User, Subject, StudySession
from datetime import date
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///studytracker.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Seed data if empty
    if not User.query.first():
        from seed import seed_data
        seed_data(db)

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@app.route("/")
def dashboard():
    from sqlalchemy import func
    total_users = User.query.count()
    total_subjects = Subject.query.count()
    total_sessions = StudySession.query.count()
    avg_progress = db.session.query(func.avg(StudySession.progress_percent)).scalar() or 0
    total_minutes = db.session.query(func.sum(StudySession.duration_minutes)).scalar() or 0

    # Top 3 subjects by session count
    top_subjects = (
        db.session.query(Subject.subject_name, func.count(StudySession.session_id).label("cnt"))
        .join(StudySession, Subject.subject_id == StudySession.subject_id)
        .group_by(Subject.subject_name)
        .order_by(func.count(StudySession.session_id).desc())
        .limit(3)
        .all()
    )

    # Monthly sessions
    monthly = (
        db.session.query(
            func.strftime("%m", StudySession.session_date).label("month"),
            func.count().label("cnt")
        )
        .group_by(func.strftime("%m", StudySession.session_date))
        .order_by("month")
        .all()
    )

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_subjects=total_subjects,
        total_sessions=total_sessions,
        avg_progress=round(float(avg_progress), 1),
        total_minutes=total_minutes,
        top_subjects=top_subjects,
        monthly=monthly,
    )

# ─────────────────────────────────────────────
# USERS CRUD
# ─────────────────────────────────────────────
@app.route("/users")
def users():
    all_users = User.query.order_by(User.user_id).all()
    return render_template("users.html", users=all_users)

@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        created_by = request.form.get("metadata_created_by", "").strip()

        # Validation
        if not name or not email:
            flash("Name and email are required.", "error")
            return redirect(url_for("add_user"))
        if "@" not in email:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("add_user"))
        if User.query.filter_by(email=email).first():
            flash("A user with that email already exists.", "error")
            return redirect(url_for("add_user"))

        user = User(name=name, email=email, created_at=date.today(),
                    last_login=date.today(), metadata_created_by=created_by or "manual")
        db.session.add(user)
        db.session.commit()
        flash(f"User '{name}' added successfully.", "success")
        return redirect(url_for("users"))
    return render_template("user_form.html", user=None)

@app.route("/users/edit/<int:uid>", methods=["GET", "POST"])
def edit_user(uid):
    user = User.query.get_or_404(uid)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email:
            flash("Name and email are required.", "error")
            return redirect(url_for("edit_user", uid=uid))
        if "@" not in email:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("edit_user", uid=uid))
        existing = User.query.filter_by(email=email).first()
        if existing and existing.user_id != uid:
            flash("That email is already in use.", "error")
            return redirect(url_for("edit_user", uid=uid))
        user.name = name
        user.email = email
        user.metadata_created_by = request.form.get("metadata_created_by", user.metadata_created_by).strip()
        db.session.commit()
        flash("User updated.", "success")
        return redirect(url_for("users"))
    return render_template("user_form.html", user=user)

@app.route("/users/delete/<int:uid>", methods=["POST"])
def delete_user(uid):
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.name}' deleted.", "success")
    return redirect(url_for("users"))

# ─────────────────────────────────────────────
# SUBJECTS CRUD
# ─────────────────────────────────────────────
@app.route("/subjects")
def subjects():
    all_subjects = Subject.query.join(User).order_by(Subject.subject_id).all()
    return render_template("subjects.html", subjects=all_subjects)

@app.route("/subjects/add", methods=["GET", "POST"])
def add_subject():
    users = User.query.order_by(User.name).all()
    if request.method == "POST":
        subject_name = request.form.get("subject_name", "").strip()
        difficulty = request.form.get("difficulty_level", "").strip()
        user_id = request.form.get("user_id")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        source = request.form.get("metadata_source", "manual").strip()

        if not subject_name or not difficulty or not user_id or not start_date or not end_date:
            flash("All fields are required.", "error")
            return render_template("subject_form.html", subject=None, users=users)
        if difficulty not in ("Easy", "Medium", "Hard"):
            flash("Invalid difficulty level.", "error")
            return render_template("subject_form.html", subject=None, users=users)
        if end_date < start_date:
            flash("End date must be after start date.", "error")
            return render_template("subject_form.html", subject=None, users=users)

        subj = Subject(user_id=int(user_id), subject_name=subject_name,
                       difficulty_level=difficulty, start_date=start_date,
                       end_date=end_date, metadata_source=source)
        db.session.add(subj)
        db.session.commit()
        flash(f"Subject '{subject_name}' added.", "success")
        return redirect(url_for("subjects"))
    return render_template("subject_form.html", subject=None, users=users)

@app.route("/subjects/edit/<int:sid>", methods=["GET", "POST"])
def edit_subject(sid):
    subj = Subject.query.get_or_404(sid)
    users = User.query.order_by(User.name).all()
    if request.method == "POST":
        subject_name = request.form.get("subject_name", "").strip()
        difficulty = request.form.get("difficulty_level", "").strip()
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        if not subject_name or not difficulty or not start_date or not end_date:
            flash("All fields are required.", "error")
            return render_template("subject_form.html", subject=subj, users=users)
        if difficulty not in ("Easy", "Medium", "Hard"):
            flash("Invalid difficulty level.", "error")
            return render_template("subject_form.html", subject=subj, users=users)
        if end_date < start_date:
            flash("End date must be after start date.", "error")
            return render_template("subject_form.html", subject=subj, users=users)
        subj.subject_name = subject_name
        subj.difficulty_level = difficulty
        subj.start_date = start_date
        subj.end_date = end_date
        subj.metadata_source = request.form.get("metadata_source", subj.metadata_source).strip()
        db.session.commit()
        flash("Subject updated.", "success")
        return redirect(url_for("subjects"))
    return render_template("subject_form.html", subject=subj, users=users)

@app.route("/subjects/delete/<int:sid>", methods=["POST"])
def delete_subject(sid):
    subj = Subject.query.get_or_404(sid)
    db.session.delete(subj)
    db.session.commit()
    flash(f"Subject '{subj.subject_name}' deleted.", "success")
    return redirect(url_for("subjects"))

# ─────────────────────────────────────────────
# STUDY SESSIONS CRUD
# ─────────────────────────────────────────────
@app.route("/sessions")
def sessions():
    all_sessions = StudySession.query.join(Subject).join(User).order_by(StudySession.session_date.desc()).all()
    return render_template("sessions.html", sessions=all_sessions)

@app.route("/sessions/add", methods=["GET", "POST"])
def add_session():
    users = User.query.order_by(User.name).all()
    subjects = Subject.query.order_by(Subject.subject_name).all()
    if request.method == "POST":
        user_id = request.form.get("user_id")
        subject_id = request.form.get("subject_id")
        session_date = request.form.get("session_date")
        duration = request.form.get("duration_minutes")
        topic = request.form.get("topic_studied", "").strip()
        progress = request.form.get("progress_percent")
        tag = request.form.get("metadata_tag", "").strip()

        errors = []
        if not all([user_id, subject_id, session_date, duration, topic, progress]):
            errors.append("All fields are required.")
        else:
            try:
                duration = int(duration)
                progress = float(progress)
                if duration <= 0:
                    errors.append("Duration must be a positive number.")
                if not (0 <= progress <= 100):
                    errors.append("Progress must be between 0 and 100.")
            except ValueError:
                errors.append("Duration and progress must be valid numbers.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("session_form.html", session=None, users=users, subjects=subjects)

        # TRANSACTION: create session and update study_hours atomically
        try:
            sess = StudySession(
                user_id=int(user_id), subject_id=int(subject_id),
                session_date=session_date, duration_minutes=duration,
                topic_studied=topic, progress_percent=progress,
                created_at=date.today(), metadata_tag=tag or "untagged",
                study_hours=round(duration / 60.0, 2)
            )
            db.session.add(sess)
            db.session.flush()   # get ID, still inside transaction
            # Could log to audit table here in extended version
            db.session.commit()
            flash("Study session logged successfully.", "success")
        except Exception as ex:
            db.session.rollback()
            flash(f"Transaction failed: {ex}", "error")
        return redirect(url_for("sessions"))
    return render_template("session_form.html", session=None, users=users, subjects=subjects)

@app.route("/sessions/edit/<int:sess_id>", methods=["GET", "POST"])
def edit_session(sess_id):
    sess = StudySession.query.get_or_404(sess_id)
    users = User.query.order_by(User.name).all()
    subjects = Subject.query.order_by(Subject.subject_name).all()
    if request.method == "POST":
        duration = request.form.get("duration_minutes")
        topic = request.form.get("topic_studied", "").strip()
        progress = request.form.get("progress_percent")
        errors = []
        try:
            duration = int(duration)
            progress = float(progress)
            if duration <= 0:
                errors.append("Duration must be positive.")
            if not (0 <= progress <= 100):
                errors.append("Progress must be 0–100.")
        except (ValueError, TypeError):
            errors.append("Invalid number values.")
        if not topic:
            errors.append("Topic is required.")
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("session_form.html", session=sess, users=users, subjects=subjects)
        sess.duration_minutes = duration
        sess.topic_studied = topic
        sess.progress_percent = progress
        sess.study_hours = round(duration / 60.0, 2)
        sess.metadata_tag = request.form.get("metadata_tag", sess.metadata_tag).strip()
        db.session.commit()
        flash("Session updated.", "success")
        return redirect(url_for("sessions"))
    return render_template("session_form.html", session=sess, users=users, subjects=subjects)

@app.route("/sessions/delete/<int:sess_id>", methods=["POST"])
def delete_session(sess_id):
    sess = StudySession.query.get_or_404(sess_id)
    db.session.delete(sess)
    db.session.commit()
    flash("Session deleted.", "success")
    return redirect(url_for("sessions"))

if __name__ == "__main__":
    app.run(debug=True)
