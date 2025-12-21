from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import User, TeacherProfile, HODProfile
from .models import Subject, Test, Question, QuestionOption


def can_create_test(user):
    """Check if user can create tests (Admin, HOD, Teacher)"""
    return user.role in ['ADMIN', 'HOD', 'TEACHER']


def admin_or_hod_required(view_func):
    """Decorator to check if user is admin or HOD"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['ADMIN', 'HOD']:
            messages.error(request, 'Admin or HOD access required')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='accounts:login')
def subject_list(request):
    """List all subjects"""
    subjects = Subject.objects.all()
    
    # Filter by department if user is HOD
    if request.user.role == 'HOD':
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            subjects = subjects.filter(department=hod_profile.department)
        except HODProfile.DoesNotExist:
            subjects = Subject.objects.none()
    
    context = {'subjects': subjects}
    return render(request, 'questions/subject_list.html', context)


@login_required(login_url='accounts:login')
@admin_or_hod_required
@csrf_protect
def create_subject(request):
    """Create a new subject"""
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        department = request.POST.get('department')
        year = request.POST.get('year')
        description = request.POST.get('description')
        
        # Validate
        if not all([name, code, department, year]):
            messages.error(request, 'All required fields must be filled')
            return render(request, 'questions/create_subject.html')
        
        if Subject.objects.filter(name=name).exists():
            messages.error(request, 'Subject already exists')
            return render(request, 'questions/create_subject.html')
        
        if Subject.objects.filter(code=code).exists():
            messages.error(request, 'Subject code already exists')
            return render(request, 'questions/create_subject.html')
        
        try:
            Subject.objects.create(
                name=name,
                code=code,
                department=department,
                year=int(year),
                description=description
            )
            messages.success(request, 'Subject created successfully!')
            return redirect('questions:subject_list')
        except Exception as e:
            messages.error(request, f'Error creating subject: {str(e)}')
            return render(request, 'questions/create_subject.html')
    
    return render(request, 'questions/create_subject.html')


@login_required(login_url='accounts:login')
def test_list(request):
    """List tests"""
    tests = Test.objects.all()
    
    # Filter by subject if provided
    subject_id = request.GET.get('subject')
    if subject_id:
        tests = tests.filter(subject_id=subject_id)
    
    # Filter by role
    if request.user.role == 'TEACHER':
        try:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            tests = tests.filter(subject__department=teacher_profile.department, subject__year=teacher_profile.year)
        except TeacherProfile.DoesNotExist:
            tests = Test.objects.none()
    elif request.user.role == 'HOD':
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            tests = tests.filter(subject__department=hod_profile.department)
        except HODProfile.DoesNotExist:
            tests = Test.objects.none()
    
    subjects = Subject.objects.all()
    
    context = {
        'tests': tests,
        'subjects': subjects,
        'selected_subject': subject_id
    }
    return render(request, 'questions/test_list.html', context)


@login_required(login_url='accounts:login')
@csrf_protect
def create_test(request):
    """Create a new test"""
    if not can_create_test(request.user):
        messages.error(request, 'You do not have permission to create tests')
        return redirect('accounts:dashboard')
    
    subjects = Subject.objects.all()
    
    # Filter subjects by department for HOD and Teacher
    if request.user.role == 'HOD':
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            subjects = subjects.filter(department=hod_profile.department)
        except HODProfile.DoesNotExist:
            subjects = Subject.objects.none()
    elif request.user.role == 'TEACHER':
        try:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            subjects = subjects.filter(
                department=teacher_profile.department,
                year=teacher_profile.year
            )
        except TeacherProfile.DoesNotExist:
            subjects = Subject.objects.none()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        subject_id = request.POST.get('subject')
        total_marks = request.POST.get('total_marks', 100)
        duration_minutes = request.POST.get('duration_minutes', 60)
        passing_marks = request.POST.get('passing_marks', 40)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_negative_marking = request.POST.get('is_negative_marking') == 'on'
        negative_mark = request.POST.get('negative_mark_per_question', 0)
        instructions = request.POST.get('instructions')
        
        # Validate
        if not all([title, subject_id, start_date, end_date]):
            messages.error(request, 'All required fields must be filled')
            return render(request, 'questions/create_test.html', {'subjects': subjects})
        
        try:
            subject = Subject.objects.get(id=subject_id)
            
            # Check permission
            if request.user.role == 'HOD':
                hod_profile = HODProfile.objects.get(user=request.user)
                if subject.department != hod_profile.department:
                    messages.error(request, 'You can only create tests for your department')
                    return render(request, 'questions/create_test.html', {'subjects': subjects})
            elif request.user.role == 'TEACHER':
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                if subject.department != teacher_profile.department or subject.year != teacher_profile.year:
                    messages.error(request, 'You can only create tests for your department and year')
                    return render(request, 'questions/create_test.html', {'subjects': subjects})
            
            # Create test
            test = Test.objects.create(
                title=title,
                description=description,
                subject=subject,
                created_by=request.user,
                total_marks=int(total_marks),
                duration_minutes=int(duration_minutes),
                passing_marks=int(passing_marks),
                start_date=datetime.fromisoformat(start_date),
                end_date=datetime.fromisoformat(end_date),
                is_negative_marking=is_negative_marking,
                negative_mark_per_question=float(negative_mark) if is_negative_marking else 0,
                instructions=instructions,
                status='DRAFT'
            )
            
            # Handle questions if added during test creation
            question_count = 0
            question_index = 0
            
            # Get all unique question indices
            while f'question_text_{question_index}' in request.POST:
                question_text = request.POST.get(f'question_text_{question_index}')
                question_marks = request.POST.get(f'question_marks_{question_index}')
                question_difficulty = request.POST.get(f'question_difficulty_{question_index}', 'EASY')
                correct_option_index = request.POST.get(f'correct_option_{question_index}')
                
                if question_text and question_marks:
                    try:
                        # Create question
                        question = Question.objects.create(
                            test=test,
                            question_text=question_text,
                            marks=int(question_marks),
                            difficulty=question_difficulty,
                            order=question_count
                        )
                        
                        # Add MCQ options
                        for opt_idx in range(4):
                            option_text = request.POST.get(f'option_{question_index}_{opt_idx}')
                            if option_text:
                                is_correct = str(correct_option_index) == str(opt_idx)
                                QuestionOption.objects.create(
                                    question=question,
                                    option_text=option_text,
                                    is_correct=is_correct,
                                    order=opt_idx
                                )
                        
                        question_count += 1
                    except Exception as e:
                        messages.warning(request, f'Error adding question {question_index + 1}: {str(e)}')
                
                question_index += 1
            
            if question_count > 0:
                messages.success(request, f'Test created successfully with {question_count} question(s)!')
            else:
                messages.success(request, 'Test created successfully! You can add questions later.')
            
            return redirect('questions:test_list')
        except Subject.DoesNotExist:
            messages.error(request, 'Selected subject does not exist')
        except Exception as e:
            messages.error(request, f'Error creating test: {str(e)}')
    
    context = {'subjects': subjects}
    return render(request, 'questions/create_test.html', context)


@login_required(login_url='accounts:login')
def test_detail(request, test_id):
    """View test details"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permission
    if request.user.role == 'TEACHER':
        try:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            if test.subject.department != teacher_profile.department:
                messages.error(request, 'You do not have permission to view this test')
                return redirect('questions:test_list')
        except TeacherProfile.DoesNotExist:
            messages.error(request, 'Teacher profile not found')
            return redirect('questions:test_list')
    
    questions = test.questions.all()
    
    context = {
        'test': test,
        'questions': questions,
        'total_questions': questions.count(),
        'can_edit': request.user == test.created_by or request.user.role == 'ADMIN'
    }
    return render(request, 'questions/test_detail.html', context)


