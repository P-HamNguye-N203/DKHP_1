from django.test import TestCase
from django.contrib.auth.models import User
from scheduling.models import Schedule
from administrators.models import Course, Administrator

class ScheduleModelTest(TestCase):
    def setUp(self):
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            credits=3
        )
        
        # Create administrator (teacher)
        self.user = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='password123'
        )
        self.teacher = Administrator.objects.create(
            user=self.user,
            admin_id='TCH001',
            full_name='Teacher User',
            email='teacher@example.com'
        )
        
        # Create schedule
        self.schedule = Schedule.objects.create(
            course=self.course,
            teacher=self.teacher,
            room='A101',
            day_of_week='MON',
            start_time='08:00:00',
            end_time='10:00:00',
            capacity=30,
            current_enrollment=0,
            semester='Fall 2023',
            academic_year='2023-2024'
        )

    def test_schedule_creation(self):
        self.assertEqual(self.schedule.course, self.course)
        self.assertEqual(self.schedule.teacher, self.teacher)
        self.assertEqual(self.schedule.room, 'A101')
        self.assertEqual(self.schedule.day_of_week, 'MON')
        self.assertEqual(str(self.schedule.start_time), '08:00:00')
        self.assertEqual(str(self.schedule.end_time), '10:00:00')
        self.assertEqual(self.schedule.capacity, 30)
        self.assertEqual(self.schedule.current_enrollment, 0)
        self.assertEqual(self.schedule.semester, 'Fall 2023')
        self.assertEqual(self.schedule.academic_year, '2023-2024')

    def test_schedule_str(self):
        expected_str = f"{self.course.name} - Thứ Hai 08:00:00-10:00:00 (A101)"
        self.assertEqual(str(self.schedule), expected_str)

    def test_is_full(self):
        # Initially not full
        self.assertFalse(self.schedule.is_full())
        
        # Update to full
        self.schedule.current_enrollment = 30
        self.schedule.save()
        self.assertTrue(self.schedule.is_full())
