from django.urls import path
from .views import (
    RegisterView, 
    VerifyEmailView, 
    ResendCodeView, 
    SetPasswordView, 
    RequestPasswordResetView, 
    ResetPasswordView,
    UserListView,
    ReferenceView,
    StoreDetailsView,
    UpdateStoreProfileView

)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),
    path('set-password/', SetPasswordView.as_view(), name='set_password'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('reference/', ReferenceView.as_view(), name='reference'),
   path('store/<int:pk>/', StoreDetailsView.as_view(), name='store-details'),
    path('stores/<int:store_id>/update/', UpdateStoreProfileView.as_view(), name='update-store-profile'),
]
