# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryDetailViewSet, DeliveryTimeViewSet, PaymentMethodViewSet, InitializePaymentView

router = DefaultRouter()
router.register(r'delivery-details', DeliveryDetailViewSet)
router.register(r'delivery-times', DeliveryTimeViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('initialize-payment/', InitializePaymentView.as_view(), name='initialize-payment'),
]
