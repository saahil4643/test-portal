# 🚀 Quick Start Guide - Test Portal

## In 5 Minutes, Create Your First Test

### Step 1: Login as Admin (1 min)
```
URL: http://localhost:8000/accounts/login/
Username: admin (or create one with: python manage.py createsuperuser)
Password: your_password
```

### Step 2: Create a Subject (1 min)
```
Path: Admin Dashboard → Create Subject
Fill in:
  - Name: "Mathematics 101"
  - Code: "MATH101"
  - Department: "Science"
  - Year: 1
  - Description: "Introduction to Calculus"
Click: Save
```

### Step 3: Create a Test (2 min)
```
Path: Admin Dashboard → Create Test
Fill in:
  - Title: "Calculus Midterm"
  - Subject: "Mathematics 101"
  - Total Marks: 100
  - Passing Marks: 40
  - Duration: 120 minutes
  
  Click "Add More Details":
  - Start Date: Today 10:00 AM
  - End Date: Today 2:00 PM
  - Status: DRAFT
  - Instructions: "Answer all questions"
  
Click: Create Test
```

### Step 4: Add Questions (2 min)
```
Path: Test Details → Add Question (button)

For Question 1:
  - Text: "What is the derivative of x²?"
  - Marks: 10
  - Difficulty: Easy
  
  Options:
    A) 2x        (select as correct ✓)
    B) x²
    C) 2
    D) x/2
  
  Click: Save Question

Repeat for more questions...
```

### Step 5: Activate & Test
```
Path: Edit Test → Change Status to "ACTIVE" → Save

Now login as a Student user and go to:
  - Dashboard → "Take Test" button
  - You should see "Calculus Midterm" in available tests
  - Click "Start Test" and take it!
```

---

## 🎯 What You Can Do Now

### 👨‍💼 As Admin:
- Create subjects for any department/year
- Create tests with custom schedules
- Add multiple choice questions
- Set negative marking rules
- View all tests in system

### 👔 As HOD:
- Create subjects for your department
- Create tests for your department
- Add questions to tests
- Manage your department's students

### 👨‍🏫 As Teacher:
- Create tests for your class
- Add questions to tests
- See when students take tests
- View their results

### 👨‍🎓 As Student:
- See available tests
- Take tests during scheduled time
- Get instant results
- Review correct answers

---

## 📝 Template Usage

### Subject Creation Template
```html
Form Fields:
  - Subject Name (text)
  - Code (text, unique)
  - Department (dropdown)
  - Year (number 1-4)
  - Description (textarea)
```

### Test Creation Template
```html
Section 1 - Basic Info:
  - Test Title
  - Description
  - Subject Selection

Section 2 - Configuration:
  - Total Marks
  - Passing Marks
  - Duration (minutes)
  - Negative Marking (toggle)
  - Negative Mark per Wrong Answer (if enabled)

Section 3 - Schedule:
  - Start Date & Time
  - End Date & Time

Section 4 - Instructions:
  - Test Instructions (optional)
```

### Question Template
```html
Form Fields:
  - Question Text (textarea)
  - Marks (number)
  - Difficulty (Easy/Medium/Hard)
  
For Each Option:
  - Option Text (A, B, C, D)
  - Mark as Correct (radio button)
```

---

## 🎨 Visual Flow

```
Admin Dashboard
├── Create Subject
│   └── Subject List
└── Create Test
    └── Test List
        ├── Test Details
        │   ├── Add Question
        │   │   ├── Edit Question
        │   │   └── Delete Question
        │   ├── Edit Test
        │   └── Delete Test
        └── [Status: ACTIVE]
            └── Available to Students
                └── Student Takes Test
                    ├── View Results
                    └── Review Answers
```

---

## ⌚ Test Schedule Example

```
Created: 2024-01-10 (Admin creates test)
Status: DRAFT (not yet available)

Scheduled:
  Start: 2024-01-15 10:00 AM
  End: 2024-01-15 11:30 AM
  
Status: ACTIVE (teacher activates it)

Student Access:
  ✓ Available from 10:00 AM - 11:30 AM on Jan 15
  ✗ Not available before 10:00 AM
  ✗ Not available after 11:30 AM

After 11:30 AM:
  Status: CLOSED (teacher closes it)
  ✓ Students can view their results
  ✗ Cannot retake test
```

---

## 🧪 Test Data Entry

### Creating a 4-Question Quiz

