from django.contrib import admin
from .models import DeliveryDetail, DeliveryTime, PaymentMethod

@admin.register(DeliveryDetail)
class DeliveryDetailAdmin(admin.ModelAdmin):
    list_display = ('reciever_name', 'reciever_mobile', 'reciver_address')  # Display key fields in the admin list view
    search_fields = ('reciever_name', 'reciever_mobile', 'reciver_address')  # Allow searching by receiver name, mobile, and address
    list_filter = ('reciver_address',)  # Enable filtering by address


@admin.register(DeliveryTime)
class DeliveryTimeAdmin(admin.ModelAdmin):
    list_display = ('delivery_time',)  # Display the delivery time in the list view
    search_fields = ('delivery_time',)  # Allow searching by delivery time


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('payment_method',)  # Display the payment method in the list view
    search_fields = ('payment_method',)  # Allow searching by payment method