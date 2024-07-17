from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]