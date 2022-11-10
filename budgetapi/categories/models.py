from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models

DEFAULT_CATEGORIES: list[str] = [
    "Забота о себе",
    "Зарплата",
    "Здоровье и фитнес",
    "Кафе и рестораны",
    "Машина",
    "Образование",
    "Отдых и развлечения",
    "Платежи, комиссии",
    "Покупки: одежда, техника",
    "Продукты",
    "Проезд",
]


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.user} {self.category_name}'

