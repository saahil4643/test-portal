from django.db import models
from accounts.models import User, TeacherProfile

class Subject(models.Model):
    """Subject model for organizing tests"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Test(models.Model):
    """Test/Exam model"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    total_marks = models.IntegerField(default=100)
    duration_minutes = models.IntegerField(default=60)  # Duration in minutes
    passing_marks = models.IntegerField(default=40)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    is_negative_marking = models.BooleanField(default=False)
    negative_mark_per_question = models.FloatField(default=0)
    
    instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class Question(models.Model):
    """MCQ Question model"""
    DIFFICULTY_CHOICES = (
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    )

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    
    marks = models.FloatField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    order = models.IntegerField(default=0)  # Order of question in test
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['test', 'order']

    def __str__(self):
        return f"Q{self.order + 1}: {self.question_text[:50]}"


class QuestionOption(models.Model):
    """Options for MCQ questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    option_image = models.ImageField(upload_to='options/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # A=0, B=1, C=2, D=3

    class Meta:
        ordering = ['question', 'order']

    def __str__(self):
        letter = chr(65 + self.order)  # Convert 0->A, 1->B, etc
        return f"{letter}. {self.option_text[:50]}"

    def get_option_letter(self):
        """Return option letter (A, B, C, D)"""
        return chr(65 + self.order)
