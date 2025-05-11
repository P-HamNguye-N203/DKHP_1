from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from students.models import Student
from administrators.models import Administrator

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('REGISTRATION', 'Đăng ký học phần'),
        ('SCHEDULE', 'Lịch học'),
        ('GRADE', 'Điểm số'),
        ('SYSTEM', 'Hệ thống'),
        ('OTHER', 'Khác'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9\s\-_.,!?()]+$',
            message='Title must contain only letters, numbers, spaces, and basic punctuation.'
        )
    ])
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, validators=[
        RegexValidator(
            regex=r'^(REGISTRATION|SCHEDULE|GRADE|SYSTEM|OTHER)$',
            message='Notification type must be one of: REGISTRATION, SCHEDULE, GRADE, SYSTEM, OTHER.'
        )
    ])
    is_read = models.BooleanField(default=False)
    related_object_id = models.CharField(max_length=50, blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    registration_notifications = models.BooleanField(default=True)
    schedule_notifications = models.BooleanField(default=True)
    grade_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Preferences for {self.user.username}"
