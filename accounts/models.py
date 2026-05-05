from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    consentimento_lgpd = models.BooleanField(default=False)
    
    # Campos para recuperação de senha
    recovery_token = models.CharField(max_length=64, blank=True, null=True)
    token_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
    