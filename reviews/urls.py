from django.urls import path
from .views import (
    SavedProductListCreateView,
    SavedStoreListCreateView,
    ProductReviewListCreateView,
    StoreReviewListCreateView,
)

urlpatterns = [
    path('saved-products/', SavedProductListCreateView.as_view(), name='saved-products'),
    path('saved-stores/', SavedStoreListCreateView.as_view(), name='saved-stores'),
    path('products/<int:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('stores/<int:store_id>/reviews/', StoreReviewListCreateView.as_view(), name='store-reviews'),
]
