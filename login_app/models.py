from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user model:
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    password = models.CharField(max_length=200)
    earning = models.IntegerField(null=True, default=0)
    spending = models.IntegerField(null=True, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
