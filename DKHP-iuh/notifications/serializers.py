from rest_framework import serializers
from .models import Notification
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class NotificationSerializer(serializers.ModelSerializer):
    recipient_details = UserSerializer(source='recipient', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_details', 'title', 'message',
            'notification_type', 'related_object_id', 'related_object_type',
            'is_read', 'created_at'
        ]
        read_only_fields = ['created_at'] 