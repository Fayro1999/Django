from django.urls import path
from .views import StoreStatisticsView

urlpatterns = [
    path('statistics/<int:store_id>/', StoreStatisticsView.as_view(), name='store-statistics'),
]
