from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Administrator
from .serializers import CourseSerializer, AdministratorSerializer
from students.models import Registration
from notifications.models import Notification
from django.contrib.auth.models import User

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Lọc theo department nếu có
        department = self.request.query_params.get('department', None)
        if department:
            return Course.objects.filter(department=department)
        return Course.objects.all()
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        course = self.get_object()
        registrations = Registration.objects.filter(course=course)
        from students.serializers import RegistrationSerializer
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        course = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can approve courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật trạng thái khóa học
        course.status = 'COURSE_OPEN'
        course.save()
        
        # Tạo thông báo cho tất cả sinh viên
        students = User.objects.filter(is_staff=False)
        for student in students:
            Notification.objects.create(
                recipient=student,
                title="Course Approved",
                message=f"The course {course.name} ({course.code}) has been approved and is now open for registration.",
                notification_type="COURSE",
                related_object_id=str(course.id),
                related_object_type="Course"
            )
        
        serializer = self.get_serializer(course)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        course = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can cancel courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật trạng thái khóa học
        course.status = 'COURSE_CANCELLED'
        course.save()
        
        # Tạo thông báo cho tất cả sinh viên đã đăng ký
        registrations = Registration.objects.filter(course=course, status='APPROVED')
        for registration in registrations:
            Notification.objects.create(
                recipient=registration.student.user,
                title="Course Cancelled",
                message=f"The course {course.name} ({course.code}) has been cancelled. Your registration will be automatically cancelled.",
                notification_type="COURSE",
                related_object_id=str(course.id),
                related_object_type="Course"
            )
            
            # Cập nhật trạng thái đăng ký
            registration.status = 'CANCELLED'
            registration.save()
        
        serializer = self.get_serializer(course)
        return Response(serializer.data)

class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        # Lọc theo department nếu có
        department = self.request.query_params.get('department', None)
        if department:
            return Administrator.objects.filter(department=department)
        return Administrator.objects.all()
    
    @action(detail=True, methods=['get'])
    def teaching_schedules(self, request, pk=None):
        administrator = self.get_object()
        from scheduling.models import Schedule
        from scheduling.serializers import ScheduleSerializer
        
        schedules = Schedule.objects.filter(teacher=administrator)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
