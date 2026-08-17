import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'complaint_portal.settings')
django.setup()

from accounts.models import CustomUser
from complaints.models import Complaint, ComplaintStatusLog

def seed():
    print("Seeding BBDU Grievance Portal database...")

    # 1. Create Student User 1 (Rahul)
    student, created = CustomUser.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@bbdu.ac.in',
            'first_name': 'Rahul',
            'last_name': 'Sharma',
            'role': 'STUDENT',
            'enrollment_no': 'BBDU-2024-0089',
            'department': 'Faculty / Teaching'
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print("  - Created Student user: student / student123")

    # 1b. Create Student User 2 (Adarsh Yadav - aegentfocks)
    student2, created2 = CustomUser.objects.get_or_create(
        email='aegentfocks@bbdu.ac.in',
        defaults={
            'username': 'aegentfocks',
            'first_name': 'Adarsh',
            'last_name': 'Yadav',
            'role': 'STUDENT',
            'enrollment_no': 'BBDU-2026-000004',
            'department': 'Faculty / Teaching'
        }
    )
    if created2:
        student2.set_password('student123')
        student2.save()
        print("  - Created Student user: aegentfocks@bbdu.ac.in (Adarsh Yadav) / student123")
    else:
        student2.username = 'aegentfocks'
        student2.first_name = 'Adarsh'
        student2.last_name = 'Yadav'
        student2.role = 'STUDENT'
        student2.save()
        print("  - Updated Student user: aegentfocks@bbdu.ac.in (Adarsh Yadav)")

    # 2. Create Staff User
    staff, created = CustomUser.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'staff@bbdu.ac.in',
            'first_name': 'Dr. Anita',
            'last_name': 'Singh',
            'role': 'STAFF',
            'department': 'Faculty / Teaching',
            'is_staff': True
        }
    )
    if created:
        staff.set_password('staff123')
        staff.save()
        print("  - Created Staff user: staff / staff123")

    # 3. Create Admin User
    admin, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@bbdu.ac.in',
            'first_name': 'Grievance',
            'last_name': 'Officer',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("  - Created Admin user: admin / admin123")

    # 4. Sample Complaints
    sample_complaints_data = [
        {
            'complaint_id': 'BBDU-2026-000001',
            'category': 'Faculty / Teaching',
            'priority': 'Medium',
            'subject': 'Teaching Method Discrepancy in CSE-302',
            'description': 'Inconsistent teaching materials and lack of clarity in recent lectures for CSE-302. Seeking structured lecture notes and practical session support.',
            'status': 'In Progress',
        },
        {
            'complaint_id': 'BBDU-2026-000002',
            'category': 'Examination',
            'priority': 'High',
            'subject': 'Mid-Semester Marks Sheet Error',
            'description': 'Correction required in the internal mid-term marks awarded for Data Structures lab exam. Practical sheet shows 24/30 but portal reflects 14/30.',
            'status': 'Under Review',
        },
        {
            'complaint_id': 'BBDU-2026-000003',
            'category': 'Infrastructure',
            'priority': 'Low',
            'subject': 'Projector Malfunction in Block B Lab 4',
            'description': 'The main projector display flickers continuously during afternoon lab sessions, disrupting presentation slides.',
            'status': 'Resolved',
        },
        {
            'complaint_id': 'BBDU-2026-000004',
            'category': 'Faculty / Teaching',
            'priority': 'Medium',
            'subject': 'Teaching Problem',
            'description': 'A simple and transparent grievance raised regarding course schedule alignment and extra doubt clearance sessions.',
            'status': 'Under Review',
        },
    ]

    for data in sample_complaints_data:
        complaint, c_created = Complaint.objects.get_or_create(
            complaint_id=data['complaint_id'],
            defaults={
                'student': student2,
                'category': data['category'],
                'priority': data['priority'],
                'subject': data['subject'],
                'description': data['description'],
                'status': data['status'],
                'assigned_staff': staff,
            }
        )
        if not c_created:
            complaint.student = student2
            complaint.save()

        if c_created:
            ComplaintStatusLog.objects.create(
                complaint=complaint,
                changed_by=student2,
                old_status='Created',
                new_status='Submitted',
                remark='Grievance submitted by student.'
            )
            if data['status'] != 'Submitted':
                ComplaintStatusLog.objects.create(
                    complaint=complaint,
                    changed_by=staff,
                    old_status='Submitted',
                    new_status=data['status'],
                    remark=f'Status updated to {data["status"]} by department staff.'
                )
            print(f"  - Created Complaint: {complaint.complaint_id} ({complaint.status})")

    print("\nDatabase seeding complete!")

if __name__ == '__main__':
    seed()
