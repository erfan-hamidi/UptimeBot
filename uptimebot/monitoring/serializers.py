from rest_framework import serializers
from .models import UserProfile, Monitor, MonitorCheck, Alert, Notification


# class MonitorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Monitor
#         fields = ['id', 'name', 'url', 'interval', 'user']

# class CheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id', 'monitor', 'timestamp']

# class CheckResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CheckResult
#         fields = ['id', 'check_instance', 'status_code', 'response_time', 'is_up', 'response_body', 'headers']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'email_verified', 'phone_verified']

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id', 'user', 'name', 'url', 'type', 'interval', 'status', 'last_checked']

class MonitorCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorCheck
        fields = ['id', 'monitor', 'checked_at', 'status_code', 'response_time', 'status', 'error_message']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'monitor', 'alert_type', 'sent_at', 'message']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'alert', 'sent_at', 'read']