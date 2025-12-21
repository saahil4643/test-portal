from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import User, AdminProfile, HODProfile, TeacherProfile, StudentProfile


def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'ADMIN':
            messages.error(request, 'Admin access required')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_protect
def create_admin(request):
    """Create a new admin user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/create_admin.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/create_admin.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/create_admin.html')
        
        # Create admin user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='ADMIN',
                is_staff=True
            )
            
            AdminProfile.objects.create(
                user=user,
                phone=phone
            )
            
            messages.success(request, 'Admin created successfully!')
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f'Error creating admin: {str(e)}')
            return render(request, 'accounts/create_admin.html')
    
    return render(request, 'accounts/create_admin.html')


@csrf_protect
def login_view(request):
    """Unified login for Admin, HOD, Teachers, and Students"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'accounts/login.html')
    
    return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login')
def dashboard(request):
    """Redirect to appropriate dashboard based on role"""
    if request.user.role == 'ADMIN':
        return redirect('accounts:admin_dashboard')
    elif request.user.role == 'HOD':
        return redirect('accounts:hod_dashboard')
    elif request.user.role == 'TEACHER':
        return redirect('accounts:teacher_dashboard')
    elif request.user.role == 'STUDENT':
        return redirect('accounts:student_dashboard')
    else:
        return redirect('accounts:login')


@login_required(login_url='accounts:login')
def logout_view(request):
    """Logout for all users"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')


@csrf_protect
@login_required(login_url='accounts:login')
@admin_required
def admin_dashboard(request):
    """Admin dashboard"""
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        admin_profile = None
    
    # Get counts
    hod_count = User.objects.filter(role='HOD').count()
    teacher_count = User.objects.filter(role='TEACHER').count()
    student_count = User.objects.filter(role='STUDENT').count()
    
    context = {
        'admin': request.user,
        'admin_profile': admin_profile,
        'hod_count': hod_count,
        'teacher_count': teacher_count,
        'student_count': student_count
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@csrf_protect
@login_required(login_url='accounts:login')
@admin_required
def add_hod(request):
    """Add HOD by admin"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/add_hod.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/add_hod.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/add_hod.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='HOD'
            )
            
            HODProfile.objects.create(
                user=user,
                phone=phone,
                department=department
            )
            
            messages.success(request, f'HOD {first_name} added successfully!')
            return redirect('accounts:list_hod')
        except Exception as e:
            messages.error(request, f'Error creating HOD: {str(e)}')
            return render(request, 'accounts/add_hod.html')
    
    return render(request, 'accounts/add_hod.html')


@login_required(login_url='accounts:login')
@admin_required
def list_hod(request):
    """List all HODs"""
    hods = User.objects.filter(role='HOD')
    context = {'hods': hods}
    return render(request, 'accounts/list_hod.html', context)


@csrf_protect
@login_required(login_url='accounts:login')
def add_teacher(request):
    """Add Teacher by admin or HOD"""
    # Get department based on role
    department = None
    is_hod = request.user.role == 'HOD'
    
    if is_hod:
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            department = hod_profile.department
        except HODProfile.DoesNotExist:
            messages.error(request, 'HOD profile not found')
            return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        year = request.POST.get('year', 1)
        
        # For admin, get department from form; for HOD, use their department
        if is_hod:
            post_department = department
        else:
            post_department = request.POST.get('department')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/add_teacher.html', {'department': department, 'is_hod': is_hod})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/add_teacher.html', {'department': department, 'is_hod': is_hod})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/add_teacher.html', {'department': department, 'is_hod': is_hod})
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='TEACHER'
            )
            
            TeacherProfile.objects.create(
                user=user,
                phone=phone,
                department=post_department,
                subject=subject,
                year=int(year)
            )
            
            messages.success(request, f'Teacher {first_name} added successfully!')
            if is_hod:
                return redirect('accounts:hod_dashboard')
            else:
                return redirect('accounts:list_teacher')
        except Exception as e:
            messages.error(request, f'Error creating teacher: {str(e)}')
            return render(request, 'accounts/add_teacher.html', {'department': department, 'is_hod': is_hod})
    
    context = {'department': department, 'is_hod': is_hod}
    return render(request, 'accounts/add_teacher.html', context)


