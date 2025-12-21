# Test Portal - Complete Feature Documentation

## 🎯 System Overview

The Test Portal is a comprehensive Django-based examination and assessment system with role-based access control. It supports four user roles: **Admin**, **HOD**, **Teacher**, and **Student**.

---

## 👥 User Roles & Permissions

### 1. **Admin**
- Full system access
- Create/manage subjects across all departments and years
- Create/manage tests across all subjects
- Add/edit/delete questions and options
- View all tests and their details
- Manage HODs, Teachers, and Students

### 2. **HOD (Head of Department)**
- Manage subjects within their department only
- Create/manage tests for subjects in their department
- Add/edit/delete questions in their department's tests
- View teachers and students in their department
- Add new teachers to their department
- Add new students to their department

### 3. **Teacher**
- Create/manage tests for their department and year
- Add/edit/delete questions in their tests
- Add students to their department and year
- View students in their department and year
- Cannot create subjects (only Admin/HOD can)

### 4. **Student**
- View available tests (based on their department and year)
- Take tests (when tests are active and within schedule)
- View test results and performance
- Cannot create or modify tests

---

## 📚 Core Features

### 1. **Subject Management**
**Location:** `/questions/subjects/`

- **Create Subject** (`/questions/subjects/create/`)
  - Name (required, unique)
  - Code (required, unique)
  - Department
  - Year
  - Description (optional)
  - Accessible by: **Admin**, **HOD**

- **View Subjects** (`/questions/subjects/`)
  - List all subjects
  - Filter by department (for HODs)
  - Quick access to create tests

### 2. **Test Management**
**Location:** `/questions/tests/`

#### Create Test (`/questions/tests/create/`)
- **Test Information**
  - Title (required)
  - Description (optional)
  - Subject (required) - filtered based on user role
  - Status (Draft, Active, Closed)

- **Test Configuration**
  - Total Marks
  - Passing Marks
  - Duration (in minutes)
  - Enable Negative Marking (optional)
  - Negative Mark per Question (if enabled)

- **Test Schedule**
  - Start Date & Time
  - End Date & Time
  - Instructions for students

- **Accessible by:** Admin, HOD (own department), Teacher (own department + year)

#### View Tests (`/questions/tests/`)
- Grid/List view of tests
- Filter by subject
- Shows test details:
  - Status badge (Draft/Active/Closed)
  - Number of questions
  - Total marks
  - Duration
  - Creator info
  - Schedule details

#### Test Details (`/questions/tests/<id>/`)
- Overview with stats
- Schedule information
- Instructions
- Complete list of all questions with options
- MCQ format display

#### Edit Test (`/questions/tests/<id>/edit/`)
- Update test information and configuration
- **Note:** Cannot change the subject (immutable)
- Status modification
- Update marks, duration, passing criteria

#### Delete Test (`/questions/tests/<id>/delete/`)
- Remove entire test with all associated questions
- Requires admin or creator access

### 3. **Question Management**
**Location:** `/questions/questions/`

#### Add Question (`/questions/tests/<test_id>/questions/add/`)
- **Question Details**
  - Question text (required)
  - Marks per question
  - Difficulty level (Easy, Medium, Hard)
  - Order (for question sequencing)

- **MCQ Options**
  - 4 options (A, B, C, D)
  - Option text for each
  - Radio button to select correct answer
  - At least one option must be marked correct

#### Edit Question (`/questions/questions/<id>/edit/`)
- Modify question text
- Change marks and difficulty
- Update MCQ options
- Change correct answer

#### Delete Question (`/questions/questions/<id>/delete/`)
- Remove question from test
- Reorder remaining questions automatically

---

## 📝 Student Test Taking

### Available Tests (`/questions/available-tests/`)
- Shows all active tests for the student's department and year
- Filters by:
  - Current date/time (only shows tests within schedule)
  - Student's department
  - Student's year
