from django.contrib import admin
from .models import StoreUserProfile, StoreDetails

class StoreDetailsInline(admin.StackedInline):
    model = StoreDetails
    extra = 0
    # Removed created_at and updated_at from readonly_fields
    readonly_fields = []

@admin.register(StoreUserProfile)
class StoreUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Add any fields you want to display in the admin list view
    search_fields = ('user__email', 'user__first_name', 'user__last_name')  # Enable searching by user-related fields
    list_filter = ('groups',)  # Filter by groups if needed
    filter_horizontal = ('groups', 'user_permissions')  # Enable horizontal filter for ManyToMany fields
    raw_id_fields = ('user',)  # Display user as a raw ID field if necessary

    # Add StoreDetails as an inline section
    inlines = [StoreDetailsInline]

    # Customizing the form in the admin interface
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
