from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
    interval = models.IntegerField(help_text="Check interval in minutes")

    def __str__(self):
        return self.name

class Check(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check for {self.monitor.name} at {self.timestamp}"

class CheckResult(models.Model):
    check_instance = models.ForeignKey('Check', on_delete=models.CASCADE)
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in seconds")
    is_up = models.BooleanField()
    response_body = models.TextField(null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Result for {self.check_instance} - {'Up' if self.is_up else 'Down'}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monitors = models.ManyToManyField(Monitor, related_name='tags')

    def __str__(self):
        return self.name