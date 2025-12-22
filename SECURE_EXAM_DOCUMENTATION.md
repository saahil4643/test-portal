# 🔐 Secure Exam Module - Documentation

## Overview
The exam module implements a **highly secure, anti-cheating exam interface** with strict security measures to prevent unauthorized activities during test taking.

## 🛡️ Security Features

### 1. **Fullscreen Enforcement**
- Exam automatically enters fullscreen mode when started
- If student exits fullscreen, they are automatically re-entered
- Generates a warning and records cheating attempt

### 2. **Tab Switching Prevention**
- Detects when student switches to another tab
- Automatically records attempt and increments warning counter
- If student opens another tab → Warning issued

### 3. **Window Focus Monitoring**
- Detects when window loses focus (minimization, Alt+Tab)
- Records as suspicious activity
- Prevents students from looking at external resources

### 4. **Right-Click Blocking**
- Prevents right-click context menu (Inspect element protection)
- Records any right-click attempts
- Blocks access to browser developer tools

### 5. **Copy/Paste Prevention**
- Blocks all copy (Ctrl+C) operations
- Blocks all paste (Ctrl+V) operations
- Prevents sharing of questions or answers

### 6. **Developer Tools Detection**
- Detects opening of browser developer tools (F12, Ctrl+Shift+I, etc.)
- Blocks keyboard shortcuts that open dev tools
- Detects dev tools by monitoring window size changes

### 7. **Three-Warning System**
- **1st Warning**: Alert modal + warning icon
- **2nd Warning**: Alert modal + warning icon (more urgent)
- **3rd Warning**: Automatic exam submission with 2-second delay
- All warnings are logged in database for review

### 8. **Session Management**
- Each exam session is tracked in `ExamSession` model
- Records start time, submission time, and warning count
- Prevents multiple concurrent sessions for same test
- Auto-disables exam after time limit expires

## 📊 Anti-Cheating Logging

### CheatingAttempt Model
```python
attempt_type choices:
- tab_switch: Student switched tabs
- fullscreen_exit: Exited fullscreen mode
- window_blur: Window lost focus (minimized)
- right_click: Right-click attempt
- copy_paste: Copy/paste attempt
- developer_tools: Developer tools opened
```

All attempts are:
- Timestamped
- Linked to exam session
- Viewable in admin panel
- Can be used for further investigation

## 🎯 User Flow

### 1. **Start Exam**
```
Student clicks "START TEST NOW"
    ↓
Validation: Check test availability & student access
    ↓
Load exam interface
    ↓
Force fullscreen mode
    ↓
Display exam with timer
```

### 2. **During Exam**
```
Student selects answers
    ↓
Real-time answer tracking
    ↓
Question navigator updates (color-coded)
    ↓
Timer counts down
    ↓
Security monitoring active
```

### 3. **Submit Exam**
```
Student clicks "Submit Exam" OR Timer runs out
    ↓
Collect all answers
    ↓
Calculate score with automatic grading
    ↓
Apply negative marking (if enabled)
    ↓
Store result in database
    ↓
Show result modal
    ↓
Close fullscreen & allow dashboard access
```

## 📁 Files Structure

```
exam/
├── models.py               # ExamSession, CheatingAttempt
├── views.py                # start_exam, submit_exam, etc.
├── urls.py                 # URL patterns
├── admin.py                # Admin interface
└── migrations/

templates/exam/
├── exam_interface.html     # Secure exam UI
└── result.html             # Result display

results/
├── models.py               # Result, StudentAnswer
├── admin.py                # Admin interface
└── migrations/
```

## 🔌 API Endpoints

### 1. **Start Exam**
```
GET /exam/test/<test_id>/start/
- Validates student access
- Checks test timing
- Returns exam interface
```

### 2. **Record Cheating Attempt** (AJAX)
```
POST /exam/api/cheating-attempt/
Body: {
    "test_id": 1,
    "attempt_type": "tab_switch"
}
Response: {
    "success": true,
    "warning_count": 1,
    "force_submit": false,
    "message": "Warning 1/3"
}
```

### 3. **Submit Exam**
```
POST /exam/test/<test_id>/submit/
Body: {
    "answers": {
        "1": "option_id",
        "2": "option_id",
        ...
    }
}
Response: {
    "success": true,
    "result": {
        "obtained_marks": 15.5,
        "total_marks": 25,
        "correct_answers": 5,
        "wrong_answers": 2,
        "percentage": 62.0,
        "is_passed": true
    }
}
```

### 4. **View Result**
```
GET /exam/result/<result_id>/
- Display result details
- Show performance analysis
```

## 🎨 UI/UX Features

### Exam Header
- Test title & subject
- Question count
- **Warning badge** (⚠️ Warnings: 0/3)
- **Timer** (⏱️ TIME REMAINING HH:MM:SS)
  - Green: > 15 minutes
  - Orange: 5-15 minutes (warning state)
  - Red: < 5 minutes (danger state)

### Question Navigator (Left Sidebar)
- Grid of 20 question buttons
- Color-coded states:
  - **Gray**: Not attempted
  - **Green**: Answered
  - **Blue**: Currently viewing
  - **Yellow**: Marked for review

