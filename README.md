# 🎓 BBDU Grievance Portal

> **Official Student Grievance & Complaint Management System** for Babu Banarasi Das University (BBDU).  
> Built with Django, Supabase PostgreSQL Cloud Database, Google OAuth 2.0, and modern responsive Vanilla CSS.

---

## 🌟 Overview

The **BBDU Grievance Portal** provides a centralized, transparent, and secure platform for students to raise concerns, track resolution progress in real time, and communicate with university department staff.

### ✨ Key Features

- **🔒 Restricted University Authentication**:
  - Unified **Student Portal** combining Sign In and Registration into a sleek tabbed interface.
  - Strict **`@bbdu.ac.in` email domain restriction** enforced across form validation and Google OAuth prompts (`hd: 'bbdu.ac.in'`).
  - Google SSO integration powered by Supabase Auth JS SDK.

- **📊 Dynamic Grievance Lifecycle & Progress Tracking**:
  - Automatic Complaint ID generation in the format `BBDU-YYYY-XXXXXX`.
  - Live progress timeline bar dynamically reflecting ticket status (`Submitted` ➔ `Under Review` ➔ `In Progress` ➔ `Resolved` / `Closed` / `Rejected`).

- **🏛️ Department-Scoped Access Control**:
  - **Student View**: Track personal grievances, view audit logs, file new complaints with attachments, and rate resolution quality.
  - **Department Staff View**: Staff members only see and process complaints assigned to their specific department (`Faculty / Teaching`, `Examination`, `Administration`, `Infrastructure`, `Hostel / Accommodation`, `Other`).
  - **Admin / Superuser View**: Oversee grievances across all university departments.

- **☁️ Supabase Cloud Database Real-time Sync**:
  - Production support for Supabase PostgreSQL.
  - Automated dual-sync via REST API (`supabase_sync.py`) so database updates, new complaints, and cloud deletions reflect live across the portal.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Django 6.1 (Python 3.13) |
| **Database** | Supabase Cloud PostgreSQL / SQLite (Local Fallback) |
| **Authentication** | Django Custom User Model & Supabase Auth (Google OAuth 2.0) |
| **Styling & UI** | Vanilla CSS, Google Font (*Plus Jakarta Sans*), Glassmorphism, Responsive Grid |
| **Database Connector** | `psycopg2-binary`, `python-dotenv`, `supabase-py` |

---

## 📁 Repository Structure

```
complaint-portal/
├── accounts/                  # Custom user model, auth views, student & staff login
│   ├── context_processors.py  # Global Supabase key context processor
│   ├── forms.py               # Student registration & domain validation
│   ├── models.py              # CustomUser model (STUDENT, STAFF, ADMIN)
│   ├── urls.py                # Auth routes & Supabase callback endpoint
│   └── views.py               # Student auth, staff login, & OAuth callback views
├── complaints/                # Grievances processing core
│   ├── forms.py               # Complaint submission & status update forms
│   ├── models.py              # Complaint, ComplaintStatusLog, Feedback models
│   ├── supabase_sync.py       # Cloud database real-time sync utility
│   ├── urls.py                # Landing, dashboard, detail, submission routes
│   └── views.py               # Landing page stats & department queue filtering
├── complaint_portal/          # Root Django settings & URL dispatchers
│   ├── settings.py            # Environment-driven database & auth settings
│   └── urls.py
├── static/css/main.css        # Central design system & aesthetic stylesheet
├── templates/                 # HTML5 Semantic Templates
│   ├── base.html              # Layout wrapper with navbar & dual-session logout
│   ├── landing.html           # Landing page with active status card & DB stats
│   ├── accounts/              # student_auth.html & staff_login.html
│   └── complaints/            # student_dashboard, staff_dashboard, submit, details
├── schema.sql                 # Supabase PostgreSQL DDL SQL DDL Script
├── migrate_to_supabase.py     # Automated Supabase provisioning script
├── seed_data.py               # Demo account & grievance seeding script
├── .env.example               # Environment settings template
└── README.md
```

---

## 🔑 Demo Login Credentials

You can test the live system locally using these pre-configured demo accounts:

### 👨‍💼 Staff & Admin Accounts ([Staff Login Portal](http://127.0.0.1:8000/accounts/staff-login/))

| Role | Username | Email | Password | Assigned Department |
| :--- | :--- | :--- | :--- | :--- |
| **Department Staff** | `staff` | `staff@bbdu.ac.in` | `staff123` | Faculty / Teaching |
| **Grievance Officer (Admin)** | `admin` | `admin@bbdu.ac.in` | `admin123` | All Departments (Superuser) |

### 🎓 Student Accounts ([Student Portal](http://127.0.0.1:8000/accounts/student/))

| Student Name | Username | Email | Password |
| :--- | :--- | :--- | :--- |
| **Adarsh Yadav** | `aegentfocks` | `aegentfocks@bbdu.ac.in` | `student123` |
| **Rahul Sharma** | `student` | `student@bbdu.ac.in` | `student123` |

---

## ⚡ Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone git@code.focks.github:manvisingh124/complaint-portal.git
cd complaint-portal
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Configuration (`.env`)
Create a `.env` file in the root directory (refer to `.env.example`):

```env
SECRET_KEY=django-insecure-bbdu-grievance-portal-key-super-secret
DEBUG=True
ALLOWED_HOSTS=*

# Supabase PostgreSQL Database Settings
USE_SUPABASE_DB=False
SUPABASE_DB_HOST=db.johefaiwcxvyyvbmkrxi.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_supabase_password
SUPABASE_DB_PORT=5432

# Supabase API & OAuth Credentials
SUPABASE_URL=https://johefaiwcxvyyvbmkrxi.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SECRET_KEY=your_supabase_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
```

### 4. Run Migrations & Seed Data
```bash
python manage.py migrate
python seed_data.py
```

### 5. Start Development Server
```bash
python manage.py runserver 8000
```
Open **[http://127.0.0.1:8000/complaints/](http://127.0.0.1:8000/complaints/)** in your browser!

---

## ☁️ Supabase Cloud Database Provisioning

To provision your Supabase PostgreSQL Cloud Database:

1. Open your **[Supabase SQL Editor](https://supabase.com/dashboard)**.
2. Copy the contents of [`schema.sql`](file:///d:/code/manvi-2/complaint-portal/schema.sql) and execute it to create all tables, indexes, and RLS policies.
3. Set `USE_SUPABASE_DB=True` and your `SUPABASE_DB_PASSWORD` in `.env`.
4. Run `python migrate_to_supabase.py` to push database schemas and seed records.

---

## 📜 License

This project is developed for **Babu Banarasi Das University (BBDU)** as an internal grievance & student complaint resolution system. All rights reserved.
