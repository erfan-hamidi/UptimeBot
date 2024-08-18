from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'monitors', views.MonitorViewSet)
router.register(r'checks', views.CheckViewSet)
router.register(r'check-results', views.CheckResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
