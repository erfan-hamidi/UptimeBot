from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
from django.utils import timezone
from .models import Monitor, MonitorCheck  # Replace with actual imports
from your_module import check_monitor  # Replace with actual module name
from .tasks import trigger_alert  # Replace with actual import

class CheckMonitorTestCase(TestCase):
    def setUp(self):
        """Set up common test data."""
        self.monitor_http = Monitor.objects.create(
            id=1,
            type='http',
            url='http://example.com',
            is_paused=False,
            interval=5,
        )
        self.monitor_ping = Monitor.objects.create(
            id=2,
            type='ping',
            url='example.com',
            is_paused=False,
            interval=5,
        )
        self.monitor_port = Monitor.objects.create(
            id=3,
            type='port',
            url='example.com:8080',
            is_paused=False,
            interval=5,
        )

    @patch('your_module.Monitor.objects.get')
    def test_monitor_does_not_exist(self, mock_get):
        """Test that the function exits gracefully if the monitor does not exist."""
        mock_get.side_effect = Monitor.DoesNotExist
        result = check_monitor(999)  # Non-existent monitor ID
        self.assertIsNone(result)

    def test_paused_monitor(self):
        """Test that the function skips checking if the monitor is paused."""
        self.monitor_http.is_paused = True
        self.monitor_http.save()

        with patch('builtins.print') as mock_print:
            check_monitor(1)
            mock_print.assert_called_with("Monitor 1 is paused. Skipping...")

    @patch('your_module.requests.get')
    def test_http_monitor_up(self, mock_requests):
        """Test HTTP monitor when the status code is 200 (up)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_requests.return_value = mock_response

        check_monitor(1)

        # Verify MonitorCheck creation
        check = MonitorCheck.objects.get(monitor=self.monitor_http)
        self.assertEqual(check.status_code, 200)
        self.assertEqual(check.response_time, 0.5)
        self.assertEqual(check.status, 'up')
        self.assertIsNone(check.error_message)

        # Verify monitor status update
        self.monitor_http.refresh_from_db()
        self.assertEqual(self.monitor_http.status, 'up')

    @patch('your_module.os.system')
    def test_ping_monitor_down(self, mock_system):
        """Test ping monitor when the host is unreachable (down)."""
        mock_system.return_value = 1  # Simulate unreachable host

        check_monitor(2)

        # Verify MonitorCheck creation
        check = MonitorCheck.objects.get(monitor=self.monitor_ping)
        self.assertIsNone(check.status_code)
        self.assertIsNone(check.response_time)
        self.assertEqual(check.status, 'down')
        self.assertIsNone(check.error_message)

        # Verify monitor status update
        self.monitor_ping.refresh_from_db()
        self.assertEqual(self.monitor_ping.status, 'down')

    @patch('socket.socket')
    def test_port_monitor_up(self, mock_socket):
        """Test port monitor when the connection is successful (up)."""
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0  # Simulate successful connection
        mock_socket.return_value = mock_sock

        check_monitor(3)

        # Verify MonitorCheck creation
        check = MonitorCheck.objects.get(monitor=self.monitor_port)
        self.assertIsNone(check.status_code)
        self.assertIsNone(check.response_time)
        self.assertEqual(check.status, 'up')
        self.assertIsNone(check.error_message)

        # Verify monitor status update
        self.monitor_port.refresh_from_db()
        self.assertEqual(self.monitor_port.status, 'up')

    @patch('requests.get')
    def test_exception_handling(self, mock_requests):
        """Test exception handling when an error occurs during the check."""
        mock_requests.side_effect = Exception("Connection timeout")

        check_monitor(1)

        # Verify MonitorCheck creation with error message
        check = MonitorCheck.objects.get(monitor=self.monitor_http)
        self.assertIsNone(check.status_code)
        self.assertIsNone(check.response_time)
        self.assertEqual(check.status, 'down')
        self.assertEqual(check.error_message, "Connection timeout")

        # Verify monitor status update
        self.monitor_http.refresh_from_db()
        self.assertEqual(self.monitor_http.status, 'down')

    @patch('trigger_alert.delay')
    @patch('check_monitor.apply_async')
    def test_alert_and_reschedule(self, mock_apply_async, mock_trigger_alert):
        """Test triggering an alert and scheduling the next check."""
        self.monitor_http.status = 'down'
        self.monitor_http.save()

        check_monitor(1)

        # Verify alert was triggered
        mock_trigger_alert.assert_called_once_with(self.monitor_http.id, self.monitor_http.monitorcheck_set.first().id)

        # Verify the next check was scheduled
        mock_apply_async.assert_called_once_with(args=[1], countdown=300)  # 5 minutes in seconds