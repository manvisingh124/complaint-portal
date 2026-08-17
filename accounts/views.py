import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import StudentRegistrationForm, StudentLoginForm, StaffLoginForm
from .models import CustomUser

def student_auth(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard' if request.user.is_student() else 'staff_dashboard')

    active_tab = request.GET.get('tab', 'login')
    login_form = StudentLoginForm()
    register_form = StudentRegistrationForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            active_tab = 'login'
            login_form = StudentLoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('student_dashboard' if user.is_student() else 'staff_dashboard')
            else:
                messages.error(request, "Invalid username or password.")

        elif action == 'register':
            active_tab = 'register'
            register_form = StudentRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, f"Welcome {user.first_name}! Your student account has been created.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Please correct the registration errors below.")

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab,
        'SUPABASE_URL': settings.SUPABASE_URL,
        'SUPABASE_ANON_KEY': settings.SUPABASE_ANON_KEY,
    }
    return render(request, 'accounts/student_auth.html', context)


@csrf_exempt
def supabase_callback(request):
    """API endpoint to receive Supabase OAuth session and sync with Django CustomUser DB."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
            full_name = data.get('full_name', '')

            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email address not provided.'}, status=400)

            if not email.endswith('@bbdu.ac.in'):
                return JsonResponse({'status': 'error', 'message': "Only official '@bbdu.ac.in' email addresses are accepted."}, status=403)

            # Extract names
            names = full_name.split(' ') if full_name else ['', '']
            first_name = names[0] if len(names) > 0 else email.split('@')[0]
            last_name = ' '.join(names[1:]) if len(names) > 1 else ''
            
            # Ensure unique username
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exclude(email=email).exists():
                username = f"{base_username}_{counter}"
                counter += 1

            # Save / Update CustomUser in Database
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'STUDENT',
                    'department': 'Faculty / Teaching'
                }
            )

            if created:
                user.set_unusable_password()
                user.save()

            # Establish Django user session
            login(request, user)
            messages.success(request, f"Authenticated via BBDU Google SSO as {user.get_full_name() or user.username}.")

            return JsonResponse({'status': 'success', 'redirect_url': '/dashboard/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method.'}, status=405)


def staff_login(request):
    if request.user.is_authenticated:
        return redirect('staff_dashboard' if request.user.is_staff_member() else 'student_dashboard')

    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff_member():
                messages.error(request, "Access denied. Student accounts must use Student Portal.")
                return render(request, 'accounts/staff_login.html', {'form': form})
            login(request, user)
            messages.success(request, f"Staff portal session active. Welcome, {user.first_name or user.username}.")
            return redirect('staff_dashboard')
        else:
            messages.error(request, "Invalid staff credentials.")
    else:
        form = StaffLoginForm()

    return render(request, 'accounts/staff_login.html', {'form': form})


@csrf_exempt
def user_logout(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('landing')
