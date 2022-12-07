# api/validators.py

from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import ValidationError


@deconstructible
class UserNameNotValidValidator:
    def __call__(self, value):
        if value == "me":
            raise ValidationError("1111")
