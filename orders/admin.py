from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'store', 'amount', 'status', 'date')  # Display order details in list view
    search_fields = ('order_id', 'user__email', 'store__store_name')  # Enable searching by order ID, user email, and store name
    list_filter = ('status', 'store', 'date')  # Filter by status, store, and date
    ordering = ('-date',)  # Orders will be listed by most recent first
    readonly_fields = ('order_id', 'date')  # order_id and date are auto-generated, so make them read-only
    filter_horizontal = ('products',)  # Better UI for selecting many-to-many products

    fieldsets = (
        (None, {
            'fields': ('order_id', 'user', 'store', 'products', 'quantity', 'amount', 'status', 'delivery', 'date')
        }),
    )

    # Override save_model to ensure custom actions, if needed
    def save_model(self, request, obj, form, change):
        obj.save()

    # Custom admin action to mark orders as completed
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected orders have been marked as completed.")
    mark_as_completed.short_description = "Mark selected orders as completed"
