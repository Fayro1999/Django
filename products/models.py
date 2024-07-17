from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')  # This field handles the image file

    def __str__(self):
        return self.name