@login_required(login_url='accounts:login')
@csrf_protect
def add_question(request, test_id):
    """Add a question to a test"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permission
    if request.user != test.created_by and request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to edit this test')
        return redirect('questions:test_detail', test_id=test_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        marks = request.POST.get('marks', 1)
        difficulty = request.POST.get('difficulty', 'MEDIUM')
        
        # Get options
        options_text = request.POST.getlist('option_text')
        correct_option = request.POST.get('correct_option')
        
        # Validate
        if not question_text:
            messages.error(request, 'Question text is required')
            return render(request, 'questions/add_question.html', {'test': test})
        
        if len(options_text) < 2:
            messages.error(request, 'At least 2 options are required')
            return render(request, 'questions/add_question.html', {'test': test})
        
        if not correct_option:
            messages.error(request, 'Please select the correct option')
            return render(request, 'questions/add_question.html', {'test': test})
        
        try:
            # Get next question order
            last_question = test.questions.all().order_by('-order').first()
            next_order = (last_question.order + 1) if last_question else 0
            
            # Create question
            question = Question.objects.create(
                test=test,
                question_text=question_text,
                marks=float(marks),
                difficulty=difficulty,
                order=next_order
            )
            
            # Create options
            for idx, option_text in enumerate(options_text):
                if option_text.strip():  # Only add non-empty options
                    is_correct = str(idx) == correct_option
                    QuestionOption.objects.create(
                        question=question,
                        option_text=option_text,
                        is_correct=is_correct,
                        order=idx
                    )
            
            messages.success(request, 'Question added successfully!')
            return redirect('questions:test_detail', test_id=test_id)
        except Exception as e:
            messages.error(request, f'Error adding question: {str(e)}')
            return render(request, 'questions/add_question.html', {'test': test})
    
    context = {'test': test}
    return render(request, 'questions/add_question.html', context)


@login_required(login_url='accounts:login')
def edit_question(request, question_id):
    """Edit a question"""
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    
    # Check permission
    if request.user != test.created_by and request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to edit this question')
        return redirect('questions:test_detail', test_id=test.id)
    
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        question.marks = float(request.POST.get('marks', 1))
        question.difficulty = request.POST.get('difficulty', 'MEDIUM')
        
        options_text = request.POST.getlist('option_text')
        correct_option = request.POST.get('correct_option')
        
        if not question.question_text:
            messages.error(request, 'Question text is required')
            return render(request, 'questions/edit_question.html', {'question': question})
        
        try:
            question.save()
            
            # Delete existing options and recreate
            question.options.all().delete()
            for idx, option_text in enumerate(options_text):
                if option_text.strip():
                    is_correct = str(idx) == correct_option
                    QuestionOption.objects.create(
                        question=question,
                        option_text=option_text,
                        is_correct=is_correct,
                        order=idx
                    )
            
            messages.success(request, 'Question updated successfully!')
            return redirect('questions:test_detail', test_id=test.id)
        except Exception as e:
            messages.error(request, f'Error updating question: {str(e)}')
    
    context = {'question': question, 'test': test}
    return render(request, 'questions/edit_question.html', context)


@login_required(login_url='accounts:login')
def delete_question(request, question_id):
    """Delete a question"""
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    
    # Check permission
    if request.user != test.created_by and request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to delete this question')
        return redirect('questions:test_detail', test_id=test.id)
    
    test_id = test.id
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('questions:test_detail', test_id=test_id)


@login_required(login_url='accounts:login')
def edit_test(request, test_id):
    """Edit a test"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permission
    if request.user != test.created_by and request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to edit this test')
        return redirect('questions:test_list')
    
    subjects = Subject.objects.all()
    
    if request.user.role == 'HOD':
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            subjects = subjects.filter(department=hod_profile.department)
        except HODProfile.DoesNotExist:
            subjects = Subject.objects.none()
    elif request.user.role == 'TEACHER':
        try:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            subjects = subjects.filter(
                department=teacher_profile.department,
                year=teacher_profile.year
            )
        except TeacherProfile.DoesNotExist:
            subjects = Subject.objects.none()
    
    if request.method == 'POST':
        try:
            test.title = request.POST.get('title')
            test.description = request.POST.get('description')
            test.total_marks = int(request.POST.get('total_marks', 100))
            test.duration_minutes = int(request.POST.get('duration_minutes', 60))
            test.passing_marks = int(request.POST.get('passing_marks', 40))
            test.start_date = datetime.fromisoformat(request.POST.get('start_date'))
            test.end_date = datetime.fromisoformat(request.POST.get('end_date'))
            test.is_negative_marking = request.POST.get('is_negative_marking') == 'on'
            test.negative_mark_per_question = float(request.POST.get('negative_mark_per_question', 0)) if test.is_negative_marking else 0
            test.instructions = request.POST.get('instructions')
            test.status = request.POST.get('status', 'DRAFT')
            
            test.save()
            messages.success(request, 'Test updated successfully!')
            return redirect('questions:test_detail', test_id=test.id)
        except Exception as e:
            messages.error(request, f'Error updating test: {str(e)}')
    
    context = {'test': test, 'subjects': subjects}
    return render(request, 'questions/edit_test.html', context)


