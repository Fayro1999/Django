from django.urls import path
from .views import (
    ProductCreateView, ProductListView, ProductUpdateView, ProductDeleteView, 
    ProductDetailView, NewestProductsView, TrendingProductsView, 
    BestSellersInAccessoriesView, MostSearchedProductsView, TopSellingStoresView
)

urlpatterns = [
    path('upload/', ProductCreateView.as_view(), name='product-upload'),
    path('list/', ProductListView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),  # Get a single product
    path('<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    # Additional Views
    path('newest/', NewestProductsView.as_view(), name='newest-products'),
    path('trending/', TrendingProductsView.as_view(), name='trending-products'),
    path('best-sellers/accessories/', BestSellersInAccessoriesView.as_view(), name='best-sellers-accessories'),
    path('most-searched/', MostSearchedProductsView.as_view(), name='most-searched-products'),
    path('top-selling-stores/', TopSellingStoresView.as_view(), name='top-selling-stores'),
]