- Quick access to test info:
  - Number of questions
  - Total marks
  - Passing marks
  - Duration

### Take Test (`/questions/tests/<id>/take/`)
- One-page test interface
- **Features:**
  - All questions and options visible
  - MCQ format with A, B, C, D options
  - Radio buttons for answer selection
  - Question counter (Q1, Q2, etc.)
  - Marks and difficulty badges
  - Test timer info (duration, total marks)
  - Submit button to finish test

- **Safety Features:**
  - Warns before leaving with unsaved answers
  - Cannot reopen test after submission
  - Auto-calculation of score

### Test Results (`/questions/test-result/`)
- **Score Summary**
  - Score obtained vs total marks
  - Percentage calculation
  - Pass/Fail status
  - Visual progress bar

- **Detailed Answer Review**
  - All questions listed
  - User's answer for each question
  - Correct answer (if user was wrong)
  - Color-coded feedback:
    - 🟢 Green: Correct answers
    - 🔴 Red: Incorrect answers
    - 🟡 Yellow: Unanswered questions

- **Scoring Features:**
  - Positive marking: Full marks for correct answer
  - Negative marking (if enabled): Deduct specified marks for wrong answer
  - Unanswered: Zero marks
  - Minimum score is 0 (cannot go negative)
  - Passing criteria: 40% marks

---

## 🎨 Dashboard Features

### Admin Dashboard (`/accounts/admin-dashboard/`)
- **Stats Cards:**
  - Total HODs
  - Total Teachers
  - Total Students
- **User Management Buttons:**
  - Add/View HODs
  - Add/View Teachers
  - Add/View Students
- **Test Management Section:**
  - Create Subject
  - View Subjects
  - Create Test
  - View All Tests

### HOD Dashboard (`/accounts/hod-dashboard/`)
- **Stats Cards:**
  - Total Teachers (in department)
  - Total Students (in department)
  - Department info
- **Quick Actions:**
  - Teacher Management
  - Student Management
  - Subject Management
  - Test Management
- **Profile Sections:**
  - Personal Details
  - Department Information

### Teacher Dashboard (`/accounts/teacher-dashboard/`)
- **Stats:** Student count
- **Quick Actions:**
  - Add Student (to their department & year)
  - View Students
  - Create Test
  - View Tests
- **Profile:** Personal and Department details

### Student Dashboard (`/accounts/student-dashboard/`)
- **Quick Stats:**
  - Roll Number
  - Department
  - Year
  - Division
- **Quick Actions:**
  - Take Test (access to available tests)
  - Logout
- **Profile:** Complete academic details

---

## 🔧 Technical Details

### Database Models

#### Subject
```
- name (CharField, unique)
- code (CharField, unique)
- department (CharField)
- year (IntegerField)
- description (TextField, optional)
```

#### Test
```
- title (CharField)
- description (TextField, optional)
- subject (ForeignKey to Subject)
- created_by (ForeignKey to User)
- status (Choice: DRAFT, ACTIVE, CLOSED)
- marks (IntegerField)
- passing_marks (IntegerField)
- duration_minutes (IntegerField)
- is_negative_marking (BooleanField)
- negative_mark_per_question (FloatField)
- start_date (DateTimeField)
- end_date (DateTimeField)
- instructions (TextField, optional)
```

#### Question
```
- test (ForeignKey to Test)
- question_text (TextField)
- marks (IntegerField)
- difficulty (Choice: EASY, MEDIUM, HARD)
- order (IntegerField)
```

#### QuestionOption
```
- question (ForeignKey to Question)
- option_text (CharField)
- is_correct (BooleanField)
- order (IntegerField, 0-3 for A-D)
- get_option_letter() method returns A/B/C/D
```

### URL Structure

