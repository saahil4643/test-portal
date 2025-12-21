from django.contrib import admin
from .models import Subject, Test, Question, QuestionOption


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('name', 'code')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    fields = ('order', 'option_text', 'is_correct')
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'test', 'marks', 'difficulty', 'order')
    list_filter = ('test', 'difficulty', 'marks')
    search_fields = ('question_text',)
    inlines = [QuestionOptionInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('get_option_letter', 'question', 'option_text', 'is_correct')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('option_text', 'question__question_text')
