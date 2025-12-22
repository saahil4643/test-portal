from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import json

from questions.models import Test, Question, QuestionOption
from accounts.models import StudentProfile


@login_required(login_url='accounts:login')
def start_exam(request, test_id):
    """Prepare exam - show fullscreen activation screen"""
    
    # Verify user is a student
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can take exams')
        return redirect('accounts:dashboard')
    
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('accounts:dashboard')
    
    # Get the test
    test = get_object_or_404(Test, id=test_id)
    
    # Verify test belongs to student's department and year
    if test.subject.department != student.department or test.subject.year != student.year:
        messages.error(request, 'You do not have access to this test')
        return redirect('questions:available_tests')
    
    # Check if test is available
    now = timezone.now()
    if now < test.start_date:
        messages.error(request, 'This test has not started yet')
        return redirect('questions:available_tests')
    
    if now > test.end_date:
        messages.error(request, 'This test has ended')
        return redirect('questions:available_tests')
    
    context = {
        'test': test,
    }
    
    return render(request, 'exam/exam_start.html', context)


@login_required(login_url='accounts:login')
def load_exam(request, test_id):
    """Load the actual exam interface after fullscreen is activated"""
    
    # Verify user is a student
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can take exams')
        return redirect('accounts:dashboard')
    
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('accounts:dashboard')
    
    # Get the test
    test = get_object_or_404(Test, id=test_id)
    
    # Verify test belongs to student's department and year
    if test.subject.department != student.department or test.subject.year != student.year:
        messages.error(request, 'You do not have access to this test')
        return redirect('questions:available_tests')
    
    # Check if test is available
    now = timezone.now()
    if now < test.start_date:
        messages.error(request, 'This test has not started yet')
        return redirect('questions:available_tests')
    
    if now > test.end_date:
        messages.error(request, 'This test has ended')
        return redirect('questions:available_tests')
    
    # Get all questions for this test
    questions = Question.objects.filter(test=test).prefetch_related('options').order_by('order')
    
    if not questions.exists():
        messages.error(request, 'This test has no questions')
        return redirect('questions:available_tests')
    
    # Calculate time remaining
    time_remaining = (test.end_date - now).total_seconds()
    
    context = {
        'test': test,
        'questions': questions,
        'total_questions': questions.count(),
        'time_remaining': int(time_remaining),
        'duration_minutes': test.duration_minutes,
    }
    
    return render(request, 'exam/exam_interface.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def submit_answer(request):
    """Submit a single answer (AJAX)"""
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        selected_option_id = data.get('option_id')
        
        question = get_object_or_404(Question, id=question_id)
        
        if selected_option_id:
            option = get_object_or_404(QuestionOption, id=selected_option_id)
            
            # Verify option belongs to this question
            if option.question_id != question_id:
                return JsonResponse({'success': False, 'error': 'Invalid option'})
            
            return JsonResponse({
                'success': True,
                'question_id': question_id,
                'selected_option_id': selected_option_id
            })
        else:
            return JsonResponse({'success': True, 'question_id': question_id, 'selected_option_id': None})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def record_cheating_attempt(request):
    """Record a cheating attempt and return warning count"""
    try:
        data = json.loads(request.body)
        test_id = data.get('test_id')
        attempt_type = data.get('attempt_type')  # 'tab_switch', 'fullscreen_exit', 'window_blur'
        
        test = get_object_or_404(Test, id=test_id)
        
        # Get or create exam session - MUST be atomic to prevent race conditions
        from exam.models import ExamSession
        from django.db import transaction
        
        with transaction.atomic():
            # Use select_for_update to lock the row
            try:
                session = ExamSession.objects.select_for_update().get(
                    student_user=request.user,
                    test=test
                )
            except ExamSession.DoesNotExist:
                # First cheating attempt - create new session
                session = ExamSession.objects.create(
                    student_user=request.user,
                    test=test,
                    started_at=timezone.now(),
                    warnings=0
                )
            
            # Check if session is still valid
            if timezone.now() > test.end_date:
                return JsonResponse({'success': False, 'message': 'Exam time has ended'})
            
            # Increment warnings (cap at 3)
            session.warnings = min(session.warnings + 1, 3)
            session.save()
            
            cheating_log = f"{attempt_type.upper()}"
            
            # Log the attempt
            from exam.models import CheatingAttempt
            CheatingAttempt.objects.create(
                exam_session=session,
                attempt_type=attempt_type,
                timestamp=timezone.now()
            )
            
            warning_count = session.warnings
            
            if warning_count >= 3:
                # Force submission
                return JsonResponse({
                    'success': True,
                    'warning_count': warning_count,
                    'force_submit': True,
                    'message': 'Three warnings received. Your exam will be submitted automatically.'
                })
            else:
                return JsonResponse({
                    'success': True,
                    'warning_count': warning_count,
                    'force_submit': False,
                    'message': f'Warning {warning_count}/3: {cheating_log}'
                })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def submit_exam(request, test_id):
    """Submit the exam and calculate score"""
    try:
        if request.user.role != 'STUDENT':
            return JsonResponse({'success': False, 'error': 'Unauthorized'})
        
        test = get_object_or_404(Test, id=test_id)
        data = json.loads(request.body)
        answers = data.get('answers', {})  # {question_id: option_id}
        
        # Calculate score
        correct_count = 0
        total_questions = 0
        
        questions = Question.objects.filter(test=test)
        
        for question in questions:
            total_questions += 1
            selected_option_id = answers.get(str(question.id))
            
            if selected_option_id:
                try:
                    selected_option = QuestionOption.objects.get(
                        id=int(selected_option_id),
                        question=question
                    )
                    if selected_option.is_correct:
                        correct_count += 1
                except (QuestionOption.DoesNotExist, ValueError):
                    pass
        
        # Calculate marks
        marks_per_question = test.total_marks / total_questions if total_questions > 0 else 0
        obtained_marks = correct_count * marks_per_question
        
        # Apply negative marking
        wrong_count = total_questions - correct_count
        if test.is_negative_marking:
            negative_marks = wrong_count * (marks_per_question * 0.25)
            obtained_marks = max(0, obtained_marks - negative_marks)
        
        # Determine pass/fail
        is_passed = obtained_marks >= test.passing_marks
        
        # Store result (use update_or_create in case student retakes the exam)
        from results.models import Result
        with transaction.atomic():
            result, created = Result.objects.update_or_create(
                student=StudentProfile.objects.get(user=request.user),
                test=test,
                defaults={
                    'obtained_marks': round(obtained_marks, 2),
                    'total_marks': test.total_marks,
                    'correct_answers': correct_count,
                    'wrong_answers': wrong_count,
                    'total_questions': total_questions,
                    'is_passed': is_passed,
                    'submitted_at': timezone.now()
                }
            )
            
            # Clear previous answers if this is a retake
            if not created:
                from results.models import StudentAnswer
                StudentAnswer.objects.filter(result=result).delete()
            
            # Store individual answers
            for question in questions:
                selected_option_id = answers.get(str(question.id))
                if selected_option_id:
                    try:
                        selected_option = QuestionOption.objects.get(id=int(selected_option_id))
                        from results.models import StudentAnswer
                        StudentAnswer.objects.create(
                            result=result,
                            question=question,
                            selected_option=selected_option
                        )
                    except (QuestionOption.DoesNotExist, ValueError):
                        pass
        
        return JsonResponse({
            'success': True,
            'result': {
                'obtained_marks': round(obtained_marks, 2),
                'total_marks': test.total_marks,
                'correct_answers': correct_count,
                'wrong_answers': wrong_count,
                'total_questions': total_questions,
                'is_passed': is_passed,
                'percentage': round((obtained_marks / test.total_marks * 100), 2) if test.total_marks > 0 else 0,
                'passing_marks': test.passing_marks
            }
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='accounts:login')
def view_result(request, result_id):
    """View exam result"""
    from results.models import Result
    
    result = get_object_or_404(Result, id=result_id)
    
    # Verify user owns this result
    if result.student.user != request.user:
        messages.error(request, 'You do not have access to this result')
        return redirect('accounts:dashboard')
    
    context = {
        'result': result,
        'test': result.test,
    }
    
    return render(request, 'exam/result.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(['POST'])
def log_exam_event(request):
    """Log exam events for audit trail (optional endpoint)"""
    try:
        data = json.loads(request.body)
        level = data.get('level', 'INFO')
        message = data.get('message', '')
        test_id = data.get('test_id')
        
        # Simple logging to console/debug
        # In production, you could save to database
        print(f"[EXAM LOG] [{level}] Test {test_id}: {message}")
        
        return JsonResponse({'success': True, 'message': 'Event logged'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
