from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserListView, ReferenceView, ResendCodeView, RequestPasswordResetView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
     path('users/', UserListView.as_view(), name='users'),
      path('reference/', ReferenceView.as_view(), name='reference'),
    path('login/', LoginView.as_view(), name='login'),
     path('resend-code/', ResendCodeView.as_view(), name='resend-code'),
     path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),

]
