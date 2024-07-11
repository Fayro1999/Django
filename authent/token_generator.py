import hashlib
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser

class TokenGenerator:
    def __init__(self, secret_key, expiration_hours=24):
        self.secret_key = secret_key
        self.expiration_hours = expiration_hours

    def make_token(self, user):
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        token = hashlib.sha256(f"{user.pk}{user.email}{timestamp}{self.secret_key}".encode()).hexdigest()
        expiration_time = (timezone.now() + timedelta(hours=self.expiration_hours)).strftime("%Y-%m-%d %H:%M:%S")
        return f"{token}:{expiration_time}"

    def validate_token(self, token, user):
        try:
            token, expiration_time = token.split(':')
            expiration_time = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S")
            if timezone.now() > expiration_time:
                return False

            expected_token = hashlib.sha256(f"{user.pk}{user.email}{expiration_time.strftime('%Y-%m-%d %H:%M:%S')}{self.secret_key}".encode()).hexdigest()
            return expected_token == token
        except Exception as e:
            return False

    def get_user_from_token(self, token):
        try:
            token, _ = token.split(':')
            user_id = int(token[:8], 16)  # Extract user ID (assuming the first 8 chars of the token is the user ID in hex)
            return CustomUser.objects.get(pk=user_id)
        except (ValueError, ObjectDoesNotExist):
            return None
