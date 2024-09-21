from django.urls import path
from .views import RegisterDispatchRiderView, LoginDispatchRiderView, ListDispatchRidersView,  RiderResponseView

urlpatterns = [
    path('register/', RegisterDispatchRiderView.as_view(), name='register-dispatch-rider'),
    path('login/', LoginDispatchRiderView.as_view(), name='login-dispatch-rider'),
    path('list/', ListDispatchRidersView.as_view(), name='list-dispatch-riders'),
    path('rider-response', RiderResponseView.as_view(), name='rider-response'),
]

