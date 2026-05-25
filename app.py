"""
app.py — Main Flask Application
================================
Entry point for the Vote Secure Online Voting System.
Registers all blueprints, initialises PostgreSQL database,
and configures the Flask app for production on Render.
"""

from flask import Flask
from database import db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.voter import voter_bp
from routes.main import main_bp
import os


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod-2024")

    
    database_url = os.environ.get("DATABASE_URL", "sqlite:///voting.db")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,   
    }

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,  url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(voter_bp, url_prefix="/voter")

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Create the default admin account if it doesn't exist yet."""
    from models import User
    from werkzeug.security import generate_password_hash

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@votesys.com",
            password=generate_password_hash("Admin@123"),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        print("✅  Default admin created  →  admin / Admin@123")

from models import User, Candidate, Vote

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)

    db.init_app(app)
    with app.app_context():
        db.create_all()
