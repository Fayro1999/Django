# cart/models.py

from django.db import models
from django.utils import timezone
from products.models import Product
from stores.models import StoreUserProfile

class Cart(models.Model):
    user = models.ForeignKey(StoreUserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this line to store the amount
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.user.email} - {self.product.name}'


