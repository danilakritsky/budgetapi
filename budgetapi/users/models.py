from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    subscribed = models.BooleanField(
        null=False,
        blank=False,
        default=True
    )