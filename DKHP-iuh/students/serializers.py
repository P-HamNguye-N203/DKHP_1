from rest_framework import serializers
from .models import Student, Registration
from administrators.serializers import CourseSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class RegistrationSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'registration_date') 