# reviews/models.py

import datetime as dt
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from users.models import User


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
        verbose_name_plural = "Категории"

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
        verbose_name_plural = "Жанры"

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
                message=("Год выпуска не может быть позже текущего года"),
            )
        ],
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Название категории",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Название жанра",
        blank=True,
        db_index=True,
        related_name="titles",
    )
    description = models.CharField(
        "Описание произведения",
        max_length=256,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("-year",)

    def __str__(self):
        return self.name


class DatePub(models.Model):

    pub_date = models.DateTimeField(
                auto_now_add=True,
                db_index=True,
                verbose_name="Дата добавления"
    )

    class Meta:
        abstract = True


class Review(DatePub):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="reviews", verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст отзыва"
    )
    score = models.PositiveIntegerField(
        "Оценка",
        validators=[
            MaxValueValidator(10, "Максимальная оценка - 10"),
            MinValueValidator(1, "Минимальная оценка - 1"),
        ],
        error_messages={"validators": "Оценка от 1 до 10."},
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="unique_review",
            )
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


class Comment(DatePub):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments", verbose_name="Автор",
    )

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments", verbose_name="Отзыв",
    )
    text = models.TextField(
        verbose_name=" Текст комментария"
    )
    
    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"

    def __str__(self):
        return self.text
