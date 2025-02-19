# 
from celery import shared_task
from celery.schedules import crontab
#from celery import periodic_task
from django.utils import timezone
from .models import Monitor, MonitorCheck
import requests
import socket
import os

@shared_task
def check_monitor(monitor_id):
    """
    Task to check the status of a single monitor.
    """
    try:
        monitor = Monitor.objects.get(id=monitor_id)
    except Monitor.DoesNotExist:
        return

    # Check if the monitor is paused
    if monitor.is_paused:
        print(f"Monitor {monitor_id} is paused. Skipping...")
        return

    status_code = None
    response_time = None
    error_message = None
    status = 'down'

    try:
        if monitor.type in ['http', 'https']:
            # HTTP/HTTPS Monitor
            url = monitor.url
            if monitor.type == 'https':
                url = url.replace('http://', 'https://', 1)  # Ensure HTTPS
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            response_time = response.elapsed.total_seconds()
            status = 'up' if status_code == 200 else 'down'

        elif monitor.type == 'ping':
            # Ping Monitor
            host = monitor.url.split('/')[2] if '/' in monitor.url else monitor.url  # Extract hostname/IP
            response = os.system(f"ping -c 1 -W 2 {host}")  # Send one ICMP packet with 2-second timeout
            status = 'up' if response == 0 else 'down'

        elif monitor.type == 'port':
            # Port Monitor
            parts = monitor.url.split(':')
            if len(parts) != 2:
                raise ValueError("Invalid URL format for port monitoring. Use 'hostname:port'.")
            host, port = parts[0], int(parts[1])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5-second timeout
            result = sock.connect_ex((host, port))
            sock.close()
            status = 'up' if result == 0 else 'down'

    except Exception as e:
        # Handle errors (e.g., timeout, connection error)
        error_message = str(e)

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

    print(f"Monitor {monitor_id} status: {status}")

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