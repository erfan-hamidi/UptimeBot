from celery import shared_task
import requests
from .models import Monitor, Check, CheckResult
from django.utils import timezone

@shared_task
def perform_check(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    check = Check.objects.create(monitor=monitor)
    
    try:
        response = requests.get(monitor.url, timeout=10)
        is_up = response.status_code == 200
        CheckResult.objects.create(
            check=check,
            status_code=response.status_code,
            response_time=response.elapsed.total_seconds(),
            is_up=is_up,
            response_body=response.text[:500],  # Limiting the response body size
            headers=dict(response.headers)
        )
    except requests.RequestException as e:
        CheckResult.objects.create(
            check=check,
            status_code=0,
            response_time=0,
            is_up=False,
            response_body=str(e),
            headers={}
        )

@shared_task
def perform_checks():
    monitors = Monitor.objects.all()
    for monitor in monitors:
        perform_check.delay(monitor.id)
