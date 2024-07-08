from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserListView, ReferenceView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('reference/', ReferenceView.as_view(), name='reference'),
]
