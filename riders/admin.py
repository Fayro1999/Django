from django.contrib import admin
from .models import DispatchRider

class DispatchRiderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'company', 'location', 'is_active', 'is_admin')  # Access user for email
    list_filter = ('is_active', 'is_admin')
    ordering = ('user__email',)  # Order by the email field in the related user model

admin.site.register(DispatchRider, DispatchRiderAdmin)
