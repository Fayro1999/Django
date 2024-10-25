from django.contrib import admin
from .models import DispatchRider

@admin.register(DispatchRider)
class DispatchRiderAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'company', 'location', 'rider_id', 'is_active', 'is_admin')
    search_fields = ('email', 'phone', 'company', 'location', 'rider_id')
    list_filter = ('location', 'is_active', 'is_admin')
    ordering = ('email',)
    readonly_fields = ('rider_id',)  # rider_id is auto-generated, so it's read-only

    # Fields to be displayed when editing a rider
    fieldsets = (
        (None, {
            'fields': ('email', 'phone', 'company', 'location', 'rider_id', 'password', 'is_active', 'is_admin')
        }),
    )

    # Fields to be displayed when adding a new rider
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'company', 'location', 'password', 'is_active', 'is_admin'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle any custom actions when saving.
        """
        obj.save()


