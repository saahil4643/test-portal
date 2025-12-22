from django.contrib import admin
from .models import Result, StudentAnswer


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'obtained_marks', 'total_marks', 'is_passed', 'submitted_at']
    list_filter = ['is_passed', 'test', 'submitted_at']
    search_fields = ['student__user__username', 'test__title']
    readonly_fields = ['student', 'test', 'obtained_marks', 'total_marks', 'correct_answers', 
                       'wrong_answers', 'total_questions', 'is_passed', 'submitted_at']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'selected_option', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['result__student__user__username']
