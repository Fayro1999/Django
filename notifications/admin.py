from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'read', 'timestamp')  # Display key fields in the admin list view
    search_fields = ('title', 'message', 'user__email')  # Allow searching by notification title, message, and user email
    list_filter = ('notification_type', 'read', 'timestamp')  # Enable filtering by notification type, read status, and timestamp
    ordering = ('-timestamp',)  # Order by most recent notifications first
    readonly_fields = ('timestamp',)  # Make timestamp read-only since it's auto-generated
    actions = ['mark_as_read', 'mark_as_unread']  # Custom actions for marking notifications

    # Custom action to mark notifications as read
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
        self.message_user(request, "Selected notifications have been marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

    # Custom action to mark notifications as unread
    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
        self.message_user(request, "Selected notifications have been marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"
