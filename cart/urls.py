# cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:store_id>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('getcart/', views.get_cart, name='get-cart'),
    # Include other cart-related URLs if necessary
]

