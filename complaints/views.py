from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint, ComplaintStatusLog, ComplaintAttachment, Feedback
from .forms import ComplaintForm, StatusUpdateForm, FeedbackForm

from .supabase_sync import fetch_live_supabase_complaints

def landing_page(request):
    fetch_live_supabase_complaints()

    total_complaints = Complaint.objects.count()
    resolved_count = Complaint.objects.filter(status__in=['Resolved', 'Closed']).count()
    active_count = Complaint.objects.filter(status__in=['Submitted', 'Under Review', 'In Progress']).count()
    categories_count = len(Complaint.CATEGORY_CHOICES)

    resolved_rate = int((resolved_count / total_complaints) * 100) if total_complaints > 0 else 100

    # Fetch active complaint: prioritize logged in user's complaint if available
    active_complaint = None
    if request.user.is_authenticated and request.user.is_student():
        active_complaint = Complaint.objects.filter(student=request.user).first()
    if not active_complaint:
        active_complaint = Complaint.objects.first()

    context = {
        'total_complaints': total_complaints,
        'resolved_count': resolved_count,
        'resolved_rate': resolved_rate,
        'active_count': active_count,
        'categories_count': categories_count,
        'active_complaint': active_complaint,
    }
    return render(request, 'landing.html', context)


@login_required
def student_dashboard(request):
    if not request.user.is_student() and request.user.is_staff_member():
        return redirect('staff_dashboard')

    # Live sync with Supabase Cloud Database: purge any rows deleted directly in Supabase
    fetch_live_supabase_complaints(student_id=request.user.id)

    complaints = Complaint.objects.filter(student=request.user)
    
    # Filter options
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    open_count = complaints.filter(status__in=['Submitted', 'Under Review', 'In Progress']).count()
    resolved_count = complaints.filter(status__in=['Resolved', 'Closed']).count()
    
    context = {
        'complaints': complaints,
        'open_count': open_count,
        'resolved_count': resolved_count,
        'total_count': complaints.count(),
        'selected_status': status_filter or '',
    }
    return render(request, 'complaints/student_dashboard.html', context)


@login_required
def submit_complaint(request):
    if not request.user.is_student() and request.user.is_staff_member():
        messages.error(request, "Staff accounts cannot submit grievances directly. Please use a student account.")
        return redirect('staff_dashboard')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        files = request.FILES.getlist('attachments')
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()

            # Handle attachments
            for f in files:
                ComplaintAttachment.objects.create(complaint=complaint, file=f)

            # Initial status log entry
            ComplaintStatusLog.objects.create(
                complaint=complaint,
                changed_by=request.user,
                old_status='Created',
                new_status='Submitted',
                remark='Complaint submitted by student.'
            )

            messages.success(request, f"Grievance recorded successfully! Your Complaint ID is {complaint.complaint_id}.")
            return redirect('student_detail', complaint_id=complaint.complaint_id)
        else:
            messages.error(request, "Error submitting grievance. Please check form fields.")
    else:
        form = ComplaintForm()

    return render(request, 'complaints/submit_complaint.html', {'form': form})


@login_required
def student_complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    
    # Security: Only owner student or staff can view
    if complaint.student != request.user and not request.user.is_staff_member():
        messages.error(request, "Permission denied to view this grievance.")
        return redirect('student_dashboard')

    feedback_form = None
    if complaint.status in ['Resolved', 'Closed'] and not hasattr(complaint, 'feedback'):
        if request.method == 'POST' and 'submit_feedback' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                fb = feedback_form.save(commit=False)
                fb.complaint = complaint
                fb.save()
                messages.success(request, "Thank you for your feedback!")
                return redirect('student_detail', complaint_id=complaint.complaint_id)
        else:
            feedback_form = FeedbackForm()

    context = {
        'complaint': complaint,
        'logs': complaint.logs.all(),
        'attachments': complaint.attachments.all(),
        'feedback_form': feedback_form,
    }
    return render(request, 'complaints/student_detail.html', context)


@login_required
def staff_dashboard(request):
    if not request.user.is_staff_member():
        messages.error(request, "Access denied to staff dashboard.")
        return redirect('student_dashboard')

    # Live sync with Supabase Cloud Database
    fetch_live_supabase_complaints()

    # Department filtering: Admins see all; Staff ONLY sees complaints targeted to their department
    if request.user.role == 'ADMIN' or request.user.is_superuser or not request.user.department:
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(department=request.user.department)

    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    open_count = complaints.filter(status='Submitted').count()
    in_progress_count = complaints.filter(status__in=['Under Review', 'In Progress']).count()
    resolved_today_count = complaints.filter(status__in=['Resolved', 'Closed']).count()
    high_priority_count = complaints.filter(priority='High', status__in=['Submitted', 'Under Review', 'In Progress']).count()

    context = {
        'complaints': complaints,
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'resolved_today_count': resolved_today_count,
        'high_priority_count': high_priority_count,
        'selected_category': category_filter or '',
        'selected_status': status_filter or '',
    }
    return render(request, 'complaints/staff_dashboard.html', context)


@login_required
def staff_complaint_detail(request, complaint_id):
    if not request.user.is_staff_member():
        messages.error(request, "Access denied.")
        return redirect('student_dashboard')

    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    # Security: Ensure staff can only view & process complaints targeted to their department
    if request.user.role != 'ADMIN' and not request.user.is_superuser and request.user.department:
        if complaint.department != request.user.department and complaint.category != request.user.department:
            messages.error(request, f"Access denied. You can only manage complaints assigned to the '{request.user.department}' department.")
            return redirect('staff_dashboard')

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            remark = form.cleaned_data['remark']
            old_status = complaint.status

            if old_status != new_status:
                complaint.status = new_status
                if not complaint.assigned_staff:
                    complaint.assigned_staff = request.user
                complaint.save()

                ComplaintStatusLog.objects.create(
                    complaint=complaint,
                    changed_by=request.user,
                    old_status=old_status,
                    new_status=new_status,
                    remark=remark or f"Status updated to {new_status}"
                )

                messages.success(request, f"Complaint status updated to '{new_status}'. Notification dispatched.")
                return redirect('staff_detail', complaint_id=complaint.complaint_id)
            else:
                messages.info(request, "No status change detected.")
    else:
        form = StatusUpdateForm(initial={'status': complaint.status})

    context = {
        'complaint': complaint,
        'logs': complaint.logs.all(),
        'attachments': complaint.attachments.all(),
        'form': form,
    }
    return render(request, 'complaints/staff_detail.html', context)
