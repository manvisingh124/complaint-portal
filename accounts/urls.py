from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_auth, name='student_auth'),
    path('login/', views.student_auth, name='student_login'),
    path('register/', views.student_auth, name='student_register'),
    path('supabase-callback/', views.supabase_callback, name='supabase_callback'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('logout/', views.user_logout, name='logout'),
]
