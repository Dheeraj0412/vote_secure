# 🗳️ VoteSecure — Online Voting System

A secure and modular Online Voting System developed using **Flask**, **PostgreSQL**, and **Bootstrap 5**.  
This project demonstrates the implementation of authentication, role-based access control, database management, and responsive user interface design in a real-world web application environment.

The system allows registered users to cast a single vote securely while providing administrators with tools to manage candidates, monitor voter participation, and view election results in real time.

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Database Design](#-database-design)
- [Installation and Setup](#-installation-and-setup)
- [Application Routes](#-application-routes)
- [System Security](#-system-security)
- [Usage Guide](#-usage-guide)
- [Screenshots / Demo](#-screenshots--demo)
- [Learning Outcomes](#-learning-outcomes)
- [Future Improvements](#-future-improvements)
- [Conclusion](#-conclusion)
- [License](#-license)

---

# 📖 Project Overview

VoteSecure is a web-based voting platform designed for academic and learning purposes. The application simulates a real-world election system where authenticated users can vote for candidates, and administrators can manage election operations through a dedicated dashboard.

The project emphasizes:

- Secure authentication
- Database integrity
- Role-based authorization
- Modular Flask application structure
- Clean and responsive UI design

---

# ✨ Key Features

## User Authentication

- User registration with email and password
- Secure login/logout functionality
- Password hashing using PBKDF2 with SHA-256

## Voting System

- One vote allowed per registered user
- Real-time vote counting and result display
- Database-level vote validation

## Admin Dashboard

- Add, edit, and delete candidates
- Monitor voter participation
- View election statistics and live results

## User Experience

- Responsive Bootstrap 5 interface
- Flash notifications for user feedback
- Mobile-friendly design

## Security Features

- Session-based authentication
- Protected admin and voter routes
- Database constraints to prevent duplicate voting

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend programming language |
| Flask 3.0 | Web framework |
| Flask-SQLAlchemy | ORM and database management |
| PostgreSQL | Relational database |
| Bootstrap 5 | Frontend styling and responsive UI |
| Jinja2 | HTML templating engine |
| Werkzeug Security | Password hashing and authentication |

---

# 🏗️ Project Architecture

```text
voting_system/
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
│
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── admin.py
│   └── voter.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── admin/
│   └── voter/
│
└── static/
    ├── css/style.css
    └── js/main.js
```

---

# 🗄️ Database Design

The system uses three primary database models:

| Model | Description |
|--------|-------------|
| User | Stores voter and administrator information |
| Candidate | Stores candidate details |
| Vote | Stores voting records and enforces one vote per user |

## Relationships

- One user can cast only one vote
- One candidate can receive multiple votes
- Votes are linked using foreign key relationships

---

# ⚙️ Installation and Setup

## Prerequisites

Ensure the following software is installed:

- Python 3.10 or higher
- PostgreSQL
- pip (Python package manager)
- Git (optional)

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/votesecure.git
cd votesecure
```

---

## Step 2 — Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure PostgreSQL Database

Create a PostgreSQL database and update the database URI in your Flask configuration.

Example configuration:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost/votesecure"
```

---

## Step 5 — Run the Application

```bash
python app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

---

# 🌐 Application Routes

## Public Routes

| Route | Description |
|--------|-------------|
| `/` | Landing page |
| `/auth/register` | User registration |
| `/auth/login` | User login |
| `/auth/logout` | User logout |

---

## Voter Routes

| Route | Description |
|--------|-------------|
| `/voter/dashboard` | View candidates and vote |
| `/voter/vote` | Submit vote |
| `/voter/results` | View election results |

---

## Admin Routes

| Route | Description |
|--------|-------------|
| `/admin/dashboard` | Admin dashboard |
| `/admin/candidates/add` | Add candidate |
| `/admin/candidates/<id>/edit` | Edit candidate |
| `/admin/candidates/<id>/delete` | Delete candidate |
| `/admin/results` | View complete election results |
| `/admin/voters` | View registered voters |

---

# 🔒 System Security

The application incorporates several security practices commonly used in web applications:

- Passwords are hashed using Werkzeug security utilities
- User sessions are securely managed through Flask sessions
- Administrative routes are protected using custom decorators
- Duplicate voting is prevented using:
  - Application-level validation
  - Database-level unique constraints
- Sensitive configuration values should be stored using environment variables

---

# 👨‍💻 Usage Guide

## Administrator Access

Administrator accounts can manage candidates, monitor voters, and access election statistics through the admin dashboard.

### Administrator Capabilities

- Manage election candidates
- Monitor registered voters
- View live election statistics
- Track voting participation

---

## Voter Access

### Steps for Voting

1. Register a new account
2. Log in to the system
3. Open the voter dashboard
4. Select a candidate
5. Submit the vote
6. View live election results

---

# 🖼️ Screenshots / Demo

Add screenshots of the following pages here:

- Landing Page
- Login & Registration
- Voter Dashboard
- Admin Dashboard
- Live Results Page

Example:

```markdown
![Landing Page](screenshots/home.png)
```

---

# 🎓 Learning Outcomes

This project demonstrates practical understanding of:

- Flask Blueprints and modular application design
- SQLAlchemy ORM relationships and queries
- Authentication and authorization systems
- Session management in web applications
- Password hashing and web security
- Database constraints and integrity enforcement
- Jinja2 template inheritance
- Responsive frontend development using Bootstrap 5
- PostgreSQL database integration and management

---

# 🚀 Future Improvements

Possible enhancements for future versions include:

- Email verification system
- OTP-based authentication
- Election scheduling and deadlines
- Graphical analytics dashboard
- REST API integration
- Docker container deployment
- MySQL database support
- Role-based permission management

---

# 📌 Conclusion

VoteSecure is a structured and secure online voting application developed to demonstrate full-stack web development concepts using Flask. The project combines backend logic, database design, authentication, and frontend responsiveness into a single practical system suitable for academic learning and portfolio demonstration.

---

# 📄 License

This project is intended for educational and academic purposes only.
