from rest_framework import serializers
from .models import Schedule
from administrators.serializers import CourseSerializer, AdministratorSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    teacher_details = AdministratorSerializer(source='teacher', read_only=True)
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'course', 'course_details', 'teacher', 'teacher_details',
            'room', 'day_of_week', 'start_time', 'end_time',
            'semester', 'academic_year', 'max_capacity', 'current_capacity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['current_capacity', 'created_at', 'updated_at'] 