from categories.models import Category
from django.conf import settings
from django.db import models


class Transaction(models.Model):
    """Class representing users transactions."""

    class Meta:
        verbose_name_plural = "transactions"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    datetime = models.DateTimeField(null=False, blank=False)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=False
    )

    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=False,
        blank=False,
    )

    company = models.CharField(null=False, blank=True, max_length=25)

    description = models.TextField(null=False, blank=True)

    def __str__(self):
        return f"{self.category} {self.datetime} {self.amount}"
