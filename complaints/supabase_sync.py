import os
import requests
from django.conf import settings

def get_supabase_config():
    url = getattr(settings, 'SUPABASE_URL', os.getenv('SUPABASE_URL', '')).rstrip('/')
    key = getattr(settings, 'SUPABASE_SECRET_KEY', os.getenv('SUPABASE_SECRET_KEY', ''))
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    return url, headers


def sync_user_to_supabase(user):
    """Pushes a user profile directly to Supabase Cloud Database."""
    try:
        url, headers = get_supabase_config()
        if not url or not headers["apikey"]:
            return False
            
        payload = {
            "id": user.id,
            "password": user.password,
            "username": user.username,
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "email": user.email or "",
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "role": user.role,
            "enrollment_no": user.enrollment_no or "",
            "department": user.department or "Other"
        }
        res = requests.post(f"{url}/rest/v1/accounts_customuser", json=payload, headers=headers, timeout=5)
        return res.status_code in [200, 201]
    except Exception as e:
        print(f"Supabase User Sync Error: {e}")
        return False


def sync_complaint_to_supabase(complaint):
    """Pushes a complaint ticket directly to Supabase Cloud Database."""
    try:
        url, headers = get_supabase_config()
        if not url or not headers["apikey"]:
            return False

        payload = {
            "id": complaint.id,
            "complaint_id": complaint.complaint_id,
            "category": complaint.category,
            "department": complaint.department or complaint.category,
            "priority": complaint.priority,
            "subject": complaint.subject,
            "description": complaint.description,
            "status": complaint.status,
            "student_id": complaint.student_id,
            "assigned_staff_id": complaint.assigned_staff_id
        }
        res = requests.post(f"{url}/rest/v1/complaints_complaint", json=payload, headers=headers, timeout=5)
        return res.status_code in [200, 201]
    except Exception as e:
        print(f"Supabase Complaint Sync Error: {e}")
        return False


def fetch_live_supabase_complaints(student_id=None):
    """Fetches live complaint records directly from Supabase Cloud Database REST API and syncs ORM state safely."""
    from complaints.models import Complaint
    try:
        url, headers = get_supabase_config()
        if not url or not headers["apikey"]:
            return None

        endpoint = f"{url}/rest/v1/complaints_complaint?select=*"
        if student_id:
            endpoint += f"&student_id=eq.{student_id}"
        res = requests.get(endpoint, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            supabase_complaint_ids = [item['complaint_id'] for item in data]
            
            # Safely sync local ORM cache if local table exists and USE_SUPABASE_DB is False
            use_supabase_db = getattr(settings, 'USE_SUPABASE_DB', False)
            if not use_supabase_db:
                try:
                    if student_id:
                        Complaint.objects.filter(student_id=student_id).exclude(complaint_id__in=supabase_complaint_ids).delete()
                    else:
                        Complaint.objects.exclude(complaint_id__in=supabase_complaint_ids).delete()
                except Exception:
                    pass
            return data
    except Exception as e:
        pass
    return None
