from django.db import models
from stores.models import StoreDetails

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/') 
    vendor = models.ForeignKey(StoreDetails, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        """Increment product views and save to database"""
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.name
