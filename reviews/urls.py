from django.urls import path
from .views import (
    SavedProductListCreateView,
    SavedStoreListCreateView,
    ProductReviewListCreateView,
    StoreReviewListCreateView,
    #SavedProductListCreateView,
    UnsaveProductView,
    CheckSavedProductView,
    #SavedStoreListCreateView,
    UnsaveStoreView, 
    CheckSavedStoreView
)

urlpatterns = [
    path('saved-products/', SavedProductListCreateView.as_view(), name='saved-products'),
    #path("save-product/", SavedProductListCreateView.as_view(), name="save-product"),
    path("unsave-product/<int:product_id>/", UnsaveProductView.as_view(), name="unsave-product"),
    path("save-status/product/<int:product_id>/", CheckSavedProductView.as_view(), name="check-save-product"),

    path('saved-stores/', SavedStoreListCreateView.as_view(), name='saved-stores'),
    #path("save-store/", SavedStoreListCreateView.as_view(), name="save-store"),
    path("unsave-store/<int:store_id>/", UnsaveStoreView.as_view(), name="unsave-store"),
    path("save-status/store/<int:store_id>/", CheckSavedStoreView.as_view(), name="check-save-store"),

    path('products/<int:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('stores/<int:store_id>/reviews/', StoreReviewListCreateView.as_view(), name='store-reviews'),
]
