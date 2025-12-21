# 📚 Test Portal - Visual Feature Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Portal System                       │
└─────────────────────────────────────────────────────────────┘

                          ↓

        ┌─────────────────────────────────────┐
        │     User Authentication Layer       │
        │  (Login/Logout/Role Management)     │
        └─────────────────────────────────────┘

                          ↓

    ┌───────────────┬──────────────┬──────────────┬──────────────┐
    │    ADMIN      │     HOD      │   TEACHER    │   STUDENT    │
    │   (Full)      │  (Dept)      │  (Dept+Yr)   │   (Read)     │
    └───────────────┴──────────────┴──────────────┴──────────────┘

                          ↓

┌─────────────────────────────────────────────────────────────┐
│              Test Management Module                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📚 Subject Management                               │  │
│  │  • Create/List Subjects                              │  │
│  │  • Department & Year Based                           │  │
│  │  • Full CRUD Operations                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📝 Test Management                                  │  │
│  │  • Create Tests with Schedule                        │  │
│  │  • Configure Marks & Duration                        │  │
│  │  • Status: DRAFT → ACTIVE → CLOSED                   │  │
│  │  • Negative Marking Support                          │  │
│  │  • Edit & Delete Operations                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ❓ Question Management (MCQ Format)                 │  │
│  │  • Add Questions with 4 Options (A,B,C,D)            │  │
│  │  • Set Difficulty: Easy/Medium/Hard                  │  │
│  │  • Select Correct Answer                             │  │
│  │  • Edit & Reorder Questions                          │  │
│  │  • Delete with Auto-Reordering                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🎓 Student Test Taking                              │  │
│  │  • View Available Tests (Filtered by Dept/Yr)        │  │
│  │  • Check Test Schedule                               │  │
│  │  • Answer MCQ Questions                              │  │
│  │  • Submit & Get Instant Results                      │  │
│  │  • Review Correct Answers                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📊 Scoring & Results                                │  │
│  │  • Auto Score Calculation                            │  │
│  │  • Positive & Negative Marking                       │  │
│  │  • Percentage Calculation                            │  │
│  │  • Pass/Fail Determination                           │  │
│  │  • Detailed Answer Review                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

                          ↓

        ┌─────────────────────────────────────┐
        │    Dashboard Layer (4 types)        │
        │  • Admin Dashboard                  │
        │  • HOD Dashboard                    │
        │  • Teacher Dashboard                │
        │  • Student Dashboard                │
        └─────────────────────────────────────┘

                          ↓

        ┌─────────────────────────────────────┐
        │    SQLite Database (Upgradable)     │
        │  • Subjects                         │
        │  • Tests                            │
        │  • Questions                        │
        │  • Question Options                 │
        └─────────────────────────────────────┘
```

---

## User Flow Diagram

### Admin User Flow
```
LOGIN
  ↓
ADMIN DASHBOARD
  ├─ Create Subject
  │   └─ Subject List
  │       └─ View Details
  │
  ├─ Create Test
  │   └─ Test List
  │       ├─ Test Details
  │       │   ├─ Add Question
  │       │   │   ├─ Edit Question
  │       │   │   └─ Delete Question
  │       │   │
  │       │   ├─ Edit Test
  │       │   └─ Delete Test
  │       │
  │       └─ Activate Test (Status: ACTIVE)
  │
  └─ User Management
      ├─ Manage HODs
      ├─ Manage Teachers
      └─ Manage Students
```

### Teacher User Flow
```
LOGIN
  ↓
TEACHER DASHBOARD
  ├─ Create Test
  │   └─ Select Subject (Dept/Yr Filtered)
  │       └─ Add Questions
  │           └─ Configure 4 MCQ Options
  │               └─ Mark Correct Answer
  │
  ├─ View Tests
  │   └─ Edit/Delete/Activate Tests
  │
  ├─ Add Students
  │   └─ View Class Roster
  │
  └─ Monitor Test Results
      └─ See Student Performance
```

### Student User Flow
```
LOGIN
  ↓
STUDENT DASHBOARD
  ├─ Take Test
  │   └─ AVAILABLE TESTS
  │       (Filtered by Dept & Year)
  │       (Only ACTIVE tests shown)
  │       (Only within schedule)
  │           ↓
  │       TAKE TEST
  │       ├─ Read Instructions
  │       ├─ Answer MCQ Questions
  │       │   ├─ Question 1
  │       │   │   ├─ Option A
  │       │   │   ├─ Option B ✓
  │       │   │   ├─ Option C
  │       │   │   └─ Option D
  │       │   │
  │       │   ├─ Question 2
  │       │   │   └─ ... (same format)
  │       │   │
  │       │   └─ Question N
  │       │
  │       ├─ Click SUBMIT
  │       │   ↓
  │       └─ GET RESULTS
  │           ├─ Score (XX/100)
  │           ├─ Percentage (XX%)
  │           ├─ Status (PASSED/FAILED)
  │           └─ ANSWER REVIEW
  │               ├─ Q1: Your Ans ✓ (Correct)
  │               ├─ Q2: Your Ans ✗ (Wrong - Correct: ...)
  │               └─ Q3: Unanswered
  │
  └─ Profile & Logout
