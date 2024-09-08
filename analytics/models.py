from django.db import models
from stores.models import StoreUserProfile
from django.utils import timezone

class StoreVisitor(models.Model):
    store = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    visitor_count = models.PositiveIntegerField(default=0)
    visit_date = models.DateField(default=timezone.now)

class StoreOrder(models.Model):
    store = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    total_orders = models.PositiveIntegerField(default=0)
    order_date = models.DateField(default=timezone.now)

class StoreRevenue(models.Model):
    store = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    revenue_date = models.DateField(default=timezone.now)

class StoreCart(models.Model):
    store = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    cart_count = models.PositiveIntegerField(default=0)
    abandoned_cart_count = models.PositiveIntegerField(default=0)
    cart_date = models.DateField(default=timezone.now)

class VisitorPurchase(models.Model):
    store = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    visitor_count = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField(default=timezone.now)
