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
