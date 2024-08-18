# monitoring/admin.py

from django.contrib import admin
from .models import Monitor, Check, CheckResult, Notification, Tag

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user', 'interval')
    list_filter = ('user', 'interval')
    search_fields = ('name', 'url')

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'timestamp')
    list_filter = ('monitor', 'timestamp')
    search_fields = ('monitor__name',)

@admin.register(CheckResult)
class CheckResultAdmin(admin.ModelAdmin):
    list_display = ('check_instance', 'status_code', 'response_time', 'is_up')
    list_filter = ('is_up', 'status_code')
    search_fields = ('check_instance__monitor__name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'monitor', 'message', 'timestamp', 'sent')
    list_filter = ('user', 'monitor', 'sent')
    search_fields = ('user__username', 'monitor__name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
