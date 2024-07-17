from django.urls import path
from .views import ProductCreateView, ProductListView

urlpatterns = [
    path('upload/', ProductCreateView.as_view(), name='product-upload'),
     path('list/', ProductListView.as_view(), name='product-list'),
]