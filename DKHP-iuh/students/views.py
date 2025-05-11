from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Student, Registration, Schedule
from administrators.models import Course
from .serializers import StudentSerializer, RegistrationSerializer
from notifications.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Nếu là admin, trả về tất cả sinh viên
        if self.request.user.is_staff:
            return Student.objects.all()
        # Nếu là sinh viên, chỉ trả về thông tin của chính họ
        return Student.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        student = self.get_object()
        registrations = Registration.objects.filter(student=student)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Nếu là admin, trả về tất cả đăng ký
        if self.request.user.is_staff:
            return Registration.objects.all()
        # Nếu là sinh viên, chỉ trả về đăng ký của họ
        student = get_object_or_404(Student, user=self.request.user)
        return Registration.objects.filter(student=student)
    
    def create(self, request, *args, **kwargs):
        # Kiểm tra xem người dùng có phải là sinh viên không
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Only students can register for courses."},
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
        
        # Kiểm tra xem sinh viên đã đăng ký khóa học này chưa
        semester = request.data.get('semester')
        academic_year = request.data.get('academic_year')
        
        if Registration.objects.filter(
            student=student,
            course=course,
            semester=semester,
            academic_year=academic_year
        ).exists():
            return Response(
                {"detail": "You have already registered for this course in this semester."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tạo đăng ký mới
        registration_data = {
            'student': student.id,
            'course': course.id,
            'semester': semester,
            'academic_year': academic_year,
            'status': 'PENDING'
        }
        
        serializer = self.get_serializer(data=registration_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Tạo thông báo cho sinh viên
        Notification.objects.create(
            recipient=request.user,
            title="Course Registration",
            message=f"You have registered for {course.name} ({course.code}) for {semester} {academic_year}.",
            notification_type="REGISTRATION",
            related_object_id=str(serializer.data['id']),
            related_object_type="Registration"
        )
        
        # Tạo thông báo cho admin
        admin_users = User.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                recipient=admin,
                title="New Course Registration",
                message=f"Student {student.full_name} ({student.student_id}) has registered for {course.name} ({course.code}).",
                notification_type="REGISTRATION",
                related_object_id=str(serializer.data['id']),
                related_object_type="Registration"
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        registration = self.get_object()
        
        # Kiểm tra xem người dùng có quyền hủy đăng ký không
        if not request.user.is_staff and registration.student.user != request.user:
            return Response(
                {"detail": "You do not have permission to cancel this registration."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Kiểm tra xem đăng ký có thể hủy không
        if registration.status in ['REJECTED', 'CANCELLED']:
            return Response(
                {"detail": f"This registration is already {registration.status.lower()}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cập nhật trạng thái đăng ký
        registration.status = 'CANCELLED'
        registration.save()
        
        # Tạo thông báo cho sinh viên
        Notification.objects.create(
            recipient=registration.student.user,
            title="Registration Cancelled",
            message=f"Your registration for {registration.course.name} ({registration.course.code}) has been cancelled.",
            notification_type="REGISTRATION",
            related_object_id=str(registration.id),
            related_object_type="Registration"
        )
        
        serializer = self.get_serializer(registration)
        return Response(serializer.data)

@login_required
def course_registration(request):
    # Lấy danh sách học phần
    courses = Course.objects.all()
    
    # Lấy lịch học của sinh viên
    student = Student.objects.get(user=request.user)
    schedules = Schedule.objects.filter(student=student)
    
    context = {
        'courses': courses,
        'schedules': schedules,
    }
    
    return render(request, 'students/course_registration.html', context)
