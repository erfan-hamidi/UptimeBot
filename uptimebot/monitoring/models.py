from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Monitor(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     url = models.URLField()
#     interval = models.IntegerField(help_text="Check interval in minutes")

#     def __str__(self):
#         return self.name

# class Check(models.Model):
#     monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Check for {self.monitor.name} at {self.timestamp}"

# class CheckAlert(models.Model):
#     check_instance = models.ForeignKey('Check', on_delete=models.CASCADE)
#     status_code = models.IntegerField()
#     response_time = models.FloatField(help_text="Response time in seconds")
#     is_up = models.BooleanField()
#     response_body = models.TextField(null=True, blank=True)
#     headers = models.JSONField(null=True, blank=True)

#     def __str__(self):
#         return f"Result for {self.check_instance} - {'Up' if self.is_up else 'Down'}"


# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     sent = models.BooleanField(default=False)

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     monitors = models.ManyToManyField(Monitor, related_name='tags')

#     def __str__(self):
#         return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Monitor(models.Model):
    MONITOR_TYPES = (
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
        ('ping', 'Ping'),
        ('port', 'Port'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()
    type = models.CharField(max_length=10, choices=MONITOR_TYPES)
    interval = models.IntegerField(help_text="Interval in minutes")
    status = models.CharField(max_length=50, default='up')
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class MonitorCheck(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.monitor.name} - {self.checked_at}"

class Alert(models.Model):
    ALERT_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    )

    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.monitor.name} - {self.alert_type}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.alert.message}"