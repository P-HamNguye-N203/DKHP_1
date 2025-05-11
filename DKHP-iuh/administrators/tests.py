from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Administrator

# Create your tests here.

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            credits=3,
            description='Basic programming concepts'
        )

    def test_course_creation(self):
        self.assertEqual(self.course.code, 'CS101')
        self.assertEqual(self.course.name, 'Introduction to Programming')
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.description, 'Basic programming concepts')

    def test_course_str(self):
        self.assertEqual(str(self.course), 'CS101 - Introduction to Programming')

class AdministratorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.admin = Administrator.objects.create(
            user=self.user,
            admin_id='ADM001',
            full_name='Admin User',
            email='admin@example.com',
            phone_number='+84123456789'
        )

    def test_administrator_creation(self):
        self.assertEqual(self.admin.admin_id, 'ADM001')
        self.assertEqual(self.admin.full_name, 'Admin User')
        self.assertEqual(self.admin.email, 'admin@example.com')
        self.assertEqual(self.admin.phone_number, '+84123456789')

    def test_administrator_str(self):
        self.assertEqual(str(self.admin), 'Admin User (ADM001)')
