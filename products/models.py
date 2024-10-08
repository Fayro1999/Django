from django.db import models
from stores.models import StoreDetails

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')  # This field handles the image file
    vendor = models.ForeignKey(StoreDetails, on_delete=models.CASCADE, related_name='products',  null=True, blank=True)  # Add this line

    def __str__(self):
        return self.name