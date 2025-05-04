from django.urls import path
from .views import (
    RegisterView, 
    VerifyEmailView, 
    ResendCodeView, 
    SetPasswordView, 
    LoginView,
    RequestPasswordResetView, 
    ResetPasswordView,
    UserListView,
    ReferenceView,
    StoreDetailsView,
    UpdateStoreProfileView,
    StoreProfileView,
    IndividualStoreProfileView,
    StoreUserProfileDetailView,
    StoreDetailsListView,
    StoreDetailView,
    StoreDetailUpdateView,
     StoreDetailDeleteView,
     LogoutView


)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),
    path('set-password/', SetPasswordView.as_view(), name='set_password'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('reference/', ReferenceView.as_view(), name='reference'),
   path('store/', StoreDetailsView.as_view(), name='store-details'),
    path('stores/<int:store_id>/update/', UpdateStoreProfileView.as_view(), name='update-store-profile'),
    path('store-profiles/', StoreProfileView.as_view(), name='store-profile-list'),
    path('store-profile/<int:store_id>/', IndividualStoreProfileView.as_view(), name='individual-store-profile'),
    path('store/<int:pk>/', StoreUserProfileDetailView.as_view(), name='store-user-profile-detail'),
    path('storeslist/', StoreDetailsListView.as_view(), name='store-details-list'),
    path('storeslist/<int:id>/', StoreDetailView.as_view(), name='store-detail'),
    path('store-details/<int:id>/update/', StoreDetailUpdateView.as_view(), name='store-detail-update'),
    path('store-details/<int:id>/delete/', StoreDetailDeleteView.as_view(), name='store-detail-delete'),
    path('logout/', LogoutView.as_view(), name='store-logout'), 
]