@login_required(login_url='accounts:login')
@admin_required
def list_teacher(request):
    """List all Teachers"""
    teachers = User.objects.filter(role='TEACHER')
    context = {'teachers': teachers}
    return render(request, 'accounts/list_teacher.html', context)


@csrf_protect
@login_required(login_url='accounts:login')
def add_student(request):
    """Add Student by admin or HOD"""
    # Get department based on role
    department = None
    is_hod = request.user.role == 'HOD'
    
    if is_hod:
        try:
            hod_profile = HODProfile.objects.get(user=request.user)
            department = hod_profile.department
        except HODProfile.DoesNotExist:
            messages.error(request, 'HOD profile not found')
            return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        roll_number = request.POST.get('roll_number')
        year = request.POST.get('year', 1)
        division = request.POST.get('division')
        
        # For admin, get department from form; for HOD, use their department
        if is_hod:
            post_department = department
        else:
            post_department = request.POST.get('department')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/add_student.html', {'department': department, 'is_hod': is_hod})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/add_student.html', {'department': department, 'is_hod': is_hod})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/add_student.html', {'department': department, 'is_hod': is_hod})
        
        if StudentProfile.objects.filter(roll_number=roll_number).exists():
            messages.error(request, 'Roll number already exists')
            return render(request, 'accounts/add_student.html', {'department': department, 'is_hod': is_hod})
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='STUDENT'
            )
            
            StudentProfile.objects.create(
                user=user,
                phone=phone,
                roll_number=roll_number,
                department=post_department,
                year=int(year),
                division=division
            )
            
            messages.success(request, f'Student {first_name} added successfully!')
            if is_hod:
                return redirect('accounts:hod_dashboard')
            else:
                return redirect('accounts:list_student')
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
            return render(request, 'accounts/add_student.html', {'department': department, 'is_hod': is_hod})
    
    context = {'department': department, 'is_hod': is_hod}
    return render(request, 'accounts/add_student.html', context)


@login_required(login_url='accounts:login')
@admin_required
def list_student(request):
    """List all Students"""
    students = User.objects.filter(role='STUDENT')
    context = {'students': students}
    return render(request, 'accounts/list_student.html', context)


@login_required(login_url='accounts:login')
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def hod_dashboard(request):
    """HOD dashboard"""
    try:
        hod_profile = HODProfile.objects.get(user=request.user)
    except HODProfile.DoesNotExist:
        hod_profile = None
    
    # Get stats for this HOD's department
    department = hod_profile.department if hod_profile else None
    teacher_count = TeacherProfile.objects.filter(department=department).count() if department else 0
    student_count = StudentProfile.objects.filter(department=department).count() if department else 0
    
    context = {
        'hod': request.user,
        'hod_profile': hod_profile,
        'teacher_count': teacher_count,
        'student_count': student_count,
        'department': department
    }
    return render(request, 'accounts/hod_dashboard.html', context)


@login_required(login_url='accounts:login')
def teacher_dashboard(request):
    """Teacher dashboard"""
    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        teacher_profile = None
    
    # Get students for this teacher's subject and year
    students = StudentProfile.objects.filter(
        department=teacher_profile.department,
        year=teacher_profile.year
    ) if teacher_profile else []
    
    context = {
        'teacher': request.user,
        'teacher_profile': teacher_profile,
        'students': students,
        'student_count': len(students)
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required(login_url='accounts:login')
def student_dashboard(request):
    """Student dashboard"""
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        student_profile = None
    
    context = {
        'student': request.user,
        'student_profile': student_profile,
    }
    return render(request, 'accounts/student_dashboard.html', context)


def home(request):
    return render(request, 'accounts/home.html')