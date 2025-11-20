from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('student/register/', views.student_register, name='student_register'),
    path('trainer/register/', views.trainer_register, name='trainer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/enroll/<int:course_id>/', views.student_enroll_course, name='student_enroll_course'),
    path('student/payment/<int:enrollment_id>/', views.student_make_payment, name='student_make_payment'),
    path('student/courses/', views.student_view_courses, name='student_view_courses'),
    path('student/assignments/', views.student_view_assignments, name='student_view_assignments'),
    path('student/submit/<int:assignment_id>/', views.student_submit_assignment, name='student_submit_assignment'),
    path('student/feedback/', views.student_give_feedback, name='student_give_feedback'),
    path('student/progress/', views.student_track_progress, name='student_track_progress'),
    
    # Trainer URLs
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/students/', views.trainer_view_students, name='trainer_view_students'),
    path('trainer/assignment/create/', views.trainer_create_assignment, name='trainer_create_assignment'),
    path('trainer/assignments/', views.trainer_manage_assignments, name='trainer_manage_assignments'),
    path('trainer/submissions/<int:assignment_id>/', views.trainer_view_submissions, name='trainer_view_submissions'),
    path('trainer/grade/<int:submission_id>/', views.trainer_grade_submission, name='trainer_grade_submission'),
    path('trainer/attendance/', views.trainer_mark_attendance, name='trainer_mark_attendance'),
    path('trainer/progress/<int:enrollment_id>/', views.trainer_update_progress, name='trainer_update_progress'),
    
    # Manager URLs
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/course/add/', views.manager_add_course, name='manager_add_course'),
    path('manager/courses/', views.manager_manage_courses, name='manager_manage_courses'),
    path('manager/allot-trainer/<int:course_id>/', views.manager_allot_trainer, name='manager_allot_trainer'),
    path('manager/feedbacks/', views.manager_view_feedbacks, name='manager_view_feedbacks'),
    path('manager/progress/', views.manager_analyse_progress, name='manager_analyse_progress'),
    path('manager/payments/', views.manager_view_payments, name='manager_view_payments'),
    path('manager/payment/update/<int:payment_id>/', views.manager_update_payment, name='manager_update_payment'),
]