# reviews/models.py

import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        "Название категории",
        max_length=200
    )
    slug = models.SlugField(
        "slug",
        unique=True
    )

    class Meta:
        verbose_name = "Категория"

    def __str__(self):
        return self.name
