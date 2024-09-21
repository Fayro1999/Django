from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.search_all, name='search_all_api'),  # API endpoint
]