### Exam Area (Main Content)
- Question text with formatting
- MCQ options with radio buttons
- Marks per question
- Progress indicator (Q1/Q25)

### Footer Controls
- **Previous** button (disabled on first question)
- **Next** button (disabled on last question)
- **Submit Exam** button (always available)

### Result Modal
- Pass/Fail indication with emoji
- Score card showing:
  - Your Score
  - Total Marks
  - Percentage
  - Correct/Wrong answers
  - Pass status
- Congratulations or improvement message
- Dashboard redirect button

## 🔒 Security Best Practices

### Server-Side Security
1. **Access Control**
   - Verify student profile exists
   - Check department & year match
   - Validate test timing

2. **Answer Validation**
   - Verify option belongs to question
   - Verify question belongs to test
   - No score calculation cheating possible

3. **Result Integrity**
   - Atomic database transaction
   - No duplicate submissions allowed
   - Immutable result records

### Client-Side Security
1. **Cannot be bypassed** (designed to be resistant)
   - Fullscreen enforcement
   - Event listener blocking
   - Developer tools detection

2. **Logged if attempted**
   - All suspicious activities recorded
   - Timestamps preserved
   - Reviewed by admins

## ⚙️ Configuration

### In `settings.py`
```python
# No special settings required
# Uses Django's default security features
```

### Timer Configuration
- Calculated from test's `end_date` minus current time
- Displays in HH:MM:SS format
- Auto-submits when reaches 0

### Negative Marking
- Applied during scoring
- Formula: `wrong_answers * (marks_per_question * 0.25)`
- Prevents final score from going below 0

## 📊 Database Models

### ExamSession
```python
- student_user: ForeignKey(User)
- test: ForeignKey(Test)
- started_at: DateTime
- submitted_at: DateTime (nullable)
- warnings: Integer (0-3)
```

### CheatingAttempt
```python
- exam_session: ForeignKey(ExamSession)
- attempt_type: Choice (6 types)
- timestamp: DateTime
- details: JSON
```

### Result
```python
- student: ForeignKey(StudentProfile)
- test: ForeignKey(Test)
- obtained_marks: Float
- total_marks: Float
- correct_answers: Integer
- wrong_answers: Integer
- total_questions: Integer
- is_passed: Boolean
- submitted_at: DateTime
```

### StudentAnswer
```python
- result: ForeignKey(Result)
- question: ForeignKey(Question)
- selected_option: ForeignKey(QuestionOption)
- is_correct: Boolean
```

## 🚀 Usage

### For Students
1. Go to "Take Test" section
2. Click "START TEST NOW" button
3. Browser enters fullscreen automatically
4. Answer questions using question navigator
5. Click "Submit Exam" when ready
6. View results immediately

### For Teachers/HOD/Admin
1. Create test with questions
2. Set start & end date/time
3. Publish test (mark as ACTIVE)
4. View cheating attempts in admin
5. Review student results & performance

### For Admins
1. Monitor exam sessions
2. Review cheating attempts (Admin Panel)
3. Check warning patterns
4. Generate reports on academic integrity

## ⚠️ Known Limitations

1. **Client-Side Detection**: Security relies partly on JavaScript (not 100% foolproof against advanced users)
2. **Browser Extensions**: Some extensions might interfere with security measures
3. **Virtual Machines**: Cannot detect VMs used for cheating
4. **Multiple Monitors**: Cannot prevent looking at secondary screens

## 🔄 Future Enhancements

1. **Proctoring**: Add webcam monitoring with alerts
2. **Biometric Auth**: Add fingerprint/face verification
3. **IP Logging**: Track exam attempts by IP address
4. **Device Fingerprinting**: Prevent device switching
5. **Question Randomization**: Randomize question & option order
6. **Keyboard Monitoring**: Detect unusual keyboard patterns

## 📚 Integration Points

### With Questions Module
- Fetches questions from `Question` model
- Gets options from `QuestionOption` model
- Validates against `Test` model

### With Accounts Module
- Verifies student profile
- Checks department & year
- Validates user role

### With Results Module
- Stores results in `Result` model
- Stores answers in `StudentAnswer` model
- Calculates percentage & pass status

## 🔗 URL Mapping

```
/exam/test/<test_id>/start/              → start_exam (GET)
/exam/api/submit-answer/                 → submit_answer (POST)
/exam/api/cheating-attempt/              → record_cheating_attempt (POST)
/exam/test/<test_id>/submit/             → submit_exam (POST)
/exam/result/<result_id>/                → view_result (GET)
```

## ✅ Testing Checklist

- [ ] Student can start exam
- [ ] Fullscreen enforces automatically
- [ ] Exiting fullscreen triggers warning
- [ ] Switching tabs triggers warning
- [ ] Minimizing triggers warning
- [ ] 3 warnings auto-submit exam
- [ ] Timer counts down correctly
- [ ] Answers are saved
- [ ] Score calculates correctly
- [ ] Results display properly
- [ ] Results persist in database
- [ ] Multiple attempts prevented
- [ ] Admin can review attempts

## 🎓 Academic Integrity

This module implements best practices for maintaining academic integrity while respecting student privacy:
- No personal data collection beyond exam data
- No persistent monitoring (only during exam)
- Transparent warning system
- Fair evaluation for all students
- Detailed audit trail for dispute resolution
