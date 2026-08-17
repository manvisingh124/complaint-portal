# Supabase Database & Google OAuth Client Setup Guide

This guide walks you through connecting your **BBDU Grievance Portal** to **Supabase PostgreSQL** and configuring **Google OAuth 2.0 Client Login** (restricted to `@bbdu.ac.in` emails).

---

## 1. Supabase PostgreSQL Database Setup

### Step 1.1: Create a Supabase Project
1. Go to [https://supabase.com](https://supabase.com) and sign in.
2. Click **New Project**, select your organization, and set:
   - **Name**: `BBDU Grievance Portal`
   - **Database Password**: Set a strong password (copy & save this password!).
   - **Region**: Select `South Asia (Mumbai)` or nearest region.

### Step 1.2: Obtain Database Connection Credentials
1. In your Supabase Dashboard, click **Project Settings** (gear icon) ➔ **Database**.
2. Scroll to **Connection Info**:
   - **Host**: `db.xxxxxxxxxxxx.supabase.co`
   - **Database name**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: The database password you created in Step 1.1.

### Step 1.3: Update your `.env` File
Open `d:\code\manvi-2\complaint-portal\.env` and set:

```env
USE_SUPABASE_DB=True
SUPABASE_DB_HOST=db.xxxxxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_actual_db_password
SUPABASE_DB_PORT=5432
```

### Step 1.4: Migrate Tables to Supabase
Run the following commands in your terminal:

```bash
python manage.py migrate
python seed_data.py
```

All your models (`CustomUser`, `Complaint`, `ComplaintStatusLog`, `Feedback`) will now live in your Supabase cloud database!

---

## 2. Google OAuth 2.0 Client Setup

### Step 2.1: Create Google OAuth Credentials
1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Go to **APIs & Services** ➔ **OAuth consent screen**:
   - User Type: Select **Internal** (if restricted to BBDU Google Workspace) or **External**.
   - App Name: `BBDU Grievance Portal`
   - User support email: `your-email@bbdu.ac.in`
4. Go to **APIs & Services** ➔ **Credentials**:
   - Click **+ Create Credentials** ➔ **OAuth client ID**.
   - Application type: **Web application**.
   - Name: `BBDU Portal Web Client`.
   - **Authorized JavaScript origins**:
     - `http://127.0.0.1:8000`
     - `https://xxxxxxxxxxxx.supabase.co` (replace with your Supabase URL)
   - **Authorized redirect URIs**:
     - `https://xxxxxxxxxxxx.supabase.co/auth/v1/callback`
     - `http://127.0.0.1:8000/accounts/student/`
5. Click **Create** and copy your:
   - **Client ID** (e.g. `xxxxxxxx.apps.googleusercontent.com`)
   - **Client Secret**

---

## 3. Enable Google Provider in Supabase Auth

1. Go to your **Supabase Dashboard** ➔ **Authentication** ➔ **Providers**.
2. Find **Google** in the provider list and click to edit:
   - Toggle **Enable Google provider** to `ON`.
   - **Client ID**: Paste your Google Client ID.
   - **Client Secret**: Paste your Google Client Secret.
3. Click **Save**.

### Step 3.1: Enforce `@bbdu.ac.in` Domain Restriction in Supabase
In Supabase Dashboard ➔ **Authentication** ➔ **URL Configuration** / **Auth Settings**:
- Add `bbdu.ac.in` to **Allowed Email Domains** (or leave configured in Django form validation).

---

## 4. Environment Variables Checklist (`.env`)

Your final `d:\code\manvi-2\complaint-portal\.env` should look like:

```env
SECRET_KEY=django-insecure-bbdu-grievance-portal-key-super-secret
DEBUG=True
ALLOWED_HOSTS=*

# Supabase DB
USE_SUPABASE_DB=True
SUPABASE_DB_HOST=db.xxxxxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_actual_db_password
SUPABASE_DB_PORT=5432

# Supabase API & OAuth
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1Ni...
GOOGLE_CLIENT_ID=xxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxx
```
