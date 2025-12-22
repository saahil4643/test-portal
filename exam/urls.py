from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    # Exam interface
    path('test/<int:test_id>/start/', views.start_exam, name='start_exam'),
    path('test/<int:test_id>/load/', views.load_exam, name='load_exam'),
    
    # AJAX endpoints for exam security
    path('api/submit-answer/', views.submit_answer, name='submit_answer'),
    path('api/cheating-attempt/', views.record_cheating_attempt, name='record_cheating_attempt'),
    path('api/log-event/', views.log_exam_event, name='log_event'),
    path('test/<int:test_id>/submit/', views.submit_exam, name='submit_exam'),
    
    # Results
    path('result/<int:result_id>/', views.view_result, name='view_result'),
]