@login_required(login_url='accounts:login')
def delete_test(request, test_id):
    """Delete a test"""
    test = get_object_or_404(Test, id=test_id)
    
    # Check permission
    if request.user != test.created_by and request.user.role != 'ADMIN':
        messages.error(request, 'You do not have permission to delete this test')
        return redirect('questions:test_list')
    
    test.delete()
    messages.success(request, 'Test deleted successfully!')
    return redirect('questions:test_list')

@login_required(login_url='accounts:login')
def available_tests(request):
    """List all tests (upcoming, active, and past) for students"""
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can access tests')
        return redirect('accounts:dashboard')
    
    from accounts.models import StudentProfile
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('accounts:dashboard')
    
    # Get all tests (ACTIVE or DRAFT) for student's department and year
    all_tests = Test.objects.filter(
        subject__department=student.department,
        subject__year=student.year
    ).exclude(status='DELETED').select_related('subject', 'created_by').order_by('start_date')
    
    # Categorize tests by timing
    now = timezone.now()
    upcoming_tests = []
    active_tests = []
    past_tests = []
    
    for test in all_tests:
        if now < test.start_date:
            # Test hasn't started yet
            upcoming_tests.append(test)
        elif test.start_date <= now <= test.end_date:
            # Test is currently active
            active_tests.append(test)
        else:
            # Test has ended
            past_tests.append(test)
    
    # Sort by date
    upcoming_tests.sort(key=lambda x: x.start_date)
    active_tests.sort(key=lambda x: x.start_date, reverse=True)
    past_tests.sort(key=lambda x: x.end_date, reverse=True)
    
    context = {
        'upcoming_tests': upcoming_tests,
        'active_tests': active_tests,
        'past_tests': past_tests,
    }
    return render(request, 'questions/available_tests.html', context)


