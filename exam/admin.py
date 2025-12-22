from django.contrib import admin
from .models import ExamSession, CheatingAttempt


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('student_user', 'test', 'started_at', 'submitted_at', 'warnings')
    list_filter = ('test', 'started_at', 'warnings')
    search_fields = ('student_user__username', 'test__title')
    readonly_fields = ('started_at', 'submitted_at')
    
    fieldsets = (
        ('Student & Test', {
            'fields': ('student_user', 'test')
        }),
        ('Session Details', {
            'fields': ('started_at', 'submitted_at')
        }),
        ('Security', {
            'fields': ('warnings',)
        }),
    )


@admin.register(CheatingAttempt)
class CheatingAttemptAdmin(admin.ModelAdmin):
    list_display = ('exam_session', 'get_attempt_type_display', 'timestamp')
    list_filter = ('attempt_type', 'timestamp')
    search_fields = ('exam_session__student_user__username', 'exam_session__test__title')
    readonly_fields = ('timestamp',)
    
    def get_readonly_fields(self, request, obj=None):
        return ['exam_session', 'attempt_type', 'timestamp']
