

# 🎓 E-Learning Platform Management System

A comprehensive Django-based e-learning platform with role-based access control for Students, Trainers, and Managers. This system provides a complete solution for managing online courses, assignments, payments, and student progress tracking.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [Contact](#contact)

## ✨ Features

### 👨‍🎓 Student Module
- ✅ User registration and authentication
- ✅ Browse and enroll in courses
- ✅ Secure payment processing for course fees
- ✅ View enrolled courses and course details
- ✅ Access and submit assignments
- ✅ Track learning progress in real-time
- ✅ Provide course feedback and ratings
- ✅ View grades and feedback from trainers

### 👨‍🏫 Trainer Module
- ✅ Trainer registration and profile management
- ✅ View assigned courses and enrolled students
- ✅ Create and manage assignments
- ✅ Review and grade student submissions
- ✅ Provide detailed feedback on assignments
- ✅ Mark student attendance
- ✅ Update student progress metrics
- ✅ Monitor class performance

### 👨‍💼 Manager Module
- ✅ Comprehensive dashboard with analytics
- ✅ Add and manage courses
- ✅ Assign trainers to courses
- ✅ View and analyze student feedbacks
- ✅ Monitor student progress across all courses
- ✅ Manage payment records
- ✅ Generate reports and statistics
- ✅ User management capabilities

## 🛠 Tech Stack

- **Backend:** Django 4.2+
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Icons:** Font Awesome 6
- **Authentication:** Django Authentication System
- **File Handling:** Django File Upload with Pillow

## 💻 System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- 2GB RAM minimum
- 500MB free disk space

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/e-learning-platform.git
cd e-learning-platform
```

### 2. Create Virtual Environment

```bash
# Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create requirements.txt

```txt
Django>=4.2,<5.0
Pillow>=10.0.0
```

### 5. Configure Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Manager)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. Then:
1. Access admin panel at `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Navigate to Users → Select your superuser
4. Change `user_type` field to **"manager"**

### 7. Create Required Directories

```bash
mkdir -p media/profiles media/submissions static
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## ⚙️ Configuration

### settings.py Key Configurations

```python
# Custom User Model
AUTH_USER_MODEL = 'e_learning_app.User'

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security (for production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secret-key-here'
```

### Environment Variables (Production)

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📖 Usage

### For Students

1. **Register:** Navigate to `/student/register/`
2. **Login:** Use credentials at `/login/`
3. **Browse Courses:** View available courses on the home page
4. **Enroll:** Click "Enroll Now" on desired courses
5. **Make Payment:** Complete payment process after enrollment
6. **Access Content:** View courses, assignments, and progress
7. **Submit Work:** Upload assignments before due dates
8. **Give Feedback:** Rate and review completed courses

### For Trainers

1. **Register:** Navigate to `/trainer/register/`
2. **Dashboard:** Access trainer dashboard at `/trainer/dashboard/`
3. **Create Assignments:** Add assignments for your courses
4. **Grade Submissions:** Review and grade student work
5. **Mark Attendance:** Record student attendance
6. **Update Progress:** Track and update student progress

### For Managers

1. **Login:** Use admin credentials at `/login/`
2. **Dashboard:** Access manager dashboard at `/manager/dashboard/`
3. **Add Courses:** Create new courses with details
4. **Assign Trainers:** Allocate trainers to courses
5. **Monitor Performance:** View analytics and reports
6. **Manage Payments:** Update and track payment records

## 📁 Project Structure

```
e_learning_platform/
│
├── e_learning_platform/          # Project settings
│   ├── __init__.py
│   ├── settings.py               # Main settings
│   ├── urls.py                   # Project URLs
│   ├── wsgi.py
│   └── asgi.py
│
├── e_learning_app/               # Main application
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   ├── student_register.html
│   │   │   └── trainer_register.html
│   │   ├── student/              # Student templates
│   │   ├── trainer/              # Trainer templates
│   │   └── manager/              # Manager templates
│   ├── __init__.py
│   ├── admin.py                  # Admin configuration
│   ├── models.py                 # Database models
│   ├── forms.py                  # Form definitions
│   ├── views.py                  # View functions
│   ├── urls.py                   # App URLs
│   └── tests.py                  # Unit tests
│
├── static/                       # Static files (CSS, JS, images)
├── media/                        # User uploaded files
│   ├── profiles/                 # Profile pictures
│   └── submissions/              # Assignment submissions
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 👥 User Roles

### Student
- **Permissions:** Enroll in courses, submit assignments, view progress, give feedback
- **Access Level:** Limited to own enrollment data
- **Registration:** Public registration available

### Trainer
- **Permissions:** Manage assigned courses, create assignments, grade submissions, mark attendance
- **Access Level:** Access to assigned courses and enrolled students
- **Registration:** Public registration available

### Manager
- **Permissions:** Full system access, manage courses, users, and settings
- **Access Level:** System-wide access to all modules
- **Registration:** Created via Django admin panel


## 🔗 API Endpoints

### Authentication
- `GET/POST /login/` - User login
- `GET/POST /student/register/` - Student registration
- `GET/POST /trainer/register/` - Trainer registration
- `GET /logout/` - User logout

### Student Routes
- `GET /student/dashboard/` - Student dashboard
- `GET /student/courses/` - View enrolled courses
- `GET /student/assignments/` - View assignments
- `POST /student/enroll/<course_id>/` - Enroll in course
- `POST /student/submit/<assignment_id>/` - Submit assignment
- `GET/POST /student/feedback/` - Give course feedback
- `GET /student/progress/` - Track progress

### Trainer Routes
- `GET /trainer/dashboard/` - Trainer dashboard
- `GET /trainer/students/` - View students
- `GET/POST /trainer/assignment/create/` - Create assignment
- `GET /trainer/assignments/` - Manage assignments
- `POST /trainer/grade/<submission_id>/` - Grade submission
- `GET/POST /trainer/attendance/` - Mark attendance
- `POST /trainer/progress/<enrollment_id>/` - Update progress

### Manager Routes
- `GET /manager/dashboard/` - Manager dashboard
- `GET/POST /manager/course/add/` - Add new course
- `GET /manager/courses/` - Manage courses
- `POST /manager/allot-trainer/<course_id>/` - Assign trainer
- `GET /manager/feedbacks/` - View feedbacks
- `GET /manager/progress/` - Analyze progress
- `GET /manager/payments/` - View payments
- `POST /manager/payment/update/<payment_id>/` - Update payment

## 🗄️ Database Models

### User
- Custom user model with role-based authentication
- Fields: username, email, user_type, phone, address

### Course
- Fields: name, description, duration, difficulty_level, fee, trainer, is_active

### Enrollment
- Links students to courses
- Fields: student, course, status, progress_percentage, enrollment_date

### Payment
- Tracks course payments
- Fields: enrollment, amount, payment_method, transaction_id, status

### Assignment
- Course assignments
- Fields: course, title, description, due_date, max_marks, created_by

### Submission
- Student assignment submissions
- Fields: assignment, student, submission_file, marks_obtained, feedback

### Feedback
- Course reviews
- Fields: student, course, rating, comment

### Attendance
- Student attendance records
- Fields: enrollment, date, status, marked_by

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test e_learning_app

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```



### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed

## 🐛 Known Issues

- File upload size limited to 5MB (configurable in settings)
- Email notifications not yet implemented
- Certificate generation pending
- Mobile app integration pending

## 🔮 Future Enhancements

- [ ] Email notifications for enrollments and deadlines
- [ ] Video lecture integration
- [ ] Quiz and test modules
- [ ] Discussion forums
- [ ] Real-time chat support
- [ ] Mobile application (React Native)
- [ ] Certificate generation
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Advanced analytics dashboard
- [ ] Calendar integration
- [ ] Export reports to PDF/Excel
- [ ] Multi-language support
- [ ] Dark mode theme

## 📞 Contact

**Project Maintainer:** Andria Fraderick

- Email: andriafraderick02@gmail.com.com
- GitHub: [@andriafraderick](https://github.com/andriafraderick)
- LinkedIn: [Andria Fraderick](https://www.linkedin.com/in/andriafraderick/)

**Project Link:** [https://github.com/andriafraderick/e-learning-platform] (https://github.com/andriafraderick/e-learning-platform.git)

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- All contributors and supporters

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ using Django
