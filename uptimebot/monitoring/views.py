from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
#from .tasks import perform_check
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .tasks import check_monitor

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]
    print()

    def get_queryset(self):
        return Monitor.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        check_monitor.delay(instance.id)

    @swagger_auto_schema(
        method='post',
        responses={200: 'Pause state updated'},
        operation_description="Toggle the pause state of the specified monitor."
    )

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """
        Toggle the pause state of a monitor.
        """
        monitor = self.get_object()  # Get the monitor instance based on the provided ID
        if monitor.is_paused:
            # Resume the monitor
            monitor.is_paused = False
            monitor.save()

            # Reschedule the monitor check
            check_monitor.apply_async(
                args=[monitor.id],
                countdown=monitor.interval * 60  # Schedule the next check after the interval
            )
            return Response({'status': 'Monitor resumed'}, status=status.HTTP_200_OK)

        else:
            # Pause the monitor
            monitor.is_paused = True
            monitor.save()
            return Response({'status': 'Monitor paused'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        responses={202: 'Check initiated'},
        operation_description="Initiate a check for the specified monitor."
    )
    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        monitor = self.get_object()
        perform_check.delay(monitor.id)
        return Response({'status': 'Check initiated'}, status=status.HTTP_202_ACCEPTED)

class CheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonitorCheck.objects.all()
    serializer_class = MonitorCheckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonitorCheck.objects.filter(monitor__user=self.request.user.id)
    @action(detail=False, methods=['get'], url_path='by-monitor/(?P<monitor_id>[^/.]+)')
    def by_monitor(self, request, monitor_id=None):
        # Validate and filter by monitor_id
        queryset = self.get_queryset().filter(monitor_id=monitor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)        

class CheckAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(monitor__user=self.request.user.id)
