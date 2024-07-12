from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserListView,  ReferenceView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
     path('users/', UserListView.as_view(), name='users'),
      path('reference/', ReferenceView.as_view(), name='reference'),
    path('login/', LoginView.as_view(), name='login'),
]
