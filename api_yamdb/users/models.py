# users/models.py

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.validators import UsernameValidator


class User(AbstractUser):

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(), UsernameValidator())
    )

    email = models.EmailField(
        "email",
        max_length=254,
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

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
