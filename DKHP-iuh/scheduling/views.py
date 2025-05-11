from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Schedule
from .serializers import ScheduleSerializer
from administrators.models import Course, Administrator
from notifications.models import Notification
from django.contrib.auth.models import User

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Lọc theo semester và academic_year nếu có
        semester = self.request.query_params.get('semester', None)
        academic_year = self.request.query_params.get('academic_year', None)
        
        queryset = Schedule.objects.all()
        
        if semester:
            queryset = queryset.filter(semester=semester)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can create schedules."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Lấy thông tin khóa học
        course_id = request.data.get('course')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Lấy thông tin giảng viên
        teacher_id = request.data.get('teacher')
        if teacher_id:
            try:
                teacher = Administrator.objects.get(id=teacher_id)
            except Administrator.DoesNotExist:
                return Response(
                    {"detail": "Teacher not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            teacher = None
        
        # Kiểm tra xem lịch học đã tồn tại chưa
        semester = request.data.get('semester')
        academic_year = request.data.get('academic_year')
        day_of_week = request.data.get('day_of_week')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if Schedule.objects.filter(
            course=course,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            semester=semester,
            academic_year=academic_year
        ).exists():
            return Response(
                {"detail": "A schedule with these details already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tạo lịch học mới
        schedule_data = {
            'course': course.id,
            'teacher': teacher.id if teacher else None,
            'room': request.data.get('room'),
            'day_of_week': day_of_week,
            'start_time': start_time,
            'end_time': end_time,
            'semester': semester,
            'academic_year': academic_year,
            'max_capacity': request.data.get('max_capacity')
        }
        
        serializer = self.get_serializer(data=schedule_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Tạo thông báo cho tất cả sinh viên
        students = User.objects.filter(is_staff=False)
        for student in students:
            Notification.objects.create(
                recipient=student,
                title="New Schedule Available",
                message=f"A new schedule for {course.name} ({course.code}) is now available for {semester} {academic_year}.",
                notification_type="SCHEDULE",
                related_object_id=str(serializer.data['id']),
                related_object_type="Schedule"
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def assign_teacher(self, request, pk=None):
        schedule = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can assign teachers."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Lấy thông tin giảng viên
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = Administrator.objects.get(id=teacher_id)
        except Administrator.DoesNotExist:
            return Response(
                {"detail": "Teacher not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cập nhật giảng viên
        schedule.teacher = teacher
        schedule.save()
        
        # Tạo thông báo cho giảng viên
        Notification.objects.create(
            recipient=teacher.user,
            title="Teaching Assignment",
            message=f"You have been assigned to teach {schedule.course.name} ({schedule.course.code}) on {schedule.day_of_week} from {schedule.start_time} to {schedule.end_time}.",
            notification_type="SCHEDULE",
            related_object_id=str(schedule.id),
            related_object_type="Schedule"
        )
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)
