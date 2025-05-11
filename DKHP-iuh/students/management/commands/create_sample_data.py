from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student, Course, Schedule
from datetime import datetime

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho ứng dụng'

    def handle(self, *args, **kwargs):
        # Tạo user và student
        user = User.objects.create_user(
            username='student1',
            password='password123',
            email='student1@example.com'
        )
        
        student = Student.objects.create(
            user=user,
            student_id='SV001',
            full_name='Nguyễn Văn A',
            email='student1@example.com',
            phone='0123456789'
        )

        # Tạo các khóa học
        courses = [
            {
                'code': 'CS101',
                'name': 'Lập trình Python',
                'credits': 3,
                'status': 'open'
            },
            {
                'code': 'CS102',
                'name': 'Cơ sở dữ liệu',
                'credits': 4,
                'status': 'open'
            },
            {
                'code': 'CS103',
                'name': 'Mạng máy tính',
                'credits': 3,
                'status': 'closed'
            }
        ]

        for course_data in courses:
            course = Course.objects.create(**course_data)
            
            # Tạo lịch học cho khóa học đầu tiên
            if course.code == 'CS101':
                Schedule.objects.create(
                    student=student,
                    course=course,
                    time='Thứ 2, 7:00 - 9:00',
                    room='A101'
                )

        self.stdout.write(self.style.SUCCESS('Đã tạo dữ liệu mẫu thành công!')) 