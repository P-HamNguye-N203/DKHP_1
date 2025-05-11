from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from administrators.models import Course

# Create your models here.

class Schedule(models.Model):
    DAY_CHOICES = [
        ('MON', 'Thứ Hai'),
        ('TUE', 'Thứ Ba'),
        ('WED', 'Thứ Tư'),
        ('THU', 'Thứ Năm'),
        ('FRI', 'Thứ Sáu'),
        ('SAT', 'Thứ Bảy'),
        ('SUN', 'Chủ Nhật'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey('administrators.Administrator', on_delete=models.SET_NULL, null=True, related_name='teaching_schedules')
    room = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9\s\-]+$',
            message='Room must contain only letters, numbers, spaces, and hyphens.'
        )
    ])
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES, validators=[
        RegexValidator(
            regex=r'^(MON|TUE|WED|THU|FRI|SAT|SUN)$',
            message='Day of week must be one of: MON, TUE, WED, THU, FRI, SAT, SUN.'
        )
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=30, validators=[
        MinValueValidator(1, message='Capacity must be at least 1.'),
        MaxValueValidator(200, message='Capacity cannot exceed 200.')
    ])
    current_enrollment = models.PositiveIntegerField(default=0)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['day_of_week', 'start_time']
        unique_together = ['course', 'day_of_week', 'start_time', 'end_time', 'semester', 'academic_year']

    def __str__(self):
        return f"{self.course.name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time} ({self.room})"

    def is_full(self):
        return self.current_enrollment >= self.capacity
