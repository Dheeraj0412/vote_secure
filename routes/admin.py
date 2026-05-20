"""
routes/admin.py — Admin Blueprint
===================================
All routes here require an active admin session.

  GET/POST /admin/dashboard          – overview stats
  GET/POST /admin/candidates/add     – add a candidate
  GET/POST /admin/candidates/<id>/edit
  POST     /admin/candidates/<id>/delete
  GET      /admin/results            – live vote tally
  GET      /admin/voters             – list of registered voters
"""

from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, session
)
from database import db
from models import Candidate, User, Vote

admin_bp = Blueprint("admin", __name__)


# ── Auth Guard ────────────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ─────────────────────────────────────────────────────────
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_voters     = User.query.filter_by(is_admin=False).count()
    total_candidates = Candidate.query.count()
    total_votes      = Vote.query.count()
    turnout = round((total_votes / total_voters * 100), 1) if total_voters else 0

    candidates = Candidate.query.order_by(Candidate.name).all()
    return render_template(
        "admin/dashboard.html",
        total_voters=total_voters,
        total_candidates=total_candidates,
        total_votes=total_votes,
        turnout=turnout,
        candidates=candidates,
    )


# ── Add Candidate ─────────────────────────────────────────────────────
@admin_bp.route("/candidates/add", methods=["GET", "POST"])
@admin_required
def add_candidate():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        party       = request.form.get("party", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not party:
            flash("Name and party are required.", "danger")
            return render_template("admin/candidate_form.html",
                                   action="Add", candidate=None)

        candidate = Candidate(name=name, party=party, description=description)
        db.session.add(candidate)
        db.session.commit()
        flash(f'Candidate "{name}" added successfully.', "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/candidate_form.html", action="Add", candidate=None)


# ── Edit Candidate ────────────────────────────────────────────────────
@admin_bp.route("/candidates/<int:cid>/edit", methods=["GET", "POST"])
@admin_required
def edit_candidate(cid):
    # db.session.get() is the SQLAlchemy 2.x recommended replacement for
    # the deprecated Model.query.get()
    candidate = db.session.get(Candidate, cid)
    if candidate is None:
        flash("Candidate not found.", "danger")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        candidate.name        = request.form.get("name", "").strip()
        candidate.party       = request.form.get("party", "").strip()
        candidate.description = request.form.get("description", "").strip()

        if not candidate.name or not candidate.party:
            flash("Name and party are required.", "danger")
            return render_template("admin/candidate_form.html",
                                   action="Edit", candidate=candidate)

        db.session.commit()
        flash("Candidate updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/candidate_form.html",
                           action="Edit", candidate=candidate)


# ── Delete Candidate ──────────────────────────────────────────────────
@admin_bp.route("/candidates/<int:cid>/delete", methods=["POST"])
@admin_required
def delete_candidate(cid):
    candidate = db.session.get(Candidate, cid)
    if candidate is None:
        flash("Candidate not found.", "danger")
        return redirect(url_for("admin.dashboard"))

    if candidate.votes:
        flash("Cannot delete a candidate who has already received votes.", "warning")
        return redirect(url_for("admin.dashboard"))

    db.session.delete(candidate)
    db.session.commit()
    flash(f'Candidate "{candidate.name}" removed.', "info")
    return redirect(url_for("admin.dashboard"))


# ── Election Results ──────────────────────────────────────────────────
@admin_bp.route("/results")
@admin_required
def results():
    candidates   = Candidate.query.order_by(Candidate.name).all()
    total_votes  = Vote.query.count()
    total_voters = User.query.filter_by(is_admin=False).count()

    # Sort by votes descending for podium display
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

    return render_template(
        "admin/results.html",
        results_data=results_data,
        total_votes=total_votes,
        total_voters=total_voters,
        winner=winner,
    )


# ── Voters List ───────────────────────────────────────────────────────
@admin_bp.route("/voters")
@admin_required
def voters():
    voters = (
        User.query
        .filter_by(is_admin=False)
        .order_by(User.created_at.desc())
        .all()
    )
    return render_template("admin/voters.html", voters=voters)
