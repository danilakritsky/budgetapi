from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from categories.models import DEFAULT_CATEGORIES, Category

class User(AbstractUser):
    subscribed = models.BooleanField(
        null=False,
        blank=False,
        default=True
    )

@receiver(post_save, sender=User)
def add_new_user_categories(instance, created, **kwargs):
    """Create default categories when a new user is created."""
    if created:
        Category.objects.bulk_create(
            [
                Category(category_name=category, user=instance)
                for category in DEFAULT_CATEGORIES
            ]
        )
