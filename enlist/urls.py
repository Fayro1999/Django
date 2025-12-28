"""
URL configuration for enlist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


 # ✅ Adjust this for production
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client  # ✅ Required for OAuth2
    callback_url = "https://django-7u8g.onrender.com/api/auth/google/login/token/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authent/', include('authent.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/', include('allauth.urls')),
     #path('api/auth/social/', include('dj_rest_auth.social_urls')),
    path('api/products/', include('products.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api/cart/', include('cart.urls')),
    path('api/', include('delivery.urls')),
    path('api/stores/', include('stores.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/analytics/', include('analytics.urls')),  # Make sure there is a trailing slash
    path('api/notify/', include('notifications.urls')),
    path('api/dispatch-riders/', include('riders.urls')),
    path('api/', include('store_locations.urls')),
    path('', include('search.urls')),
    path('api/auth/google/login/token/', GoogleLogin.as_view(), name='google_login'),
    path("api/payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


