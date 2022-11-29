# reviews/models.py

import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        "Название категории",
        max_length=200,
    )
    slug = models.SlugField(
        "slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название жанра",
        max_length=200,
    )
    slug = models.SlugField(
        "slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        "Название произведения",
        max_length=256,
        db_index=True,
    )
    year = models.IntegerField(
        "Год выпуска",
        blank=True,
        validators=[
            MaxValueValidator(
                dt.datetime.now().year,
                message=(
                    'Год выпуска не может быть позже текущего года'
                )
            )
        ]
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Название категории",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Название жанра",
        blank=True,
        db_index=True,
        related_name='titles',
    )
    description = models.CharField(
        "Описание произведения",
        max_length=256,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Произведение",
        ordering = ('-year',)

    def __str__(self):
        return self.name
