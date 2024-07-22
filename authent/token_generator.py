import random
from datetime import datetime, timedelta
from django.utils import timezone

class TokenGenerator:
    def __init__(self, expiration_minutes=10):
        self.expiration_minutes = expiration_minutes
        self.tokens = {}  # This should be replaced with a more secure storage (e.g., a database)

    def make_token(self, user):
        code = ''.join(random.choices('0123456789', k=6))
        expiration_time = timezone.now() + timedelta(minutes=self.expiration_minutes)
        self.tokens[user.email] = (code, expiration_time)
        return code

    def validate_token(self, email, code):
        if email not in self.tokens:
            return False

        stored_code, expiration_time = self.tokens[email]
        if timezone.now() > expiration_time:
            return False

        return stored_code == code

    def get_user_from_token(self, email):
        if email not in self.tokens:
            return None

        code, expiration_time = self.tokens[email]
        if timezone.now() > expiration_time:
            return None

        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
