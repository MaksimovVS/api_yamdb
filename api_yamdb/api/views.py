# api/views.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import SignUpSerializer, TokenSerializer
from users.models import User


class SignUpSet(CreateAPIView):

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация на YaMDb',
            f'Здравствуйте, {user.username}! Вы зарегистрировались на YaMDb.ru.\n'
            f'confirmation_code для получения токена:\n{confirmation_code}',
            'registrate@YaMDb.ru',
            (user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenSet(CreateAPIView):

    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.get(username=data['username'])
        token = data['confirmation_code']
        if default_token_generator.check_token(user, token):
            token = RefreshToken.for_user(user).access_token
            return Response({'JWT': str(token)},  status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )
