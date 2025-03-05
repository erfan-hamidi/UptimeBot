from rest_framework import serializers
from .models import UserProfile, Monitor, MonitorCheck, Alert, Notification, AlertType


# class MonitorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Monitor
#         fields = ['id', 'name', 'url', 'interval', 'user']

# class CheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id', 'monitor', 'timestamp']

# class CheckAlertSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CheckAlert
#         fields = ['id', 'check_instance', 'status_code', 'response_time', 'is_up', 'response_body', 'headers']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'email_verified', 'phone_verified']

class MonitorSerializer(serializers.ModelSerializer):
    alert_types = serializers.PrimaryKeyRelatedField(
        queryset=AlertType.objects.all(),
        many=True
    )

    class Meta:
        model = Monitor
        fields = ['id', 'user', 'name', 'url', 'type', 'interval', 'status', 'last_checked', 'is_paused', 'alert_types']
        read_only_fields = ['user', 'status', 'last_checked', 'is_paused'] 

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

class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = ['id', 'name']