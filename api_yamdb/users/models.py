# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    )

    email = models.EmailField(
        "email",
        max_length=128,
        unique=True,
    )

    role = models.CharField(
        "Роль",
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER
    )

    bio = models.TextField(
        "Биография",
        blank=True,
        null=True,
    )

    confirmation_code = models.CharField(
        "Проверочный код",
        max_length=25,
        blank=True,
        null=True,
    )