**Question 1 (Easy, 5 marks)**
```
Text: What is 2+2?
Options:
  A) 3
  B) 4 ✓ (correct)
  C) 5
  D) 6
```

**Question 2 (Easy, 5 marks)**
```
Text: Capital of France?
Options:
  A) London
  B) Berlin
  C) Paris ✓ (correct)
  D) Madrid
```

**Question 3 (Medium, 10 marks)**
```
Text: Who wrote Romeo & Juliet?
Options:
  A) Charles Dickens
  B) William Shakespeare ✓ (correct)
  C) Jane Austen
  D) Mark Twain
```

**Question 4 (Hard, 10 marks)**
```
Text: What is Photosynthesis?
Options:
  A) Animal reproduction process
  B) Process of plant making food from light ✓ (correct)
  C) Process of water evaporation
  D) Cell division in animals
```

---

## 📊 Scoring Example

**Test Configuration:**
- Total Marks: 30
- Passing Marks: 12 (40%)
- Negative Marking: ON
- Negative Mark per Wrong: 1

**Student Answers:**
- Q1 (5 marks): Correct ✓ → +5
- Q2 (5 marks): Wrong ✗ → -1
- Q3 (10 marks): Correct ✓ → +10
- Q4 (10 marks): Unanswered → 0

**Result:**
- Score: 5 - 1 + 10 + 0 = **14 marks**
- Total: 30
- Percentage: (14/30) × 100 = **46.67%**
- Status: **PASSED** ✓

---

## 🔄 Common Workflows

### Workflow 1: Admin Sets Up Initial Subject
```
1. Login as Admin
2. Create Subject: "Physics 101"
3. Add Department: "Science"
4. Logout
5. Ready for Teachers to create tests
```

### Workflow 2: Teacher Creates & Activates Test
```
1. Login as Teacher
2. Create Test: "Chapter 5 Quiz"
3. Add 5 MCQ questions
4. Set Schedule: Next Monday 10 AM - 11 AM
5. Change Status from DRAFT to ACTIVE
6. Students can now see & take test
```

### Workflow 3: Student Takes Test
```
1. Login as Student
2. Dashboard → "Take Test"
3. See "Chapter 5 Quiz" in available tests
4. Click "Start Test"
5. Answer all 5 questions
6. Click "Submit Test"
7. See results immediately
8. Review correct answers
```

---

## 💡 Tips & Tricks

### Question Bank Tips:
- Order questions from easy to hard
- Use consistent difficulty levels
- Mix conceptual and application questions
- Ensure each question has exactly ONE correct option

### Test Scheduling Tips:
- Set end time 2-3 hours after start
- Avoid scheduling during lunch/breaks
- Give 30-60 minutes for most tests
- Set passing criteria at 40-50%

### Best Practices:
- Add clear instructions to every test
- Use negative marking for higher levels
- Include question difficulty tags
- Review test before activating

---

## ❓ FAQ

**Q: Can students retake tests?**
A: No, once submitted, test is locked. Create multiple tests for practice/reassessment.

**Q: Can I change test after students start?**
A: Not recommended. Close the test and create a new one if changes needed.

**Q: How long are test results stored?**
A: Indefinitely in the database. Results persist after test ends.

**Q: Can I export results?**
A: Currently shows on screen. You can screenshot or export later via Django admin.

**Q: What if test schedule is wrong?**
A: Edit test before students start. Adjust start/end times and save.

**Q: Can negative marks go below 0?**
A: No, system ensures minimum score is always 0.

---

## 🚀 Next Steps

1. **Create your first test** following steps above
2. **Invite students** by adding them to your system
3. **Set realistic schedule** for your test
4. **Prepare questions** beforehand
5. **Test as student** before making it live
6. **Activate test** when ready
7. **Monitor student progress** in results

---

## 📱 Mobile Access

✓ All pages responsive
✓ Works on phones & tablets
✓ Touch-friendly interface
✓ Same functionality as desktop

**Note**: Recommended to use desktop for test creation, mobile for taking tests

---

## 🆘 Need Help?

### System Won't Start?
```
python manage.py migrate
python manage.py runserver
```

### No Admin User?
```
python manage.py createsuperuser
```

### Forgot Password?
```
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('newpassword')
user.save()
```

---

**Ready to Create Your First Test?** Start with Step 1 above! 🎉

Expected time: **5-10 minutes**
