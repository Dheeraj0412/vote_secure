"""
routes/voter.py — Voter Blueprint
===================================
Routes available to authenticated (non-admin) users.

  GET  /voter/dashboard   – see candidates & voting status
  POST /voter/vote        – cast a vote (one per user, enforced at DB level too)
  GET  /voter/results     – read-only public results
"""

from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, session
)
from database import db
from models import Candidate, Vote, User

voter_bp = Blueprint("voter", __name__)


# ── Auth Guard ────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("is_admin"):
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ─────────────────────────────────────────────────────────
@voter_bp.route("/dashboard")
@login_required
def dashboard():
    user       = db.session.get(User, session["user_id"])
    candidates = Candidate.query.order_by(Candidate.name).all()
    return render_template("voter/dashboard.html",
                           user=user, candidates=candidates)


# ── Cast Vote ─────────────────────────────────────────────────────────
@voter_bp.route("/vote", methods=["POST"])
@login_required
def cast_vote():
    user = db.session.get(User, session["user_id"])

    # Double-check at application layer
    if user.has_voted():
        flash("You have already cast your vote.", "warning")
        return redirect(url_for("voter.dashboard"))

    candidate_id = request.form.get("candidate_id")
    if not candidate_id:
        flash("Please select a candidate.", "danger")
        return redirect(url_for("voter.dashboard"))

    candidate = db.session.get(Candidate, int(candidate_id))
    if not candidate:
        flash("Invalid candidate selected.", "danger")
        return redirect(url_for("voter.dashboard"))

    # DB-level unique constraint on user_id handles race conditions
    vote = Vote(user_id=user.id, candidate_id=candidate.id)
    db.session.add(vote)
    db.session.commit()

    flash(f'✅ Your vote for <strong>{candidate.name}</strong> has been recorded. Thank you!',
          "success")
    return redirect(url_for("voter.dashboard"))


# ── Public Results ────────────────────────────────────────────────────
@voter_bp.route("/results")
@login_required
def results():
    candidates  = Candidate.query.order_by(Candidate.name).all()
    total_votes = Vote.query.count()

    ranked = sorted(candidates, key=lambda c: c.vote_count, reverse=True)
    results_data = []
    for c in ranked:
        pct = round(c.vote_count / total_votes * 100, 1) if total_votes else 0
        results_data.append({
            "candidate": c,
            "votes": c.vote_count,
            "percentage": pct,
        })

    winner = ranked[0] if ranked and total_votes > 0 else None
    return render_template("voter/results.html",
                           results_data=results_data,
                           total_votes=total_votes,
                           winner=winner)
