from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'stock', 'discount_price', 'vendor')  # Include vendor here
    search_fields = ('name', 'vendor__name')  # Enable search by vendor name