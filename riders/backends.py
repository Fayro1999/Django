from django.contrib.auth.backends import ModelBackend
from .models import DispatchRider

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = DispatchRider.objects.get(email=username)
        except DispatchRider.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
