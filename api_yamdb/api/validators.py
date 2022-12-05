from rest_framework import serializers

from rest_framework.exceptions import ValidationError


class UserNameNotValidValidator:
    requires_context = True

    def __call__(self, attrs, serializer):
        try:
            username = serializer.initial_data["username"]
        except Exception:
            username = None

        if username == "me":
            message = "Зарезервированное имя."
            raise ValidationError(message, code="incorrect_username")
