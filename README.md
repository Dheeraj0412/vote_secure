# 🗳️ VoteSecure — Online Voting System

A complete, beginner-friendly Online Voting System built with **Flask**, **SQLite**, and **Bootstrap 5**.  
Designed as a learning project for CS students — structured like a real-world application.

---

## 📁 Project Structure

```
voting_system/
│
├── app.py                  ← Main Flask app (factory function)
├── database.py             ← SQLAlchemy db instance
├── models.py               ← User, Candidate, Vote models
├── requirements.txt        ← Python dependencies
│
├── routes/
│   ├── __init__.py
│   ├── main.py             ← Public landing page
│   ├── auth.py             ← Register / Login / Logout
│   ├── admin.py            ← Admin dashboard & candidate management
│   └── voter.py            ← Voter dashboard, cast vote, results
│
├── templates/
│   ├── base.html           ← Shared layout (navbar, flash, footer)
│   ├── index.html          ← Landing page
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── candidate_form.html
│   │   ├── results.html
│   │   └── voters.html
│   └── voter/
│       ├── dashboard.html
│       └── results.html
│
└── static/
    ├── css/style.css       ← Complete design system
    └── js/main.js          ← UI enhancements
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone / download the project
cd voting_system

# 2. Create a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

The app will be live at **http://127.0.0.1:5000**

---

## 🔑 Default Admin Account

| Field    | Value          |
|----------|----------------|
| Username | `admin`        |
| Password | `Admin@123`    |

> ⚠️ Change this in production! Edit `_seed_admin()` in `app.py`.

---

## ✅ Features

| Feature                  | Details                                                |
|--------------------------|--------------------------------------------------------|
| **User Registration**    | Username + email + bcrypt-hashed password              |
| **User Login / Logout**  | Session-based authentication                           |
| **Admin Panel**          | Separate admin interface, seeded on first run          |
| **Candidate Management** | Add, edit, delete candidates (can't delete if voted)   |
| **One Vote Per User**    | Enforced at both application AND database level        |
| **Live Results**         | Animated bar chart with vote counts and percentages    |
| **Voter Overview**       | Admin can see all voters and their voting status       |
| **Flash Messages**       | Success / error / info notifications throughout        |
| **Responsive UI**        | Bootstrap 5 — works on mobile and desktop              |
| **Session Handling**     | Secure server-side sessions with Flask's secret key    |
| **Error Handling**       | Input validation with clear, user-friendly messages    |

---

## 🗺️ URL Routes

### Public
| Route         | Description        |
|---------------|--------------------|
| `GET /`       | Landing page       |
| `GET/POST /auth/register` | User registration |
| `GET/POST /auth/login`    | User login        |
| `GET /auth/logout`        | Logout            |

### Voter (login required)
| Route                  | Description           |
|------------------------|-----------------------|
| `GET /voter/dashboard` | View candidates, vote |
| `POST /voter/vote`     | Cast a vote           |
| `GET /voter/results`   | View live results     |

### Admin (admin login required)
| Route                              | Description             |
|------------------------------------|-------------------------|
| `GET /admin/dashboard`             | Stats + candidate table |
| `GET/POST /admin/candidates/add`   | Add a candidate         |
| `GET/POST /admin/candidates/<id>/edit` | Edit candidate      |
| `POST /admin/candidates/<id>/delete`   | Delete candidate    |
| `GET /admin/results`               | Full election tally     |
| `GET /admin/voters`                | All registered voters   |

---

## 🔒 Security Notes

- Passwords hashed with **Werkzeug's** `generate_password_hash` (PBKDF2 / SHA-256).
- One-vote-per-user enforced by a **UNIQUE constraint** on `votes.user_id` (database level) + application-level check.
- Admin routes protected by `@admin_required` decorator.
- Voter routes protected by `@login_required` decorator.
- Change `SECRET_KEY` via environment variable in production.

---

## 🧑‍💻 How to Use

### As Admin
1. Go to `/auth/login` and sign in as `admin / Admin@123`
2. Add candidates via **Dashboard → Add Candidate**
3. Monitor votes in real time at **Results**
4. See voter participation at **Voters**

### As a Voter
1. Register at `/auth/register`
2. Log in and see all candidates
3. Select one and click **Submit My Vote**
4. View live results after voting

---

## 🎓 Learning Objectives

After studying this project, you will understand:

- **Flask Blueprints** — how to split a Flask app into logical modules
- **SQLAlchemy ORM** — defining models, relationships, and queries
- **Session Management** — storing user state securely
- **Password Hashing** — why plain-text passwords are dangerous
- **Decorator Patterns** — building `@login_required` / `@admin_required`
- **Flash Messages** — giving feedback without JavaScript
- **Template Inheritance** — Jinja2 `extends` / `block` system
- **Database Constraints** — enforcing business rules at the DB level

---

## 🛠️ Built With

- [Flask 3.0](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLite](https://sqlite.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Google Fonts — Syne & DM Sans](https://fonts.google.com/)
