from rest_framework import serializers
from .models import Monitor, Check, CheckResult

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id', 'name', 'url', 'interval', 'user']

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['id', 'monitor', 'timestamp']

class CheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckResult
        fields = ['id', 'check_instance', 'status_code', 'response_time', 'is_up', 'response_body', 'headers']
