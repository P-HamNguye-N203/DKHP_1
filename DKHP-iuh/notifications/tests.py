from django.test import TestCase
from django.contrib.auth.models import User
from notifications.models import Notification, NotificationPreference

class NotificationModelTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password123'
        )
        
        # Create notification
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='SYSTEM',
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.recipient, self.user)
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.message, 'This is a test notification')
        self.assertEqual(self.notification.notification_type, 'SYSTEM')
        self.assertFalse(self.notification.is_read)

    def test_notification_str(self):
        self.assertEqual(str(self.notification), 'Test Notification - user')

class NotificationPreferenceModelTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password123'
        )
        
        # Create notification preference
        self.preference = NotificationPreference.objects.create(
            user=self.user,
            email_notifications=True,
            sms_notifications=False,
            registration_notifications=True,
            schedule_notifications=True,
            grade_notifications=True,
            system_notifications=True
        )

    def test_preference_creation(self):
        self.assertEqual(self.preference.user, self.user)
        self.assertTrue(self.preference.email_notifications)
        self.assertFalse(self.preference.sms_notifications)
        self.assertTrue(self.preference.registration_notifications)
        self.assertTrue(self.preference.schedule_notifications)
        self.assertTrue(self.preference.grade_notifications)
        self.assertTrue(self.preference.system_notifications)

    def test_preference_str(self):
        self.assertEqual(str(self.preference), 'Notification Preferences for user')
