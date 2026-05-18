"""
models.py — Database Models
=============================
Defines three tables:
  • User      – registered voters + admin accounts
  • Candidate – people standing for election
  • Vote      – immutable ballot records
"""

from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)          # bcrypt hash
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one: a user can cast only one vote
    vote = db.relationship("Vote", back_populates="voter", uselist=False)

    def has_voted(self):
        return self.vote is not None

    def __repr__(self):
        return f"<User {self.username}>"


class Candidate(db.Model):
    __tablename__ = "candidates"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    party       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Votes received
    votes = db.relationship("Vote", back_populates="candidate")

    @property
    def vote_count(self):
        return len(self.votes)

    def __repr__(self):
        return f"<Candidate {self.name}>"


class Vote(db.Model):
    __tablename__ = "votes"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"),      nullable=False, unique=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    cast_at      = db.Column(db.DateTime, default=datetime.utcnow)

    voter     = db.relationship("User",      back_populates="vote")
    candidate = db.relationship("Candidate", back_populates="votes")

    def __repr__(self):
        return f"<Vote user={self.user_id} → candidate={self.candidate_id}>"
