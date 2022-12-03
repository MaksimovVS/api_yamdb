from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = 1
    MODERATOR = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )

    confirmation_code = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
