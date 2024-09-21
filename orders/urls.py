from django.urls import path
from .views import CreateOrderView, OrderListView, OrderAuthenticationView,  AssignDeliveryView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('list/', OrderListView.as_view(), name='order-list'),
    path('authenticate-order/', OrderAuthenticationView.as_view(), name='authenticate-order'),
    path('assign-delivery/',  AssignDeliveryView.as_view(), name='assign-delivery'),

]