@login_required(login_url='accounts:login')
def take_test(request, test_id):
    """Take a test - view and submit answers"""
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can take tests')
        return redirect('accounts:dashboard')
    
    test = get_object_or_404(Test, id=test_id, status='ACTIVE')
    
    # Check if test is available
    now = timezone.now()
    if not (test.start_date <= now <= test.end_date):
        messages.error(request, 'This test is not available at this time')
        return redirect('questions:available_tests')
    
    questions = test.question_set.all().order_by('order')
    
    if request.method == 'GET':
        context = {
            'test': test,
            'questions': questions,
        }
        return render(request, 'questions/take_test.html', context)
    
    # Handle test submission
    if request.method == 'POST':
        # Store answers (you can extend this to save to a StudentAnswer model)
        score = 0
        total_marks = 0
        answers = {}
        
        for question in questions:
            total_marks += question.marks
            selected_option_id = request.POST.get(f'question_{question.id}')
            
            if selected_option_id:
                try:
                    selected_option = QuestionOption.objects.get(id=selected_option_id)
                    answers[question.id] = {
                        'selected': selected_option.option_text,
                        'correct': selected_option.is_correct
                    }
                    
                    if selected_option.is_correct:
                        score += question.marks
                    elif test.is_negative_marking:
                        score -= test.negative_mark_per_question
                except QuestionOption.DoesNotExist:
                    answers[question.id] = {'selected': None, 'correct': False}
            else:
                answers[question.id] = {'selected': None, 'correct': False}
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        percentage = (score / total_marks * 100) if total_marks > 0 else 0
        
        context = {
            'test': test,
            'questions': questions,
            'answers': answers,
            'score': score,
            'total_marks': total_marks,
            'percentage': percentage,
            'passed': percentage >= 40,  # 40% is passing criteria
        }
        return render(request, 'questions/test_result.html', context)