from datetime import datetime
from sqlalchemy import Index
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email_enc = db.Column(db.LargeBinary, nullable=False)
    email_hash = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    first_login_attempted = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (Index("ix_users_email_hash", "email_hash"),)

    def to_public(self, email_plain=None):
        return {
            "id": self.id,
            "email": email_plain if email_plain else None,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
            # optional: expose this for debugging/admin purposes
            # "first_login_attempted": self.first_login_attempted  
        }

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # "A", "B", "C", "D"

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class ExamSession(db.Model):
    __tablename__ = "exam_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    submitted = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", backref="exam_sessions")


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    exam_session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    chosen_option = db.Column(db.String(1), nullable=False)  # "A", "B", "C", "D"

    exam_session = db.relationship("ExamSession", backref="answers")
    question = db.relationship("Question")

class ExamQuestion(db.Model):
    __tablename__ = "exam_questions"
    id = db.Column(db.Integer, primary_key=True)
    exam_session_id = db.Column(db.Integer, db.ForeignKey("exam_sessions.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    exam_session = db.relationship("ExamSession", backref="exam_questions")
    question = db.relationship("Question")
