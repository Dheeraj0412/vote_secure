"""
routes/main.py — Public Landing Page
======================================
Handles the root URL and any unauthenticated public pages.
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


# ── DB Viewer API Endpoints ────────────────────────────────────────────
# These power the db_viewer.html frontend tool
from flask import jsonify

@main_bp.route('/api/db/users')
def api_users():
    from models import User
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'is_admin': u.is_admin,
        'has_voted': u.has_voted(),
        'created_at': u.created_at.isoformat() if u.created_at else None
    } for u in users])


@main_bp.route('/api/db/candidates')
def api_candidates():
    from models import Candidate
    cands = Candidate.query.order_by(Candidate.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'party': c.party,
        'description': c.description,
        'vote_count': c.vote_count,
        'created_at': c.created_at.isoformat() if c.created_at else None
    } for c in cands])


@main_bp.route('/api/db/votes')
def api_votes():
    from models import Vote
    votes = Vote.query.order_by(Vote.cast_at.desc()).all()
    return jsonify([{
        'id': v.id,
        'voter_username': v.voter.username,
        'candidate_name': v.candidate.name,
        'candidate_party': v.candidate.party,
        'cast_at': v.cast_at.isoformat() if v.cast_at else None
    } for v in votes])