```
/questions/
├── subjects/ (GET, POST)
├── subjects/create/ (GET, POST)
├── tests/ (GET)
├── tests/create/ (GET, POST)
├── tests/<id>/ (GET)
├── tests/<id>/edit/ (GET, POST)
├── tests/<id>/delete/ (POST)
├── tests/<id>/questions/add/ (GET, POST)
├── questions/<id>/edit/ (GET, POST)
├── questions/<id>/delete/ (POST)
├── available-tests/ (GET) - Student view
└── tests/<id>/take/ (GET, POST) - Student test taking
```

### Decorators & Permission Checks

- `@login_required` - Authentication check
- `@admin_or_hod_required` - Admin or HOD access
- `can_create_test()` - Check if Admin, HOD, or Teacher
- Role-based filtering at query level for department/year constraints

---

## 🎨 Styling

All pages use consistent modern styling with:
- **Gradient Headers** (color varies by role)
- **Card-based Layout**
- **Professional Color Scheme**
- **Responsive Design** (Mobile & Desktop)
- **Interactive Elements** (Hover effects, Transitions)
- **Status Badges** (Visual feedback)
- **Icon Support** (Emoji for quick recognition)

---

## 📱 Mobile Support

All pages are fully responsive and work on:
- Desktop browsers
- Tablets
- Mobile devices

Layout automatically adjusts for smaller screens with:
- Stack-based layouts
- Touch-friendly buttons
- Readable fonts on all sizes

---

## 🔐 Security Features

1. **CSRF Protection** - All forms protected with {% csrf_token %}
2. **Login Required** - All protected pages require authentication
3. **Role-Based Access** - Role validation before accessing views
4. **Department/Year Filtering** - HOD and Teacher views filtered at database level
5. **Creator Validation** - Only test creator or admin can edit/delete
6. **Test Schedule Validation** - Students can only take tests within schedule

---

## 📊 Workflow Examples

### Admin Creating a Test
1. Login as Admin
2. Go to Admin Dashboard → Create Subject
3. Fill subject details and save
4. Go to Admin Dashboard → Create Test
5. Select the subject
6. Configure test details (marks, duration, schedule)
7. Save test
8. Add questions via Test Detail page
9. Set test status to ACTIVE to make it available

### Teacher Creating & Managing Tests
1. Login as Teacher
2. Go to Teacher Dashboard → Create Test
3. Subjects are pre-filtered to their department/year
4. Create test with all details
5. Add questions from test details page
6. View student responses after test ends

### Student Taking a Test
1. Login as Student
2. Go to Student Dashboard → Take Test
3. See all available tests for their department/year
4. Click "Start Test"
5. Answer all questions
6. Click "Submit Test"
7. View results with detailed answer review

---

## 🚀 Getting Started

### Initial Setup
```bash
# Create subjects (as Admin)
# Create tests (as Admin/HOD/Teacher)
# Add questions (as Admin/HOD/Teacher)
# Activate test (change status to ACTIVE)
# Students can now take the test
```

### Create Your First Test
1. Admin/HOD/Teacher logs in
2. Create subject (Admin/HOD only)
3. Create test with schedule
4. Add 4+ questions with MCQ options
5. Set status to ACTIVE
6. Test is now available to students

---

## 📝 Notes

- **Test Schedule:** Tests are only available to students between start and end datetime
- **Negative Marking:** Optional feature that can be enabled per test
- **Question Order:** Maintains question sequence within a test
- **Difficulty Levels:** For difficulty tagging (EASY, MEDIUM, HARD)
- **Status Tracking:** Tests can be DRAFT (prep stage), ACTIVE (live), or CLOSED (completed)

---

## 🔄 Future Enhancement Ideas

1. Save test progress and resume later
2. Test analytics and performance reports
3. Bulk import of questions from CSV
4. Question bank management
5. Multiple choice test variations
6. Integration with gradebook
7. Automated test scheduling
8. Student performance tracking over time

---

**System Version:** 1.0  
**Last Updated:** 2024  
**Framework:** Django 4.2  
**Database:** SQLite (can be upgraded to PostgreSQL)
