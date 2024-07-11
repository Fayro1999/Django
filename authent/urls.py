from django.urls import path
from .views import RegisterView, SetPasswordView, VerifyEmailView, LoginView, UserListView,  ReferenceView

urlpatterns = [
    path('api/authent/register/', RegisterView.as_view(), name='register'),
    path('api/authent/set-password/', SetPasswordView.as_view(), name='set-password'),
    path('api/authent/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
     path('api/authent/users/', UserListView.as_view(), name='verify-email'),
      path('api/authent/reference/', ReferenceView.as_view(), name='verify-email'),
    path('api/authent/login/', LoginView.as_view(), name='login'),
]