```

---

## Data Model Relationships

```
┌──────────────────┐
│    Subject       │
├──────────────────┤
│ • id             │
│ • name           │ ──┐
│ • code           │   │
│ • department     │   │
│ • year           │   │
│ • description    │   │
└──────────────────┘   │
                       │
                       │
         ┌─────────────┘
         │
         ↓
┌──────────────────────────┐
│       Test               │
├──────────────────────────┤
│ • id                     │
│ • title                  │
│ • subject_id (FK) ◄──────┘
│ • created_by (FK to User)│
│ • status                 │
│ • marks                  │
│ • duration_minutes       │
│ • passing_marks          │
│ • negative_marking       │
│ • start_date             │
│ • end_date               │
│ • instructions           │
└──────────────────────────┘
         │
         │
         ↓
┌──────────────────────────┐
│    Question              │
├──────────────────────────┤
│ • id                     │
│ • test_id (FK) ◄─────────┘
│ • question_text          │
│ • marks                  │
│ • difficulty             │
│ • order                  │
└──────────────────────────┘
         │
         │
         ↓
┌──────────────────────────┐
│   QuestionOption         │
├──────────────────────────┤
│ • id                     │
│ • question_id (FK) ◄─────┘
│ • option_text            │
│ • is_correct             │
│ • order (0-3 = A-D)      │
└──────────────────────────┘
```

---

## Test Lifecycle Diagram

```
                    TEST CREATION
                         ↓
                    ┌─────────────┐
                    │  DRAFT      │  Not visible to students
                    │  Status     │  Can be edited freely
                    └─────────────┘
                         ↓
                  [Add Questions]
                         ↓
                  [Review Test]
                         ↓
                    ┌─────────────┐
                    │  ACTIVE     │  Visible to students
                    │  Status     │  Within schedule only
                    └─────────────┘
                         ↓
                  [Students Take Test]
                         ↓
                    ┌─────────────┐
                    │  CLOSED     │  No more submissions
                    │  Status     │  Results available
                    └─────────────┘
                         ↓
                  [View Results/Analytics]

Time: START_DATE -----> [TEST WINDOW] -----> END_DATE
      (Hidden)         (Visible)           (Closed)
```

---

## URL Routing Structure

```
/questions/
│
├── subjects/
│   ├── GET           → List all subjects
│   ├── POST          → Create new subject
│   │
│   └── create/
│       ├── GET       → Show subject form
│       └── POST      → Save subject
│
├── tests/
│   ├── GET           → List all tests (with filter)
│   ├── POST          → Create test
│   │
│   ├── create/
│   │   ├── GET       → Show test form
│   │   └── POST      → Save test
│   │
│   └── <test_id>/
│       ├── GET           → View test details
│       ├── /edit/
│       │   ├── GET       → Show edit form
│       │   └── POST      → Update test
│       │
│       ├── /delete/
│       │   └── POST      → Delete test
│       │
│       ├── /questions/add/
│       │   ├── GET       → Show question form
│       │   └── POST      → Save question
│       │
│       └── /take/
│           ├── GET       → Show test questions (Student)
│           └── POST      → Submit answers (Student)
│
├── questions/
│   └── <question_id>/
│       ├── /edit/
│       │   ├── GET       → Show edit form
│       │   └── POST      → Update question
│       │
│       └── /delete/
│           └── POST      → Delete question
│
└── available-tests/
    └── GET           → List available tests (Student only)
```

---

## Test Scoring Formula

```
                    Score Calculation

Initial Score = 0

For Each Question:
    If Answer is Correct:
        Score += Question Marks
    Else If Answer is Wrong:
        If Negative Marking Enabled:
            Score -= Negative Mark Per Question
        Else:
            Score += 0
    Else If Unanswered:
        Score += 0

Final Score = MAX(0, Score)  // Never below 0

Percentage = (Final Score / Total Marks) × 100

Pass/Fail = if Percentage >= Passing Criteria: PASS
            else: FAIL

Passing Criteria = Typically 40% or configured per test
```

---

## Role Access Control Matrix

```
┌──────────────┬────────┬────────┬─────────┬─────────┐
│   Feature    │ Admin  │  HOD   │ Teacher │ Student │
├──────────────┼────────┼────────┼─────────┼─────────┤
│Create        │        │        │         │         │
│ Subject      │   ✓    │   ✓*   │   ✗     │   ✗     │
│              │        │        │         │         │
│Create Test   │   ✓    │   ✓*   │   ✓*    │   ✗     │
│              │        │        │         │         │
│Add Question  │   ✓    │   ✓*   │   ✓*    │   ✗     │
│              │        │        │         │         │
│Edit Test     │   ✓    │   ✓*   │   ✓*    │   ✗     │
│              │        │        │         │         │
│Delete Test   │   ✓    │   ✓*   │   ✓*    │   ✗     │
│              │        │        │         │         │
│View Tests    │   ✓    │   ✓    │   ✓     │   ✓*    │
│              │        │        │         │         │
│Take Test     │   ✗    │   ✗    │   ✗     │   ✓*    │
│              │        │        │         │         │
│View Results  │   ✓    │   ✓    │   ✓     │   ✓*    │
│              │        │        │         │         │
└──────────────┴────────┴────────┴─────────┴─────────┘

