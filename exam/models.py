from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Test
from django.utils import timezone

User = get_user_model()


class ExamSession(models.Model):
    """Track exam sessions for security purposes"""
    student_user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    warnings = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('student_user', 'test')
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student_user.username} - {self.test.title}"


class CheatingAttempt(models.Model):
    """Log suspicious activities during exam"""
    ATTEMPT_TYPES = [
        ('tab_switch', 'Tab Switched'),
        ('fullscreen_exit', 'Exited Fullscreen'),
        ('window_blur', 'Window Lost Focus'),
        ('right_click', 'Right Click Detected'),
        ('copy_paste', 'Copy/Paste Detected'),
        ('developer_tools', 'Developer Tools Opened'),
    ]
    
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='cheating_attempts')
    attempt_type = models.CharField(max_length=20, choices=ATTEMPT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.exam_session.student_user.username} - {self.get_attempt_type_display()}"
