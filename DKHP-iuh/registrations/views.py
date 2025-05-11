from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Registration
from .serializers import RegistrationSerializer
from scheduling.models import Schedule
from notifications.models import Notification
from django.db import transaction

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Lọc theo user nếu không phải admin
        if not self.request.user.is_staff:
            return Registration.objects.filter(student=self.request.user)
        return Registration.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Kiểm tra xem user có phải là sinh viên không
        if request.user.is_staff:
            return Response(
                {"detail": "Only students can register for courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Lấy thông tin lịch học
        schedule_id = request.data.get('schedule')
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response(
                {"detail": "Schedule not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Kiểm tra xem sinh viên đã đăng ký lịch học này chưa
        if Registration.objects.filter(student=request.user, schedule=schedule).exists():
            return Response(
                {"detail": "You have already registered for this schedule."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra xem lịch học đã đầy chưa
        if schedule.current_capacity >= schedule.max_capacity:
            return Response(
                {"detail": "This schedule is already full."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra xem sinh viên đã đăng ký bao nhiêu môn học trong học kỳ này
        semester = schedule.semester
        academic_year = schedule.academic_year
        current_registrations = Registration.objects.filter(
            student=request.user,
            schedule__semester=semester,
            schedule__academic_year=academic_year
        ).count()
        
        if current_registrations >= 5:  # Giới hạn 5 môn học mỗi học kỳ
            return Response(
                {"detail": "You have reached the maximum number of courses for this semester."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tạo đăng ký mới
        registration_data = {
            'student': request.user.id,
            'schedule': schedule.id,
            'status': 'PENDING'
        }
        
        serializer = self.get_serializer(data=registration_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Cập nhật số lượng đăng ký hiện tại
        schedule.current_capacity += 1
        schedule.save()
        
        # Tạo thông báo cho giảng viên
        if schedule.teacher:
            Notification.objects.create(
                recipient=schedule.teacher.user,
                title="New Course Registration",
                message=f"Student {request.user.username} has registered for {schedule.course.course_name} ({schedule.course.course_id}).",
                notification_type="REGISTRATION",
                related_object_id=str(serializer.data['id']),
                related_object_type="Registration"
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        registration = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can approve registrations."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật trạng thái
        registration.status = 'APPROVED'
        registration.save()
        
        # Tạo thông báo cho sinh viên
        Notification.objects.create(
            recipient=registration.student,
            title="Registration Approved",
            message=f"Your registration for {registration.schedule.course.course_name} ({registration.schedule.course.course_id}) has been approved.",
            notification_type="REGISTRATION",
            related_object_id=str(registration.id),
            related_object_type="Registration"
        )
        
        serializer = self.get_serializer(registration)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        registration = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can reject registrations."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật trạng thái
        registration.status = 'REJECTED'
        registration.save()
        
        # Giảm số lượng đăng ký hiện tại
        schedule = registration.schedule
        schedule.current_capacity -= 1
        schedule.save()
        
        # Tạo thông báo cho sinh viên
        Notification.objects.create(
            recipient=registration.student,
            title="Registration Rejected",
            message=f"Your registration for {registration.schedule.course.course_name} ({registration.schedule.course.course_id}) has been rejected.",
            notification_type="REGISTRATION",
            related_object_id=str(registration.id),
            related_object_type="Registration"
        )
        
        serializer = self.get_serializer(registration)
        return Response(serializer.data) 