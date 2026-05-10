from datetime import date
from database import User, Subject, StudySession

def seed_data(db):
    users = [
        User(user_id=1, name="Asha",  email="asha@email.com",  created_at=date(2024,1,1),  last_login=date(2024,2,1),  metadata_created_by="admin"),
        User(user_id=2, name="Brian", email="brian@email.com", created_at=date(2024,1,5),  last_login=date(2024,2,3),  metadata_created_by="super_admin"),
        User(user_id=3, name="Cathy", email="cathy@email.com", created_at=date(2024,1,10), last_login=date(2024,2,5),  metadata_created_by="system"),
        User(user_id=4, name="David", email="david@email.com", created_at=date(2024,1,15), last_login=date(2024,2,7),  metadata_created_by="system"),
        User(user_id=5, name="Emma",  email="emma@email.com",  created_at=date(2024,1,20), last_login=date(2024,2,10), metadata_created_by="admin"),
    ]
    db.session.add_all(users)
    db.session.flush()

    subjects = [
        Subject(subject_id=101, user_id=1, subject_name="Database Systems",  difficulty_level="Hard",   start_date=date(2024,2,1),  end_date=date(2024,6,1),  metadata_source="manual"),
        Subject(subject_id=102, user_id=2, subject_name="Python Programming", difficulty_level="Medium", start_date=date(2024,2,3),  end_date=date(2024,5,20), metadata_source="manual"),
        Subject(subject_id=103, user_id=3, subject_name="Statistics",         difficulty_level="Hard",   start_date=date(2024,2,5),  end_date=date(2024,5,25), metadata_source="imported"),
        Subject(subject_id=104, user_id=4, subject_name="Web Development",    difficulty_level="Easy",   start_date=date(2024,2,7),  end_date=date(2024,5,18), metadata_source="imported"),
        Subject(subject_id=105, user_id=5, subject_name="Machine Learning",   difficulty_level="Hard",   start_date=date(2024,2,10), end_date=date(2024,5,30), metadata_source="manual"),
    ]
    db.session.add_all(subjects)
    db.session.flush()

    sessions = [
        StudySession(session_id=1001, user_id=1, subject_id=101, session_date=date(2024,3,1), duration_minutes=120, topic_studied="ER Diagrams",         progress_percent=70.00, created_at=date(2024,3,1), metadata_tag="week1", study_hours=2.00),
        StudySession(session_id=1002, user_id=2, subject_id=102, session_date=date(2024,3,2), duration_minutes=90,  topic_studied="Loops and Functions",  progress_percent=60.00, created_at=date(2024,3,2), metadata_tag="week1", study_hours=1.50),
        StudySession(session_id=1003, user_id=3, subject_id=103, session_date=date(2024,3,3), duration_minutes=100, topic_studied="Probability Basics",   progress_percent=80.00, created_at=date(2024,3,3), metadata_tag="week1", study_hours=1.67),
        StudySession(session_id=1005, user_id=5, subject_id=105, session_date=date(2024,3,5), duration_minutes=140, topic_studied="Regression Models",    progress_percent=65.00, created_at=date(2024,3,5), metadata_tag="week1", study_hours=2.33),
    ]
    db.session.add_all(sessions)
    db.session.commit()
