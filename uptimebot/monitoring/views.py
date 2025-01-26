from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
#from .tasks import perform_check
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Monitor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        return Check.objects.filter(monitor__user=self.request.user)

class CheckResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CheckResult.objects.filter(check_instance__monitor__user=self.request.user)
