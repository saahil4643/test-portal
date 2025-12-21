from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-admin/', views.create_admin, name='create_admin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    
    # HOD Management (by Admin)
    path('add-hod/', views.add_hod, name='add_hod'),
    path('list-hod/', views.list_hod, name='list_hod'),
    
    # Teacher Management (by Admin or HOD)
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('list-teacher/', views.list_teacher, name='list_teacher'),
    
    # Student Management (by Admin or HOD)
    path('add-student/', views.add_student, name='add_student'),
    path('list-student/', views.list_student, name='list_student'),
]
