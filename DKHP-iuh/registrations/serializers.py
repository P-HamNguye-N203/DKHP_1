from rest_framework import serializers
from .models import Registration
from scheduling.serializers import ScheduleSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegistrationSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    schedule_details = ScheduleSerializer(source='schedule', read_only=True)
    
    class Meta:
        model = Registration
        fields = [
            'id', 'student', 'student_details', 'schedule', 'schedule_details',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 