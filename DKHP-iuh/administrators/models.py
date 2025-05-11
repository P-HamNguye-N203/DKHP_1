from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Create your models here.

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(
            regex=r'^[A-Z0-9]+$',
            message='Course ID must contain only uppercase letters and numbers.'
        )
    ])
    course_name = models.CharField(max_length=100)
    credits = models.PositiveIntegerField(validators=[
        MinValueValidator(1, message='Credits must be at least 1.'),
        MaxValueValidator(10, message='Credits cannot exceed 10.')
    ])
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='prerequisite_for')
    status = models.CharField(max_length=20, choices=[
        ('ACCEPTANCE_TO_OPEN', 'Acceptance to Open'),
        ('COURSE_CANCELLED', 'Course Cancelled'),
        ('COURSE_CLOSED', 'Course Closed'),
        ('COURSE_OPEN', 'Course Open')
    ], default='ACCEPTANCE_TO_OPEN')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_id} - {self.course_name}"
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['course_id']

class Administrator(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='administrator_profile')
    admin_id = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(
            regex=r'^[A-Z0-9]+$',
            message='Admin ID must contain only uppercase letters and numbers.'
        )
    ])
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        )
    ])
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=[
        ('ADMIN', 'Administrator'),
        ('STAFF', 'Staff'),
        ('TEACHER', 'Teacher')
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.admin_id} - {self.full_name}"
    
    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"
        ordering = ['admin_id']
