from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
     phone=models.CharField(max_length=15)
     verification_code = models.CharField(max_length=6, null=True, blank=True)
     verification_code_expiration = models.DateTimeField(null=True, blank=True)
   
    

