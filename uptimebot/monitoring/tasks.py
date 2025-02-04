# 
from celery import shared_task
from celery.schedules import crontab
#from celery import periodic_task
from django.utils import timezone
from .models import Monitor, MonitorCheck
import requests

@shared_task
def check_monitor(monitor_id):
    """
    Task to check the status of a single monitor.
    """
    try:
        monitor = Monitor.objects.get(id=monitor_id)
    except Monitor.DoesNotExist:
        return

    try:
        # Simulate checking the status of the monitor
        response = requests.get(monitor.url, timeout=10)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()
        status = 'up' if status_code == 200 else 'down'
    except requests.RequestException as e:
        # Handle errors (e.g., timeout, connection error)
        status_code = None
        response_time = None
        status = 'down'
        error_message = str(e)
    else:
        error_message = None

    # Create a MonitorCheck record
    MonitorCheck.objects.create(
        monitor=monitor,
        status_code=status_code,
        response_time=response_time,
        status=status,
        error_message=error_message,
    )

    # Update the monitor's last_checked field
    monitor.last_checked = timezone.now()
    monitor.status = status
    monitor.save()
    print(status)
    # Schedule the task to run again after the monitor's interval
    check_monitor.apply_async(args=[monitor_id], countdown=monitor.interval * 60)  # Convert minutes to seconds

@shared_task
def start_monitor_tasks():
    """
    Task to start monitoring tasks for all monitors.
    """
    monitors = Monitor.objects.all()
    for monitor in monitors:
        check_monitor.delay(monitor.id)  # Start the monitoring task for each monitor



@shared_task
def trigger_alert(monitor_id):
    """
    Task to trigger an alert if a monitor is down.
    """
    from .models import Monitor, Alert
    monitor = Monitor.objects.get(id=monitor_id)
    message = f"Monitor {monitor.name} is down!"
    Alert.objects.create(
        monitor=monitor,
        alert_type='email',  # You can customize this #TODO
        message=message,
    )