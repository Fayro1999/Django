# payments/urls.py
from django.urls import path
from .views import OpenVirtualAccount, TransferFundsView, VerifyAccountView, GetAccountBalance

urlpatterns = [
    path("open-virtual-account/", OpenVirtualAccount.as_view(), name="open-virtual-account"),
    path("transfer/", TransferFundsView.as_view(), name="transfer-funds"),
    path("verify-account/", VerifyAccountView.as_view(), name="verify-account"),
    path("get-balance/", GetAccountBalance.as_view(), name="get-balance"),

]
