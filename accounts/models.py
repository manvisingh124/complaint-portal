from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin / Grievance Officer'),
    )
    
    DEPARTMENT_CHOICES = (
        ('School of Engineering', 'School of Engineering'),
        ('School of Management', 'School of Management'),
        ('School of Computer Applications', 'School of Computer Applications'),
        ('School of Pharmacy', 'School of Pharmacy'),
        ('School of Allied Health Sciences', 'School of Allied Health Sciences'),
        ('School of Hotel Management', 'School of Hotel Management'),
        ('School of Architecture', 'School of Architecture'),
        ('School of Mass Communication', 'School of Mass Communication'),
        ('School of Legal Studies', 'School of Legal Studies'),
        ('School of Basic Sciences', 'School of Basic Sciences'),
        ('School of Education', 'School of Education'),
        ('Other / Administration', 'Other / Administration'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    enrollment_no = models.CharField(max_length=50, blank=True, null=True, help_text="Student Enrollment Number")
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_student(self):
        return self.role == 'STUDENT'

    def is_staff_member(self):
        return self.role in ['STAFF', 'ADMIN'] or self.is_staff or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def auto_sync_user_to_supabase(sender, instance, **kwargs):
    try:
        from complaints.supabase_sync import sync_user_to_supabase
        sync_user_to_supabase(instance)
    except Exception as e:
        print(f"User Supabase signal error: {e}")
