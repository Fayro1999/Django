from django.urls import path
from .views import ProductCreateView, ProductListView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('upload/', ProductCreateView.as_view(), name='product-upload'),
     path('list/', ProductListView.as_view(), name='product-list'),
     path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]