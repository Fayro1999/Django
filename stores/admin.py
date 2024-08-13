# stores/admin.py
from django.contrib import admin
from .models import StoreUserProfile

@admin.register(StoreUserProfile)
class StoreUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Add any fields you want to display in the admin list view
    search_fields = ('user__email', 'user__first_name', 'user__last_name')  # Enable searching by user-related fields
    list_filter = ('groups',)  # Filter by groups if needed
    filter_horizontal = ('groups', 'user_permissions')  # Enable horizontal filter for ManyToMany fields
    raw_id_fields = ('user',)  # Display user as a raw ID field if necessary

    # If you want to customize the form used in the admin interface
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')  # Optimize queryset by using select_related for the user field
