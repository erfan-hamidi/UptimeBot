from urllib.parse import urlparse
from celery import shared_task
from celery.schedules import crontab
#from celery import periodic_task
from django.utils import timezone
from .models import Monitor, MonitorCheck, Alert,AlertType
import requests
import socket
import os, logging
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def check_monitor(monitor_id):
    try:
        monitor = Monitor.objects.get(id=monitor_id)
    except Monitor.DoesNotExist:
        return

    # Check if the monitor is paused
    if monitor.is_paused:
        print(f"Monitor {monitor.url} is paused. Skipping...")
        return

    status_code = None
    response_time = None
    error_message = None
    status = 'down'

    try:
        if monitor.type in ['http', 'https']:
            url = monitor.url.replace('http://', 'https://', 1) if monitor.type == 'https' else monitor.url
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
            parsed_url = urlparse(monitor.url)
            ports = parsed_url.netloc.split(':')
            parts= list(ports)
            if len(parts) != 2:
                raise ValueError("Invalid URL format for port monitoring. Use 'hostname:port'.")
            host, port = parts[0], int(parts[1])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            status = 'up' if result == 0 else 'down'

    except Exception as e:
        # Handle errors (e.g., timeout, connection error)
        error_message = str(e)

    # Create a MonitorCheck record
    check = MonitorCheck.objects.create(
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

    print(f"Monitor {monitor.url} status: {status}")

    # Trigger alert if the monitor is down
    if status == 'down':
        trigger_alert.delay(monitor.id, check.id)  # Queue the alert task

    # Schedule the next check
    check_monitor.apply_async(args=[monitor_id], countdown=monitor.interval * 60)

@shared_task
def start_monitor_tasks():
    """
    Task to start monitoring tasks for all monitors.
    """
    monitors = Monitor.objects.all()
    for monitor in monitors:
        check_monitor.delay(monitor.id)  # Start the monitoring task for each monitor


logger = logging.getLogger(__name__)

@shared_task
def trigger_alert(monitor_id, check):
    try:
        monitor = Monitor.objects.get(id=monitor_id)
        monitorcheck = MonitorCheck.objects.get(id=check)
    except Monitor.DoesNotExist:
        logger.error(f"Monitor {monitor_id} does not exist.")
        return
    # Build the alert message
    message = (
        f"Monitor '{monitor.name}' is DOWN!\n"
        f"URL: {monitor.url}\n"
        f"Status: {monitor.status}\n"
        f"Status Code: {monitorcheck.status_code}\n"
        f"Last Checked: {monitor.last_checked}\n"
        #f"Error: {monitorcheck.error_message if hasattr(monitor, 'last_check') else 'N/A'}"
    )

    # Iterate through all alert types associated with the monitor
    for alert_type in monitor.alert_types.all():
        try:
            if alert_type.name == 'alertemail':
                # Send an email alert
                send_email_alert(monitor, message)

            # elif alert_type.name == 'alertsms':
            #     # Send an SMS alert (requires integration with an SMS gateway)
            #     send_sms_alert(monitor, message)

            # elif alert_type.name == 'alertphone':
            #     # Trigger a webhook alert (requires integration with a webhook service)
            #     trigger__alert(monitor, message)

            # Create an alert record for this specific alert type
            Alert.objects.create(
                monitor=monitor,
                alert_type=alert_type,
                message=message,
            )
        except Exception as e:
            logger.error(f"Failed to send {alert_type.name} alert for monitor {monitor_id}: {str(e)}")


def send_email_alert(monitor, message):
    send_mail(
        subject=f"ALERT: {monitor.name} is DOWN",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[monitor.user.email],  # Send to the user's email
        fail_silently=False,
    )
    logger.info(f"Email alert sent for monitor {monitor.id}.")