from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    @staticmethod
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')