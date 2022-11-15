import datetime
import random

from categories.models import DEFAULT_CATEGORIES, Category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction


class User(AbstractUser):
    subscribed = models.BooleanField(null=False, blank=False, default=True)


@receiver(post_save, sender=User)
def add_new_user_categories(instance, created, **kwargs):
    """Create default categories when a new user is created."""
    if created and not instance.is_superuser:
        Category.objects.bulk_create(
            [
                Category(category_name=category, user=instance)
                for category in DEFAULT_CATEGORIES
            ]
        )
    # create a testuser after first superuser has been created
    elif User.objects.all().count() == 1:
        # generating test data
        user = User(
            username="testuser",
            password="testuser",
            email="testuser@example.com",
        )
        user.save()  # categories are generated automatically
        categories = Category.objects.filter(user=user)
        for transaction_num in range(1, 20):
            Transaction(
                user=user,
                amount=random.randint(-1000, 1000) + random.random(),
                category=random.choice(categories),
                company=f"Company {random.randint(1, 5)}",
                datetime=(
                    datetime.datetime.now()
                    + datetime.timedelta(
                        hours=random.randint(-12, 12),
                        minutes=random.randint(0, 59),
                        seconds=random.randint(0, 59),
                        days=(
                            random.randint(-594, 0)
                            if transaction_num > 3
                            else random.randint(
                                -datetime.date.today().weekday(), 0
                            )
                        ),
                    )
                ),
            ).save()
