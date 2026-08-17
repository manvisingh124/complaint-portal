from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('complaints/', views.landing_page, name='complaints_home'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('complaints/new/', views.submit_complaint, name='submit_complaint'),
    path('complaints/<str:complaint_id>/', views.student_complaint_detail, name='student_detail'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/complaints/<str:complaint_id>/', views.staff_complaint_detail, name='staff_detail'),
]
