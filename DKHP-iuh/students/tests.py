from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student, Registration
from administrators.models import Course
from scheduling.models import Schedule

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='12345678',
            full_name='Student User',
            email='student@example.com',
            phone='+84123456789'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.student_id, '12345678')
        self.assertEqual(self.student.full_name, 'Student User')
        self.assertEqual(self.student.email, 'student@example.com')
        self.assertEqual(self.student.phone, '+84123456789')

    def test_student_str(self):
        self.assertEqual(str(self.student), 'Student User (12345678)')

class RegistrationModelTest(TestCase):
    def setUp(self):
        # Create user and student
        self.user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='12345678',
            full_name='Student User',
            email='student@example.com'
        )
        
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            credits=3
        )
        
        # Create registration
        self.registration = Registration.objects.create(
            student=self.student,
            course=self.course,
            semester='Fall 2023',
            academic_year='2023-2024',
            status='PENDING'
        )

    def test_registration_creation(self):
        self.assertEqual(self.registration.student, self.student)
        self.assertEqual(self.registration.course, self.course)
        self.assertEqual(self.registration.semester, 'Fall 2023')
        self.assertEqual(self.registration.academic_year, '2023-2024')
        self.assertEqual(self.registration.status, 'PENDING')

    def test_registration_str(self):
        expected_str = f"{self.student.full_name} - {self.course.name} (Fall 2023 2023-2024)"
        self.assertEqual(str(self.registration), expected_str)
