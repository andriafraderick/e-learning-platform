from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import User, Course, Enrollment, Payment, Assignment, Submission, Feedback, Attendance
from .forms import (StudentRegistrationForm, TrainerRegistrationForm, CustomLoginForm,
                    CourseForm, EnrollmentForm, PaymentForm, AssignmentForm, SubmissionForm,
                    GradeSubmissionForm, FeedbackForm, AttendanceForm, UpdatePaymentForm, TrainerAllotmentForm)


# ============= AUTHENTICATION VIEWS =============
def home(request):
    courses = Course.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'courses': courses})


def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/student_register.html', {'form': form})


def trainer_register(request):
    if request.method == 'POST':
        form = TrainerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Trainer registration successful!')
            return redirect('trainer_dashboard')
    else:
        form = TrainerRegistrationForm()
    return render(request, 'registration/trainer_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'student':
                    return redirect('student_dashboard')
                elif user.user_type == 'trainer':
                    return redirect('trainer_dashboard')
                elif user.user_type == 'manager':
                    return redirect('manager_dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ============= STUDENT VIEWS =============
@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(student=request.user)
    available_courses = Course.objects.filter(is_active=True).exclude(
        id__in=enrollments.values_list('course_id', flat=True)
    )
    
    context = {
        'enrollments': enrollments,
        'available_courses': available_courses,
    }
    return render(request, 'student/dashboard.html', context)


@login_required
def student_enroll_course(request, course_id):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('student_dashboard')
    
    enrollment = Enrollment.objects.create(student=request.user, course=course, status='pending')
    messages.success(request, f'Successfully enrolled in {course.name}. Please complete payment.')
    return redirect('student_make_payment', enrollment_id=enrollment.id)


@login_required
def student_make_payment(request, enrollment_id):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.enrollment = enrollment
            payment.status = 'completed'
            payment.save()
            enrollment.status = 'active'
            enrollment.save()
            messages.success(request, 'Payment successful! You can now access the course.')
            return redirect('student_dashboard')
    else:
        form = PaymentForm(initial={'amount': enrollment.course.fee})
    
    return render(request, 'student/make_payment.html', {'form': form, 'enrollment': enrollment})


@login_required
def student_view_courses(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(student=request.user, status='active')
    return render(request, 'student/view_courses.html', {'enrollments': enrollments})


@login_required
def student_view_assignments(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrolled_courses = Enrollment.objects.filter(student=request.user, status='active').values_list('course', flat=True)
    assignments = Assignment.objects.filter(course__in=enrolled_courses)
    submissions = Submission.objects.filter(student=request.user)
    
    context = {
        'assignments': assignments,
        'submissions': submissions,
    }
    return render(request, 'student/view_assignments.html', context)


@login_required
def student_submit_assignment(request, assignment_id):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.warning(request, 'You have already submitted this assignment.')
        return redirect('student_view_assignments')
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('student_view_assignments')
    else:
        form = SubmissionForm()
    
    return render(request, 'student/submit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def student_give_feedback(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('student_dashboard')
    else:
        enrolled_courses = Enrollment.objects.filter(student=request.user, status='active').values_list('course', flat=True)
        form = FeedbackForm()
        form.fields['course'].queryset = Course.objects.filter(id__in=enrolled_courses)
    
    return render(request, 'student/give_feedback.html', {'form': form})


@login_required
def student_track_progress(request):
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'student/track_progress.html', {'enrollments': enrollments})


# ============= TRAINER VIEWS =============
@login_required
def trainer_dashboard(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    courses = Course.objects.filter(trainer=request.user)
    total_students = Enrollment.objects.filter(course__trainer=request.user, status='active').count()
    
    context = {
        'courses': courses,
        'total_students': total_students,
    }
    return render(request, 'trainer/dashboard.html', context)


@login_required
def trainer_view_students(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(course__trainer=request.user, status='active')
    return render(request, 'trainer/view_students.html', {'enrollments': enrollments})


@login_required
def trainer_create_assignment(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('trainer_manage_assignments')
    else:
        form = AssignmentForm()
        form.fields['course'].queryset = Course.objects.filter(trainer=request.user)
    
    return render(request, 'trainer/create_assignment.html', {'form': form})


@login_required
def trainer_manage_assignments(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    assignments = Assignment.objects.filter(created_by=request.user)
    return render(request, 'trainer/manage_assignments.html', {'assignments': assignments})


@login_required
def trainer_grade_submission(request, submission_id):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            graded_submission = form.save(commit=False)
            graded_submission.graded_by = request.user
            graded_submission.graded_at = timezone.now()
            graded_submission.save()
            messages.success(request, 'Submission graded successfully!')
            return redirect('trainer_view_submissions', assignment_id=submission.assignment.id)
    else:
        form = GradeSubmissionForm(instance=submission)
    
    return render(request, 'trainer/grade_submission.html', {'form': form, 'submission': submission})


@login_required
def trainer_view_submissions(request, assignment_id):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    submissions = Submission.objects.filter(assignment=assignment)
    
    return render(request, 'trainer/view_submissions.html', {'assignment': assignment, 'submissions': submissions})


@login_required
def trainer_mark_attendance(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('trainer_mark_attendance')
    else:
        form = AttendanceForm()
        form.fields['enrollment'].queryset = Enrollment.objects.filter(course__trainer=request.user, status='active')
    
    return render(request, 'trainer/mark_attendance.html', {'form': form})


@login_required
def trainer_update_progress(request, enrollment_id):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__trainer=request.user)
    
    if request.method == 'POST':
        progress = request.POST.get('progress_percentage')
        if progress:
            enrollment.progress_percentage = int(progress)
            enrollment.save()
            messages.success(request, 'Progress updated successfully!')
            return redirect('trainer_view_students')
    
    return render(request, 'trainer/update_progress.html', {'enrollment': enrollment})


# ============= MANAGER VIEWS =============
@login_required
def manager_dashboard(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    total_students = User.objects.filter(user_type='student').count()
    total_trainers = User.objects.filter(user_type='trainer').count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.filter(status='active').count()
    
    context = {
        'total_students': total_students,
        'total_trainers': total_trainers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
    }
    return render(request, 'manager/dashboard.html', context)


@login_required
def manager_add_course(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('manager_manage_courses')
    else:
        form = CourseForm()
        form.fields['trainer'].queryset = User.objects.filter(user_type='trainer')
    
    return render(request, 'manager/add_course.html', {'form': form})


@login_required
def manager_manage_courses(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    courses = Course.objects.all()
    return render(request, 'manager/manage_courses.html', {'courses': courses})


@login_required
def manager_allot_trainer(request, course_id):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = TrainerAllotmentForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Trainer allotted to {course.name} successfully!')
            return redirect('manager_manage_courses')
    else:
        form = TrainerAllotmentForm(instance=course)
        form.fields['trainer'].queryset = User.objects.filter(user_type='trainer')
    
    return render(request, 'manager/allot_trainer.html', {'form': form, 'course': course})


@login_required
def manager_view_feedbacks(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    feedbacks = Feedback.objects.all()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 2) if avg_rating else 0,
    }
    return render(request, 'manager/view_feedbacks.html', context)


@login_required
def manager_analyse_progress(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.filter(status='active')
    courses = Course.objects.annotate(
        avg_progress=Avg('enrollments__progress_percentage'),
        student_count=Count('enrollments', filter=Q(enrollments__status='active'))
    )
    
    context = {
        'enrollments': enrollments,
        'courses': courses,
    }
    return render(request, 'manager/analyse_progress.html', context)


@login_required
def manager_update_payment(request, payment_id):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        form = UpdatePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment details updated successfully!')
            return redirect('manager_view_payments')
    else:
        form = UpdatePaymentForm(instance=payment)
    
    return render(request, 'manager/update_payment.html', {'form': form, 'payment': payment})


@login_required
def manager_view_payments(request):
    if request.user.user_type != 'manager':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    payments = Payment.objects.all()
    return render(request, 'manager/view_payments.html', {'payments': payments})