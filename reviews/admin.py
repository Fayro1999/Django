from django.contrib import admin

# Register your models here.
from .models import SavedProduct, SavedStore, ProductReview, StoreReview

admin.site.register(SavedProduct)
admin.site.register(SavedStore)
admin.site.register(ProductReview)
admin.site.register(StoreReview)
