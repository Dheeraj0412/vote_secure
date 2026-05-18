"""
database.py — SQLAlchemy Instance
===================================
Single db object imported by app.py and all models.
Keeping it here breaks circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
