from django.db import models
from django.contrib.auth.models import User
from accounts.models import StudentProfile
from questions.models import Test, Question, QuestionOption
from django.utils import timezone


class Result(models.Model):
    """Store test results and scores"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    obtained_marks = models.FloatField(default=0)
    total_marks = models.FloatField()
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('student', 'test')
    
    def __str__(self):
        return f"{self.student.user.username} - {self.test.title}"
    
    @property
    def percentage(self):
        if self.total_marks > 0:
            return (self.obtained_marks / self.total_marks) * 100
        return 0


class StudentAnswer(models.Model):
    """Store individual student answers"""
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('result', 'question')
    
    def __str__(self):
        return f"{self.result.student.user.username} - Q{self.question.id}"
    
    def save(self, *args, **kwargs):
        if self.selected_option:
            self.is_correct = self.selected_option.is_correct
        super().save(*args, **kwargs)
