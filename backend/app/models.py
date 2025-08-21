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
