# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=15, null=False, blank=False,
                                unique=True)
    password = models.CharField(max_length=200, null=False, blank=False,
                                unique=True)
    is_verified = models.BooleanField(null=False, blank=False,
                                      default=False)
