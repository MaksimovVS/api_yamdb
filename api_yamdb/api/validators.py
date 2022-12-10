# api/validators.py

from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import ValidationError


@deconstructible
class UsernameValidator:

    def __call__(self, username):
        if username.lower() == "me":
            raise ValidationError("Invalid username")
