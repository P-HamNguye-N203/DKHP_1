from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from administrators.models import Course
from scheduling.models import Schedule as SchedulingSchedule

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(
            regex=r'^\d{8,10}$',
            message='Student ID must be 8-10 digits.'
        )
    ])
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        )
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

# Sử dụng model Course từ administrators
Course = Course

# Sử dụng model Schedule từ scheduling
Schedule = SchedulingSchedule

class Registration(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ xác nhận'),
        ('APPROVED', 'Đã xác nhận'),
        ('REJECTED', 'Từ chối'),
        ('CANCELLED', 'Đã hủy'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9\s]+$',
            message='Semester must contain only letters, numbers, and spaces.'
        )
    ])
    academic_year = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{4}$',
            message='Academic year must be in the format: "2023-2024".'
        )
    ])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name} ({self.semester} {self.academic_year})"
