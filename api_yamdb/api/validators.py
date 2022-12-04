from rest_framework import serializers


class UserNameNotValidValidator:
    def __init__(self, username):
        self.base = username

    def __call__(self, value):
        if len(self.username) < 4:
            message = "username должен содержать не мение 4 символов"
            raise serializers.ValidationError(message)
