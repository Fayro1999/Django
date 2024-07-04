import hashlib
import random
import string
from datetime import datetime, timedelta

class TokenGenerator:
    def __init__(self, secret_key, expiration_hours=24):
        self.secret_key = secret_key
        self.expiration_hours = expiration_hours

    def make_token(self, user):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        token = hashlib.sha256(f"{user.pk}{user.email}{timestamp}{self.secret_key}".encode()).hexdigest()
        expiration_time = (datetime.now() + timedelta(hours=self.expiration_hours)).strftime("%Y-%m-%d %H:%M:%S")
        return f"{token}:{expiration_time}"

    def validate_token(self, token, user):
        try:
            token, expiration_time = token.split(':')
            expiration_time = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > expiration_time:
                return False

            expected_token = hashlib.sha256(f"{user.pk}{user.email}{expiration_time.strftime('%Y-%m-%d %H:%M:%S')}{self.secret_key}".encode()).hexdigest()
            return expected_token == token
        except Exception as e:
            return False
