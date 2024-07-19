import random
from datetime import datetime, timedelta
from .models import CustomUser

class TokenGenerator:
    def __init__(self, expiration_minutes=10):
        self.expiration_minutes = expiration_minutes

    def make_token(self, user):
        code = ''.join(random.choices('0123456789', k=6))
        expiration_time = datetime.now() + timedelta(minutes=self.expiration_minutes)
        user.verification_code = code
        user.verification_code_expiration = expiration_time
        user.save()
        return code

    def validate_token(self, email, code):
        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == code and user.verification_code_expiration > datetime.now():
                return True
        except CustomUser.DoesNotExist:
            return False
        return False