✓  = Full access
✓* = Filtered access (own department/year)
✗  = No access
```

---

## Template Rendering Flow

```
Browser Request
      ↓
    URL Router (urls.py)
      ↓
  View Function (views.py)
      ↓
  ┌─────────────────────────┐
  │  Process Request        │
  │  • Check Permissions    │
  │  • Query Database       │
  │  • Calculate Data       │
  └─────────────────────────┘
      ↓
  ┌─────────────────────────┐
  │  Render Template        │
  │  • Load HTML File       │
  │  • Inject Context Data  │
  │  • Apply CSS Styling    │
  │  • Execute JavaScript   │
  └─────────────────────────┘
      ↓
  HTML Response to Browser
      ↓
  ┌─────────────────────────┐
  │  Browser Rendering      │
  │  • Parse HTML           │
  │  • Apply CSS            │
  │  • Execute JavaScript   │
  │  • Display to User      │
  └─────────────────────────┘
      ↓
  Interactive Web Page
```

---

## MCQ Display Format

```
┌─────────────────────────────────────────────────┐
│           Test: Chapter 5 Quiz                  │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Q1. What is the capital of France?            │
│  [10 marks] [Medium Difficulty]                │
│                                                 │
│  ○ A) London                                   │
│  ○ B) Berlin                                   │
│  ● C) Paris          ← Selected                │
│  ○ D) Madrid                                   │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Q2. What is 2+2?                              │
│  [5 marks] [Easy]                              │
│                                                 │
│  ○ A) 3                                        │
│  ○ B) 4                                        │
│  ○ C) 5                                        │
│  ○ D) 6                                        │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  [← Previous] [1 of 10] [Next →] [Submit]     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Result Display Format

```
┌──────────────────────────────────┐
│   ✅ Congratulations!             │
│   You Passed the Test             │
├──────────────────────────────────┤
│                                  │
│  Score: 75/100      Percentage:  │
│                     75%           │
│                                  │
│  Status: PASSED ✓                │
│                                  │
├──────────────────────────────────┤
│  Overall Performance             │
│  ████████████████░░ 75%         │
│  Passing Criteria: 40%            │
├──────────────────────────────────┤
│  Your Answers                    │
│                                  │
│  Q1 ✓ Correct        +10 marks   │
│  Q2 ✗ Incorrect      -2 marks    │
│      Your: Option B              │
│      Correct: Option A           │
│  Q3 ✓ Correct        +8 marks    │
│  Q4 ⊘ Unanswered     0 marks     │
│                                  │
└──────────────────────────────────┘
```

---

## Integration with Existing System

```
Existing Portal
├── User Authentication
├── Role Management (Admin, HOD, Teacher, Student)
├── Dashboard System
│   ├── Admin Dashboard
│   ├── HOD Dashboard
│   ├── Teacher Dashboard
│   └── Student Dashboard
│
├── Accounts Management
│   ├── User Creation
│   ├── Profile Management
│   └── Department Assignment
│
└── [NEW] Test Management System ← Added
    ├── Subject Management
    ├── Test Creation & Scheduling
    ├── Question Management (MCQ)
    ├── Test Taking Interface
    └── Results & Analytics
```

---

## Mobile Responsive Design

```
Desktop View (1200px+)          Mobile View (320px-600px)
┌──────────────────────┐        ┌────────────┐
│  Header              │        │ Header     │
├──────────────────────┤        ├────────────┤
│ Sidebar   │Main Content       │ Menu       │
│           │                   ├────────────┤
│ • Create  │ ┌─────────────┐   │ Main       │
│   Subject │ │ Subject 1   │   │ Content    │
│ • Create  │ └─────────────┐   │ (Stacked)  │
│   Test    │ ┌─────────────┐   │            │
│ • Manage  │ │ Subject 2   │   └────────────┘
│   Tests   │ └─────────────┐
│           │ ┌─────────────┐
└───────────┴─┴─────────────┘
```

---

## Performance Optimization

```
Database Layer:
  • Filtered queries (department/year)
  • Indexed lookups (subject, test_id)
  • Eager loading (select_related)

Template Layer:
  • CSS minified & inline
  • JavaScript optimized
  • Image optimization
  • Responsive images

Caching:
  • Template caching
  • Query result caching
  • Static file caching

Security:
  • CSRF tokens
  • SQL injection prevention
  • XSS protection
  • Role-based access
```

---

## Browser Compatibility

```
Modern Browsers        Mobile Browsers
• Chrome 90+           • Chrome Mobile
• Firefox 88+          • Safari Mobile
• Safari 14+           • Firefox Mobile
• Edge 90+             • Samsung Browser

Responsive Breakpoints:
• 320px  (Mobile Phone)
• 768px  (Tablet)
• 1024px (Large Tablet)
• 1200px (Desktop)
• 1920px (Large Desktop)
```

---

**This comprehensive system provides a complete solution for online testing and assessment!** 🎉
