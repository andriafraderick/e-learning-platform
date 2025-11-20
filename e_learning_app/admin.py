from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, Enrollment, Payment, Assignment, Submission, Feedback, Attendance


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'address', 'profile_picture')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'address')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'trainer', 'duration_weeks', 'difficulty_level', 'fee', 'is_active', 'created_at']
    list_filter = ['difficulty_level', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'progress_percentage', 'enrollment_date']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['student__username', 'course__name']
    date_hierarchy = 'enrollment_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'amount', 'payment_method', 'status', 'transaction_id', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['transaction_id', 'enrollment__student__username']
    date_hierarchy = 'payment_date'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_by', 'due_date', 'max_marks', 'created_at']
    list_filter = ['course', 'created_at', 'due_date']
    search_fields = ['title', 'course__name']
    date_hierarchy = 'due_date'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'marks_obtained', 'graded_by']
    list_filter = ['submitted_at', 'graded_at']
    search_fields = ['student__username', 'assignment__title']
    date_hierarchy = 'submitted_at'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['student__username', 'course__name', 'comment']
    date_hierarchy = 'created_at'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date']
    search_fields = ['enrollment__student__username', 'enrollment__course__name']
    date_hierarchy = 'date'