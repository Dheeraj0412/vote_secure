"""
routes/auth.py — Authentication Blueprint
==========================================
Handles:
  POST /auth/register  – create a new voter account
  POST /auth/login     – log in (voter or admin)
  GET  /auth/logout    – destroy session
"""

from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, session
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

auth_bp = Blueprint("auth", __name__)


# ── Register ─────────────────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("voter.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # ── Validation ────────────────────────────────────────────
        errors = []
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        if not email or "@" not in email:
            errors.append("Enter a valid email address.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.query.filter_by(username=username).first():
            errors.append("Username already taken.")
        if User.query.filter_by(email=email).first():
            errors.append("Email already registered.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/register.html",
                                   username=username, email=email)

        # ── Create user ───────────────────────────────────────────
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ── Login ─────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        if session.get("is_admin"):
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("voter.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", username=username)

        # ── Populate session ──────────────────────────────────────
        session.clear()
        session["user_id"]  = user.id
        session["username"] = user.username
        session["is_admin"] = user.is_admin
        # Mark session as permanent so it survives across Render restarts
        session.permanent = True

        flash(f"Welcome back, {user.username}!", "success")
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("voter.dashboard"))

    return render_template("auth/login.html")


# ── Logout ────────────────────────────────────────────────────────────
@auth_bp.route("/logout")
def logout():
    username = session.get("username", "")
    session.clear()
    flash(f"Goodbye, {username}! You have been logged out.", "info")
    return redirect(url_for("auth.login"))
