from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Monitor, MonitorCheck, Alert, Notification

# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

# Extend the default UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Monitor Admin
@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'url', 'type', 'interval', 'status', 'last_checked')
    list_filter = ('type', 'status', 'user')
    search_fields = ('name', 'url')
    readonly_fields = ('last_checked',)

# MonitorCheck Admin
@admin.register(MonitorCheck)
class MonitorCheckAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'checked_at', 'status_code', 'response_time', 'status')
    list_filter = ('status', 'monitor')
    search_fields = ('monitor__name', 'error_message')
    readonly_fields = ('checked_at',)

# Alert Admin
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'alert_type', 'sent_at', 'message')
    list_filter = ('alert_type', 'monitor')
    search_fields = ('monitor__name', 'message')
    readonly_fields = ('sent_at',)

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert', 'sent_at', 'read')
    list_filter = ('read', 'user')
    search_fields = ('user__username', 'alert__message')
    readonly_fields = ('sent_at',)