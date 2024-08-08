from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartDetailView, AddToCartView, RemoveFromCartView,  CartItemViewSet

router = DefaultRouter()
router.register(r'cart', CartItemViewSet)

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('', include(router.urls)),
    path('cart/<int:pk>/update_quantity/', CartItemViewSet.as_view({'patch': 'update_quantity'})),
]