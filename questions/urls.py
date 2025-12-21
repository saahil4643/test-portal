from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    # Subject Management
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.create_subject, name='create_subject'),
    
    # Test Management
    path('tests/', views.test_list, name='test_list'),
    path('tests/create/', views.create_test, name='create_test'),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/edit/', views.edit_test, name='edit_test'),
    path('tests/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    
    # Question Management
    path('tests/<int:test_id>/questions/add/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Student Test Taking
    path('available-tests/', views.available_tests, name='available_tests'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),]