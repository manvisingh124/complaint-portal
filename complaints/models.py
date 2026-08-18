from django.db import models
from django.conf import settings
import datetime

class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ('Faculty / Teaching', 'Faculty / Teaching'),
        ('Examination', 'Examination'),
        ('Administration', 'Administration'),
        ('Infrastructure', 'Infrastructure'),
        ('Hostel / Accommodation', 'Hostel / Accommodation'),
        ('Other', 'Other'),
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

    PRIORITY_CHOICES = (
        ('Low', 'Low Priority'),
        ('Medium', 'Medium Priority'),
        ('High', 'High Priority'),
    )

    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    )

    complaint_id = models.CharField(max_length=30, unique=True, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_complaints')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    department = models.CharField(max_length=80, choices=DEPARTMENT_CHOICES, default='School of Engineering', help_text="Target Department/School for grievance processing")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    subject = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Submitted')
    assigned_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.complaint_id:
            year = datetime.datetime.now().year
            last_complaint = Complaint.objects.filter(complaint_id__startswith=f"BBDU-{year}").order_by('id').last()
            if last_complaint:
                try:
                    last_num = int(last_complaint.complaint_id.split('-')[-1])
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
            self.complaint_id = f"BBDU-{year}-{new_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} — {self.subject} ({self.status})"

    def get_progress_percentage(self):
        mapping = {
            'Submitted': 25,
            'Under Review': 50,
            'In Progress': 75,
            'Resolved': 100,
            'Closed': 100,
            'Rejected': 100
        }
        return mapping.get(self.status, 25)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Complaint)
def auto_sync_complaint_to_supabase(sender, instance, **kwargs):
    try:
        from .supabase_sync import sync_complaint_to_supabase
        sync_complaint_to_supabase(instance)
    except Exception as e:
        print(f"Complaint Supabase signal error: {e}")


class ComplaintStatusLog(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.complaint.complaint_id}: {self.old_status} ➔ {self.new_status} by {self.changed_by.username}"


class ComplaintAttachment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='complaint_attachments/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.complaint.complaint_id}: {self.rating} Stars"
