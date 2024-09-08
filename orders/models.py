from django.db import models
from django.conf import settings 
import random
import string

class Order(models.Model):
    store = models.ForeignKey('stores.StoreDetails', on_delete=models.CASCADE)  # Connects to StoreDetails
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Connects to CustomUser
    products = models.ManyToManyField('products.Product')  # Adjust based on your product model
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[
        ('received', 'Received'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ])
    order_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            store_name = self.store.store_name
            store_prefix = store_name[:2].upper()
            random_digits = ''.join(random.choices(string.digits, k=6))  # Adjust length as needed
            self.order_id = f"{store_prefix}{random_digits}"
        super().save(*args, **kwargs)


