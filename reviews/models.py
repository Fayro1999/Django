from django.db import models

# Create your models here.
from django.conf import settings
from products.models import Product
from stores.models import StoreDetails

User = settings.AUTH_USER_MODEL

# Model for saving favorite products
class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user} saved {self.product}"

# Model for saving favorite stores
class SavedStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_stores")
    store = models.ForeignKey(StoreDetails, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'store')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user} saved {self.store}"

# Model for product ratings and reviews
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # One review per user per product

    def __str__(self):
        return f"{self.user} rated {self.product} {self.rating} stars"

# Model for store ratings and reviews
class StoreReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store_reviews")
    store = models.ForeignKey(StoreDetails, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'store')

    def __str__(self):
        return f"{self.user} rated {self.store} {self.rating} stars"
